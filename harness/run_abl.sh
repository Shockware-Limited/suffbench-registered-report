export PYTHONIOENCODING=utf-8
[ -f "$(dirname "$0")/env.local.sh" ] && . "$(dirname "$0")/env.local.sh"
PY=/c/Python314/python
mkdir -p results-abl
for id in $(cat abl_ids.txt); do   # the 23 valid pilot instances (0c2eea6338a2 excluded: empty task text)
  [ -f abl-$id/contexts.json ] || { echo "## $id no contexts"; continue; }
  echo "## abl $id $(date +%H:%M)"
  $PY pilot_run.py --instance instances/$id.json --contexts abl-$id --model claude-haiku-5-5 --k 20 --out results-abl/$id-claude-haiku-5-5.jsonl 2>&1 | grep -v "cached=True" | tail -12
done
echo "## ABL_RUN_DONE $(date +%H:%M)"
