# Review of the submitted draft

## Status

The `=== DRAFT ===` section is empty. No LaTeX, prose, tables or references were supplied. The automated audit confirms this: "0 distinct numbers checked". The audit's "none" means there was nothing to check. It is not a clean result.

Checks (a)–(h) cannot be applied to text that does not exist. I have not invented offending passages.

## REQUIRED edits

1. **Offending text:** (none; the draft body is absent)
   - **Problem:** There is nothing to review, compile or check against RESULTS.md.
   - **Replacement:** Supply the complete LaTeX source, including preamble, all `\input`/`\include` files, the `.bib` file and any table-generating includes. Then re-run the numbers audit so that it reports a non-zero count.

## Pre-submission traps

These are not edits, because there is no text to quote. Each item is grounded in RESULTS.md and the preregistration. The resubmitted draft will be checked against all of them.

### (a) Numbers and sample sets

1. **Phase 3 Wd − W on Haiku has a sample-set-dependent verdict.**
   - Post-screen (n=30): lower bound (LB) −0.043, which is non-inferior at ε=0.05.
   - All samples: LB −0.051, which is not non-inferior.
   - The Phase 3 amendment does not say which sample set is primary. The draft must report both, name one as primary, and state that the choice was not preregistered.
   - The post-screen set is the defensible primary, because the screen samples were used for selection (winner's-curse risk).

2. **Report spend correctly.**
   - Total spend is $148.75.
   - Pilot spend is about $73 (erratum 2026-10-12), not $61.

### (b) Over-claiming

3. **Phase 1 contrasts.**
   - A1g − A1 is +0.017 [−0.002, +0.041] and A1t − A1 is +0.007 [−0.020, +0.030]. These are non-inferiority results, not equivalence or "no difference".
   - These runs are exploratory: the faulty aggregate was seen before the repair.

4. **Phase 1 W − A1 is not non-inferior** (LB −0.083).
   - The §8 sentence "on 22 of 23 instances dependency interfaces add nothing measurable" is a post-hoc single-instance exclusion.
   - Do not restate it as a finding.

5. **Leave-one-out at k=100: every count falls inside its null range.**

   | Instance | Observed | Null reference |
   |---|---|---|
   | caddy 6727b2f3a92b | 9/13 | 5.5 [1, 12] |
   | caddy c8591a1e46e4 | 2/5 | 2.3 [0, 5] |
   | cli 2bcdfbb1ac02 | 2/4 | 1.5 [0, 4] |

   - No necessity claim is supported at the count level.
   - The single cell "queries removal 0.27→0.00" may be reported descriptively.

6. **The diagnostic of 2026-10-13 is not a script output.**
   - RESULTS labels it "harness session, not a script output".
   - The attribution "reader behaviour (load, framing, semantic reminders)" is an untested mechanism.
   - Label both as unverified interpretation. Do not use "shows" or "proves".

7. **Phase 1 necessity fraction.**
   - "Necessary 0.244 [0.178, 0.319]" ignores instance clustering.
   - The count of 33 matches the null reference of 30.8 [13, 49].
   - Precision and recall are declared uninterpretable in §8. Do not report them as predictor quality.

### (c) Floor and ceiling

8. **Phase 2 relative contrasts are near-vacuous.**
   - Degenerate instances: 7/10 (Haiku 5.5), 9/10 (Haiku 4.5), 5/10 (Sonnet), 5/10 (Opus).
   - Opus A1t − W of +0.000 [+0.000, +0.000] with signs 0/0/9 is a degenerate interval, not evidence of sufficiency.
   - Haiku 5.5 A1t − A1 has LB −0.038, but rests on 3 informative instances. Report absolute rates and the non-degeneracy condition alongside it.

9. **Phase 3 Sonnet is at ceiling on 6/11 instances** (W = A1 = 1.00).
   - State this next to every Sonnet contrast.

### (d) Decision bound

10. **Use the one-sided 95% LB, not the lower end of the two-sided interval.**
    - The two-sided lower end corresponds to a one-sided 2.5% test (amendment 2026-10-12).
    - Correct readings:
      - Sonnet Wd − W: LB −0.082, so not non-inferior. Its two-sided interval [−0.082, −0.009] also excludes zero (Wd worse than W).
      - Sonnet A1r − W: [−0.200, −0.045], which also excludes zero.

11. **Wpad results on Haiku.**
    - Wpad − W is −0.138 [−0.281, −0.018], and Wpad − A1 is −0.178 [−0.373, −0.024]. These intervals exclude zero.
    - On Sonnet, Wpad − W is −0.045 [−0.118, +0.009]. Do not call it a padding effect.

### (e) Preregistration, amendments and deviations

12. **H5 was preregistered as "confirmatory on the Phase 3 instances".**
    - Phase 3 ran no A1g arm.
    - RESULTS reports no Phase 3 A1t − A1 contrast.
    - The draft must state that H5a/H5b were not tested confirmatorily, and why. Otherwise this is an undisclosed deviation.

13. **RESULTS says all integrity events are "recorded in preregistration.md §8". The supplied §8 does not contain:**
    - the 2026-10-14 Phase 3 build-cache incident (about 150 GB), the hugo drop, or the purge and re-sampling of 17 records;
    - the 2026-10-12/13 contamination of the hugo baseline and 17 mining rejections;
    - the M1-relaxation re-examination of caddy, hugo and cli that the 2026-10-13 amendment required. It was stopped and not rerun.

    Either cite the correct §8 version or add dated deviation entries.

14. **Bootstrap seeds.**
    - The paired bootstrap uses seed 2 versus seed 1 in §6.
    - Cite the 2026-10-12 analysis amendment.

### (f) Invented content

15. **Cite only what exists.**
    - The only citable DOIs are 10.5281/zenodo.23282196 and 10.5281/zenodo.23307204.
    - Any other reference, model version or mechanism needs a source.

### (g) Internal consistency

16. **Haiku 4.5 sample sizes differ by contrast.**
    - n=8 for most contrasts, but A1t − W has n=9 (caddy 7910dd94eea2 has no W/A1 cells).
    - Prose must not claim "10 instances" for this model.

17. **Phase 3 A1t was not run as a separate arm on some instances.**
    - On babd691446b9, 2bcdfbb1ac02 and cba9646b8c25 it is marked "–=" (identical arm).
    - Tables must mark these entries and must not invent rates.

### (h) LaTeX

18. **Escape special characters outside math:**
    - `%` (as in "7%", "80%");
    - `_` and `__` in instance IDs, e.g. `caddyserver\_\_caddy-...` or `\texttt{}` with escapes;
    - `&` in any prose;
    - `$` in USD amounts.

    Also:
    - Use `\textminus` or math mode for "−" (U+2212) and for "ε", "≥" and "→" unless `inputenc`/`unicode-math` handles them.
    - Wide tables (Phase 3 has 23 columns) need `\resizebox`, `landscape` or a split.

## OPTIONAL improvements

1. Report the Phase 1 "without most influential instance" estimates alongside each contrast.
2. Add a per-instance figure of absolute rates for Phase 3, with Haiku and Sonnet side by side.
3. Report token ratios next to every non-inferiority claim (e.g. Wd/W median 0.47).
4. Present Wpad − A1 at matched tokens (ratio 1.00) as the cleanest load-versus-content contrast, with its exploratory status explicit.

## Verdict

**NOT YET:** no draft was supplied.