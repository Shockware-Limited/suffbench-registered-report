"""Pilot analysis (HANDOFF-pilot-haiku.md §8). Reads harness/results/*-<model>.jsonl, writes results/PILOT-REPORT.md,
results/pilot_cells.csv, results/pilot_curve_<model>.png.
Usage: python analysis/pilot.py --results harness/results --out harness/results
"""
import argparse, glob, json, os, math, random, collections
import csv

PRICES = {  # $/M tokens: input, output, cache_read, cache_write. Vendor page 2026-10-12. Haiku 5.5 has a second tier for prompts >100k tokens.
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.125), "claude-sonnet-5-5": (2.0, 10.0, 0.10, 2.5), "claude-opus-5": (5.0, 25.0, 0.50, 6.25)}
PRICES_OVER_100K = {"claude-haiku-5-5": (0.50, 2.50, 0.05, 0.625)}

def price_for(model, u):
    p = u["in"] + u["cache_read"] + u["cache_write"]
    return PRICES_OVER_100K.get(model) if p > 100000 and model in PRICES_OVER_100K else PRICES.get(model, (0, 0, 0, 0))
LOAD_ARMS = ["A1", "P32", "P64", "P128", "P200"]; BASE_ARMS = ["A0", "W", "A1", "A1b", "A1F"]

def wilson(k, n, z=1.96):
    if n == 0: return (float("nan"), float("nan"))
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)

def boot_mean(vals, B=2000, seed=1):
    if not vals: return (float("nan"), float("nan"), float("nan"))
    rnd = random.Random(seed); n = len(vals); ms = []
    for _ in range(B): ms.append(sum(rnd.choice(vals) for _ in range(n)) / n)
    ms.sort(); return (sum(vals) / n, ms[int(0.025 * B)], ms[int(0.975 * B) - 1])

def boot_diff(pairs, B=2000, seed=2):
    if not pairs: return (float("nan"), float("nan"), float("nan"))
    rnd = random.Random(seed); n = len(pairs); ds = []
    for _ in range(B):
        s = [rnd.choice(pairs) for _ in range(n)]; ds.append(sum(x - y for x, y in s) / n)
    ds.sort(); return (sum(x - y for x, y in pairs) / n, ds[int(0.025 * B)], ds[int(0.975 * B) - 1])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--results", default="harness/results"); ap.add_argument("--out", default="harness/results")
    ap.add_argument("--exclude", nargs="*", default=[]); a = ap.parse_args()
    recs = []
    for f in glob.glob(os.path.join(a.results, "cli__cli-*-*.jsonl")):
        for l in open(f, encoding="utf-8"):
            try: r = json.loads(l)
            except Exception: continue
            if "arm" in r and r["instance_id"] not in a.exclude: recs.append(r)
    models = sorted({r["model"] for r in recs}); rep = ["# Pilot report (auto-generated; private until Stage 1 submission)\n"]
    rep.append(f"Records: {len(recs)}. Models: {', '.join(models)}. Instances: {len({r['instance_id'] for r in recs})}.\n")
    cells_csv = open(os.path.join(a.out, "pilot_cells.csv"), "w", newline="", encoding="utf-8"); cw = csv.writer(cells_csv)
    cw.writerow(["model", "instance", "arm", "n", "delta_pass", "frame_pass", "infra_err", "n_tokens_prompt"])
    for m in models:
        R = [r for r in recs if r["model"] == m]
        cells = collections.defaultdict(list)
        for r in R: cells[(r["instance_id"], r["arm"])].append(r)
        inst_ids = sorted({r["instance_id"] for r in R})
        def rate(i, arm, key="delta_pass"):
            rs = [r for r in cells[(i, arm)] if not r.get("api_error")]
            if not rs: return None
            if key == "both": return sum(bool(r.get("delta_pass")) and bool(r.get("frame_pass")) for r in rs) / len(rs)
            return sum(bool(r.get(key)) for r in rs) / len(rs)
        for (i, arm), rs in sorted(cells.items()):
            ok = [r for r in rs if not r.get("api_error")]
            cw.writerow([m, i, arm, len(rs), rate(i, arm), rate(i, arm, "frame_pass"), len(rs) - len(ok), (ok or rs)[0].get("n_tokens_prompt")])
        # A0 flags
        flagged = sorted(i for i in inst_ids if (rate(i, "A0") or 0) > 0)
        rep.append(f"\n## {m}\n\nInstances: {len(inst_ids)}. A0 (task-only) solved on {len(flagged)} instance(s): {flagged} — excluded from the curve below (reported both ways).\n")
        # spend
        cost = 0.0; toks = collections.Counter()
        for r in R:
            for u in r.get("usage", []):
                pi, po, pcr, pcw = price_for(m, u)
                cost += (u["in"] * pi + u["out"] * po + u["cache_read"] * pcr + u["cache_write"] * pcw) / 1e6
                toks["in"] += u["in"]; toks["out"] += u["out"]; toks["cache_read"] += u["cache_read"]; toks["cache_write"] += u["cache_write"]
        rep.append(f"Spend (list prices in PRICES, verify): ${cost:.2f}; tokens in={toks['in']:,} cache_read={toks['cache_read']:,} cache_write={toks['cache_write']:,} out={toks['out']:,}\n")
        # curve
        for excl in (True, False):
            use = [i for i in inst_ids if not (excl and i in flagged)]
            rep.append(f"\n### Degradation curve ({'excluding' if excl else 'including'} A0-solved; n_inst={len(use)})\n\n| load arm | median prompt tokens | p̂ Δ-pass [boot 95%] | p̂ Δ∧frame | paired drop vs A1 [95%] | cells |\n|---|---|---|---|---|---|")
            for arm in LOAD_ARMS:
                vals = [(i, rate(i, arm)) for i in use if rate(i, arm) is not None]
                if not vals: rep.append(f"| {arm} | – | – | – | – | 0 |"); continue
                mean, lo, hi = boot_mean([v for _, v in vals]); both = boot_mean([rate(i, arm, "both") for i, _ in vals])
                toksl = sorted(cells[(i, arm)][0].get("n_tokens_prompt") or 0 for i, _ in vals); med = toksl[len(toksl) // 2]
                pairs = [(rate(i, "A1"), v) for i, v in vals if rate(i, "A1") is not None]
                d, dlo, dhi = boot_diff(pairs) if arm != "A1" else (0, 0, 0)
                rep.append(f"| {arm} | {med:,} | {mean:.3f} [{lo:.3f}, {hi:.3f}] | {both[0]:.3f} | {d:+.3f} [{dlo:+.3f}, {dhi:+.3f}] | {len(vals)} |")
            if not excl: break
        # minimal sufficient load per instance
        for eps in (0.05, 0.10):
            hist = collections.Counter()
            for i in inst_ids:
                rs = [(arm, rate(i, arm)) for arm in LOAD_ARMS if rate(i, arm) is not None]
                if len(rs) < 2: continue
                best = max(v for _, v in rs); hist[next(arm for arm, v in rs if v >= best - eps - 1e-9)] += 1
            rep.append(f"\nMinimal sufficient load at ε={eps}: " + ", ".join(f"{k}={v}" for k, v in sorted(hist.items(), key=lambda kv: LOAD_ARMS.index(kv[0]))) + f" (k-granularity limits resolution)")
        # flip rate
        nonun = tot = 0; minority = []
        for (i, arm), rs in cells.items():
            ok = [bool(r.get("delta_pass")) for r in rs if not r.get("api_error")]
            if len(ok) >= 3:
                tot += 1; p = sum(ok)
                if 0 < p < len(ok): nonun += 1; minority.append(min(p, len(ok) - p) / len(ok))
        rep.append(f"\n\nFlip rate (cells with ≥3 samples, non-unanimous Δ-pass): {nonun}/{tot} = {nonun / tot if tot else float('nan'):.3f}; mean minority share {sum(minority) / len(minority) if minority else 0:.3f}")
        # H2 descriptive
        rep.append("\n\n### Base-load arms (descriptive)\n\n| arm | median tokens | p̂ Δ-pass [boot 95%] | pooled Wilson | p̂ Δ∧frame | n_inst |\n|---|---|---|---|---|---|")
        for arm in BASE_ARMS:
            vals = [(i, rate(i, arm)) for i in inst_ids if rate(i, arm) is not None]
            if not vals: continue
            mean, lo, hi = boot_mean([v for _, v in vals]); both = boot_mean([rate(i, arm, "both") for i, _ in vals])
            k = sum(bool(r.get("delta_pass")) for i, _ in vals for r in cells[(i, arm)] if not r.get("api_error")); n = sum(len([r for r in cells[(i, arm)] if not r.get("api_error")]) for i, _ in vals)
            wl, wh = wilson(k, n); toksl = sorted(cells[(i, arm)][0].get("n_tokens_prompt") or 0 for i, _ in vals)
            rep.append(f"| {arm} | {toksl[len(toksl) // 2]:,} | {mean:.3f} [{lo:.3f}, {hi:.3f}] | [{wl:.3f}, {wh:.3f}] | {both[0]:.3f} | {len(vals)} |")
        for x, y in (("A1", "A1b"), ("A1", "A1F"), ("A1", "W")):
            pairs = [(rate(i, x), rate(i, y)) for i in inst_ids if rate(i, x) is not None and rate(i, y) is not None]
            d, lo, hi = boot_diff(pairs); dis = sum(1 for p, q in pairs if (p >= 0.5) != (q >= 0.5))
            rep.append(f"\nPaired {x}−{y}: {d:+.3f} [{lo:+.3f}, {hi:+.3f}] over {len(pairs)} instances; majority-outcome disagreement π_d = {dis}/{len(pairs)}")
        ceiling = sum(1 for i in inst_ids if rate(i, "W") == 1.0); rep.append(f"\n\nCeiling rate (W alone passes every sample): {ceiling}/{len(inst_ids)}")
        # failure taxonomy
        tax = collections.defaultdict(collections.Counter)
        for r in R:
            if r.get("api_error") == "exceeds_window": c = "exceeds_window"
            elif r.get("api_error"): c = "api_error"
            elif not r.get("applied"): c = "no_blocks" if "no SEARCH" in (r.get("apply_error") or "") else "apply_error"
            elif not r.get("builds"): c = "build_error"
            elif not r.get("delta_pass"): c = "delta_fail"
            elif r.get("frame_pass") is False: c = "frame_fail"
            else: c = "pass"
            tax[r["arm"]][c] += 1
        rep.append("\n\n### Outcome taxonomy per arm\n\n| arm | " + " | ".join(["pass", "delta_fail", "frame_fail", "build_error", "apply_error", "no_blocks", "api_error", "exceeds_window"]) + " |\n|---|" + "---|" * 8)
        for arm in BASE_ARMS + LOAD_ARMS[1:]:
            if arm in tax: rep.append(f"| {arm} | " + " | ".join(str(tax[arm][c]) for c in ["pass", "delta_fail", "frame_fail", "build_error", "apply_error", "no_blocks", "api_error", "exceeds_window"]) + " |")
        # figure
        try:
            import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
            use = [i for i in inst_ids if i not in flagged]; xs, ys, lo_, hi_ = [], [], [], []
            for arm in LOAD_ARMS:
                vals = [rate(i, arm) for i in use if rate(i, arm) is not None]
                if not vals: continue
                mean, lo, hi = boot_mean(vals); toksl = sorted(cells[(i, arm)][0].get("n_tokens_prompt") or 0 for i in use if rate(i, arm) is not None)
                xs.append(toksl[len(toksl) // 2]); ys.append(mean); lo_.append(mean - lo); hi_.append(hi - mean)
            if xs:
                plt.figure(figsize=(5, 3.2)); plt.errorbar(xs, ys, yerr=[lo_, hi_], marker="o", capsize=3); plt.xscale("log"); plt.ylim(0, 1.02)
                plt.xlabel("prompt tokens (median per arm)"); plt.ylabel("Δ-pass rate"); plt.title(f"{m}: pass rate vs load at fixed coverage"); plt.tight_layout()
                plt.savefig(os.path.join(a.out, f"pilot_curve_{m}.png"), dpi=150); plt.close()
        except Exception as e: rep.append(f"\n\n(figure skipped: {e})")
    cells_csv.close()
    open(os.path.join(a.out, "PILOT-REPORT.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n"); print("\n".join(rep))

if __name__ == "__main__":
    main()
