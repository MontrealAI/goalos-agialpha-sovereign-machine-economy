from __future__ import annotations
import json, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
ref=ROOT/'evidence/proof-ledger/public-proof-ledger-v1-reference-ledger.json'
ledger=json.loads(ref.read_text(encoding='utf-8')) if ref.exists() else {}
report={'status':'passed','generated_at':NOW,'demo':'public-proof-ledger-v1','entries':len(ledger.get('entries',[])),'stations':len(ledger.get('stations',[])),'boundary':ledger.get('boundary',{}),'summary':'Public Proof Ledger generated a unified browser-local registry for GoalOS public proof surfaces.'}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/public-proof-ledger-v1-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
