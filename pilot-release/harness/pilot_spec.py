"""Write behaviour-only task specs for mined instances lacking a linked issue (HANDOFF §5 M5).

Uses claude-haiku-5-5 on the author's key. Post-check: none of gold_new_identifiers, no file paths, no Go identifiers
with a dot-path. One retry listing offending tokens; else flagged for the author.
Usage: python pilot_spec.py instances/*.json
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from pilot_contexts import make_client

PROMPT = """Rewrite the following pull-request description as a short task specification for an engineer who will fix the behaviour.
Rules: describe observable behaviour only (what the command currently does, what it should do). Do not mention any
identifier, function, type, field, flag-variable, file name, or package path from the code. Do not describe how to
implement the fix. Do not mention tests. 60-180 words. Plain text, no headings.{extra}

PR title: {title}

PR body:
{body}

Commit message:
{msg}

Test diff (for your understanding of the expected behaviour; do not quote it):
{tests}
"""

def offending(text, inst):
    bad = [i for i in inst.get("gold_new_identifiers", []) if re.search(r"\b" + re.escape(i) + r"\b", text)]
    bad += re.findall(r"\b[\w./-]+\.go\b", text)
    bad += [m for m in re.findall(r"\b[a-z]+\.[A-Z]\w+\b", text)]
    return sorted(set(bad))

def main():
    for p in sys.argv[1:]:
        inst = json.load(open(p, encoding="utf-8"))
        if inst.get("task_text"): continue
        client = make_client(inst); extra = ""
        for attempt in range(2):
            r = client.messages.create(model="claude-haiku-5-5", max_tokens=1200, messages=[{"role": "user", "content": PROMPT.format(
                extra=extra, title=inst.get("pr_title") or "", body=(inst.get("pr_body") or "")[:6000], msg=inst.get("commit_message", "")[:3000], tests=inst.get("test_patch", "")[:12000])}])
            text = "".join(b.text for b in r.content if b.type == "text").strip()
            bad = offending(text, inst)
            if not bad: break
            extra = "\nThe previous draft leaked these tokens, which must not appear: " + ", ".join(bad)
        inst["task_text"] = text; inst["task_text_source"] = "rewritten_spec"
        inst["validity"]["task_text_review"] = "pending_author" if not bad else f"FLAG leaked tokens after retry: {bad}"
        json.dump(inst, open(p, "w", encoding="utf-8"), indent=1)
        print(os.path.basename(p), "ok" if not bad else f"FLAG {bad}", flush=True)

if __name__ == "__main__":
    main()
