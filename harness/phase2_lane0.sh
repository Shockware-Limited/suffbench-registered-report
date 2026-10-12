# Phase 2 lane, stage 0: prepare one repository and screen its instances.
# usage: bash phase2_lane0.sh <lane> <repo owner/name> <clone dir name> <worktree name> [since]
# Produces: $CORPUS_ROOT/<clone>-baseline.json (if missing), instances/_template_<lane>.json, mined instances,
# task specs for instances without an issue, arms in abl-<id>/, W screen at k=5 in results-p2screen/, and manifest rows in p2_manifest_<lane>.tsv.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
LANE=$1; REPO=$2; CLONE=$3; WT=$4; SINCE=${5:-2026-06-01}
TARGET=${TARGET:-40}; MAXC=${MAXC:-300}
log() { echo "## [$LANE] $* $(date +%H:%M)"; }

if [ "$LANE" != "cli" ]; then
  until [ -f "$CORPUS_ROOT/$CLONE/go.mod" ] && [ ! -f "$CORPUS_ROOT/$CLONE/.git/index.lock" ] && [ -z "$(git -C "$CORPUS_ROOT/$CLONE" status --porcelain 2>/dev/null | head -1)" ]; do log "waiting for clone $CLONE"; sleep 60; done
  [ -d "$CORPUS_ROOT/$WT" ] || git -C "$CORPUS_ROOT/$CLONE" worktree add -q --detach "../$WT" HEAD
  if [ ! -s "$CORPUS_ROOT/$CLONE-baseline.json" ]; then
    log "baseline $CLONE"; (cd "$CORPUS_ROOT/$CLONE" && timeout 3600 go test -count=1 -json ./... > "$CORPUS_ROOT/$CLONE-baseline.json" 2> "$CORPUS_ROOT/$CLONE-baseline.err"); log "baseline done"
  fi
  $PY make_template.py --repo "$REPO" --wt "$WT" --baseline "$CORPUS_ROOT/$CLONE-baseline.json" --out "instances/_template_$LANE.json"
  log "mine $REPO since $SINCE"
  timeout 14400 $PY pilot_mine.py --clone "$CORPUS_ROOT/$CLONE" --wt "$CORPUS_ROOT/$WT" --since "$SINCE" --target $TARGET --max-commits $MAXC --out instances --template "instances/_template_$LANE.json" 2>&1 | grep -E "valid|examined=" | tail -50
  log "mine done"
  PREFIX=$(echo "$REPO" | sed 's#/#__#')
  IDS=$(ls instances/$PREFIX-*.json 2>/dev/null | xargs -n1 basename | sed 's/\.json$//')
  CTX=abl-
else
  IDS=$(tr -d '\r' < abl_ids.txt); CTX=ablr-   # the 23 pilot instances: rebuild arms under the amended task rule
fi
[ -n "$IDS" ] || { log "no instances"; exit 0; }
log "specs"; $PY pilot_spec.py $(for id in $IDS; do echo instances/$id.json; done) 2>&1 | tail -5
: > p2_manifest_$LANE.tsv
for id in $IDS; do
  log "build $id"
  $PY pilot_ablation.py --instance instances/$id.json --out $CTX$id 2>&1 | tail -1
  [ -f $CTX$id/contexts.json ] && printf '%s\t%s\t%s\n' "$id" "$CTX$id" "$WT" >> p2_manifest_$LANE.tsv
done
mkdir -p results-p2screen
while IFS=$'\t' read -r id ctx wt; do
  log "screen $id"
  $PY pilot_run.py --instance instances/$id.json --contexts $ctx --model claude-haiku-5-5 --k 5 --arms W --out results-p2screen/$id-claude-haiku-5-5.jsonl 2>&1 | tail -1
done < p2_manifest_$LANE.tsv
log "LANE0_DONE"
