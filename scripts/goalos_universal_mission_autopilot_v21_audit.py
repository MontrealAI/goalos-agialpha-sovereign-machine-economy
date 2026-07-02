from __future__ import annotations
import json, pathlib, re, datetime, sys
ROOT=pathlib.Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'
required=[PUBLIC/'tell-goalos.html', PUBLIC/'universal-mission-autopilot.html', ASSETS/'goalos-universal-mission-autopilot-v21.js', ASSETS/'goalos-universal-mission-autopilot-v21.css', ASSETS/'goalos-universal-mission-routes-v21.js']
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
missing=[str(p) for p in required if not p.exists()]; hits=[]
for p in [ASSETS/'goalos-universal-mission-autopilot-v21.js', ASSETS/'goalos-universal-mission-routes-v21.js']:
    if p.exists():
        text=p.read_text(encoding='utf-8', errors='ignore')
        for f in forbidden:
            if f in text: hits.append({'file':str(p),'term':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    text=p.read_text(encoding='utf-8', errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', text):
        if href.startswith(('http','mailto:','#')): continue
        if not (PUBLIC/href).exists(): broken.append({'file':p.name,'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
report={'status':status,'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(list(PUBLIC.glob('*.html')))}
for name in ['qa','audit','route-health']:
    q=ROOT/f'reports/universal-mission-autopilot-v21-{name}.json'; q.parent.mkdir(parents=True, exist_ok=True); q.write_text(json.dumps(report,indent=2), encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
