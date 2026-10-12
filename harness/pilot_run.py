"""Pilot runner: one instance × arms × k samples on one model; verdict cache; W∪F frame check; window cap.

Usage: python pilot_run.py --instance instances/<id>.json --contexts contexts-<id>/ --model claude-haiku-5-5 \
         --k 10 --arms A0 W A1 A1b A1F P32 P64 P128 P200 --out results/<id>-haiku55.jsonl
Sampling parameters are not settable on these models; every sample is an independent default-sampling call.
"""
import argparse, json, os, sys, time, hashlib, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "context-sufficiency-note" / "experiments"))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from run_mutation import run, GO
from run_instance import parse_blocks, apply_blocks, resolve_repo
from pilot_contexts import make_client, messages_for, SYSTEM
import anthropic

def reset(repo, inst):
    run(["git", "checkout", "-q", "-f", inst["base_commit"]], repo); run(["git", "clean", "-fdq"], repo)
    for tf, content in inst["test_files"].items():
        full = os.path.join(repo, tf)
        if content is None:
            if os.path.exists(full): os.remove(full)
        else:
            os.makedirs(os.path.dirname(full), exist_ok=True); open(full, "w", encoding="utf-8", newline="\n").write(content)

def test_status(stdout):
    tests, pkgs = {}, {}
    for l in stdout.splitlines():
        try: e = json.loads(l)
        except Exception: continue
        if e.get("Test") and e.get("Action") in ("pass", "fail") and "/" not in e["Test"]: tests[f"{e['Package']}:{e['Test']}"] = e["Action"]
        if e.get("Test") is None and e.get("Action") in ("pass", "fail", "skip"): pkgs[e["Package"]] = e["Action"]
    return tests, pkgs

def verify(repo, inst, scope):
    rec = {}
    b = run([GO, "build", "./..."], repo, timeout=900); rec["builds"] = b.returncode == 0
    if not rec["builds"]: rec["delta_pass"] = False; rec["build_error"] = b.stderr[:1500]; return rec
    bypkg = {}
    for x in inst["fail_to_pass"]: p, t = x.split(":"); bypkg.setdefault(p, []).append(t)
    ok = True; out = ""
    for p, ts in bypkg.items():
        t = run([GO, "test", "-count=1", "-json", "-run", "^(" + "|".join(ts) + ")$", p], repo, timeout=900)
        st, _ = test_status(t.stdout)
        for tn in ts:
            if st.get(f"{p}:{tn}") != "pass": ok = False
        if not ok: out += "".join(json.loads(l).get("Output", "") for l in t.stdout.splitlines() if l.startswith("{") and '"Output"' in l)[-2500:]
    rec["delta_pass"] = ok
    if not ok: rec["test_output"] = out[-2500:]; return rec
    tt = run([GO, "test", "-count=1", "-json", *scope], repo, timeout=2400)
    _, pk = test_status(tt.stdout)
    fails = sorted(p for p, v in pk.items() if v == "fail")
    rec["frame_fail_pkgs"] = fails; rec["frame_pass"] = not fails; rec["frame_scope"] = "W∪F"
    return rec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instance", required=True); ap.add_argument("--contexts", required=True); ap.add_argument("--model", required=True)
    ap.add_argument("--k", type=int, default=10); ap.add_argument("--arms", nargs="*"); ap.add_argument("--out", required=True)
    ap.add_argument("--max-prompt-tokens", type=int, default=900000); ap.add_argument("--max-tokens", type=int, default=16000)
    a = ap.parse_args()
    inst = json.load(open(a.instance, encoding="utf-8")); repo = resolve_repo(inst["repo_path"])
    meta = json.load(open(os.path.join(a.contexts, "contexts.json"), encoding="utf-8"))
    scope = [p for p in inst["write_set"] + meta["forward_slice"] if p not in inst.get("baseline_fail_pkgs", [])]
    client = make_client(inst); out = open(a.out, "a", encoding="utf-8")
    done = set()
    if os.path.exists(a.out):
        for l in open(a.out, encoding="utf-8"):
            try: r = json.loads(l); done.add((r["arm"], r["sample"]))
            except Exception: pass
    verdicts = {}
    for arm in (a.arms or list(meta["arms"].keys())):
        am = meta["arms"].get(arm)
        if not am or "file" not in am: print(f"[{arm}] skipped (not built)", flush=True); continue
        ctx = open(os.path.join(a.contexts, am["file"]), encoding="utf-8").read() if arm != "A0" else ""
        msgs = messages_for(ctx, inst["task_text"])
        try: n_tok = client.messages.count_tokens(model=a.model, system=SYSTEM, messages=msgs).input_tokens
        except anthropic.APIStatusError as e: n_tok = None; print(f"[{arm}] count_tokens failed: {e.status_code}", flush=True)
        for s in range(a.k):
            if (arm, s) in done: continue
            rec = {"instance_id": inst["instance_id"], "model": a.model, "arm": arm, "sample": s, "n_tokens_prompt": n_tok, "chars": len(ctx)}
            if n_tok is not None and n_tok > a.max_prompt_tokens:
                rec.update({"api_error": "exceeds_window", "applied": False, "builds": False, "delta_pass": False}); out.write(json.dumps(rec) + "\n"); out.flush()
                print(f"[{arm} s{s}] exceeds window ({n_tok})", flush=True); continue
            reset(repo, inst); messages = list(msgs); t0 = time.time(); usage = []; repaired = False; text = ""; ok = False; err = ""
            try:
                for turn in range(2):
                    with client.messages.stream(model=a.model, max_tokens=a.max_tokens, system=SYSTEM, messages=messages) as stream:
                        resp = stream.get_final_message()
                    usage.append({"in": resp.usage.input_tokens, "out": resp.usage.output_tokens,
                                  "cache_read": getattr(resp.usage, "cache_read_input_tokens", 0) or 0,
                                  "cache_write": getattr(resp.usage, "cache_creation_input_tokens", 0) or 0, "stop": resp.stop_reason})
                    if resp.stop_reason == "refusal": rec["refusal"] = True; err = "refusal"; break
                    text = "".join(b.text for b in resp.content if b.type == "text")
                    blocks = parse_blocks(text)
                    ok, err = apply_blocks(repo, blocks) if blocks else (False, "no SEARCH/REPLACE blocks found")
                    if ok or turn == 1: break
                    repaired = True
                    messages = messages + [{"role": "assistant", "content": text},
                                           {"role": "user", "content": f"The edit could not be applied: {err}\nRe-emit corrected SEARCH/REPLACE blocks only."}]
            except anthropic.APIStatusError as e:
                rec["api_error"] = f"{e.status_code}: {e.message}"; ok, err = False, "api error"
            rec.update({"applied": ok, "apply_error": "" if ok else err, "repaired": repaired, "usage": usage, "latency_s": round(time.time() - t0, 1),
                        "n_blocks": len(parse_blocks(text)), "response": text[:4000]})
            if ok:
                diff = run(["git", "diff", "--", "*.go", ":!*_test.go"], repo).stdout
                sha = hashlib.sha1(diff.encode("utf-8", "replace")).hexdigest(); rec["patch_sha"] = sha; rec["diff_stat"] = run(["git", "diff", "--stat", "--", "*.go", ":!*_test.go"], repo).stdout.strip()[-300:]
                if sha in verdicts: rec.update(verdicts[sha]); rec["verdict_cached"] = True
                else: v = verify(repo, inst, scope); verdicts[sha] = v; rec.update(v); rec["verdict_cached"] = False
            else: rec["builds"] = False; rec["delta_pass"] = False
            out.write(json.dumps(rec) + "\n"); out.flush()
            u = usage[0] if usage else {}
            print(f"[{arm} s{s}] tok={n_tok} applied={ok} builds={rec.get('builds')} delta={rec.get('delta_pass')} frame={rec.get('frame_pass','-')} "
                  f"cached={rec.get('verdict_cached','-')} in={u.get('in')} cr={u.get('cache_read')} out={u.get('out')} {rec['latency_s']}s", flush=True)
    reset(repo, inst)

if __name__ == "__main__":
    main()
