#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
required=[PUBLIC/'autonomy-theatre.html',PUBLIC/'assets/goalos-autonomy-theatre-v41.js',PUBLIC/'assets/goalos-autonomy-theatre-v41.css',PUBLIC/'assets/goalos-autonomy-theatre-data-v41.js']
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in (PUBLIC/'assets').glob('*v41*.js'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for f in forbidden:
        if f in s: hits.append({'file':str(p),'token':f})
pages={p.name for p in PUBLIC.glob('*.html')}; broken=[]
for p in PUBLIC.glob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']',s):
        t=href.split('#')[0]
        if t and '/' not in t and not t.startswith('http') and t not in pages: broken.append({'page':p.name,'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
report={'version':'v41','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(pages)}
Path('reports').mkdir(exist_ok=True)
(Path('reports')/'autonomy-theatre-v41-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
