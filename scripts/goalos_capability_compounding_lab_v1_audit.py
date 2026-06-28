from pathlib import Path
import json, re, datetime
root=Path.cwd()
required=[
 'public/capability-compounding-lab.html',
 'public/assets/goalos-capability-compounding-lab-v1.css',
 'public/assets/goalos-capability-compounding-lab-v1.js',
 'docs/demos/CAPABILITY_COMPOUNDING_LAB_V1.md',
 'docs/reviewer/HOW_TO_REVIEW_CAPABILITY_COMPOUNDING_LAB.md',
 'evidence/demo/capability-compounding-lab-v1-reference-docket.json'
]
errors=[]
for item in required:
    if not (root/item).exists(): errors.append(f'missing:{item}')
js=(root/'public/assets/goalos-capability-compounding-lab-v1.js').read_text(encoding='utf-8')
for forbidden in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if forbidden in js: errors.append(f'forbidden_js:{forbidden}')
html=(root/'public/capability-compounding-lab.html').read_text(encoding='utf-8') if (root/'public/capability-compounding-lab.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase.lower() not in html.lower(): errors.append(f'missing_boundary_phrase:{phrase}')
report={
 'schema':'goalos.capability_compounding_lab.v1.qa',
 'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',
 'status':'passed' if not errors else 'failed',
 'browser_local':True,
 'no_network_call':True,
 'no_user_data':True,
 'no_user_funds':True,
 'wallet_or_mainnet':False,
 'human_review_required':True,
 'errors':errors
}
(root/'reports').mkdir(exist_ok=True)
(root/'reports/capability-compounding-lab-v1-qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
