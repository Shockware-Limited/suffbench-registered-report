"""Build the named contexts for one SuffBench instance from a Go module checkout at the BASE commit.

Contexts (spec 0.1): W, W+iface(deps), W+bodies(deps), transitive (W + bodies+tests of B(W) ∪ F(W)).
Also: expressibility check (gold-patch identifiers present), token counts via the model tokenizer.

Usage: python build_contexts.py --instance inst.json --out contexts/
Requires the worktree at --repo to be checked out at base_commit (clean).
"""
import argparse, json, os, re, subprocess, sys, pathlib
from run_instance import resolve_repo
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
from run_mutation import load_packages, build_graph, run, GO  # reuse graph code

def go_doc_all(repo, pkg):
    r = run([GO, "doc", "-all", pkg], repo)
    return r.stdout if r.returncode == 0 else f"// go doc failed for {pkg}: {r.stderr.strip()[:200]}\n"

def read_files(dirpath, files):
    out = []
    for f in sorted(files):
        p = os.path.join(dirpath, f)
        try: out.append((p, open(p, encoding="utf-8", errors="replace").read()))
        except FileNotFoundError: pass
    return out

def serialise(blocks):
    """blocks: list of (label, text). Deterministic; W last by construction of the caller."""
    parts = []
    for label, text in blocks:
        parts.append(f"// ===== {label} =====\n{text.rstrip()}\n")
    return "\n".join(parts)

def identifiers_added(gold_patch):
    ids = set()
    for line in gold_patch.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            ids |= set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", line))
    # drop Go keywords and very common tokens
    kw = {"func","return","package","import","var","const","type","struct","interface","map","chan","range","for","if","else","nil","true","false","string","int","bool","error","err","opts","len","append"}
    return sorted(i for i in ids if i not in kw)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8"))
    repo = resolve_repo(inst["repo_path"])
    head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()
    assert head.startswith(inst["base_commit"][:12]), f"worktree at {head}, expected base {inst['base_commit']}"
    pk, mod = load_packages(repo)
    deps, tdeps, fwd = build_graph(pk, mod)
    W = inst["write_set"]  # import paths
    rel = lambda p: os.path.relpath(p, repo).replace("\\", "/")
    def pkg_src(p):  # (label, text) for non-test files of package p
        o = pk[p]; return [(rel(path), txt) for path, txt in read_files(o["Dir"], o.get("GoFiles", []))]
    def pkg_tests(p):
        o = pk[p]; return [(rel(path), txt) for path, txt in read_files(o["Dir"], o.get("TestGoFiles", []) + o.get("XTestGoFiles", []))]

    direct = sorted({d for w in W for d in pk[w].get("Imports", []) if d in pk and d not in W})
    B = sorted(set().union(*[deps[w] for w in W]) - set(W))
    F = sorted(set().union(*[fwd[w] for w in W]) - set(W))
    w_blocks = [b for w in W for b in pkg_src(w)]

    contexts = {
        "W": w_blocks,
        "W+iface(deps)": [(f"{d} (exported API)", go_doc_all(repo, d)) for d in direct] + w_blocks,
        "W+bodies(deps)": [b for d in direct for b in pkg_src(d)] + w_blocks,
        "transitive": [b for p in B for b in pkg_src(p)] + [b for p in F for b in pkg_src(p) + pkg_tests(p)]
                      + [b for w in W for b in pkg_tests(w)] + w_blocks,
    }
    ids = identifiers_added(inst["gold_patch"])
    os.makedirs(a.out, exist_ok=True)
    meta = {"write_set": W, "direct_deps": direct, "backward_slice": B, "forward_slice": F, "gold_identifiers": ids, "contexts": {}}
    for name, blocks in contexts.items():
        text = serialise(blocks)
        fn = os.path.join(a.out, name.replace("+", "_").replace("(", "").replace(")", "") + ".txt")
        open(fn, "w", encoding="utf-8", newline="\n").write(text)
        missing = [i for i in ids if i not in text]
        meta["contexts"][name] = {"file": os.path.basename(fn), "n_blocks": len(blocks), "chars": len(text),
                                  "expressible": not missing, "missing_identifiers": missing}
        print(f"{name:16s} blocks={len(blocks):4d} chars={len(text):9,d} expressible={not missing} missing={missing}")
    json.dump(meta, open(os.path.join(a.out, "contexts.json"), "w", encoding="utf-8"), indent=1)
    print("direct deps:", len(direct), "| B:", len(B), "| F:", len(F))

if __name__ == "__main__":
    main()
