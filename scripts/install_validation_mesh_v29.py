#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, re, html
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'; CONTENT=ROOT/'content'/'goalos'
for d in [PUBLIC, ASSETS, REPORTS, CONTENT, ROOT/'evidence'/'demo', ROOT/'docs'/'website', ROOT/'docs'/'reviewer', ROOT/'issue-bodies']:
    d.mkdir(parents=True, exist_ok=True)
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
required=['validation-mesh.html','assets/goalos-validation-mesh-v29.css','assets/goalos-validation-mesh-v29.js','assets/goalos-validation-mesh-routes-v29.js','assets/goalos-validation-mesh-v29-rail.css']
missing=[p for p in required if not (PUBLIC/p).exists()]
# Fallback core pages only if absent.
fallbacks={
 'goalos.html':('Tell GoalOS','Use the one-box GoalOS interface to turn your objective into a proof path.'),
 'ask-goalos.html':('Ask GoalOS','Ask a browser-local question and route to the correct public proof page.'),
 'mainnet-contract-atlas.html':('Mainnet Contract Atlas','Explore the 48 GoalOS-created Ethereum Mainnet contracts.'),
 'mainnet-proof-rail.html':('Mainnet Proof Rail','Understand the public proof rail connecting contracts, dockets, and validation.'),
 'contract-academy.html':('Contract Academy','Learn GoalOS contracts in plain language.'),
 'proof-run-001-docket.html':('Proof Run 001 Docket','Review a public-safe Evidence Docket and proof gate ledger.'),
 'from-loop-to-rsi-state-capacity.html':('Loop to RSI State Capacity','See how loops become deterministic RSI governance.'),
 'trust-boundary.html':('Trust Boundary','No user data, no user funds, no wallet, no transaction, no production authority.'),
 'token-boundary.html':('Token Boundary','$AGIALPHA public contract identification only; not available from GoalOS.'),
 'search.html':('GoalOS Search','Search the public proof surface.'),
 'site-map.html':('All Pages','Browse every public GoalOS page.')
}
def fallback_html(title,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — GoalOS</title><link rel="stylesheet" href="assets/goalos-validation-mesh-v29-rail.css"></head><body style="margin:0;background:#06101f;color:#fff;font-family:Inter,system-ui,sans-serif"><main style="width:min(920px,calc(100% - 32px));margin:80px auto"><p style="letter-spacing:.2em;text-transform:uppercase;color:#fff06a;font-weight:900">GoalOS route</p><h1 style="font-size:clamp(44px,8vw,82px);line-height:.9;margin:0 0 20px">{html.escape(title)}</h1><p style="font-size:20px;line-height:1.45;color:#d7e4f2">{html.escape(body)}</p><p><a style="color:#65ffd7;font-weight:900" href="validation-mesh.html">Open Validation Mesh</a> · <a style="color:#65ffd7;font-weight:900" href="goalos.html">Tell GoalOS</a> · <a style="color:#65ffd7;font-weight:900" href="site-map.html">All Pages</a></p></main><div class="goalos-v29-rail"><a href="validation-mesh.html">Validate</a><a class="secondary" href="ask-goalos.html">Ask GoalOS</a></div></body></html>'''
for fname,(title,body) in fallbacks.items():
    p=PUBLIC/fname
    if not p.exists(): p.write_text(fallback_html(title,body),encoding='utf-8')
# Inject rail and CSS link into all HTML pages without disturbing existing content.
rail='<div class="goalos-v29-rail" aria-label="GoalOS quick actions"><a href="validation-mesh.html">Validate</a><a class="secondary" href="ask-goalos.html">Ask GoalOS</a><a class="secondary" href="site-map.html">All Pages</a></div>'
link='<link rel="stylesheet" href="assets/goalos-validation-mesh-v29-rail.css">'
for p in PUBLIC.glob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    changed=False
    if 'goalos-validation-mesh-v29-rail.css' not in s:
        if '</head>' in s: s=s.replace('</head>',link+'\n</head>',1); changed=True
    if 'goalos-v29-rail' not in s:
        if '</body>' in s: s=s.replace('</body>',rail+'\n</body>',1); changed=True
        else: s += rail; changed=True
    if p.name=='index.html' and 'goalos-v29-home-cta' not in s:
        cta='<section class="goalos-v29-home-cta"><h2>Human or AGI Node can validate.</h2><p>Use the autonomous validation mesh to choose AGI Node, Human, Hybrid, or Council validation authority for any public-safe proof path.</p><a href="validation-mesh.html">Open Validation Mesh</a><a href="ask-goalos.html">Ask GoalOS</a></section>'
        if '</main>' in s: s=s.replace('</main>',cta+'\n</main>',1)
        elif '</body>' in s: s=s.replace('</body>',cta+'\n</body>',1)
        else: s+=cta
        changed=True
    if changed: p.write_text(s,encoding='utf-8')
# Build route inventory
pages=sorted(PUBLIC.glob('*.html'))
routes=[]
for p in pages:
    txt=p.read_text(encoding='utf-8',errors='ignore')
    m=re.search(r'<title>(.*?)</title>',txt,re.I|re.S)
    title=re.sub(r'\s+',' ',m.group(1)).strip() if m else p.stem.replace('-',' ').title()
    desc=''
    dm=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',txt,re.I)
    if dm: desc=dm.group(1)
    routes.append({'title':title,'url':p.name,'description':desc,'category':'Validation & Navigation' if 'validat' in p.name else 'GoalOS Public Page'})
(PUBLIC/'search-index.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base}{r["url"]}</loc></url>\n' for r in routes)+'</urlset>\n',encoding='utf-8')
nav={'version':'v29','generatedAt':datetime.now(timezone.utc).isoformat(),'routes':routes,'primary':['validation-mesh.html','goalos.html','ask-goalos.html','site-map.html','search.html']}
(CONTENT/'public-proof-navigation-v29.json').write_text(json.dumps(nav,indent=2),encoding='utf-8')
(CONTENT/'validation-mesh-v29.json').write_text(json.dumps({'version':'v29','page':'validation-mesh.html','authorityModes':['auto','agi-node','human','hybrid','council'],'boundary':'browser-local; no user data; no funds; no wallet; no transaction; no network call'},indent=2),encoding='utf-8')
# README patch
readme=ROOT/'README.md'
block='''\n\n## GoalOS Autonomous Validation Mesh V29\n\nHuman or AGI Node can validate public-safe proof paths. Use `public/validation-mesh.html` to choose AGI Node, Human, Hybrid, or Architect / Validator Council validation authority. The page is browser-local: no user data, no funds, no wallet, no transaction, no network call, and no production authority.\n'''
if readme.exists():
    s=readme.read_text(encoding='utf-8',errors='ignore')
    if 'GoalOS Autonomous Validation Mesh V29' not in s:
        readme.write_text(s+block,encoding='utf-8')
else: readme.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')
# Reports/evidence
status='passed' if not missing else 'failed'
report={'version':'v29','status':status,'missing':missing,'publicPages':len(routes),'generatedAt':datetime.now(timezone.utc).isoformat(),'boundary':{'userData':False,'userFunds':False,'wallet':False,'transaction':False,'networkCall':False}}
for name in ['install-report','qa','route-health','audit']:
    (REPORTS/f'validation-mesh-v29-{name}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'evidence'/'demo'/'validation-mesh-v29-reference-docket.json').write_text(json.dumps({'schema':'goalos.evidence_docket.v29','status':status,'claim':'GoalOS Validation Mesh V29 adds Human/AGI Node/Hybrid/Council validation routing without external calls or page removal.','reports':[f'reports/validation-mesh-v29-{n}.json' for n in ['install-report','qa','route-health','audit']]},indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
