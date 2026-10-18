# Reviewer notes to honour in the write-up (prior critiques, verbatim where possible)

## A. Independent adversarial critique of the Phase 1 result (2026-10-12, Claude agent run by the author)

- The W/A1g/A1t distinction in Phase 1 rested on a single instance (babd691446b9); without it W was non-inferior to A1.
- The 33/135 necessity counts were indistinguishable from binomial noise (null simulation expected 30.8 necessary, 30.5 helps); the shared A1 cell induces instance-level clustering.
- Aliasing: 16/23 (A1g) and 15/23 (A1t) paired differences were exactly zero (ceiling/floor); report sign tests alongside the bootstrap.
- Non-inferiority logic: the table used a two-sided interval where the preregistration specifies one-sided α = 0.05; bootstrap seed differs from the text.
- ε = 0.05 equals the model's day-to-day shift (A1 drift −0.041).
- A1t's package-name rule matched English words (context, source, text, status, extension, artifact, verification, variable).
- A1g is an oracle by construction.
- Serialisation always places W last; recency confounded with arm size but consistent across arms.
- The repair of the Phase 1 verdicts (re-verification from stored responses with patch-hash equality) is sound.

## B. External critique of the Phase 2 summary (2026-10-13)

- "A1 never beats W" contradicted the examples (cli 2bcd 0→0.27; caddy c8591 Sonnet 0.60 vs 0.20). Say "no average advantage on the point estimate" if that is meant.
- Near-zero averages with wide intervals do not establish equivalence; positive and negative task effects can cancel.
- Floor performance is not evidence of useful sufficiency; report relative performance, absolute success, and whether the task permits a comparison separately. "The predictor correctly selected nothing" is too strong when every arm fails.
- Opus had no A1 arm; its result concerns A1t versus W at five trials per arm. Repeated runs do not create independent tasks; ten instances from two repositories is a small basis.
- Cutting LOO: acceptable as an explicitly exploratory budget decision, but removing a distracting dependency could raise performance on a floor instance, so the cut loses the ability to detect rescue effects; preserve completed samples; label the subset.
- LOO establishes the effect of removing one dependency while all others remain; it cannot identify a minimal sufficient subset (redundancy, interaction).
- A k=5 screen can only yield rates 0, 0.2, ..., 1.0; a true 20% task gives 0/5 about a third of the time; use triage then further screening; evaluate retained tasks on fresh runs and distinguish the enriched population from the mining population.
- Suggested defensible conclusion: "Across ten screened tasks from two repositories, we detected no clear average advantage from adding dependency interfaces. Individual task–model comparisons showed both benefits and harms. Seven tasks were near floor on the primary model, limiting inference. The tested static selectors missed a clear dependency-sensitive case, so their ability to recover sufficient context remains unestablished."
- On making dependencies explicit in a graph of obligations: the critical test is whether the graph can be built before seeing the solution; a gold-derived graph is an oracle diagnostic only; explicit dependency does not imply mandatory inclusion; separate structural relevance, reader need, and presentation.

## C. Points the author asked to keep in view

- Only report novelty that is in the data; publish regardless of outcome; the pilot, note and Stage 1 protocol are already public with DOIs.
- The AI-use disclosure must be present and accurate.
