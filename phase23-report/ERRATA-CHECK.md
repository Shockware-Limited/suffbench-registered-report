# Contradiction check: Phase 1–3 evidence against the prior publications and the preregistration

Scope: I list only sentences the RESULTS file or the preregistration errata contradict, materially qualify, or show to be wrong. Anything not listed is still correct.

Where the 2026-10-12 pilot erratum already gives recomputed values, I use them. Where it does not (write-set contrast, Sonnet and Opus rows, standard deviations), I mark "recompute" rather than invent numbers.

## Pilot paper (DOI 10.5281/zenodo.23307204)

**P1. Instance count (Title, Abstract, Results, Table 1, Tables, Availability).**
- Quotes: "A 24-Instance Pilot Measurement of…", "24 fail-to-pass instances were obtained", "Sonnet solved 14 of 24 instances at least once from the task text alone, Haiku 4 of 24", "Sonnet solved 14 of 24 (0.44, $k=3$)".
- Problem: cli__cli-0c2eea6338a2 had an empty task text and scored 0 on every arm and model. It is invalid, so 23 instances are valid.
- Proposed erratum: "Erratum (2026-10-12): instance cli__cli-0c2eea6338a2 was run with an empty task text and scored 0 on every arm and model; it is invalid. All instance counts of 24 should read 23 valid instances (24 obtained). Sonnet 5.5 solved 14 of 23 instances from the task text alone; Haiku 5.5 solved 4 of 23. Pooled rates, the $\pi_d$ denominators (/24), the 22/24 and 7/9 within-$\eps$ counts, and all other per-instance counts are to be recomputed on 23 instances in the released script."

**P2. Headline Haiku contrasts (Abstract and Results).**
- Quote: "the interface context had a higher pass rate than bodies by $+0.04$ [$+0.01$, $+0.08$]…" and, in Results, "$+0.042$ [$+0.012$, $+0.075$]".
- Proposed erratum: "Recomputed on 23 instances: A1 $\Delta$-pass 0.674 [0.491, 0.843] (was 0.646); A1$-$A1b $+0.043$ [$+0.013$, $+0.078$] (was $+0.042$ [$+0.012$, $+0.075$]). The rounded abstract values are unchanged. Table 1 rows other than A1 and the A1$-$W, A1$-$A1F contrasts are to be recomputed."

**P3. Padding contrast (Abstract and Results).**
- Quote: "Padding A1 to 200k tokens changed the pass rate by $-0.03$ [$-0.15$, $+0.09$] on Haiku".
- Proposed erratum: "Recomputed on 23 instances: $-0.029$ [$-0.129$, $+0.081$]. The Sonnet ($+0.04$) and Opus ($+0.07$) intervals and the Table 2 rows are to be recomputed. Sonnet scored 0 on the invalid instance task-only, so it falls in Opus's 10-instance subset (the effective n is 9)."

**P4. Cost (Abstract and Cost paragraph).**
- Quotes: "The whole measurement cost about \$61 in API calls at list prices." and "Haiku 5.5: \$0.10 / \$0.50 per million input / output tokens, cache reads \$0.01" … "about \$4.71".
- Problem: Haiku 5.5 is billed at a higher rate for prompts above 100k tokens, and 697 of 2,256 Haiku calls were above it. The RESULTS file records about $73.
- Proposed erratum: "Haiku 5.5 is billed at a higher rate for prompts above 100k tokens; 697 of 2,256 Haiku calls exceeded it. The Haiku arm cost about \$16.44, not \$4.71, and the whole pilot about \$73 (Haiku \$16.44, Sonnet \$29.16, Opus \$27.00), not \$61. The listed Haiku prices apply to prompts of 100k tokens or fewer."

**P5. Task-text writing (Instances section).**
- Quote: "a behaviour-only specification was written by Claude Haiku~5.5 … the author reviewed the rewritten ones before release."
- Problem: for one rewritten instance, `rewritten_spec` produced no text, and the review did not catch it.
- Proposed amendment: "One of the 11 rewritten specifications was empty (instance 0c2eea6338a2) and was not caught in review; ten valid rewritten specifications remain. A non-empty-task-text check has been added to mining."

**P6. Interfaces versus write-set alone (Abstract and Results; materially qualified).**
- Quote: "than the write-set alone by $+0.07$ [$+0.02$, $+0.13$]".
- Evidence: Phase 1 re-measured this on 23 instances at k=20. W$-$A1 was $-0.028$ [$-0.096$, $+0.017$], with one-sided lower bound $-0.083$ (not non-inferior) and signs 4/4/15. Phase 1 also found A1 itself shifted by $-0.041$ [$-0.074$, $-0.013$] between the pilot (k=10) and Phase 1 (k=20), so the pilot's A1 level is not stable across runs. The difference is carried by one instance (babd691446b9). Phase 2 (W$-$A1 $+0.000$) and Phase 3 (A1$-$W $+0.039$ [$-0.076$, $+0.185$]) did not resolve it either.
- Proposed amendment: "Subsequent exploratory re-measurement (Phase 1, 23 instances, k=20) estimated A1 minus the write-set alone at $+0.028$ [$-0.017$, $+0.096$] (two-sided), carried by one instance, and A1 itself fell by 0.041 [0.013, 0.074] relative to this pilot's cell values. The pilot's $+0.067$ is a post-hoc-selected contrast and should not be read as a replicated advantage of interfaces over the write-set alone."

**P7. Flat degradation curve (Abstract, Results, "What this changes" item 3; materially qualified).**
- Quotes: "so the degradation curve is flat within the resolution of this pilot", "Within this pilot's resolution the average degradation curve $g$ is flat from 40k to 200k tokens", and "H1 … found no consistent effect up to 200k on this task class".
- Evidence:
  - The pilot's instances were mostly ceiling or floor (Phase 1: 8 with W and A1 both at 1.0, 5 both at 0.0).
  - In Phase 3, on 11 instances with headroom (screen rate in [0.1, 0.9]), Haiku 5.5 with same-module padding matched to A1's tokens had lower pass rates: Wpad$-$W $-0.138$ [$-0.281$, $-0.018$] and Wpad$-$A1 $-0.178$ [$-0.373$, $-0.024$].
  - Wpad is W plus padding, not A1 plus padding, and was matched on tokens only up to the pool limit.
- Proposed amendment: "The pilot's flat curve was measured mostly on ceiling and floor instances. A later exploratory phase (Phase 3, 11 headroom instances) found lower Haiku 5.5 pass rates under inert-by-construction same-module padding (Wpad$-$W $-0.138$ [$-0.281$, $-0.018$]; instance-level interval, exploratory, with token matching failing on two instances). The pilot's flat curve should therefore not be read as evidence that padding is harmless on instances with headroom."

**P8. Pilot set reuse (Availability).**
- Quote: "The pilot set is disjoint from any future confirmatory set and will not be reused."
- Problem: Phase 1 used 23 pilot instances, and 8 of the 11 Phase 3 instances are pilot cli/cli instances.
- Proposed amendment: "The pilot set is disjoint from the confirmatory set. It was reused for the exploratory Phase 1 and Phase 3 ablations (Phase 3: 8 of 11 instances); see preregistration §8, entry of 2026-10-18."

**P9. Released verdicts (Abstract and Availability).**
- Quote: "all 2,360 verdicts are released".
- Proposed amendment: "The release includes the 24 verdict records of the invalid instance, which must be excluded in analysis."

## Stage 1 protocol (preregistration, v1.0)

**S1. Pilot instance count and findings that bind the design.**
- Quotes:
  - "A 24-instance pilot on one repository (2,360 verified samples, three models, about \$61, published with all data)" and "after the mid-tier model solved 14 of 24 instances"
  - "(i) … $+0.042$ [$+0.012$, $+0.075$]"
  - "(ii) … $-0.03$ [$-0.15$, $+0.09$] on Haiku"
  - "(iii) Sonnet 5.5 solved 14 of 24 instances"
  - "the sample standard deviation of A1$-$A1b over 24 instances is 0.083"
  - "screen loss (14 of 24 on the mid-tier model)" and "a 58\% task-only screen loss"
- Proposed amendment: apply the pilot erratum values: 23 valid instances; A1$-$A1b $+0.043$ [$+0.013$, $+0.078$]; P200$-$A1 $-0.029$ [$-0.129$, $+0.081$]; Sonnet solved 14/23 (61% screen loss, not 58%); recompute the standard deviations (0.083, 0.26, 0.42) on 23 instances. "Conclusions unchanged" holds for the margins only after that recomputation.

**S2. Pilot cost and its derived budget.**
- Quotes:
  - "which is what made the pilot's 2,360 samples cost \$61"
  - "(\$0.20 per instance for nine arms at ten samples on the dense model; …)"
  - "dense model, all arms within its window, 200 instances, about \$150"
  - "with an upper bound of \$2,200 if input above 200k tokens is billed at a higher tier"
  - "Padding above 200k may be priced at a higher tier; the budget below carries that as its upper bound."
- Problem: the pilot cost about $73. The dense-model arm cost $16.44, about $0.71 per instance (23 instances), not $0.20. The higher Haiku tier already applies above 100k tokens. A1b (120k median), A2, and the padded arms (P200 and above) sit largely in that tier.
- Proposed amendment: "Pilot cost was about \$73 (Haiku \$16.44), not \$61. The dense-model unit cost is about \$0.71 per instance for the pilot's nine arms, because Haiku 5.5 bills a higher rate above 100k prompt tokens. The dense-model budget (\$150) and the total (\$1,600; upper bound \$2,200) are to be re-derived with this rate; the higher tier is a known cost, not an upper-bound contingency."

**S3. Interfaces versus the write-set alone (finding (i)).**
- Quote: "$+0.067$ [$+0.021$, $+0.133$]" (A1 over W).
- Proposed note: add the Phase 1 re-estimate, as in P6, to "Findings that bind this design". As a record of the pilot the sentence is accurate, but it should not be read as a replicated effect.

**S4. Reuse of pilot data.**
- Quote: "Pilot data are exploratory and are not reused."
- Problem: Phase 1 and Phase 3 reused pilot instances.
- Proposed amendment: "Pilot instances were reused in exploratory Phases 1–3 (preregistration §8); they remain excluded from the confirmatory set."

## Definitions note (v1.1)

No sentence is contradicted or materially qualified. The note reports no language-model experiments and makes no empirical claim about editors.

The new evidence is consistent with its stated hypotheses: Hypothesis 1 (portability of $g_A$) is explicitly a hypothesis, and non-closure under superset is a theorem of the stylised model. No erratum is needed.

## Preregistration (preregistration.md)

### Body text inconsistent with the erratum

- **§4 Screening:** "In the pilot this removed 14 of 24 instances for Sonnet 5.5." Proposed: "14 of 23 (see 2026-10-12 erratum)".
- **§4 Sample size:** "the 24-instance pilot … is disjoint and not reused" and "σ=0.083". Add a cross-reference to the erratum and to §8 (reuse in the exploratory phases; σ to be recomputed on 23 instances).
- **§2 H5:** "confirmatory on the Phase 3 instances". The draft states that none of the results is confirmatory. The Phase 3 instances were chosen by screens on the evaluated models and reuse pilot instances, and H5a (A1g) was not run in Phase 3. Proposed deviation text is D6 below.

### Missing from, or inconsistent in, the Deviations section

**D1. Phase 3 disk and build-cache incident is not recorded.**
- RESULTS events: on 2026-10-14 the shared Go build cache reached about 150 GB (per-patch relinking of test binaries); lanes were restarted with per-lane caches; 17 records written while the disk was full were purged with their cached-verdict dependants and re-sampled; originals are retained by the author. RESULTS claims "all recorded in preregistration.md §8"; this is not so.
- Proposed entry: "2026-10-14 (Phase 3 harness/disk incident): the shared Go build cache reached about 150 GB. Lanes were restarted with per-lane caches. 17 records written while the disk was full were purged together with the cached verdicts that depended on them and re-sampled; the originals are retained by the author. No model output was altered."

**D2. Hugo drop reason is inconsistent.**
- Quote, entry 2026-10-18 (vii): "hugo c9f6e4d4abc3 was selected by the Phase 3 screen and dropped for cost, with partial data labelled as such".
- RESULTS says the instance was dropped as unrunnable because it produced a 182 GB build cache. It also lists 12 selected, 11 run, and mentions no partial data. The RESULTS file itself gives both 182 GB (the instance) and about 150 GB (the shared cache); the author should reconcile these.
- Proposed text: "…dropped on 2026-10-14 because its single instance produced a 182 GB build cache (unrunnable); no partial data enter the reported results [or: state which partial data exist and where they are labelled]."

**D3. Phase 2 disk-full contamination is only partly recorded.**
- Entry 2026-10-13 mentions only the absent instance bd81afda9ab6 and docker/cli. RESULTS adds that the disk-full interruption contaminated the hugo baseline and 17 mining rejections (purged and re-examined).
- Proposed addition: "The same interruption contaminated the hugo baseline and 17 mining rejections; these were purged and re-examined."

**D4. Phase 1 sample counts do not add up.**
- Quote: "4,456 applied samples … 4,409 samples were re-verified this way … The 44 samples … were discarded and re-sampled".
- Problem: 4,409 + 44 = 4,453, three short of 4,456. The RESULTS file repeats the same figures.
- Proposed text: "…the remaining 3 samples: [state their disposition]" or correct the totals.

**D5. "Under 7%" is not accurate.**
- Quote, entry 2026-10-13: "7 of 10 selected instances pass under 7% in every arm on Haiku 5.5".
- RESULTS: caddy 7910dd94eea2 has A1 = 0.07, and the stated criterion is best arm below 0.1. Proposed: "at most 7% (best arm below 0.1)".

**D6. H5 status and scope.**
- Phase 3 ran A1t but not A1g, so H5a was not tested there. H5b was computable on only 8 instances for Haiku (6 for Sonnet).
- Proposed entry: "H5 is exploratory throughout: the Phase 3 instances were selected by screens on the evaluated models and reuse pilot instances. H5a (A1g$-$A1) was not run on Phase 3; H5b (A1t$-$A1) was computed on 8 instances (Haiku, one-sided lower bound $-0.156$, not non-inferior). Neither is confirmatory."

**D7. Phase 2 design was not recorded before the run.**
- Phase 2 used four models (including claude-haiku-4-5-20251001, in none of the planned model sets), with k=100/20/10/5 and arms A0/W/A1t for Opus. The 2026-10-13 entry was written "after stages 2–5", and the 2026-10-12 amendment covers only the screen and k≥100 per-cell estimation.
- Proposed entry: "Phase 2 model set, per-model k and arm lists were fixed in the harness before the run but not recorded here beforehand: haiku-5-5 k=100, haiku-4-5-20251001 k=20, sonnet-5-5 k=10, opus-5-5 k=5 (A0, W, A1t). Haiku 4.5 is not in the Stage 1 model plan."

**D8. Caddy was used in Phases 2–3.**
- Caddy is not in the §4/Stage 1 ranked list, and Stage 1 says it was dropped from the pilot because its tests install a root certificate. 14 caddy instances were mined (159 first-parent commits), 4 were run in Phase 2 and 3 in Phase 3.
- Proposed entry: "caddyserver/caddy, outside the §4 list, was used for exploratory Phases 2–3; state how the baseline problem was handled."

**D9. Relaxed mining was not completed as amended.**
- The 2026-10-13 amendment says "previously examined commits rejected only by the old limits are re-examined". RESULTS: relaxed mining of caddy, hugo and cli was stopped by the disk incident and not rerun; restic and golangci-lint relaxed mining (2026-10-14) produced nothing.
- Proposed entry: "Relaxed-limit re-examination was completed only for restic and golangci-lint (no new instance); caddy, hugo and cli were not re-examined."

**D10. Entry 2026-10-13 attributes a mechanism the data do not establish.**
- Quote: "the effects are attributed to reader behaviour (load, framing, semantic reminders), not missing information".
- RESULTS records the diagnostic as a harness-session observation, not a script output, covering three cells. The draft calls the attribution an untested mechanism.
- Proposed rewording: "In three cells where context changed the outcome, a manual harness-session check (not scripted, output not saved) found no code identifiers in passing patches supplied only by dependency documentation. The attribution to reader behaviour is an untested hypothesis."

**D11. Entry 2026-10-12 (H5 exploratory reading) overstates the finding.**
- Quote: "so on 22 of 23 instances dependency interfaces add nothing measurable once the write-set bodies are present".
- Phase 1 data: the "without most influential" W−A1 is +0.000 [−0.025, +0.023], but 13 of 23 instances are at ceiling or floor and 10 have W inexpressible. Phase 2 at k=100 then showed cli 2bcdfbb1ac02 (among the 22) at W 0/100 against A1 27/100.
- Proposed rewording: "Without that instance, W is non-inferior to A1 on the remaining 22 (+0.000 [−0.025, +0.023]). With 13 of 23 instances at ceiling or floor, this does not show that interfaces add nothing; a later k=100 cell (cli 2bcdfbb1ac02: W 0.00, A1 0.27) shows a large difference."

## Minor note on the draft

Pilot and Stage 1 state "Contexts are serialised deterministically with $W$ last, immediately before the task". The draft says the serialisation order of A1 "was not checked for this report". The draft could cite the pilot's stated design, while noting it is a design statement rather than a check in these phases.