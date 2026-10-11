# HANDOFF: SuffBench pilot — degradation curve at verified coverage

Written 2026-10-11 by the design model (Fable 5.1). Executed by a cheaper agent (Haiku) against the author's
Anthropic key. Read the whole file before running anything. Every section has an acceptance check; do not
proceed past a failed check — stop and report.

## 0. What this pilot is for

The published note (DOI 10.5281/zenodo.23282824) defines a context K as ε-sufficient when the editor's pass rate on K
is within ε of its best pass rate over a candidate family, and proves that under a decreasing load curve g,
sufficiency is not closed under superset. Nothing empirical has been run yet. This pilot produces the first numbers:

- **G (primary): the degradation curve.** For each model, pass rate as a function of absolute context load
  {base, 32k, 64k, 128k, 200k tokens} while *coverage is held fixed* (the base context already contains everything
  the fix needs; the extra load is irrelevant same-repository code). This is the note's g, estimated with intervals.
  The "smallest context that gives the same result" is read off this curve: the smallest load whose pass rate is
  within ε of the curve's maximum. It is a curve with a probability on the y-axis, not a single number.
- **Flip rate** (run-to-run variation at default sampling) and **between-arm disagreement π_d**, which the
  Registered Report (main.tex, §Analysis) needs to fix its non-inferiority margin ε before 20 Nov 2026.
- **H2 at base load, descriptive:** W vs W+iface(deps) vs W+bodies(deps). Expect mostly ceiling (all pass); report
  the ceiling rate honestly — it is itself a finding about this task class.
- **A∅ (task text only):** detects memorisation / under-specified tasks. Any instance the model solves with no
  repository context is flagged and excluded from G.

This is a pilot: exploratory, instance set disjoint from the future confirmatory set, no hypothesis is "confirmed".
The numbers go into the Registered Report (private until Stage 1 submission). Do not publish outcomes anywhere.

## 1. Budget and stop rules

- Anthropic credit remaining: **$89.15** (2026-10-11). Hard cap for this pilot: **$70**. Keep ≥ $19 reserve.
- Record cumulative spend after every instance from the `usage` fields using the price table in §7. Stop at $60
  and report; the author decides whether to continue.
- Stop and report if: any instance's fail-to-pass check behaves unexpectedly; any arm's pass rate on W is 0 for
  more than 3 instances (suggests a harness bug, not a model effect); API errors other than 400 "prompt too long"
  recur after retries; more than 10% of samples fail to parse.
- Never print, log, or commit the API key. Never use the agent harness's own ANTHROPIC_* credentials (the runner
  already pops them; keep that code).

## 2. Environment (Windows, Git Bash) — all previously hit, all fixed, do not rediscover

- Python with the SDK: `/c/Python314/python`. `anthropic` 1.13.0 lives in the *user* site-packages, which Python
  cannot find once `APPDATA` is overridden. Always export
  `PYTHONPATH='C:\Users\visci\Python\Python314\site-packages'` **and** use Windows-style paths for the Go vars:
  `GOCACHE='C:\Users\visci\AppData\Local\go-build' GOPATH='C:\Users\visci\go' GOMODCACHE='C:\Users\visci\go\pkg\mod'
  LOCALAPPDATA='C:\Users\visci\AppData\Local' APPDATA='C:\Users\visci\AppData\Roaming' PYTHONIOENCODING=utf-8`.
- Go binary: `'C:/Program Files/Go/bin/go.exe'` (quote it; `/c/Program Files/...` breaks in `$GO` expansion).
- Corpus: clone at `C:/Users/visci/tools/corpus/cli`; experiment worktree `C:/Users/visci/tools/corpus/wt`
  (instance `repo_path`). `wt2` exists for diagnosis only. Hashes from `git rev-parse` in the clone are valid in
  the worktree; **always take the full 40-char hash from `git rev-parse <ref>`**, never from a truncated display.
- Key file: `C:/Users/visci/.config/context-sufficiency-note/anthropic.key` (read with `utf-8-sig`).
- Harness: `suffbench-registered-report/harness/` — `build_contexts.py`, `run_instance.py`, `instances/`,
  `results/`. Contexts dirs `harness/contexts-*/` are git-ignored; results `.jsonl` are committed; `.log` ignored.
- Commit trailer: end commit messages with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- Before any `git checkout -f`/`clean` in the worktree, that is expected (the runner resets it). Never do it in the
  RR repo without `git status` first.

## 3. Lessons from the three instances already run (read before touching anything)

| Instance | What happened | Lesson |
|---|---|---|
| `cli__cli-7f0590c2b805` | 0/12 pass. Test pins private field name `isCrossRepository` via `ExpectFields`; issue text never mentions it. | Identifier-leak check must cover **string literals** in test diffs, not just code identifiers. Expressibility is syntactic and cannot catch this. |
| `cli__cli-9b031151a825` | 12/12 pass in all four contexts; identical 148-token edit every time. | Ceiling case. Useless for H2, **ideal base for the degradation curve** (coverage verified by pass rate 1.0 at base). |
| `cli__cli-b6770c8bc54c` | 11/11 pass. Model wrote `gh.TokenTypeUserToServer` even from W alone (inferred from the pattern). | Also a ceiling; also usable as a curve base. |
| `cli__cli-996be976cad9` | **Invalid, my error.** Gold patch changes two packages (`pkg/extensions` and `pkg/cmd/root`); write-set listed only one, so no context contained the caller; task text did not state the signature change. The 9 "failures" were caused by that. The 3 transitive samples never reached a model: 400 "prompt too long: 2.88M tokens > 1M". | Write-set = **all** packages whose non-test files the gold patch changes. Contexts above ~900k tokens are not runnable; record `api_error`, never count it as a model failure. The fail-to-pass check must require the parent **to compile** with the child's tests (a build failure at parent is a different thing). |

Analysis misreadings to avoid: `api_error` ≠ model failure; `applied=False` with `api_error` set is infrastructure;
differing output lengths are not evidence of anything; "the model struggled" is not a finding when the context
provably lacked the needed file.

## 4. Harness fixes (do these first; each has a check)

F1. **Write-set from the patch.** In the instance builder: parse `gold_patch` for `+++ b/<path>` with `.go` and not
`_test.go`; map each file to its package import path via `go list -json ./<dir>`; `write_set` = sorted unique set.
Check: for `cli__cli-996be976cad9` this yields two packages.

F2. **Expressibility on code only.** In `build_contexts.identifiers_added`, before extracting identifiers from an
added line: drop the line if its stripped content starts with `//`; strip any trailing `// ...` comment; strip the
contents of string literals (`"..."` and backticks). Keep the keyword drop-list. Check: on `cli__cli-b6770c8bc54c`
the missing set for W becomes exactly `['TokenTypeUserToServer']` and W+iface becomes expressible.

F3. **Window cap.** In the runner, before calling the API, count tokens with `client.messages.count_tokens` (free)
for the full message; if > 900,000 write a record with `api_error: "exceeds_window"` and `applied=False`, and skip
the call. Check: the old transitive context for 996b is skipped without a request.

F4. **Verdict cache by patch hash.** After applying blocks, compute `sha1(git diff -- '*.go' ':!*_test.go')`. Keep a
dict per instance; if seen, copy `builds/delta_pass/frame_pass/frame_fail_pkgs` from the earlier record and set
`verdict_cached: true`. Identical edits are common (the 148-token case) and this saves most verification time.

F5. **Frame check scoped to W ∪ F.** Replace `--full-suite` (`go test ./...`, too slow for ~1,800 samples) with
`go test -count=1 -json` over the packages in `write_set ∪ forward_slice` (from `contexts.json`), excluding
`baseline_fail_pkgs`. Record `frame_scope: "W∪F"`. Rationale (state it in the report): by the note's own observation,
a frame violation can only surface in dependents of W.

F6. **Record `n_tokens_prompt`** (from `count_tokens`) and `model`, `effort` (if used) in every record. Keep
`test_output` capture and the optional-FILE-header parser as they are.

F7. **Mark `cli__cli-996be976cad9` invalid** in its instance JSON (`validity.status = "invalid_misconfigured"`, reason
as in §3) and leave its results file in place.

Then read the `claude-api` skill (Skill tool, `claude-api`) once and confirm: exact model IDs for Haiku 5.5 and
Sonnet 5.5; whether `output_config: {effort}` is accepted by each (if not, omit it); long-context pricing tier
above 100k/200k input tokens; batch API availability. Write the confirmed values into §7 of this file.

## 5. Mining protocol (systematic — no hand-picking)

Candidate commits: `git log --since=2026-09-01 --first-parent --format=%H main` in the clone (cli/cli). For each
commit C with parent P, in order, until **24 valid instances** (target 20 + spares):

M1. Changed files: ≥1 non-test `.go` and ≥1 `_test.go`; no `go.mod`/`go.sum`/`vendor` changes; ≤ 2 changed
non-test packages; total non-test added+deleted lines ≤ 120.
M2. Checkout P in `wt`; write the child's versions of **all changed `_test.go` files** into place.
`go test -count=1 -json <changed test packages>` must **compile** and at least one test must **fail**. Record
the failing test names as `fail_to_pass`. (A build failure here → reject with reason `child_tests_do_not_compile_at_parent`.)
M3. Checkout C; the same packages must pass. Then run `go test -count=1 -json` over W ∪ F at C; any failing
package not in `baseline_fail_pkgs` → reject (`not_green_at_child`).
M4. Identifier leak: extract identifiers **and string literal contents** from added lines of the child's test
diff; intersect with identifiers added by the gold patch (code only, F2). Non-empty → reject
(`test_references_gold_identifiers`). Exception: none in the pilot (flagged spec-supplied variants are out of scope).
M5. Task text: if the commit message or PR body links an issue (`#NNNN`, `Fixes #`), fetch the issue body with
`gh issue view NNNN --repo cli/cli --json body` (needs `GH_CONFIG_DIR`) → `task_text_source: "issue"`. Otherwise
write a behaviour-only specification from the commit message and the test diff: what the command should do, no
identifiers, no file names, no field names → `task_text_source: "rewritten_spec"`. Save the draft; **the author
reviews every task text before the confirmatory run; for the pilot, record them and move on.**
M6. Write `instances/<id>.json` with the schema of `cli__cli-9b031151a825.json` plus `validity`, `reject_reason`
(for rejects, in a separate `instances/rejected.jsonl` with commit, reason), `fail_to_pass`, and `write_set` (F1).

Acceptance: `instances/rejected.jsonl` lists every examined commit with a reason; yield (valid / examined) is
reported. If yield < 10% after 60 commits, stop and report (the repo may need a different window).

The two existing ceiling instances count toward the 24 if they pass M1–M4 under the new rules (re-run the checks).

## 6. Arms for the pilot

Base arms (from `build_contexts.py`, W last, immediately before the task):

| Arm | Content |
|---|---|
| A∅ | task text only (no repository context) |
| W | write-set bodies |
| A1 = W+iface(deps) | W + `go doc -all` of direct in-module deps |
| A1b = W+bodies(deps) | W + bodies of direct deps |
| A1F | A1 + `go doc -all` of forward-slice packages + their test function names (`grep -h '^func Test'`) |

Padded arms P32, P64, P128, P200: **A1 padded to 32k/64k/128k/200k prompt tokens** (measured with `count_tokens`
on the full message). Padding = non-test source of same-module packages **outside W ∪ B ∪ F** and **not sharing a
parent directory with any W package** (lexical-proximity ceiling, pilot version). Order packages by
`sha1(instance_id + import_path)`; concatenate files in that order; cut the last file at a line boundary to hit
the target ± 2%. Padding goes **before** A1 so W stays last. Skip a level if A1 alone already exceeds it; skip any
message > 900k tokens (F3). Record `pad_pkgs` and `n_tokens_prompt`.

Do **not** run the full transitive arm in the pilot (it exceeded the window on 996b and costs the most).

## 7. Models, sampling, cost

Sampling parameters are not settable on these models: every sample is an independent default-sampling call.
Prompt caching (`cache_control` on the context block, already in the runner) makes samples 2..k nearly free.

| Model | Role | Arms | k | Est. cost (20 instances) |
|---|---|---|---|---|
| claude-haiku-5-5 | dense estimation | all 9 arms | 10 | ≈ $3–6 (check >100k tier) |
| claude-sonnet-5-5 | second model, descriptive | A∅, A1, P64, P128, P200 | 3 | ≈ $25–30 |

List prices seen 2026-10-10: Haiku 5.5 $0.10/$0.50 per M in/out (≤100k input), cache read $0.01; Sonnet 5.5
$2/$10, cache read $0.10; cache write ≈ 1.25× input. Confirm in the `claude-api` skill and overwrite this table.
Opus 5/5.5 is **out of scope** for the pilot (would exceed the cap); the two Opus 5 pipeline runs already done
are kept as pipeline evidence only.

Run order: (1) Haiku, one instance, all arms, k=2 → check records, spend, timing. (2) Haiku, all instances, k=10.
(3) Compute spend; if < $20 so far, Sonnet as in the table; if Sonnet projection would breach $60 total, drop P64.
(4) Report.

Runner invocation per instance (one call per arm set; `--only` to select arms; add a `--pad` mode or a separate
`pad_contexts.py` that writes P-arm files into the same contexts dir with entries in `contexts.json`):

```
/c/Python314/python run_instance.py --instance instances/<id>.json --contexts contexts-<id>/ \
  --model claude-haiku-5-5 --k 10 --out results/<id>-haiku55.jsonl
```

## 8. Analysis (`analysis/pilot.py`; outputs `results/PILOT-REPORT.md` + CSVs)

Per model:

1. **Curve G.** For each load level L ∈ {A1(base), P32, P64, P128, P200}: per-instance pass rate
   r_i(L) = passes/k (Δ-pass; and separately Δ∧frame). p̂(L) = mean_i r_i(L). CI: instance-level bootstrap
   (2,000 resamples, percentile). Also pooled Wilson for reference. Paired drop d(L) = p̂(base) − p̂(L) with bootstrap CI.
   Exclude instances flagged by A∅ (see 4) and report both with/without.
2. **Minimal sufficient load per instance** at ε ∈ {0.05, 0.10}: smallest L with r_i(L) ≥ max_L r_i(L) − ε.
   Histogram. (k=10 gives 0.1 granularity; say so.)
3. **Flip rate.** Over all cells with k ≥ 3: fraction of cells with non-unanimous outcomes; mean minority share.
   Report separately per model and per arm.
4. **A∅ control.** Per instance, A∅ pass rate; flag if > 0 (memorisation or under-specified task). Report count.
5. **H2 descriptive.** p̂(W), p̂(A1), p̂(A1b), p̂(A1F) with CIs; paired differences A1−A1b, A1−A1F; ceiling rate
   = fraction of instances with r_i(W) = 1. π_d = fraction of instances whose majority outcomes differ between A1
   and A1b.
6. **Cost.** Tokens and $ per arm per model from `usage`.
7. **Failure taxonomy** for non-passing samples: `no_blocks`, `apply_error`, `build_error`, `delta_fail`,
   `frame_fail`, `api_error`, `exceeds_window` — counts per arm. Never pool `api_error`/`exceeds_window` with model
   outcomes.

Deliverables: `results/PILOT-REPORT.md` (tables + a single curve figure per model, PNG via matplotlib), CSVs,
and a short `results/DEVIATIONS.md` listing every departure from this handoff with reasons.

## 9. What the author then does

- Reads every task text (M5) and every rejected reason; vetoes instances.
- Reads PILOT-REPORT.md; decides ε for the RR (rule in `preregistration.md`: ≥ 2× the larger flip rate, power ≥ 0.8
  at measured π_d), and inserts pilot numbers into `main.tex` (abstract, §Analysis "Pilot", §Threats).
- Keeps the RR repo private; submits abstract 13 Nov, report 20 Nov 2026.
- Optional public update now, no outcomes: the harness and the two pipeline-demonstration instance *configs*
  (not results) as SuffBench v0.1.1-tools, if a visible artefact is wanted before Stage 1.

## 10. Known gaps this pilot does not close (say them in the report)

One repository, one language; task texts partly rewritten by a model; padding of one type (same-repo, proximity
ceiling only); no open-weights model (temperature-zero flip rate still unmeasured); k=10 granularity; frame check
scoped to W ∪ F rather than the full suite; model training cutoffs unverified against commit dates (record what
the vendor documents).
