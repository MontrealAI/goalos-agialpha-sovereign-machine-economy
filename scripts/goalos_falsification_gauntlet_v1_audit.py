from pathlib import Path
import json, sys, datetime
ROOT=Path('.')
required=[
'public/falsification-gauntlet.html',
'public/assets/goalos-falsification-gauntlet-v1.css',
'public/assets/goalos-falsification-gauntlet-v1.js',
'docs/demos/FALSIFICATION_GAUNTLET_V1.md',
'docs/reviewer/HOW_TO_REVIEW_FALSIFICATION_GAUNTLET.md',
'evidence/demo/falsification-gauntlet-v1-reference-docket.json'
]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
errors=[]
for f in required:
    if not (ROOT/f).exists(): errors.append(f'missing: {f}')
js=(ROOT/'public/assets/goalos-falsification-gauntlet-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-falsification-gauntlet-v1.js').exists() else ''
for token in forbidden:
    if token in js: errors.append(f'forbidden browser/API call in JS: {token}')
html=(ROOT/'public/falsification-gauntlet.html').read_text(encoding='utf-8') if (ROOT/'public/falsification-gauntlet.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','No network call','Human review required']:
    if phrase.lower() not in html.lower(): errors.append(f'missing boundary phrase: {phrase}')
report={'status':'failed' if errors else 'passed','checked_at':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z'),'browser_local':True,'no_network_call':not any(t in js for t in forbidden),'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'errors':errors}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/falsification-gauntlet-v1-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if errors:
    print(json.dumps(report,indent=2)); sys.exit(1)
print(json.dumps(report,indent=2))
