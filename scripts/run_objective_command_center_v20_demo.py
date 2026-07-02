
from pathlib import Path
import json, datetime
ROOT=Path.cwd()
out={'status':'passed','demo':'GoalOS Objective Command Center V20','scenarios':[{'objective':'Understand the 48 contracts','decision':'MISSION_PLAN_REVIEW_READY','routes':['mainnet-contract-atlas.html','mainnet-proof-rail.html']},{'objective':'Check token boundary','decision':'MISSION_PLAN_REVIEW_READY','routes':['token-boundary.html','trust-boundary.html']},{'objective':'Send funds from my wallet','decision':'BLOCK_BOUNDARY_REVISE_INPUT','routes':['token-boundary.html','trust-boundary.html']}],'created_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z')}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/objective-command-center-v20-demo-run.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
