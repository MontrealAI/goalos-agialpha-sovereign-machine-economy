#!/usr/bin/env python3
from pathlib import Path
import json,re
root=Path.cwd(); public=root/'public'; forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']; hits=[]
for p in (public/'assets').glob('goalos-agi-agent-mission-*v37*.js'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for f in forbidden:
        if f in txt: hits.append({'file':str(p),'pattern':f})
broken=[]
for h in public.glob('*.html'):
    txt=h.read_text(encoding='utf-8',errors='ignore')
    for m in re.findall(r'''href=["']([^"']+\.html(?:#[^"']*)?)["']''',txt):
        target=m.split('#')[0]
        if not (public/target).exists(): broken.append({'file':h.name,'target':target})
report={'version':'v37','status':'passed' if not hits and not broken else 'failed','forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(list(public.glob('*.html')))}
(root/'reports').mkdir(exist_ok=True); (root/'reports/agi-agent-mission-control-v37-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if hits or broken: raise SystemExit(1)
