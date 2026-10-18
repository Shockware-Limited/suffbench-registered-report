# Review of the Phase 1–3 ablation report

## REQUIRED EDITS (most severe first)

**1. Decision bound: §6 is misdescribed, and the headline Phase 3 verdict depends on it.**
- Offending text (Statistics): "the one-sided 95\% lower bound (LB), which is the preregistered decision bound". Repeated in the abstract ("lower bound $-0.043$") and in Supported item 2.
- Problem: §6 of the preregistration specifies the lower bound of the percentile bootstrap "(2,000 resamples, seed 1, 95% two-sided)". It also states "one-sided α = 0.05", so §6 is internally ambiguous.
  - The 2026-10-12 analysis amendment adopted the more lenient reading. It asserts that §6 "specifies" the one-sided 95% bound, which the literal §6 text does not.
  - Under the literal §6 text, the post-screen Haiku 5.5 Wd−W bound is −0.053 < −0.05. Wd is then not non-inferior on either sample set.
  - No other non-inferiority verdict in the report flips under the literal reading (A1g−A1 −0.002; A1t−A1 −0.020; Phase 2 Haiku 5.5 −0.043, −0.042, −0.036).
- Replacement (Statistics, after the decision-rule list): "Section 6 of the preregistration names both a two-sided 95\% bootstrap interval and one-sided $\alpha=0.05$. The analysis amendment of 2026-10-12 adopted the one-sided 95\% lower bound. Under the two-sided interval's lower end, the only verdict that changes is Haiku 5.5 Wd$-$W on the post-screen set ($-0.053$), which would not be non-inferior."
- Add to the abstract after "($-0.051$)": "nor with the lower end of the two-sided interval ($-0.053$)".

**2. Structural zeros inflate the non-inferiority readings.**
- Offending text: "\textbf{Wd$-$W}: $+0.009$ $[-0.053, +0.072]$, LB $-0.043$, signs 4/4/3 … This is non-inferior". Also "The lower bounds of A1t$-$A1, A1g$-$A1 and A1t$-$W clear $-0.05$."
- Problem, Phase 3: Wd is byte-identical to W on 3 of 11 instances (2bcdfbb1ac02, 326faaac8b5c, 8f7afbdbdbd6). The three zero signs are therefore forced by construction. They shrink the mean and the interval toward 0 and favour non-inferiority.
- Problem, Phase 2: A1t kept no dependency on 8 of 10 instances, so A1t = W there. The A1t−W signs 1/1/8 are structural, not a measurement.
- Replacement:
  - Add after the Wd−W bullet: "On 3 of the 11 instances Wd is byte-identical to W, so 3 of the paired differences are zero by construction. The contrast on the 8 instances where Wd differs from W should be reported (not computed here)." Compute and report it if possible.
  - Add to the Phase 2 Haiku 5.5 paragraph: "A1t equals W on 8/10 instances, so A1t$-$W is zero by construction there."

**3. A post-hoc primary set is used as a "Supported" finding.**
- Offending text (Supported item 2): "the reachable-declaration slice Wd was non-inferior to W at $\eps$ on the primary set …"
- Problem: the sample set was designated primary after the data were seen (the report concedes this in §Limitations), and the verdict flips with it. A forking-path result whose verdict depends on an unregistered analytic choice is not "supported".
- Replacement: move the item to a third list headed "Fragile". Reword it as: "Wd met the margin against W only on the post-hoc post-screen set and only under the one-sided bound; it did not with screen samples included, nor under the two-sided bound, nor on Sonnet 5.5."
- In the abstract, replace "a reachable-declaration slice of W was non-inferior to W" with "a reachable-declaration slice of W met the non-inferiority margin against W only under a post-hoc sample-set choice".

**4. Spend does not reconcile.**
- Offending text: the by-model list (\$89.85 + \$7.37 + \$31.07 + \$8.36) next to "total: USD 148.75".
- Problem:
  - The by-model costs sum to \$136.65, not \$148.75; the gap is \$12.10.
  - The sample counts do reconcile: 520 + 16202 + 105 + 860 = 17687.
  - This propagates directly from RESULTS.md, so the automated audit cannot catch it.
- Replacement: reconcile in `analysis/phase23.py` and regenerate. If the gap cannot be explained, state: "The by-model costs sum to \$136.65; the \$12.10 difference from the phase totals is unexplained."

**5. The meaning of "the Phase 3 instances" in H5 contradicts the report's framing.**
- Offending text: "H5 was preregistered as confirmatory on ``the Phase 3 instances''. … H5a and H5b were therefore not tested confirmatorily." Also the Purpose section: "Section~\ref{sec:lim} explains why it was not tested confirmatorily in Phase 3."
- Problem:
  - The abstract and the Purpose section state that all three phases are exploratory and preceded any confirmatory call. A confirmatory test inside exploratory Phase 3 is therefore incoherent.
  - The H5 text was written on 2026-10-12, before this report's Phase 3 was defined (2026-10-13). "Phase 3" there may denote the confirmatory study.
- Replacement: "The H5 paragraph (2026-10-12) calls H5 confirmatory on `the Phase 3 instances'. That phrase predates the Phase 3 defined on 2026-10-13. If it refers to the confirmatory study, H5 remains to be tested there. If it refers to the Phase 3 reported here, H5a and H5b were not tested (no A1g arm; no A1t$-$A1 contrast), which is an undated deviation." The author must state which reading holds, and record it in §8 of the preregistration.

**6. "Worse" claims for Sonnet 5.5 rest on a bootstrap that ignores within-cell sampling noise at k=10.**
- Offending text: Supported item 3, "On Sonnet 5.5, Wd, A1r and Wdr were each worse than W, with intervals excluding zero, despite ceiling on 6/11 instances". Also "Not non-inferior, and the interval excludes zero with Wd worse".
- Problem:
  - Wd−W consists of four differences of −1 or −2 samples out of 10, plus seven zeros.
  - An instance-level percentile bootstrap over values that are all non-positive excludes zero almost automatically: P(all resampled differences are zero) = (7/11)^11 ≈ 0.007.
  - Binomial variance within each cell is ignored.
  - "Despite ceiling" inverts the logic. Ceiling restricts which instances can show a difference; it does not strengthen the claim.
- Replacement: "On Sonnet 5.5 ($k=10$), the point estimates of Wd$-$W, A1r$-$W and Wdr$-$W were negative and their instance-level intervals exclude zero. Each rests on 4–5 instances with differences of 1–4 samples out of 10. The interval does not include within-cell sampling variance, so these are indications, not resolved effects." Move the item from "Supported" to the "Fragile" list.

**7. A1r is mischaracterised.**
- Offending text: "On Sonnet 5.5, every arm that removes bodies or declarations from W is worse than W where the interval is resolved."
- Problem: A1r is "full W plus only the dependency declarations W references". It adds to W; it removes nothing from W.
- Replacement: "On Sonnet 5.5, Wd, Wdr and A1r each had lower point estimates than W (Wd$-$W $-0.045$, Wdr$-$W $-0.109$, A1r$-$W $-0.118$), subject to item 6."

**8. The static-computability conclusion is contradicted by the report's own data.**
- Offending text: "They also show that statically computed dependency selections did not reproduce the pass rate of full A1 where A1 mattered."
- Problem: A1r is a statically computed dependency selection. On cli 2bcdfbb1ac02 it passed 0.60 against 0.22 for A1 on Haiku 5.5.
- Replacement: "The package-level predictors (A1g, A1t) did not reproduce full A1's pass rate on the two Phase 2 instances where A1 differed from W (cli 2bcdfbb1ac02: 0.14 against 0.27; caddy c8591a1e46e4 on Sonnet 5.5: 0.00 against 0.60). The declaration-level A1r exceeded A1 on cli 2bcdfbb1ac02 for Haiku 5.5 but scored 0.00 against 0.30 for W on Sonnet 5.5."

**9. Non-additivity is stated as fact; the comparisons cross phases.**
- Offending text: "The effects of removals are therefore not additive on this instance." Also "Selecting at the level of referenced declarations did better here than selecting whole packages."
- Problem, additivity:
  - An additive prediction for removing cmdutil and client is 0.27 − 0.05 + 0.01 = 0.23. The observed value is 0.14, a gap of about 0.09.
  - Both cells have n=100, so the gap is within roughly two standard errors.
  - On the same instance, A1 fell to 0.17 post-screen in Phase 3, so a drift of this size has been observed.
  - The A1 cell and the stage 6 cells were not run at the same time.
- Problem, A1r versus A1g/A1t: the comparison is 0.60 (Phase 3, n=50) against 0.14 (Phase 2, n=100). It is not same-day paired.
- Replacement:
  - "The data suggest that removal effects may not be additive on this instance (expected about 0.23 under additivity, observed 0.14). The cells come from different runs, and a drift of this size has been observed on this instance, so this is not established."
  - "A1r (Phase 3) passed 0.60, against 0.14 for A1g $=$ A1t in Phase 2. The comparison crosses phases, and A1r is smaller than A1."

**10. The leave-one-out null cannot be exceeded on two of three instances.**
- Offending text: "Each count of removals with absolute difference above 0.05 lies within its simulated null range". Also, in the abstract, "gave counts inside their null ranges".
- Problem: for c8591a1e46e4 the null range is [0, 5] with 5 removals. For 2bcdfbb1ac02 it is [0, 4] with 4 removals. Each range covers the entire support, so the count test has no power there.
- Replacement: add "On caddy c8591a1e46e4 and cli 2bcdfbb1ac02 the null range spans every possible count, so the count test could not have rejected." In the abstract, use "(on two of the three instances the test could not reject by construction)".

**11. Missing cells are unexplained, and one sample count suggests they were sampled and then dropped.**
- Offending text: "This model has no cells on caddy 7910dd94eea2 and no A1 cell on caddy 6727b2f3a92b." Also, for Opus 5.5 on cli 2bcdfbb1ac02, A0 and W only.
- Problem:
  - Counting distinct non-identical Haiku 4.5 cells in Table~\ref{tab:p2inst} gives 22 × k=20 = 440 samples. The results file reports 520.
  - The difference of 80 samples equals exactly four cells: 7910dd94eea2 W, A1 and A1g, plus 6727b2f3a92b A1.
  - Opus A1t on 2bcdfbb1ac02 keeps 2 of 4 dependencies, so it is distinct from W and should exist.
  - §6 requires missing data to be flagged with its cause.
- Replacement: state the cause of each missing cell (API errors, build failure, or exclusion) with its date. If samples were drawn and excluded, say so, and add the event to the deviations.

**12. The Phase 2 screen sample count does not match the design.**
- Offending text: "Phase 2 screen: USD 1.58 for 162 samples". Also "We screened 35 instances … with arm W at $k=5$".
- Problem: 35 × 5 = 175, not 162.
- Replacement: explain the 13 missing screen samples, or correct either the instance count or the k.

**13. A0 is undefined.**
- Offending text: "\textbf{A0}: the arm of that name in the Stage 1 protocol \cite{stage1}".
- Problem:
  - The preregistration lists both A∅ (task only) and A0 but never defines A0.
  - Readers cannot interpret A0−W (−0.140) or the cross-model cases (7910dd94eea2: A0 0.60, W 0.00).
- Replacement: give the definition explicitly, for example "A0: [contents]". If A0 means task-only, write A∅ and say so.

**14. The Wpad padding source is impossible as described for the caddy instances.**
- Offending text: "W preceded by inert same-module padding, drawn from the pilot padding pool".
- Problem: the pilot was entirely `cli/cli`. A pilot pool cannot supply same-module padding for the three caddy instances.
- Replacement: state the actual padding source per repository. If caddy instances received cli/cli code, call it cross-repository padding for those instances and report Wpad contrasts with and without them.

**15. The position confound is misstated.**
- Offending text: "Wpad places W after the padding, and the adversarial review of Phase 1 noted that serialisation always places W last; position effects \cite{liu2024} are therefore not separated from content."
- Problem:
  - If W is last in both Wpad and A1, position is held constant in Wpad−A1. Position is then not confounded with content in that contrast.
  - In Wpad−W, position and length are confounded with each other, not with content.
  - The citation of an "adversarial review of Phase 1" is unverifiable (see item 16).
- Replacement: "In both A1 and Wpad, W follows the added text, so Wpad$-$A1 holds W's position fixed. Wpad$-$W changes length and W's distance from the prompt start together. Position is therefore separated from content only in Wpad$-$A1, and only if A1 serialises W last; [state A1's serialisation]."

**16. Unverifiable authorities are cited as evidence.**
- Offending text:
  - "The adversarial review judged the repair procedure sound."
  - "As noted in the external critique, leave-one-out measures …"
  - "An idea raised in the external critique …"
  - "An independent adversarial critique … from a Claude agent run by the author".
- Problem:
  - None of these critiques is archived or cited.
  - An endorsement by the author's own AI agent is not evidence.
  - An agent run by the author on the same vendor's models is not "independent".
- Replacement:
  - Delete "The adversarial review judged the repair procedure sound."
  - State the leave-one-out limitation in the author's own voice: "Leave-one-out measures …".
  - Either cite the critiques with an archived location or write "a critique received by the author (not archived)".
  - Change "An independent adversarial critique" to "An adversarial critique".

**17. An invented intention.**
- Offending text: "This was an exploratory budget decision."
- Problem: the 2026-10-13 note gives the reason as responsiveness (A1 ≥ 0.1), not budget.
- Replacement: "The restriction followed the note of 2026-10-13, which limited leave-one-out to instances with A1 $\geq 0.1$ on Haiku 5.5."

**18. The diagnostic's scope is ambiguous, and "changed the outcome" is overstated.**
- Offending text: "It examined the three Phase 2 cells listed above, in which context changed the outcome."
- Problem:
  - The preceding list contains five model–instance cells, not three.
  - The diagnostic covered only three: Sonnet 5.5 on c8591a1e46e4, Haiku 5.5 on 2bcdfbb1ac02, and Haiku 5.5 on 6727b2f3a92b.
  - Haiku 5.5 on c8591a1e46e4 (57/100 against 46/100) is not a resolved change.
- Replacement:
  - "It examined three cells: caddy c8591a1e46e4 on Sonnet 5.5, cli 2bcdfbb1ac02 on Haiku 5.5 and caddy 6727b2f3a92b on Haiku 5.5."
  - Retitle the earlier paragraph "Cells with large differences between arms" and give counts, for example "Sonnet 5.5 6/10 against 2/10".

**19. Small-k differences are presented as effects or drift.**
- Offending text:
  - "A1 beat W on Sonnet 5.5 (0.60 against 0.20) but lost to W on both Haiku models."
  - "There was also day-to-day variation in Sonnet's W cell on cli 2bcdfbb1ac02: 0.00 in Phase 2 and 0.30 in Phase 3."
- Problem:
  - 6/10 against 2/10 has Fisher p ≈ 0.17.
  - 8/20 against 3/20 (Haiku 4.5) has p ≈ 0.16.
  - 0/10 against 3/10 has p ≈ 0.21.
  - "Drift" and "variation" imply a mechanism that sampling noise explains.
- Replacement:
  - "The point estimates favoured A1 on Sonnet 5.5 (6/10 against 2/10) and W on both Haiku models (Haiku 5.5 57/100 against 46/100; Haiku 4.5 8/20 against 3/20). None is resolved at these $k$."
  - "Sonnet's W cell on cli 2bcdfbb1ac02 was 0/10 in Phase 2 and 3/10 in Phase 3, which is compatible with sampling noise."

**20. Padding "Supported" item: report the sign counts.**
- Offending text: "inert same-module padding matched to A1's size lowered pass rates relative to both W and A1. Both intervals exclude zero in both sample sets."
- Problem:
  - Wpad−A1 has signs 5/6/0 (post-screen) and 4/6/1 (all samples). The mean is carried by a few large drops: babd691446b9 0.16 against 1.00; 8f7afbdbdbd6 0.28 against 0.92.
  - Percentile bootstrap intervals at n=11 with skewed differences are unreliable.
  - "Inert" and "same-module" are unverified (item 14).
- Replacement: "… lowered mean pass rates relative to W ($-0.138$, signs 3/7/1) and A1 ($-0.178$, signs 5/6/0). The means are driven by large drops on 2–4 instances. Intervals at $n=11$ exclude zero in both sample sets."

**21. Table~\ref{tab:p3inst}: the `--=` cells contradict the caption, and the identity on cli 2bcdfbb1ac02 is suspect.**
- Offending text: the caption, "A trailing $=$ marks an arm byte-identical to another arm (it carries that arm's rate)". Also the body: "On babd691446b9, 2bcdfbb1ac02 and cba9646b8c25 it is marked as identical … without a separate rate."
- Problem:
  - These cells carry no rate and do not name the arm they duplicate.
  - On 2bcdfbb1ac02, A1t keeps queries and iostreams (Phase 2), so it can be identical to neither W nor A1.
- Replacement: name the identical arm and give its rate, or state "not run". Explain the 2bcdfbb1ac02 A1t identity, or correct the table.

**22. Wrong or missing date.**
- Offending text: "\textbf{H1 (revised after the pilot; date recorded in the preregistration).}"
- Replacement: "\textbf{H1 (revised 2026-10-11).}"

**23. References and DOIs that cannot be verified from the sources.**
- Offending text:
  - "concept DOI 10.5281/zenodo.23282195"
  - Stage 1 DOI "10.5281/zenodo.23307547"
  - "Gloaguen et al. Evaluating AGENTS.md. arXiv:2602.11988"
- Problem:
  - None of these appears in RESULTS.md or the preregistration.
  - The preregistration says Stage 1 will be registered on OSF at MSR submission, not on Zenodo.
- Replacement: confirm each identifier and give the full title and authors, or delete the identifier. For gloaguen2026, give the full title and verify the arXiv identifier.

**24. The record of deviations is inconsistent with its source.**
- Offending text: "The results file states that all events are recorded in Section 8 … The version of that section used to prepare this report does not contain the following items".
- Problem: the paper documents that the archive contradicts itself. Either §8 or the RESULTS line must be corrected before release.
- Replacement: add the 2026-10-12/13 hugo and mining-rejection events, the 2026-10-14 events and the relaxed-mining outcome to §8 with dates. Regenerate the RESULTS header. Change the paragraph to "These items were added to §8 on [date]".

**25. Double negative.**
- Offending text: "was lower than A1 in the pilot at $k=10$ by $-0.041$ $[-0.074, -0.013]$"
- Replacement: "differed from A1 in the pilot at $k=10$ by $-0.041$ $[-0.074, -0.013]$". Also replace "This day-to-day shift" with "This shift (which also confounds $k$ and date)".

**26. Table and prose disagree on the sample basis.**
- Problem: the caption of Table~\ref{tab:p3inst} does not say that the Haiku W and A1 columns pool all 50 samples. The primary contrasts use n=30.
- Replacement: append to the caption: "Haiku W and A1 pool screen and post-screen samples ($n=50$); the primary contrasts in Table~\ref{tab:p3con} use $n=30$ for these arms."

**27. Opus "no A1 arm" against the table.**
- Offending text: "Opus had no A1 arm."
- Problem: Table~\ref{tab:p2inst} shows Opus A1 0.00 on 015e6cf6ac39.
- Replacement: "Opus had no A1 arm; the A1 entry on 015e6cf6ac39 (0 dependencies) is W by identity."

**28. Garbled phrase.**
- Offending text: "Padding harmed Haiku 5.5 clearly but not Sonnet 5.5 on the resolved level."
- Replacement: "Padding lowered Haiku 5.5 pass rates with intervals excluding zero; the Sonnet 5.5 padding contrasts were unresolved."

**29. Compilation dependencies.**
- `\eps` is used throughout, including in `\bibitem`, but is not defined in the material shown. Add `\newcommand{\eps}{\varepsilon}` to the preamble.
- `\toprule`, `\midrule`, `\cmidrule`, `\addlinespace` and `\bottomrule` require `\usepackage{booktabs}`.
- `\url` requires `url` or `hyperref`.
- If these are absent, the file will not compile.

## OPTIONAL IMPROVEMENTS

1. Add a Phase 1 table; every Phase 1 number currently appears only in prose.
2. Report exact or binomial tests alongside the bootstrap for cell-level claims, for example 27/100 against 0/100 on queries removal, Fisher p < 10⁻⁸. Note that this is one of 22 removals tested.
3. Report W−A1 signs (3/3/4) for Phase 2 Haiku 5.5, for symmetry with the other contrasts.
4. Print LBs to four decimals where they sit at the margin (Sonnet A1t−W −0.050).
5. Use one model label consistently: Table~\ref{tab:p2con} prints "haiku-4-5-20251001", while Table~\ref{tab:p2inst} and the prose use "Haiku 4.5".
6. Render the predictor lists in Table~\ref{tab:loo} with `\texttt{}`; straight quotes typeset as ‘ ’.
7. Typeset Table~\ref{tab:p3inst} (23 columns) as `sidewaystable` or `table*`, and Table~\ref{tab:p2inst} as `table*`, to avoid overfull boxes.
8. State that the Phase 2 models and per-model k were not fixed in a dated amendment, if that is the case.
9. Explain why only 10 of the 14 valid caddy instances were screened.
10. State the overlap of the Phase 2 and Phase 3 instance sets (6727b2f3a92b, c8591a1e46e4, 2bcdfbb1ac02).
11. Note that the 2026-10-12 Phase 1 reading in the preregistration ("on 22 of 23 instances dependency interfaces add nothing measurable") is superseded by this report's treatment of the babd691446b9 exclusion as post hoc.
12. Abstract: change "Some aggregates were seen" to "One aggregate (Phase 1) was seen", and qualify "with headroom" as "selected for headroom on Haiku 5.5" (Sonnet was at ceiling on 6/11).
13. Clarify that the "relative" contrasts are absolute differences in pass rate, and that non-degeneracy concerns the best arm's absolute level.
14. The inference in the final Interpretation paragraph, from "no dependency-only identifiers" to "presentation rather than facts", ignores type and signature information used without being copied. Say so.
15. "This is the sense of `reader effects' in the title": the title is not shown in this body, so confirm that it matches.
16. Note that percentile bootstrap intervals at n=10–11 tend to under-cover.

NOT YET