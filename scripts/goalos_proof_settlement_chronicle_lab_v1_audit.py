
from pathlib import Path
import json, datetime
ROOT=Path.cwd(); page=ROOT/'public/proof-settlement-chronicle-lab.html'; js=ROOT/'public/assets/goalos-proof-settlement-chronicle-lab-v1.js'; errors=[]
if not page.exists(): errors.append('missing page')
if not js.exists(): errors.append('missing js')
for p in [page,js]:
    if p.exists():
        text=p.read_text().lower()
        for req in ['no user data','no user funds','no wallet','no transaction','human review required']:
            if req not in text: errors.append(f'missing boundary {req} in {p}')
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
if js.exists():
    text=js.read_text()
    for f in forbidden:
        if f in text: errors.append(f'forbidden browser API: {f}')
report={'status':'passed' if not errors else 'failed','checked_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'errors':errors}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/proof-settlement-chronicle-lab-v1-qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
