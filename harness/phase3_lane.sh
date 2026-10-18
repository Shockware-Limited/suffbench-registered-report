# Phase 3 lane: run one model over the rows of a selection file that belong to one worktree, with a spend cap.
# usage: SEL=<rows: id, contexts dir, worktree, instance file> OUT=<results dir> bash phase3_lane.sh <worktree> <model> <k> <cap-usd> <max-prompt-tokens> <arms...>
#   arms "LOO" expands to A1 plus every A1-NN arm of the instance.
# Each lane uses its own Go build cache, deleted after every instance: distinct patches relink every dependent test
# binary, so a shared persistent cache grows without bound.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
WT=$1; MODEL=$2; K=$3; CAP=$4; MAXTOK=$5; shift 5; ARMS="$*"
SEL=${SEL:-p3_selected_existing.tsv}; OUT=${OUT:-results-p3}; mkdir -p $OUT
export GOCACHE="$LOCALAPPDATA/go-build-lane-$WT"
log() { echo "## [$WT $MODEL] $* $(date +%H:%M)"; }
awk -F'\t' -v w="$WT" '$3==w' "$SEL" | while IFS=$'\t' read -r id ctx wt inst; do
  INST=${inst:-instances/$id.json}
  if ! $PY spend.py $OUT --model $MODEL --cap $CAP --quiet; then log "cap reached before $id"; break; fi
  while [ "$(df -k /c | awk 'NR==2{print int($4/1048576)}')" -lt 8 ]; do log "under 8G free; pausing"; sleep 300; done
  arms="$ARMS"
  if [ "$ARMS" = "LOO" ]; then arms="A1 $($PY -c "import json; m=json.load(open('$ctx/contexts.json')); print(' '.join(a for a in m['arms'] if a.startswith('A1-') and 'file' in m['arms'][a]))")"; fi
  log "run $id k=$K arms=$arms"
  $PY pilot_run.py --instance $INST --contexts $ctx --model $MODEL --k $K --arms $arms --max-prompt-tokens $MAXTOK --out $OUT/$id-$MODEL.jsonl 2>&1 | grep -v "cached=True" | tail -2
  rm -rf "$GOCACHE"; log "cache cleared; $(df -k /c | awk 'NR==2{print int($4/1048576)}')G free"
done
log "LANE_DONE"
