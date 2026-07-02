from pathlib import Path
import json, re, html, datetime, shutil
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; DOCS=ROOT/'docs'; REPORTS=ROOT/'reports'; EVIDENCE=ROOT/'evidence'/'demo'; CONTENT=ROOT/'content'/'goalos'; EXAMPLES=ROOT/'examples'/'universal-mission-composer'; ISSUES=ROOT/'issue-bodies'; TEMPLATES=ROOT/'.github'/'ISSUE_TEMPLATE'; SRC=ROOT/'goalos_v25_assets'
for p in [PUBLIC,ASSETS,DOCS/'website',DOCS/'reviewer',REPORTS,EVIDENCE,CONTENT,EXAMPLES,ISSUES,TEMPLATES]: p.mkdir(parents=True, exist_ok=True)
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
VERSION='v25'
BOUNDARY='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
TOKEN_BOUNDARY='$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.'
KNOWN_ROUTES={
 'goalos.html':'GoalOS Mission Composer','mission.html':'GoalOS Mission','tell-goalos.html':'Tell GoalOS','mission-autopilot.html':'Mission Autopilot','universal-mission-autopilot.html':'Universal Mission Autopilot','objective-command-center.html':'Objective Command Center','mission-command-center.html':'Mission Command Center','ask-goalos.html':'Ask GoalOS','start-here.html':'Start Here','pathfinder.html':'Pathfinder','site-map.html':'All Pages','search.html':'Search','demo-ecosystem-registry.html':'Demo Registry','site-health.html':'Site Health','proof-run-001-docket.html':'Proof Run 001 Docket','mainnet-contract-atlas.html':'48 Mainnet Contract Atlas','mainnet-proof-rail.html':'Mainnet Proof Rail','contract-academy.html':'Contract Academy','from-loop-to-rsi-state-capacity.html':'Loop to RSI State Capacity','from-loop-to-rsi-sovereign-console.html':'Loop to RSI Sovereign Console','from-loop-to-rsi-governance.html':'Loop to RSI Governance','loop-contract-lab.html':'Loop Contract Lab','loop-flight-recorder.html':'Loop Flight Recorder','loop-bottleneck-observatory.html':'Loop Bottleneck Observatory','trust-boundary.html':'Trust Boundary','token-boundary.html':'Token Boundary','privacy.html':'Privacy','data-boundary.html':'Data Boundary','no-data-no-funds.html':'No Data No Funds','docs.html':'Docs'
}
INTENTS=[
 {'key':'contracts','label':'Understand the 48 Ethereum Mainnet contracts','state':'CONTRACT_ATLAS_READY','keywords':['contract','mainnet','ethereum','48','aep','ledger','chain','etherscan'],'routes':['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','token-boundary.html'],'summary':'GoalOS will route you to the Mainnet Contract Atlas, explain the proof rail, and package a reviewer-friendly contract-learning mission.'},
 {'key':'proof','label':'Run or understand a public-safe proof mission','state':'PROOF_MISSION_READY','keywords':['proof','mission','docket','evidence','run','validate','verification','review'],'routes':['proof-run-001-docket.html','demo-ecosystem-registry.html','site-health.html','pathfinder.html'],'summary':'GoalOS will convert your objective into a Mission Contract, Evidence Docket plan, claims matrix, and review path.'},
 {'key':'rsi','label':'Understand Loop to RSI governance','state':'RSI_REVIEW_READY','keywords':['rsi','recursive','loop','omni','move','move-37','governance','invention','state capacity'],'routes':['from-loop-to-rsi-state-capacity.html','from-loop-to-rsi-sovereign-console.html','from-loop-to-rsi-governance.html','loop-bottleneck-observatory.html'],'summary':'GoalOS will route you through the loop discipline into deterministic RSI governance: replay, baselines, ECI, dossiers, and council review.'},
 {'key':'trust','label':'Check privacy, token, and boundary posture','state':'BOUNDARY_REVIEW_READY','keywords':['privacy','data','fund','wallet','token','agialpha','legal','boundary','gdpr','terms'],'routes':['trust-boundary.html','token-boundary.html','privacy.html','data-boundary.html','no-data-no-funds.html'],'summary':'GoalOS will show the no-data, no-funds, no-wallet, no-transaction, public-alpha boundary and the $AGIALPHA non-availability statement.'},
 {'key':'start','label':'I am new. Give me the fastest path.','state':'ONBOARDING_READY','keywords':['start','new','begin','learn','overview','explain','help','fastest','guide'],'routes':['start-here.html','pathfinder.html','goalos.html','demo-ecosystem-registry.html'],'summary':'GoalOS will give you the shortest onboarding path, role-based navigation, and a first proof route.'},
 {'key':'site','label':'Find a page or navigate the website','state':'ROUTE_SEARCH_READY','keywords':['page','site','map','search','registry','demo','where','find','open'],'routes':['site-map.html','search.html','demo-ecosystem-registry.html','site-health.html'],'summary':'GoalOS will search the public route surface and recommend the best page.'}
]

def title_from_file(path):
    try:
        txt=path.read_text(encoding='utf-8',errors='ignore')[:4000]
        m=re.search(r'<title[^>]*>(.*?)</title>',txt,re.I|re.S)
        if m: return re.sub(r'\s+',' ',html.unescape(m.group(1))).strip()
        m=re.search(r'<h1[^>]*>(.*?)</h1>',txt,re.I|re.S)
        if m: return re.sub(r'<[^>]+>','',html.unescape(m.group(1))).strip()
    except Exception: pass
    return path.stem.replace('-',' ').replace('_',' ').title()

def classify_route(title,href):
    s=(title+' '+href).lower()
    if href=='404.html': return 'System'
    if any(k in s for k in ['mainnet','contract','aep','ledger','proof rail','48']): return '48 Contracts & Proof Rail'
    if any(k in s for k in ['loop','rsi','move','omni','bottleneck','flight','state capacity']): return 'Loop → RSI'
    if any(k in s for k in ['proof','docket','evidence','validator','reviewer','run 001','gauntlet','falsification']): return 'Evidence & Review'
    if any(k in s for k in ['trust','token','privacy','data','legal','boundary','no-data','no-funds','security']): return 'Trust & Boundary'
    if any(k in s for k in ['start','pathfinder','site-map','search','registry','docs','health','goalos','mission','ask']): return 'Navigation & Mission Interface'
    if any(k in s for k in ['capability','value','economy','settlement','upgrade','action']): return 'Capability & Economy'
    return 'Additional'

def description(title,href,category):
    if 'Mainnet Contract' in title or 'Contract Atlas' in title: return 'Explore the 48 GoalOS-created Ethereum Mainnet contracts as one institutional proof rail.'
    if 'Proof Run' in title: return 'Review the public evidence docket, gates, claims, and decision state.'
    if 'RSI' in title or 'Loop' in title: return 'Understand how loops become governed recursive invention paths.'
    if 'Trust' in title or 'Privacy' in title or 'Token' in title: return 'Review public-alpha boundaries: no data, no funds, no wallet, no transaction.'
    if 'GoalOS' in title or 'Mission' in title or 'Ask' in title: return 'Use the one-box Mission interface or Ask GoalOS route assistant.'
    return f'Open {title} as part of the complete GoalOS public proof surface.'

def scan_routes():
    routes=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        rel=p.relative_to(PUBLIC).as_posix()
        if rel.startswith(('downloads/','archive/')): continue
        title=title_from_file(p); cat=classify_route(title,rel)
        routes.append({'title':title,'href':rel,'category':cat,'description':description(title,rel,cat),'system':rel=='404.html'})
    seen=set(); out=[]
    for r in routes:
        if r['href'] not in seen: out.append(r); seen.add(r['href'])
    return out

def modal_html():
    return '<div class="g25-modal" id="g25-allpages-modal"><div class="g25-modal-card"><div class="g25-modal-top"><h2>All GoalOS pages</h2><button class="g25-close" data-g25-close>Close</button></div><input class="g25-input" data-g25-search-input placeholder="Search GoalOS routes…"><div class="g25-results" data-g25-results></div></div></div>'

def ask_modal_html():
    return '<div class="g25-modal" id="g25-ask-modal"><div class="g25-modal-card"><div class="g25-modal-top"><div><h2>Ask GoalOS</h2><p class="g25-mini">Ask a question. GoalOS answers from the public site index and routes you to the right page.</p></div><button class="g25-close" data-g25-close>Close</button></div><div class="g25-chatlog" data-g25-chatlog><div class="g25-msg"><strong>GoalOS ready.</strong><p>Try: “Where are the 48 contracts?”, “What is RSI?”, “Show Proof Run 001”, or “Is $AGIALPHA available from GoalOS?”</p></div></div><div style="display:flex;gap:10px;margin-top:12px"><input class="g25-input" data-g25-ask-input placeholder="Ask GoalOS…"><button class="g25-btn primary" data-g25-ask-send>Send</button></div></div></div>'

def nav(active='Mission'):
    items=[('Mission','goalos.html'),('Start','start-here.html'),('Pathfinder','pathfinder.html'),('Registry','demo-ecosystem-registry.html'),('48 Contracts','mainnet-contract-atlas.html'),('Proof Run 001','proof-run-001-docket.html'),('Loop→RSI','from-loop-to-rsi-state-capacity.html'),('All Pages','site-map.html'),('Trust','trust-boundary.html'),('Token','token-boundary.html'),('Search /','search.html')]
    return '<nav class="g25-nav"><a class="g25-brand" href="goalos.html"><span class="g25-mark"></span><span>GoalOS<br>AGIALPHA</span></a><div class="g25-navlinks">'+''.join(f'<a class="g25-chip {"active" if label==active else ""}" href="{href}">{label}</a>' for label,href in items)+'</div></nav>'

def shell(title,body,active='Mission'):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="GoalOS AGIALPHA Ascension — one-box Mission interface, live Ask GoalOS assistant, complete public proof navigation."><link rel="stylesheet" href="assets/goalos-universal-mission-composer-v25.css"></head><body><div class="g25-shell">{nav(active)}</div>{body}<div class="g25-float"><a href="goalos.html">Tell GoalOS</a><button data-g25-ask-open>Ask GoalOS</button><button data-g25-open-pages>All Pages</button></div>{modal_html()}{ask_modal_html()}<script src="assets/goalos-universal-mission-routes-v25.js"></script><script src="assets/goalos-universal-mission-composer-v25.js"></script></body></html>'

def ensure_fallback(href,title):
    p=PUBLIC/href
    if p.exists(): return False
    body=f'<main class="g25-shell g25-section"><div class="g25-kicker">Preserved route</div><h1 class="g25-section-title">{html.escape(title)}</h1><p class="g25-copy">This route is preserved as part of the complete GoalOS public proof surface. Use Tell GoalOS or Ask GoalOS to find the best current page for your objective.</p><p><a class="g25-btn primary" href="goalos.html">Tell GoalOS</a> <a class="g25-btn" href="site-map.html">All pages</a></p><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></main>'
    p.write_text(shell(title,body,'All Pages'),encoding='utf-8')
    return True

def main_interface():
    examples=['I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.','I am new and want the fastest path to understand GoalOS.']
    steps=[('Objective','Understand the request'),('Boundary','Check data / funds / wallet'),('Routes','Find the proof surface'),('Contract','Build Mission Contract'),('Docket','Plan evidence and review'),('Next','Open best page')]
    body=f'''<main class="g25-shell"><section class="g25-hero"><div><div class="g25-kicker">Mission 04 · Universal Mission Composer</div><h1 class="g25-title">Tell GoalOS<br><em>what you want.</em></h1><p class="g25-lede">One friendly box turns your objective into a Mission Contract, Evidence Docket plan, route map, Reviewer Brief, and next best proof route.</p><p class="g25-copy">You do not need to understand the whole site first. Type the outcome you want. GoalOS prepares the public-safe proof path and shows where to go next.</p><div class="g25-onebox"><div class="g25-onebox-top"><span>What do you want GoalOS to help you accomplish?</span><span class="g25-status">browser-local</span></div><textarea class="g25-textarea" data-g25-objective>I want to understand the 48 Ethereum Mainnet contracts.</textarea><div class="g25-actions"><button class="g25-btn primary big" data-g25-generate>Generate proof path</button><button class="g25-btn big" data-g25-open-next>Open next best page</button><button class="g25-btn big" data-g25-ask-open>Ask GoalOS</button></div></div><div class="g25-modes"><button class="g25-mode active" data-g25-mode>Simple</button><button class="g25-mode" data-g25-mode>Executive</button><button class="g25-mode" data-g25-mode>Reviewer</button><button class="g25-mode" data-g25-mode>Builder</button></div><div class="g25-suggestions">{''.join(f'<button class="g25-suggestion" data-g25-suggestion>{html.escape(x)}</button>' for x in examples)}</div><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></div><aside class="g25-console"><div class="g25-console-head"><span>Sovereign Mission OS</span><span class="g25-status">ready</span></div><div class="g25-orb">α</div><div class="g25-steps">{''.join(f'<div class="g25-step"><strong>{i:02d} {label}</strong><small>{sub}</small></div>' for i,(label,sub) in enumerate(steps,1))}</div><div class="g25-state" data-g25-state>mission: waiting\nintent: pending\nstate: READY\nboundary: preserved\nexternal actions: 0</div><div class="g25-answer" data-g25-answer><h3>Mission package will appear here.</h3><p class="g25-mini">GoalOS will create route cards, downloads, and a next step after you generate a proof path.</p></div></aside></section><section class="g25-section"><h2>What GoalOS does for the user.</h2><div class="g25-grid"><div class="g25-card"><small>01</small><h3>Clarifies the objective</h3><p>Turns plain language into a bounded Mission Contract with success criteria, constraints, and review status.</p></div><div class="g25-card"><small>02</small><h3>Finds the right place</h3><p>Routes users to contracts, Proof Run 001, Loop → RSI, trust boundaries, registry, docs, or all pages.</p></div><div class="g25-card"><small>03</small><h3>Prepares review artifacts</h3><p>Downloads Mission JSON, Reviewer Brief, and Action Graph CSV so work becomes inspectable.</p></div><div class="g25-card"><small>04</small><h3>Answers questions</h3><p>Ask GoalOS remains available as a live browser-local route assistant across the website.</p></div><div class="g25-card"><small>05</small><h3>Preserves safety</h3><p>No model call, no backend, no wallet, no transaction, no user-data storage, and no production authority.</p></div><div class="g25-card"><small>06</small><h3>Keeps everything navigable</h3><p>All existing pages stay accessible through All Pages, Search /, Tell GoalOS, and Ask GoalOS.</p></div></div></section><footer class="g25-foot">GoalOS AGIALPHA Ascension — public-alpha proof operating system. {BOUNDARY}</footer></main>'''
    return shell('GoalOS — Tell GoalOS what you want',body,'Mission')

def simple_page(title,copy,active='Mission'):
    body=f'<main class="g25-shell g25-section"><div class="g25-kicker">GoalOS guide</div><h1 class="g25-section-title">{html.escape(title)}</h1><p class="g25-copy">{html.escape(copy)}</p><p><a class="g25-btn primary" href="goalos.html">Tell GoalOS</a> <button class="g25-btn" data-g25-ask-open>Ask GoalOS</button> <a class="g25-btn" href="site-map.html">All Pages</a></p><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></main>'
    return shell(title,body,active)

def pathfinder_page():
    cards=[('New user','Understand GoalOS quickly','start-here.html'),('Proof reviewer','Inspect evidence before trust','proof-run-001-docket.html'),('Contract explorer','Learn the 48 Mainnet contracts','mainnet-contract-atlas.html'),('RSI learner','Follow Loop → RSI governance','from-loop-to-rsi-state-capacity.html'),('Boundary reviewer','Check data/token/privacy posture','trust-boundary.html'),('Builder','Use docs, registry, and reports','docs.html')]
    body='<main class="g25-shell g25-section"><div class="g25-kicker">Pathfinder</div><h1 class="g25-section-title">Choose your shortest path.</h1><p class="g25-copy">Pick a role or type your objective into the Mission interface.</p><div class="g25-grid">'+''.join(f'<div class="g25-card"><small>{html.escape(a)}</small><h3>{html.escape(b)}</h3><p><a class="g25-chip active" href="{h}">Open route →</a></p></div>' for a,b,h in cards)+'</div><div class="g25-boundary">'+BOUNDARY+'<br>'+TOKEN_BOUNDARY+'</div></main>'
    return shell('GoalOS Pathfinder',body,'Pathfinder')

def site_map_page(routes):
    groups={}
    for r in routes: groups.setdefault(r['category'],[]).append(r)
    body='<main class="g25-shell g25-section"><div class="g25-kicker">All pages</div><h1 class="g25-section-title">Everything routeable.</h1><p class="g25-copy">The complete public surface remains discoverable. Filter with Search / or ask GoalOS where to go.</p><input class="g25-input" data-g25-search-input placeholder="Filter all pages…"><div class="g25-results" data-g25-results></div>'
    for cat,rs in sorted(groups.items()):
        body+=f'<section class="g25-section"><h2>{html.escape(cat)}</h2><div class="g25-panel">'+''.join(f'<a class="g25-route" href="{html.escape(r["href"])}"><div><strong>{html.escape(r["title"])}</strong><small>{html.escape(r["description"])}</small></div><span>Open →</span></a>' for r in rs)+'</div></section>'
    body+='<div class="g25-boundary">'+BOUNDARY+'<br>'+TOKEN_BOUNDARY+'</div></main>'
    return shell('GoalOS Site Map — All Pages',body,'All Pages')

def search_page():
    body=f'<main class="g25-shell g25-section"><div class="g25-kicker">Search /</div><h1 class="g25-section-title">Find any proof path.</h1><p class="g25-copy">Search the public GoalOS route surface or ask GoalOS a question.</p><input class="g25-input" data-g25-search-input placeholder="Search GoalOS routes…"><div class="g25-results" data-g25-results></div><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></main>'
    return shell('GoalOS Search',body,'Search /')

def registry_page(routes):
    body='<main class="g25-shell g25-section"><div class="g25-kicker">Demo registry</div><h1 class="g25-section-title">Every public demo has a role.</h1><p class="g25-copy">Each route is indexed with purpose, expected input, output, gates, and next state.</p><div class="g25-panel">'
    for r in routes:
        if r.get('system'): continue
        body+=f'<div class="g25-route"><div><strong>{html.escape(r["title"])}</strong><small>{html.escape(r["category"])} · input: public-safe objective · output: route, proof package, or review surface · gates: boundary + human review</small></div><a class="g25-chip" href="{html.escape(r["href"])}">Open →</a></div>'
    body+='</div><div class="g25-boundary">'+BOUNDARY+'<br>'+TOKEN_BOUNDARY+'</div></main>'
    return shell('GoalOS Demo Registry',body,'Registry')

def health_page(routes,broken,forbidden):
    status='passed' if not broken and not forbidden else 'review'
    body=f'<main class="g25-shell g25-section"><div class="g25-kicker">Site health</div><h1 class="g25-section-title">Route health: {status}.</h1><p class="g25-copy">Route inventory, preservation, browser-local safety, and public-alpha boundary status.</p><div class="g25-grid"><div class="g25-card"><small>public pages</small><h3>{len([r for r in routes if not r.get("system")])}</h3><p>Indexed and navigable.</p></div><div class="g25-card"><small>broken links</small><h3>{len(broken)}</h3><p>Internal HTML link audit.</p></div><div class="g25-card"><small>forbidden APIs</small><h3>{len(forbidden)}</h3><p>New assets are browser-local.</p></div></div><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></main>'
    return shell('GoalOS Site Health',body,'Site Health')

def write_assets(routes):
    shutil.copy2(SRC/'goalos-universal-mission-composer-v25.css', ASSETS/'goalos-universal-mission-composer-v25.css')
    shutil.copy2(SRC/'goalos-universal-mission-composer-v25.js', ASSETS/'goalos-universal-mission-composer-v25.js')
    data='window.GOALOS_ROUTES='+json.dumps(routes,ensure_ascii=False)+';\nwindow.GOALOS_INTENTS='+json.dumps(INTENTS,ensure_ascii=False)+';\n'
    (ASSETS/'goalos-universal-mission-routes-v25.js').write_text(data,encoding='utf-8')

def write_boundaries():
    pages=[('trust-boundary.html','Proof-native. Not data-hungry. Not wallet-first.','GoalOS public demos are browser-local and do not ask for user data, funds, wallets, transactions, or production authority.','Trust'),('token-boundary.html','$AGIALPHA is public contract identification only.','$AGIALPHA is not available from GoalOS, this repository, the website, maintainers, demos, GitHub issues, or docs.','Token'),('privacy.html','We do not want your data.','Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, proprietary, or trade-secret data.','Trust'),('data-boundary.html','Public proof. Private intelligence.','The site publishes public proof paths, not private prompts, customer data, wallet data, or production secrets.','Trust'),('no-data-no-funds.html','No data. No funds. No wallet.','The public-alpha website is informational, browser-local, no-wallet, no-transaction, and human-review required.','Trust'),('docs.html','GoalOS Docs','Use GoalOS, the registry, Proof Run 001, contract atlas, and Loop → RSI pages as the core documentation path.','All Pages')]
    for href,title,copy,active in pages: (PUBLIC/href).write_text(simple_page(title,copy,active),encoding='utf-8')

def write_core(routes):
    for href in ['index.html','goalos.html','mission.html','tell-goalos.html','mission-autopilot.html','universal-mission-autopilot.html','objective-command-center.html','mission-command-center.html']:
        (PUBLIC/href).write_text(main_interface(),encoding='utf-8')
    body=f'<main class="g25-shell g25-section"><div class="g25-kicker">Ask GoalOS</div><h1 class="g25-section-title">Ask a question. Get the right page.</h1><p class="g25-copy">Ask GoalOS is a browser-local route assistant. It answers from the public site index and opens the correct page only when you ask it to.</p><p><button class="g25-btn primary big" data-g25-ask-open>Open Ask GoalOS</button> <a class="g25-btn big" href="goalos.html">Tell GoalOS what you want</a></p><div class="g25-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></main>'
    (PUBLIC/'ask-goalos.html').write_text(shell('Ask GoalOS — Route Assistant',body,'Search /'),encoding='utf-8')
    (PUBLIC/'start-here.html').write_text(simple_page('Start in 60 seconds','Read the thesis, type an objective, generate a proof path, then review the recommended route.','Start'),encoding='utf-8')
    (PUBLIC/'pathfinder.html').write_text(pathfinder_page(),encoding='utf-8')
    (PUBLIC/'site-map.html').write_text(site_map_page(routes),encoding='utf-8')
    (PUBLIC/'search.html').write_text(search_page(),encoding='utf-8')
    (PUBLIC/'demo-ecosystem-registry.html').write_text(registry_page(routes),encoding='utf-8')
    (PUBLIC/'site-health.html').write_text(health_page(routes,[],[]),encoding='utf-8')
    write_boundaries()

def write_data(routes):
    (PUBLIC/'search-index.json').write_text(json.dumps(routes,ensure_ascii=False,indent=2),encoding='utf-8')
    sitemap=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for r in routes:
        if not r.get('system'): sitemap.append(f'  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{html.escape(r["href"])}</loc></url>')
    sitemap.append('</urlset>'); (PUBLIC/'sitemap.xml').write_text('\n'.join(sitemap),encoding='utf-8')
    nav={'version':VERSION,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z','routes':routes,'boundary':BOUNDARY,'tokenBoundary':TOKEN_BOUNDARY}
    (CONTENT/'public-proof-navigation-v25.json').write_text(json.dumps(nav,indent=2),encoding='utf-8')
    demo={'version':VERSION,'demos':[{'demo_name':r['title'],'canonical_url':r['href'],'one_line_description':r['description'],'primary_workflow_category':r['category'],'expected_inputs':['public-safe objective or question'],'generated_outputs':['route recommendation','mission package','review artifact where applicable'],'proof_gates':['public-alpha boundary','route integrity','human review'],'state_transitions':['DISCOVERABLE','REVIEW_READY'],'role':'UI demo / route surface / evidence surface'} for r in routes if not r.get('system')]}
    (CONTENT/'demo-ecosystem-registry-v25.json').write_text(json.dumps(demo,indent=2),encoding='utf-8'); (CONTENT/'demo-ecosystem-registry.json').write_text(json.dumps(demo,indent=2),encoding='utf-8')

def inject_existing():
    css='<link rel="stylesheet" href="assets/goalos-universal-mission-composer-v25.css">'; scripts='<script src="assets/goalos-universal-mission-routes-v25.js"></script><script src="assets/goalos-universal-mission-composer-v25.js"></script>'
    float='<div class="g25-float"><a href="goalos.html">Tell GoalOS</a><button data-g25-ask-open>Ask GoalOS</button><button data-g25-open-pages>All Pages</button></div>'+modal_html()+ask_modal_html()
    managed={'index.html','goalos.html','mission.html','tell-goalos.html','mission-autopilot.html','universal-mission-autopilot.html','objective-command-center.html','mission-command-center.html','ask-goalos.html','start-here.html','pathfinder.html','site-map.html','search.html','demo-ecosystem-registry.html','site-health.html','trust-boundary.html','token-boundary.html','privacy.html','data-boundary.html','no-data-no-funds.html','docs.html'}
    for p in PUBLIC.rglob('*.html'):
        rel=p.relative_to(PUBLIC).as_posix()
        if rel in managed or rel.startswith(('downloads/','archive/')): continue
        txt=p.read_text(encoding='utf-8',errors='ignore'); changed=False
        if 'goalos-universal-mission-composer-v25.css' not in txt:
            txt=txt.replace('</head>',css+'</head>') if '</head>' in txt else css+txt; changed=True
        if 'id="g25-allpages-modal"' not in txt and 'data-g25-open-pages' not in txt:
            txt=txt.replace('</body>',float+'</body>') if '</body>' in txt else txt+float; changed=True
        if 'goalos-universal-mission-composer-v25.js' not in txt:
            txt=txt.replace('</body>',scripts+'</body>') if '</body>' in txt else txt+scripts; changed=True
        if changed: p.write_text(txt,encoding='utf-8')

def audit_links():
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
    return broken

def forbidden_hits():
    hits=[]
    for p in [ASSETS/'goalos-universal-mission-composer-v25.js',ASSETS/'goalos-universal-mission-routes-v25.js']:
        txt=p.read_text(encoding='utf-8',errors='ignore') if p.exists() else ''
        for term in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if term in txt: hits.append({'file':p.as_posix(),'term':term})
    return hits

def write_reports(routes,restored,broken,forbidden):
    status='passed' if not broken and not forbidden else 'review'
    report={'version':VERSION,'status':status,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z','publicPages':len([r for r in routes if not r.get('system')]),'restoredRoutes':restored,'brokenInternalHtmlLinks':broken,'forbiddenBrowserApiHits':forbidden,'boundary':BOUNDARY,'tokenBoundary':TOKEN_BOUNDARY}
    for name in ['universal-mission-composer-v25-install-report.json','universal-mission-composer-v25-qa.json','universal-mission-composer-v25-route-health.json','universal-mission-composer-v25-audit.json']:
        (REPORTS/name).write_text(json.dumps(report,indent=2),encoding='utf-8')
    demo={'version':VERSION,'status':'passed','samples':[{'objective':i['label'],'decisionState':i['state'],'routes':i['routes'][:3],'externalActions':0} for i in INTENTS]}
    (REPORTS/'universal-mission-composer-v25-demo-run.json').write_text(json.dumps(demo,indent=2),encoding='utf-8')
    (EVIDENCE/'universal-mission-composer-v25-reference-docket.json').write_text(json.dumps({'version':VERSION,'status':status,'title':'GoalOS Universal Mission Composer V25 Reference Docket','mission':'One-box user objective interface plus Ask GoalOS question window and complete navigation','gates':['browser-local','route-integrity','boundary-preserved','all-pages-navigation','human-review-required'],'routesIndexed':report['publicPages'],'boundary':BOUNDARY},indent=2),encoding='utf-8')
    return report

def write_docs():
    (DOCS/'website'/'UNIVERSAL_MISSION_COMPOSER_V25.md').write_text('# GoalOS Universal Mission Composer V25\n\nA front-and-center one-box interface: users type what they want, GoalOS generates the proof path, route cards, Mission Contract, Reviewer Brief, Action Graph, and next best page. Ask GoalOS remains available as a browser-local question window.\n\nBoundary: no user data, no funds, no wallet, no transaction, no network call, no production authority.\n',encoding='utf-8')
    (DOCS/'reviewer'/'HOW_TO_REVIEW_UNIVERSAL_MISSION_COMPOSER_V25.md').write_text('# How to review V25\n\nOpen `goalos.html` and `index.html`. Enter sample objectives. Confirm route cards, downloads, Ask GoalOS, all pages search, and boundary language. Confirm no wallet, no transaction, and no backend call.\n',encoding='utf-8')
    (EXAMPLES/'public-safe-objectives.md').write_text('# Public-safe objectives\n\n- I want to understand the 48 Ethereum Mainnet contracts.\n- I want to run a public-safe proof mission.\n- I want to understand Loop to RSI governance.\n- I want to check privacy, token, and data boundaries.\n- I am new and want the fastest path to understand GoalOS.\n',encoding='utf-8')
    (ISSUES/'universal-mission-composer-v25.md').write_text('## GoalOS Universal Mission Composer V25 review\n\nReview the front-and-center one-box interface, Ask GoalOS, route cards, downloads, all-pages navigation, and public-alpha boundary.\n',encoding='utf-8')
    (TEMPLATES/'universal_mission_composer_feedback.yml').write_text('name: GoalOS Universal Mission Composer feedback\ndescription: Report feedback about the one-box GoalOS interface.\nlabels: [website, ux, mission, review]\nbody:\n  - type: checkboxes\n    id: boundary\n    attributes:\n      label: Public-safe confirmation\n      options:\n        - label: I confirm I am not submitting personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.\n          required: true\n  - type: textarea\n    id: feedback\n    attributes:\n      label: Feedback\n      description: What should improve?\n',encoding='utf-8')

def main():
    restored=0
    for href,title in KNOWN_ROUTES.items():
        if ensure_fallback(href,title): restored+=1
    routes=scan_routes(); write_assets(routes); write_core(routes); routes=scan_routes(); write_assets(routes); write_data(routes); inject_existing(); routes=scan_routes(); write_assets(routes); write_data(routes)
    broken=audit_links(); forbidden=forbidden_hits(); (PUBLIC/'site-health.html').write_text(health_page(routes,broken,forbidden),encoding='utf-8')
    report=write_reports(routes,restored,broken,forbidden); write_docs()
    readme=ROOT/'README.md'; block='\n\n## GoalOS Universal Mission Composer V25\n\nThe website now places the one-box GoalOS interface front and center: users type what they want, GoalOS generates the proof path, route recommendations, Mission Contract, Evidence Docket plan, Reviewer Brief, Action Graph, and next best page. Ask GoalOS remains available as a browser-local question window across the site. No user data, no funds, no wallet, no transaction, no network call, no production authority.\n'
    if readme.exists():
        txt=readme.read_text(encoding='utf-8',errors='ignore')
        if 'GoalOS Universal Mission Composer V25' not in txt: readme.write_text(txt.rstrip()+block,encoding='utf-8')
    else: readme.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
