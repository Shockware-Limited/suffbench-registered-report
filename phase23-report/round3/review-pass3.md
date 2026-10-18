# Adversarial review: exploratory ablation report (Phases 1–3)

## REQUIRED edits (most severe first)

**1. LaTeX will not compile (unescaped `$` in the by-model spend list).**
- Quoted: `\texttt{claude-haiku-5-5}: 16202 samples, $101.81;` … `520 samples, $7.32;` … `860 samples, $31.28;` … `105 samples, $8.34.`
- Problem: the four bare `$` open and close math mode across `\item` and `\texttt`, so LaTeX fails.
- Replacement:
  - `16202 samples, USD 101.81;`
  - `520 samples, USD 7.32;`
  - `860 samples, USD 31.28;`
  - `105 samples, USD 8.34.`

**2. Invented discrepancy in spend.**
- Quoted: "The by-model costs, however, sum to less than the total of USD 148.75 obtained from the phase costs. This difference is unexplained in the results file and remains to be reconciled in \texttt{analysis/phase23.py}."
- Problem: 101.81 + 7.32 + 31.28 + 8.34 = 148.75 exactly. The claim is false.
- Replacement: "The by-model sample counts and costs both sum to the per-phase totals (17687 samples, USD 148.75)."

**3. Wpad is not token-matched on the two largest caddy instances, yet the text says it is.**
- Quoted: "ratio 1.00 (matched tokens)" and "padding matched to A1's size".
- Problem: Table `tab:p3inst` gives:
  - 30d3bd2a8959: Wpad 183,345 against A1 237,893.
  - 6727b2f3a92b: Wpad 229,911 against A1 277,505.
  - These are 48–55k tokens short, about 17–23%.
  - The median ratio of 1.00 hides this.
  - 6727b2f3a92b is one of the instances carrying the padding harm.
  - Both are caddy instances, whose padding source is already unrecorded.
  - The H7 amendment (2026-10-13) requires matching, so this is an unrecorded deviation.
- Replacements:
  - Replace "ratio 1.00 (matched tokens)" with "median ratio 1.00; matching failed on caddy 30d3bd2a8959 (0.77) and 6727b2f3a92b (0.83)".
  - Add to the deviations list: "Wpad was not token-matched to A1 on two caddy instances, contrary to the 2026-10-13 amendment; cause not recorded."
  - Compute and report Wpad−W and Wpad−A1 on the 8 cli instances (both sample sets) before making any padding claim. The body already says this was not done.

**4. Downgrade the padding claim from "Supported", and qualify it in the abstract.**
- Quoted: "\paragraph{Supported, within the exploratory scope.} … padding … lowered mean pass rates relative to W ($-0.138$, signs 3/7/1) and A1 ($-0.178$, signs 5/6/0)."
- Problem: the claim rests on several weak points:
  - The padding source is unknown for 3/11 instances, and matching failed on 2 of them (item 3).
  - Wpad−A1 signs are 5/6/0, an almost even split.
  - The upper interval ends are −0.018 and −0.024.
  - A percentile bootstrap at n=11 is known to under-cover.
  - The interval omits within-cell variance; the same caveat you apply to Sonnet applies here.
  - These are 2 of 8 unadjusted contrasts.
- Replacement: move the item under "Fragile". Rewrite it as: "On Haiku 5.5 in Phase 3, Wpad had lower mean pass rates than W ($-0.138$ $[-0.281,-0.018]$, signs 3/7/1) and A1 ($-0.178$ $[-0.373,-0.024]$, signs 5/6/0), driven by large drops on 2–4 instances; the padding source and token matching are unverified on the caddy instances, the intervals ignore within-cell variance and are not adjusted for the eight contrasts, and the percentile bootstrap at $n=11$ may under-cover."
- In the abstract, after "(Wpad$-$W $-0.138$ $[-0.281, -0.018]$)", add: "; token matching failed on two of the three caddy instances and the padding source there is unrecorded."

**5. Placeholders for facts the author controls must be resolved, not left as open statements.**
- Quoted:
  - "Its contents are not defined in the materials used to prepare this report… it is not established that A0 is that arm."
  - "The actual padding source for the caddy instances is not recorded…"
  - "A1's serialisation order is not recorded in the materials used for this report."
  - "Which reading holds is to be stated by the author…"
  - "Before release, these items are to be added to Section 8… and the header of the results file regenerated."
- Problem: the author built the harness. A published report cannot say it does not know what its own arm contains. These sentences read as drafting notes.
- Action:
  - Define A0 from `contexts.json`, or delete all A0 results. This includes the cross-model bullets on 20147bf81fed and 7910dd94eea2, Table `tab:p2con` row A0−W, and the Opus A0 cells.
  - State the caddy padding source.
  - State where W sits in A1.
  - State which reading of "the Phase 3 instances" holds.
  - Add the deviations to §8 and replace "are to be added" with "are recorded in Section 8 on [date]".

**6. Undisclosed reuse of pilot instances in Phase 3, and its implications.**
- Problem: all 8 cli instances in Phase 3 appear in the Phase 1 per-instance or influence lists: 2bcdfbb1ac02, 326faaac8b5c, 3f6a16a9f8c7, 8f7afbdbdbd6, ad2a33837712, b87e58a1d390, babd691446b9, cba9646b8c25. They are therefore pilot instances already run on Haiku 5.5 in the pilot and in Phase 1.
- Consequences:
  - (a) The selection effect is larger than stated.
  - (b) The preregistration makes H5 *exploratory* on the pilot instances. "Confirmatory on the Phase 3 instances" therefore cannot coherently mean this Phase 3, which supports the reading that it means the confirmatory study.
  - (c) The report must state whether the Phase 2/3 non-pilot instances (caddy and new cli) are excluded from the confirmatory set. They have now been screened and run on the evaluated models.
- Additions:
  - In §2.1 Phase 3: "All 8 cli instances are pilot instances also used in Phase 1."
  - In the H5 deviation paragraph: "Because 8 of the 11 Phase 3 instances are pilot instances, on which H5 is exploratory by the preregistration, the phrase can only coherently refer to the confirmatory study."
  - In Consequences: a sentence stating whether instances used here enter the confirmatory set.

**7. A preregistered contrast was computable but not computed (H5b on Phase 3).**
- Quoted: "H5a and H5b were not tested (no A1g arm; no A1t$-$A1 contrast)".
- Problem: Haiku 5.5 ran A1t on all 11 Phase 3 instances, so A1t−A1 is computable. Omitting a contrast named by the preregistration while the data exist looks like selective reporting.
- Action:
  - Compute and report A1t−A1 and A1t−W for Phase 3 Haiku in both sample sets.
  - Fill the three A1t cells shown as `--=` in Table `tab:p3inst` with the rate and the arm duplicated.
  - Replace "(no A1g arm; no A1t$-$A1 contrast)" with "(no A1g arm; A1t$-$A1 is reported in Table~\ref{tab:p3con} as exploratory)".
  - Delete "these cells are effectively unreported", since the table must be fixed rather than apologised for.

**8. The one-sided bound amendment is described incompletely.**
- Quoted: "It adopted the one-sided 95\% lower bound as the decision bound, which is the more lenient of the two readings of Section 6".
- Problem: the amendment was made after the exploratory H5 run, after the faulty aggregate had been seen. It also describes itself as "no change to the decision rule", although §6 H2 explicitly names the 95% two-sided interval's lower bound. The only verdict it changes is the report's headline Phase 3 result (Wd−W, −0.043 vs −0.053).
- Replacement: "It adopted the one-sided 95\% lower bound, the more lenient of the two readings of Section 6, after the exploratory Phase 1 run and after the faulty Phase 1 aggregate had been seen; the amendment describes this as no change to the decision rule, which is contestable because Section 6's H2 text names the two-sided interval. The only verdict in this report that depends on the choice is Haiku 5.5 Wd$-$W on the post-screen set."

**9. The 6727b2f3a92b W>A1 cell did not replicate, so "both directions" and "better choice" are overstated.**
- Quoted: "Individual task--model cells showed large effects of context in both directions" and "both predictors kept nothing. This was the better choice for Haiku 5.5 (W 0.44 against A1 0.22)."
- Problem:
  - In Phase 3 post-screen on 6727b2f3a92b, W = 0.27 and A1 = 0.27 (pooled 0.34 vs 0.26).
  - The Sonnet c8591a1e46e4 cell (6/10 vs 2/10) is unresolved.
  - Only the 2bcdfbb1ac02 cell replicated across phases.
- Replacements:
  - For the first sentence: "Individual Haiku 5.5 cells at $k=100$ showed large differences in both directions (cli 2bcdfbb1ac02: W 0/100, A1 27/100; caddy 6727b2f3a92b: W 44/100, A1 22/100); the second did not replicate in Phase 3 post-screen samples (W 0.27, A1 0.27). The largest was the loss of all passes on cli 2bcdfbb1ac02 when queries was removed from A1."
  - For the second: "This matched the Phase 2 Haiku 5.5 cell (W 0.44 against A1 0.22) but not the Phase 3 post-screen cell (0.27 each)."

**10. The non-additivity gap is itself unresolved.**
- Quoted: "the observed rate of the arm that keeps only queries and iostreams was 0.14."
- Problem: 0.14 vs the expected about 0.23 at n=100 each gives z ≈ 1.6. This is not resolved even before cross-run drift.
- Append: "The gap between 0.14 and about 0.23 is itself not resolved at $k=100$ (two-proportion $z \approx 1.6$)."

**11. A methods claim about absolute rates is false.**
- Quoted: "every relative statement is accompanied by the non-degeneracy condition (best arm $\geq 0.1$) and by absolute rates."
- Problem: no arm-level mean pass rates are given for Phase 1, the Phase 2 aggregates, or the Phase 3 aggregates. Only contrasts and selected cells appear.
- Action: either add per-arm mean pass rates per model and phase, or replace with "every Phase 2 and Phase 3 contrast is accompanied by the non-degeneracy condition, and per-instance absolute rates are given in Tables~\ref{tab:p2inst} and~\ref{tab:p3inst}."

**12. "Same-day paired" is unsupported.**
- Quoted: "Phase 3 contrasts are same-day paired."
- Problem: Phase 3 ran on 2026-10-13/14 and lanes were restarted after the disk incident on 10-14. The all-samples set includes screen samples. Nothing in the results shows same-day pairing.
- Replacement: "Phase 3 was run on 2026-10-13/14, including a restart after the disk incident; whether each pair was sampled on the same day is not recorded."

**13. Availability statement contradicts the body.**
- Quoted: "The script \texttt{analysis/phase23.py} generates every number in this report" and "All data, harness code and analysis scripts are in the repository".
- Problem:
  - Phase 1 numbers come from `analysis/ablation.py` via the frozen ABLATION-REPORT.md.
  - The diagnostic is a harness-session note.
  - The erratum figures come from the preregistration.
  - The invalid originals are not in the repository.
- Replacements:
  - "\texttt{analysis/phase23.py} generates the Phase 2 and Phase 3 numbers; Phase 1 numbers are from \texttt{analysis/ablation.py} via the frozen report; the 2026-10-13 diagnostic is not script output."
  - "All data except the invalid originals, which are retained by the author, …"

**14. The null-reference description is wrong for Phase 1.**
- Quoted: "counts removals exceeding $\eps$ in absolute difference. It uses 2,000 simulations, at $k=20$ in Phase 1 and $k=100$ in Phase 2."
- Problem: Phase 1 counts lowering ("necessary") and raising ("helps") separately.
- Replacement: "In Phase 1 it counts removals lowering and raising the rate by more than $\eps$ separately ($k=20$); in Phase 2 stage 6 it counts removals with $|$difference$| > 0.05$ ($k=100$). Both use 2,000 simulations."

**15. A1g is not governed by the task-text rule.**
- Quoted: "Under the original rule, the predictors kept nothing on many pilot instances (A1g 14/23, A1t 11/23)."
- Replacement: "On the pilot instances the predictors kept nothing on 14/23 (A1g) and, under the original task-text rule, 11/23 (A1t)."

**16. Padding conclusion is overgeneralised.**
- Quoted: "The padding harm appeared only on instances selected for headroom."
- Problem: Wpad was run only on headroom instances, the effect is Haiku-only, and see items 3–4.
- Replacement: "Lower pass rates under padding were observed for Haiku 5.5 on instances selected for headroom; the pilot padding contrast on unselected instances was unresolved."

**17. The citation is used to claim more than n=11 supports, and Du et al. is characterised loosely.**
- Quoted: "but adds the qualification that the kind of added text matters."
- Problem: Du et al. report degradation even with whitespace or masked filler, which is in tension with, rather than qualified by, this finding. One matched length on 11 instances with unverified padding cannot "add a qualification" to it.
- Replacement: "On these instances, at one length, padding was worse than dependency interfaces of similar size; whether this conflicts with reports that length alone hurts even with non-informative filler \cite{du2025} is not tested here."

**18. Amendment (iv) was fixed but is not reported, and it is not listed as a deviation.**
- Quoted: "The set-level comparison of task-text and gold-referenced sets in amendment (iv) is not reported here."
- Action: add to "Deviations not in the version of Section 8": "Amendment (iv) (2026-10-12), set-level precision and recall of the task-text predictor on every mineable instance, was not computed."

**19. Table captions must carry the facts the prose apologises for.**
- Quoted: "The caption of Table~\ref{tab:p3inst} does not state this."
- Action:
  - Add to the `tab:p3inst` caption: "Haiku W and A1 pool the $k=20$ screen and 30 post-screen samples ($n=50$); the primary contrasts in Table~\ref{tab:p3con} use the post-screen 30."
  - Delete the apologetic sentence.
  - Add "-- : not run" to the `tab:p2inst` caption.

**20. Haiku 4.5 sample arithmetic: state the basis.**
- Quoted: "The 520 samples reported for this model are more than the distinct cells shown in Table~\ref{tab:p2inst} account for at $k=20$".
- Problem: the claim holds only if byte-identical arms were not sampled separately. Under that assumption there are 22 distinct cells, giving 440 samples. The surplus of 80 equals exactly 4 cells: the 3 distinct arms of 7910dd94eea2 plus A1 on 6727b2f3a92b. This indicates those cells were sampled and not reported.
- Replacement: "Counting byte-identical arms once, the shown cells account for 22 cells, or 440 samples; the 80 excess samples equal the four missing cells (three distinct arms on 7910dd94eea2 and A1 on 6727b2f3a92b), which indicates these cells were sampled and not reported."
- Report those cells or state why they were excluded.

**21. Build-cache figures are inconsistent.**
- Problem: a single hugo instance is said to have produced a "182 GB build cache", but the shared cache "reached about 150 GB".
- Action: reconcile the two figures, or state that they refer to different caches.

**22. "Valid" instance count includes invalid and template instances.**
- Quoted: "The valid instances on disk number … 30 for \texttt{cli/cli}. The 30 \texttt{cli/cli} instances include the 24 pilot instances, one of them invalid."
- Problem: the results file also says this count includes "earlier template/test instances".
- Replacement: "The instance directories number 14 for caddy and 30 for cli/cli; the latter include the 24 pilot instances (one invalid) and earlier template/test instances, so the count of valid cli instances is lower."

**23. Overstatement about the slice.**
- Quoted: "The slice is a candidate for reducing context without loss for one model on these instances."
- Replacement: "…for reducing context within the 0.05 margin for one model on these instances."

**24. Overgeneralisation about cross-model solving.**
- Quoted: "Instances at floor for Haiku 5.5 were solved by Sonnet 5.5 or Opus 5.5."
- Replacement: "Two instances at floor for Haiku 5.5 were solved by another model (cli ff28e72b59be by Sonnet 5.5 W and Opus 5.5; cli 20147bf81fed by Opus 5.5 W)."

**25. A bound sits exactly at the margin.**
- Quoted: "LB $-0.050$, which does not clear the margin."
- Action: state the unrounded value. With k=10 the mean differences are multiples of 0.01, so this is plausibly exactly −0.05.
- Replacement: "LB $-0.050$ (exactly at the margin; the rule requires LB $> -0.05$)".

**26. Reference list is incomplete.**
- `gloaguen2026` has no full title, arXiv identifier or author initials. Supply all three or delete the citation and the sentence citing it.
- `definitions` lacks its DOI (10.5281/zenodo.23282196, given in the preregistration). Add it.

**27. LaTeX robustness.**
- `\eps` is not standard. Confirm `\newcommand{\eps}{\varepsilon}` in the preamble.
- `\toprule`, `\cmidrule` and `\addlinespace` require booktabs. `\url` requires url or hyperref.
- `tab:p3inst` (23 columns) and `tab:p2inst` (11.5 cm of p-columns plus five more) will overflow badly. Use `sidewaystable`/`table*` or split the tables.
- "see Section~2.2" is hard-coded. Add `\label{sec:arms}` and use `\ref`.

**28. Duplicate "17" counts.**
- Problem: 17 mining rejections (Phase 2) and 17 purged records (Phase 3) are reported as separate events.
- Action: confirm they are distinct, or merge them.

## OPTIONAL improvements

1. Mixed sample sets in the instance-level prose. The "Instances that carry the Haiku contrasts" and slice-loss paragraphs quote pooled W/A1 (n=50) while the primary contrasts use post-screen values. Quote post-screen W/A1, for example 6727b2f3a92b W 0.27 and c8591a1e46e4 W 0.60.
2. Wilson intervals. Report Wilson intervals on per-instance rates, as §6 specifies. Within-cell uncertainty at k=10 is otherwise invisible. Also note that the §6 Tango/Newcombe intervals are not reported.
3. Shared reference cell in leave-one-out. On 6727b2f3a92b, 10/13 removals raise the rate relative to a single A1 cell (0.22) that is lower than Phase 3 A1 (0.26). All differences share this reference, so a low A1 draw shifts every difference upward.
4. Repeated text. The Sonnet caveat ("Each rests on 4--5 instances…") is repeated verbatim. The seed sentence appears twice in Statistics. Deduplicate both.
5. Opus A1t−W. Note that 8 of the 9 zeros are zero by construction (A1t = W).
6. Instance supply. Quantify scarcity against the preregistration: the requirement is ≥200 instances from 5–8 repositories, with pilot instances excluded, against about 23 non-pilot valid instances.
7. Pool overlap. Say which instances overlap between Phases 2 and 3 (2bcdfbb1ac02, 6727b2f3a92b, c8591a1e46e4).
8. Screen coverage. Explain why 22 of the cli and 10 of the 14 caddy instances were screened.
9. Table formatting. In `tab:loo`, replace Python list syntax (`['caddyhttp']`, `[]`) with prose or "none".
10. Title reference. The body refers to "reader effects in the title", but no title is shown. Check that it exists.
11. Acknowledgements. Drop "which the author refers to as Lemma"; it is not informative. Archive the two critiques or omit "Both critiques are reflected in the text".
12. Group cap. State the 16-group cap in the H5 summary.
13. Phase 1 reading. Note that the preregistration's 2026-10-12 Phase 1 reading ("on 22 of 23 instances dependency interfaces add nothing measurable") rests on the post-hoc single-instance exclusion this report rejects.

NOT YET