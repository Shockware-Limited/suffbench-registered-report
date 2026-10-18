# Phase 3 orchestrator (preregistration amendment 2026-10-13): declaration-level arms (H6), matched padding (H7), two-stage
# screen, relaxed mining. Run detached: nohup setsid bash phase3.sh > p3.log 2>&1 &
# Worktrees: the LOO lanes keep caddy-wt and wt. This phase runs cli on wt2, caddy on caddy-wt2, the others on their *-wt.
# Mining lanes mine and run their new instances on their own *-mine worktree, so no two lanes share a checkout.
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
. ./env.local.sh
PY=/c/Python314/python
log() { echo "#### $* $(date '+%m-%d %H:%M')"; }
guard() { free=$(df -k /c | awk 'NR==2{print int($4/1048576)}'); if [ "$free" -lt 25 ]; then log "free ${free}G: cleaning Go build cache"; go clean -cache; fi; }
until_done() { while [ -n "$(ls $1 2>/dev/null | xargs grep -L "$2" 2>/dev/null)" ]; do sleep 60; done; }
export OUT=results-p3; mkdir -p results-p3 abl-instances-h6

log "STAGE A: manifest for existing instances"
$PY - <<'EOF'
import json
wt = {"cli/cli": "wt2", "caddyserver/caddy": "caddy-wt2", "gohugoio/hugo": "hugo-wt", "restic/restic": "restic-wt", "golangci/golangci-lint": "golangci-wt"}
rows = []
for l in open("p2_manifest.tsv", encoding="utf-8"):
    if not l.strip(): continue
    iid, ctx, _ = l.rstrip("\n").split("\t"); d = json.load(open(f"instances/{iid}.json", encoding="utf-8")); w = wt[d["repo"]]; d["repo_path"] = w
    json.dump(d, open(f"abl-instances-h6/{iid}.json", "w", encoding="utf-8"), indent=1); rows.append(f"{iid}\t{ctx}\t{w}\tabl-instances-h6/{iid}.json\n")
open("p3_manifest_existing.tsv", "w", encoding="utf-8", newline="\n").write("".join(rows)); print(len(rows), "rows")
EOF

log "STAGE M: relaxed mining lanes (caddy, hugo, cli) in background"
bash phase3_mine_lane.sh caddy caddyserver/caddy caddy caddy-mine caddy-mine > p3_mine_caddy.log 2>&1 &
bash phase3_mine_lane.sh hugo gohugoio/hugo hugo hugo-mine hugo-mine > p3_mine_hugo.log 2>&1 &
bash phase3_mine_lane.sh cli cli/cli cli cli-mine cli-mine > p3_mine_cli.log 2>&1 &

log "STAGE B: screen2 (W, A1 at k=20, Haiku 5.5) on existing instances"
for w in $(cut -f3 p3_manifest_existing.tsv | sort -u); do SEL=p3_manifest_existing.tsv bash phase3_lane.sh $w claude-haiku-5-5 20 70 900000 W A1 > p3_screen2_$w.log 2>&1 & done
until_done "p3_screen2_*.log" LANE_DONE
$PY select_h6.py --manifest p3_manifest_existing.tsv --results results-p3 --out p3_selected_existing.tsv
log "STAGE B selected: $(grep -c . p3_selected_existing.tsv)"

log "STAGE C: build declaration-level arms and matched padding"
while IFS=$'\t' read -r id ctx wt inst; do echo "-- $id"; $PY build_struct.py --instance $inst --contexts $ctx --pad 2>&1 | tail -1; done < p3_selected_existing.tsv
guard
log "STAGE D: Haiku 5.5 k=50 on all arms"
for w in $(cut -f3 p3_selected_existing.tsv | sort -u); do SEL=p3_selected_existing.tsv bash phase3_lane.sh $w claude-haiku-5-5 50 70 900000 W A1 A1t Wd A1r Wdr Wpad > p3_D_$w.log 2>&1 & done
until_done "p3_D_*.log" LANE_DONE
log "STAGE D done: $($PY spend.py results-p3 | tail -1)"
guard
log "STAGE E: Sonnet 5.5 k=10"
for w in $(cut -f3 p3_selected_existing.tsv | sort -u); do SEL=p3_selected_existing.tsv bash phase3_lane.sh $w claude-sonnet-5-5 10 60 900000 W A1 Wd A1r Wdr Wpad > p3_E_$w.log 2>&1 & done
until_done "p3_E_*.log" LANE_DONE
log "STAGE E done: $($PY spend.py results-p3 | tail -1)"

log "STAGE F: waiting for the first mining wave"
until_done "p3_mine_caddy.log p3_mine_hugo.log p3_mine_cli.log" MINE_LANE_DONE
log "second mining wave (restic, golangci-lint)"
bash phase3_mine_lane.sh restic restic/restic restic restic-mine restic-mine > p3_mine_restic.log 2>&1 &
bash phase3_mine_lane.sh golangci golangci/golangci-lint golangci-lint golangci-mine golangci-mine > p3_mine_golangci.log 2>&1 &
until_done "p3_mine_restic.log p3_mine_golangci.log" MINE_LANE_DONE
cat p3_manifest_new_*.tsv > p3_manifest_new.tsv 2>/dev/null
if [ -s p3_manifest_new.tsv ]; then
  $PY select_h6.py --manifest p3_manifest_new.tsv --results results-p3 --out p3_selected_new.tsv
  log "STAGE F selected new: $(grep -c . p3_selected_new.tsv)"
  guard
  log "STAGE G: Haiku 5.5 k=50 on new instances"
  for w in $(cut -f3 p3_selected_new.tsv | sort -u); do SEL=p3_selected_new.tsv bash phase3_lane.sh $w claude-haiku-5-5 50 70 900000 W A1 A1t Wd A1r Wdr Wpad > p3_G_$w.log 2>&1 & done
  until_done "p3_G_*.log" LANE_DONE
  log "STAGE H: Sonnet 5.5 k=10 on new instances"
  for w in $(cut -f3 p3_selected_new.tsv | sort -u); do SEL=p3_selected_new.tsv bash phase3_lane.sh $w claude-sonnet-5-5 10 60 900000 W A1 Wd A1r Wdr Wpad > p3_H_$w.log 2>&1 & done
  until_done "p3_H_*.log" LANE_DONE
else
  log "no new instances mined"
fi
log "PHASE3_DONE"
$PY spend.py results-p3 results-p2 results-p2screen
