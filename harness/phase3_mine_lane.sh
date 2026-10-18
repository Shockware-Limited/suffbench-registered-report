# Phase 3 mining lane (amendment 2026-10-13): relaxed M1 limits, then specs, arms (reference and declaration-level), and the
# k=20 W/A1 screen into results-p3. usage: bash phase3_mine_lane.sh <lane> <repo owner/name> <clone> <mine-worktree> <run-worktree>
# Uses its own Go build cache, deleted after mining and after each screened instance.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
LANE=$1; REPO=$2; CLONE=$3; MWT=$4; RWT=$5; SINCE=${SINCE:-2026-06-01}
export GOCACHE="$LOCALAPPDATA/go-build-lane-$MWT"
log() { echo "## [$LANE] $* $(date +%H:%M)"; }
PREFIX=$(echo "$REPO" | sed 's#/#__#')
[ -f "instances/_template_$LANE.json" ] || $PY make_template.py --repo "$REPO" --wt "$MWT" --baseline "$CORPUS_ROOT/$CLONE-baseline.json" --out "instances/_template_$LANE.json"
ls instances/$PREFIX-*.json 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.json$//' | sort > p3_before_$LANE.txt
log "mine relaxed (pkgs<=4, churn<=300) $REPO"
timeout 18000 $PY pilot_mine.py --clone "$CORPUS_ROOT/$CLONE" --wt "$CORPUS_ROOT/$MWT" --since "$SINCE" --target 40 --max-commits 400 --max-pkgs 4 --max-churn 300 \
  --out instances --template "instances/_template_$LANE.json" 2>&1 | grep -E "valid|examined=" | tail -40
rm -rf "$GOCACHE"; log "mine done; cache cleared"
ls instances/$PREFIX-*.json 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.json$//' | sort > p3_after_$LANE.txt
NEW=$(comm -13 p3_before_$LANE.txt p3_after_$LANE.txt)
[ -n "$NEW" ] || { log "no new instances"; echo "## MINE_LANE_DONE $LANE $(date +%H:%M)"; exit 0; }
log "specs"; $PY pilot_spec.py $(for id in $NEW; do echo instances/$id.json; done) 2>&1 | tail -3
mkdir -p abl-instances-h6 results-p3; : > p3_manifest_new_$LANE.tsv
for id in $NEW; do
  $PY -c "import json; d=json.load(open('instances/$id.json',encoding='utf-8')); d['repo_path']='$RWT'; json.dump(d,open('abl-instances-h6/$id.json','w',encoding='utf-8'),indent=1)"
  log "build $id"; $PY pilot_ablation.py --instance abl-instances-h6/$id.json --out abl-$id 2>&1 | tail -1
  [ -f abl-$id/contexts.json ] || continue
  $PY build_struct.py --instance abl-instances-h6/$id.json --contexts abl-$id --pad 2>&1 | tail -1
  printf '%s\t%s\t%s\t%s\n' "$id" "abl-$id" "$RWT" "abl-instances-h6/$id.json" >> p3_manifest_new_$LANE.tsv
  log "screen2 $id"; $PY pilot_run.py --instance abl-instances-h6/$id.json --contexts abl-$id --model claude-haiku-5-5 --k 20 --arms W A1 --out results-p3/$id-claude-haiku-5-5.jsonl 2>&1 | tail -1
  rm -rf "$GOCACHE"
done
echo "## MINE_LANE_DONE $LANE $(date +%H:%M)"
