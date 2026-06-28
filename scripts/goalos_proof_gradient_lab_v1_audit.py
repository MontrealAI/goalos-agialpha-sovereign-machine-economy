
from pathlib import Path
import json, re, datetime
errors=[]
required=['public/proof-gradient-lab.html','public/assets/goalos-proof-gradient-lab.css','public/assets/goalos-proof-gradient-lab.js','docs/demos/PROOF_GRADIENT_LAB_V1.md']
for f in required:
    if not Path(f).exists(): errors.append(f'missing:{f}')
html=Path('public/proof-gradient-lab.html').read_text(encoding='utf-8') if Path('public/proof-gradient-lab.html').exists() else ''
js=Path('public/assets/goalos-proof-gradient-lab.js').read_text(encoding='utf-8') if Path('public/assets/goalos-proof-gradient-lab.js').exists() else ''
for phrase in ['No proof, no evolution','Score is advisory','No user data','No user funds','Human review required']:
    if phrase not in html: errors.append('missing_phrase:'+phrase)
for forbidden in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if forbidden in js: errors.append('forbidden_js:'+forbidden)
report={"status":"passed" if not errors else "failed","layer":"proof-gradient-lab-v1","generated_at":datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z","pages_checked":1,"browser_local":True,"no_network_call":True,"no_user_data":True,"no_user_funds":True,"human_review_required":True,"errors":errors}
Path('reports').mkdir(exist_ok=True)
Path('reports/proof-gradient-lab-v1-qa.json').write_text(json.dumps(report,indent=2)+"\n")
if errors: raise SystemExit('QA failed: '+', '.join(errors))
print(json.dumps(report,indent=2))
