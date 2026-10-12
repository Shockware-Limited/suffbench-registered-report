"""Run one editor on one instance across named contexts, apply its edits, verify, record.

Protocol (spec / RR design): single shot; context + task in, SEARCH/REPLACE blocks out; one format-repair
turn only if a block fails to apply (no test feedback). k samples per context. Sampling parameters are
not settable on Claude Opus 5-class models, so each sample is an independent default-sampling call;
identical prompts share a prompt cache (cache_control on the context block).

Usage: python run_instance.py --instance inst.json --contexts contexts/ --model claude-opus-5 --k 3 --out results.jsonl
Requires the worktree at instance.repo_path; the script resets it to base_commit before each run.
"""
import argparse, json, os, re, subprocess, sys, time, pathlib
import anthropic
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
from run_mutation import run, GO, parse_test_json

SYSTEM = """You are an expert Go engineer making a minimal, correct change to a repository.
You are given repository context (Go source files and exported API listings) and a task.
Produce the edit as one or more SEARCH/REPLACE blocks and nothing else. Format exactly:

<<<< FILE: relative/path/to/file.go
<<<<<<< SEARCH
exact lines copied verbatim from the file
=======
replacement lines
>>>>>>> REPLACE

Rules: SEARCH text must match the file exactly (including indentation). Keep edits minimal. Do not modify
test files. Do not add explanations outside the blocks."""

BLOCK = re.compile(r"(?:<<<< FILE: (?P<path>[^\n]+)\n)?<<<<<<< SEARCH\n(?P<search>.*?)\n=======\n(?P<replace>.*?)\n>>>>>>> REPLACE", re.S)

def parse_blocks(text):
    """SEARCH/REPLACE blocks; a block without a FILE header inherits the previous block's path."""
    out, last = [], None
    for m in BLOCK.finditer(text):
        path = (m.group("path") or last or "").strip()
        if not path: continue
        last = path
        out.append((path, m.group("search"), m.group("replace")))
    return out

def apply_blocks(repo, blocks):
    """Apply in order; return (ok, error_message)."""
    for path, search, replace in blocks:
        full = os.path.join(repo, path)
        if not os.path.isfile(full): return False, f"file not found: {path}"
        src = open(full, encoding="utf-8").read()
        if src.count(search) == 0: return False, f"SEARCH text not found in {path}:\n{search[:300]}"
        if src.count(search) > 1: return False, f"SEARCH text ambiguous ({src.count(search)} matches) in {path}"
        open(full, "w", encoding="utf-8", newline="").write(src.replace(search, replace, 1))
    return True, ""

def reset(repo, base):
    run(["git", "checkout", "-q", "-f", base], repo); run(["git", "clean", "-fdq"], repo)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--contexts", required=True)
    ap.add_argument("--model", default="claude-opus-5"); ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--effort", default="high"); ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*", help="context names to run (default all)")
    ap.add_argument("--full-suite", action="store_true", help="run full suite on patches passing fail-to-pass")
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8")); repo = inst["repo_path"]
    meta = json.load(open(os.path.join(a.contexts, "contexts.json"), encoding="utf-8"))
    key = open(os.path.expanduser(inst["api_key_file"]), encoding="utf-8-sig").read().strip()
    # Always use the author's key against the public endpoint; ignore any proxy credentials in the environment.
    for var in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"):
        os.environ.pop(var, None)
    client = anthropic.Anthropic(api_key=key, base_url="https://api.anthropic.com", max_retries=3)
    out = open(a.out, "a", encoding="utf-8")
    names = a.only or list(meta["contexts"].keys())
    for name in names:
        ctx_text = open(os.path.join(a.contexts, meta["contexts"][name]["file"]), encoding="utf-8").read()
        for s in range(a.k):
            reset(repo, inst["base_commit"])
            # apply the child's test patch so the hidden tests exist (they are never shown to the model)
            for tf, content in inst["test_files"].items():
                open(os.path.join(repo, tf), "w", encoding="utf-8", newline="\n").write(content)
            messages = [{"role": "user", "content": [
                {"type": "text", "text": "REPOSITORY CONTEXT\n\n" + ctx_text, "cache_control": {"type": "ephemeral"}},
                {"type": "text", "text": "TASK\n\n" + inst["task_text"] + "\n\nProduce the SEARCH/REPLACE blocks now."},
            ]}]
            rec = {"instance_id": inst["instance_id"], "model": a.model, "context": name, "sample": s,
                   "effort": a.effort, "chars": len(ctx_text)}
            t0 = time.time(); usage = []; repaired = False; text = ""
            try:
                for turn in range(2):
                    with client.messages.stream(model=a.model, max_tokens=16000, system=SYSTEM, messages=messages,
                                                output_config={"effort": a.effort}) as stream:
                        resp = stream.get_final_message()
                    usage.append({"in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
                                  "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0) or 0,
                                  "cache_write": getattr(resp.usage, "cache_creation_input_tokens", 0) or 0,
                                  "stop": resp.stop_reason})
                    if resp.stop_reason == "refusal":
                        rec["refusal"] = True; break
                    text = "".join(b.text for b in resp.content if b.type == "text")
                    blocks = parse_blocks(text)
                    if not blocks:
                        ok, err = False, "no SEARCH/REPLACE blocks found"
                    else:
                        ok, err = apply_blocks(repo, blocks)
                    if ok or turn == 1: break
                    repaired = True  # one repair turn, format error only, no test feedback
                    messages += [{"role": "assistant", "content": text},
                                 {"role": "user", "content": f"The edit could not be applied: {err}\nRe-emit corrected SEARCH/REPLACE blocks only."}]
            except anthropic.APIStatusError as e:
                rec["api_error"] = f"{e.status_code}: {e.message}"; ok, err = False, "api error"
            rec.update({"applied": ok, "apply_error": err if not ok else "", "repaired": repaired, "usage": usage,
                        "latency_s": round(time.time() - t0, 1), "n_blocks": len(parse_blocks(text)), "response": text[:4000]})
            if ok:
                b = run([GO, "build", "./..."], repo, timeout=600)
                rec["builds"] = b.returncode == 0
                if rec["builds"]:
                    t = run([GO, "test", "-count=1", "-json", "-run", "|".join(inst["fail_to_pass"]), inst["test_pkg"]], repo, timeout=900)
                    st = parse_test_json(t.stdout); rec["delta_pass"] = all(v == "pass" for v in st.values()) and bool(st)
                    if not rec["delta_pass"]:
                        fail_lines = [json.loads(l).get("Output", "") for l in t.stdout.splitlines() if l.startswith("{") and '"Output"' in l]
                        rec["test_output"] = "".join(fail_lines)[-2500:]
                    if rec["delta_pass"] and a.full_suite:
                        tt = run([GO, "test", "./...", "-count=1", "-json"], repo, timeout=2400)
                        stf = parse_test_json(tt.stdout)
                        fails = sorted(p for p, v in stf.items() if v == "fail")
                        rec["frame_fail_pkgs"] = [p for p in fails if p not in inst.get("baseline_fail_pkgs", [])]
                        rec["frame_pass"] = not rec["frame_fail_pkgs"]
                else:
                    rec["delta_pass"] = False; rec["build_error"] = b.stderr[:1500]
            else:
                rec["builds"] = False; rec["delta_pass"] = False
            rec["gold_diff_lines"] = run(["git", "diff", "--stat", "--", "*.go", ":!*_test.go"], repo).stdout.strip()[-300:]
            out.write(json.dumps(rec) + "\n"); out.flush()
            u = usage[0] if usage else {}
            print(f"[{name} s{s}] applied={ok} builds={rec.get('builds')} delta_pass={rec.get('delta_pass')} "
                  f"frame_pass={rec.get('frame_pass','-')} in={u.get('in')} cache_read={u.get('cache_read')} out={u.get('out')} {rec['latency_s']}s", flush=True)
    reset(repo, inst["base_commit"])

if __name__ == "__main__":
    main()
