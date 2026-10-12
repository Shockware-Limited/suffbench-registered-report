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

## Published 2026-10-11

Zenodo DOI 10.5281/zenodo.23307204 (concept 10.5281/zenodo.23307203), deposition 23307204. Public release: Shockware-Limited/suffbench tag v0.1.1-pilot (commit 11159c9). Note: zenodo_publish.py still returns 415 on the bucket upload; files were uploaded with curl --upload-file and metadata PUT separately, as for the note.

## Stage 1 protocol published 2026-10-11

Zenodo DOI 10.5281/zenodo.23307547 (concept 10.5281/zenodo.23307546), deposition 23307547: registered-report-stage1.pdf + preregistration.md. Published as a preregistration since the MSR 2027 RR track had closed; to be submitted to a Registered Reports venue. No confirmatory call may be made before models and cutoffs are fixed in preregistration.md with a dated note.
