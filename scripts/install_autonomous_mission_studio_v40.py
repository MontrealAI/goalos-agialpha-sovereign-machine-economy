
from pathlib import Path
import json, re, datetime
VERSION='v40'
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
PUBLIC.mkdir(exist_ok=True)
(PUBLIC/'.nojekyll').write_text('', encoding='utf-8')
created=[]
required=['index.html','site-map.html','search.html','ask-goalos.html','agi-agent-workbench.html','validation-control-tower.html','goalos.html','mainnet-contract-atlas.html','trust-boundary.html','token-boundary.html','mainnet-proof-rail.html','contract-academy.html','proof-mission-demo-academy.html','demo-ecosystem-registry.html','site-health.html','from-loop-to-rsi-state-capacity.html','privacy.html','data-boundary.html','no-data-no-funds.html','autonomous-proof-mission-demo.html']
for name in required:
    p=PUBLIC/name
    if not p.exists():
        title=name.replace('.html','').replace('-',' ').title()
        p.write_text(f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="assets/goalos-autonomous-mission-studio-v40.css"></head><body class="grid"><div class="aurora"></div><header class="topbar"><a class="logo" href="index.html"><span class="logoMark"></span><span class="logoText"><b>GOALOS</b><span>AGIALPHA ASCENSION</span></span></a><nav class="nav"><a class="primary" href="autonomous-mission-studio.html">Demo</a><a href="site-map.html">All Pages</a><a href="search.html">Search /</a></nav></header><main class="wrap hero"><div class="eyebrow">Fallback route</div><h1 class="headline">{title}<br><i>preserved route.</i></h1><p class="subhead">This fallback keeps navigation complete. Replace with the richer preserved page when available.</p><div class="actions"><a class="btn" href="autonomous-mission-studio.html">Run end-to-end demo</a><a class="btn ghost" href="site-map.html">Open all pages</a></div></main></body></html>''', encoding='utf-8')
        created.append(str(p))
# inject a small route strip into existing html pages without deleting content
strip='''<div style="position:fixed;left:16px;bottom:16px;z-index:50;display:flex;gap:8px;flex-wrap:wrap"><a href="autonomous-mission-studio.html" style="font:800 12px system-ui;padding:9px 12px;border-radius:999px;background:#eefa76;color:#061018;text-decoration:none">Run end-to-end demo</a><a href="ask-goalos.html" style="font:800 12px system-ui;padding:9px 12px;border-radius:999px;background:#78ffd8;color:#061018;text-decoration:none">Ask GoalOS</a><a href="site-map.html" style="font:800 12px system-ui;padding:9px 12px;border-radius:999px;background:rgba(255,255,255,.18);color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.2)">All Pages</a></div>'''
for p in PUBLIC.glob('*.html'):
    try: html=p.read_text(encoding='utf-8')
    except Exception: continue
    if 'autonomous-mission-studio.html' not in html and '</body>' in html:
        p.write_text(html.replace('</body>', strip+'</body>'), encoding='utf-8')
# add homepage callout without overwriting if possible
idx=PUBLIC/'index.html'
if idx.exists():
    html=idx.read_text(encoding='utf-8')
    call='''<section style="margin:28px auto;padding:24px;border:1px solid rgba(120,255,216,.35);border-radius:24px;background:rgba(255,255,255,.08);max-width:1100px"><p style="letter-spacing:.22em;color:#fff36f;font-weight:900;text-transform:uppercase">New end-to-end demo</p><h2 style="font-size:clamp(36px,5vw,72px);line-height:.9;margin:0 0 12px;color:#fff">One objective → agents → proof → validation → Chronicle.</h2><p style="color:#d6e2f0;font:500 18px/1.5 system-ui">A non-technical user can now run the full GoalOS proof path in the browser.</p><a href="autonomous-mission-studio.html" style="display:inline-block;margin-top:8px;padding:13px 18px;border-radius:999px;background:linear-gradient(135deg,#fff26c,#65ffd5);color:#051014;text-decoration:none;font-weight:900">Run the autonomous mission demo</a></section>'''
    if 'One objective → agents → proof → validation → Chronicle' not in html:
        if '</main>' in html: html=html.replace('</main>', call+'</main>',1)
        elif '</body>' in html: html=html.replace('</body>', call+'</body>',1)
        else: html+=call
        idx.write_text(html, encoding='utf-8')
# search index
routes=[]
for p in sorted(PUBLIC.glob('*.html')):
    try: h=p.read_text(encoding='utf-8')
    except Exception: h=''
    title=(re.search(r'<title>(.*?)</title>',h,re.I|re.S) or [None,p.stem.replace('-',' ').title()])[1]
    routes.append({'title':re.sub('<.*?>','',title).strip(),'url':p.name,'category':'GoalOS public route','description':'GoalOS route preserved and searchable.'})
(PUBLIC/'search-index.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{r["url"]}</loc></url>' for r in routes)+'\n</urlset>\n',encoding='utf-8')
# nav metadata
content=ROOT/'content/goalos'; content.mkdir(parents=True, exist_ok=True)
(content/'public-proof-navigation-v40.json').write_text(json.dumps({'version':VERSION,'primary':'autonomous-mission-studio.html','routes':routes},indent=2),encoding='utf-8')
(content/'demo-ecosystem-registry-v40.json').write_text(json.dumps({'version':VERSION,'demo':'GoalOS Autonomous Mission Studio','primary':'autonomous-mission-studio.html','outputs':['Mission Contract','AGI Job Spec','AGI Node Handoff','ProofBundle','Evidence Docket Plan','Validation Certificate','Reviewer Brief','Action Graph','Chronicle Entry']},indent=2),encoding='utf-8')
# audit
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in (PUBLIC/'assets').glob('*v40*.js'):
    txt=p.read_text(encoding='utf-8')
    for f in forbidden:
        if f in txt: hits.append({'file':str(p),'token':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', txt):
        if href.startswith('http') or href.startswith('mailto:'): continue
        if not (PUBLIC/href.split('#')[0]).exists(): broken.append({'source':p.name,'href':href})
reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
status='passed' if not hits and not broken else 'needs_review'
report={'version':VERSION,'status':status,'createdFallbacks':created,'publicPages':len(list(PUBLIC.glob('*.html'))),'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
for name in ['install-report','qa','route-health']:
    (reports/f'autonomous-mission-studio-v40-{name}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
# evidence docket
ed=ROOT/'evidence/demo'; ed.mkdir(parents=True, exist_ok=True)
(ed/'autonomous-mission-studio-v40-reference-docket.json').write_text(json.dumps({'version':VERSION,'status':status,'claimBoundary':'public-safe browser-local demo; no AGI/ASI/SOTA claim','primary':'public/autonomous-mission-studio.html'},indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if hits or broken:
    raise SystemExit(2)
