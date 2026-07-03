#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
required=[Path('public/validation-mesh.html'),Path('public/assets/goalos-validation-mesh-v29.js'),Path('public/assets/goalos-validation-mesh-v29.css'),Path('public/assets/goalos-validation-mesh-routes-v29.js')]
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [Path('public/assets/goalos-validation-mesh-v29.js'),Path('public/assets/goalos-validation-mesh-routes-v29.js')]:
    if p.exists():
        s=p.read_text(encoding='utf-8',errors='ignore')
        for f in forbidden:
            if f in s: hits.append({'file':str(p),'api':f})
broken=[]
for p in Path('public').glob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']',s):
        if href.startswith(('http://','https://','mailto:')): continue
        target=(p.parent/href.split('#')[0]).resolve()
        if not target.exists(): broken.append({'page':p.name,'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
report={'version':'v29','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken}
Path('reports').mkdir(exist_ok=True,parents=True)
Path('reports/validation-mesh-v29-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if status=='passed' else 1)
