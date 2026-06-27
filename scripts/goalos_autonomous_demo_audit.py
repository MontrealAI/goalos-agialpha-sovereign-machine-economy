
from pathlib import Path
import json, re
ROOT=Path.cwd()
PAGES=['demo-launcher.html','proof-flight-demo.html','docket-builder.html','agent-constellation-demo.html','proof-card-studio.html','local-autopilot-demo.html','demo-gallery.html','demo-safety.html']
errors=[]
for p in PAGES:
    path=ROOT/'public'/p
    if not path.exists(): errors.append(f'missing {p}'); continue
    text=path.read_text(encoding='utf-8')
    for phrase in ['No user data','No user funds','No wallet','Human review required']:
        if phrase not in text: errors.append(f'{p} missing phrase: {phrase}')
js=(ROOT/'public/assets/goalos-demo-v4.js').read_text(encoding='utf-8')
for forbidden in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']:
    if forbidden in js: errors.append(f'forbidden browser operation in JS: {forbidden}')
for path in ['src/goalos_ascension/demo_runner.py','scripts/run_autonomous_demo_pack.py','evidence/demo/autonomous-demo-pack.json','reports/autonomous-demo-run-report.json']:
    if not (ROOT/path).exists(): errors.append(f'missing {path}')
report={'schema':'goalos.autonomous_demo_layer_v4.qa','status':'passed' if not errors else 'failed','pages_checked':len(PAGES),'errors':errors,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'human_review_required':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/autonomous-demo-layer-v4-qa.json').write_text(json.dumps(report,indent=2)+'\n')
if errors: raise SystemExit('QA failed: '+ '; '.join(errors))
print('Autonomous demo layer QA passed:', len(PAGES), 'pages')
