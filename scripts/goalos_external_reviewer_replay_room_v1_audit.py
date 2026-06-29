#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT=Path.cwd(); NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
errors=[]
required=[
 'public/external-reviewer-replay-room.html','public/assets/goalos-reviewer-replay-v1.css','public/assets/goalos-reviewer-replay-v1.js','docs/reviewer/EXTERNAL_REVIEWER_REPLAY_ROOM_V1.md','docs/reviewer/HOW_TO_USE_EXTERNAL_REVIEWER_REPLAY_ROOM.md','reports/external-reviewer-replay-room-v1-demo-run.json','evidence/reviewer-replay/external-reviewer-replay-room-v1-reference-docket.json'
]
for f in required:
    if not (ROOT/f).exists(): errors.append(f'missing:{f}')
page=(ROOT/'public/external-reviewer-replay-room.html').read_text(errors='ignore') if (ROOT/'public/external-reviewer-replay-room.html').exists() else ''
for phrase in ['No user data','No user funds','Human review required','no wallet','no transaction']:
    if phrase.lower() not in page.lower(): errors.append('missing boundary phrase:'+phrase)
js=(ROOT/'public/assets/goalos-reviewer-replay-v1.js').read_text(errors='ignore') if (ROOT/'public/assets/goalos-reviewer-replay-v1.js').exists() else ''
for bad in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if bad in js: errors.append('forbidden browser API:'+bad)
report={'status':'passed' if not errors else 'failed','generated_at':NOW,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'errors':errors}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/external-reviewer-replay-room-v1-qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
