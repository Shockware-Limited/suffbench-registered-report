"""Ablation analysis (preregistration H5). Reads harness/results-abl/*-<model>.jsonl and harness/abl-<id>/contexts.json.
Writes ABLATION-REPORT.md and ablation_cells.csv into --out.
Usage: python analysis/ablation.py --results harness/results-abl --contexts-root harness --out harness/results-abl
"""
import argparse, glob, json, os, collections, csv, sys
sys.path.insert(0, os.path.dirname(__file__))
from pilot import boot_diff, boot_mean, price_for

def boot_sorted(pairs, B=2000, seed=2):
    """Sorted bootstrap distribution of the mean paired difference; same generator as pilot.boot_diff."""
    import random; rnd = random.Random(seed); n = len(pairs); ds = []
    for _ in range(B):
        s = [rnd.choice(pairs) for _ in range(n)]; ds.append(sum(x - y for x, y in s) / n)
    return sorted(ds)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default="harness/results-abl"); ap.add_argument("--contexts-root", default="harness")
    ap.add_argument("--out", default="harness/results-abl"); ap.add_argument("--eps", type=float, default=0.05)
    ap.add_argument("--pilot-results", default="harness/results"); a = ap.parse_args()
    recs = []
    for f in glob.glob(os.path.join(a.results, "cli__cli-*-*.jsonl")):
        for l in open(f, encoding="utf-8"):
            try: r = json.loads(l)
            except Exception: continue
            if "arm" in r: recs.append(r)
    models = sorted({r["model"] for r in recs}); rep = ["# Ablation report (auto-generated)\n"]
    insts = sorted({r["instance_id"] for r in recs})
    meta = {i: json.load(open(os.path.join(a.contexts_root, f"abl-{i}", "contexts.json"), encoding="utf-8")) for i in insts}
    rep.append(f"Records: {len(recs)}. Models: {', '.join(models)}. Instances: {len(insts)}. eps={a.eps}.\n")
    cw = csv.writer(open(os.path.join(a.out, "ablation_cells.csv"), "w", newline="", encoding="utf-8"))
    cw.writerow(["model", "instance", "arm", "n", "delta_pass", "frame_pass", "n_tokens_prompt", "removed", "same_as"])
    for m in models:
        R = [r for r in recs if r["model"] == m]; cells = collections.defaultdict(list)
        for r in R: cells[(r["instance_id"], r["arm"])].append(r)
        def raw_rate(i, arm, key="delta_pass"):
            rs = [r for r in cells[(i, arm)] if not r.get("api_error")]
            return None if not rs else sum(bool(r.get(key)) for r in rs) / len(rs)
        def rate(i, arm, key="delta_pass"):
            am = meta[i]["arms"].get(arm, {})
            return rate(i, am["same_as"], key) if "same_as" in am else raw_rate(i, arm, key)
        def toks(i, arm):
            am = meta[i]["arms"].get(arm, {})
            return toks(i, am["same_as"]) if "same_as" in am else am.get("n_tokens_prompt")
        for i in insts:
            for arm, am in meta[i]["arms"].items():
                cw.writerow([m, i, arm, len(cells[(i, arm)]), rate(i, arm), rate(i, arm, "frame_pass"), toks(i, arm), ";".join(am.get("removed", [])), am.get("same_as", "")])
        cost = sum((u["in"] * p[0] + u["out"] * p[1] + u["cache_read"] * p[2] + u["cache_write"] * p[3]) / 1e6
                   for r in R for u in r.get("usage", []) for p in [price_for(m, u)])
        rep.append(f"\n## {m}\n\nSpend at list prices: ${cost:.2f}. Samples: {len(R)}.\n")
        # A1 drift vs pilot
        pilot = collections.defaultdict(list)
        for f in glob.glob(os.path.join(a.pilot_results, f"cli__cli-*-{m}.jsonl")):
            for l in open(f, encoding="utf-8"):
                try: r = json.loads(l)
                except Exception: continue
                if r.get("arm") == "A1" and not r.get("api_error"): pilot[r["instance_id"]].append(bool(r.get("delta_pass")))
        drift = [(rate(i, "A1"), sum(pilot[i]) / len(pilot[i])) for i in insts if pilot.get(i) and rate(i, "A1") is not None]
        if drift:
            d = boot_diff(drift); rep.append(f"A1 now (k=20) minus A1 pilot (k=10), {len(drift)} instances: {d[0]:+.3f} [{d[1]:+.3f}, {d[2]:+.3f}]\n")
        # H5a / H5b
        rep.append("\n### H5: predicted-minimal contexts vs A1 (paired, instance-level bootstrap)\n\n"
                   "Decision rule (preregistration §6, one-sided α=0.05): one-sided 95% lower bound > −eps. The two-sided interval, sign counts and the "
                   "estimate without the most influential instance are shown alongside (added 2026-10-12 after the exploratory run; descriptive).\n\n"
                   "| contrast | n | mean diff | 95% CI (two-sided) | one-sided 95% LB | non-inferior at eps | sign +/−/0 | without most influential | median tokens | tokens A1 |\n|---|---|---|---|---|---|---|---|---|---|")
        for arm in ("A1g", "A1t", "W"):
            trip = [(i, rate(i, arm), rate(i, "A1")) for i in insts if rate(i, arm) is not None and rate(i, "A1") is not None]
            if not trip: continue
            pairs = [(x, y) for _, x, y in trip]; d = boot_diff(pairs); lb1 = boot_sorted(pairs)[int(0.05 * 2000)]
            pos = sum(x > y for x, y in pairs); neg = sum(x < y for x, y in pairs)
            infl = max(trip, key=lambda t: abs(t[1] - t[2])); d_wo = boot_diff([(x, y) for i, x, y in trip if i != infl[0]])
            tk = sorted(toks(i, arm) or 0 for i in insts); ta = sorted(toks(i, "A1") or 0 for i in insts)
            rep.append(f"| {arm} − A1 | {len(pairs)} | {d[0]:+.3f} | [{d[1]:+.3f}, {d[2]:+.3f}] | {lb1:+.3f} | {'yes' if lb1 > -a.eps else 'no'} | {pos}/{neg}/{len(pairs) - pos - neg} | "
                       f"{d_wo[0]:+.3f} [{d_wo[1]:+.3f}, {d_wo[2]:+.3f}] (drop {infl[0][-12:]}) | {tk[len(tk)//2]:,} | {ta[len(ta)//2]:,} |")
        same_w = {arm: sum(1 for i in insts if meta[i]["arms"].get(arm, {}).get("same_as") == "W") for arm in ("A1g", "A1t")}
        ceil = sum(1 for i in insts if rate(i, "A1") == 1.0 and rate(i, "W") == 1.0); floor = sum(1 for i in insts if rate(i, "A1") == 0.0 and rate(i, "W") == 0.0)
        inexpr = sum(1 for i in insts if not meta[i]["arms"].get("W", {}).get("expressible", True))
        rep.append(f"\nInstances where the predictor keeps no dependency (arm equals W): A1g {same_w['A1g']}/{len(insts)}, A1t {same_w['A1t']}/{len(insts)}. "
                   f"Instances with W and A1 both at ceiling (1.0): {ceil}; both at floor (0.0): {floor}; W inexpressible (gold identifiers missing from W): {inexpr}. "
                   f"Only instances outside ceiling and floor can separate the arms.\n")
        # necessity
        rows = []; informative = []
        for i in insts:
            base = rate(i, "A1")
            if base is None: continue
            if base > 0: informative.append(i)
            kept_g = set(meta[i]["arms"].get("A1g", {}).get("kept", [])); kept_t = set(meta[i]["arms"].get("A1t", {}).get("kept", []))
            for gi, g in enumerate(meta[i]["groups"]):
                arm = f"A1-{gi:02d}"; r_ = rate(i, arm)
                if r_ is None: continue
                drop = base - r_
                rows.append({"inst": i, "group": g, "drop": drop, "necessary": drop > a.eps, "helps": -drop > a.eps, "informative": base > 0,
                             "pred_g": bool(kept_g & set(g)), "pred_t": bool(kept_t & set(g)), "dtok": (toks(i, "A1") or 0) - (toks(i, arm) or 0)})
        inf_rows = [r for r in rows if r["informative"]]
        rep.append(f"\n### Necessity of dependency interfaces (removal lowers instance pass by > eps)\n\nInstances with A1 pass > 0 (informative): {len(informative)}/{len(insts)}. "
                   f"Dependency groups on informative instances: {len(inf_rows)}.\n")
        if inf_rows:
            nec = [r for r in inf_rows if r["necessary"]]; helps = [r for r in inf_rows if r["helps"]]
            bm = boot_mean([float(r["necessary"]) for r in inf_rows])
            rep.append(f"- Necessary: {len(nec)}/{len(inf_rows)} = {bm[0]:.3f} [{bm[1]:.3f}, {bm[2]:.3f}] (bootstrap over groups; instance clustering ignored here).")
            rep.append(f"- Removal raises pass by > eps (non-monotone cells): {len(helps)}/{len(inf_rows)}.")
            # null reference (added 2026-10-12): every cell of an instance drawn from one pooled rate at k=20
            import random; rnd = random.Random(3); sim_n = []; sim_h = []; K = 20
            per_inst = collections.defaultdict(list)
            for r in inf_rows: per_inst[r["inst"]].append(r)
            for _ in range(2000):
                n_ = h_ = 0
                for i, rs in per_inst.items():
                    p = (rate(i, "A1") + sum(rate(i, "A1") - r["drop"] for r in rs)) / (len(rs) + 1)
                    base = sum(rnd.random() < p for _ in range(K)) / K
                    for _r in rs:
                        cell = sum(rnd.random() < p for _ in range(K)) / K
                        n_ += base - cell > a.eps; h_ += cell - base > a.eps
                sim_n.append(n_); sim_h.append(h_)
            sim_n.sort(); sim_h.sort()
            rep.append(f"- Null reference (all cells of an instance share one rate, k={K}, 2,000 simulations): necessary {sum(sim_n)/len(sim_n):.1f} "
                       f"[{sim_n[50]}, {sim_n[1949]}], helps {sum(sim_h)/len(sim_h):.1f} [{sim_h[50]}, {sim_h[1949]}]. Observed counts inside this range are not evidence of necessity.")
            by_inst = sorted(((i, sum(r['necessary'] for r in rs), sum(r['helps'] for r in rs), len(rs)) for i, rs in per_inst.items()), key=lambda t: -(t[1] + t[2]))
            rep.append("- Per instance (necessary/helps/groups): " + ", ".join(f"{i[-12:]} {n_}/{h_}/{g}" for i, n_, h_, g in by_inst[:8]) + ".")
            for name, key in (("gold-referenced", "pred_g"), ("task-referenced", "pred_t")):
                tp = sum(r[key] and r["necessary"] for r in inf_rows); fp = sum(r[key] and not r["necessary"] for r in inf_rows); fn = sum((not r[key]) and r["necessary"] for r in inf_rows)
                prec = tp / (tp + fp) if tp + fp else float("nan"); rec_ = tp / (tp + fn) if tp + fn else float("nan")
                rep.append(f"- Predictor {name}: predicted {tp + fp}, precision {prec:.2f}, recall {rec_:.2f} (tp={tp}, fp={fp}, fn={fn}).")
            slack = []
            for i in informative:
                ta = toks(i, "A1") or 0; unnecessary = sum(r["dtok"] for r in inf_rows if r["inst"] == i and not r["necessary"])
                if ta: slack.append(ta / max(1, ta - unnecessary))
            if slack:
                bs = boot_mean(slack); rep.append(f"- Slack tokens(A1)/tokens(W ∪ necessary): mean {bs[0]:.2f} [{bs[1]:.2f}, {bs[2]:.2f}], median {sorted(slack)[len(slack)//2]:.2f}.")
            rep.append("\n| instance | A1 pass | group removed | pass after | drop | pred gold | pred task |\n|---|---|---|---|---|---|---|")
            for r in sorted(inf_rows, key=lambda r: -abs(r["drop"]))[:40]:
                rep.append(f"| {r['inst'][-12:]} | {rate(r['inst'], 'A1'):.2f} | {', '.join(g.split('/')[-1] for g in r['group'])[:40]} | {rate(r['inst'], 'A1') - r['drop']:.2f} | {r['drop']:+.2f} | {int(r['pred_g'])} | {int(r['pred_t'])} |")
    open(os.path.join(a.out, "ABLATION-REPORT.md"), "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep))

if __name__ == "__main__":
    main()
