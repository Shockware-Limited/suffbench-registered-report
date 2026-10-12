"""Build pilot arms for one mined instance (HANDOFF-pilot-haiku.md §6).

Arms: A0 (task only), W, A1=W+iface(deps), A1b=W+bodies(deps), A1F=A1+iface(F)+test names, P32/P64/P128/P200 = A1
padded (before A1) with same-module packages outside W∪B∪F not sharing a parent dir with W, ordered by
sha1(instance_id+path). Token targets measured with messages.count_tokens on the full message using --model.
Writes <out>/contexts.json with per-arm file, chars, n_tokens_prompt (for --model), expressible, missing_identifiers.
"""
import argparse, json, os, re, sys, hashlib, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_mutation import run, GO, load_packages, build_graph
from build_contexts import go_doc_all, read_files, serialise
from pilot_mine import code_tokens, added_lines
import anthropic

SYSTEM = open(os.path.join(os.path.dirname(__file__), "SYSTEM_PROMPT.txt"), encoding="utf-8").read()
LEVELS = {"P32": 32000, "P64": 64000, "P128": 128000, "P200": 198000}

def make_client(inst):
    key = open(os.path.expanduser(inst.get("api_key_file", "~/.config/context-sufficiency-note/anthropic.key")), encoding="utf-8-sig").read().strip()
    for v in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"): os.environ.pop(v, None)
    return anthropic.Anthropic(api_key=key, base_url="https://api.anthropic.com", max_retries=3)

def messages_for(ctx_text, task_text):
    if not ctx_text:
        return [{"role": "user", "content": [{"type": "text", "text": "TASK\n\n" + task_text + "\n\nProduce the SEARCH/REPLACE blocks now."}]}]
    return [{"role": "user", "content": [
        {"type": "text", "text": "REPOSITORY CONTEXT\n\n" + ctx_text, "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "TASK\n\n" + task_text + "\n\nProduce the SEARCH/REPLACE blocks now."}]}]

def count(client, model, ctx_text, task_text):
    return client.messages.count_tokens(model=model, system=SYSTEM, messages=messages_for(ctx_text, task_text)).input_tokens

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--out", required=True); ap.add_argument("--model", default="claude-haiku-5-5")
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8")); repo = inst["repo_path"]
    run(["git", "checkout", "-q", "-f", inst["base_commit"]], repo); run(["git", "clean", "-fdq"], repo)
    pk, mod = load_packages(repo); deps, tdeps, fwd = build_graph(pk, mod)
    W = inst["write_set"]; rel = lambda p: os.path.relpath(p, repo).replace("\\", "/")
    def pkg_src(p): o = pk[p]; return [(rel(x), t) for x, t in read_files(o["Dir"], o.get("GoFiles", []))]
    def test_names(p):
        o = pk[p]; names = []
        for _, t in read_files(o["Dir"], o.get("TestGoFiles", []) + o.get("XTestGoFiles", [])): names += re.findall(r"^func (Test\w+)", t, re.M)
        return names
    direct = sorted({d for w in W for d in pk[w].get("Imports", []) if d in pk and d not in W})
    B = sorted(set().union(*[deps[w] for w in W]) - set(W)); F = sorted(set().union(*[fwd[w] for w in W]) - set(W))
    w_blocks = [b for w in W for b in pkg_src(w)]
    a1 = [(f"{d} (exported API)", go_doc_all(repo, d)) for d in direct] + w_blocks
    a1f = [(f"{d} (exported API)", go_doc_all(repo, d)) for d in direct] + \
          [(f"{f} (dependent package: exported API)", go_doc_all(repo, f) + "\n// tests: " + ", ".join(test_names(f))) for f in F] + w_blocks
    arms = {"A0": [], "W": w_blocks, "A1": a1, "A1b": [b for d in direct for b in pkg_src(d)] + w_blocks, "A1F": a1f}
    # padding pool
    wdirs = {os.path.dirname(pk[w]["Dir"]) for w in W}
    pool = [p for p in pk if p not in W and p not in B and p not in F and os.path.dirname(pk[p]["Dir"]) not in wdirs and pk[p].get("GoFiles")]
    pool.sort(key=lambda p: hashlib.sha1((inst["instance_id"] + p).encode()).hexdigest())
    client = make_client(inst); task = inst["task_text"]
    a1_text = serialise(a1); base_tokens = count(client, a.model, a1_text, task)
    pad_text = ""; pad_pkgs = []; pi = 0
    for name, target in LEVELS.items():
        if base_tokens > target: arms[name] = None; continue
        # grow the pad until the whole message exceeds the target, then trim at a line boundary
        while pi < len(pool):
            txt = serialise(pad_text and [("pad", pad_text)] or []) if False else None
            full = count(client, a.model, pad_text + a1_text, task) if pad_text else base_tokens
            if full >= target: break
            p = pool[pi]; pi += 1; blk = serialise(pkg_src(p)) + "\n"; pad_text += blk; pad_pkgs.append(p)
        full = count(client, a.model, pad_text + a1_text, task)
        if full < target * 0.98: arms[name] = None; continue
        cpt = len(pad_text) / max(1, full - base_tokens)
        cut = pad_text
        for _ in range(4):
            over = count(client, a.model, cut + a1_text, task) - target
            if abs(over) <= target * 0.02: break
            keep = max(0, len(cut) - int(over * cpt)); cut = cut[:cut.rfind("\n", 0, keep) + 1] if over > 0 else pad_text[:min(len(pad_text), len(cut) + int(-over * cpt))]
        arms[name] = ("PAD", cut + a1_text, pad_pkgs[:])
    gold_ids = set()
    for l in added_lines(inst["gold_patch"], False): gold_ids |= code_tokens(l, False)[0]
    os.makedirs(a.out, exist_ok=True)
    meta = {"write_set": W, "direct_deps": direct, "backward_slice": B, "forward_slice": F, "gold_identifiers": sorted(gold_ids), "count_model": a.model, "arms": {}}
    for name, blocks in arms.items():
        if blocks is None: meta["arms"][name] = {"skipped": "base exceeds level or pool exhausted"}; print(name, "skipped"); continue
        if isinstance(blocks, tuple): text, pads = blocks[1], blocks[2]
        else: text, pads = serialise(blocks), []
        fn = name + ".txt"; open(os.path.join(a.out, fn), "w", encoding="utf-8", newline="\n").write(text)
        missing = [i for i in sorted(gold_ids) if i not in text] if name != "A0" else sorted(gold_ids)
        nt = count(client, a.model, text, task)
        meta["arms"][name] = {"file": fn, "chars": len(text), "n_tokens_prompt": nt, "expressible": not missing, "missing_identifiers": missing, "pad_pkgs": pads}
        print(f"{name:5s} tokens={nt:7d} chars={len(text):9,d} expressible={not missing} missing={missing[:6]}", flush=True)
    json.dump(meta, open(os.path.join(a.out, "contexts.json"), "w", encoding="utf-8"), indent=1)

if __name__ == "__main__":
    main()
