
from pathlib import Path
import json, re, py_compile
missing=[]
required=['public/validation-control-tower.html','public/validation-use-cases.html','public/agi-node-use-cases.html','public/assets/goalos-validation-control-tower-v33.css','public/assets/goalos-validation-control-tower-v33.js','public/assets/goalos-validation-control-routes-v33.js']
for r in required:
    if not Path(r).exists(): missing.append(r)
for script in ['scripts/install_validation_control_tower_v33.py','scripts/run_validation_control_tower_v33_demo.py','scripts/goalos_validation_control_tower_v33_audit.py']:
    py_compile.compile(script, doraise=True)
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in Path('public/assets').glob('goalos-validation-control*tower-v33.js'):
    txt=p.read_text(encoding='utf-8', errors='ignore')
    for f in forbidden:
        if f in txt: hits.append({'file':str(p),'pattern':f})
html_pages=list(Path('public').glob('*.html'))
links=[]
for p in html_pages:
    text=p.read_text(encoding='utf-8', errors='ignore')
    for href in re.findall(r'href="([^"]+\.html)"', text):
        if href.startswith('http') or href.startswith('#'): continue
        target=(p.parent/href.split('#')[0]).resolve()
        if not target.exists(): links.append({'source':str(p),'href':href})
status='passed' if not missing and not hits and not links else 'failed'
report={'version':'v33','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':links,'publicPages':len(html_pages)}
Path('reports').mkdir(exist_ok=True)
Path('reports/validation-control-tower-v33-qa.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
Path('reports/validation-control-tower-v33-audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(0 if status=='passed' else 1)
