export PYTHONIOENCODING=utf-8 PYTHONPATH='C:\Users\visci\Python\Python314\site-packages'
PY=/c/Python314/python
mkdir -p results-abl
for f in instances/cli__cli-*.json; do id=$(basename $f .json)
  [ -d contexts-$id ] || continue                      # the 24 pilot instances only
  [ "$id" = cli__cli-0c2eea6338a2 ] && continue        # empty task text; invalid (erratum 2026-10-12)
  [ -f abl-$id/contexts.json ] || { echo "## $id no contexts"; continue; }
  echo "## abl $id $(date +%H:%M)"
  $PY pilot_run.py --instance $f --contexts abl-$id --model claude-haiku-5-5 --k 20 --out results-abl/$id-claude-haiku-5-5.jsonl 2>&1 | grep -v "cached=True" | tail -12
done
echo "## ABL_RUN_DONE $(date +%H:%M)"
