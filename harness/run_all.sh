export PYTHONIOENCODING=utf-8
[ -f "$(dirname "$0")/env.local.sh" ] && . "$(dirname "$0")/env.local.sh"
PY=/c/Python314/python
IDS=$(ls -d contexts-cli__cli-* | sed 's/contexts-//')
for id in $IDS; do
  [ "$(python -c "import json;print(json.load(open('instances/$id.json'))['repo_path'])" 2>/dev/null)" = "C:/Users/visci/tools/corpus/wt2" ] && continue
  echo "## haiku $id $(date +%H:%M)"; $PY pilot_run.py --instance instances/$id.json --contexts contexts-$id --model claude-haiku-5-5 --k 10 --out results/$id-claude-haiku-5-5.jsonl 2>&1 | grep -v "^\[.*cached=True" | tail -40
done
echo "## HAIKU_DONE $(date +%H:%M)"
for id in $IDS; do
  [ "$(python -c "import json;print(json.load(open('instances/$id.json'))['repo_path'])" 2>/dev/null)" = "C:/Users/visci/tools/corpus/wt2" ] && continue
  echo "## sonnet $id $(date +%H:%M)"; $PY pilot_run.py --instance instances/$id.json --contexts contexts-$id --model claude-sonnet-5-5 --k 3 --arms A0 A1 P64 P128 P200 --out results/$id-claude-sonnet-5-5.jsonl 2>&1 | tail -20
done
echo "## SONNET_DONE $(date +%H:%M)"
