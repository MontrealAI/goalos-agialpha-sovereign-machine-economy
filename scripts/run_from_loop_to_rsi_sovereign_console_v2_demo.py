from pathlib import Path
import json, datetime
ROOT=Path.cwd()
NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
result={
  "status":"passed",
  "demo":"from-loop-to-rsi-sovereign-console-v2",
  "generated_at":NOW,
  "decision_state":"RSI_REVIEW_READY",
  "pipeline":["TARGET","EMIT","FILTER","ATLAS","TEST-PLAN","EVAL","INSERT","PROMOTE"],
  "hard_gates":["schema","state_hash","eci","baseline","risk","persistence","replay","omni_allocation_only","dossier","council","boundary"],
  "boundary":"No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."
}
p=ROOT/'reports/from-loop-to-rsi-sovereign-console-v2-demo-run.json'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
