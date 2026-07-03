
from pathlib import Path
import json, re, datetime
PUBLIC=Path('public')
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in PUBLIC.glob('assets/*v40*.js'):
    t=p.read_text(encoding='utf-8')
    for f in forbidden:
        if f in t: hits.append({'file':str(p),'token':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', txt):
        if href.startswith('http'): continue
        if not (PUBLIC/href.split('#')[0]).exists(): broken.append({'source':p.name,'href':href})
status='passed' if not hits and not broken else 'needs_review'
obj={'version':'v40','status':status,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
out=Path('reports'); out.mkdir(exist_ok=True)
(out/'autonomous-mission-studio-v40-audit.json').write_text(json.dumps(obj,indent=2),encoding='utf-8')
print(json.dumps(obj,indent=2))
if hits or broken: raise SystemExit(2)
