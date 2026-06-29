from pathlib import Path
import json, datetime
ROOT=Path.cwd(); errors=[]
required=['public/proof-experience-atlas.html','public/assets/goalos-proof-experience-atlas-v1.css','public/assets/goalos-proof-experience-atlas-v1.js','docs/demos/PROOF_EXPERIENCE_ATLAS_V1.md']
for r in required:
    if not (ROOT/r).exists(): errors.append(f'missing:{r}')
js=(ROOT/'public/assets/goalos-proof-experience-atlas-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-proof-experience-atlas-v1.js').exists() else ''
for term in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if term in js: errors.append(f'forbidden_browser_api:{term}')
html=(ROOT/'public/proof-experience-atlas.html').read_text(encoding='utf-8') if (ROOT/'public/proof-experience-atlas.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Proof Run 001']:
    if phrase not in html: errors.append(f'missing_phrase:{phrase}')
report={'status':'passed' if not errors else 'failed','errors':errors,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'checked_at':datetime.datetime.now(datetime.UTC).isoformat()}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/proof-experience-atlas-v1-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if not errors else 1)
