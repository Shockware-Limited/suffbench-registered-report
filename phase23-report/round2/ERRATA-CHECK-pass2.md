# Contradiction check: Phases 1–3 evidence vs. prior publications and preregistration

Quotations are from the supplied sources. Where the erratum figures already in the preregistration (§8) settle a number, I use them. Where a number is affected but no corrected value has been recorded, I say "recompute" rather than invent one.

---

## Pilot paper (DOI 10.5281/zenodo.23307204, v1.0)

**P1. Instance count (invalid instance cli__cli-0c2eea6338a2).**
- Quotes:
  - Title: "A 24-Instance Pilot Measurement…"
  - Abstract: "24 fail-to-pass instances were obtained" and "exploratory paired estimates on 24 instances"
  - §2: "Twenty-four instances remain: 13 from August--October and 11 from June--July 2026, in 18 distinct packages."
- Problem: one of the 24 had an empty task text and scored 0 on every arm and model, so it is invalid.
- Proposed erratum: "Erratum (2026-10-12). Instance cli__cli-0c2eea6338a2 was run with an empty task text and is invalid. All analyses should be read on the 23 remaining instances. The per-window counts (13 / 11) and the package count (18) are to be recomputed on 23 instances. The released records for this instance are flagged invalid."

**P2. Haiku base-arm estimates (Results, "Interfaces versus bodies"; Table 1).**
- Quotes:
  - "$+0.042$ [$+0.012$, $+0.075$] over the same packages with bodies (A1b)"
  - Table 1: A1 "0.646 [0.467, 0.817]"
  - "$+0.067$ [$+0.021$, $+0.133$] over the write-set alone"
  - "$+0.046$ [$+0.012$, $+0.083$] over A1F"
  - "The difference comes from six instances"
- Problem: the preregistration erratum gives corrected values for A1 and A1−A1b only. The other rows and contrasts have not been recomputed.
- Proposed text: "On 23 valid instances, A1 has Δ-pass 0.674 [0.491, 0.843]; A1−A1b is +0.043 [+0.013, +0.078]. The A1−W contrast (+0.067), the A1F contrast, the A∅/W/A1b/A1F rows of Table 1 and the 'six instances' count are to be recomputed on 23 instances."
- The abstract's rounded "+0.04 [+0.01, +0.08]" still holds at two decimals.

**P3. Padding on Haiku (abstract and Table 2).**
- Quote (abstract): "Padding A1 to 200k tokens changed the pass rate by $-0.03$ [$-0.15$, $+0.09$] on Haiku"
- Quote (Table 2): P200 "$-0.033$ [$-0.150$, $+0.094$]"
- Problem: the erratum recomputes this as −0.029 [−0.129, +0.081] on 23 instances.
- Proposed text: "…by −0.03 [−0.13, +0.08] on Haiku (23 instances; erratum 2026-10-12)." Table 2 rows and the "−0.03 and +0.01 at every level" sentence need recomputation. The Sonnet and Opus padding figures are likewise not yet recomputed.

**P4. Task-only counts.**
- Quotes: "Sonnet solved 14 of 24 instances at least once from the task text alone, Haiku 4 of 24"; "Sonnet solved 14 of 24 (0.44, $k=3$)"; "Haiku solved 4 of 24 … (pooled pass 0.10…)".
- Problem: the erratum gives Sonnet 14/23. Haiku's 4 solved instances are unaffected, so 4/23. The pooled rates change denominators.
- Proposed text: "Sonnet solved 14 of 23 valid instances, Haiku 4 of 23. Pooled rates are recomputed on 23."
- The same denominator change applies to "5 of 11 from June--July, 9 of 13 from August--October" (the invalid instance's window needs to be stated) and to the abstract's "which makes a task-only control essential".

**P5. Opus/Sonnet subset size.**
- Quotes: "on the 10 instances Sonnet had not solved from task text alone" (abstract); "the 10 instances that Sonnet did not solve" (§3).
- Problem: the invalid instance cannot have been solved from task text, so it sits inside that 10. The valid subset is 9.
- Proposed text: "…the 9 valid instances Sonnet had not solved (a tenth, invalid, instance was also run and is excluded)."

**P6. Cost.**
- Quotes: "The whole measurement cost about \$61 in API calls at list prices." And "the Haiku arm consumed … about \$4.71".
- Problem: Haiku 5.5 is billed higher above 100k prompt tokens, and 697 of 2,256 Haiku calls were above it. The corrected figures are Haiku $16.44 and a total of about $73 (16.44 + 29.16 + 27.00).
- Proposed text: "…about \$73 (Haiku \$16.44, Sonnet \$29.16, Opus \$27.00)."
- The list-price sentence "(Haiku 5.5: \$0.10 / \$0.50 per million input / output tokens, cache reads \$0.01 …)" is incomplete. It should add: "…and a higher rate for prompts above 100k tokens."

**P7. Task-text authorship counts.**
- Quotes: "For 11 without a usable issue, a behaviour-only specification was written by Claude Haiku 5.5…"; "Eleven task texts were written by Haiku 5.5"; "Claude Haiku 5.5 wrote the eleven rewritten task specifications".
- Problem: one of the eleven (the invalid instance) produced no text.
- Proposed text: "Ten task specifications were written by Haiku 5.5; for one instance the rewriting step produced no text and the instance is invalid."

**P8. Flat degradation curve (qualified, not refuted).**
- Quotes:
  - "so the degradation curve is flat within the resolution of this pilot"
  - "Within this pilot's resolution the average degradation curve $g$ is flat from 40k to 200k tokens"
  - §5: "H1 (degradation with load) found no consistent effect up to 200k on this task class"
- Evidence: Phase 1 shows 13 of 23 pilot instances had no room to move (W and A1 both at ceiling on 8, both at floor on 5). On headroom instances, Phase 3 Haiku 5.5 gives Wpad−W −0.138 [−0.281, −0.018] at about 2.35× W's tokens, with the interval excluding zero in both sample sets. The designs differ: Wpad pads W to A1's size, and the pilot pads A1 up to 200k.
- Proposed note: "Subsequent exploratory work (Phases 1–3, DOI pending) found that 13 of the 23 valid pilot instances were at ceiling or floor for both W and A1 and so could not show degradation. On instances with headroom, padding W with inert same-module code to A1's size lowered Haiku 5.5 pass rates (−0.138 [−0.281, −0.018], n=11). The flat pilot curve should be read as a statement about mostly uninformative instances, not as evidence that load does not matter."

**P9. Size of the interface advantage over the write-set alone (qualified).**
- Quote: "$+0.067$ [$+0.021$, $+0.133$] over the write-set alone".
- Evidence:
  - Phase 1 (same 23 instances, Haiku 5.5, k=20): W−A1 = −0.028 [−0.096, +0.017], not non-inferior.
  - A1 itself moved by −0.041 [−0.074, −0.013] relative to the pilot. This confounds k and date.
  - Phase 3 A1−W is +0.039/+0.049, unresolved. Phase 2 W−A1 is +0.000.
- Proposed note: "The pilot's +0.067 was an after-the-fact estimate. A k=20 re-run on the same instances gave A1−W of +0.028 with an interval including zero, and A1 itself came out 0.041 lower than in the pilot. The pilot figure should not be taken as a replicated effect size."

**P10. Reuse of the pilot set.**
- Quote (§7 Availability): "The pilot set is disjoint from any future confirmatory set and will not be reused."
- Problem: the 23 pilot instances were reused for the Phase 1 ablation, and several of them (e.g. cli 2bcdfbb1ac02, cba9646b8c25, babd691446b9) appear in Phases 2–3.
- Proposed text: "The pilot set is disjoint from the confirmatory set. It was reused after publication for exploratory ablations (see DOI pending), which are not confirmatory."

**P11. Run-to-run percentages.**
- Quote: "25\% of Haiku cells (48 of 194 …), 11\% of Sonnet cells (12 of 111) and 7\% of Opus cells (2 of 29)".
- Problem: the invalid instance contributed unanimous cells, so denominators change.
- Proposed text: "Recompute on 23 instances (erratum 2026-10-12)."

**P12. Released data.**
- Quote: "all 2,360 verdict records".
- Proposed text: "The released records include those for the invalid instance, flagged `invalid`. The tag v0.1.1-pilot is superseded by an errata tag."

---

## Stage 1 protocol (v1.0, 2026-10-11)

**S1. Cost and instance count in the abstract.**
- Quote: "A 24-instance pilot on one repository (2,360 verified samples, three models, about \$61, published with all data)… after the mid-tier model solved 14 of 24 instances with no repository context".
- Proposed text: "A pilot on 23 valid instances of one repository (2,360 verified samples including one invalid instance, three models, about \$73; erratum 2026-10-12)… after the mid-tier model solved 14 of 23 instances…".
- The "24-instance pilot" wording in the Introduction, in §Analysis "Pilot" ("Twenty-four instances mined…") and in the Table 1 caption ("24 cli/cli instances") needs the same fix.

**S2. Task-text composition.**
- Quote: "(11 of those 24 task texts were model-rewritten specifications, 13 were issue bodies)".
- Proposed text: "(10 of those 23 valid task texts were model-rewritten specifications, 13 were issue bodies; one rewritten text was empty and the instance is invalid)".

**S3. Pilot findings that bind the design (§Analysis, "Pilot").**
- Quotes: "$+0.042$ [$+0.012$, $+0.075$]"; "padding A1 to 200k changed $\Delta$-pass by $-0.03$ [$-0.15$, $+0.09$] on Haiku"; "(iii) Sonnet 5.5 solved 14 of 24 instances from the task text alone"; "the latter two on nine instances selected as those Sonnet had not solved".
- Proposed text:
  - (i) "+0.043 [+0.013, +0.078]".
  - (ii) "−0.029 [−0.129, +0.081]".
  - (iii) "14 of 23".
  - (iv) and (v): recompute on 23.
  - Add: "A k=20 re-run on the same instances gave A1 lower by 0.041 [−0.074, −0.013]; the pilot's point estimates are therefore not stable at the second decimal."

**S4. Margin justification.**
- Quote: "on Haiku the sample standard deviation of A1$-$A1b over 24 instances is 0.083, so… $n \ge 6.18\,\sigma^2/\eps^2 \approx 17$".
- Problem: the instance count changes to 23, so σ and n need recomputation. The preregistration's §4 Margin bullet gives σ ≈ 0.11 and n ≈ 30 for the same quantity, which is inconsistent with this protocol.
- Proposed text: "Recomputed on 23 instances, σ = [value]; n = [value]. The preregistration's σ ≈ 0.11 is reconciled in a dated note."

**S5. Pilot unit costs and budget.**
- Quotes: "(\$0.20 per instance for nine arms at ten samples on the dense model; \$1.22 per instance…)" and "about \$150" for the dense model; "Padding above 200k may be priced at a higher tier"; "which is what made the pilot's 2,360 samples cost \$61".
- Problem: the dense-model unit cost was understated. $16.44/24 ≈ $0.69 per instance, about 3.5 times the stated $0.20. The higher Haiku tier applies above 100k tokens, not only above 200k.
- Proposed text:
  - "Dense-model unit cost from the pilot is about \$0.69 per instance (\$16.44 across 24 instances). The dense-model budget and the \$1,600 / \$2,200 totals are to be recomputed accordingly."
  - "Haiku 5.5 is billed at a higher rate above 100k prompt tokens."
  - "…cost about \$73."

**S6. Screen-loss figure.**
- Quote: "a 58\% task-only screen loss".
- Proposed text: "…(14 of 23, 61%)".

**S7. "Pilot data are exploratory and are not reused."**
- Problem: the pilot instances and data were reused (see P10).
- Proposed text: "…and are not reused in any confirmatory analysis; they were reused after publication for exploratory ablations (Phases 1–3)."

**S8. Mining rule gap.**
- The mining list has no non-empty-task-text check, although the preregistration records "A mining check (non-empty task text) is added".
- Proposed amendment: "Mining: candidates with an empty or whitespace-only task text are rejected and logged."

**S9. Qualification of pilot finding (ii), the padding result behind H1.**
- Quote: "extended the load range after padding to 200k produced no consistent effect".
- Proposed addition: "The pilot padding contrast was run on instances of which 13 of 23 had W and A1 at ceiling or floor. Exploratory Phase 3 found degradation on instances with headroom, so H1 is to be analysed with and without ceiling/floor instances (descriptive)."

**S10. Hypothesis list.**
- The preregistration says it "mirrors the Stage 1 report". The report contains no H5, H6 or H7 and none of the dated revisions. Either state that the report is superseded by the dated preregistration entries, or add H5–H7 as exploratory-phase hypotheses.

---

## Definitions note (v1.1, DOI 10.5281/zenodo.23282196)

No sentence in this document is contradicted by, or materially qualified by, the new evidence. The note reports no language-model experiments. It treats non-increasing $g$ as an assumption and explicitly allows noise to help. Its mutation measurement is unaffected. No erratum is required.

---

## Preregistration §8 (Deviations)

The RESULTS file says all data-integrity events are "recorded in preregistration.md §8". Several are not, and some entries are inconsistent with the RESULTS data.

**D1. Entries that are present but wrong or imprecise**

1. **Build-fault accounting.**
   - Entry: "4,456 applied samples… 4,409 samples were re-verified… The 44 samples… were discarded and re-sampled."
   - Problem: 4,409 + 44 = 4,453, leaving 3 samples unaccounted for.
   - Proposed text: "The remaining 3 of 4,456 were [disposition]."

2. **H5 exploratory reading.**
   - Entry: "so on 22 of 23 instances dependency interfaces add nothing measurable once the write-set bodies are present."
   - Problem: Phase 1 sign counts for W−A1 are 4/4/15, so four instances favoured A1. Phase 2 at k=100 shows cli 2bcdfbb1ac02 with W 0.00 vs A1 0.27, and Phase 3 shows the same (0.00 vs 0.22). The Phase 3 screen shows ad2a33837712 with W 0.35 vs A1 0.65.
   - Proposed replacement: "W−A1 is not non-inferior (one-sided LB −0.083). Without babd691446b9 the difference is +0.000 [−0.025, +0.023], but at least one other instance (cli 2bcdfbb1ac02: W 0.00, A1 0.27 at k=100) shows a clear A1 advantage. The statement that interfaces 'add nothing measurable' on 22 of 23 instances is withdrawn."

3. **Phase 2 attribution.**
   - Entry: "the effects are attributed to reader behaviour (load, framing, semantic reminders), not missing information."
   - Problem: this rests on a harness-session diagnostic that is not a script output, on three cells. Removal of one package took cli 2bcdfbb1ac02 from 0.27 to 0.00, and the mechanism was never tested.
   - Proposed replacement: "…are hypothesised to reflect reader behaviour; this is an untested hypothesis based on an unscripted diagnostic in three cells."

4. **Floor wording.**
   - Entry: "7 of 10 selected instances pass under 7% in every arm on Haiku 5.5".
   - Problem: caddy 7910dd94eea2 has A1 = 0.07, and 0.07 is not under 7%.
   - Proposed text: "…at most 7%".

5. **Instance-set status of H5.**
   - Entry: "confirmatory on the Phase 3 instances".
   - Problem: Phase 3 instances were chosen by a screen on the evaluated model, and 8 of the 11 are pilot/Phase 1 instances. Phase 3 did not run A1g at all, and A1t−A1 is not among the reported contrasts. The draft states that none of the results is confirmatory.
   - Proposed new entry: "2026-10-14: H5a/H5b are not confirmatory on the Phase 3 instances. The set was selected by screens on the evaluated model and overlaps the pilot, A1g was not run, and A1t−A1 was not analysed. H5 remains exploratory."

6. **"All contrasts are same-day paired within instance" (2026-10-13 Phase 3 amendment).**
   - Problem: W and A1 reuse the k=20 screen samples (post-screen n=30 vs all-sample n=50). Seventeen records were re-sampled after the disk fault.
   - Proposed new entry: "The same-day pairing was not met for W and A1 pooled with screen samples, or for the re-sampled records. The pre-specified reading uses all samples (Wd−W one-sided LB −0.051, not meeting the ε=0.05 margin). The post-screen-only analysis (LB −0.043) is a post-hoc sensitivity analysis."

**D2. Events in RESULTS "Data-integrity events" that are missing from §8**

1. **Phase 2 disk-full interruption.**
   - Only instance bd81afda9ab6 is mentioned. Missing: the contaminated hugo baseline, and the 17 mining rejections that were purged and re-examined.
   - Proposed text: "The disk-full interruption contaminated the hugo baseline and 17 mining rejections; the rejections were purged and re-examined."

2. **All 2026-10-14 Phase 3 events:**
   - The shared Go build cache reached about 150 GB (per-patch relinking of test binaries).
   - Lanes were restarted with per-lane caches.
   - hugo c9f6e4d4abc3 was selected by the screen, then dropped as unrunnable.
   - 17 records written while the disk was full were purged with their cached-verdict dependants and re-sampled, with originals retained by the author.
   - The hugo cache size is given as 182 GB in the Phase 3 header and as about 150 GB in the integrity list. Reconcile this. Also confirm that the two uses of "17" (Phase 2 mining rejections, Phase 3 sample records) are distinct sets.
   - Proposed text: one dated entry covering each of these items.

3. **Relaxed mining (M1).** The 2026-10-13 amendment states that previously rejected commits would be re-examined. RESULTS says relaxed mining of caddy, hugo and cli "was stopped by the disk incident and not rerun", and the relaxed restic/golangci-lint mining found no instance. Missing entry: "Relaxed-limit re-examination was incomplete for caddy, hugo and cli."

4. **Repositories outside the §4 list.**
   - The Phase 2 screen includes 10 caddy instances (14 valid caddy instances in the pool), and caddy appears in Phases 2–3. The protocol says Caddy was dropped by the pilot because its tests install a root certificate, and caddy is not on the §4 list.
   - Missing entry: "Caddy (and zap, none valid) was mined and used in the exploratory phases outside the registered list; how the root-certificate baseline issue was handled is [explain]."

5. **Models and k allocations in Phase 2.**
   - Phase 2 used four models (Haiku 5.5, Haiku 4.5 at k=20, Sonnet 5.5 at k=10, Opus 5.5 at k=5 with arms A0/W/A1t). These are not recorded anywhere in §8.
   - The Phase 2 Haiku 4.5 data have unexplained holes: no A1 cell for caddy 6727b2f3a92b, and no cells at all for caddy 7910dd94eea2. This is why the Haiku 4.5 contrasts have n = 8 and 9.
   - Missing entries: the model and k allocation, and the cause of the missing cells (§6 requires missing data to be recorded).

**D3. Other**

- The bootstrap-seed deviation (seed 2 for paired differences) is recorded only for analysis/pilot.py. State that analysis/phase23.py also uses seed 2.
- RESULTS "By model" dollars sum to $136.65, but the phase totals sum to $148.75 (a $12.10 gap). The sample counts agree (17,687). Reconcile before quoting spend.
- Related: preregistration §4's Margin bullet (σ ≈ 0.11, n ≈ 30) disagrees with the Sample-size bullet and the protocol (σ = 0.083, n ≈ 17). Reconcile with a dated note.

---

## Notes on the draft (outside the requested scope)

- The draft's "A1's serialisation order is not recorded in the materials used for this report" is contradicted by the pilot paper and protocol, which state that contexts are "serialised deterministically with $W$ last". The position confound it describes may be resolvable by citing them.
- The "Data" paragraph in the declaration-level slicing section says Wd retains W's pass rate "on the primary set". This conflicts with the abstract's "post-hoc sample-set choice". Under the preregistered all-sample set, Wd−W has one-sided LB −0.051 and fails.