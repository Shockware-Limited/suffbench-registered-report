export PYTHONIOENCODING=utf-8 PYTHONPATH='C:\Users\visci\Python\Python314\site-packages'
PY=/c/Python314/python
for f in instances/cli__cli-*.json; do
  id=$(basename "$f" .json)
  $PY -c "import json,sys; sys.exit(0 if json.load(open('$f')).get('repo_path','').endswith('wt2') else 1)" || continue
  [ -f "contexts-$id/contexts.json" ] || { echo "== build $id"; $PY pilot_contexts.py --instance "$f" --out "contexts-$id" --model claude-haiku-5-5 2>&1 | tail -10; }
done
echo "## BUILD2_DONE $(date +%H:%M)"
for f in instances/cli__cli-*.json; do
  id=$(basename "$f" .json)
  $PY -c "import json,sys; sys.exit(0 if json.load(open('$f')).get('repo_path','').endswith('wt2') else 1)" || continue
  [ -f "contexts-$id/contexts.json" ] || continue
  echo "## haiku2 $id $(date +%H:%M)"; $PY pilot_run.py --instance "$f" --contexts "contexts-$id" --model claude-haiku-5-5 --k 10 --out "results/$id-claude-haiku-5-5.jsonl" 2>&1 | grep -v "cached=True" | tail -30
done
echo "## HAIKU2_DONE $(date +%H:%M)"
for f in instances/cli__cli-*.json; do
  id=$(basename "$f" .json)
  $PY -c "import json,sys; sys.exit(0 if json.load(open('$f')).get('repo_path','').endswith('wt2') else 1)" || continue
  [ -f "contexts-$id/contexts.json" ] || continue
  echo "## sonnet2 $id $(date +%H:%M)"; $PY pilot_run.py --instance "$f" --contexts "contexts-$id" --model claude-sonnet-5-5 --k 3 --arms A0 A1 P64 P128 P200 --out "results/$id-claude-sonnet-5-5.jsonl" 2>&1 | tail -16
done
echo "## SONNET2_DONE $(date +%H:%M)"
