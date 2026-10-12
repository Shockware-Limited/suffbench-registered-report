"""Re-verify stored model outputs after a build-environment fault (preregistration §8, 2026-10-12).

Reads <results>, re-applies each applied response at the instance base commit in --repo, recomputes the
build/test verdicts with pilot_run.verify, and rewrites <results> in place; the original file is kept in --backup.
Records whose stored response was truncated, needed a repair turn, or do not reproduce the original patch hash
are dropped so pilot_run.py re-samples them.
"""
import argparse, json, os, sys, hashlib, shutil, pathlib, time
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from pilot_run import reset, verify
from run_instance import parse_blocks, apply_blocks
from run_mutation import run

FAULT = "build cache is required"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--contexts", required=True); ap.add_argument("--repo", required=True)
    ap.add_argument("--results", required=True); ap.add_argument("--backup", default="results-abl-invalid")
    a = ap.parse_args()
    inst = dict(json.load(open(a.instance, encoding="utf-8"))); inst["repo_path"] = a.repo; repo = a.repo
    meta = json.load(open(os.path.join(a.contexts, "contexts.json"), encoding="utf-8"))
    scope = [p for p in inst["write_set"] + meta["forward_slice"] if p not in inst.get("baseline_fail_pkgs", [])]
    os.makedirs(a.backup, exist_ok=True)
    bk = os.path.join(a.backup, os.path.basename(a.results))
    if not os.path.exists(bk): shutil.copy2(a.results, bk)
    recs = [json.loads(l) for l in open(bk, encoding="utf-8") if l.strip().startswith("{")]
    verdicts = {}; out = []; kept = redone = dropped = 0; t0 = time.time()
    for r in recs:
        if "arm" not in r: continue
        if not r.get("applied") or FAULT not in (r.get("build_error") or ""):
            out.append(r); kept += 1; continue
        if r.get("repaired") or len(r.get("response", "")) >= 4000:
            dropped += 1; continue
        reset(repo, inst)
        ok, err = apply_blocks(repo, parse_blocks(r["response"]))
        if not ok:
            dropped += 1; print(f"[{r['arm']} s{r['sample']}] re-apply failed: {err[:80]}", flush=True); continue
        diff = run(["git", "diff", "--", "*.go", ":!*_test.go"], repo).stdout
        sha = hashlib.sha1(diff.encode("utf-8", "replace")).hexdigest()
        if sha != r.get("patch_sha"):
            dropped += 1; print(f"[{r['arm']} s{r['sample']}] patch hash differs from the original; dropped", flush=True); continue
        for k in ("build_error", "test_output", "frame_fail_pkgs", "frame_pass", "frame_scope"): r.pop(k, None)
        if sha in verdicts: r.update(verdicts[sha]); r["verdict_cached"] = True
        else: v = verify(repo, inst, scope); verdicts[sha] = v; r.update(v); r["verdict_cached"] = False
        r["reverified"] = "2026-10-12 build-environment fault"; out.append(r); redone += 1
        print(f"[{r['arm']} s{r['sample']}] builds={r.get('builds')} delta={r.get('delta_pass')} frame={r.get('frame_pass', '-')} cached={r['verdict_cached']}", flush=True)
    reset(repo, inst)
    with open(a.results, "w", encoding="utf-8") as f:
        for r in out: f.write(json.dumps(r) + "\n")
    print(f"done {inst['instance_id']}: kept={kept} reverified={redone} dropped_for_resampling={dropped} {time.time() - t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
