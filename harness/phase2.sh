# Phase 2 orchestrator (preregistration amendment 2026-10-12). Run detached: nohup setsid bash phase2.sh > p2.log 2>&1 &
# Stage 0 prepares and screens every repository in parallel lanes; stage 1 selects instances; stages 2-6 run the models
# over the selected instances with per-model spend caps (USD at list prices, cumulative over results-p2/).
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
log() { echo "#### $* $(date '+%m-%d %H:%M')"; }

log "STAGE0 start"
bash phase2_lane0.sh cli cli/cli cli wt > p2_lane0_cli.log 2>&1 &
bash phase2_lane0.sh caddy caddyserver/caddy caddy caddy-wt > p2_lane0_caddy.log 2>&1 &
bash phase2_lane0.sh zap uber-go/zap zap zap-wt > p2_lane0_zap_full.log 2>&1 &
bash phase2_lane0.sh hugo gohugoio/hugo hugo hugo-wt > p2_lane0_hugo.log 2>&1 &
bash phase2_lane0.sh docker docker/cli docker-cli docker-wt > p2_lane0_docker.log 2>&1 &
wait
log "STAGE0 done"

cat p2_manifest_*.tsv > p2_manifest.tsv
$PY screen.py --manifest p2_manifest.tsv --out p2_selected.tsv
N=$(grep -c . p2_selected.tsv)
log "STAGE1 selected $N instances"
[ "$N" -gt 0 ] || { log "nothing selected; stopping"; exit 0; }
read K_MAIN K_H45 K_OPUS K_SON <<< "$($PY -c "n=$N; print(min(100,max(30,8000//(4*n))), min(20,max(5,1500//(4*n))), min(5,max(3,450//(3*n))), min(10,max(3,1200//(4*n))))")"
log "k: haiku55=$K_MAIN haiku45=$K_H45 opus55=$K_OPUS sonnet55=$K_SON"
WTS=$(cut -f3 p2_selected.tsv | sort -u)

stage() { # name model k cap maxtok arms...
  local name=$1 model=$2 k=$3 cap=$4 maxtok=$5; shift 5
  log "$name start (model=$model k=$k cap=\$$cap)"
  for wt in $WTS; do bash phase2_lane.sh $wt $model $k $cap $maxtok "$@" > p2_${name}_$wt.log 2>&1 & done
  wait
  log "$name done: $($PY spend.py results-p2 results-p2screen --quiet; $PY spend.py results-p2 results-p2screen | tail -1)"
}
stage S2_haiku55  claude-haiku-5-5          $K_MAIN 45 900000 W A1 A1g A1t
stage S3_haiku45  claude-haiku-4-5-20251001 $K_H45  70 190000 W A1 A1g A1t
stage S4_opus55   claude-opus-5-5           $K_OPUS 60 900000 A0 W A1t
stage S5_sonnet55 claude-sonnet-5-5         $K_SON  60 900000 W A1 A1g A1t
stage S6_loo      claude-haiku-5-5          100     90 900000 LOO
log "PHASE2_DONE"
$PY spend.py results-p2 results-p2screen
