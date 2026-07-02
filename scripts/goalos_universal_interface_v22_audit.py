from __future__ import annotations
import json, pathlib, re, sys
ROOT=pathlib.Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'
required=[PUBLIC/'goalos.html',PUBLIC/'index.html',ASSETS/'goalos-universal-interface-v22.js',ASSETS/'goalos-universal-interface-v22.css',PUBLIC/'site-map.html',PUBLIC/'search.html']
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [ASSETS/'goalos-universal-interface-v22.js',ASSETS/'goalos-universal-interface-routes-v22.js']:
    txt=p.read_text(encoding='utf-8') if p.exists() else ''
    for f in forbidden:
        if f in txt: hits.append({'file':str(p),'pattern':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']',txt,re.I):
        if href.startswith(('http://','https://','mailto:')): continue
        if not (PUBLIC/href.split('#')[0]).exists(): broken.append({'file':p.name,'href':href})
report={'status':'passed' if not missing and not hits and not broken else 'failed','missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(list(PUBLIC.glob('*.html')))}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/universal-interface-v22-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if report['status']!='passed': sys.exit(1)
