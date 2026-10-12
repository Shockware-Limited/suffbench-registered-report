# Preregistration (embargoed draft) — Interfaces or bodies? A test of ε-sufficient context for LM code editing in Go

To be registered on OSF (embargoed) at the time of the MSR 2027 Registered Reports Stage 1 submission, and unembargoed on in-principle acceptance. This text mirrors the Stage 1 report; the report is authoritative.

## 1. Study information
- Title: as above.
- Authors: Jude Castiel Johansen (Shockware Limited, independent researcher).
- Description: a paired, multi-model, single-shot code-editing study that operationalises ε-sufficient context (DOI 10.5281/zenodo.23282196) as a non-inferiority test of a compiler-computed interface context against bodies and against the transitive slice, with a degradation curve at verified fixed coverage, a descriptive forward-slice contrast, and token costs.

## 2. Hypotheses (confirmatory unless marked)
- H2 (primary): A1 is non-inferior to A1b and to A2 at margin ε on Δ-pass (intersection–union).
- H1 (revised 2026-10-11): at each load level L ∈ {200k, 400k, 950k} and padding type, (a) one-sided paired superiority of A1 over A1 padded to L (degradation) and (b) TOST equivalence at ±0.05 (flatness); outcomes per level: degradation / flat / inconclusive, all reportable. Full curve at {base, 64k, 200k, 400k, 700k, 950k} reported with intervals.
- H3 (descriptive): Δ-pass-and-frame-pass, A1F vs A1, overall and by shared-helper stratum.
- H4 (descriptive): tokens, latency, cost per arm.
- Control: A∅ (task only) per repository.

## 3. Design plan
- Within-instance (paired) design (revised 2026-10-11): dense cheap model (Haiku 5.5 class) on every arm within its window, k=10; one open-weights 1M-window model at temperature 0 on every arm, k=3 on A∅/A1/A1b/A2 and k=1 on padded and retrieval arms; frontier model (Opus 5 class) on A∅ for all instances (the screen) and on A1, A1b, A2, P200 over a stratified 100-instance subset (strata: repository × write-set size; seed 20261120), P950 over a 30-instance sub-subset. Confirmatory H2 is carried by the dense and open-weights models; the frontier replication is descriptive.
- Blinding: the analysis script is written and frozen before the confirmatory run; outcomes are computed mechanically by tests.
- Randomisation: order of arms within an instance is irrelevant (independent calls); provider and quantisation pinned.

## 4. Sampling plan
- Population: fail-to-pass commits after the latest documented cutoff of the evaluated models, in 5–8 single-module Go repositories with green Linux baselines.
- Exclusions: fail-to-pass tests that do not compile at the parent; tests referencing identifiers introduced by the gold patch (unless signatures supplied, flagged); flaky tests (fail ≥1 of 3 clean reruns); under-specified or leaking task text (manual screen).
- Sample size (revised 2026-10-11): ≥200 confirmatory instances (stretch 300) after manual screening and the task-only screen; the 24-instance pilot (DOI 10.5281/zenodo.23307204) is disjoint and not reused. Power from pilot per-instance SDs: dense model ε=0.05, σ=0.083 (A1−A1b, Haiku) → >0.99 at n=200 (still >0.99 at σ=0.35); open-weights ε=0.075, σ between 0.26 and 0.42 (Sonnet P200−A1, all / screened instances) → 0.99 to 0.81 at n=200. Frontier subset n=100: 0.56 at σ=0.42, hence descriptive. Stopping rule: none; fixed n. If fewer than 200 survive after the tenth listed repository, run on the survivors and report the implied power.
- Margin (revised 2026-10-11 after the pilot, DOI 10.5281/zenodo.23307204): cell non-unanimity (0.25 on Haiku at k=10) is not usable as a margin basis. ε is set from the standard deviation of per-instance paired differences observed in the pilot: ε = 0.05 for the dense model (σ ≈ 0.11, n required ≈ 30 at 80% power) and ε = 0.075 for models run at k=3 (σ ≈ 0.25, n ≈ 69). Fixed here before the confirmatory run; no further change without a dated note.
- Screening (added 2026-10-11): the task-only arm is run first on the strongest evaluated model (k=3); any instance solved at least once is excluded from the confirmatory set and reported separately. In the pilot this removed 14 of 24 instances for Sonnet 5.5.
- Load range (revised 2026-10-11): padding levels 64k, 200k, 400k, 700k, 950k; a flat curve is an admissible outcome.

## 5. Variables
- Manipulated: context arm (A∅, A0, A1, A1b, A1F, A2, A4s, A4l, P64, P200, P400, P700, P950 × 3 padding types: same-repository code outside W∪B∪F with directory-proximity ceiling, cross-repository Go from a fixed listed repository, Go release-note prose).
- Measured: applied; Δ-pass; frame-pass; tokens in/out; latency; expressibility per arm; W_I flag; shared-helper flag; task-text source; cutoff flags.
- Indices: Δ-pass-and-frame-pass; tokens ratio A1/A2, A1/A4l.

## 6. Analysis plan
- Paired difference of proportions per contrast with a paired score (Tango/Newcombe) interval; Wilson intervals on all proportions; bootstrap over instances alongside.
- H2 (revised 2026-10-11): intersection–union; both lower bounds of the instance-level percentile bootstrap (2,000 resamples, seed 1, 95% two-sided) of the mean per-instance difference > −ε; level α=0.05 without further adjustment, tested first and alone. Tango score interval on majority outcomes reported alongside. H1: per model, one Holm family of nine superiority tests (3 levels × 3 padding types) at α=0.05; TOST at ±0.05 per level reported uncorrected as the pre-specified reading of a null superiority result. Instance set per (model, level) fixed before any call as the instances where that arm can be built.
- Per-instance ε-sufficiency only on cells with k = 3 samples; reported descriptively.
- Subgroup analyses (pre-specified, descriptive): by repository; by task-text source; by W_I; by shared-helper; by expressibility.
- Missing data: unapplied patches count as failures; API errors are retried three times then recorded as missing and excluded from that arm's pair with the instance flagged.
- Inference criteria: one-sided α = 0.05; H2 unadjusted (intersection–union), H1 after Holm within its nine-test family per model. No change to any item above after the first confirmatory model call; earlier changes are dated here.

## 7. Exploratory analyses
- Degradation curve shape per model; interaction of padding type with model; per-repository parametric-memory rate.

## 8. Deviations
Any deviation from this plan will be reported in a dedicated section of the Stage 2 paper with the reason and its date.
