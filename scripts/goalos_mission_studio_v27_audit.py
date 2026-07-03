from pathlib import Path
import json,re,sys
PUBLIC=Path('public');AS=PUBLIC/'assets';REPORTS=Path('reports');REPORTS.mkdir(exist_ok=True)
required=['goalos.html','index.html','use-case-playbooks.html','ask-goalos.html','site-map.html','search.html','trust-boundary.html','token-boundary.html','assets/goalos-mission-studio-v27.js','assets/goalos-mission-studio-v27.css','assets/goalos-mission-routes-v27.js']
missing=[r for r in required if not (PUBLIC/r).exists()]
forbidden=[]
for p in [AS/'goalos-mission-studio-v27.js',AS/'goalos-mission-routes-v27.js']:
    if p.exists():
        tx=p.read_text(encoding='utf-8',errors='ignore')
        for pat in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if pat in tx: forbidden.append({'file':str(p),'pattern':pat})
broken=[]
for p in PUBLIC.rglob('*.html'):
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('downloads/','archive/')): continue
    tx=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+)["\']',tx,re.I):
        if href.startswith(('#','http','mailto:','tel:','javascript:')): continue
        target=href.split('#')[0].split('?')[0]
        if target.endswith('.html') and not (PUBLIC/target).exists(): broken.append({'from':rel,'to':target})
status='passed' if not missing and not forbidden and not broken else 'failed'
report={'version':'v27','status':status,'missing':missing,'forbiddenBrowserApiHits':forbidden,'brokenInternalHtmlLinks':broken,'publicPages':len(list(PUBLIC.rglob('*.html')))}
(REPORTS/'mission-studio-v27-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
