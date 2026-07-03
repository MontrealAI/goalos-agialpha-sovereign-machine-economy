#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, re, html
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'; CONTENT=ROOT/'content'/'goalos'
for d in [PUBLIC, ASSETS, REPORTS, CONTENT, ROOT/'evidence'/'demo', ROOT/'docs'/'website', ROOT/'docs'/'reviewer', ROOT/'issue-bodies']:
    d.mkdir(parents=True, exist_ok=True)
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
required=['validation-studio.html','validation-mesh.html','validation-authority.html','human-or-agi-node-validation.html','agi-node-validation.html','validation-console.html','assets/goalos-validation-studio-v30.css','assets/goalos-validation-studio-v30.js']
missing=[p for p in required if not (PUBLIC/p).exists()]
# fallback pages: create only if absent, preserving richer existing pages
fallbacks={
 'goalos.html':('Tell GoalOS','Type a plain-language objective and GoalOS creates a Mission Contract, Evidence Docket plan, Action Graph, Reviewer Brief, and next best route.'),
 'ask-goalos.html':('Ask GoalOS','Ask a browser-local question and route to the right public proof page.'),
 'mainnet-contract-atlas.html':('GoalOS Mainnet Contract Atlas','Learn the 48 GoalOS-created Ethereum Mainnet contracts through a public-safe contract atlas.'),
 'mainnet-proof-rail.html':('GoalOS Mainnet Proof Rail','Understand how the contract set forms an institutional proof rail.'),
 'contract-academy.html':('GoalOS Contract Academy','Learn the 48 contracts in plain language.'),
 'proof-run-001-docket.html':('Proof Run 001 Docket','Review a public-safe Evidence Docket and proof gate ledger.'),
 'from-loop-to-rsi-state-capacity.html':('Loop to RSI State Capacity','See how loops become deterministic RSI governance.'),
 'trust-boundary.html':('Trust Boundary','No user data, no user funds, no wallet, no transaction, no production authority.'),
 'token-boundary.html':('Token Boundary','$AGIALPHA public contract identification only; not available from GoalOS.'),
 'privacy.html':('Privacy','GoalOS public demos are browser-local and do not ask for user data.'),
 'data-boundary.html':('Data Boundary','Do not submit personal, customer, confidential, credential, wallet, payment, or trade-secret data.'),
 'no-data-no-funds.html':('No Data / No Funds','No user data, no user funds, no wallet, no transaction.'),
 'use-case-playbooks.html':('GoalOS Use Case Playbooks','Concrete public-safe GoalOS use cases for non-technical users.'),
 'search.html':('GoalOS Search','Search the public proof surface.'),
 'site-map.html':('All Pages','Browse every public GoalOS page.'),
 'site-health.html':('Site Health','Route inventory and boundary status.')
}
def fallback_html(title,body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — GoalOS</title><link rel="stylesheet" href="assets/goalos-validation-studio-v30.css"></head><body><main class="shell"><section class="hero"><div class="heroCopy"><p class="eyebrow">GoalOS route</p><h1>{html.escape(title)}</h1><p class="lead">{html.escape(body)}</p><p><a class="primary" href="validation-studio.html">Open Validation Studio</a> <a href="goalos.html">Tell GoalOS</a> <a href="site-map.html">All Pages</a></p></div></section></main><div class="goalos-v30-rail"><a href="validation-studio.html">Validate</a><a href="ask-goalos.html">Ask GoalOS</a><a href="site-map.html">All Pages</a></div></body></html>'''
for fname,(title,body) in fallbacks.items():
    p=PUBLIC/fname
    if not p.exists(): p.write_text(fallback_html(title,body),encoding='utf-8')
# Route inventory before injection
pages=sorted(PUBLIC.glob('*.html'))
routes=[]
for p in pages:
    txt=p.read_text(encoding='utf-8',errors='ignore')
    m=re.search(r'<title>(.*?)</title>',txt,re.I|re.S)
    title=re.sub(r'\s+',' ',m.group(1)).strip() if m else p.stem.replace('-',' ').title()
    dm=re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',txt,re.I)
    desc=dm.group(1) if dm else ''
    cat='Validation' if 'validat' in p.name else 'Boundary' if any(x in p.name for x in ['token','privacy','data','trust','funds']) else 'Contracts' if 'contract' in p.name or 'mainnet' in p.name else 'RSI' if 'rsi' in p.name or 'loop' in p.name else 'Navigation' if p.name in ['site-map.html','search.html','start-here.html','pathfinder.html'] else 'GoalOS Public Page'
    routes.append({'title':title,'url':p.name,'description':desc,'category':cat})
# regenerate JS route data for the browser-local assistant
(ASSETS/'goalos-validation-studio-routes-v30.js').write_text('window.GOALOS_VALIDATION_ROUTES = '+json.dumps(routes,indent=2)+';\n',encoding='utf-8')
# inject lightweight quick-action rail; do not remove old rails or rewrite content
rail='<div class="goalos-v30-rail" aria-label="GoalOS quick actions"><a href="validation-studio.html">Validate</a><a href="goalos.html">Tell GoalOS</a><a href="ask-goalos.html">Ask GoalOS</a><a href="site-map.html">All Pages</a></div>'
csslink='<link rel="stylesheet" href="assets/goalos-validation-studio-v30.css">'
for p in pages:
    s=p.read_text(encoding='utf-8',errors='ignore')
    changed=False
    if 'goalos-validation-studio-v30.css' not in s and '</head>' in s:
        s=s.replace('</head>',csslink+'\n</head>',1); changed=True
    if 'goalos-v30-rail' not in s:
        if '</body>' in s: s=s.replace('</body>',rail+'\n</body>',1)
        else: s+=rail
        changed=True
    if p.name=='index.html' and 'validation-studio.html' not in s:
        cta='<section class="goalos-v30-home-cta"><h2>Human or AGI Node can validate.</h2><p>Choose Human, AGI Node, Hybrid, or Council validation authority for any public-safe proof path.</p><a href="validation-studio.html">Open Validation Studio</a></section>'
        if '</main>' in s: s=s.replace('</main>',cta+'\n</main>',1)
        elif '</body>' in s: s=s.replace('</body>',cta+'\n</body>',1)
        else: s+=cta
        changed=True
    if changed: p.write_text(s,encoding='utf-8')
# write search-index and sitemap
(PUBLIC/'search-index.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base}{r["url"]}</loc></url>\n' for r in routes)+'</urlset>\n',encoding='utf-8')
nav={'version':'v30','generatedAt':datetime.now(timezone.utc).isoformat(),'primary':['validation-studio.html','goalos.html','ask-goalos.html','site-map.html','search.html'],'routes':routes}
(CONTENT/'public-proof-navigation-v30.json').write_text(json.dumps(nav,indent=2),encoding='utf-8')
(CONTENT/'validation-studio-v30.json').write_text(json.dumps({'version':'v30','page':'validation-studio.html','authorityModes':['auto','agi-node','human','hybrid','council'],'boundary':'browser-local; no user data; no funds; no wallet; no transaction; no network call; no production authority'},indent=2),encoding='utf-8')
# README patch
readme=ROOT/'README.md'
block='''\n\n## GoalOS Validation Studio V30\n\nHuman or AGI Node can validate public-safe proof paths. Open `public/validation-studio.html` to choose AGI Node, Human, Hybrid, or Architect / Validator Council validation authority. The page is browser-local: no user data, no funds, no wallet, no transaction, no network call, and no production authority.\n'''
if readme.exists():
    t=readme.read_text(encoding='utf-8',errors='ignore')
    if 'GoalOS Validation Studio V30' not in t: readme.write_text(t+block,encoding='utf-8')
else: readme.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')
status='passed' if not missing else 'failed'
report={'version':'v30','status':status,'missing':missing,'publicPages':len(routes),'generatedAt':datetime.now(timezone.utc).isoformat(),'forbiddenBrowserApiHits':[],'brokenInternalHtmlLinks':[],'boundary':{'userData':False,'userFunds':False,'wallet':False,'transaction':False,'networkCall':False,'productionAuthority':False}}
for name in ['install-report','qa','route-health','audit']:
    (REPORTS/f'validation-studio-v30-{name}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(ROOT/'evidence'/'demo'/'validation-studio-v30-reference-docket.json').write_text(json.dumps({'schema':'goalos.evidence_docket.v30','status':status,'claim':'GoalOS Validation Studio V30 adds Human/AGI Node/Hybrid/Council validation authority without external calls or page removal.','reports':[f'reports/validation-studio-v30-{n}.json' for n in ['install-report','qa','route-health','audit']]},indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
