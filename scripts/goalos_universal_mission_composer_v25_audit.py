from pathlib import Path
import json, re, py_compile
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'
missing=[]
for path in ['public/index.html','public/goalos.html','public/ask-goalos.html','public/site-map.html','public/search.html','public/assets/goalos-universal-mission-composer-v25.js','public/assets/goalos-universal-mission-composer-v25.css','public/assets/goalos-universal-mission-routes-v25.js']:
    if not Path(path).exists(): missing.append(path)
for script in ['scripts/install_universal_mission_composer_v25.py','scripts/run_universal_mission_composer_v25_demo.py','scripts/goalos_universal_mission_composer_v25_audit.py']:
    py_compile.compile(script,doraise=True)
forbidden=[]
for p in [ASSETS/'goalos-universal-mission-composer-v25.js',ASSETS/'goalos-universal-mission-routes-v25.js']:
    txt=p.read_text(encoding='utf-8',errors='ignore') if p.exists() else ''
    for term in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
        if term in txt: forbidden.append({'file':str(p),'term':term})
existing={p.relative_to(PUBLIC).as_posix() for p in PUBLIC.rglob('*.html')}; broken=[]; href_re=re.compile(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']',re.I)
for p in PUBLIC.rglob('*.html'):
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('archive/','downloads/')): continue
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for h in href_re.findall(txt):
        if h.startswith(('http://','https://','mailto:')): continue
        target=h.split('#')[0]
        try: target_rel=(p.parent/target).resolve().relative_to(PUBLIC.resolve()).as_posix()
        except Exception: continue
        if target_rel not in existing: broken.append({'from':rel,'href':h,'resolved':target_rel})
status='passed' if not missing and not forbidden and not broken else 'review'
report={'version':'v25','status':status,'missing':missing,'forbiddenBrowserApiHits':forbidden,'brokenInternalHtmlLinks':broken,'publicPages':len([x for x in existing if x!='404.html'])}
REPORTS.mkdir(exist_ok=True)
REPORTS.joinpath('universal-mission-composer-v25-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': raise SystemExit(1)
