"""Drive the write-up of the Phase 1-3 exploratory report through the Anthropic API with an adversarial review loop and a
numbers audit against phase23-report/RESULTS.md. No experiment is run; the writer may only cite numbers in RESULTS.md and the
tables are rendered locally by analysis/phase23_tables.py (tables.tex) so no table number can be invented.
Usage (repository root): python analysis/writeup.py [--rounds 2]
Outputs in phase23-report/: body-r0.tex, review-r0.md, audit-r0.md, body-r1.tex, ..., main.tex (preamble + final body), ERRATA-CHECK.md, api-log.json
"""
import argparse, json, os, re, sys, time
import anthropic
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(ROOT, "phase23-report")
KEY = open(os.path.expanduser("~/.config/context-sufficiency-note/anthropic.key"), encoding="utf-8-sig").read().strip()
for v in ("ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"): os.environ.pop(v, None)
client = anthropic.Anthropic(api_key=KEY, base_url="https://api.anthropic.com", max_retries=3)
WRITER = "claude-opus-5-5"; CRITIC = "claude-opus-5-5"; CHECKER = "claude-sonnet-5-5"
LOG = []
TITLE = r"Load, Granularity and Reader Effects: Exploratory Ablations of\\ $\eps$-Sufficient Context for Language-Model Code Editing in Go (Phases 1 to 3)"
DATE = r"18 October 2026 \quad\textit{Exploratory report, version 1.0}"

def read(p): return open(p, encoding="utf-8").read()
def call(model, system, user, max_tokens, tag, effort="high"):
    t0 = time.time()
    with client.messages.stream(model=model, max_tokens=max_tokens, system=system, messages=[{"role": "user", "content": user}], output_config={"effort": effort}) as s:
        msg = s.get_final_message()
    text = "".join(b.text for b in msg.content if b.type == "text")
    LOG.append({"tag": tag, "model": model, "in": msg.usage.input_tokens, "out": msg.usage.output_tokens, "stop": msg.stop_reason, "secs": round(time.time() - t0)})
    print(f"[{tag}] {model} in={msg.usage.input_tokens} out={msg.usage.output_tokens} stop={msg.stop_reason} {time.time()-t0:.0f}s", flush=True)
    json.dump(LOG, open(os.path.join(OUT, "api-log.json"), "w"), indent=1)
    if msg.stop_reason == "max_tokens": print(f"WARNING: {tag} truncated at max_tokens", flush=True)
    return text

def body_only(text):
    t = text.strip()
    t = re.sub(r"^```(?:latex|tex)?\s*", "", t); t = re.sub(r"\s*```$", "", t)
    if "\\begin{abstract}" in t: t = t[t.index("\\begin{abstract}"):]
    if "\\end{document}" in t: t = t[:t.index("\\end{document}")]
    return t.strip() + "\n"

RULES = """You are drafting the body of a scientific report for Jude Castiel Johansen (Shockware Limited, independent researcher). Hard rules:
1. Every number, count, interval, token figure, date, model identifier and dollar amount you write MUST appear verbatim (or as an exact arithmetic restatement of two given counts, such as a percentage) in the RESULTS file. If a figure you want is not there, do not write it; say the quantity was not measured.
2. Do not invent instances, experiments, references, affiliations, prior results, mechanisms, or statements about what a model "knows" or "intends".
3. The work is exploratory; say so in the abstract and the reading. Use "non-inferior at ε = 0.05" only when the one-sided 95% lower bound exceeds −0.05. An interval containing zero is an unresolved difference, not equivalence. Report absolute rates alongside relative ones and state the non-degeneracy condition (best arm ≥ 0.1). Name the primary sample set for Phase 3 (post-screen W and A1) and say the choice was not preregistered.
4. Separate what the data show from interpretation; label interpretation as such. Keep the per-instance evidence visible. Eleven instances from two repositories is a small basis; say so.
5. The tables are provided in tables.tex with fixed labels (tab:p2inst, tab:p2con, tab:loo, tab:p3inst, tab:p3con). Do not reproduce tables; cite them with \\ref and place \\input{tables} once, at the start of the Results section.
6. British English, plain sentences, no em-dashes, no marketing language, no claims of novelty beyond what the prior publications (cited by DOI) and the evidence support. Escape % & _ outside math. Only macros from the preamble: \\eps is defined; \\texttt, \\emph, \\cite, \\ref, \\url, booktabs are available.
7. Output only the LaTeX body: start at \\begin{abstract} and stop before \\end{document}. No preamble, no \\documentclass, no \\maketitle, no code fences."""

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rounds", type=int, default=2); ap.add_argument("--start-body", default=None); ap.add_argument("--review-effort", default="medium"); a = ap.parse_args()
    results = read(os.path.join(OUT, "RESULTS.md")); prereg = read(os.path.join(ROOT, "preregistration.md")); tables = read(os.path.join(OUT, "tables.tex"))
    pilot_tex = read(os.path.join(ROOT, "pilot-paper", "main.tex")); stage1_tex = read(os.path.join(ROOT, "main.tex"))
    note_tex = read(os.path.join(ROOT, "..", "context-sufficiency-note", "paper", "main.tex"))
    notes = read(os.path.join(OUT, "REVIEWER-NOTES.md"))
    r0 = os.path.join(OUT, "round0", "review-r0.md")
    if os.path.exists(r0): notes += "\n\n## D. Pre-submission traps listed by the API reviewer on the first attempt (honour all of them)\n\n" + read(r0).split("## Pre-submission traps", 1)[-1]
    preamble = pilot_tex.split("\\begin{document}")[0]
    preamble = re.sub(r"\\title\{.*?\}\n", "\\\\title{" + TITLE.replace("\\", "\\\\") + "}\n", preamble, flags=re.S)
    preamble = re.sub(r"\\date\{.*?\}\n", "\\\\date{" + DATE.replace("\\", "\\\\") + "}\n", preamble, flags=re.S)
    writer_user = f"""Write the LaTeX body of the report titled "Load, Granularity and Reader Effects: Exploratory Ablations of ε-Sufficient Context for Language-Model Code Editing in Go (Phases 1 to 3)".

Sections in this order: Abstract (≤ 220 words); 1 Purpose and relation to the prior publications (definitions note concept DOI 10.5281/zenodo.23282195, pilot DOI 10.5281/zenodo.23307204, Stage 1 protocol DOI 10.5281/zenodo.23307547; hypotheses H1, H2, H5 as they appear in the preregistration); 2 Design (instances and screens by phase; arms with their exact construction rules; models and k; the task-text rule and its 2026-10-12 amendment; statistics; every amendment dated as in the preregistration); 3 Results (\\input{{tables}} first; then Phase 1, Phase 2, leave-one-out at k=100, Phase 3, each citing its table and stating the headline numbers in prose); 4 Reading of the evidence (what is supported and what is not: load degradation on headroom instances and why the pilot curve was flat; declaration-level slicing; granularity versus package selection and the non-additive necessity on cli 2bcdfbb1ac02; the cross-model asymmetry; the predictors; what this does and does not say about static computability); 5 Limitations and deviations (every data-integrity event; selection and k; hugo; two repositories; Sonnet k=10 granularity; the slice losses on caddy c8591a1e46e4 and 6727b2f3a92b; the sample-set choice); 6 Consequences for the registered report and future work (headroom screening for H1; declaration-level arms as candidate confirmatory arms; a load dose curve; a second dense model; instance scarcity; the obligation-graph idea as untested); 7 Availability (repository github.com/Shockware-Limited/suffbench-registered-report; harness/results-abl, results-p2, results-p2screen, results-p3; arm metadata in harness/abl-*/ and harness/ablr-*/contexts.json; analysis/phase23.py generates every number and analysis/phase23_tables.py every table); Acknowledgements and AI-use disclosure (\\section*): the author used Anthropic's Claude Fable 5.1 (referred to by the author as Lemma) through GitHub Copilot to design and run the phases and write the analysis scripts, and Claude Opus 5.5 through the Anthropic API to draft and adversarially review this report against the generated results file; the author is responsible for all claims. Bibliography as \\begin{{thebibliography}}{{9}} with only: the three Shockware DOIs; Joren et al. 2025 (ICLR) Sufficient Context: A New Lens on Retrieval Augmented Generation Systems; Du et al. 2025 (Findings of EMNLP) Context Length Alone Hurts LLM Performance Despite Perfect Retrieval; Liu et al. 2024 (TACL) Lost in the Middle; Gloaguen et al. 2026 (arXiv:2602.11988) Evaluating AGENTS.md. Target about 6 to 8 pages of prose plus the tables.

=== RESULTS FILE (the only source of numbers) ===
{results}

=== TABLES (already rendered; cite by label, do not copy) ===
{tables}

=== PREREGISTRATION (amendments and deviations; cite dates) ===
{prereg}

=== REVIEWER NOTES TO HONOUR ===
{notes}
"""
    if a.start_body: body = read(os.path.join(OUT, a.start_body))
    else:
        body = body_only(call(WRITER, RULES, writer_user, 64000, "write-r0"))
        open(os.path.join(OUT, "body-r0.tex"), "w", encoding="utf-8").write(body)
    for r in range(a.rounds):
        audit = number_audit(body, results + "\n" + tables); open(os.path.join(OUT, f"audit-r{r}.md"), "w", encoding="utf-8").write(audit)
        critic_user = f"""Adversarially review this LaTeX report body (the tables are in a separate file, included here for reference). You are a sceptical statistician and software-engineering reviewer. Produce a numbered list of REQUIRED edits, most severe first, each with the quoted offending text, the problem, and the exact replacement or deletion. Check: (a) every number against the RESULTS file and tables; (b) claims stronger than the evidence (intervals containing zero described as equivalence; "never", "always", "proves"; mechanisms stated as facts); (c) relative-versus-absolute confusion at floor or ceiling; (d) the one-sided decision bound used correctly and the primary sample set named; (e) preregistration amendments and deviations cited with the right dates; (f) anything that reads as invented (references, mechanisms, intentions); (g) consistency between tables and prose; (h) LaTeX that will not compile (unbalanced environments, undefined macros, unescaped % & _ outside math, undefined labels). Then OPTIONAL improvements. End with one line: PUBLISHABLE AFTER EDITS or NOT YET.

=== NUMBERS AUDIT (automated) ===
{audit}

=== RESULTS FILE ===
{results}

=== TABLES ===
{tables}

=== PREREGISTRATION ===
{prereg}

=== BODY ===
{body}
"""
        review = call(CRITIC, "You review scientific drafts for accuracy. Be exact and unsparing. Output only the review.", critic_user, 64000, f"review-r{r}", a.review_effort)
        open(os.path.join(OUT, f"review-r{r}.md"), "w", encoding="utf-8").write(review)
        if not review.strip(): print("WARNING: empty review text", flush=True)
        rev_user = f"""Apply every REQUIRED edit from the review to the body and return the complete corrected LaTeX body only (from \\begin{{abstract}} to just before \\end{{document}}). Where the review asks for a number that is not in the RESULTS file or the tables, remove the number rather than guess. Keep everything else unchanged.

=== REVIEW ===
{review}

=== NUMBERS AUDIT ===
{audit}

=== RESULTS FILE ===
{results}

=== TABLES ===
{tables}

=== BODY ===
{body}
"""
        body = body_only(call(WRITER, RULES, rev_user, 64000, f"revise-r{r+1}"))
        open(os.path.join(OUT, f"body-r{r+1}.tex"), "w", encoding="utf-8").write(body)
    final_audit = number_audit(body, results + "\n" + tables); open(os.path.join(OUT, "audit-final.md"), "w", encoding="utf-8").write(final_audit); print(final_audit[:1200])
    main_tex = preamble + "\\begin{document}\n\\maketitle\n\n" + body + "\n\\end{document}\n"
    open(os.path.join(OUT, "main.tex"), "w", encoding="utf-8").write(main_tex)
    chk_user = f"""Compare the new evidence (RESULTS file and the draft's abstract and reading section) against the three prior publications below and the preregistration. List every sentence in a prior publication that the new evidence contradicts, materially qualifies, or that is now known to be wrong (including the pilot cost and instance-count errata already recorded in the preregistration), quoting the sentence, naming the document, and proposing the exact erratum or amendment text. Then list anything in the preregistration's deviations section that is missing or inconsistent with the RESULTS file's data-integrity events. Be exhaustive but do not invent problems: if a statement is still correct, do not list it. Output Markdown with a heading per document.

=== RESULTS FILE ===
{results}

=== NEW DRAFT (abstract and reading section) ===
{extract(body, 'abstract')}
{extract(body, 'Reading of the evidence')}

=== DEFINITIONS NOTE (context-sufficiency-note/paper/main.tex) ===
{note_tex}

=== PILOT PAPER (pilot-paper/main.tex) ===
{pilot_tex}

=== STAGE 1 PROTOCOL (main.tex) ===
{stage1_tex}

=== PREREGISTRATION ===
{prereg}
"""
    errata = call(CHECKER, "You check scientific publications for statements that later evidence contradicts. Be exact; quote; propose text.", chk_user, 64000, "errata-check", a.review_effort)
    open(os.path.join(OUT, "ERRATA-CHECK.md"), "w", encoding="utf-8").write(errata)
    cost = sum((l["in"] * (4 if "opus" in l["model"] else 2) + l["out"] * (20 if "opus" in l["model"] else 10)) / 1e6 for l in LOG)
    print(f"API spend for the write-up (list prices, no caching): ${cost:.2f}")

def extract(tex, key):
    if key == "abstract":
        m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S); return m.group(1) if m else ""
    m = re.search(r"\\section\{[^}]*" + re.escape(key) + r"[^}]*\}(.*?)(?=\\section\{|\\section\*\{|\\begin\{thebibliography\})", tex, re.S); return m.group(0) if m else ""

def number_audit(tex, results):
    body = re.sub(r"%.*", "", tex)
    nums = set(re.findall(r"(?<![\w.$])[+−-]?\d+\.\d{2,3}(?![\d.])", body)) | set(re.findall(r"\b\d{1,3}(?:,\d{3})+\b", body)) | set(re.findall(r"\\\$\d+(?:\.\d+)?", body))
    res = results.replace("−", "-"); miss = []
    for n in sorted(nums):
        k = n.replace("−", "-").lstrip("+").replace("\\$", "$")
        if k.lstrip("-") not in res and k not in res: miss.append(n)
    return "Numbers in the body (decimals with 2-3 places, comma-grouped integers, dollar amounts) not found in RESULTS.md or tables.tex:\n" + ("\n".join(f"- {m}" for m in miss) if miss else "- none") + f"\n({len(nums)} distinct numbers checked)\n"

if __name__ == "__main__":
    main()
