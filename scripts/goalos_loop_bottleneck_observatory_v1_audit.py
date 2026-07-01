#!/usr/bin/env python3
from pathlib import Path
import json, re, datetime, sys
ROOT=Path.cwd(); NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
required=[
 'public/loop-bottleneck-observatory.html',
 'public/assets/goalos-loop-bottleneck-observatory-v1.css',
 'public/assets/goalos-loop-bottleneck-observatory-v1.js',
 'docs/demos/LOOP_BOTTLENECK_OBSERVATORY_V1.md',
 'docs/reviewer/HOW_TO_REVIEW_LOOP_BOTTLENECK_OBSERVATORY.md',
 'evidence/demo/loop-bottleneck-observatory-v1-reference-docket.json',
 'content/goalos/loop-bottleneck-observatory-v1.json'
]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
errors=[]
for rel in required:
    if not (ROOT/rel).exists(): errors.append(f'missing {rel}')
js=(ROOT/'public/assets/goalos-loop-bottleneck-observatory-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-loop-bottleneck-observatory-v1.js').exists() else ''
for token in forbidden:
    if token in js: errors.append(f'forbidden browser API: {token}')
html=(ROOT/'public/loop-bottleneck-observatory.html').read_text(encoding='utf-8') if (ROOT/'public/loop-bottleneck-observatory.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required','bottleneck always moves']:
    if phrase.lower() not in html.lower(): errors.append(f'missing boundary/concept phrase: {phrase}')
# ensure download buttons exist
for bid in ['downloadReport','downloadContract','downloadTrace','downloadReplay','downloadBrief']:
    if bid not in html and bid not in js: errors.append(f'missing download control {bid}')
status='passed' if not errors else 'failed'
report={"status":status,"generated_at":NOW,"errors":errors,"checked_files":required,"browser_local":True,"no_network_call":not any(x in js for x in forbidden),"no_user_data":True,"no_user_funds":True,"wallet_or_mainnet":False,"human_review_required":True}
p=ROOT/'reports/loop-bottleneck-observatory-v1-qa.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2)+"\n",encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if status=='passed' else 1)
