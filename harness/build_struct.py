"""Build declaration-level arms for one instance (preregistration amendment 2026-10-13, H6 and H7).

Adds to an existing contexts directory: Wd (declaration slice of W reachable from the fail-to-pass tests and the task text),
A1r (full W plus the dependency declarations that W references, rendered without bodies), Wdr (the slice plus the dependency
declarations the slice references), and with --pad: Wpad (W preceded by inert same-module padding matched to A1's token count).
Requires tools/declgraph/declgraph.exe. Writes <arm>.txt files and merges the arms into contexts.json.
"""
import argparse, json, os, re, sys, pathlib, hashlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_mutation import run, load_packages, build_graph
from build_contexts import read_files, serialise
from pilot_contexts import make_client, count
from pilot_run import reset
from run_instance import resolve_repo
from pilot_ablation import CODESPAN, SELECTOR, WORD

IDENT = re.compile(r"\b[A-Za-z_]\w*\b")
HERE = pathlib.Path(__file__).resolve().parent

def key(d): return d["pkg"] + "." + (d["recv"] + "." if d.get("recv") else "") + d["name"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--contexts", required=True)
    ap.add_argument("--declgraph", default=str(HERE / "tools" / "declgraph" / "declgraph.exe")); ap.add_argument("--model", default="claude-haiku-5-5")
    ap.add_argument("--pad", action="store_true", help="also build Wpad matched to A1's prompt tokens")
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8")); repo = resolve_repo(inst["repo_path"])
    meta = json.load(open(os.path.join(a.contexts, "contexts.json"), encoding="utf-8"))
    reset(repo, inst)
    pk, mod = load_packages(repo); W = inst["write_set"]
    direct = sorted({d for w in W for d in pk[w].get("Imports", []) if d in pk and d not in W})
    r = run([a.declgraph, "-dir", repo] + W + direct, repo)
    if r.returncode != 0: sys.exit("declgraph failed: " + r.stderr[:400])
    decls = json.loads(r.stdout)["decls"]; byk = {}
    for d in decls: byk.setdefault(key(d), d)
    wdecls = [d for d in decls if d["pkg"] in W]
    rel = lambda p: os.path.relpath(p, repo).replace("\\", "/")
    # roots: identifiers used by the fail-to-pass tests and by code spans or selectors in the task text
    root_ids = set()
    for tf, content in inst["test_files"].items():
        if content: root_ids |= set(IDENT.findall(content))
    task = inst["task_text"]; root_ids |= set(WORD.findall(" ".join(CODESPAN.findall(task)))); root_ids |= {m[1] for m in SELECTOR.findall(task)}
    roots = {key(d) for d in wdecls if d["name"] in root_ids}
    sel = set(roots); stack = list(roots)
    while stack:
        d = byk.get(stack.pop())
        if not d: continue
        for ref in d["refs"]:
            if ref in byk and byk[ref]["pkg"] in W and ref not in sel: sel.add(ref); stack.append(ref)
    for k in list(sel):
        d = byk[k]
        if d.get("recv"):
            rk = d["pkg"] + "." + d["recv"]
            if rk in byk: sel.add(rk)
    def dep_refs(keys):
        s = set()
        for k in keys:
            for ref in byk[k]["refs"]:
                if ref in byk and byk[ref]["pkg"] in direct: s.add(ref)
        for k in list(s):
            d = byk[k]
            if d.get("recv"):
                rk = d["pkg"] + "." + d["recv"]
                if rk in byk: s.add(rk)
        return s
    refs_all = dep_refs([key(d) for d in wdecls]); refs_sel = dep_refs(sel)

    def w_blocks(selected=None):
        blocks = []
        for w in W:
            o = pk[w]
            for path, text in read_files(o["Dir"], o.get("GoFiles", [])):
                rp = rel(path)
                if selected is None: blocks.append((rp, text)); continue
                lines = text.split("\n"); units = {}
                for d in decls:
                    if d["pkg"] == w and d["file"] == rp: units.setdefault((d["doc_start"], d["end"]), []).append(d)
                if not units: blocks.append((rp, text)); continue
                first = min(u[0] for u in units); parts = ["\n".join(lines[:first - 1]).rstrip()]; omitted = []
                def flush():
                    nonlocal omitted
                    if omitted:
                        names = sorted(set(omitted)); parts.append(f"// ... {len(names)} declaration(s) omitted: " + ", ".join(names[:10]) + (" ..." if len(names) > 10 else ""))
                        omitted = []
                for (ds, en), group in sorted(units.items()):
                    if any(key(d) in selected for d in group): flush(); parts.append("\n".join(lines[ds - 1:en]))
                    else: omitted += [d["name"] for d in group]
                flush(); blocks.append((rp, "\n\n".join(p for p in parts if p)))
        return blocks
    def dep_blocks(refs):
        blocks = []
        for dep in direct:
            sigs = []
            for k in sorted(refs):
                d = byk[k]
                if d["pkg"] == dep and d["sig"] and d["sig"] not in sigs: sigs.append(d["sig"])
            if sigs: blocks.append((f"{dep} (referenced declarations)", f"package {pk[dep]['Name']}\n\n" + "\n\n".join(sigs)))
        return blocks
    full_w = w_blocks(None); slice_w = w_blocks(sel)
    arms = {"Wd": serialise(slice_w), "A1r": serialise(dep_blocks(refs_all) + full_w), "Wdr": serialise(dep_blocks(refs_sel) + slice_w)}
    client = make_client(inst)
    if a.pad:
        deps_t, _, fwd = build_graph(pk, mod)
        B = set().union(*[deps_t[w] for w in W]) - set(W); F = set().union(*[fwd[w] for w in W]) - set(W)
        wdirs = {os.path.dirname(pk[w]["Dir"]) for w in W}
        pool = [p for p in pk if p not in W and p not in B and p not in F and os.path.dirname(pk[p]["Dir"]) not in wdirs and pk[p].get("GoFiles")]
        pool.sort(key=lambda p: hashlib.sha1((inst["instance_id"] + p).encode()).hexdigest())
        a1m = meta["arms"]["A1"]; target = a1m.get("n_tokens_prompt") or meta["arms"][a1m["same_as"]]["n_tokens_prompt"]
        w_text = serialise(full_w); base = count(client, a.model, w_text, task); pad = ""; pads = []; i = 0; full = base
        while full < target and i < len(pool):
            p = pool[i]; i += 1; pad += serialise([(rel(x), t) for x, t in read_files(pk[p]["Dir"], pk[p]["GoFiles"])]) + "\n"; pads.append(p)
            full = count(client, a.model, pad + w_text, task)
        if full > target and pad:
            cpt = len(pad) / max(1, full - base); keep = max(0, len(pad) - int((full - target) * cpt)); pad = pad[:pad.rfind("\n", 0, keep) + 1]
        arms["Wpad"] = pad + w_text; meta.setdefault("pad_meta", {})["Wpad"] = {"pad_pkgs": pads, "target_tokens": target}
    gold_ids = set(meta.get("gold_identifiers", [])); existing = {}
    for name, am in meta["arms"].items():
        if "file" in am and os.path.exists(os.path.join(a.contexts, am["file"])):
            existing[open(os.path.join(a.contexts, am["file"]), encoding="utf-8").read()] = name
    for name, text in arms.items():
        rec = {"chars": len(text)}
        if text in existing: rec["same_as"] = existing[text]; meta["arms"][name] = rec; print(f"{name:5s} same as {existing[text]}"); continue
        existing[text] = name
        open(os.path.join(a.contexts, name + ".txt"), "w", encoding="utf-8", newline="\n").write(text)
        missing = [i for i in sorted(gold_ids) if i not in text]
        rec.update({"file": name + ".txt", "n_tokens_prompt": count(client, a.model, text, task), "expressible": not missing, "missing_identifiers": missing})
        meta["arms"][name] = rec; print(f"{name:5s} tokens={rec['n_tokens_prompt']:7d}", flush=True)
    meta["struct_meta"] = {"rule": "2026-10-13 amendment: declaration slice from fail-to-pass tests and task code spans; referenced dependency declarations without bodies",
                           "n_w_decls": len(wdecls), "n_selected": len(sel), "n_roots": len(roots), "n_dep_refs_all": len(refs_all), "n_dep_refs_sel": len(refs_sel),
                           "selected": sorted(sel), "dep_refs_sel": sorted(refs_sel)}
    json.dump(meta, open(os.path.join(a.contexts, "contexts.json"), "w", encoding="utf-8"), indent=1)
    print(f"w_decls={len(wdecls)} selected={len(sel)} roots={len(roots)} dep_refs_all={len(refs_all)} dep_refs_sel={len(refs_sel)}")

if __name__ == "__main__":
    main()
