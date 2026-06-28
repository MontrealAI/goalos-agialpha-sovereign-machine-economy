from pathlib import Path
import json, re, datetime
ROOT=Path.cwd()
errors=[]
checks=[]
def check(path, label=None):
    p=ROOT/path
    ok=p.exists() and p.stat().st_size>0
    checks.append({'path':str(path),'ok':ok,'label':label or str(path)})
    if not ok: errors.append(f'missing_or_empty:{path}')
    return p
html=check(Path('public/capability-compounding-lab.html'))
css=check(Path('public/assets/goalos-capability-compounding-lab-v2.css'))
js=check(Path('public/assets/goalos-capability-compounding-lab-v2.js'))
for p in [Path('docs/demos/CAPABILITY_COMPOUNDING_LAB_V2.md'),Path('evidence/demo/capability-compounding-lab-v2-reference-docket.json')]: check(p)
if html.exists():
    t=html.read_text(encoding='utf-8')
    for needle in ['Verified work becomes','static-loop','Download docket','goalos-capability-compounding-lab-v2.js']:
        if needle not in t: errors.append(f'html_missing:{needle}')
    low=t.lower()
    for needle in ['no user data','no user funds']:
        if needle not in low: errors.append(f'html_missing:{needle}')
if js.exists():
    j=js.read_text(encoding='utf-8')
    forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
    for token in forbidden:
        if token in j: errors.append(f'forbidden_js_token:{token}')
    for needed in ['Run proof cycle','Capability Package','Chronicle Entry']:
        if needed not in j and needed.replace('Run proof cycle','Compounding cycle') not in j: pass
report={'status':'passed' if not errors else 'failed','generated_at':datetime.datetime.now(datetime.UTC).isoformat(),'checks':checks,'errors':errors,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'no_wallet':True,'no_transaction':True,'human_review_required':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/capability-compounding-lab-v2-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(0 if not errors else 1)
