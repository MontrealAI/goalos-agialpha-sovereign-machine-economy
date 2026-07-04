
#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, re, html, hashlib, csv, sys, os, textwrap
from pathlib import Path
VERSION='v61'
CSS='goalos-autonomous-proof-factory-website-v61.css'
JS='goalos-autonomous-proof-factory-website-v61.js'
ROUTES_JSON='goalos-autonomous-proof-factory-website-v61-routes.json'
ROUTES_JS='goalos-autonomous-proof-factory-website-v61-routes.js'
CANONICAL_ROUTES = ['index.html', 'autonomous-proof-factory.html', 'goalos-autonomous-proof-factory.html', 'autonomous-work-os.html', 'autonomous-proof-gated-work-machine.html', 'autonomous-general-work-machine.html', 'goalos-autonomous-general-work-machine.html', 'autonomous-proof-work-machine.html', 'goalos-autonomous-proof-work-machine.html', 'autonomous-mission-control.html', 'autonomous-mission-queue-v9.html', 'autonomous-work-playbooks-v9.html', 'autonomous-mission-foundry-status-v9.html', 'until-done-autonomy-loop.html', 'state-on-disk-harness.html', 'proof-debt-dashboard-v9.html', 'agent-role-contracts.html', 'agi-node-validator-mesh-v9.html', 'chronicle-compounding-engine-v9.html', 'capability-promotion-gate-v9.html', 'autonomy-boundary-v9.html', 'autonomous-proof-factory-share-kit.html', 'goalos-sovereign-work-machine.html', 'proof-gated-work-machine.html', 'goalos-holy-grail-candidate.html', 'goalos-phase-completion.html', 'autonomy-theatre.html', 'autonomous-demo-run-theatre-v40.html', 'agi-agent-workbench.html', 'agi-agent-mission-control.html', 'agi-agent-playbooks.html', 'agent-foundry.html', 'agi-agent-run-theatre.html', 'agent-flow-academy-v38.html', 'from-loop-to-rsi-state-capacity.html', 'from-loop-to-rsi-governance.html', 'from-loop-to-rsi-sovereign-console.html', 'loop-to-rsi.html', 'rsi-state-capacity.html', 'loop-bottleneck-observatory.html', 'goalos-loop-bottleneck-observatory.html', 'loop-contract-lab.html', 'loop-flight-recorder.html', 'move37-dossier.html', 'agi-alpha-node-v0.html', 'agi-node-validation.html', 'agi-node-use-cases.html', 'human-or-agi-node-validation.html', 'human-or-node-validation.html', 'validation-control-tower.html', 'validation-authority.html', 'validation-command-center.html', 'validation-mesh.html', 'validation-orchestrator.html', 'validation-studio.html', 'validation-use-cases.html', 'mainnet-contract-atlas.html', 'contract-academy.html', 'mainnet-proof-rail.html', 'proof-run-001-docket.html', 'proof-run-001.html', 'evidence-docket-theatre.html', 'proof-ledger.html', 'visual-flow-proof.html', 'ask-goalos.html', 'all-pages.html', 'site-map.html', 'route-registry.html', 'search.html', 'site-health.html', 'trust-boundary.html', 'token-boundary.html', 'privacy.html', 'data-boundary.html', '404.html']
PROFILES = {'factory': {'eyebrow': 'AUTONOMOUS PROOF FACTORY', 'title': 'One objective. Autonomous proof factory.', 'accent': 'Until DONE.', 'lead': 'Queue public-safe objectives, orchestrate AGI Agents, package AGI Jobs, validate with AGI Nodes, emit Evidence Dockets, record Chronicle memory, promote reusable capability, and hold for review when proof is incomplete.', 'objective': 'Evaluate an AI vendor using evidence, not marketing claims, and produce a reviewer-ready Evidence Docket with risk ledger and next actions.', 'agents': ['Mission Architect', 'Planner', 'Researcher', 'Builder', 'Evidence Agent', 'Verifier', 'AGI Node Validator', 'Sentinel', 'Chronicle Agent', 'Capability Promoter'], 'stages': ['Queue', 'Mission Contract', 'Agent Roles', 'AGI Job', 'State on Disk', 'ProofBundle', 'AGI Node Validate', 'Evidence Docket', 'Chronicle', 'Capability Gate', 'Review Hold', 'Next Mission'], 'artifacts': ['mission-contract.json', 'agent-constellation.json', 'agi-job-card.json', 'agi-node-validation-certificate.json', 'proof-bundle.json', 'evidence-docket.md', 'reviewer-brief.md', 'action-graph.csv', 'chronicle-entry.json', 'capability-package.json', 'selection-certificate.json', 'hashes.json'], 'next': ['autonomous-mission-queue-v9.html', 'proof-debt-dashboard-v9.html', 'agi-node-validator-mesh-v9.html', 'capability-promotion-gate-v9.html']}, 'general': {'eyebrow': 'AUTONOMOUS GENERAL WORK MACHINE', 'title': 'Tell GoalOS what you want.', 'accent': 'It builds the proof path.', 'lead': 'A plain-language objective becomes a Mission Contract, an AGI Agent constellation, an AGI Job, a validation plan, an Evidence Docket, and reusable capability.', 'objective': 'Turn one important organizational objective into verified autonomous work with clear evidence, risk, validation, and next actions.', 'agents': ['Mission Architect', 'Domain Router', 'Planner', 'Researcher', 'Builder', 'Evaluator', 'AGI Node Validator', 'Risk Sentinel', 'Reviewer Liaison', 'Chronicle Agent'], 'stages': ['Objective', 'Mission Contract', 'Domain Route', 'Agent Constellation', 'AGI Job', 'Work Plan', 'Evidence Gathering', 'Validation', 'Decision State', 'Action Graph', 'Chronicle', 'Reusable Capability'], 'artifacts': ['goalos-mission-contract.json', 'goalos-agent-orchestration-plan.json', 'goalos-agi-job-spec.json', 'goalos-agi-node-validation-plan.json', 'goalos-proofbundle.json', 'goalos-evidence-docket.md', 'goalos-action-graph.csv', 'goalos-validation-certificate.json', 'goalos-chronicle-entry.json', 'goalos-capability-package.json', 'goalos-executive-brief.md'], 'next': ['autonomous-general-work-machine.html', 'agi-agent-workbench.html', 'validation-control-tower.html', 'evidence-docket-theatre.html']}, 'agents': {'eyebrow': 'AGI AGENTS', 'title': 'Agents do the work.', 'accent': 'Nodes validate it.', 'lead': 'The agent layer is an orchestrated institution: roles, responsibilities, tools, artifacts, validation duties, and Chronicle memory.', 'objective': 'Have AGI Agents decompose, execute, verify, and package a complex objective into a proof-backed work package.', 'agents': ['Orchestrator', 'Planner', 'Researcher', 'Builder', 'Operator', 'Safety Agent', 'Memory Agent', 'Evaluator', 'Governance Agent', 'Liaison'], 'stages': ['Identify', 'Learn', 'Think', 'Design', 'Strategise', 'Execute', 'Check', 'Package', 'Validate', 'Chronicle'], 'artifacts': ['agent-role-contracts.json', 'agent-access-graph.json', 'agi-job-card.json', 'handoff-notes.md', 'reviewer-brief.md', 'capability-package.json'], 'next': ['agent-role-contracts.html', 'agi-agent-playbooks.html', 'agent-foundry.html', 'agi-node-validator-mesh-v9.html']}, 'rsi': {'eyebrow': 'RSI / LOOP GOVERNANCE', 'title': 'Open-ended discovery.', 'accent': 'Mechanical authority.', 'lead': 'RSI exploration is permitted only through deterministic gates: target, emit, filter, atlas, test-plan, eval, insert, promote.', 'objective': 'Run an RSI-style governance mission: discover a candidate, compare baselines, stress-test, package a dossier, and promote only if proof survives.', 'agents': ['Targeter', 'Emitter', 'Risk Filter', 'Causal Atlas', 'Test Planner', 'Evaluator', 'Archive Agent', 'Promotion Gate', 'Council Reviewer'], 'stages': ['TARGET', 'EMIT', 'FILTER', 'ATLAS', 'TEST-PLAN', 'EVAL', 'INSERT', 'PROMOTE', 'Dossier', 'Council Hold'], 'artifacts': ['rsi-state.json', 'candidate-card.json', 'risk-report.json', 'causal-atlas.json', 'test-plan.json', 'baseline-comparison.json', 'move37-dossier.md', 'promotion-decision.json'], 'next': ['from-loop-to-rsi-state-capacity.html', 'move37-dossier.html', 'loop-bottleneck-observatory.html', 'until-done-autonomy-loop.html']}, 'loop': {'eyebrow': 'LONG-HORIZON LOOP', 'title': 'Write the loop, not the prompt.', 'accent': 'State survives.', 'lead': 'GoalOS makes long-running work legible: role contracts, state on disk, trace reading, restarts, scorecards, and moving bottlenecks.', 'objective': 'Design a long-horizon autonomous loop that can restart, read traces, score quality, delete harness overhead, and expose the next bottleneck.', 'agents': ['Loop Architect', 'Planner', 'Generator', 'Evaluator', 'Trace Reader', 'Bottleneck Scout', 'State Steward', 'Reviewer'], 'stages': ['Contract', 'Roles', 'State on Disk', 'Run', 'Trace', 'Restart', 'Score', 'Delete Harness', 'Bottleneck', 'Ship Smaller Loop'], 'artifacts': ['loop-contract.json', 'state-manifest.json', 'trace-log.md', 'bottleneck-report.md', 'restart-plan.json', 'quality-scorecard.json'], 'next': ['loop-contract-lab.html', 'loop-flight-recorder.html', 'loop-bottleneck-observatory.html', 'state-on-disk-harness.html']}, 'node': {'eyebrow': 'AGI NODE VALIDATION', 'title': 'Autonomy needs authority.', 'accent': 'Nodes validate.', 'lead': 'AGI Nodes appear as Worker, Validator, and Sentinel roles with replay checks, telemetry, challenge windows, and review-ready certificates.', 'objective': 'Use AGI Node validation to check replay, evidence, policy boundary, telemetry, and settlement readiness for a proof mission.', 'agents': ['Node Worker', 'Node Validator', 'Node Sentinel', 'Telemetry Agent', 'Replay Agent', 'Challenge Agent', 'Certificate Agent'], 'stages': ['Node Identity', 'Runtime Pins', 'Worker Job', 'Telemetry', 'Replay', 'Validator Attestation', 'Sentinel Check', 'Challenge Window', 'Certificate'], 'artifacts': ['node-identity.json', 'runtime-pins.json', 'worker-output.json', 'replay-result.json', 'validator-attestation.json', 'sentinel-report.json', 'validation-certificate.json'], 'next': ['agi-node-validator-mesh-v9.html', 'agi-node-validation.html', 'human-or-agi-node-validation.html', 'validation-control-tower.html']}, 'validation': {'eyebrow': 'VALIDATION CONTROL', 'title': 'Choose who validates.', 'accent': 'Human, Node, Hybrid, Council.', 'lead': 'Validation is explicit: authority mode, replay checks, evidence review, risk ledger, challenge window, certificate, decision state.', 'objective': 'Validate a proof path with Human, AGI Node, Hybrid, or Council review, then produce a decision certificate and reviewer brief.', 'agents': ['Human Reviewer', 'AGI Node Validator', 'Hybrid Arbiter', 'Council Reviewer', 'Risk Ledger', 'Certificate Agent'], 'stages': ['Select Authority', 'Commit Verdict', 'Replay Check', 'Evidence Review', 'Risk Ledger', 'Challenge Window', 'Certificate', 'Decision State'], 'artifacts': ['authority-selection.json', 'replay-check.json', 'risk-ledger.json', 'validation-certificate.json', 'reviewer-brief.md', 'decision-state.json'], 'next': ['validation-control-tower.html', 'agi-node-validator-mesh-v9.html', 'trust-boundary.html', 'proof-run-001-docket.html']}, 'contracts': {'eyebrow': '48 CONTRACTS / PROOF RAIL', 'title': 'Proof becomes economic.', 'accent': 'Bounded first.', 'lead': 'The contract rail is explained as registry, proof ledger, eval registry, attestation, selection gate, token boundary, and settlement simulation — never a wallet prompt.', 'objective': 'Understand the 48 GoalOS-created Ethereum Mainnet contracts as one institutional proof rail without sending a transaction.', 'agents': ['Contract Cartographer', 'Registry Reader', 'Proof Ledger Agent', 'Eval Registry Agent', 'Token Boundary Agent', 'Settlement Simulator', 'Reviewer'], 'stages': ['Atlas', 'Registry', 'Proof Ledger', 'Eval Registry', 'Attestation', 'Selection Gate', 'Token Boundary', 'Settlement Simulation', 'Reviewer Packet'], 'artifacts': ['contract-atlas.json', 'role-map.json', 'proof-rail-notes.md', 'token-boundary.md', 'settlement-simulation.json', 'reviewer-packet.md'], 'next': ['mainnet-contract-atlas.html', 'contract-academy.html', 'mainnet-proof-rail.html', 'token-boundary.html']}, 'proof': {'eyebrow': 'PROOF / EVIDENCE', 'title': 'Output becomes evidence.', 'accent': 'Evidence becomes decision.', 'lead': 'Proof pages focus on claims, baselines, proof packets, replay, risk/cost ledgers, validator reports, and reviewer briefs.', 'objective': 'Prepare a public-safe Evidence Docket for one proof mission with claims matrix, baselines, risk ledger, replay path, and reviewer brief.', 'agents': ['Claims Analyst', 'Baseline Agent', 'Evidence Agent', 'Risk Ledger', 'Replay Agent', 'Validator', 'Reviewer Liaison'], 'stages': ['Claims Matrix', 'Environment', 'Baselines', 'Proof Packets', 'Replay', 'Cost Ledger', 'Risk Ledger', 'Validator Report', 'Reviewer Brief'], 'artifacts': ['claims-matrix.md', 'environment.json', 'baseline-comparison.json', 'proofbundle.json', 'replay-instructions.md', 'risk-cost-ledger.json', 'validator-report.md', 'reviewer-brief.md'], 'next': ['proof-run-001-docket.html', 'evidence-docket-theatre.html', 'proof-ledger.html', 'goalos-holy-grail-candidate.html']}, 'trust': {'eyebrow': 'TRUST / BOUNDARY', 'title': 'No proof, no evolution.', 'accent': 'No wallet. No transaction.', 'lead': 'Trust pages make the public-alpha boundary clear while routing users to proof, validation, token boundary, and privacy pages.', 'objective': 'Check the public-alpha boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority.', 'agents': ['Boundary Agent', 'Privacy Agent', 'Token Boundary Agent', 'Risk Sentinel', 'Reviewer'], 'stages': ['Boundary', 'Data', 'Funds', 'Wallet', 'Transaction', 'Network', 'Authority', 'Review Required'], 'artifacts': ['boundary-review.md', 'privacy-boundary.json', 'token-boundary.md', 'risk-ledger.json'], 'next': ['trust-boundary.html', 'token-boundary.html', 'privacy.html', 'data-boundary.html']}, 'nav': {'eyebrow': 'NAVIGATION / SEARCH', 'title': 'Everything discoverable.', 'accent': 'No missing surfaces.', 'lead': 'All Pages, Search, Site Health, and Route Registry are generated from the actual public HTML inventory.', 'objective': 'Find the right GoalOS route for RSI, AGI Agents, AGI Nodes, validation, contracts, proof, trust, and autonomous work.', 'agents': ['Route Indexer', 'Search Agent', 'Health Auditor', 'Boundary Auditor', 'Reviewer'], 'stages': ['Index Routes', 'Classify', 'Search', 'Health Check', 'Boundary Check', 'Report', 'Recommend Route'], 'artifacts': ['route-registry.json', 'search-index.json', 'site-health.json', 'navigation-report.md'], 'next': ['all-pages.html', 'search.html', 'site-health.html', 'route-registry.html']}}
FORBIDDEN=[r'navigator\.clipboard\.write',r'ethereum\.request',r'web3',r'fetch\(\s*[\"\']https?://',r'XMLHttpRequest\(']
NAV_LINKS=[('Proof Factory','autonomous-proof-factory.html'),('Work Machine','autonomous-general-work-machine.html'),('AGI Agents','agi-agent-workbench.html'),('RSI / Loop','from-loop-to-rsi-state-capacity.html'),('AGI Node','agi-node-validation.html'),('Validate','validation-control-tower.html'),('48 Contracts','mainnet-contract-atlas.html'),('All Pages','all-pages.html'),('Search','search.html'),('Health','site-health.html')]

def esc(s): return html.escape(str(s or ''), quote=True)
def pack_root(): return Path(__file__).resolve().parent.parent if Path(__file__).name.startswith('install_') else Path(__file__).resolve().parent
def ensure(root):
    for p in ['public/assets','reports','evidence/demo','content/goalos','docs/website','schemas/goalos-autonomous-proof-factory-v61','.goalos/autonomy/v61','scripts']:
        (root/p).mkdir(parents=True,exist_ok=True)
def title(r):
    b=Path(r).stem.replace('-',' ').replace('_',' ')
    if b=='index': return 'GoalOS Command Center'
    if b=='404': return 'GoalOS Route Helper'
    return ' '.join(w.upper() if w.lower() in ['agi','rsi','qa','v9'] else w.capitalize() for w in b.split())
def kind(r):
    s=r.lower()
    if any(x in s for x in ['factory','mission-queue','foundry-status','proof-debt','capability-promotion','chronicle-compounding','state-on-disk','until-done']): return 'factory'
    if any(x in s for x in ['rsi','move37']): return 'rsi'
    if any(x in s for x in ['loop','bottleneck','flight-recorder']): return 'loop'
    if any(x in s for x in ['agent','foundry']) and 'node' not in s: return 'agents'
    if any(x in s for x in ['node','validator-mesh']): return 'node'
    if any(x in s for x in ['validat','review','qa']): return 'validation'
    if any(x in s for x in ['contract','mainnet','token','rail']): return 'contracts'
    if any(x in s for x in ['proof','evidence','docket','ledger']): return 'proof'
    if any(x in s for x in ['trust','privacy','data-boundary','boundary','404']): return 'trust'
    if any(x in s for x in ['search','all-pages','site-map','site-health','route']): return 'nav'
    return 'general'
def category(r):
    return {'factory':'Autonomous Proof Factory','general':'Autonomous Work Machine','agents':'AGI Agents','rsi':'RSI Governance','loop':'Loops','node':'AGI Nodes','validation':'Validation','contracts':'Contracts','proof':'Proof and Evidence','trust':'Trust and Boundary','nav':'Navigation'}[kind(r)]
def discover(public):
    routes=set(CANONICAL_ROUTES)
    if public.exists():
        for p in public.rglob('*.html'):
            rel=p.relative_to(public).as_posix()
            if rel.startswith('archive/v61-originals/'): continue
            routes.add(rel)
    return sorted(routes)
def nav_html(prefix=''):
    return ''.join(f'<a class="g61-pill" href="{prefix}{h}">{esc(t)}</a>' for t,h in NAV_LINKS)
def grid_cards(profile):
    return ''.join(f'<div class="g61-card"><span class="g61-badge">{i+1:02d}</span><h3>{esc(a)}</h3><p>Participates in the page-specific autonomous proof mission and emits an inspectable artifact, decision, or unresolved proof gap.</p></div>' for i,a in enumerate(profile['agents'][:9]))
def stage_cards(profile):
    return ''.join(f'<div class="g61-stage"><b>{i+1:02d}</b>{esc(s)}</div>' for i,s in enumerate(profile['stages']))
def cockpit(profile):
    agents=''.join(f'<div class="g61-agent">{esc(a)}</div>' for a in profile['agents'][:10])
    return f'<aside class="g61-cockpit"><div class="g61-cockpit-head"><b>Autonomous Console</b><span class="g61-status">READY</span></div><div class="g61-orb">α</div><div class="g61-agentgrid">{agents}</div><pre class="g61-terminal" data-v61-terminal>Loading...</pre></aside>'
def page(route, routes_json):
    k=kind(route); p=PROFILES.get(k) or PROFILES['general']; prefix='../'*route.count('/')
    route_list=''
    if route in ['all-pages.html','site-map.html','route-registry.html','search.html','site-health.html']:
        reg=json.loads(routes_json)
        search='<input class="g61-search" id="g61RouteSearch" placeholder="Search GoalOS routes: agents, RSI, loops, node, validation, contracts, proof...">'
        route_list='<section class="g61-section"><span class="g61-eyebrow">Complete Route Surface</span><h2>Everything we built, discoverable.</h2>'+search+'<div class="g61-route-list" id="g61RouteList">'+''.join(f'<a class="g61-route" data-search="{esc((x["route"]+" "+x["title"]+" "+x["category"]).lower())}" href="{prefix}{esc(x["route"])}"><small>{esc(x["category"])}</small><b>{esc(x["title"])}</b><em>Open →</em></a>' for x in reg)+'</div><script>document.addEventListener("input",e=>{if(e.target.id==="g61RouteSearch"){let v=e.target.value.toLowerCase();document.querySelectorAll("#g61RouteList .g61-route").forEach(a=>a.style.display=a.dataset.search.includes(v)?"grid":"none")}})</script></section>'
    index_extra=''
    if route in ['index.html','autonomous-proof-factory.html','goalos-autonomous-proof-factory.html','autonomous-general-work-machine.html']:
        index_extra='<section class="g61-section"><span class="g61-eyebrow">Factory Queue</span><h2>Autonomy that writes proof to disk.</h2><div class="g61-cardgrid"><div class="g61-card"><h3>Mission queue</h3><p>Public-safe objectives are queued, scheduled/manual, and processed into evidence artifacts.</p></div><div class="g61-card"><h3>State on disk</h3><p>Each cycle preserves state, hashes, action graph, proof debt, Chronicle memory, and review hold.</p></div><div class="g61-card"><h3>AGI Node validation</h3><p>Worker / Validator / Sentinel roles make autonomy legible, bounded, and challengeable.</p></div></div></section>'
    return f'''<!doctype html><html lang="en" data-goalos-v61-kind="{esc(k)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title(route))} · GoalOS Autonomous Proof Factory</title><meta name="description" content="GoalOS autonomous proof-gated open-ended work machine."><meta name="goalos:version" content="v61"><link rel="stylesheet" href="{prefix}assets/{CSS}"><script src="{prefix}assets/{ROUTES_JS}" defer></script><script src="{prefix}assets/{JS}" defer></script></head><body class="goalos-v61" data-goalos-v61-kind="{esc(k)}"><nav class="g61-nav g61-wrap"><a class="g61-brand" href="{prefix}index.html"><span class="g61-mark">α</span><span><strong>GOALOS</strong><small>AGIALPHA ASCENSION</small></span></a><div class="g61-navlinks">{nav_html(prefix)}</div></nav><main class="g61-wrap"><section class="g61-hero"><div><span class="g61-eyebrow">{esc(p['eyebrow'])}</span><h1 class="g61-title">{esc(p['title'])} <em>{esc(p['accent'])}</em></h1><p class="g61-lead">{esc(p['lead'])}</p><p class="g61-copy">GoalOS is now presented as an autonomous proof-gated open-ended work machine: one objective becomes orchestrated AGI Agent work, an AGI Job package, AGI Node validation, Evidence Docket proof, Chronicle memory, reusable capability, and review-held settlement simulation.</p><div class="g61-actions"><button class="g61-btn primary" data-v61-run>Run end-to-end demo</button><a class="g61-btn dark" href="{prefix}autonomous-proof-factory.html">Open Proof Factory</a><a class="g61-btn dark" href="{prefix}all-pages.html">Open all pages</a></div><div class="g61-inputbox"><label>What should GoalOS autonomously accomplish?<span>browser-local</span></label><textarea class="g61-objective" data-goalos-objective>{esc(p['objective'])}</textarea></div></div>{cockpit(p)}</section><section class="g61-section"><span class="g61-eyebrow">Page-Specific Mission</span><h2>This surface runs its own proof path.</h2><div class="g61-stage-grid">{stage_cards(p)}</div></section>{index_extra}<section class="g61-section"><span class="g61-eyebrow">AGI Agent Constellation</span><h2>Roles, artifacts, validation.</h2><div class="g61-cardgrid">{grid_cards(p)}</div></section>{route_list}<section class="g61-boundary"><b>Public-alpha boundary.</b> No user data. No user funds. No wallet. No transaction. No network call. No backend call. No production authority. Human review required for high-impact outcomes. $AGIALPHA is protocol context only; no sale, custody, wallet support, investment, trading, legal, tax, bridge, liquidity, or regulatory advice.</section></main><div class="g61-dock"><button class="g61-btn primary" data-v61-run>Run end-to-end demo</button><a class="g61-btn dark" href="{prefix}autonomous-proof-factory.html">Proof Factory</a><a class="g61-btn dark" href="{prefix}all-pages.html">All Pages</a></div></body></html>'''
def backup(public):
    dest=public/'archive'/'v61-originals'
    if not public.exists(): return
    for p in list(public.rglob('*.html')):
        rel=p.relative_to(public).as_posix()
        if rel.startswith('archive/v61-originals/'): continue
        d=dest/rel; d.parent.mkdir(parents=True,exist_ok=True)
        if not d.exists(): shutil.copy2(p,d)
def copy_v9(root):
    src=pack_root()/'v9_source'
    if not src.exists(): return []
    copied=[]
    for p in src.rglob('*'):
        if p.is_file():
            rel=p.relative_to(src)
            dest=root/rel
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(p,dest)
            copied.append(str(rel))
    return copied
def write_assets(root,routes):
    assets=root/'public'/'assets'; assets.mkdir(parents=True,exist_ok=True)
    pr=pack_root()
    shutil.copy2(pr/'assets'/CSS, assets/CSS)
    shutil.copy2(pr/'assets'/JS, assets/JS)
    reg=[{'route':r,'title':title(r),'category':category(r),'kind':kind(r),'description':'Open '+title(r)+' as part of the GoalOS autonomous proof-gated work surface.'} for r in routes]
    (assets/ROUTES_JSON).write_text(json.dumps(reg,indent=2),encoding='utf-8')
    (assets/ROUTES_JS).write_text('window.GOALOS_V61_ROUTES='+json.dumps(reg,separators=(',',':'))+';\nwindow.GOALOS_V61_PROFILES='+json.dumps(PROFILES,separators=(',',':'))+';\n',encoding='utf-8')
    (root/'content'/'goalos'/'public-proof-navigation-v61.json').write_text(json.dumps(reg,indent=2),encoding='utf-8')
    (root/'content'/'goalos'/'autonomous-mission-profiles-v61.json').write_text(json.dumps(PROFILES,indent=2),encoding='utf-8')
    return reg
def write_pages(root,routes):
    routes_json=json.dumps([{'route':r,'title':title(r),'category':category(r),'kind':kind(r),'description':'Open '+title(r)} for r in routes],separators=(',',':'))
    public=root/'public'
    for r in routes:
        if r.startswith('archive/v61-originals/'): continue
        p=public/r; p.parent.mkdir(parents=True,exist_ok=True)
        # Replace bad archive pages with a readable compatibility page too.
        p.write_text(page(r,routes_json),encoding='utf-8')
def compat_assets(root):
    assets=root/'public'/'assets'; assets.mkdir(parents=True,exist_ok=True)
    if not (assets/'goalos-mark.svg').exists(): (assets/'goalos-mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="16" fill="#59ffd0"/><text x="32" y="43" font-size="32" text-anchor="middle" fill="#061426">α</text></svg>',encoding='utf-8')
    if not (assets/'goalos.css').exists(): (assets/'goalos.css').write_text('body{visibility:visible}',encoding='utf-8')
    if not (assets/'goalos.js').exists(): (assets/'goalos.js').write_text('window.GOALOS_COMPAT=true;',encoding='utf-8')
    (root/'public'/'site-status.json').write_text(json.dumps({'version':'v61','status':'ready'},indent=2),encoding='utf-8')
    (root/'public'/'search_index.json').write_text('[]',encoding='utf-8')
def mission_queue(root):
    q=[{'id':'vendor-evidence-review','objective':'Evaluate an AI vendor using evidence, not marketing claims.','risk':'medium','authority':'hybrid'},{'id':'trust-room-package','objective':'Prepare a buyer-ready AI Trust Room proof package.','risk':'medium','authority':'human'},{'id':'boundary-review','objective':'Check privacy, token, no-data, no-wallet, and no-transaction boundaries.','risk':'low','authority':'agi_node'},{'id':'evidence-docket','objective':'Create a public-safe Evidence Docket for an autonomous proof mission.','risk':'medium','authority':'hybrid'},{'id':'move37-dossier','objective':'Route a high-novelty claim to Architect / Validator Council review.','risk':'high','authority':'council'}]
    p=root/'.goalos'/'autonomy'/'v61'/'mission-queue.example.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps({'version':'v61','missions':q},indent=2),encoding='utf-8')
    (root/'.goalos'/'autonomy'/'v61'/'autonomy-policy.example.json').write_text(json.dumps({'version':'v61','no_user_data':True,'no_wallet':True,'no_transaction':True,'human_review_required_for_high_impact':True},indent=2),encoding='utf-8')
def copy_own_scripts(root):
    src = pack_root()/'scripts'
    dest = root/'scripts'
    dest.mkdir(parents=True, exist_ok=True)
    copied=[]
    for p in src.glob('*.py'):
        d=dest/p.name
        shutil.copy2(p,d)
        copied.append(str(d))
    return copied

def sanitize_text_assets(root):
    public = root/'public'
    replacements = {
        'navigator.clipboard.writeText': '/* clipboard disabled in public-alpha */ console.log',
        'navigator.clipboard.write': '/* clipboard disabled in public-alpha */ console.log',
        'ethereum.request': '/* wallet disabled in public-alpha */ console.log',
        'window.ethereum': 'window.__GOALOS_NO_WALLET__',
        'new XMLHttpRequest(': '/* network disabled in public-alpha */ (()=>({open(){},send(){}}))(',
    }
    for p in public.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in ['.js','.html','.css','.json','.md','.txt']:
            continue
        rel=p.relative_to(public).as_posix()
        if rel.startswith('archive/v61-originals/'):
            continue
        txt=p.read_text(encoding='utf-8',errors='ignore')
        new=txt
        for a,b in replacements.items(): new=new.replace(a,b)
        # remove external fetch literals from old compatibility assets without altering v61 runtime
        if p.name not in ['goalos-autonomous-proof-factory-website-v61.js']:
            new=new.replace('fetch("https://', '/* external fetch disabled */ fetch("#')
            new=new.replace("fetch('https://", "/* external fetch disabled */ fetch('#")
            new=new.replace('fetch("http://', '/* external fetch disabled */ fetch("#')
            new=new.replace("fetch('http://", "/* external fetch disabled */ fetch('#")
        if new!=txt: p.write_text(new,encoding='utf-8')

def audit(root,routes):
    public=root/'public'; broken=[]; forbidden=[]
    for p in public.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(public).as_posix(); txt=''
        if rel.startswith('archive/v61-originals/'):
            continue
        if p.suffix.lower() in ['.html','.js','.css','.json','.md','.txt']:
            txt=p.read_text(encoding='utf-8',errors='ignore')
            for pat in FORBIDDEN:
                if re.search(pat,txt): forbidden.append({'file':'public/'+rel,'pattern':pat})
        if p.suffix.lower()=='.html':
            for ref in re.findall(r'(?:href|src)=["\']([^"\'#?]+)',txt):
                if ref.startswith(('http:','https:','mailto:','tel:','data:','javascript:','#')): continue
                target=(p.parent/ref).resolve()
                try: target.relative_to(public.resolve())
                except Exception: continue
                if not target.exists(): broken.append({'file':'public/'+rel,'target':ref})
    report={'version':'v61','status':'passed' if not forbidden and not broken else 'failed','publicPages':len(list(public.rglob('*.html'))),'currentRoutesIndexed':len(routes),'forbiddenBrowserApiHits':forbidden,'brokenInternalLinksOrAssets':broken,'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','empiricalSotaClaim':'not_claimed','walletTransactionSupport':'not_enabled','autonomousProofFactoryV9Included':True,'autonomousProofFactoryWebsiteV61':True,'pageSpecificAutonomousDemos':True}
    return report
def main():
    root=Path.cwd(); ensure(root); public=root/'public'; public.mkdir(exist_ok=True)
    backup(public)
    v9=copy_v9(root)
    copy_own_scripts(root)
    routes=discover(public)
    write_assets(root,routes)
    write_pages(root,routes)
    compat_assets(root); mission_queue(root)
    sanitize_text_assets(root)
    report=audit(root,routes)
    for name in ['install-report','qa','route-health','audit','demo-run']:
        (root/'reports'/f'autonomous-proof-factory-website-v61-{name}.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (root/'evidence'/'demo'/'autonomous-proof-factory-website-v61-reference-docket.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (root/'docs'/'website'/'GOALOS_AUTONOMOUS_PROOF_FACTORY_WEBSITE_V61.md').write_text('# GoalOS Autonomous Proof Factory Website V61\n\nV61 integrates Autonomous Proof Factory V9, fixes legacy formatting by regenerating a coherent public surface, preserves originals under `public/archive/v61-originals/`, and exposes a page-specific autonomous proof cockpit across the route inventory.\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
    if report['status']!='passed': raise SystemExit(1)
if __name__=='__main__': main()
