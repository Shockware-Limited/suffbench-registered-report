# Publish the pilot (author-owned steps; run after your cold read of pilot-paper/main.pdf)

Shell: Git Bash. All paths relative to the chat workspace root.

1. Public data + code release (SuffBench v0.1.1-pilot):
   cp -r suffbench-registered-report/pilot-release suffbench/pilot
   cd suffbench && git add pilot && git commit -m "Pilot v0.1.1: 24-instance pilot measurement (paper, instances, harness, verdicts)" && git tag v0.1.1-pilot && git push && git push --tags && cd ..

2. Zenodo deposit (new record, linked to the note's concept DOI):
   /c/Python314/python context-sufficiency-note/release/zenodo_publish.py --host zenodo.org \
     --token-file "C:/Users/visci/.config/context-sufficiency-note/zenodo-prod.token" \
     --pdf suffbench-registered-report/pilot-paper/main.pdf \
     --metadata suffbench-registered-report/pilot-paper/zenodo-metadata.json \
     --extra suffbench-registered-report/pilot-paper/suffbench-pilot-v0.1.1.zip --publish
   (Omit --publish first for a dry run that leaves a draft you can inspect in the Zenodo UI.)

3. After the DOI resolves: add it to suffbench/README.md and suffbench/CITATION.cff, and to the note repo README under "Follow-on work"; commit and push both.

Checks before step 1: every rewritten task text in pilot-release/instances/*.json with task_text_source = rewritten_spec (11 files) reads as behaviour-only; the veto in instances/vetoes.json is one you agree with; numbers in main.pdf match results/PILOT-REPORT.md.
