# Preregistration (embargoed draft) — Interfaces or bodies? A test of ε-sufficient context for LM code editing in Go

To be registered on OSF (embargoed) at the time of the MSR 2027 Registered Reports Stage 1 submission, and unembargoed on in-principle acceptance. This text mirrors the Stage 1 report; the report is authoritative.

## 1. Study information
- Title: as above.
- Authors: Jude Castiel Johansen (Shockware Limited, independent researcher).
- Description: a paired, multi-model, single-shot code-editing study that operationalises ε-sufficient context (DOI 10.5281/zenodo.23282196) as a non-inferiority test of a compiler-computed interface context against bodies and against the transitive slice, with a degradation curve at verified fixed coverage, a descriptive forward-slice contrast, and token costs.

## 2. Hypotheses (confirmatory unless marked)
- H2 (primary): A1 is non-inferior to A1b and to A2 at margin ε on Δ-pass (intersection–union).
- H1: Δ-pass at P128 and P200 is lower than at A1 (one-sided), per padding type.
- H3 (descriptive): Δ-pass-and-frame-pass, A1F vs A1, overall and by shared-helper stratum.
- H4 (descriptive): tokens, latency, cost per arm.
- Control: A∅ (task only) per repository.

## 3. Design plan
- Within-instance (paired) design; every instance receives every arm on the open-weights models; frontier model on A1, A1b, A2, P128, P200, A∅ over a stratified 100-instance subset.
- Blinding: the analysis script is written and frozen before the confirmatory run; outcomes are computed mechanically by tests.
- Randomisation: order of arms within an instance is irrelevant (independent calls); provider and quantisation pinned.

## 4. Sampling plan
- Population: fail-to-pass commits after the latest documented cutoff of the evaluated models, in 5–8 single-module Go repositories with green Linux baselines.
- Exclusions: fail-to-pass tests that do not compile at the parent; tests referencing identifiers introduced by the gold patch (unless signatures supplied, flagged); flaky tests (fail ≥1 of 3 clean reruns); under-specified or leaking task text (manual screen).
- Sample size: ≥300 confirmatory instances; 30 disjoint pilot instances. Justification: with n = 300, one-sided α = 0.05, π_d = 0.2, power at true difference 0 is 0.90 for ε = 0.075 and 0.61 for ε = 0.05 (analysis/power.py). Stopping rule: none; fixed n.
- Margin (revised 2026-10-11 after the pilot, DOI 10.5281/zenodo.23307204): cell non-unanimity (0.25 on Haiku at k=10) is not usable as a margin basis. ε is set from the standard deviation of per-instance paired differences observed in the pilot: ε = 0.05 for the dense model (σ ≈ 0.11, n required ≈ 30 at 80% power) and ε = 0.075 for models run at k=3 (σ ≈ 0.25, n ≈ 69). Fixed here before the confirmatory run; no further change without a dated note.
- Screening (added 2026-10-11): the task-only arm is run first on the strongest evaluated model (k=3); any instance solved at least once is excluded from the confirmatory set and reported separately. In the pilot this removed 14 of 24 instances for Sonnet 5.5.
- Load range (revised 2026-10-11): padding levels 64k, 200k, 400k, 700k, 950k; a flat curve is an admissible outcome.

## 5. Variables
- Manipulated: context arm (A∅, A0, A1, A1b, A1F, A2, A4s, A4l, P32, P64, P128, P200 × 3 padding types).
- Measured: applied; Δ-pass; frame-pass; tokens in/out; latency; expressibility per arm; W_I flag; shared-helper flag; task-text source; cutoff flags.
- Indices: Δ-pass-and-frame-pass; tokens ratio A1/A2, A1/A4l.

## 6. Analysis plan
- Paired difference of proportions per contrast with a paired score (Tango/Newcombe) interval; Wilson intervals on all proportions; bootstrap over instances alongside.
- H2: both lower bounds > −ε. H1: upper bound of (P_k − A1) < 0. Holm correction per model over the confirmatory family.
- Per-instance ε-sufficiency only on cells with k = 3 samples; reported descriptively.
- Subgroup analyses (pre-specified, descriptive): by repository; by task-text source; by W_I; by shared-helper; by expressibility.
- Missing data: unapplied patches count as failures; API errors are retried three times then recorded as missing and excluded from that arm's pair with the instance flagged.
- Inference criteria: one-sided α = 0.05 after Holm.

## 7. Exploratory analyses
- Degradation curve shape per model; interaction of padding type with model; per-repository parametric-memory rate.

## 8. Deviations
Any deviation from this plan will be reported in a dedicated section of the Stage 2 paper with the reason and its date.
