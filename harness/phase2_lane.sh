# Phase 2 lane, later stages: run one model over the selected instances of one worktree, with a spend cap.
# usage: bash phase2_lane.sh <worktree> <model> <k> <cap-usd-for-model> <max-prompt-tokens> <arms...>
#   arms "LOO" expands to A1 plus every A1-NN arm of the instance.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
WT=$1; MODEL=$2; K=$3; CAP=$4; MAXTOK=$5; shift 5; ARMS="$*"
log() { echo "## [$WT $MODEL] $* $(date +%H:%M)"; }
mkdir -p results-p2
grep -P "\t$WT$" p2_selected.tsv | while IFS=$'\t' read -r id ctx wt; do
  if ! $PY spend.py results-p2 --model $MODEL --cap $CAP --quiet; then log "cap reached before $id"; break; fi
  arms="$ARMS"
  if [ "$ARMS" = "LOO" ]; then arms="A1 $($PY -c "import json; m=json.load(open('$ctx/contexts.json')); print(' '.join(a for a in m['arms'] if a.startswith('A1-') and 'file' in m['arms'][a]))")"; fi
  log "run $id k=$K arms=$arms"
  $PY pilot_run.py --instance instances/$id.json --contexts $ctx --model $MODEL --k $K --arms $arms --max-prompt-tokens $MAXTOK --out results-p2/$id-$MODEL.jsonl 2>&1 | grep -v "cached=True" | tail -2
done
log "LANE_DONE"
