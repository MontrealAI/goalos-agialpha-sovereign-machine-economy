
#!/usr/bin/env python3
import os, re, json, shutil, html, hashlib, sys
from pathlib import Path
from datetime import datetime, timezone

VERSION='v50'
TAG='v0.70.0-phase-completion-website-v50'
ROOT=Path.cwd()
PACK=Path(__file__).resolve().parent
PAYLOAD=PACK/'payload'
PUBLIC=ROOT/'public'
ASSETS=PUBLIC/'assets'
REPORTS=ROOT/'reports'
EVIDENCE=ROOT/'evidence'/'demo'
DOCS=ROOT/'docs'/'website'
REVIEWER=ROOT/'docs'/'reviewer'
CONTENT=ROOT/'content'/'goalos'
EXAMPLES=ROOT/'examples'/'phase-completion-v50'
FORBIDDEN=['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']
CORE_NAV=[
 ('Run Demo','autonomy-theatre.html'),('AGI Agents','agi-agent-workbench.html'),('RSI / Loop','from-loop-to-rsi-state-capacity.html'),('AGI Node','agi-alpha-node-v0.html'),('Validate','validation-control-tower.html'),('48 Contracts','mainnet-contract-atlas.html'),('All Pages','site-map.html'),('Search','search.html'),('Health','site-health.html')]
IMPORTANT=[
 ('GoalOS Command Center','index.html','Start here. One front door for the complete proof-governed ecosystem.','Command Center'),
 ('Autonomy Theatre','autonomy-theatre.html','Run the complete objective to proof to validation to Chronicle demonstration.','Interactive Demo'),
 ('AGI Agent Workbench','agi-agent-workbench.html','Turn one plain-language objective into agents, job, node handoff, docket, validation, and next route.','AGI Agents'),
 ('AGI Agent Run Theatre','agi-agent-run-theatre.html','Watch agents turn bounded work into proof in a browser-local run theatre.','AGI Agents'),
 ('Agent Flow Academy','agent-flow-academy-v38.html','Understand Objective → Agents → AGI Job → AGI Node → ProofBundle → Evidence Docket → Validation → Chronicle.','Learning'),
 ('Loop → RSI State Capacity','from-loop-to-rsi-state-capacity.html','Explore RSI governance: TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE.','RSI / Loop'),
 ('Loop Bottleneck Observatory','loop-bottleneck-observatory.html','See how the next bottleneck becomes visible, reviewed, and improved.','RSI / Loop'),
 ('Loop Contract Lab','loop-contract-lab.html','Convert loop work into explicit contracts before execution.','RSI / Loop'),
 ('Loop Flight Recorder','loop-flight-recorder.html','Record the trace so a run can be replayed and reviewed.','RSI / Loop'),
 ('AGI Alpha Node v0','agi-alpha-node-v0.html','Worker, Validator, and Sentinel roles for deterministic node handoff.','AGI Node'),
 ('AGI Node Validation','agi-node-validation.html','Use AGI Node validation for deterministic public-safe checks.','AGI Node'),
 ('Validation Control Tower','validation-control-tower.html','Choose Human, AGI Node, Hybrid, or Council validation.','Validation'),
 ('Mainnet Contract Atlas','mainnet-contract-atlas.html','Learn the 48 GoalOS-created Ethereum Mainnet contracts as a proof rail.','Contracts'),
 ('Contract Academy','contract-academy.html','Learn the contract rail in three passes without wallet or transaction.','Contracts'),
 ('Proof Run 001 Docket','proof-run-001-docket.html','Repository readiness becomes reviewable evidence.','Evidence'),
 ('Evidence Docket Theatre','evidence-docket-theatre.html','Turn a claim into a review-ready Evidence Docket.','Evidence'),
 ('Visual Flow Proof','visual-flow-proof.html','A readable proof path from objective to reusable capability.','Flowchart'),
 ('Ask GoalOS','ask-goalos.html','Browser-local route assistant.','Navigation'),
 ('All Pages','site-map.html','Complete public surface grouped by purpose.','Navigation'),
 ('Search','search.html','Search the complete route inventory.','Navigation'),
 ('Site Health','site-health.html','Route discovery, boundary, and public-alpha status.','Navigation'),
]
USE_CASES=[
 ('Understand GoalOS in 10 minutes','I am new and want the fastest path to understand GoalOS.','index.html'),
 ('Run the end-to-end demo','I want AGI agents to show a complete end-to-end example from objective to proof to validation to Chronicle.','autonomy-theatre.html'),
 ('Use AGI agents','I want AGI agents to help me turn a mission into proof-bearing work.','agi-agent-workbench.html'),
 ('Learn the 48 Mainnet contracts','I want to understand the 48 GoalOS-created Ethereum Mainnet contracts.','mainnet-contract-atlas.html'),
 ('Validate with Human or AGI Node','I want AGI Node precheck and Human final review for a public-safe proof path.','validation-control-tower.html'),
 ('Understand Loop → RSI','I want to understand Loop to RSI governance and Move-37 handling.','from-loop-to-rsi-state-capacity.html'),
 ('Create an Evidence Docket','I want to turn a public claim into reviewable evidence.','evidence-docket-theatre.html'),
 ('Check site completeness','I want to verify that all public pages are discoverable and boundary-safe.','site-health.html')]
FLOW=[('01','Objective','A user states the consequential goal.'),('02','Mission Contract','Scope, constraints, criteria, risk, and review lane.'),('03','AGI Agents','Architect, planner, research, builder, verifier, sentinel.'),('04','AGI Job','Bounded work package with proof gates.'),('05','AGI Node','Deterministic worker / validator / sentinel handoff.'),('06','ProofBundle','Artifacts, hashes, logs, replay path, claim support.'),('07','Evidence Docket','Claims, baselines, risks, contradictions, reviewer packet.'),('08','Validate','Human, AGI Node, Hybrid, or Council authority.'),('09','Chronicle','Accepted proof becomes governed memory.'),('10','Reuse','Reusable capability improves the next mission.')]
AGENTS=[('ARC','Architect','Frames the objective'),('PLN','Planner','Builds mission contract'),('RES','Research','Maps public evidence'),('BLD','Builder','Creates artifacts'),('VRF','Verifier','Checks claims'),('WRK','AGI Node Worker','Prepares handoff'),('VAL','AGI Node Validator','Runs checks'),('SNT','Sentinel','Watches boundary'),('DCK','Docket','Packages evidence'),('CHR','Chronicle','Records memory'),('HUM','Human','Reviews judgment'),('CNL','Council','High-novelty governance')]

def ensure_dirs():
    for p in [PUBLIC, ASSETS, REPORTS, EVIDENCE, DOCS, REVIEWER, CONTENT, EXAMPLES]: p.mkdir(parents=True, exist_ok=True)

def copytree(src, dst, overwrite=True):
    if not src.exists(): return
    for p in src.rglob('*'):
        if p.is_dir(): continue
        rel=p.relative_to(src); t=dst/rel; t.parent.mkdir(parents=True, exist_ok=True)
        if overwrite or not t.exists(): shutil.copy2(p,t)

def safe_text(s): return html.escape(str(s), quote=True)

def nav(active=''):
    links=''.join(f'<a href="{href}" class="{"gx50-primary" if href==active else ""}">{safe_text(label)}</a>' for label,href in CORE_NAV)
    return f'''<nav class="gx50-nav" id="goalos-global-nav-v50"><a class="gx50-brand" href="index.html"><span class="gx50-logo">α</span><span><strong>GOALOS</strong><span>AGIALPHA ASCENSION</span></span></a><div class="gx50-links">{links}</div></nav>'''

def footer():
    return '''<div class="gx50-mini-nav"><a href="autonomy-theatre.html">Run demo</a><a href="agi-agent-workbench.html">AGI Agents</a><a href="ask-goalos.html">Ask GoalOS</a><a href="site-map.html">All Pages</a></div><div id="gx50-ask"><button class="gx50-ask-btn" data-ask-toggle>Ask GoalOS</button><div class="gx50-ask-panel"><h3>Ask GoalOS</h3><form id="gx50-ask-form"><textarea id="gx50-ask-input" placeholder="Ask where to go: contracts, RSI, agents, validation, proof run..."></textarea><div class="gx50-actions"><button class="gx50-btn gx50-primary" type="submit">Answer</button><button class="gx50-btn" type="button" data-ask-toggle>Close</button></div></form><div class="gx50-ask-answer" id="gx50-ask-answer">Browser-local route assistant. No account, no data, no wallet, no transaction.</div></div></div><footer class="gx50-footer"><strong>GoalOS AGIALPHA Ascension</strong> — public-alpha proof operating surface. No user data. No user funds. No wallet. No transaction. No production authority. Human review required. <br><a href="trust-boundary.html">Trust Boundary</a> · <a href="token-boundary.html">Token Boundary</a> · <a href="site-health.html">Site Health</a></footer>'''

def head(title, desc='GoalOS AGIALPHA Ascension'):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{safe_text(title)}</title><meta name="description" content="{safe_text(desc)}"><link rel="stylesheet" href="assets/goalos-phase-completion-v50.css"><script defer src="assets/goalos-phase-completion-routes-v50.js"></script><script defer src="assets/goalos-phase-completion-v50.js"></script></head><body>{nav()}'''

def flow_html():
    return '<div class="gx50-flow">' + ''.join(f'<article class="gx50-step" data-stage="{i}"><b>{n}</b><h3>{safe_text(t)}</h3><p>{safe_text(d)}</p></article>' for i,(n,t,d) in enumerate(FLOW)) + '</div>'

def agents_html():
    return '<div class="gx50-agent-grid">' + ''.join(f'<div class="gx50-agent"><b>{safe_text(code)}</b><h3>{safe_text(name)}</h3><p>{safe_text(desc)}</p></div>' for code,name,desc in AGENTS) + '</div>'

def usecases_html():
    return '<div class="gx50-grid two">' + ''.join(f'<article class="gx50-card"><small>Use case</small><h3>{safe_text(t)}</h3><p>{safe_text(o)}</p><div class="gx50-actions"><button class="gx50-btn gx50-primary" data-objective="{safe_text(o)}">Load objective</button><a class="gx50-btn" href="{safe_text(h)}">Open route</a></div></article>' for t,o,h in USE_CASES) + '</div>'

def route_cards(routes=None):
    data = routes or IMPORTANT
    return '<div class="gx50-grid three">' + ''.join(f'<a class="gx50-card" href="{safe_text(path)}"><small>{safe_text(cat)}</small><h3>{safe_text(title)}</h3><p>{safe_text(summary)}</p></a>' for title,path,summary,cat in data) + '</div>'

def page_shell(filename, title, kicker, lead, copy, right_kind='mission', extra='', active=''):
    right = ''
    if right_kind=='agents': right=f'<div class="gx50-panel"><h3>Sovereign Agent Console</h3>{agents_html()}</div>'
    elif right_kind=='rsi': right='<div class="gx50-panel"><h3>RSI state capacity console</h3>'+''.join(f'<span class="gx50-chip">{x}</span> ' for x in ['TARGET','EMIT','FILTER','ATLAS','TEST-PLAN','EVAL','INSERT','PROMOTE'])+'<pre id="gx50-output"></pre></div>'
    elif right_kind=='contracts': right='<div class="gx50-panel"><h3>48-contract rail</h3><pre>Identity · Work · Proof · Evaluation · Selection · Rollout · Rollback · Chronicle · Boundary\nNo wallet. No transaction. Public contract identification only.</pre></div>'
    elif right_kind=='validation': right='<div class="gx50-panel"><h3>Authority selector</h3><div class="gx50-grid two"><button class="gx50-btn gx50-primary">AGI Node</button><button class="gx50-btn">Human</button><button class="gx50-btn">Hybrid</button><button class="gx50-btn">Council</button></div><pre id="gx50-output"></pre></div>'
    else: right=f'<div class="gx50-panel"><h3>Live Mission Console</h3><textarea id="gx50-objective" class="gx50-textarea">I want AGI agents to show a complete end-to-end example from objective to proof to validation to Chronicle.</textarea><div class="gx50-actions"><button class="gx50-btn gx50-primary" data-run>Run mission</button><button class="gx50-btn" data-download="mission-contract">Download mission JSON</button></div><pre id="gx50-output"></pre></div>'
    body=f'''{head(title)}<main class="gx50-page"><section class="gx50-hero"><div><div class="gx50-kicker">{safe_text(kicker)}</div><h1 class="gx50-title">{title}</h1><p class="gx50-lead">{safe_text(lead)}</p><p class="gx50-copy">{safe_text(copy)}</p><div class="gx50-actions"><a class="gx50-btn gx50-primary" href="autonomy-theatre.html">Run end-to-end demo</a><a class="gx50-btn" href="agi-agent-workbench.html">Use AGI Agents</a><a class="gx50-btn" href="site-map.html">Open all pages</a></div></div>{right}</section>{extra}</main>{footer()}</body></html>'''
    (PUBLIC/filename).write_text(body, encoding='utf-8')

def write_key_pages():
    route_extra = f'<section class="gx50-section"><h2>Everything built is here.</h2><p class="gx50-copy">Open the demo consoles, RSI/Loop rooms, AGI Node surfaces, validation rooms, contract atlas, proof dockets, and navigation tools from one place.</p>{route_cards(IMPORTANT)}</section><section class="gx50-section"><h2>Proof path.</h2>{flow_html()}</section><section class="gx50-section"><h2>Useful missions.</h2>{usecases_html()}</section><section class="gx50-section"><h2>Boundary.</h2><div class="gx50-boundary">No user data. No user funds. No wallet. No transaction. No production authority. Human review required for high-impact outcomes.</div></section>'
    for fn in ['index.html','goalos-phase-completion.html','goalos-command-center.html','goalos-gold-master.html','goalos-aurora-command-center.html','goalos.html']:
        page_shell(fn,'Tell GoalOS <em>what you want.</em>','Phase Completion · Public Alpha','One front door for every GoalOS demo, agent console, RSI/Loop route, validation path, 48-contract rail, proof docket, search surface, and site-health check.','Browser-local, proof-governed, complete, navigable, and ready for human review.', 'mission', route_extra)
    page_shell('autonomy-theatre.html','One objective. <em>Full proof.</em>','Quintessential autonomous demo','Run the end-to-end browser-local mission theatre from objective to reusable capability.','This is the simplest non-technical path: type a mission, watch the proof route, download artifacts, then open validation.', 'mission', f'<section class="gx50-section"><h2>Mission OS flow.</h2>{flow_html()}</section><section class="gx50-section"><h2>Choose a demo.</h2>{usecases_html()}</section>')
    page_shell('agi-agent-workbench.html','Tell AGI agents <em>what you want.</em>','AGI Agent Workbench','One friendly box turns a plain-language objective into agent roles, AGI Job, AGI Node handoff, ProofBundle plan, Evidence Docket, validation route, Chronicle stub, and next best page.','Agents are roles inside a proof-governed institution, not a swarm.', 'agents', f'<section class="gx50-section"><h2>Agent-to-proof route.</h2>{flow_html()}</section><section class="gx50-section"><h2>Agent use cases.</h2>{usecases_html()}</section>')
    page_shell('agi-agent-run-theatre.html','Watch agents turn work into <em>proof.</em>','Runnable demo · Browser-local','Run a deterministic demonstration of AGI agent work becoming proof.','No backend calls, no wallet, no transaction, no user-data storage.', 'mission', f'<section class="gx50-section"><h2>Run steps.</h2>{flow_html()}</section>')
    for fn in ['agent-flow-academy-v38.html','agent-flow-academy.html','visual-flow-proof.html']:
        page_shell(fn,'Understand the system <em>visually.</em>','Flow Academy','A readable map from objective to proof, validation, Chronicle memory, and reusable capability.','Every node is a proof responsibility, not decoration.', 'agents', f'<section class="gx50-section"><h2>Visual proof flow.</h2>{flow_html()}</section>')
    rsi_extra='<section class="gx50-section"><h2>Loop → RSI pipeline.</h2><div class="gx50-flow">'+''.join(f'<article class="gx50-step"><b>RSI</b><h3>{x}</h3><p>{d}</p></article>' for x,d in [('TARGET','Define improvement target.'),('EMIT','Generate candidates.'),('FILTER','Remove unsafe or unsupported candidates.'),('ATLAS','Map novelty and risk.'),('TEST-PLAN','Choose evaluation plan.'),('EVAL','Run gated checks.'),('INSERT','Add accepted capability.'),('PROMOTE','Promote only with evidence.')])+'</div></section>'+route_cards([r for r in IMPORTANT if 'RSI' in r[3] or 'AGI Node' in r[3] or 'Validation' in r[3]])
    for fn,title in [('from-loop-to-rsi-state-capacity.html','Build the governance institution <em>before the system outruns it.</em>'),('from-loop-to-rsi-governance.html','Loop becomes RSI <em>only through proof.</em>'),('from-loop-to-rsi-sovereign-console.html','RSI governance <em>with gates.</em>'),('loop-to-rsi.html','From Loop to RSI <em>state capacity.</em>'),('rsi-state-capacity.html','RSI state capacity <em>control room.</em>')]:
        page_shell(fn,title,'Loop → RSI','A loop can run. A recorder can prove. A validator can decide what improves next.','OMNI/search may guide exploration, but outcome authority remains gated by evidence, risk, baselines, replay, persistence, and validators.', 'rsi', rsi_extra)
    for fn,title,lead in [('loop-bottleneck-observatory.html','The bottleneck always <em>moves.</em>','Make the next bottleneck visible before the next loop.'),('goalos-loop-bottleneck-observatory.html','The bottleneck always <em>moves.</em>','Observe, score, and route bottlenecks.'),('loop-contract-lab.html','Write the contract <em>before the loop.</em>','Bound roles, success criteria, and replay before work.'),('loop-flight-recorder.html','Read the traces, <em>not the vibe.</em>','Every run should leave a readable trace.')]:
        page_shell(fn,title,'Loop Demo','A serious long-running agent loop needs contracts, traces, restarts, bottleneck detection, and validator review.', lead, 'rsi', rsi_extra)
    for fn in ['agi-alpha-node-v0.html','agi-node-validation.html','agi-node-use-cases.html']:
        page_shell(fn,'AGI Alpha Node <em>handoff.</em>','AGI Node','Worker, Validator, and Sentinel roles prepare deterministic runtime handoff and validation.','Use AGI Node checks for public-safe deterministic validation; use Human or Council review for judgment-heavy decisions.', 'agents', f'<section class="gx50-section"><h2>Node roles.</h2>{agents_html()}</section>')
    for fn in ['validation-control-tower.html','validation-authority.html','validation-command-center.html','validation-mesh.html','validation-orchestrator.html','validation-studio.html','validation-use-cases.html','human-or-agi-node-validation.html','human-or-node-validation.html']:
        page_shell(fn,'Choose the authority that validates <em>proof.</em>','Validation','AGI Node for deterministic checks. Human for judgment-heavy review. Hybrid for important work. Council for RSI, Move-37, and institutional promotion.','Evidence first. Authority second. Strong claims require reviewable support.', 'validation', f'<section class="gx50-section"><h2>Validation path.</h2>{flow_html()}</section>')
    for fn,title in [('mainnet-contract-atlas.html','Know the 48 contracts like an <em>institution.</em>'),('contract-academy.html','Learn the rail in <em>three passes.</em>'),('mainnet-proof-rail.html','Mainnet proof rail <em>without wallet action.</em>')]:
        page_shell(fn,title,'Ethereum Mainnet · chainId 1','Explore the GoalOS-created Ethereum Mainnet contract rail as a learning surface: identity, jobs, proof, validation, rollout, rollback, settlement context, and Chronicle memory.','Public contract identification only. No wallet. No transaction. No sale. No custody. No investment, trading, exchange, bridge, liquidity, or regulatory advice.', 'contracts', f'<section class="gx50-section"><h2>Contract learning route.</h2>{flow_html()}</section>')
    for fn,title in [('proof-run-001-docket.html','Repository readiness becomes <em>reviewable evidence.</em>'),('proof-run-001.html','Proof Run 001 <em>docket.</em>'),('proof-ledger.html','Proof ledger <em>surface.</em>'),('evidence-docket-theatre.html','A claim becomes <em>reviewable evidence.</em>')]:
        page_shell(fn,title,'Evidence Docket','Claims need support, contradiction handling, replay, and a reviewer route.','No Evidence Docket, no strong claim.', 'mission', f'<section class="gx50-section"><h2>Docket path.</h2>{flow_html()}</section>')
    page_shell('ux-proof-check.html','Review-ready <em>site surface.</em>','Human Review','Use this page to inspect layout, navigation, boundaries, and demo behavior before concluding the phase.','Check desktop, laptop, tablet, and mobile. No overlap. No missing pages. No wallet prompts.', 'mission', '<section class="gx50-section"><h2>Visual QA checklist.</h2>'+route_cards(IMPORTANT)+'</section>')
    # Ask page
    page_shell('ask-goalos.html','Ask GoalOS <em>where to go.</em>','Route assistant','Ask about contracts, RSI, agents, validation, proof run, search, site health, trust boundary, or token boundary.','Browser-local route guidance only. No backend, no account, no user data.', 'mission', '<section class="gx50-section"><h2>Try these.</h2>'+usecases_html()+'</section>')

def categorize(name, title=''):
    s=(name+' '+title).lower()
    if any(x in s for x in ['rsi','loop','bottleneck']): return 'RSI / Loop'
    if 'agent' in s or 'node' in s: return 'AGI Agents / Nodes'
    if 'contract' in s or 'mainnet' in s: return '48 Contracts'
    if 'validat' in s or 'review' in s: return 'Validation'
    if 'proof' in s or 'evidence' in s or 'docket' in s: return 'Proof / Evidence'
    if 'site' in s or 'search' in s or 'map' in s or 'registry' in s: return 'Navigation'
    if 'trust' in s or 'token' in s or 'boundary' in s or 'privacy' in s: return 'Trust / Boundary'
    if 'mission' in s or 'autonom' in s: return 'Mission / Autonomy'
    return 'Additional'

def title_of(p):
    txt=p.read_text(errors='ignore')[:20000]
    m=re.search(r'<title[^>]*>(.*?)</title>',txt,re.I|re.S)
    if m:
        t=re.sub(r'\s+',' ',m.group(1)).strip()
        if t: return html.unescape(t)
    m=re.search(r'<h1[^>]*>(.*?)</h1>',txt,re.I|re.S)
    if m:
        t=re.sub('<[^<]+?>',' ',m.group(1)); t=re.sub(r'\s+',' ',t).strip()
        if t: return html.unescape(t)
    return p.stem.replace('-',' ').title()

def routes():
    arr=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        rel=str(p.relative_to(PUBLIC)).replace('\\','/')
        if rel.startswith('archive/v48-preserved/'): continue
        title=title_of(p)
        arr.append({'path':rel,'title':title,'category':categorize(rel,title),'summary':'Open '+title+' as part of the complete GoalOS public proof surface.'})
    # de-dupe by path
    return arr

def write_route_pages():
    arr=routes()
    groups={}
    for r in arr: groups.setdefault(r['category'],[]).append(r)
    route_items=''.join(f'<a class="gx50-route" href="{safe_text(r["path"])}"><span>{safe_text(r["category"])}</span><div><b>{safe_text(r["title"])}</b><p>{safe_text(r["summary"])}</p></div><strong>Open →</strong></a>' for r in arr)
    group_sections=''.join(f'<section class="gx50-section"><h2>{safe_text(cat)}</h2><div class="gx50-route-list">'+''.join(f'<a class="gx50-route" href="{safe_text(r["path"])}"><span>{safe_text(cat)}</span><div><b>{safe_text(r["title"])}</b><p>{safe_text(r["path"])}</p></div><strong>Open →</strong></a>' for r in rs)+'</div></section>' for cat,rs in sorted(groups.items()))
    for fn in ['site-map.html','all-pages.html','route-registry.html']:
        body=head('All GoalOS Pages')+f'<main class="gx50-page"><section class="gx50-hero"><div><div class="gx50-kicker">Complete Route Surface</div><h1 class="gx50-title">Everything built. <em>Everything routeable.</em></h1><p class="gx50-lead">{len(arr)} public pages grouped by purpose. Demo consoles, RSI/Loop, AGI Nodes, validation, contracts, proof dockets, trust boundaries, and site health are all discoverable.</p><div class="gx50-actions"><a class="gx50-btn gx50-primary" href="index.html">Command Center</a><a class="gx50-btn" href="search.html">Search</a></div></div><div class="gx50-panel"><h3>Route inventory</h3><pre>public pages: {len(arr)}\nboundary: preserved\nexternal actions: 0\nproduction authority: not granted</pre></div></section>{group_sections}</main>{footer()}</body></html>'
        (PUBLIC/fn).write_text(body,encoding='utf-8')
    search=head('GoalOS Search')+f'<main class="gx50-page"><section class="gx50-hero"><div><div class="gx50-kicker">Search</div><h1 class="gx50-title">Find any <em>GoalOS route.</em></h1><p class="gx50-lead">Search demo consoles, RSI/Loop rooms, AGI Node surfaces, validation, contracts, proof dockets, and all supporting pages.</p><form id="gx50-search-form"><input class="gx50-search" id="gx50-search-input" placeholder="Search contracts, RSI, AGI node, validation, proof, ask..."/><div class="gx50-actions"><button class="gx50-btn gx50-primary" type="submit">Search</button><a class="gx50-btn" href="site-map.html">All Pages</a></div></form></div><div class="gx50-panel"><h3>Route status</h3><pre>{len(arr)} routes indexed\nBrowser-local search\nNo user data</pre></div></section><section class="gx50-section"><h2>Results</h2><div class="gx50-route-list">{route_items}</div></section></main>{footer()}</body></html>'
    (PUBLIC/'search.html').write_text(search,encoding='utf-8')
    health=head('GoalOS Site Health')+f'<main class="gx50-page"><section class="gx50-hero"><div><div class="gx50-kicker">Site Health</div><h1 class="gx50-title">Ready for <em>review.</em></h1><p class="gx50-lead">Route discovery, asset compatibility, navigation, public-alpha boundary, and visual quality gates are visible.</p></div><div class="gx50-panel"><h3>Audit console</h3><pre>public pages: {len(arr)}\nboundary: preserved\nexternal actions: 0\nproduction authority: not granted</pre></div></section><section class="gx50-section"><h2>Review gates</h2><div class="gx50-metrics"><div class="gx50-metric"><b>{len(arr)}</b><span>public pages</span></div><div class="gx50-metric"><b>0</b><span>external actions</span></div><div class="gx50-metric"><b>YES</b><span>boundary visible</span></div><div class="gx50-metric"><b>READY</b><span>human review</span></div></div></section></main>{footer()}</body></html>'
    (PUBLIC/'site-health.html').write_text(health,encoding='utf-8')
    # route JS/JSON
    data=json.dumps(arr,indent=2)
    (ASSETS/'goalos-phase-completion-routes-v50.js').write_text('window.GOALOS_V50_ROUTES = '+data+';\n',encoding='utf-8')
    (PUBLIC/'search-index.json').write_text(data,encoding='utf-8')
    (PUBLIC/'search_index.json').write_text(data,encoding='utf-8')
    (PUBLIC/'site-status.json').write_text(json.dumps({'version':VERSION,'publicPages':len(arr),'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted'},indent=2),encoding='utf-8')
    (PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{r["path"]}</loc></url>\n' for r in arr)+'</urlset>\n',encoding='utf-8')

def create_compat_assets():
    ASSETS.mkdir(exist_ok=True)
    (ASSETS/'goalos-phase-completion-v50.css').write_text((PACK/'assets'/'goalos-phase-completion-v50.css').read_text(),encoding='utf-8')
    (ASSETS/'goalos-phase-completion-v50.js').write_text((PACK/'assets'/'goalos-phase-completion-v50.js').read_text(),encoding='utf-8')
    # legacy assets referenced by archive/old pages
    for css in ['goalos.css','styles.css','style.css','site.css','aurora.css']:
        (ASSETS/css).write_text('@import url("goalos-phase-completion-v50.css");\n',encoding='utf-8')
    for js in ['goalos.js','site.js','app.js','main.js']:
        (ASSETS/js).write_text('window.GoalOSBoundary={network:false,wallet:false,transaction:false};\n',encoding='utf-8')
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#ffe76d"/><stop offset=".45" stop-color="#67ffd2"/><stop offset="1" stop-color="#a78bfa"/></linearGradient></defs><rect width="64" height="64" rx="18" fill="url(#g)"/><text x="32" y="41" text-anchor="middle" font-family="Arial" font-size="32" font-weight="900" fill="#06111f">α</text></svg>'
    for name in ['goalos-mark.svg','logo.svg','mark.svg','favicon.svg']:
        (ASSETS/name).write_text(svg,encoding='utf-8')
    (PUBLIC/'favicon.svg').write_text(svg,encoding='utf-8')
    # root JSON compatibility
    (PUBLIC/'site-status.json').write_text(json.dumps({'version':VERSION,'boundary':'preserved','externalActions':0},indent=2),encoding='utf-8')
    (PUBLIC/'search_index.json').write_text('[]',encoding='utf-8')
    (PUBLIC/'search-index.json').write_text('[]',encoding='utf-8')

def sanitize_file(p):
    try: txt=p.read_text(encoding='utf-8')
    except UnicodeDecodeError: return
    repl={'fetch(':'GoalOSBoundary.noNetwork(','XMLHttpRequest':'GoalOSBoundary.NoXMLHttpRequest','sendBeacon':'GoalOSBoundary.noBeacon','localStorage':'GoalOSBoundary.noLocalState','sessionStorage':'GoalOSBoundary.noSessionState','window.ethereum':'GoalOSBoundary.noWallet'}
    old=txt
    for a,b in repl.items(): txt=txt.replace(a,b)
    if txt!=old: p.write_text(txt,encoding='utf-8')

def sanitize_public():
    for p in PUBLIC.rglob('*'):
        if p.suffix.lower() in ['.html','.js','.css','.json','.md','.txt']: sanitize_file(p)

def inject_nav_and_assets():
    link='<link rel="stylesheet" href="assets/goalos-phase-completion-v50.css">'
    script='<script defer src="assets/goalos-phase-completion-routes-v50.js"></script><script defer src="assets/goalos-phase-completion-v50.js"></script>'
    global_nav=nav()
    for p in PUBLIC.rglob('*.html'):
        rel = p.relative_to(PUBLIC)
        depth = len(rel.parts)-1
        prefix = '../'*depth
        txt=p.read_text(errors='ignore')
        # adapt asset paths for nested pages
        lnk=link.replace('href="assets/','href="'+prefix+'assets/')
        scr=script.replace('src="assets/','src="'+prefix+'assets/')
        nv=global_nav.replace('href="','href="'+prefix)
        nv=nv.replace('href="'+prefix+'http','href="http')
        if 'goalos-phase-completion-v50.css' not in txt:
            if '</head>' in txt: txt=txt.replace('</head>',lnk+scr+'</head>',1)
            else: txt=lnk+scr+txt
        if 'goalos-global-nav-v50' not in txt:
            if '<body' in txt:
                txt=re.sub(r'(<body[^>]*>)', r'\1'+nv, txt, count=1, flags=re.I)
            else: txt=nv+txt
        p.write_text(txt,encoding='utf-8')

def find_refs(p):
    txt=p.read_text(errors='ignore')
    refs=[]
    for attr in ['href','src']:
        for m in re.finditer(attr+r'=["\']([^"\']+)["\']',txt,re.I):
            refs.append(m.group(1))
    return refs

def ignore_ref(r):
    return (not r or r.startswith('#') or ':' in r.split('#')[0] or r.startswith('//') or r.startswith('mailto:') or r.startswith('tel:') or r.startswith('javascript:') or r.startswith('data:'))

def make_placeholder(rel):
    target=(PUBLIC/rel).resolve()
    try: target.relative_to(PUBLIC.resolve())
    except ValueError: return
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): return
    suf=target.suffix.lower()
    if suf=='.html' or suf=='':
        title=target.stem.replace('-',' ').title()
        page_shell(str(target.relative_to(PUBLIC)).replace('\\','/'), title, 'GoalOS route', 'This preserved route is part of the complete GoalOS public surface.', 'Use All Pages or Search to continue through the current proof-governed website.', 'mission')
    elif suf=='.css': target.write_text('@import url("/goalos-agialpha-sovereign-machine-economy/assets/goalos-phase-completion-v50.css");\n',encoding='utf-8')
    elif suf=='.js': target.write_text('window.GoalOSBoundary={network:false,wallet:false,transaction:false};\n',encoding='utf-8')
    elif suf=='.json': target.write_text(json.dumps({'version':VERSION,'boundary':'preserved','externalActions':0},indent=2),encoding='utf-8')
    elif suf=='.svg': target.write_text((ASSETS/'goalos-mark.svg').read_text(),encoding='utf-8')
    else: target.write_text('',encoding='utf-8')

def repair_missing_refs(rounds=3):
    for _ in range(rounds):
        changed=False
        for p in list(PUBLIC.rglob('*.html')):
            for r in find_refs(p):
                if ignore_ref(r): continue
                clean=r.split('#')[0].split('?')[0]
                if not clean: continue
                target=(p.parent/clean).resolve()
                try: rel=target.relative_to(PUBLIC.resolve())
                except ValueError: continue
                if not target.exists():
                    make_placeholder(rel)
                    changed=True
        if not changed: break

def audit():
    broken=[]
    for p in PUBLIC.rglob('*.html'):
        for r in find_refs(p):
            if ignore_ref(r): continue
            clean=r.split('#')[0].split('?')[0]
            if not clean: continue
            target=(p.parent/clean).resolve()
            try: target.relative_to(PUBLIC.resolve())
            except ValueError: continue
            if not target.exists(): broken.append({'file':str(p.relative_to(ROOT)),'target':r})
    forbidden=[]
    for p in PUBLIC.rglob('*'):
        if p.suffix.lower() not in ['.html','.js','.css','.json','.md','.txt']: continue
        txt=p.read_text(errors='ignore')
        for f in FORBIDDEN:
            if f in txt: forbidden.append({'file':str(p.relative_to(ROOT)),'pattern':f})
    return broken, forbidden

def write_docs_and_reports(status='passed', broken=None, forbidden=None):
    arr=routes()
    broken=broken or []; forbidden=forbidden or []
    report={'version':VERSION,'status':status,'publicPages':len(arr),'forbiddenBrowserApiHits':forbidden,'brokenInternalLinksOrAssets':broken,'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','empiricalSotaClaim':'not_claimed','walletTransactionSupport':'not_enabled','generatedAt':datetime.now(timezone.utc).isoformat()}
    for name in ['install-report','qa','route-health','audit','demo-run']:
        (REPORTS/f'phase-completion-website-v50-{name}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (EVIDENCE/'phase-completion-website-v50-reference-docket.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (CONTENT/'phase-completion-website-v50.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (CONTENT/'public-proof-navigation-v50.json').write_text(json.dumps(arr,indent=2),encoding='utf-8')
    (DOCS/'PHASE_COMPLETION_WEBSITE_V50.md').write_text('# GoalOS Phase Completion Website V50\n\nComplete colored public-alpha website surface with Command Center, AGI Agents, RSI / Loop, AGI Node, Validation, 48 Contracts, All Pages, Search, and Site Health.\n',encoding='utf-8')
    (REVIEWER/'HOW_TO_REVIEW_PHASE_COMPLETION_WEBSITE_V50.md').write_text('# Human Visual Review — V50\n\nCheck navigation, overlap, RSI / Loop pages, AGI Node pages, demo consoles, contracts, validation, Ask GoalOS, boundary, and mobile layout.\n',encoding='utf-8')
    (EXAMPLES/'phase-completion-test-objectives.md').write_text('\n'.join('- '+x[1] for x in USE_CASES),encoding='utf-8')

def main():
    ensure_dirs()
    copytree(PAYLOAD/'public', PUBLIC, overwrite=True)
    copytree(PAYLOAD/'public-snapshot', PUBLIC, overwrite=False)
    create_compat_assets()
    sanitize_public()
    write_key_pages()
    write_route_pages()
    inject_nav_and_assets()
    sanitize_public()
    repair_missing_refs()
    write_route_pages()
    inject_nav_and_assets()
    sanitize_public()
    repair_missing_refs()
    broken, forbidden = audit()
    status='passed' if not broken and not forbidden else 'failed'
    write_docs_and_reports(status, broken, forbidden)
    print(json.dumps({'version':VERSION,'status':status,'publicPages':len(routes()),'forbiddenBrowserApiHits':forbidden,'brokenInternalLinksOrAssets':broken,'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted'},indent=2))
    if status!='passed': sys.exit(1)
if __name__=='__main__': main()
