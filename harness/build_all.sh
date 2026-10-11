for f in instances/cli__cli-*.json; do
  id=$(basename "$f" .json)
  case "$id" in cli__cli-7f0590c2b805|cli__cli-996be976cad9|cli__cli-9b031151a825|cli__cli-b6770c8bc54c) continue;; esac
  [ -f "contexts-$id/contexts.json" ] && continue
  echo "== $id"; /c/Python314/python pilot_contexts.py --instance "$f" --out "contexts-$id" --model claude-haiku-5-5 2>&1 | tail -12
done
echo BUILD_DONE
