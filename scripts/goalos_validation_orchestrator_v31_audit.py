#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [ASSETS/'goalos-validation-orchestrator-v31.js', ASSETS/'goalos-validation-orchestrator-routes-v31.js']:
    if p.exists():
        txt=p.read_text(encoding='utf-8',errors='ignore')
        for f in forbidden:
            if f in txt: hits.append({'file':str(p),'token':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']',s):
        if href.startswith('http') or href.startswith('mailto:'): continue
        target=p.parent/href.split('#')[0]
        if not target.exists(): broken.append({'source':p.name,'target':href})
required=['validation-orchestrator.html','validation-studio.html','validation-use-cases.html','assets/goalos-validation-orchestrator-v31.css','assets/goalos-validation-orchestrator-v31.js']
missing=[x for x in required if not (PUBLIC/x).exists()]
status='passed' if not hits and not broken and not missing else 'failed'
out={'version':'v31','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(list(PUBLIC.glob('*.html')))}
for name in ['qa','route-health','audit']:
    (REPORTS/f'validation-orchestrator-v31-{name}.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
if status!='passed': raise SystemExit(1)
