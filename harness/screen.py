"""Select H5 contrast instances (preregistration amendment 2026-10-12 (ii)): W inexpressible and W pass rate below --threshold
on the k=5 screen. Reads results-p2screen/<id>-<model>.jsonl and <ctxdir>/contexts.json for each row of --manifest
(tab-separated: instance_id, contexts dir, worktree). Writes --out (same format, selected rows only) and a JSON summary.
"""
import argparse, json, os, collections

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--manifest", required=True); ap.add_argument("--screen", default="results-p2screen")
    ap.add_argument("--model", default="claude-haiku-5-5"); ap.add_argument("--threshold", type=float, default=0.8); ap.add_argument("--out", required=True)
    a = ap.parse_args(); rows = [l.rstrip("\n").split("\t") for l in open(a.manifest, encoding="utf-8") if l.strip()]
    sel = []; summary = []
    for iid, ctx, wt in rows:
        meta = json.load(open(os.path.join(ctx, "contexts.json"), encoding="utf-8"))
        expressible = meta["arms"].get("W", {}).get("expressible", True)
        f = os.path.join(a.screen, f"{iid}-{a.model}.jsonl"); ok = []
        if os.path.exists(f):
            for l in open(f, encoding="utf-8"):
                try: r = json.loads(l)
                except Exception: continue
                if r.get("arm") == "W" and not r.get("api_error"): ok.append(bool(r.get("delta_pass")))
        w_rate = sum(ok) / len(ok) if ok else None
        keep = (not expressible) and w_rate is not None and w_rate < a.threshold
        summary.append({"instance_id": iid, "repo": meta.get("repo"), "task_text_source": meta.get("task_text_source"), "w_expressible": expressible,
                        "w_screen_rate": w_rate, "n_screen": len(ok), "selected": keep, "n_deps": len(meta["direct_deps"]),
                        "a1g_kept": meta["arms"].get("A1g", {}).get("kept", []), "a1t_kept": meta["arms"].get("A1t", {}).get("kept", [])})
        if keep: sel.append((iid, ctx, wt))
    open(a.out, "w", encoding="utf-8", newline="\n").write("".join(f"{i}\t{c}\t{w}\n" for i, c, w in sel))
    json.dump(summary, open(os.path.splitext(a.out)[0] + ".json", "w", encoding="utf-8"), indent=1)
    by = collections.Counter((s["repo"], s["selected"]) for s in summary)
    print(f"screened {len(summary)} selected {len(sel)}; " + ", ".join(f"{r}: {by[(r, True)]}/{by[(r, True)] + by[(r, False)]}" for r in sorted({s['repo'] for s in summary}, key=str)))

if __name__ == "__main__":
    main()
