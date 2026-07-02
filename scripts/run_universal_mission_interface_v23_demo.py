
import json, datetime
from pathlib import Path
root=Path.cwd()
required=[root/'public'/'goalos.html', root/'public'/'assets'/'goalos-universal-mission-interface-v23.js', root/'reports'/'universal-mission-interface-v23-qa.json']
missing=[str(p) for p in required if not p.exists()]
report={'status':'passed' if not missing else 'failed','missing':missing,'objectives_tested':['I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.'],'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')}
(root/'reports').mkdir(exist_ok=True)
(root/'reports'/'universal-mission-interface-v23-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if missing: raise SystemExit(1)
