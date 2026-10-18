"""Render the report tables deterministically from phase23-report/RESULTS.json into phase23-report/tables.tex.
Labels: tab:p2inst, tab:p2con, tab:loo, tab:p3inst, tab:p3con. Usage: python analysis/phase23_tables.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "phase23-report")
R = json.load(open(os.path.join(OUT, "RESULTS.json"), encoding="utf-8"))
def esc(s): return str(s).replace("_", "\\_").replace("%", "\\%").replace("&", "\\&")
def ci(c): return f"${c['mean']:+.3f}$ $[{c['lo']:+.3f}, {c['hi']:+.3f}]$"
def short(i): return i.split("-")[-1]
L = []
# Phase 2 per instance
L += ["\\begin{table}[t]\\centering\\footnotesize", "\\caption{Phase 2: per-instance pass rates on the 10 screened instances (Haiku 5.5 $k{=}100$, Haiku 4.5 $k{=}20$, Sonnet 5.5 $k{=}10$, Opus 5.5 $k{=}5$). An arm byte-identical to another arm carries that arm's rate. ``deps'' is the number of direct dependencies; ``kept'' the dependencies retained by the gold-referenced (A1g) and task-referenced (A1t) predictors.}\\label{tab:p2inst}",
      "\\begin{tabular}{llrrr p{3.1cm} p{2.9cm} p{2.9cm} p{2.6cm}}\\toprule", "instance & repo & deps & A1g & A1t & Haiku 5.5 & Haiku 4.5 & Sonnet 5.5 & Opus 5.5\\\\\\midrule"]
for row in R["phase2_instances"]:
    def cell(m): d = row.get(m, {}); return " ".join(f"{a}\\,{v:.2f}" for a, v in d.items()) if d else "--"
    L.append(f"{short(row['instance'])} & {esc(row['repo'].split('/')[0])} & {row['deps']} & {row['a1g_kept']} & {row['a1t_kept']} & {cell('claude-haiku-5-5')} & {cell('claude-haiku-4-5-20251001')} & {cell('claude-sonnet-5-5')} & {cell('claude-opus-5-5')}\\\\")
L += ["\\bottomrule\\end{tabular}\\end{table}", ""]
# Phase 2 contrasts
L += ["\\begin{table}[t]\\centering\\small", "\\caption{Phase 2: paired contrasts on the 10 screened instances. Instance-level percentile bootstrap (2{,}000 resamples): mean difference with two-sided 95\\% interval, one-sided 95\\% lower bound (LB), sign counts $+/-/0$, and $n$. Degenerate instances (best arm $<0.1$): Haiku 5.5 " + f"{R['phase2_floor_instances']['claude-haiku-5-5']}/10, Haiku 4.5 {R['phase2_floor_instances']['claude-haiku-4-5-20251001']}/10, Sonnet 5.5 {R['phase2_floor_instances']['claude-sonnet-5-5']}/10, Opus 5.5 {R['phase2_floor_instances']['claude-opus-5-5']}/10" + ".}\\label{tab:p2con}",
      "\\begin{tabular}{llrrrr}\\toprule", "model & contrast & mean [95\\% CI] & LB & $+/-/0$ & $n$\\\\\\midrule"]
for key, c in R["phase2_contrasts"].items():
    m, con = key.split(":"); x, y = con.split("-")
    L.append(f"{esc(m.replace('claude-', ''))} & {x} $-$ {y} & {ci(c)} & ${c['lb1']:+.3f}$ & {c['pos']}/{c['neg']}/{c['zero']} & {c['n']}\\\\")
L += ["\\bottomrule\\end{tabular}\\end{table}", ""]
# LOO
L += ["\\begin{table}[t]\\centering\\small", "\\caption{Leave-one-dependency-out at $k{=}100$ (Haiku 5.5) on the three instances with A1 $\\geq 0.1$. Difference is pass(A1 minus group) $-$ pass(A1). The null reference draws every cell of an instance from one pooled rate and counts removals with $|\\text{difference}| > 0.05$.}\\label{tab:loo}",
      "\\begin{tabular}{llrrr}\\toprule", "instance (A1, W; tokens A1) & removed group & pass & difference & $n$\\\\\\midrule"]
for i, d in R["loo"].items():
    first = True
    for g in sorted(d["groups"], key=lambda g: g["diff"]):
        head = f"{short(i)} (A1 {d['A1']:.2f}, W {d['W']:.2f}; {d['tokens_A1']:,})" if first else ""; first = False
        L.append(f"{head} & {esc(', '.join(g['removed']))} & {g['pass']:.2f} & ${g['diff']:+.2f}$ & {g['n']}\\\\")
    L.append(f"\\multicolumn{{5}}{{l}}{{\\quad removals with $|$difference$|>0.05$: {d['obs_over_eps']} of {len(d['groups'])}; null reference {d['null_mean']} [{d['null_95'][0]}, {d['null_95'][1]}]; gold-referenced kept {esc(d['a1g_kept'])}; task-referenced kept {esc(d['a1t_kept'])}}}\\\\\\addlinespace")
L += ["\\bottomrule\\end{tabular}\\end{table}", ""]
# Phase 3 per instance
arms = ["W", "Wd", "A1", "A1r", "Wdr", "Wpad", "A1t"]
L += ["\\begin{table}[t]\\centering\\scriptsize\\setlength{\\tabcolsep}{3pt}", "\\caption{Phase 3: prompt tokens and pass rates on the 11 instances (Haiku 5.5 $k{=}50$; Sonnet 5.5 $k{=}10$). A trailing $=$ marks an arm byte-identical to another arm (it carries that arm's rate). ``slice'' is kept/total declarations of W; ``dep decls'' is referenced dependency declarations for the slice/for all of W.}\\label{tab:p3inst}",
      "\\begin{tabular}{llrrrrrrll" + "r" * 7 + "r" * 6 + "}\\toprule",
      "instance & repo & tok W & tok Wd & tok A1 & tok A1r & tok Wdr & tok Wpad & slice & dep decls & " + " & ".join("H " + a for a in arms) + " & " + " & ".join("S " + a for a in arms[:6]) + "\\\\\\midrule"]
for row in R["phase3_instances"]:
    def cell(d, a):
        v = d.get(a); return ("--" if v is None else f"{v:.2f}") + ("=" if row["alias"][a] != a else "")
    t = row["tokens"]
    L.append(f"{short(row['instance'])} & {esc(row['repo'].split('/')[0])} & {t['W']:,} & {t['Wd']:,} & {t['A1']:,} & {t['A1r']:,} & {t['Wdr']:,} & {t['Wpad']:,} & {row['slice']} & {row['deprefs']} & " + " & ".join(cell(row["haiku"], a) for a in arms) + " & " + " & ".join(cell(row["sonnet"], a) for a in arms[:6]) + "\\\\")
L += ["\\bottomrule\\end{tabular}\\end{table}", ""]
# Phase 3 contrasts
L += ["\\begin{table}[t]\\centering\\small", "\\caption{Phase 3: paired contrasts on the 11 instances. Haiku 5.5 is reported with W and A1 restricted to post-screen samples ($n{=}30$ per instance; other arms $n{=}50$) and with all samples; Sonnet 5.5 at $k{=}10$. NI: one-sided 95\\% lower bound $> -0.05$. Ratio: median per-instance prompt-token ratio.}\\label{tab:p3con}",
      "\\begin{tabular}{l rrrr r rrr rrr}\\toprule", " & \\multicolumn{5}{c}{Haiku 5.5, post-screen} & \\multicolumn{3}{c}{Haiku 5.5, all samples} & \\multicolumn{3}{c}{Sonnet 5.5}\\\\\\cmidrule(lr){2-6}\\cmidrule(lr){7-9}\\cmidrule(lr){10-12}",
      "contrast & mean [95\\% CI] & LB & NI & $+/-/0$ & ratio & mean [95\\% CI] & LB & $+/-/0$ & mean [95\\% CI] & LB & $+/-/0$\\\\\\midrule"]
for x, y in (("Wd", "W"), ("A1r", "A1"), ("Wdr", "A1"), ("Wdr", "W"), ("A1", "W"), ("Wpad", "W"), ("Wpad", "A1"), ("A1r", "W"), ("A1t", "A1"), ("A1t", "W")):
    a = R["phase3_contrasts"][f"haiku_post:{x}-{y}"]; b = R["phase3_contrasts"][f"haiku_all:{x}-{y}"]; s = R["phase3_contrasts"].get(f"sonnet:{x}-{y}")
    scol = f"{ci(s)} & ${s['lb1']:+.3f}$ & {s['pos']}/{s['neg']}/{s['zero']}" if s else r"\multicolumn{3}{c}{not run}"
    L.append(f"{x} $-$ {y} & {ci(a)} & ${a['lb1']:+.3f}$ & {'yes' if a['lb1'] > -0.05 else 'no'} & {a['pos']}/{a['neg']}/{a['zero']} & {a['token_ratio_median']:.2f} & {ci(b)} & ${b['lb1']:+.3f}$ & {b['pos']}/{b['neg']}/{b['zero']} & {scol}\\\\")
L += ["\\bottomrule\\end{tabular}\\end{table}", ""]
open(os.path.join(OUT, "tables.tex"), "w", encoding="utf-8").write("\n".join(L)); print("tables.tex written:", len("\n".join(L)), "chars")
