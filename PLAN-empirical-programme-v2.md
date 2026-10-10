# PLAN v2: Proving ε-sufficient context empirically at minimum cost

Revised after an independent review (21 literature searches, power and budget recomputed).
Status: proposal. Nothing run. Cash cap about $1,000; solo author; laptop with WSL2.

## 0. What the review changed

| Issue found | Decision |
|---|---|
| Padded arms (2× and 4× the 150k transitive slice) exceed model windows; A3 "to 128k" smaller than A2 | Load curve rebuilt on a SMALL fully-covered base (A1, ~15–40k) at fixed absolute loads {base, 32k, 64k, 128k, 200k}; every point fits every model |
| Stubbing packages with panics + ddmin reduces to package coverage; spot-check of "outside" packages vacuous (statically linked test binaries) | Oracle slice = `go test -coverpkg` over the test-binary import closure (cheap, honest) PLUS a mutation-based semantic slice (a package is in the slice iff some mutant in it flips a verdict), reusing the existing mutator. Hypothesis 2 restated as a static closure check |
| Non-inferiority test at ε=0.05, n=100, temperature 0: 30–45% power; "best-of" comparator has winner's curse; McNemar is a superiority test | Pre-specified comparators (A1-bodies, A2); intersection–union non-inferiority with a paired score interval; k=3 samples per cell on the C2 arms; ε justified against the measured temperature-0 flip rate; n ≥ 300 screened instances across repos; Holm correction across claims |
| A1 vs A2 confounds five things | Add A1-bodies (same package set as A1, bodies instead of interfaces) so interfaces-vs-bodies and scope are separate contrasts |
| Parametric memory of cli/cli | Add A∅ (task text only) arm; identifier-renaming control on a subset |
| Padding from same repo is not neutral (sibling commands are templates) | Padding drawn from outside the test-binary closure with a lexical-similarity ceiling; plus cross-repo Go padding and neutral (whitespace/masked) padding; W position fixed across arms |
| One repo yields ~40–50 PR-text instances, ~10–25 issue-text; pilot consumes some | Mine 5–8 single-module Go repos from day 1; reuse Multi-SWE-bench harness (it already ships cli/cli); pilot instances disjoint from confirmatory set |
| PR bodies leak the fix; fail-to-pass tests referencing new identifiers are unsolvable | Issue text only, or LLM-rewritten behaviour-only spec hand-checked; exclude instances whose fail-to-pass tests reference gold-patch identifiers, or supply those signatures as spec (ties to W_I); manual underspecification screen |
| C3 conditioned on Δ-pass is biased and has 2–4 events per arm | Unconditional outcome "Δ-pass AND frame-pass"; oversample shared-helper write-sets; otherwise C3 is descriptive. Positioned against TDAD (2603.17973), which already showed impact maps cut regressions 6.1%→1.8% |
| Interim stopping spends almost no α and saves little | Dropped. Fixed n, pre-registered contrast hierarchy |
| Token arithmetic 4× low; prompt caching mostly unavailable | Recomputed below |
| "Publish as you go" risks salami slicing and being scooped by a funded team | No separate pilot paper; pilot goes into the preregistration appendix. Submit as a REGISTERED REPORT (MSR / ESEM / EMSE RR track): in-principle acceptance before data collection is the dated, peer-reviewed priority claim. Embargo OSF and dataset until submission. Anonymised artefact copies |

## 1. Claims (unchanged in substance, sharpened)

- C1 Degradation curve. At verified fixed coverage, success vs absolute load {base…200k}, per model, with intervals, three padding types.
- C2 Interface sufficiency (P1). Interface context A1 is non-inferior (margin ε, pre-justified) to A1-bodies and to A2, population-average over instances, k=3 samples. Estimand stated as population-level; per-instance ε-sufficiency only on the k>1 subset.
- C3 Forward slice. Descriptive unless shared-helper oversampling yields power: "Δ-pass AND frame-pass" A1 vs A1F.
- C4 Cost. Tokens per arm; A1 vs A4 at matched (A1) budget and at one large budget.
Coverage is defined OPERATIONALLY per arm: the gold patch's referenced identifiers, declarations and packages are present in the context (checked mechanically, per instance, as Sam-Bodden does). New-import cases flagged.

## 2. Dataset: SuffBench v0.1

- 5–8 active single-module Go repos with green Linux baselines; Multi-SWE-bench harness and Docker reused and cited.
- Post-cutoff commits only (cutoffs recorded per model). Target ≥300 screened instances; ~30 disjoint pilot instances.
- Per instance: task text (issue-only or rewritten spec, source recorded), gold patch, W, W_I flag, fail-to-pass set (compiling at parent), pass-to-pass set, coverage slice, mutation slice, static closure check, expressibility check per arm.
- Manual screen ~10 min/instance (~50 h).
- Release under embargo until submission; Zenodo dataset DOI at submission.

## 3. Arms

A∅ task only | A0 W bodies | A1 W + interfaces of deps(W) | A1-bodies | A1F = A1 + interfaces and test names of F(W) | A2 transitive slice with tests | A4s lexical retrieval at A1 budget | A4l lexical retrieval at a large budget | Curve: A1 padded to 32k, 64k, 128k, 200k with three padding types (on cheap models; two points on the frontier model).
Protocol: temperature 0 (k=3 on C2 arms), search/replace edit format, one format-repair turn only, pinned provider and quantisation, W position fixed. Verification two-stage on WSL2 (ext4), 3× clean reruns for flake control.

## 4. Budget (recomputed; API rates to be checked live before commit)

| Item | Estimate |
|---|---|
| Two open-weights models, all arms, 300 instances (~0.8M input tokens per instance per model, plus k=3 on C2 arms) | $250–$600 |
| Frontier model on a stratified 100-instance subset: A1, A1-bodies, A2, two curve points, k=3 on C2 arms, thinking output | $300–$500 |
| Pilot, variance subset, repair turns | $30–$60 |
| Verification, slices, mining | $0 (WSL2), ~150 laptop-hours |
| Two critic reviews | ~$10 |
| Total | $600–$1,150 |
Levers if over: frontier on 60 instances; drop one curve point; one padding type on the frontier model. Floor ~$450.

## 5. Timeline (~3.5 months part-time)

| Weeks | Work | Artefact |
|---|---|---|
| 1 | Note v1.1 citing the 2026 work (Sam-Bodden, Xue, Mohammadi, Agent Retrieval Bench, TDAD, Jia/Barr/Mechtaev, HCP, Du et al., Joren, Multi-SWE-bench); WSL2; miner on Multi-SWE-bench harness | Zenodo v1.1 |
| 2–5 | Mine 5–8 repos; screen; slices; expressibility checks | Dataset (embargoed) |
| 6–7 | Harness; pilot (30 disjoint instances, one cheap model, all arms); measure temperature-0 flip rate; power analysis; critic review #1 | OSF preregistration (embargoed) → Registered Report stage 1 submission |
| 8–10 | Full run after in-principle acceptance (or in parallel if the venue timeline is long) | — |
| 11–14 | Analysis; paper; critic review #2; checker + context compiler emitting A1/A1F contexts | Stage 2 paper; dataset DOI public; tool release |

## 6. Honest novelty position

- Dataset with verified slices and frame sets: partly anticipated (SWE-bench pass-to-pass; Multi-SWE-bench; ContextBench; OCD/SWEzze editor-side minimal context; TDAD). Residual: oracle-side, verdict-based slices with expressibility checks, in Go, post-cutoff.
- Degradation curve at fixed coverage: partly anticipated (Du et al. 2510.05381 with neutral padding; LongCodeBench; Xue). Residual: repository editing with oracle localisation and verified coverage, per model, with intervals.
- Forward slice vs frame failures: largely anticipated by TDAD. Residual: single-shot setting, shared-helper stratification, Go. Descriptive.
- ε-sufficiency as preregistered non-inferiority tied to a formal definition: novel as framing; credited as rigour if powered.
- Interfaces suffice in a typed language via type-graph interfaces: a replication (HCP, Sam-Bodden, CatCoder, Blinn et al.), legitimate as such.
Headline therefore: C1 and C2, preregistered, multi-repo, powered. C3 and the dataset are supporting contributions.

## 7. Where it can be published

As a Registered Report at MSR, ESEM, or EMSE: estimated 40–50% in-principle acceptance with the power analysis. Main track ICSE/FSE/ASE with the fixes: 15–25%, ASE or ICSME more realistic. MSR Data/Tool showcase for the dataset: 35–45%. Workshop (LLM4Code, FORGE): ~60%.
