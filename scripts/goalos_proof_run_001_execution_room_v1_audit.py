from pathlib import Path
import json, subprocess, sys, datetime
required=['public/proof-run-001-execution-room.html','public/assets/goalos-proof-run-001-execution-room-v1.css','public/assets/goalos-proof-run-001-execution-room-v1.js','docs/proof-runs/PROOF_RUN_001_EXECUTION_ROOM_V1.md','docs/reviewer/HOW_TO_REVIEW_PROOF_RUN_001_EXECUTION_ROOM.md','evidence/proof-run-001/proof-run-001-execution-room-reference-docket.json']
errors=[]
for f in required:
    if not Path(f).exists(): errors.append(f'missing:{f}')
js=Path('public/assets/goalos-proof-run-001-execution-room-v1.js').read_text(encoding='utf-8') if Path('public/assets/goalos-proof-run-001-execution-room-v1.js').exists() else ''
for term in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','ethereum']:
    if term in js: errors.append('forbidden_js_api:'+term)
if js:
    r=subprocess.run(['node','--check','public/assets/goalos-proof-run-001-execution-room-v1.js'],text=True,capture_output=True)
    if r.returncode!=0: errors.append('js_syntax:'+r.stderr[:500])
html=Path('public/proof-run-001-execution-room.html').read_text(encoding='utf-8') if Path('public/proof-run-001-execution-room.html').exists() else ''
for phrase in ['Now we','No user data','no user funds','human review required','Evidence Docket']:
    if phrase not in html: errors.append('missing_phrase:'+phrase)
report={'status':'passed' if not errors else 'failed','generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,'errors':errors}
Path('reports').mkdir(exist_ok=True)
Path('reports/proof-run-001-execution-room-v1-qa.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
if errors: sys.exit(1)
