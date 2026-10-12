"""Build ablation arms for one instance (preregistration H5).

Arms: W, A1 (rebuilt; checked against the pilot's A1.txt), A1-<i> = A1 minus the interface of direct dep i
(grouped into <=16 contiguous groups when there are more than 16 deps), A1g = W + interfaces of deps referenced by
the gold patch (oracle predictor), A1t = W + interfaces of deps referenced by the task text (inference-time predictor).
Arms whose text equals another arm's are not written; metadata records same_as.
Writes <out>/contexts.json compatible with pilot_run.py.
"""
import argparse, json, os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_mutation import run, load_packages, build_graph
from build_contexts import go_doc_all, read_files, serialise
from pilot_mine import code_tokens, added_lines
from pilot_contexts import make_client, count
from run_instance import resolve_repo

MAX_GROUPS = 16
SELECTOR = re.compile(r"\b([A-Za-z_]\w*)\.([A-Z]\w*)")
WORD = re.compile(r"[A-Za-z_]\w*")
DECL = re.compile(r"^(?:func (?:\([^)]*\) )?|type |var |const |\t)([A-Z]\w*)", re.M)

def default_name(pkg):
    seg = pkg.rstrip("/").split("/")
    return seg[-2] if re.fullmatch(r"v\d+", seg[-1]) and len(seg) > 1 else seg[-1]

def import_aliases(files):
    """pkg path -> set of aliases used across the given Go sources (default name when unaliased)."""
    out = {}
    for _, text in files:
        for m in re.finditer(r'^\s*(?:([A-Za-z_]\w*|\.)\s+)?"([^"]+)"\s*$', text, re.M):
            alias, path = m.group(1), m.group(2)
            out.setdefault(path, set()).add(alias or default_name(path))
    return out

def referenced(text_lines, deps, aliases, exports):
    """deps whose (alias, Exported) selector appears in the lines; ambiguous aliases resolve by export membership.
    A selector through a variable (v.Method) counts when Method is exported by exactly one dep."""
    hits = {}
    for line in text_lines:
        for alias, name in SELECTOR.findall(line):
            cands = [d for d in deps if alias in aliases.get(d, {default_name(d)})]
            if len(cands) > 1: cands = [d for d in cands if name in exports[d]] or cands
            if not cands:
                owners = [d for d in deps if name in exports[d]]
                if len(owners) == 1: hits.setdefault(owners[0], set()).add(f"member:{alias}.{name}")
                continue
            for d in cands: hits.setdefault(d, set()).add(f"{alias}.{name}")
    return hits

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--pilot-contexts"); ap.add_argument("--model", default="claude-haiku-5-5")
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8")); repo = resolve_repo(inst["repo_path"])
    run(["git", "checkout", "-q", "-f", inst["base_commit"]], repo); run(["git", "clean", "-fdq"], repo)
    pk, mod = load_packages(repo); deps, tdeps, fwd = build_graph(pk, mod)
    W = inst["write_set"]; rel = lambda p: os.path.relpath(p, repo).replace("\\", "/")
    def pkg_src(p): o = pk[p]; return [(rel(x), t) for x, t in read_files(o["Dir"], o.get("GoFiles", []))]
    direct = sorted({d for w in W for d in pk[w].get("Imports", []) if d in pk and d not in W})
    F = sorted(set().union(*[fwd[w] for w in W]) - set(W))
    w_blocks = [b for w in W for b in pkg_src(w)]
    docs = {d: go_doc_all(repo, d) for d in direct}
    exports = {d: set(DECL.findall(docs[d])) for d in direct}
    aliases = import_aliases(w_blocks)
    dep_blocks = [(f"{d} (exported API)", docs[d]) for d in direct]
    a1_text = serialise(dep_blocks + w_blocks); w_text = serialise(w_blocks)
    a1_matches = None
    if a.pilot_contexts and os.path.exists(os.path.join(a.pilot_contexts, "A1.txt")):
        a1_matches = open(os.path.join(a.pilot_contexts, "A1.txt"), encoding="utf-8").read() == a1_text
    gold_lines = list(added_lines(inst["gold_patch"], False))
    gold_ids = set()
    for l in gold_lines: gold_ids |= code_tokens(l, False)[0]
    gold_ref = referenced(gold_lines, direct, aliases, exports)
    task = inst["task_text"]; task_words = set(WORD.findall(task))
    task_ref = referenced(task.splitlines(), direct, aliases, exports)
    name_owner = {}
    for d in direct:
        for n in exports[d]:
            if len(n) >= 6: name_owner.setdefault(n, []).append(d)
    for d in direct:
        nm = default_name(d)
        if len(nm) >= 4 and nm in task_words: task_ref.setdefault(d, set()).add(f"pkgname:{nm}")
        for n in exports[d]:
            if len(n) >= 6 and n in task_words and name_owner.get(n) == [d]: task_ref.setdefault(d, set()).add(f"ident:{n}")
    # groups for leave-one-out
    if len(direct) <= MAX_GROUPS: groups = [[d] for d in direct]
    else:
        n = len(direct); groups = [direct[i * n // MAX_GROUPS:(i + 1) * n // MAX_GROUPS] for i in range(MAX_GROUPS)]
    arms = {"W": (w_text, {}), "A1": (a1_text, {})}
    for i, g in enumerate(groups):
        keep = [b for d, b in zip(direct, dep_blocks) if d not in g]
        arms[f"A1-{i:02d}"] = (serialise(keep + w_blocks), {"removed": g})
    for name, ref in (("A1g", gold_ref), ("A1t", task_ref)):
        keep = [b for d, b in zip(direct, dep_blocks) if d in ref]
        arms[name] = (serialise(keep + w_blocks), {"kept": sorted(ref), "evidence": {d: sorted(v) for d, v in ref.items()}})
    client = make_client(inst); os.makedirs(a.out, exist_ok=True)
    meta = {"write_set": W, "direct_deps": direct, "forward_slice": F, "groups": groups, "gold_identifiers": sorted(gold_ids),
            "exports_per_dep": {d: len(exports[d]) for d in direct}, "a1_matches_pilot": a1_matches, "count_model": a.model, "arms": {}}
    seen = {}
    for name, (text, extra) in arms.items():
        rec = dict(extra); rec["chars"] = len(text)
        if text in seen: rec["same_as"] = seen[text]; meta["arms"][name] = rec; print(f"{name:6s} same as {seen[text]}"); continue
        seen[text] = name
        fn = name + ".txt"; open(os.path.join(a.out, fn), "w", encoding="utf-8", newline="\n").write(text)
        missing = [i for i in sorted(gold_ids) if i not in text]
        rec.update({"file": fn, "n_tokens_prompt": count(client, a.model, text, task), "expressible": not missing, "missing_identifiers": missing})
        meta["arms"][name] = rec
        print(f"{name:6s} tokens={rec['n_tokens_prompt']:7d} {extra.get('removed') or extra.get('kept', '')}", flush=True)
    print(f"deps={len(direct)} groups={len(groups)} gold_ref={len(gold_ref)} task_ref={len(task_ref)} a1_matches_pilot={a1_matches}")
    json.dump(meta, open(os.path.join(a.out, "contexts.json"), "w", encoding="utf-8"), indent=1)

if __name__ == "__main__":
    main()
