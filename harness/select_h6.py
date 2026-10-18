"""Select H6 instances (amendment 2026-10-13): keep an instance when its Haiku 5.5 W or A1 pass rate on the k=20 screen lies in
[--lo, --hi]. Manifest rows: id, contexts dir, worktree, instance file. Writes the selected rows and a JSON summary.
Usage: python select_h6.py --manifest p3_manifest.tsv --results results-p3 --out p3_selected.tsv
"""
import argparse, json, os, collections

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", required=True); ap.add_argument("--results", default="results-p3")
    ap.add_argument("--model", default="claude-haiku-5-5"); ap.add_argument("--lo", type=float, default=0.1); ap.add_argument("--hi", type=float, default=0.9); ap.add_argument("--out", required=True)
    a = ap.parse_args(); rows = [l.rstrip("\n").split("\t") for l in open(a.manifest, encoding="utf-8") if l.strip()]
    sel = []; summary = []
    for row in rows:
        iid, ctx, wt = row[:3]; meta = json.load(open(os.path.join(ctx, "contexts.json"), encoding="utf-8"))
        rates = {}
        f = os.path.join(a.results, f"{iid}-{a.model}.jsonl")
        if os.path.exists(f):
            cells = collections.defaultdict(list)
            for l in open(f, encoding="utf-8"):
                try: r = json.loads(l)
                except Exception: continue
                if r.get("arm") in ("W", "A1") and not r.get("api_error"): cells[r["arm"]].append(bool(r.get("delta_pass")))
            rates = {k: sum(v) / len(v) for k, v in cells.items() if v}
        keep = any(a.lo <= v <= a.hi for v in rates.values())
        summary.append({"instance_id": iid, "repo": meta.get("repo"), "rates": rates, "selected": keep, "w_expressible": meta["arms"].get("W", {}).get("expressible")})
        if keep: sel.append(row)
    open(a.out, "w", encoding="utf-8", newline="\n").write("".join("\t".join(r) + "\n" for r in sel))
    json.dump(summary, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), indent=1)
    by = collections.Counter((s["repo"], s["selected"]) for s in summary)
    print(f"screened {len(summary)} selected {len(sel)}; " + ", ".join(f"{r}: {by[(r, True)]}/{by[(r, True)] + by[(r, False)]}" for r in sorted({s['repo'] for s in summary}, key=str)))

if __name__ == "__main__":
    main()
