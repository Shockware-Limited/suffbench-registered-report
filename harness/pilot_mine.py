"""Systematic instance mining for the SuffBench pilot.

Walks first-parent commits of the corpus since --since, applies M1..M6, writes instances/<id>.json for valid
instances and appends one line per examined commit to instances/rejected.jsonl (reason or "valid").

Usage: python pilot_mine.py --clone /path/to/cli --wt /path/to/worktree \
         --since 2026-09-01 --target 24 --out instances/ --template instances/cli__cli-9b031151a825.json
"""
import argparse, json, os, re, sys, pathlib, hashlib, urllib.request
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
from run_mutation import run, GO, load_packages, build_graph

KW = {"func","return","package","import","var","const","type","struct","interface","map","chan","range","for","if","else",
      "nil","true","false","string","int","bool","error","err","opts","len","append","switch","case","default","break",
      "continue","defer","go","select","fallthrough","goto","byte","rune","any","make","new","cap","copy","delete","panic",
      "recover","print","println","int64","int32","uint","float64","context","fmt","strings","testing","assert","require"}
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]{2,}")
STR = re.compile(r'"(?:[^"\\]|\\.)*"|`[^`]*`')

def code_tokens(line, keep_literals):
    """Identifiers (and optionally string-literal word tokens) from one added source line, comments removed."""
    s = line.lstrip()
    if s.startswith("//"): return set(), set()
    lits = set()
    for m in STR.finditer(s): lits |= set(IDENT.findall(m.group(0)))
    s = STR.sub('""', s); s = s.split("//")[0]
    ids = set(IDENT.findall(s)) - KW
    return ids, (lits if keep_literals else set())

def git(clone, *a): return run(["git", *a], clone).stdout

def added_lines(patch, test):
    out, cur = [], None
    for l in patch.splitlines():
        if l.startswith("+++ b/"): cur = l[6:]
        elif l.startswith("+") and not l.startswith("+++") and cur and cur.endswith(".go") and (cur.endswith("_test.go") == test):
            out.append(l[1:])
    return out

def test_events(stdout):
    """(failing top-level tests as pkg->set, build_failed:bool, pkg_status)"""
    fails, status, build_failed = {}, {}, False
    for l in stdout.splitlines():
        try: e = json.loads(l)
        except Exception: continue
        if e.get("Action") == "output" and "[build failed]" in e.get("Output", ""): build_failed = True
        if e.get("Test") and e.get("Action") == "fail": fails.setdefault(e["Package"], set()).add(e["Test"].split("/")[0])
        if e.get("Test") is None and e.get("Action") in ("pass", "fail", "skip"): status[e["Package"]] = e["Action"]
    return fails, build_failed, status

def gh_api(path):
    try:
        req = urllib.request.Request("https://api.github.com" + path, headers={"User-Agent": "suffbench-pilot", "Accept": "application/vnd.github+json"})
        tok = os.environ.get("GITHUB_TOKEN")
        if tok: req.add_header("Authorization", "Bearer " + tok)
        with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)
    except Exception as e:
        return {"_error": str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True); ap.add_argument("--wt", required=True); ap.add_argument("--since", default="2026-09-01")
    ap.add_argument("--target", type=int, default=24); ap.add_argument("--out", default="instances"); ap.add_argument("--template", required=True)
    ap.add_argument("--max-commits", type=int, default=80); ap.add_argument("--branch", default=None)
    a = ap.parse_args()
    tpl = json.load(open(a.template, encoding="utf-8"))
    branch = a.branch or next(b for b in ("origin/trunk", "origin/main", "HEAD") if run(["git", "rev-parse", "--verify", b], a.clone).returncode == 0)
    commits = git(a.clone, "log", f"--since={a.since}", "--first-parent", "--format=%H", branch).split()
    rej = open(os.path.join(a.out, "rejected.jsonl"), "a", encoding="utf-8")
    seen = set()
    for l in open(os.path.join(a.out, "rejected.jsonl"), encoding="utf-8"): seen.add(json.loads(l)["commit"])
    def log(c, reason, **kw):
        rej.write(json.dumps({"commit": c, "reason": reason, **kw}) + "\n"); rej.flush(); print(f"{c[:10]} {reason}", flush=True)
    valid = 0; examined = 0
    for C in commits:
        if valid >= a.target or examined >= a.max_commits: break
        if C in seen: continue
        examined += 1
        P = git(a.clone, "rev-parse", C + "^").strip()
        # diff against the first parent explicitly: `git show` on a merge commit gives a combined diff
        ns = [l.split("\t") for l in git(a.clone, "diff", "--name-status", "-M", P, C).splitlines() if l.strip()]
        files = [(s[0][0], s[-1]) for s in ns]
        if any(p in ("go.mod", "go.sum") or p.startswith("vendor/") for _, p in files): log(C, "touches_go_mod_or_vendor"); continue
        src = [(s, p) for s, p in files if p.endswith(".go") and not p.endswith("_test.go")]
        tst = [(s, p) for s, p in files if p.endswith("_test.go")]
        if not src or not tst: log(C, "needs_source_and_test_change"); continue
        if any(s == "D" for s, _ in src) or any(s == "R" for s, _ in src + tst): log(C, "deletes_or_renames_source"); continue
        src_dirs = sorted({os.path.dirname(p) for _, p in src}); tst_dirs = sorted({os.path.dirname(p) for _, p in tst})
        if len(src_dirs) > 2: log(C, "more_than_2_packages", n=len(src_dirs)); continue
        numstat = git(a.clone, "diff", "--numstat", P, C, "--", *[p for _, p in src])
        churn = sum(int(x.split("\t")[0]) + int(x.split("\t")[1]) for x in numstat.splitlines() if x.strip() and not x.startswith("-"))
        if churn > 120: log(C, "churn_over_120", churn=churn); continue
        # M2: parent + child's tests must compile and fail
        run(["git", "checkout", "-q", "-f", P], a.wt); run(["git", "clean", "-fdq"], a.wt)
        test_files = {}
        for s, p in tst:
            full = os.path.join(a.wt, p)
            if s == "D":
                if os.path.exists(full): os.remove(full)
                test_files[p] = None
            else:
                content = git(a.clone, "show", f"{C}:{p}"); os.makedirs(os.path.dirname(full), exist_ok=True)
                open(full, "w", encoding="utf-8", newline="\n").write(content); test_files[p] = content
        pk, mod = load_packages(a.wt)
        if not pk: log(C, "go_list_failed_at_parent"); continue
        W = sorted({f"{mod}/{d}" if d else mod for d in src_dirs}); tpkgs = [f"./{d}/" for d in tst_dirs]
        if any(w not in pk for w in W): log(C, "write_set_not_in_module", W=W); continue
        t = run([GO, "test", "-count=1", "-json", *tpkgs], a.wt, timeout=900)
        fails, build_failed, _ = test_events(t.stdout)
        if build_failed: log(C, "child_tests_do_not_compile_at_parent"); continue
        if not fails: log(C, "no_failing_test_at_parent"); continue
        f2p = sorted({f"{p}:{tn}" for p, ts in fails.items() for tn in ts})
        # M3: green at child on test pkgs, then on W ∪ F
        run(["git", "checkout", "-q", "-f", C], a.wt); run(["git", "clean", "-fdq"], a.wt)
        t2 = run([GO, "test", "-count=1", "-json", *tpkgs], a.wt, timeout=900)
        f2, bf2, st2 = test_events(t2.stdout)
        if bf2 or f2 or any(v == "fail" for v in st2.values()): log(C, "not_green_at_child_testpkgs"); continue
        pkC, modC = load_packages(a.wt); deps, tdeps, fwd = build_graph(pkC, modC)
        F = sorted(set().union(*[fwd.get(w, set()) for w in W]) - set(W))
        scope = [p for p in W + F if p not in tpl["baseline_fail_pkgs"]]
        t3 = run([GO, "test", "-count=1", "-json", *scope], a.wt, timeout=2400)
        _, bf3, st3 = test_events(t3.stdout)
        bad = sorted(p for p, v in st3.items() if v == "fail")
        if bf3 or bad: log(C, "not_green_at_child_WuF", failing=bad[:10]); continue
        # M4: identifier leak (new names in gold code/literals that the added test lines reference)
        gold_patch = git(a.clone, "diff", P, C, "--", *[p for _, p in src])
        test_patch = git(a.clone, "diff", P, C, "--", *[p for _, p in tst])
        gold_ids, gold_lits = set(), set()
        for l in added_lines(gold_patch, False):
            i, s = code_tokens(l, True); gold_ids |= i; gold_lits |= s
        # "introduced" = not present in the write-set's own non-test sources at the parent (conservative:
        # also catches names the patch newly imports from a dependency, and private strings the test pins)
        w_tokens = set()
        for w in W:
            for f in pk[w].get("GoFiles", []):
                try: w_tokens |= set(IDENT.findall(open(os.path.join(pk[w]["Dir"], f), encoding="utf-8", errors="replace").read()))
                except FileNotFoundError: pass
        new = (gold_ids | gold_lits) - w_tokens - KW
        test_toks = set()
        for l in added_lines(test_patch, True):
            i, s = code_tokens(l, True); test_toks |= i | s
        leak = sorted(new & test_toks)
        if leak: log(C, "test_references_gold_identifiers", leak=leak[:10]); continue
        # M5: task text
        subj = git(a.clone, "show", "-s", "--format=%s%n%b", C)
        m = re.search(r"#(\d+)", subj); pr = gh_api(f"/repos/cli/cli/pulls/{m.group(1)}") if m else {}
        issue_no = None
        for pat in (r"(?:[Ff]ix(?:es|ed)?|[Cc]lose[sd]?|[Rr]esolve[sd]?)\s*:?\s*(?:https://github.com/cli/cli/issues/)?#?(\d+)",):
            mm = re.search(pat, (pr.get("body") or "") + "\n" + subj)
            if mm: issue_no = mm.group(1); break
        task_text, src_kind, url = None, None, None
        if issue_no:
            iss = gh_api(f"/repos/cli/cli/issues/{issue_no}")
            if iss.get("body") and "pull_request" not in iss:
                task_text = f"# {iss['title']}\n\n{iss['body']}"; src_kind = "issue"; url = iss.get("html_url")
        inst_id = f"cli__cli-{P[:12]}"
        d = {k: tpl[k] for k in ("repo", "repo_path", "api_key_file", "baseline_fail_pkgs")}
        d.update({"instance_id": inst_id, "base_commit": P, "gold_commit": C, "created_at": git(a.clone, "show", "-s", "--format=%cI", C).strip(),
                  "pr_number": m.group(1) if m else None, "pr_title": pr.get("title"), "pr_body": pr.get("body"), "commit_message": subj.strip(),
                  "task_text": task_text, "task_text_source": src_kind or "rewritten_spec_pending", "task_text_url": url,
                  "gold_patch": gold_patch, "test_patch": test_patch, "test_files": test_files, "write_set": W, "interface_write_set": [],
                  "test_pkgs": tpkgs, "fail_to_pass": f2p, "forward_slice": F, "gold_new_identifiers": sorted(new),
                  "churn": churn, "cutoff_flags": {"note": "model cutoffs recorded at analysis; instance postdates 2026-09-01"},
                  "validity": {"status": "valid_pilot", "checks": "M1-M4 passed by pilot_mine.py", "task_text_review": "pending_author"}})
        json.dump(d, open(os.path.join(a.out, inst_id + ".json"), "w", encoding="utf-8"), indent=1)
        valid += 1; log(C, "valid", instance_id=inst_id, W=W, f2p=f2p, churn=churn, nF=len(F), task=src_kind or "spec_pending")
    run(["git", "checkout", "-q", "-f", commits[0]], a.wt)
    print(f"examined={examined} valid={valid}")

if __name__ == "__main__":
    main()
