export PYTHONIOENCODING=utf-8 PYTHONPATH='C:\Users\visci\Python\Python314\site-packages'
PY=/c/Python314/python
IDS=$($PY -c "
import json,glob
ids=[]
for f in sorted(glob.glob('results/cli__cli-*-claude-sonnet-5-5.jsonl')):
    rs=[json.loads(l) for l in open(f,encoding='utf-8')]
    if not any(r['arm']=='A0' and r.get('delta_pass') for r in rs): ids.append(rs[0]['instance_id'])
print(' '.join(ids))")
echo "## subset: $IDS"
for id in $IDS; do
  spent=$($PY -c "
import json,glob
c=0
for f in glob.glob('results/cli__cli-*-claude-opus-5.jsonl'):
    for l in open(f,encoding='utf-8'):
        for u in json.loads(l).get('usage',[]): c+=(u['in']*5+u['out']*25+u['cache_read']*0.5+u['cache_write']*6.25)/1e6
print(round(c,2))")
  echo "## opus $id spent_so_far=\$$spent $(date +%H:%M)"
  awk -v s="$spent" 'BEGIN{exit !(s>30)}' && { echo "## STOP spend cap"; break; }
  wt=$($PY -c "import json;print(json.load(open('instances/$id.json'))['repo_path'])")
  $PY pilot_run.py --instance instances/$id.json --contexts contexts-$id --model claude-opus-5 --k 3 --arms A0 A1 P200 --out results/$id-claude-opus-5.jsonl 2>&1 | tail -9
done
echo "## OPUS_DONE $(date +%H:%M)"
