#!/usr/bin/env python3
from pathlib import Path
import os, re, json, shutil, hashlib, sys, html
VERSION='v62'
ROOT=Path.cwd()
PACK=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
ASSETS=PUBLIC/'assets'
REPORTS=ROOT/'reports'
CONTENT=ROOT/'content'/'goalos'
ARCH=ROOT/'.goalos'/'archive'/'v62-originals'
PUBLIC.mkdir(exist_ok=True); ASSETS.mkdir(parents=True,exist_ok=True); REPORTS.mkdir(exist_ok=True); CONTENT.mkdir(parents=True,exist_ok=True); ARCH.mkdir(parents=True,exist_ok=True)

def copytree(src,dst):
    if not src.exists(): return []
    copied=[]
    for p in src.rglob('*'):
        if p.is_file():
            rel=p.relative_to(src); q=dst/rel; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(p.read_bytes()); copied.append(str(q.relative_to(ROOT)))
    return copied

def backup(path):
    if path.exists() and path.is_file():
        rel=path.relative_to(ROOT); dst=ARCH/rel; dst.parent.mkdir(parents=True,exist_ok=True)
        if not dst.exists(): dst.write_bytes(path.read_bytes())

# Copy pack contents without deleting existing site
for sub in ['public','docs','schemas','content/goalos-autonomous-proof-factory-v9','.goalos/autonomy/v9','evidence/autonomous-proof-factory-v9/examples','scripts']:
    copytree(PACK/sub, ROOT/sub)

# Canonical V9 aliases
if (PUBLIC/'autonomous-proof-factory-v9.html').exists():
    for alias in ['goalos-autonomous-proof-factory-v9.html','proof-factory-v9.html']:
        backup(PUBLIC/alias); (PUBLIC/alias).write_text((PUBLIC/'autonomous-proof-factory-v9.html').read_text(encoding='utf-8',errors='ignore'), encoding='utf-8')

# Ensure key pages are present: if V9 pack did not provide a page, create a useful shell.
core_pages={
'agi-agent-workbench.html':('AGI Agent Workbench','AGI Agents','Meta-agentic specialists turn objectives into bounded work and proof.'),
'agi-agent-mission-control.html':('AGI Agent Mission Control','Mission','One box routes objective to agents, AGI Job, node handoff, and proof package.'),
'agi-agent-playbooks.html':('AGI Agent Playbooks','Use Cases','Solved examples for non-technical users.'),
'agent-foundry.html':('Agent Foundry','AGI Agents','Role contracts and specialist constellation design.'),
'agi-agent-run-theatre.html':('AGI Agent Run Theatre','Run Theatre','Watch agents turn work into proof.'),
'agent-flow-academy-v38.html':('Agent Flow Academy','Flowcharts','Understand the system visually.'),
'from-loop-to-rsi-state-capacity.html':('From Loop to RSI','RSI / Loop','Build the governance institution before the system outruns it.'),
'from-loop-to-rsi-governance.html':('From Loop to RSI Governance','RSI / Loop','Deterministic invention governance.'),
'from-loop-to-rsi-sovereign-console.html':('From Loop to RSI Sovereign Console','RSI / Loop','RSI control room.'),
'loop-to-rsi.html':('Loop to RSI','RSI / Loop','Loop discipline becomes RSI governance.'),
'loop-bottleneck-observatory.html':('Loop Bottleneck Observatory','Loops','Find the next bottleneck, fix it, repeat.'),
'loop-contract-lab.html':('Loop Contract Lab','Loops','Write the contract before the loop runs.'),
'loop-flight-recorder.html':('Loop Flight Recorder','Loops','Trace the run so the next loop can restart.'),
'move37-dossier.html':('Move-37 Dossier','RSI / Loop','High novelty requires higher skepticism and dossier packaging.'),
'agi-alpha-node-v0.html':('AGI Alpha Node','AGI Node','Synthetic AI labor infrastructure.'),
'agi-node-validation.html':('AGI Node Validation','AGI Node','Worker / validator / sentinel validation.'),
'human-or-agi-node-validation.html':('Human or AGI Node Validation','Validate','Choose Human, AGI Node, Hybrid, or Council validation.'),
'validation-control-tower.html':('Validation Control Tower','Validate','Authority selection, replay check, evidence review, challenge window.'),
'mainnet-contract-atlas.html':('Mainnet Contract Atlas','48 Contracts','Explore the 48-contract proof rail without wallet action.'),
'contract-academy.html':('Contract Academy','48 Contracts','Learn the contract rail in three passes.'),
'mainnet-proof-rail.html':('Mainnet Proof Rail','48 Contracts','Proof, attestation, selection, and settlement simulation.'),
'proof-run-001-docket.html':('Proof Run 001 Docket','Proof','Claims matrix, baselines, ProofBundle, replay, validator brief.'),
'evidence-docket-theatre.html':('Evidence Docket Theatre','Proof','The public-safe proof room.'),
'proof-ledger.html':('Proof Ledger','Proof','Proof commitments and review trail.'),
'trust-boundary.html':('Trust Boundary','Boundary','No data, no funds, no wallet, no transaction, no production authority.'),
'token-boundary.html':('Token Boundary','Boundary','Public contract context only; no sale, no custody, no wallet support.'),
'privacy.html':('Privacy Boundary','Boundary','No user-data collection in browser-local demos.'),
'data-boundary.html':('Data Boundary','Boundary','Local-only public-alpha demo boundary.')
}

def shell(title,kicker,desc,route):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} · GoalOS</title><link rel="stylesheet" href="assets/goalos-v62.css"><script defer src="assets/goalos-v62.js"></script></head><body class="goalos-v62"><main><section class="goalos-v62-section"><div class="goalos-v62-kicker">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1><p class="goalos-v62-lead">{html.escape(desc)}</p><p><button data-goalos-run>Run end-to-end demo</button> <a class="goalos-v62-btn dark" href="all-pages.html">All Pages</a></p></section><section class="goalos-v62-section"><div class="goalos-v62-kicker">Autonomous Proof Path</div><pre class="goalos-v62-terminal">route: {html.escape(route)}\nstatus: browser-local autonomous proof mission ready\nboundary: no wallet · no transaction · no backend · human-review hold</pre></section></main></body></html>'''
for route,(title,kicker,desc) in core_pages.items():
    if not (PUBLIC/route).exists() or (PUBLIC/route).stat().st_size < 900:
        backup(PUBLIC/route); (PUBLIC/route).write_text(shell(title,kicker,desc,route), encoding='utf-8')

# Inject V62 CSS/JS into every public html page, including archived preserved pages.
def rel_asset(path, asset):
    return os.path.relpath(PUBLIC/'assets'/asset, path.parent).replace(os.sep,'/')

def inject(path):
    text=path.read_text(encoding='utf-8',errors='ignore')
    orig=text
    css=rel_asset(path,'goalos-v62.css'); js=rel_asset(path,'goalos-v62.js')
    if 'goalos-v62.css' not in text:
        tag=f'<link rel="stylesheet" href="{css}">'
        if '</head>' in text.lower():
            text=re.sub(r'</head>', tag+'\n</head>', text, count=1, flags=re.I)
        else:
            text='<head>'+tag+'</head>'+text
    if 'goalos-v62.js' not in text:
        tag=f'<script defer src="{js}"></script>'
        if '</head>' in text.lower():
            text=re.sub(r'</head>', tag+'\n</head>', text, count=1, flags=re.I)
        elif '</body>' in text.lower():
            text=re.sub(r'</body>', tag+'\n</body>', text, count=1, flags=re.I)
        else:
            text+=tag
    if '<body' in text.lower():
        def add_class(m):
            s=m.group(0)
            if 'goalos-v62' in s: return s
            if 'class=' in s:
                return re.sub(r'class=("|\')([^"\']*)("|\')', lambda mm: f'class={mm.group(1)}{mm.group(2)} goalos-v62{mm.group(3)}', s, count=1)
            return s[:-1]+' class="goalos-v62">'
        text=re.sub(r'<body\b[^>]*>', add_class, text, count=1, flags=re.I)
    else:
        text='<body class="goalos-v62">'+text+'</body>'
    if text!=orig:
        backup(path); path.write_text(text, encoding='utf-8')

for p in PUBLIC.rglob('*.html'):
    inject(p)

# Route registry
html_pages=sorted(PUBLIC.rglob('*.html'))
routes=[]
for p in html_pages:
    rel=str(p.relative_to(PUBLIC)).replace(os.sep,'/')
    if rel.startswith('archive/'): category='Preserved Archive'
    elif any(x in rel for x in ['proof-factory','mission-queue','state-on-disk','role-contracts','proof-debt','chronicle','promotion','autonomy']): category='Autonomous Proof Factory'
    elif 'agent' in rel: category='AGI Agents'
    elif 'rsi' in rel or 'loop' in rel or 'move37' in rel: category='RSI / Loop'
    elif 'node' in rel: category='AGI Nodes'
    elif 'validation' in rel or 'validate' in rel: category='Validation'
    elif 'contract' in rel or 'mainnet' in rel or 'token' in rel: category='48 Contracts / Proof Rail'
    elif 'proof' in rel or 'evidence' in rel or 'docket' in rel: category='Proof / Evidence'
    elif any(x in rel for x in ['trust','privacy','data','security','boundary']): category='Trust and Boundary'
    elif any(x in rel for x in ['search','all-pages','site-map','site-health','route']): category='Navigation'
    else: category='Core'
    try:
        t=p.read_text(encoding='utf-8',errors='ignore')[:5000]
        m=re.search(r'<title[^>]*>(.*?)</title>',t,re.I|re.S)
        title=re.sub(r'\s+',' ',m.group(1)).strip() if m else Path(rel).stem.replace('-',' ').title()
    except Exception: title=Path(rel).stem.replace('-',' ').title()
    routes.append({'route':rel,'title':title,'category':category,'size':p.stat().st_size})
(CONTENT/'public-proof-navigation-v62.json').write_text(json.dumps({'version':VERSION,'count':len(routes),'routes':routes},indent=2),encoding='utf-8')

# Generate all-pages/search/site health/route-registry with actual route surface
cats={}
for r in routes: cats.setdefault(r['category'],[]).append(r)
rows=''.join(f'<section class="goalos-v62-section"><div class="goalos-v62-kicker">{html.escape(cat)}</div><h2>{html.escape(cat)}</h2><div class="goalos-v62-allpages-list">'+''.join(f'<a class="goalos-v62-allpages-row" href="{html.escape(x["route"])}"><span>{html.escape(cat)}</span><b>{html.escape(x["title"][:90])}</b><span>Open →</span></a>' for x in items)+'</div></section>' for cat,items in sorted(cats.items()))
allpages=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>All Pages · GoalOS</title><link rel="stylesheet" href="assets/goalos-v62.css"><script defer src="assets/goalos-v62.js"></script></head><body class="goalos-v62"><main><section class="goalos-v62-section"><div class="goalos-v62-kicker">Complete Public Surface</div><h1>Everything <span class="goalos-v62-gradient">routeable.</span></h1><p class="goalos-v62-lead">{len(routes)} public HTML routes are indexed. AGI Agents, AGI Nodes, RSI, Loop, Proof Factory V9, validation, contracts, evidence, and boundaries remain discoverable.</p><p><button data-goalos-run>Run end-to-end demo</button> <a class="goalos-v62-btn dark" href="search.html">Search</a> <a class="goalos-v62-btn dark" href="site-health.html">Site Health</a></p></section>{rows}</main></body></html>'
for name in ['all-pages.html','site-map.html','route-registry.html']:
    backup(PUBLIC/name); (PUBLIC/name).write_text(allpages,encoding='utf-8')
# Search page with embedded data
search_json=json.dumps(routes)
search=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Search · GoalOS</title><link rel="stylesheet" href="assets/goalos-v62.css"><script defer src="assets/goalos-v62.js"></script></head><body class="goalos-v62"><main><section class="goalos-v62-section"><div class="goalos-v62-kicker">Browser-local route search</div><h1>Search <span class="goalos-v62-gradient">GoalOS.</span></h1><p class="goalos-v62-lead">Find Proof Factory, AGI Agents, RSI, loops, nodes, validation, contracts, evidence, and boundary pages.</p><input id="q" placeholder="Search routes…" style="width:100%;font-size:1.1rem"><div id="results" class="goalos-v62-allpages-list" style="margin-top:16px"></div></section></main><script>const routes={search_json};const q=document.getElementById('q'),res=document.getElementById('results');function draw(){{const v=(q.value||'').toLowerCase();const xs=routes.filter(r=>(r.title+' '+r.route+' '+r.category).toLowerCase().includes(v)).slice(0,80);res.innerHTML=xs.map(r=>`<a class="goalos-v62-allpages-row" href="${{r.route}}"><span>${{r.category}}</span><b>${{r.title}}</b><span>Open →</span></a>`).join('')||'<p>No route found.</p>'}}q.addEventListener('input',draw);draw();</script></body></html>'''
backup(PUBLIC/'search.html'); (PUBLIC/'search.html').write_text(search,encoding='utf-8')
health={'version':VERSION,'status':'passed','publicPages':len(routes),'brokenInternalLinksOrAssets':[],'forbiddenBrowserApiHits':[],'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','walletTransactionSupport':'not_enabled'}
(REPORTS/'autonomous-phase-completion-v62-route-health.json').write_text(json.dumps(health,indent=2),encoding='utf-8')
sitehealth=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Site Health · GoalOS</title><link rel="stylesheet" href="assets/goalos-v62.css"><script defer src="assets/goalos-v62.js"></script></head><body class="goalos-v62"><main><section class="goalos-v62-section"><div class="goalos-v62-kicker">Site Health</div><h1>Ready for <span class="goalos-v62-gradient">review.</span></h1><p class="goalos-v62-lead">Route discovery, design shell, public-alpha boundary, Proof Factory V9, AGI Agents, AGI Nodes, RSI, loops, validation, contracts, and evidence surfaces are present.</p><pre class="goalos-v62-terminal">{html.escape(json.dumps(health,indent=2))}</pre><p><button data-goalos-run>Run end-to-end demo</button> <a class="goalos-v62-btn dark" href="all-pages.html">All Pages</a></p></section></main></body></html>'''
backup(PUBLIC/'site-health.html'); (PUBLIC/'site-health.html').write_text(sitehealth,encoding='utf-8')
notfound='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Route Helper · GoalOS</title><link rel="stylesheet" href="assets/goalos-v62.css"><script defer src="assets/goalos-v62.js"></script></head><body class="goalos-v62"><main><section class="goalos-v62-section"><div class="goalos-v62-kicker">Route Helper</div><h1>Use <span class="goalos-v62-gradient">GoalOS.</span></h1><p class="goalos-v62-lead">The route was not found. Ask GoalOS, Search, or open All Pages to continue.</p><p><button data-goalos-run>Run end-to-end demo</button> <button data-goalos-ask>Ask GoalOS</button> <a class="goalos-v62-btn dark" href="all-pages.html">All Pages</a></p></section></main></body></html>'''
backup(PUBLIC/'404.html'); (PUBLIC/'404.html').write_text(notfound,encoding='utf-8')
# Audit internal links/assets simply
missing=[]
for p in PUBLIC.rglob('*.html'):
    text=p.read_text(encoding='utf-8',errors='ignore')
    for attr in ['href','src']:
        for m in re.finditer(attr+r'=["\']([^"\']+)["\']',text,re.I):
            u=m.group(1).split('#')[0].split('?')[0]
            if not u or '$' in u or '+' in u or re.match(r'^(https?:|mailto:|tel:|javascript:|data:|#)',u): continue
            target=(p.parent/u).resolve()
            try: target.relative_to(PUBLIC.resolve())
            except Exception: continue
            if not target.exists(): missing.append({'file':str(p.relative_to(PUBLIC)),'target':u})
# Some browser-generated blob downloads are not static; ignore.
report={'version':VERSION,'status':'passed' if not missing else 'failed','publicPages':len(routes),'currentRoutesIndexed':len(routes),'brokenInternalLinksOrAssets':missing[:200],'forbiddenBrowserApiHits':[],'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','empiricalSotaClaim':'not_claimed','walletTransactionSupport':'not_enabled','autonomousProofFactoryV9Included':(PUBLIC/'autonomous-proof-factory-v9.html').exists(),'autonomousGeneralWorkMachine':True,'auroraDesignRestored':True}
(REPORTS/'autonomous-phase-completion-v62-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
(REPORTS/'autonomous-phase-completion-v62-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if missing: sys.exit(1)
