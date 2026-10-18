# Handoff: Phase 1 to 3 exploratory report (publication package)

Directory: `suffbench-registered-report/phase23-report/`. Everything here was produced on 2026-10-18 from data collected 2026-10-12 to 2026-10-14. No new experiment was run for the write-up.

## How the report was produced

1. `analysis/phase23.py` computes every number from the verdict records and arm metadata into `RESULTS.md` / `RESULTS.json`.
2. `analysis/phase23_tables.py` renders every table from `RESULTS.json` into `tables.tex`.
3. `analysis/writeup.py` drafts the LaTeX body with Claude Opus 5.5 through the Anthropic API under hard rules (numbers only from `RESULTS.md`; exploratory framing; one-sided bound stated), then runs an adversarial review (Opus 5.5), an automated numbers audit, a revision, and a cross-check of the three prior publications against the new evidence (Sonnet 5.5, `ERRATA-CHECK.md`).
4. Five passes were run. Pass 1 (`round0/`) was truncated by the output budget. Pass 2 (`round1/`) produced the draft but the reviews came back empty (the reviewer consumed its budget thinking). Pass 3 (`round2/`) was the first real review: 11 required edits, applied; it also found a per-record rounding error in the by-model spend summary, fixed in `analysis/phase23.py`. Pass 4 (`round3/`) found 19 required edits (unescaped `$`, a stale spend discrepancy, padding not matched on two caddy instances, pilot-instance reuse undisclosed, H5b on Phase 3 computable but not computed, "same-day" overstated, and others), applied; the A1t contrasts and the padding-match facts were then added to the results file and the preregistration gained a dated 2026-10-18 deviations entry. Pass 5 (top level: `review-r0.md`, `audit-r0.md`, `audit-final.md`) returned PUBLISHABLE AFTER EDITS with 17 required edits, which the revision step applied into `main.tex`.
5. The whole write-up cost about $9 in API calls (`api-log.json` per pass).

## Contents

| File | What it is |
|---|---|
| `main.tex`, `main.pdf` | The report (pilot-paper preamble; body from the final revision) |
| `tables.tex` | Every table, generated |
| `RESULTS.md`, `RESULTS.json` | Every number, generated |
| `review-r0.md`, `audit-r0.md`, `audit-final.md` | Final pass: review, pre-revision audit, post-revision audit |
| `ERRATA-CHECK.md` | Prior-publication cross-check from the final pass |
| `round0/ round1/ round2/ round3/` | Earlier passes (reviews, audits, bodies, logs) |
| `REVIEWER-NOTES.md` | Prior critiques fed to the writer |
| `zenodo-metadata.json` | Deposition metadata |
| `HANDOFF.md` | This file |

## Before publishing (author checklist)

1. Cold read `main.pdf`. Priority: abstract, section 4 (reading), section 5 (limitations and deviations), the AI-use disclosure, and every sentence that says "supported".
2. Read `review-r0.md` to the end. If its verdict is NOT YET, the remaining required edits were applied by the revision step; spot-check three of them in `main.tex`. Any edit you disagree with is yours to revert.
3. Confirm `audit-final.md` lists no numbers.
4. Reproduce: `python analysis/phase23.py && python analysis/phase23_tables.py` must leave `RESULTS.md` and `tables.tex` unchanged.
5. Read `ERRATA-CHECK.md`. Items for the pilot paper (instance count 24 to 23, cost $61 to $73, the recomputed Haiku rows, the padding figure, the task-only denominators, the Opus/Sonnet subset of 9) belong in an erratum note on the pilot's Zenodo record and the suffbench README. Items for the Stage 1 protocol (headroom screening for H1, the decision-bound wording in §6, declaration-level arms) belong in the protocol revision before submission. The definitions note needs no correction unless the check says otherwise.
6. Commit and tag `v0.2.0-phase123`; push.
7. Zenodo: upload `main.pdf`, `RESULTS.md`, `RESULTS.json`, `tables.tex`, and a zip of `harness/results-abl`, `harness/results-p2`, `harness/results-p2screen`, `harness/results-p3` plus the `contexts.json` files; metadata from `zenodo-metadata.json`. Mint the DOI, add it to the Availability section, recompile, upload the final PDF.
8. Optional: OpenTimestamps the final PDF.
9. Update the READMEs of `suffbench-registered-report` and `suffbench` with the DOI and one sentence on the findings.

## What the report claims, in one paragraph

Exploratory; no confirmatory claim. On eleven screened instances from cli/cli and caddy with headroom, Haiku 5.5 pass rates were lower with inert same-module padding added to the write-set (Wpad − W −0.138 [−0.281, −0.018]) while the same budget of real dependency interfaces was not resolved from zero; token matching failed on the two largest caddy instances. A declaration-level slice of the write-set met the non-inferiority margin against W only under a post-hoc sample-set choice and the one-sided bound (lower bound −0.043, median token ratio 0.47); with screen samples included or under the two-sided lower end it did not. On the one cli instance with a necessary dependency, referenced dependency declarations (4,443 tokens) outperformed whole-package interfaces of the predicted packages, and single-dependency necessity was non-additive. Sonnet 5.5 was at ceiling on most instances and its point estimates were below W for the sliced arms at k = 10. Two data-integrity incidents (repaired, documented), reuse of pilot instances, and a screen designated after the data were seen limit all of this to hypothesis generation for the registered report.

## Not done, by decision

- No Zenodo upload or DOI minting (needs the author's token).
- No change to the published definitions note, pilot paper or Stage 1 PDFs; proposed errata are in `ERRATA-CHECK.md`.
- Relaxed mining of caddy, hugo and cli was never rerun after the disk incident.
- Amendment (iv) of 2026-10-13 (set-level precision and recall of the task-text predictor) was not performed; recorded as a deviation.
