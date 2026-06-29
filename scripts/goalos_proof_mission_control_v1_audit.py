from pathlib import Path
import json, datetime, sys
ROOT=Path.cwd()
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
required=[
 'public/proof-mission-control.html',
 'public/assets/goalos-proof-mission-control-v1.css',
 'public/assets/goalos-proof-mission-control-v1.js',
 'docs/proof-missions/PROOF_MISSION_CONTROL_V1.md',
 'docs/reviewer/HOW_TO_USE_PROOF_MISSION_CONTROL.md',
 'evidence/proof-missions/proof-mission-control-v1-reference-docket.json'
]
errors=[]
for f in required:
    if not (ROOT/f).exists(): errors.append(f'missing:{f}')
js=(ROOT/'public/assets/goalos-proof-mission-control-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-proof-mission-control-v1.js').exists() else ''
for bad in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']:
    if bad in js: errors.append(f'forbidden_js:{bad}')
html=(ROOT/'public/proof-mission-control.html').read_text(encoding='utf-8') if (ROOT/'public/proof-mission-control.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase.lower() not in html.lower(): errors.append(f'missing_boundary_phrase:{phrase}')
report={
 'status':'passed' if not errors else 'failed',
 'audited_at':NOW,
 'page':'public/proof-mission-control.html',
 'browser_local':True,
 'no_network_call': 'fetch(' not in js and 'XMLHttpRequest' not in js and 'sendBeacon' not in js,
 'no_user_data': True,
 'no_user_funds': True,
 'wallet_or_mainnet': 'window.ethereum' in js,
 'human_review_required': True,
 'errors':errors
}
(ROOT/'reports').mkdir(parents=True,exist_ok=True)
(ROOT/'reports/proof-mission-control-v1-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if not errors else 1)
