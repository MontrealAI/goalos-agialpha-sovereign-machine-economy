
import json, re, datetime
from pathlib import Path
root=Path.cwd(); public=root/'public'; assets=public/'assets'
required=[public/'goalos.html',public/'index.html',public/'site-map.html',assets/'goalos-universal-mission-interface-v23.js',assets/'goalos-universal-mission-interface-v23.css',assets/'goalos-universal-mission-routes-v23.js']
missing=[str(p) for p in required if not p.exists()]
forbidden=[]
for p in [assets/'goalos-universal-mission-interface-v23.js', assets/'goalos-universal-mission-routes-v23.js']:
    txt=p.read_text(encoding='utf-8',errors='ignore') if p.exists() else ''
    for term in ['XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
        if term in txt: forbidden.append({'file':p.name,'term':term})
    if re.search(r'\bfetch\s*\(', txt): forbidden.append({'file':p.name,'term':'fetch('})
broken=[]
for p in public.rglob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+)["\']',txt,re.I):
        if href.startswith(('http://','https://','mailto:','tel:','#','javascript:')): continue
        target=href.split('#')[0].split('?')[0]
        if target.endswith('.html'):
            path=(p.parent/target).resolve()
            try: path.relative_to(public.resolve())
            except Exception: continue
            if not path.exists(): broken.append({'page':p.relative_to(public).as_posix(),'href':href})
report={'status':'passed' if not missing and not forbidden and not broken else 'failed','missing':missing,'forbiddenBrowserApiHits':forbidden,'brokenInternalHtmlLinks':broken,'publicPages':len(list(public.rglob('*.html'))),'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')}
(root/'reports').mkdir(exist_ok=True)
(root/'reports'/'universal-mission-interface-v23-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if report['status']!='passed': raise SystemExit(1)
