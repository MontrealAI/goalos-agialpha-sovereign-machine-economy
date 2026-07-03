#!/usr/bin/env python3
import json, re
from pathlib import Path
from datetime import datetime, timezone
required=[
 'public/validation-authority.html','public/human-or-node-validation.html','public/agi-node-validation.html',
 'public/assets/goalos-validation-authority-v28.css','public/assets/goalos-validation-authority-v28.js',
 'public/assets/goalos-validation-authority-routes-v28.js','docs/website/VALIDATION_AUTHORITY_V28.md',
 'docs/reviewer/HOW_TO_REVIEW_VALIDATION_AUTHORITY_V28.md','content/goalos/validation-authority-v28.json',
 'reports/validation-authority-v28-install-report.json','reports/validation-authority-v28-demo-run.json'
]
missing=[p for p in required if not Path(p).exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for js in Path('public/assets').glob('goalos-validation-authority-v28*.js'):
    s=js.read_text(encoding='utf-8')
    for f in forbidden:
        if f in s: hits.append({'file':str(js),'term':f})
broken=[]
for hp in [Path('public/validation-authority.html'),Path('public/human-or-node-validation.html'),Path('public/agi-node-validation.html')]:
    if not hp.exists(): continue
    s=hp.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"]+\.html)"',s):
        if href.startswith('http'): continue
        target=(hp.parent/href.split('#')[0])
        if not target.exists(): broken.append({'file':str(hp),'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
report={'version':'v28','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'generatedAt':datetime.now(timezone.utc).isoformat()}
Path('reports').mkdir(exist_ok=True)
Path('reports/validation-authority-v28-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
Path('reports/validation-authority-v28-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if status=='passed' else 1)
