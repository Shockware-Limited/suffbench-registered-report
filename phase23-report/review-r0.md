## REQUIRED edits (most severe first)

**1. False claim that the Phase 3 A1t contrasts were not computed (four places).**

Offending text:
- §Results, Phase 3: "Haiku 5.5 ran A1t on all 11 instances; the contrasts A1t$-$A1 and A1t$-$W were not computed for this report."
- §Limitations: "\textbf{Phase 3 A1t contrasts.} … it was not computed for this report."
- §Limitations, H5 item: "(no A1g arm; A1t$-$A1 on Haiku 5.5 is computable from the Phase 3 samples but was not computed)".

Problem:
- RESULTS and Table~\ref{tab:p3con} report Haiku 5.5 A1t$-$A1 and A1t$-$W in both sample sets: post-screen $-0.046$ $[-0.177,+0.051]$, LB $-0.156$, 2/2/4, $n=8$; and $-0.087$ $[-0.223,+0.000]$, LB $-0.203$, 0/2/6, $n=8$.
- Preregistration §8, 2026-10-18 (vii), states that H5b "was computable on the Phase 3 instances and is reported there".
- "Ran A1t on all 11" is also unsupported. Table~\ref{tab:p3inst} gives A1t rates on 8 instances only, and marks the other 3 "--=" with no rate.
- Of those 8, six are byte-identical carry-overs ("="). Distinct A1t data exist only on c8591a1e46e4 (0.44) and 8f7afbdbdbd6 (0.46). A1t$-$W is therefore driven by those 2 instances, and on the other 6 A1t$-$A1 equals W$-$A1.

Replacement:
- Results: "Haiku 5.5 has A1t rates on 8 of the 11 instances. On 6 of these A1t is byte-identical to another arm, and distinct A1t samples exist only on c8591a1e46e4 and 8f7afbdbdbd6. On the post-screen set, A1t$-$A1 was $-0.046$ $[-0.177, +0.051]$, LB $-0.156$, signs 2/2/4, $n=8$: not non-inferior. A1t$-$W was $-0.087$ $[-0.223, +0.000]$, LB $-0.203$, signs 0/2/6, carried entirely by those two instances. On all samples the figures are $-0.047$ $[-0.180, +0.045]$, LB $-0.155$, 5/3/0; and $-0.090$ $[-0.220, +0.000]$, LB $-0.195$."
- Delete the "Phase 3 A1t contrasts" limitation item.
- H5 item: replace the parenthesis with: "(H5a untested, since there was no A1g arm; H5b would be a confirmatory test that failed, A1t$-$A1 LB $-0.156$ on $n=8$, six of them by byte identity)".

**2. Table~\ref{tab:p3con} reports Sonnet 5.5 A1t contrasts for an arm Sonnet never sampled.**

Offending text: Sonnet columns, rows "A1t $-$ A1 … $+0.083$ $[+0.000, +0.217]$ & $+0.000$ & 2/0/4" and "A1t $-$ W … $+0.000$ …".

Problem:
- The Phase 3 arm list for Sonnet (results file; amendment of 2026-10-13) excludes A1t.
- The Sonnet sample total confirms this: 260 (Phase 2) + 60 cells × 10 (Phase 3) = 860.
- These rows are therefore W$-$A1 and W$-$W imputed through byte-identity, on 6 instances. As printed, A1t$-$A1 (LB $+0.000$) reads as a passed H5b non-inferiority test on Sonnet.

Replacement: delete the Sonnet cells of both A1t rows (set them to "--"). Add to the caption: "Sonnet 5.5 did not run A1t."

**3. Padding source described as unrecorded, and an invented pilot-pool argument (abstract, §Arms, Limitations ×2).**

Offending text:
- Abstract: "and the padding source there is unrecorded".
- §Arms: "The pilot was drawn entirely from \texttt{cli/cli}, so for the three caddy instances a pilot pool cannot supply same-module padding as described. The padding source for the caddy instances is not recorded in the results file".
- Limitations: "The padding source for the caddy instances in Wpad is not recorded".
- Limitations, Wpad item: "cause not recorded".

Problem:
- RESULTS states that the padding "is drawn from same-module packages outside W, its dependencies and dependents, in a fixed hash order". Package names are stored in each contexts.json under pad_meta. Per-instance counts are given, including 5 and 12 caddy packages.
- Preregistration §8, 2026-10-18 (iv), records the cause: the same-module pool was exhausted on the two largest caddy instances.
- "Pilot pool" refers to the pilot's padding procedure (prereg §5: same-repository code outside W∪B∪F), not to cli/cli files. The body's inference is unsupported.

Replacement:
- Abstract: "token matching fell short on two of the three caddy instances, where the same-module padding pool was exhausted."
- §Arms: "The padding is drawn from same-module packages outside W, its dependencies and dependents, in a fixed hash order. Package names are recorded in each contexts.json under pad_meta (5 and 12 packages on the two short caddy instances). The pool was exhausted below A1's size on those instances (deviation of 2026-10-18 (iv)). The `inert' property has not been verified."
- Limitations: delete "padding source … not recorded" and "cause not recorded". Cite 2026-10-18 (iv).

**4. The 2026-10-18 deviation entry is omitted, and items it covers are called "not in Section 8".**

Offending text:
- "Further events not recorded in the version of Section 8 used for this report are listed in Section~\ref{sec:lim}."
- The list headed "Deviations not in the version of Section 8 used for this report", including the items Wpad token matching, Amendment (iv), Phase 3 sample set and Phase 3 A1t contrasts.

Problem: preregistration §8 contains a dated 2026-10-18 entry that records the following:
- (i) amendment (iv) not performed;
- (ii) pilot-instance reuse;
- (iii) same-day pairing not met;
- (iv) the Wpad pool exhausted;
- (v) post-screen primary chosen post hoc;
- (vi) one- versus two-sided bound;
- (vii) H5b reported, and hugo dropped "for cost" with partial data labelled;
- (viii) a by-model spend rounding error, corrected.

Replacement:
- Add to the dated amendments list: "\item \textbf{2026-10-18, deviations recorded at write-up.} (i) amendment (iv) not performed; (ii) 8 of 11 Phase 3 instances are pilot instances; (iii) Phase 3 pairs were not same-day; (iv) Wpad pool exhausted on two caddy instances; (v) post-screen set designated primary after seeing data; (vi) one-sided bound adopted; (vii) H5b computable and reported, hugo dropped with partial data labelled; (viii) by-model spend rounding error corrected."
- Restrict the "not in Section 8" list to items absent from every entry: the hugo baseline contamination and 17 mining rejections, the 2026-10-14 build-cache incident and 17-record purge, the relaxed-mining outcome, the missing Phase 2 cells, and the 162-sample screen shortfall.

**5. Hugo drop reason conflicts between sources, and partial data are not mentioned.**

Offending text: "That instance was dropped on 2026-10-14 because it produced a 182 GB build cache."

Problem: RESULTS gives the build cache as the reason. Prereg 2026-10-18 (vii) says "dropped for cost, with partial data labelled as such". The body reports neither the discrepancy nor the partial data.

Replacement: append "The preregistration (2026-10-18 (vii)) records the reason as cost. Partial hugo data exist and are labelled as such; they are excluded from all contrasts."

**6. Same-day pairing is misreported.**

Offending text:
- "whether each pair was sampled on the same day is not recorded".
- The Phase 3 amendment summary, which omits "All contrasts are same-day paired within instance".

Problem: the amendment required same-day pairing. Deviation 2026-10-18 (iii) records that W and A1 began with the 2026-10-13 screen while the other arms ran on 2026-10-13/14.

Replacement:
- In the amendment summary, add "and requires same-day pairing within instance".
- In Limitations: "Pairs were not same-day: W and A1 began with the 2026-10-13 screen and the other arms ran on 2026-10-13/14 (deviation 2026-10-18 (iii))."

**7. A mechanism stated as a consequence of an unverified diagnostic.**

Offending text: "If the unverified diagnostic is right that passing patches did not use dependency-only identifiers, then the differences between arms reflect how a model responds to a presentation rather than which facts are available."

Problem: the absence of new identifiers does not exclude informational use. Types, signatures or semantics can guide a patch without their identifiers appearing in it. The conditional asserts the untested mechanism that the body disclaims elsewhere.

Replacement: "If the unverified diagnostic is right, the differences between arms need not involve identifiers that only dependency text supplies; whether they reflect presentation rather than information is untested."

**8. The preregistration's missing-data rule is misquoted.**

Offending text: "Section 6 of the preregistration requires missing data to be flagged with its cause".

Problem: §6 says API errors are retried, then recorded as missing, excluded from the pair, and the instance flagged. It does not require a cause.

Replacement: "Section 6 of the preregistration requires missing data to be recorded and the instance flagged; neither is done in the results file".

**9. The "well above W" wording contradicts the body's own "unresolved".**

Offending text: "on the two Phase 2 cells in which A1 passed well above W (… caddy c8591a1e46e4 on Sonnet 5.5: 0.00 against 0.60)".

Problem: the body states that 6/10 against 2/10 is not resolved ("None is resolved at these $k$").

Replacement: "on the two Phase 2 cells with the largest A1-over-W point estimates (cli 2bcdfbb1ac02 at $k=100$: 0.14 against 0.27; caddy c8591a1e46e4 on Sonnet 5.5 at $k=10$, unresolved: 0.00 against 0.60)".

**10. A non-replicated cell is listed as "Supported".**

Offending text: "Supported … (cli 2bcdfbb1ac02: W 0/100, A1 27/100; caddy 6727b2f3a92b: W 44/100, A1 22/100); the second did not replicate".

Problem: a result that failed to replicate is not supported.

Replacement: keep cli 2bcdfbb1ac02 and the queries removal under "Supported". Move caddy 6727b2f3a92b to "Fragile" with the replication failure.

**11. The A0 exclusion is unexplained, and A0 is undefined.**

Offending text: "Opus 5.5 also ran an arm labelled A0 … it is excluded from the analysis in this report."

Problem:
- A0 is never defined.
- A0$-$W ($-0.140$ $[-0.440, +0.120]$) appears in Table~\ref{tab:p2con}.
- On 7910dd94eea2, A0 passed 0.60 against W 0.00. On 2bcdfbb1ac02 A0 passed 0.80, as did W. Silently excluding an arm that outperforms W on a task-only basis is selective.

Replacement: define A0, state the reason for exclusion, and report "On Opus 5.5, A0 exceeded W on caddy 7910dd94eea2 (0.60 against 0.00, $k=5$) and equalled W on cli 2bcdfbb1ac02 (0.80)."

**12. Wording implies equivalence.**

Offending text: "Wd retains W's pass rate within the margin".

Replacement: "Wd's one-sided lower bound against W clears $-0.05$".

**13. Wrong contrast count.**

Offending text: "not adjusted for the eight contrasts".

Problem: Table~\ref{tab:p3con} has ten Phase 3 contrasts.

Replacement: "not adjusted for the ten contrasts".

**14. Preregistered task-text thresholds are misstated.**

Offending text: "a whole-word package name above a preregistered minimum length; a unique exported identifier above a preregistered minimum length", and the selector clause.

Problem: the preregistration says "length ≥4" and "length ≥6". It also includes the selector `v.Name` with Name exported by exactly one direct dependency.

Replacement: "a selector \texttt{alias.Name} resolved through W's imports, or \texttt{v.Name} where \texttt{Name} is exported by exactly one direct dependency; a whole-word package name of length at least 4; a unique exported identifier of length at least 6."

**15. LaTeX compile risks.**

- `\eps` is not a standard macro. Ensure `\newcommand{\eps}{\varepsilon}` is in the preamble, or replace `\eps` with `\varepsilon` throughout.
- `\toprule`, `\midrule`, `\cmidrule` and `\addlinespace` require `\usepackage{booktabs}`.
- `\url` requires `url` or `hyperref`.
- `abstract` requires a class that defines it.
- If any of these is absent, the document will not compile.

**16. Missing DOI for the definitions note.**

Offending text: `\bibitem{definitions}` with no identifier.

Problem: the preregistration gives DOI 10.5281/zenodo.23282196.

Replacement: add "DOI \url{https://doi.org/10.5281/zenodo.23282196}."

**17. H1 revision date omitted.**

Offending text: "\textbf{H1 (revised after the pilot).}"

Replacement: "\textbf{H1 (revised 2026-10-11, after the pilot).}"

## OPTIONAL improvements

1. Opus has no A1t cell on 2bcdfbb1ac02. The sample count (105 = 21 distinct cells × 5) shows it was never sampled, unlike the Haiku 4.5 cells, which were sampled and not reported. Say so.
2. The three "--=" A1t entries in Phase 3 most likely mark identity with A1g, which was not run in Phase 3. This would also resolve the 2bcdfbb1ac02 "conflict", since A1t = A1g there. Verify this and state it.
3. Phase 2 Haiku 5.5 W$-$A1: add the signs 3/3/4.
4. State that the token ratios 0.77 and 0.83 are computed from Table~\ref{tab:p3inst}. The audit flagged 0.77 as absent from RESULTS; it is $183{,}345/237{,}893$.
5. The per-instance padding narrative uses pooled ($n=50$) W and A1 rates, while the primary contrasts use post-screen rates. Say this, or quote the post-screen rates. Note also that Wpad$-$W is negative on 7 of 11 instances, not only on "2–4".
6. Phase 2 sample total: 7754 exceeds the reconstructed cells (about 5,685) by about 2,069. This is presumably leave-one-out samples on floor instances. Quantify it.
7. Of the 14 caddy instance directories, only 10 were screened. Explain why.
8. Tables~\ref{tab:p3inst} (23 columns) and~\ref{tab:p3con} will overflow `\textwidth`. Use `sidewaystable` or `\resizebox`. Also note in Table~\ref{tab:p3inst}'s caption that the Haiku W and A1 columns pool the screen and post-screen samples.
9. Haiku 4.5 W$-$A1 has an LB of $-0.013$, so it clears the margin under both bounds. Say so explicitly, alongside "no information".
10. Quote the pilot P200$-$A1 erratum value ($-0.029$ $[-0.129, +0.081]$) in "Interpretation (pilot curve)".
11. "the sense of `reader effects' in the title": no title is visible in the body. Confirm that it exists.
12. Check A1's serialisation order instead of leaving the position confound conditional.
13. Since the prereg H5 text says "at most 16 contiguous groups", state that number.

PUBLISHABLE AFTER EDITS