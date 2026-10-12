"""Sum API spend over result files at list prices. Exit 2 when --cap is exceeded (used by the orchestrator between instances).
Usage: python spend.py results-p2 [results-p2screen ...] [--model claude-haiku-5-5] [--cap 45]
"""
import argparse, glob, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analysis"))
from pilot import price_for

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("dirs", nargs="+"); ap.add_argument("--model"); ap.add_argument("--cap", type=float); ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(); tot = {}; n = {}
    for d in a.dirs:
        for f in glob.glob(os.path.join(d, "*.jsonl")):
            for l in open(f, encoding="utf-8"):
                try: r = json.loads(l)
                except Exception: continue
                if "arm" not in r or (a.model and r["model"] != a.model): continue
                m = r["model"]; n[m] = n.get(m, 0) + 1
                for u in r.get("usage", []):
                    p = price_for(m, u); tot[m] = tot.get(m, 0.0) + (u["in"] * p[0] + u["out"] * p[1] + u["cache_read"] * p[2] + u["cache_write"] * p[3]) / 1e6
    total = sum(tot.values())
    if not a.quiet:
        for m in sorted(tot): print(f"{m}: ${tot[m]:.2f} over {n[m]} samples")
        print(f"TOTAL ${total:.2f}")
    if a.cap is not None and total > a.cap: print(f"CAP EXCEEDED {total:.2f} > {a.cap}"); sys.exit(2)

if __name__ == "__main__":
    main()
