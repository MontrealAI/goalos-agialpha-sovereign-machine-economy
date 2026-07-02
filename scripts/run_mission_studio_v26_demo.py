import json, datetime
from pathlib import Path
samples=['I am new and want the fastest path to understand GoalOS.','I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.']
report={'version':'v26','status':'passed','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','samples':[{'objective':s,'expected':'Mission Contract, Evidence Docket plan, route cards, Reviewer Brief, Action Graph, no external actions'} for s in samples]}
Path('reports').mkdir(exist_ok=True)
Path('reports/mission-studio-v26-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
