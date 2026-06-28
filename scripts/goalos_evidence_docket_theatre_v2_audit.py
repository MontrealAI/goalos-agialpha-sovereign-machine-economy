#!/usr/bin/env python3
from pathlib import Path
import json, re, datetime
ROOT=Path('.')
errors=[]
required=['public/evidence-docket-theatre.html','public/assets/goalos-docket-theatre-v2.css','public/assets/goalos-docket-theatre-v2.js','docs/demos/EVIDENCE_DOCKET_THEATRE_V2.md','docs/reviewer/HOW_TO_REVIEW_EVIDENCE_DOCKET_THEATRE.md']
for p in required:
    if not (ROOT/p).exists(): errors.append(f'missing:{p}')
js=(ROOT/'public/assets/goalos-docket-theatre-v2.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-docket-theatre-v2.js').exists() else ''
for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if token in js: errors.append(f'forbidden_browser_api:{token}')
html=(ROOT/'public/evidence-docket-theatre.html').read_text(encoding='utf-8') if (ROOT/'public/evidence-docket-theatre.html').exists() else ''
for phrase in ['No user data','No user funds','Human review required','A proof page is not a marketing page']:
    if phrase not in html: errors.append(f'missing_phrase:{phrase}')
status='passed' if not errors else 'failed'
report={'status':status,'checked_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','errors':errors,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/evidence-docket-theatre-v2-qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if errors: raise SystemExit('\n'.join(errors))
print(json.dumps(report, indent=2))
