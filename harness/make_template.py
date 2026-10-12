"""Write a mining template for a repository from its `go test -json ./...` baseline.
Usage: python make_template.py --repo owner/name --wt <worktree name under CORPUS_ROOT> --baseline <repo>-baseline.json --out instances/_template_<name>.json
"""
import argparse, json

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--repo", required=True); ap.add_argument("--wt", required=True); ap.add_argument("--baseline", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); st = {}
    for l in open(a.baseline, encoding="utf-8", errors="replace"):
        try: e = json.loads(l)
        except Exception: continue
        if e.get("Test") is None and e.get("Action") in ("pass", "fail", "skip"): st[e["Package"]] = e["Action"]
    fails = sorted(p for p, v in st.items() if v == "fail")
    json.dump({"repo": a.repo, "repo_path": a.wt, "baseline_fail_pkgs": fails, "baseline_pkgs": len(st)}, open(a.out, "w", encoding="utf-8"), indent=1)
    print(f"{a.repo}: {len(st)} packages, {len(fails)} failing at baseline")

if __name__ == "__main__":
    main()
