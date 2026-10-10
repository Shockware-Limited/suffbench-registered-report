# Registered Report, Stage 1 — MSR 2027 Registered Reports track (with EMSE)

**Status: draft v0.1, not submitted. Embargoed. Private repository.**

| Date | Item |
|---|---|
| 13 Nov 2026 | Abstract registration on HotCRP (https://msr2027-registered-reports.hotcrp.com) |
| 20 Nov 2026 | Initial report: 6 pages + 1 page references, IEEE conference format, PDF |
| 23 Dec 2026 | Reviews returned |
| 15 Jan 2027 | Response letter + revised report (12 + 1 pages) |
| 4 Feb 2027 | Stage 1 notification (in-principle acceptance) |
| by 28 Feb 2027 | Preprint with DOI required |
| 26–27 Apr 2027 | MSR 2027, Dublin: in-person presentation required |
| by 30 Sep 2027 | Stage 2 full paper to EMSE |

Track page: https://2027.msrconf.org/track/msr-2027-registered-reports (single-anonymous review; deadlines AoE).

## Files

- `main.tex`, `refs.bib`: the report (IEEEtran). Build: `tectonic main.tex`.
- `analysis/power.py`: power and sample size for the paired non-inferiority test.
- `preregistration.md`: OSF-style preregistration text (embargoed until submission).
- `PLAN-empirical-programme-v2.md`: the reviewed design this report is written from.

## Before 20 November

1. Run the 30-instance pilot on one open-weights model (budget under $60) to measure the temperature-0 flip rate and the between-arm disagreement rate; insert into §V and fix ε.
2. Confirm the repository list (5–8 Go repos) and the mined instance count; if under 300, state the fallback.
3. Record documented training cutoffs for the three candidate models.
4. Second critic review of the draft.
5. Author's read; check the AI-use disclosure is true; submit.

## Embargo

Do not post the design, the dataset, or the pilot publicly before the Stage 1 submission is in. The MSR RR track requires a preprint with DOI only after in-principle acceptance.
