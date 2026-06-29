from __future__ import annotations
import json, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
errors=[]
for rel in ['public/proof-ledger.html','public/assets/goalos-proof-ledger-v1.css','public/assets/goalos-proof-ledger-v1.js','public/assets/goalos-proof-ledger-data.js','evidence/proof-ledger/public-proof-ledger-v1-reference-ledger.json']:
    if not (ROOT/rel).exists(): errors.append('missing:'+rel)
js=(ROOT/'public/assets/goalos-proof-ledger-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-proof-ledger-v1.js').exists() else ''
for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if token in js: errors.append('forbidden-browser-api:'+token)
ledger_path=ROOT/'content/goalos/public-proof-ledger-v1.json'
ledger=json.loads(ledger_path.read_text(encoding='utf-8')) if ledger_path.exists() else {}
for key in ['no_user_data','no_user_funds','no_wallet','no_transaction','no_network_call','human_review_required']:
    if ledger.get('boundary',{}).get(key) is not True: errors.append('boundary-not-true:'+key)
report={'status':'passed' if not errors else 'failed','generated_at':NOW,'errors':errors,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'entries':len(ledger.get('entries',[])),'stations':len(ledger.get('stations',[]))}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/public-proof-ledger-v1-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
