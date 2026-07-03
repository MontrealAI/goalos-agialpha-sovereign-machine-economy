#!/usr/bin/env python3
import json, re
from pathlib import Path
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in list(PUBLIC.glob('assets/*v39*.js'))+list(PUBLIC.glob('*demo*.html')):
    s=p.read_text(encoding='utf-8', errors='ignore')
    for f in forbidden:
        if f in s: hits.append({'file':str(p),'term':f})
missing=[]
for rel in ['public/autonomous-proof-mission-demo.html','public/autonomous-demo-run-theatre.html','public/end-to-end-demo-use-cases.html','public/proof-mission-demo-academy.html']:
    if not (ROOT/rel).exists(): missing.append(rel)
links=[]
for p in PUBLIC.glob('*.html'):
    s=p.read_text(encoding='utf-8', errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', s):
        if href.startswith('http'): continue
        target=(p.parent/href.split('#')[0]).resolve()
        if not target.exists(): links.append({'from':str(p),'href':href})
status='passed' if not hits and not missing and not links else 'failed'
report={'version':'v39','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':links}
(ROOT/'reports/autonomous-proof-mission-demo-v39-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if status=='passed' else 1)
