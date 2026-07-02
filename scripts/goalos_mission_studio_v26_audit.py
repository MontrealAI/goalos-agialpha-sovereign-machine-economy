from pathlib import Path
import json, re, sys
PUBLIC=Path('public'); ASSETS=PUBLIC/'assets'
required=[PUBLIC/'index.html',PUBLIC/'goalos.html',PUBLIC/'ask-goalos.html',PUBLIC/'use-case-playbooks.html',PUBLIC/'site-map.html',PUBLIC/'search.html',ASSETS/'goalos-mission-studio-v26.css',ASSETS/'goalos-mission-studio-v26.js',ASSETS/'goalos-mission-routes-v26.js']
missing=[p.as_posix() for p in required if not p.exists()]
forbidden=[]
for p in [ASSETS/'goalos-mission-studio-v26.js',ASSETS/'goalos-mission-routes-v26.js']:
    if p.exists():
        txt=p.read_text(encoding='utf-8',errors='ignore')
        for term in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if term in txt: forbidden.append({'file':p.as_posix(),'term':term})
existing={p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob('*.html')} if PUBLIC.exists() else set()
href_re=re.compile(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']',re.I)
broken=[]
for p in PUBLIC.rglob('*.html') if PUBLIC.exists() else []:
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('downloads/','archive/')): continue
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for h in href_re.findall(txt):
        if h.startswith(('http://','https://','mailto:')): continue
        target=h.split('#')[0].lstrip('/')
        try: tr=(p.parent/target).resolve().relative_to(PUBLIC.resolve()).as_posix()
        except Exception: continue
        if tr not in existing: broken.append({'from':rel,'href':h,'resolved':tr})
status='passed' if not missing and not forbidden and not broken else 'failed'
report={'version':'v26','status':status,'missing':missing,'forbiddenBrowserApiHits':forbidden,'brokenInternalHtmlLinks':broken,'publicPages':len(existing)}
Path('reports').mkdir(exist_ok=True)
Path('reports/mission-studio-v26-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
