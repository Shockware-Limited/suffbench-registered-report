export PYTHONIOENCODING=utf-8 PYTHONPATH='C:\Users\visci\Python\Python314\site-packages'
PY=/c/Python314/python
for f in instances/cli__cli-*.json; do id=$(basename $f .json)
  [ -d contexts-$id ] || continue; [ "$id" = cli__cli-0c2eea6338a2 ] && continue
  [ -f abl-$id/contexts.json ] && continue
  echo "## $id"; $PY pilot_ablation.py --instance $f --out abl-$id --pilot-contexts contexts-$id 2>&1 | tail -1
done; echo "## ABL_BUILD_DONE"
