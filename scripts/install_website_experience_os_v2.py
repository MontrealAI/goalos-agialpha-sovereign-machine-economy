
#!/usr/bin/env python3
from __future__ import annotations
import json, re, html, datetime, hashlib
from pathlib import Path

ROOT = Path.cwd()
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"
DOCS = ROOT / "docs" / "website"
REPORTS = ROOT / "reports"
CONTENT = ROOT / "content" / "goalos"
ISSUES = ROOT / "issue-bodies"
EVIDENCE = ROOT / "evidence" / "demo"

NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

CANONICAL_ROUTES = [
  ("index.html", "Home", "Turn AI work into verified capability.", "start", "new users", "homepage"),
  ("start-here.html", "Start Here", "The simplest path for first-time visitors.", "start", "new users", "onboarding"),
  ("website-operating-system.html", "Website Operating System", "One map for the full GoalOS website.", "start", "all users", "navigation"),
  ("pathfinder.html", "GoalOS Pathfinder", "Choose a role and get the right route through the institution.", "start", "all users", "navigation"),
  ("demo-ecosystem-registry.html", "Demo Ecosystem Registry", "The canonical registry of demos, routes, inputs, outputs, gates, and next states.", "start", "advanced users", "registry"),
  ("site-map.html", "Site Map", "Every public page in one place.", "start", "all users", "navigation"),
  ("proof-experience-atlas.html", "Proof Experience Atlas", "A guided tour through the public proof journey.", "evidence", "all users", "journey"),
  ("proof-ledger.html", "Public Proof Ledger", "A registry of public dockets, reports, pages, and review assets.", "evidence", "reviewers", "ledger"),
  ("proof-run-001-docket.html", "Proof Run 001 Docket", "The first repository-readiness Evidence Docket.", "evidence", "reviewers", "docket"),
  ("proof-run-001-execution-room.html", "Proof Run 001 Execution Room", "The operating room for the first public proof run.", "evidence", "reviewers", "execution"),
  ("external-reviewer-replay-room.html", "External Reviewer Replay Room", "Replay, challenge, accept, reject, revise, or dissent.", "review", "reviewers", "review"),
  ("validator-council-arena.html", "Validator Council Arena", "Trust is not one judge. It is a validator council.", "review", "validators", "validator"),
  ("proof-mission-forge.html", "Proof Mission Forge", "Turn an objective into a proof mission.", "mission", "mission authors", "mission"),
  ("proof-mission-control.html", "Proof Mission Control", "A public operating board for proof mission readiness.", "mission", "mission authors", "mission"),
  ("institutional-deployment-wedge.html", "Institutional Deployment Wedge", "Start with one workflow. Earn the right to scale.", "adoption", "institutions", "adoption"),
  ("value-realization-control-room.html", "Value Realization Control Room", "Verified work becomes allocable capacity.", "adoption", "institutions", "value"),
  ("multi-agent-institution.html", "Multi-Agent Institution", "Not a swarm. An institution.", "core demo", "all users", "demo"),
  ("proof-gradient-lab.html", "Proof Gradient Lab", "No proof, no evolution.", "core demo", "all users", "demo"),
  ("evidence-docket-theatre.html", "Evidence Docket Theatre", "A proof page is not a marketing page.", "core demo", "all users", "demo"),
  ("proof-to-action-command-room.html", "Proof-to-Action Command Room", "The deliverable is a governed decision state.", "core demo", "all users", "demo"),
  ("capability-compounding-lab.html", "Capability Compounding Lab", "Verified work becomes reusable capability.", "core demo", "all users", "demo"),
  ("sovereign-experience-stream-lab.html", "Sovereign Experience Stream Lab", "Proof becomes governed experience.", "core demo", "advanced users", "demo"),
  ("proof-settlement-chronicle-lab.html", "Proof-Settlement Chronicle Lab", "No ProofBundle, no settlement.", "core demo", "advanced users", "demo"),
  ("falsification-gauntlet.html", "Falsification Gauntlet", "Strong claims survive baselines.", "core demo", "reviewers", "demo"),
  ("real-task-benchmark-bridge.html", "Real-Task Benchmark Bridge", "Demos become benchmark-ready evidence.", "benchmark", "reviewers", "benchmark"),
  ("proof-carrying-artifact-foundry.html", "Proof-Carrying Artifact Foundry", "The central object is the Proof-Carrying Artifact.", "advanced demo", "advanced users", "artifact"),
  ("evolution-ledger-control-room.html", "Evolution Ledger Control Room", "The ledger remembers proof, not secrets.", "advanced demo", "advanced users", "ledger"),
  ("proof-backed-upgrade-rights-room.html", "Proof-Backed Upgrade Rights Room", "The artifact earns an upgrade right.", "advanced demo", "institutions", "upgrade"),
  ("open-ended-work-engine.html", "Open-Ended Work Engine", "Generate tasks. Gate descendants.", "advanced demo", "advanced users", "engine"),
  ("action-reason-trace-contract.html", "Action-Reason Trace Contract", "Every action must carry a reason.", "advanced demo", "advanced users", "action"),
  ("frontier-release-room.html", "Frontier Release Room", "An evidence-governed decision room for frontier release governance.", "frontier", "reviewers", "frontier"),
  ("console.html", "Proof Console", "Interactive proof console for GoalOS public-alpha workflows.", "hands-on", "all users", "console"),
  ("try-goalos.html", "Try GoalOS", "Start a safe browser-local GoalOS experience.", "hands-on", "new users", "try"),
  ("docket-builder.html", "Docket Builder", "Build a public-safe Evidence Docket draft in the browser.", "hands-on", "mission authors", "docket"),
  ("proof-flight-demo.html", "Proof Flight Demo", "Watch a proof flight execute through gates.", "hands-on", "new users", "demo"),
  ("agent-constellation-demo.html", "Agent Constellation Demo", "See how roles, validators, and proof gates coordinate.", "hands-on", "all users", "demo"),
  ("proof-card-studio.html", "Proof Card Studio", "Create a public-safe proof card.", "hands-on", "all users", "card"),
  ("local-autopilot-demo.html", "Local Autopilot Demo", "Run a local proof autopilot demonstration.", "hands-on", "developers", "local"),
  ("docs/", "Docs", "Repository documentation, guides, and review paths.", "docs", "developers", "docs"),
  ("privacy.html", "Privacy", "No user data boundary.", "trust", "all users", "trust"),
  ("data-boundary.html", "Data Boundary", "What not to submit, and why.", "trust", "all users", "trust"),
  ("token-boundary.html", "$AGIALPHA Boundary", "Public contract identification only. Not available from us.", "trust", "all users", "trust"),
  ("legal.html", "Legal / Disclaimer", "Public-alpha, claim-bounded legal and safety notices.", "trust", "all users", "trust"),
  ("no-data-no-funds.html", "No Data / No Funds", "The public-alpha operating boundary.", "trust", "all users", "trust"),
]

PATH_OVERRIDES = {
  'meta-agentic-alpha-agi.html': ('META-Agentic α‑AGI', 'The meta-agentic origin surface reimplemented under GoalOS.', 'legacy / canon', 'advanced users', 'canon'),
  'agi-alpha-node-v0.html': ('AGI Alpha Node v0', 'The sovereign node theatre and node-runtime concept surface.', 'legacy / canon', 'advanced users', 'node'),
  'agi-jobs-v0-v2.html': ('AGI Jobs v0/v2', 'The AGI Jobs proof-settlement work OS concept surface.', 'legacy / canon', 'advanced users', 'jobs'),
  'research-spine.html': ('Research Spine', 'The paper-to-product canon for GoalOS.', 'docs', 'researchers', 'research'),
  'paper-to-product.html': ('Paper to Product', 'How the papers map into repository and website surfaces.', 'docs', 'researchers', 'research'),
  'mission-os-canon.html': ('Mission OS Canon', 'The Proof OS for autonomous AI work.', 'docs', 'researchers', 'mission-os'),
  'proof-of-evolution.html': ('Proof-of-Evolution Constitution', 'AEP-001: proof before evolution.', 'docs', 'researchers', 'aep'),
  'trust-center.html': ('Trust Center', 'Boundaries, privacy, security, token, and human review.', 'trust', 'all users', 'trust'),
}

SECTION_ORDER = ['start','evidence','review','mission','core demo','advanced demo','benchmark','adoption','frontier','hands-on','legacy / canon','docs','trust','additional']

PUBLIC.mkdir(exist_ok=True)
ASSETS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)
CONTENT.mkdir(parents=True, exist_ok=True)
ISSUES.mkdir(parents=True, exist_ok=True)
EVIDENCE.mkdir(parents=True, exist_ok=True)

# Optional backup of previous homepage. Never overwrite if it already exists.
archive = PUBLIC / 'archive'
archive.mkdir(exist_ok=True)
prev = PUBLIC / 'index.html'
backup = archive / 'index-before-website-experience-os-v2.html'
if prev.exists() and not backup.exists():
    backup.write_text(prev.read_text(encoding='utf-8'), encoding='utf-8')

existing_pages = sorted(p for p in PUBLIC.glob('*.html') if p.is_file())
existing_names = {p.name for p in existing_pages}

routes = []
seen = set()
for path, title, desc, category, audience, role in CANONICAL_ROUTES:
    is_dir = path.endswith('/')
    exists = (PUBLIC / path).exists() if not is_dir else True
    if is_dir:
        exists = True
    routes.append({
        'path': path,
        'title': title,
        'description': desc,
        'category': category,
        'audience': audience,
        'role': role,
        'status': 'live' if exists else 'expected',
        'inputs': infer_inputs(role, title) if False else [],
        'outputs': [],
        'gates': [],
        'nextState': ''
    })
    seen.add(path)

# Helper maps for registry richness.
def classify_page(name: str):
    if name in PATH_OVERRIDES:
        title, desc, cat, aud, role = PATH_OVERRIDES[name]
        return title, desc, cat, aud, role
    stem = name[:-5].replace('-', ' ').strip().title()
    title = stem
    desc = f"Public page: {stem}."
    cat = 'additional'
    aud = 'all users'
    role = 'page'
    lowered = name.lower()
    if 'privacy' in lowered or 'legal' in lowered or 'boundary' in lowered or 'token' in lowered:
        cat, role = 'trust', 'trust'
        desc = 'Trust, privacy, legal, data, token, or public-alpha boundary page.'
    elif 'proof' in lowered or 'docket' in lowered or 'ledger' in lowered:
        cat, role = 'evidence', 'evidence'
        desc = 'Evidence, proof, ledger, or docket page.'
    elif 'mission' in lowered:
        cat, role = 'mission', 'mission'
        desc = 'Mission creation, mission control, or proof-mission path.'
    elif 'review' in lowered or 'validator' in lowered:
        cat, role = 'review', 'review'
        desc = 'Reviewer, validator, or independent inspection page.'
    elif 'demo' in lowered or 'lab' in lowered or 'room' in lowered or 'arena' in lowered:
        cat, role = 'advanced demo', 'demo'
        desc = 'Interactive public-alpha GoalOS demonstration.'
    elif 'doc' in lowered or 'research' in lowered or 'canon' in lowered:
        cat, role = 'docs', 'docs'
        desc = 'Research, documentation, or canon page.'
    return title, desc, cat, aud, role

def enrich(route):
    r = dict(route)
    role = r.get('role','page')
    title = r.get('title','')
    category = r.get('category','additional')
    gates_common = ['No user data', 'No user funds', 'Human review required', 'Claim boundary']
    r['inputs'] = {
        'mission': ['Plain-language objective', 'risk class', 'source boundary', 'required evidence'],
        'docket': ['Claim under review', 'claims matrix', 'evidence packets', 'review boundary'],
        'review': ['Evidence Docket', 'claims matrix', 'replay path', 'validator notes'],
        'validator': ['ProofBundle', 'replay trace', 'validator quorum', 'dissent status'],
        'ledger': ['Proof roots', 'attestations', 'selection certificate', 'rollback receipt'],
        'artifact': ['Artifact candidate', 'proof history', 'scope', 'rollback target'],
        'upgrade': ['Candidate artifact', 'requested scope', 'proof gates', 'challenge window'],
        'action': ['Objective', 'permission scope', 'reason', 'expected observation'],
        'engine': ['Seed objective', 'generation scenario', 'validator gates', 'risk boundary'],
        'benchmark': ['Task family', 'claim under test', 'baseline ladder', 'replay requirements'],
        'value': ['Capability candidate', 'verified work strength', 'allocation policy', 'risk pressure'],
        'adoption': ['Repeatable workflow', 'evidence readiness', 'canary plan', 'rollback maturity'],
        'demo': ['Scenario preset', 'gate toggles', 'risk controls', 'browser-local run'],
        'trust': ['Policy question', 'public-alpha boundary', 'no-data/no-funds confirmation'],
        'navigation': ['User role', 'goal', 'preferred route'],
        'homepage': ['User intent', 'site path'],
        'journey': ['User role', 'proof journey station'],
        'registry': ['Search query', 'workflow category'],
        'console': ['Mission preset', 'proof gate route'],
        'try': ['Public-safe demo choice'],
        'card': ['Proof card content', 'claim boundary'],
        'local': ['Local runtime context', 'no-secrets environment'],
        'docs': ['Reader role', 'documentation path'],
        'research': ['Paper/canon question'],
        'aep': ['Protocol concept', 'object lifecycle'],
        'mission-os': ['Objective-to-proof concept'],
        'node': ['Node runtime concept'],
        'jobs': ['Job/settlement concept'],
        'canon': ['Legacy system concept'],
    }.get(role, ['Public-safe user intent'])
    r['outputs'] = {
        'mission': ['Mission Contract', 'Evidence Docket plan', 'Validator Packet', 'GitHub-ready issue'],
        'docket': ['Evidence Docket', 'Claims Matrix', 'Review Checklist', 'Governed Decision State'],
        'review': ['Reviewer Report', 'Replay Checklist', 'Dissent Memo', 'Verdict'],
        'validator': ['Validator Attestation', 'Challenge Record', 'Dissent Memo', 'Evidence Docket'],
        'ledger': ['Public Ledger Entry', 'Selection Certificate', 'Rollback Receipt', 'Boundary Map'],
        'artifact': ['Proof-Carrying Artifact JSON', 'Selection Certificate', 'Rollback Receipt'],
        'upgrade': ['Upgrade Right JSON', 'Selection Certificate', 'Rollback Receipt'],
        'action': ['Trace Contract', 'Action Graph', 'Rollback Playbook', 'Evidence Pointer Map'],
        'engine': ['Generated Mission Set', 'Validator Lattice', 'Proof Template Pack'],
        'benchmark': ['Benchmark Plan', 'Baseline Matrix CSV', 'Evidence Docket Plan'],
        'value': ['Value Realization Ledger', 'Capacity Allocation Plan', 'Reviewer Brief'],
        'adoption': ['Deployment Plan', 'GoalOSCommit', 'Canary Monitor', 'Rollback Playbook'],
        'demo': ['Evidence Docket sample', 'review brief', 'proof artifacts'],
        'trust': ['Boundary understanding', 'safe next step'],
        'navigation': ['Recommended route', 'page links'],
        'homepage': ['Route to Start / Atlas / Registry / Docket'],
        'journey': ['Ordered proof journey'],
        'registry': ['Route matrix', 'canonical URL list'],
        'docs': ['Guide', 'checklist', 'safe contribution path'],
    }.get(role, ['Public-safe page output'])
    if role in ['mission','docket','review','validator','ledger','artifact','upgrade','action','engine','benchmark','value','adoption','demo']:
        r['gates'] = gates_common + ['Replay path', 'Evidence Docket', 'Risk boundary']
    elif category == 'trust':
        r['gates'] = ['No user data', 'No user funds', 'No wallet', 'No transaction', 'No advice']
    else:
        r['gates'] = gates_common
    r['nextState'] = {
        'mission': 'MISSION_READY_FOR_REVIEW', 'docket': 'DOCKET_REVIEW_READY', 'review': 'ACCEPT_REJECT_REVISE_OR_DISSENT',
        'validator': 'VALIDATION_REVIEW_READY', 'ledger': 'LEDGER_REVIEW_READY', 'artifact': 'ARTIFACT_REVIEW_READY',
        'upgrade': 'UPGRADE_RIGHT_REVIEW_READY', 'action': 'ACTION_REVIEW_READY', 'engine': 'ENGINE_REVIEW_READY',
        'benchmark': 'EMPIRICAL_BRIDGE_READY', 'value': 'VALUE_REALIZATION_REVIEW_READY', 'adoption': 'CANARY_READY',
        'demo': 'HUMAN_REVIEW_REQUIRED', 'trust': 'BOUNDARY_CONFIRMED', 'navigation': 'ROUTE_SELECTED',
        'homepage': 'USER_PATH_SELECTED', 'journey': 'PROOF_JOURNEY_SELECTED', 'registry': 'ROUTE_DISCOVERED',
        'docs': 'GUIDE_SELECTED'
    }.get(role, 'PUBLIC_ALPHA_REVIEW')
    return r

# add all actual public html pages not already canonical
for p in existing_pages:
    if p.name not in seen:
        title, desc, cat, aud, role = classify_page(p.name)
        routes.append({'path': p.name, 'title': title, 'description': desc, 'category': cat, 'audience': aud, 'role': role, 'status':'live'})
        seen.add(p.name)

# ensure generated pages are listed live
for name, title, desc, cat, aud, role in [
    ('website-operating-system.html','Website Operating System','One map for the full GoalOS website.','start','all users','navigation'),
    ('pathfinder.html','GoalOS Pathfinder','Choose a role and get the right route through the institution.','start','all users','navigation'),
    ('site-map.html','Site Map','Every public page in one place.','start','all users','navigation'),
    ('trust-boundary.html','Trust Boundary','No user data, no user funds, no wallet, no transaction, human review required.','trust','all users','trust'),
]:
    if name not in seen:
        routes.append({'path': name,'title':title,'description':desc,'category':cat,'audience':aud,'role':role,'status':'live'})
        seen.add(name)

routes = [enrich(r) for r in routes]
# Sort by section order then title; homepage first
order = {c:i for i,c in enumerate(SECTION_ORDER)}
routes.sort(key=lambda r: (0 if r['path']=='index.html' else 1, order.get(r['category'], 99), r['title'].lower()))
for i,r in enumerate(routes,1):
    r['id'] = f"GOALOS-ROUTE-{i:03d}"

live_routes = [r for r in routes if r.get('status') == 'live']
core_demo_titles = [r for r in routes if r['category'] in ['core demo','advanced demo','benchmark','adoption'] and r.get('status')=='live']

site_meta = {
    'generatedAt': NOW,
    'generator': 'scripts/install_website_experience_os_v2.py',
    'routeCount': len(routes),
    'liveRouteCount': len(live_routes),
    'coreDemoCount': len(core_demo_titles),
    'boundary': ['No user data', 'No user funds', 'No wallet', 'No transaction', 'No network call', 'No production authority', 'Human review required'],
    'canonicalJourney': [
        'Start Here','Proof Experience Atlas','Demo Ecosystem Registry','Public Proof Ledger','Proof Mission Forge','Proof Mission Control','Proof Run 001 Docket','External Reviewer Replay Room'
    ]
}

(ASSETS/'goalos-site-index-data-v2.js').write_text('window.GOALOS_SITE_META = '+json.dumps(site_meta, indent=2)+';\nwindow.GOALOS_SITE_ROUTES = '+json.dumps(routes, indent=2)+';\n', encoding='utf-8')
(CONTENT/'website-experience-os-v2.json').write_text(json.dumps({'meta': site_meta, 'routes': routes}, indent=2), encoding='utf-8')
(CONTENT/'public-proof-navigation.json').write_text(json.dumps({'generatedAt': NOW, 'primaryPath': ['index.html','proof-experience-atlas.html','demo-ecosystem-registry.html','proof-ledger.html','proof-run-001-docket.html','external-reviewer-replay-room.html'], 'routes': routes}, indent=2), encoding='utf-8')

css = r'''
:root{--bg:#030812;--panel:rgba(14,23,36,.76);--panel2:rgba(24,39,58,.68);--line:rgba(180,215,255,.22);--text:#f7fbff;--muted:#c8d5e6;--soft:#91a7bd;--gold:#ffe96f;--mint:#62ffd6;--cyan:#83d9ff;--violet:#b799ff;--pink:#ff78b5;--danger:#ff6b9d;--ok:#6cffb6;--shadow:0 30px 90px rgba(0,0,0,.45);--radius:28px;--max:1280px}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 20% 20%,rgba(28,121,122,.30),transparent 34%),radial-gradient(circle at 78% 12%,rgba(61,87,148,.25),transparent 35%),linear-gradient(135deg,#071d20,#050913 55%,#03050b);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;line-height:1.45;min-height:100vh;overflow-x:hidden}.grid-bg:before{content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:48px 48px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.9),rgba(0,0,0,.15));}.grid-bg:after{content:"GOALOS";position:fixed;left:-2vw;bottom:-12vh;font-weight:1000;font-size:22vw;letter-spacing:-.08em;color:rgba(255,255,255,.035);pointer-events:none}.shell{width:min(var(--max),calc(100% - 40px));margin:0 auto}.nav{position:sticky;top:18px;z-index:20;margin:28px auto 0;width:min(var(--max),calc(100% - 40px));display:flex;align-items:center;justify-content:space-between;padding:16px 22px;background:rgba(3,8,18,.82);border:1px solid var(--line);border-radius:24px;box-shadow:var(--shadow);backdrop-filter:blur(18px)}.brand{display:flex;align-items:center;gap:13px;text-decoration:none;color:var(--text);min-width:max-content}.mark{width:42px;height:42px;border-radius:14px;background:radial-gradient(circle at 35% 30%,var(--gold),var(--mint) 35%,var(--cyan) 62%,var(--violet));box-shadow:0 0 32px rgba(98,255,214,.35)}.brand b{display:block;letter-spacing:.22em;font-size:14px}.brand span{display:block;color:var(--muted);letter-spacing:.24em;font-size:10px}.links{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end}.links a,.mini-btn{border:0;color:var(--text);text-decoration:none;font-weight:800;font-size:13px;padding:11px 13px;border-radius:999px;background:transparent;cursor:pointer}.links a:hover,.mini-btn:hover,.links a.active{background:rgba(255,255,255,.10)}.hero{display:grid;grid-template-columns:1.1fr .85fr;gap:64px;align-items:center;min-height:calc(100vh - 130px);padding:80px 0 46px}.eyebrow{color:var(--gold);font-size:13px;letter-spacing:.45em;text-transform:uppercase;font-weight:1000}.hero h1{font-size:clamp(58px,8.2vw,124px);line-height:.86;letter-spacing:-.085em;margin:26px 0 24px}.hero em{font-family:Georgia,serif;font-weight:500;font-style:italic;background:linear-gradient(90deg,var(--gold),var(--mint),var(--cyan),var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent}.lead{font-size:clamp(18px,2vw,28px);font-weight:850;letter-spacing:-.04em;margin:0 0 20px}.copy{font-size:18px;color:var(--muted);max-width:760px}.actions{display:flex;gap:12px;flex-wrap:wrap;margin:28px 0}.btn{display:inline-flex;align-items:center;gap:10px;padding:14px 19px;border-radius:999px;background:linear-gradient(90deg,#ffef75,#70ffd7);color:#06111b;text-decoration:none;font-weight:1000;border:0;box-shadow:0 14px 40px rgba(97,255,214,.15);cursor:pointer}.btn.secondary{background:rgba(255,255,255,.10);color:var(--text);border:1px solid var(--line);box-shadow:none}.btn.small{padding:10px 13px;font-size:13px}.boundary{border:1px solid rgba(255,107,157,.55);background:rgba(70,12,36,.42);border-radius:18px;padding:14px 18px;color:#fff;font-weight:800;max-width:780px}.orb-card{min-height:330px;border:1px solid var(--line);border-radius:32px;background:linear-gradient(135deg,rgba(255,255,255,.16),rgba(255,255,255,.04));box-shadow:var(--shadow);position:relative;overflow:hidden;display:grid;place-items:center}.orb-card:before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:32px 32px}.orbit{position:relative;width:min(330px,80%);aspect-ratio:1}.core{position:absolute;inset:34%;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 35% 25%,var(--gold),var(--mint) 35%,var(--cyan) 62%,var(--violet));font-size:64px;font-weight:1000;color:#031018;box-shadow:0 0 68px rgba(98,255,214,.35)}.ring{position:absolute;inset:5%;border:1px dashed rgba(255,233,111,.45);border-radius:50%;animation:spin 28s linear infinite}.node{position:absolute;width:48px;height:48px;border-radius:50%;display:grid;place-items:center;background:#04111d;border:1px solid rgba(98,255,214,.55);font-weight:1000;box-shadow:0 0 22px rgba(98,255,214,.18)}.n1{left:43%;top:-2%}.n2{right:2%;top:20%}.n3{right:2%;bottom:20%}.n4{left:43%;bottom:-2%}.n5{left:2%;bottom:20%}.n6{left:2%;top:20%}@keyframes spin{to{transform:rotate(360deg)}}.stats{display:grid;grid-template-columns:repeat(6,1fr);border:1px solid var(--line);border-radius:24px;overflow:hidden;background:rgba(255,255,255,.08);margin:20px 0 74px}.stat{padding:22px 24px;border-right:1px solid var(--line)}.stat:last-child{border-right:0}.stat strong{display:block;color:var(--gold);font-size:38px;line-height:1}.stat span{font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:var(--muted);font-weight:1000}.section{padding:34px 0}.section-head{display:flex;justify-content:space-between;align-items:end;gap:24px;margin-bottom:18px}.section h2{font-size:clamp(34px,4vw,66px);line-height:.94;letter-spacing:-.07em;margin:0}.section p{color:var(--muted)}.path-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.card,.wide-card{border:1px solid var(--line);background:linear-gradient(135deg,var(--panel),rgba(255,255,255,.045));border-radius:24px;padding:24px;box-shadow:0 18px 70px rgba(0,0,0,.24)}.card h3,.wide-card h3{font-size:24px;line-height:1;margin:0 0 10px;letter-spacing:-.04em}.card p{min-height:72px}.tag{display:inline-flex;align-items:center;gap:6px;color:var(--gold);font-size:11px;text-transform:uppercase;letter-spacing:.28em;font-weight:1000;margin-bottom:14px}.journey{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.route-card{position:relative;min-height:210px}.route-card .num{color:var(--mint);font-weight:1000}.route-card a{position:absolute;bottom:20px;left:24px}.filters{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0 22px}.filter{padding:10px 13px;border-radius:999px;background:rgba(255,255,255,.08);color:var(--text);border:1px solid var(--line);font-weight:900;cursor:pointer}.filter.active{background:linear-gradient(90deg,var(--gold),var(--mint));color:#06111b}.registry-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.route-list-card{padding:18px;border-radius:18px;background:rgba(255,255,255,.065);border:1px solid var(--line)}.route-list-card h4{margin:0 0 6px}.route-list-card p{font-size:14px;margin:0 0 12px}.searchbox{width:100%;padding:16px 18px;border-radius:18px;border:1px solid var(--line);background:rgba(0,0,0,.25);color:var(--text);font-size:16px;font-weight:800}.trust-band{display:grid;grid-template-columns:1fr 1fr;gap:18px}.footer{padding:60px 0 80px;color:var(--soft)}.palette{position:fixed;inset:0;display:none;z-index:50;background:rgba(0,0,0,.58);backdrop-filter:blur(12px);padding:8vh 20px}.palette.open{display:block}.palette-panel{width:min(880px,100%);margin:0 auto;background:#06101d;border:1px solid var(--line);border-radius:28px;box-shadow:var(--shadow);overflow:hidden}.palette-head{padding:18px;border-bottom:1px solid var(--line)}.palette input{width:100%;padding:18px;border-radius:16px;border:1px solid var(--line);background:#0b1626;color:var(--text);font-size:20px;font-weight:900}.palette-results{max-height:58vh;overflow:auto;padding:10px}.palette-results a{display:block;text-decoration:none;color:var(--text);padding:14px;border-radius:16px}.palette-results a:hover{background:rgba(255,255,255,.08)}.palette-results small{display:block;color:var(--muted)}.float-map{position:fixed;right:22px;bottom:22px;z-index:15}@media(max-width:1000px){.hero{grid-template-columns:1fr}.path-grid,.journey,.registry-grid,.trust-band{grid-template-columns:1fr 1fr}.stats{grid-template-columns:repeat(3,1fr)}}@media(max-width:680px){.nav{align-items:flex-start;gap:16px;flex-direction:column}.hero h1{font-size:64px}.path-grid,.journey,.registry-grid,.trust-band{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.stat{border-bottom:1px solid var(--line)}}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
'''
(ASSETS/'goalos-website-os-v2.css').write_text(css, encoding='utf-8')

js = r'''
(function(){
  const routes = window.GOALOS_SITE_ROUTES || [];
  const meta = window.GOALOS_SITE_META || {};
  const $ = (s,root=document)=>root.querySelector(s);
  const $$ = (s,root=document)=>Array.from(root.querySelectorAll(s));
  function routeUrl(path){ return path.endsWith('/') ? path : path; }
  function card(route){
    const status = route.status === 'live' ? '' : ' · expected';
    return `<article class="route-list-card" data-category="${route.category}" data-search="${[route.title,route.description,route.category,route.audience,route.role].join(' ').toLowerCase()}">
      <h4>${route.title}</h4><p>${route.description}</p><small>${route.category} · ${route.audience}${status}</small><br>
      ${route.status==='live'?`<a class="btn small secondary" href="${routeUrl(route.path)}">Open</a>`:`<span class="btn small secondary" aria-disabled="true">Expected</span>`}
    </article>`;
  }
  function renderRegistry(){
    const host = $('#routeRegistry');
    if(!host) return;
    host.innerHTML = routes.filter(r=>r.path!=='index.html').map(card).join('');
    const count = $('#routeCount'); if(count) count.textContent = routes.filter(r=>r.status==='live').length;
  }
  function applyFilter(cat){
    $$('.filter').forEach(b=>b.classList.toggle('active', b.dataset.filter===cat));
    const q = ($('#routeSearch')?.value || '').toLowerCase().trim();
    $$('.route-list-card').forEach(c=>{
      const okCat = cat==='all' || c.dataset.category===cat;
      const okQ = !q || c.dataset.search.includes(q);
      c.style.display = okCat && okQ ? '' : 'none';
    });
  }
  function setupFilters(){
    if(!$('#routeRegistry')) return;
    $$('.filter').forEach(b=>b.addEventListener('click',()=>applyFilter(b.dataset.filter)));
    $('#routeSearch')?.addEventListener('input',()=>{
      const active = $('.filter.active')?.dataset.filter || 'all'; applyFilter(active);
    });
    applyFilter('all');
  }
  function openPalette(){ $('.palette')?.classList.add('open'); $('#paletteInput')?.focus(); renderPalette(''); }
  function closePalette(){ $('.palette')?.classList.remove('open'); }
  function renderPalette(q){
    const box = $('#paletteResults'); if(!box) return;
    const query = (q||'').toLowerCase().trim();
    const hits = routes.filter(r=>r.status==='live' && (!query || [r.title,r.description,r.category,r.audience,r.role].join(' ').toLowerCase().includes(query))).slice(0,40);
    box.innerHTML = hits.map(r=>`<a href="${routeUrl(r.path)}"><b>${r.title}</b><small>${r.description} · ${r.category}</small></a>`).join('') || '<div style="padding:18px;color:var(--muted)">No route found.</div>';
  }
  function setupPalette(){
    document.addEventListener('keydown', e=>{
      if(e.key==='/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();openPalette();}
      if(e.key==='Escape') closePalette();
    });
    $$('[data-open-palette]').forEach(b=>b.addEventListener('click',openPalette));
    $('.palette')?.addEventListener('click',e=>{ if(e.target.classList.contains('palette')) closePalette(); });
    $('#paletteInput')?.addEventListener('input',e=>renderPalette(e.target.value));
  }
  function setupPathfinder(){
    const select = $('#roleSelect'); const out = $('#roleRoute'); if(!select || !out) return;
    const paths = {
      new: ['start-here.html','proof-experience-atlas.html','try-goalos.html','demo-ecosystem-registry.html'],
      reviewer: ['proof-run-001-docket.html','proof-ledger.html','external-reviewer-replay-room.html','validator-council-arena.html'],
      mission: ['proof-mission-forge.html','proof-mission-control.html','proof-run-001-execution-room.html','evidence-docket-theatre.html'],
      developer: ['website-operating-system.html','demo-ecosystem-registry.html','action-reason-trace-contract.html','docs/'],
      institution: ['institutional-deployment-wedge.html','value-realization-control-room.html','proof-backed-upgrade-rights-room.html','trust-boundary.html']
    };
    function render(){
      const ids = paths[select.value] || paths.new;
      out.innerHTML = ids.map((p,i)=>{ const r=routes.find(x=>x.path===p)||{title:p,description:'Open page',path:p,status:'live'}; return `<article class="route-list-card"><div class="tag">Step ${i+1}</div><h4>${r.title}</h4><p>${r.description}</p><a class="btn small" href="${r.path}">Open</a></article>`; }).join('');
    }
    select.addEventListener('change',render); render();
  }
  document.addEventListener('DOMContentLoaded',()=>{renderRegistry(); setupFilters(); setupPalette(); setupPathfinder();});
})();
'''
(ASSETS/'goalos-website-os-v2.js').write_text(js, encoding='utf-8')

# HTML helpers
nav_links = [
    ('index.html','Start'),('proof-experience-atlas.html','Atlas'),('proof-ledger.html','Proof Ledger'),('proof-run-001-docket.html','Proof Run 001'),('demo-ecosystem-registry.html','Registry'),('external-reviewer-replay-room.html','Reviewer Room')
]
def nav(active=''):
    links = ''.join(f'<a class="{"active" if href==active else ""}" href="{href}">{label}</a>' for href,label in nav_links)
    return f'''<nav class="nav"><a class="brand" href="index.html"><span class="mark"></span><span><b>GOALOS</b><span>AGIALPHA ASCENSION</span></span></a><div class="links">{links}<button class="mini-btn" data-open-palette>Search</button></div></nav>'''

def palette():
    return '''<div class="palette" role="dialog" aria-modal="true" aria-label="GoalOS site command palette"><div class="palette-panel"><div class="palette-head"><input id="paletteInput" placeholder="Search GoalOS pages, demos, proof rooms, trust boundaries…" aria-label="Search site routes"></div><div id="paletteResults" class="palette-results"></div></div></div>'''

def html_doc(title, body, active=''):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="GoalOS AGIALPHA Ascension — Sovereign Machine Economy"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="AI creates output. GoalOS creates proof."><meta property="og:image" content="assets/social-preview.svg"><link rel="stylesheet" href="assets/goalos-website-os-v2.css"></head><body class="grid-bg">{nav(active)}<main>{body}</main><a class="btn small float-map" href="website-operating-system.html">Open site map</a>{palette()}<script src="assets/goalos-site-index-data-v2.js"></script><script src="assets/goalos-website-os-v2.js"></script></body></html>'''

def section_cards(cat, limit=None):
    items = [r for r in routes if r['category']==cat and r['status']=='live']
    if limit: items = items[:limit]
    return ''.join(f'''<article class="route-card card"><div class="tag">{html.escape(r['category'])}</div><h3>{html.escape(r['title'])}</h3><p>{html.escape(r['description'])}</p><a class="btn small secondary" href="{html.escape(r['path'])}">Open</a></article>''' for r in items)

journey_paths = ['multi-agent-institution.html','proof-gradient-lab.html','evidence-docket-theatre.html','proof-to-action-command-room.html','capability-compounding-lab.html','sovereign-experience-stream-lab.html','proof-settlement-chronicle-lab.html','falsification-gauntlet.html','real-task-benchmark-bridge.html','proof-carrying-artifact-foundry.html','evolution-ledger-control-room.html','proof-backed-upgrade-rights-room.html','institutional-deployment-wedge.html','value-realization-control-room.html','open-ended-work-engine.html','validator-council-arena.html','action-reason-trace-contract.html']
journey = [r for p in journey_paths for r in routes if r['path']==p and r['status']=='live']
journey_html = ''.join(f'''<article class="route-card card"><div class="num">{i:02d}</div><h3>{html.escape(r['title'])}</h3><p>{html.escape(r['description'])}</p><a class="btn small secondary" href="{html.escape(r['path'])}">Open station</a></article>''' for i,r in enumerate(journey,1))

index_body = f'''
<section class="hero shell"><div><div class="eyebrow">GoalOS AGIALPHA Ascension · Sovereign Machine Economy</div><h1>Turn AI work into <em>verified capability.</em></h1><p class="lead">A model can answer. An agent can act. An institution must prove.</p><p class="copy">GoalOS is the proof-governed operating regime for autonomous AI work: Mission Contracts, Evidence Dockets, validator review, governed decision states, Chronicle memory, capability packages, public proof ledgers, and human-review boundaries.</p><div class="actions"><a class="btn" href="start-here.html">Start Here</a><a class="btn secondary" href="proof-experience-atlas.html">Open the Atlas</a><a class="btn secondary" href="proof-run-001-docket.html">Review Proof Run 001</a><a class="btn secondary" href="demo-ecosystem-registry.html">Demo Registry</a></div><div class="boundary"><b>PUBLIC-ALPHA BOUNDARY</b> &nbsp; No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.</div></div><div class="orb-card" aria-label="Institutional intelligence orbit"><div class="orbit"><div class="ring"></div><div class="core">α</div><div class="node n1">M1</div><div class="node n2">R2</div><div class="node n3">V3</div><div class="node n4">S6</div><div class="node n5">P6</div><div class="node n6">N8</div></div></div></section>
<section class="shell stats"><div class="stat"><strong>1</strong><span>Institution</span></div><div class="stat"><strong>{len(live_routes)}</strong><span>Live pages</span></div><div class="stat"><strong>{len(journey)}</strong><span>Core demos</span></div><div class="stat"><strong>0</strong><span>External actions</span></div><div class="stat"><strong>∞</strong><span>Mission space</span></div><div class="stat"><strong>1</strong><span>Human boundary</span></div></section>
<section class="section shell"><div class="section-head"><div><div class="eyebrow">Choose your path</div><h2>A spectacular launch becomes a usable institution.</h2><p>Start with a guided route: understand GoalOS, try browser-local demos, inspect dockets, replay the proof path, or propose a mission.</p></div><button class="btn secondary" data-open-palette>Search all pages</button></div><div class="path-grid">
<article class="card"><div class="tag">New user</div><h3>Understand GoalOS</h3><p>Learn what GoalOS does, what it does not do, and where to click first.</p><a class="btn small" href="start-here.html">Start here</a></article>
<article class="card"><div class="tag">Reviewer</div><h3>Inspect proof</h3><p>Open Proof Run 001, the Public Proof Ledger, and the External Reviewer Replay Room.</p><a class="btn small" href="proof-run-001-docket.html">Review docket</a></article>
<article class="card"><div class="tag">Mission</div><h3>Forge a proof mission</h3><p>Convert a public-safe objective into a Mission Contract and Evidence Docket plan.</p><a class="btn small" href="proof-mission-forge.html">Forge mission</a></article>
<article class="card"><div class="tag">Institution</div><h3>Start with one workflow</h3><p>Use the deployment wedge to earn limited, review-ready expansion.</p><a class="btn small" href="institutional-deployment-wedge.html">Open wedge</a></article>
</div></section>
<section class="section shell"><div class="section-head"><div><div class="eyebrow">Public proof journey</div><h2>The demos now form one route.</h2><p>Each station demonstrates one GoalOS primitive. No page is removed; the registry and site map preserve everything.</p></div><a class="btn secondary" href="demo-ecosystem-registry.html">Open registry</a></div><div class="journey">{journey_html}</div></section>
<section class="section shell"><div class="section-head"><div><div class="eyebrow">Evidence and review</div><h2>Proof is inspectable.</h2></div></div><div class="path-grid">{section_cards('evidence',4)}{section_cards('review',4)}</div></section>
<section class="section shell"><div class="section-head"><div><div class="eyebrow">Mission and adoption</div><h2>From objective to rolloutable learning.</h2></div></div><div class="path-grid">{section_cards('mission',4)}{section_cards('adoption',4)}</div></section>
<section class="section shell"><div class="trust-band"><article class="wide-card"><div class="tag">Legal & privacy shield</div><h2>We do not want your data.</h2><p>GoalOS public pages and demos are designed for browser-local, no-wallet, no-transaction, no-intentional-analytics use. Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, trade-secret, or proprietary data through public channels.</p><div class="actions"><a class="btn small" href="privacy.html">Privacy</a><a class="btn small secondary" href="data-boundary.html">Data boundary</a><a class="btn small secondary" href="trust-boundary.html">Trust boundary</a></div></article><article class="wide-card"><div class="tag">$AGIALPHA boundary</div><h2>Public contract address only. Not available from us.</h2><p>$AGIALPHA may be referenced only as public-contract identification. GoalOS does not sell, distribute, custody, broker, recommend, support, or make available $AGIALPHA. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.</p><div class="actions"><a class="btn small" href="token-boundary.html">Token boundary</a><a class="btn small secondary" href="legal.html">Disclaimer</a></div></article></div></section>
<section class="footer shell"><b>AI creates output. GoalOS creates proof.</b><br>Public-alpha architecture. Claim-bounded. Browser-local demos. Human review required.</section>
'''
(PUBLIC/'index.html').write_text(html_doc('GoalOS AGIALPHA Ascension — Sovereign Machine Economy', index_body, 'index.html'), encoding='utf-8')

# Website operating system page
sections = []
for cat in SECTION_ORDER:
    items = [r for r in routes if r['category']==cat and r['status']=='live']
    if not items: continue
    cards = ''.join(f'''<article class="route-list-card"><h4>{html.escape(r['title'])}</h4><p>{html.escape(r['description'])}</p><small>{html.escape(r['audience'])} · {html.escape(r['role'])}</small><br><a class="btn small secondary" href="{html.escape(r['path'])}">Open</a></article>''' for r in items)
    sections.append(f'<section class="section shell"><div class="eyebrow">{html.escape(cat)}</div><h2>{html.escape(cat.title())}</h2><div class="registry-grid">{cards}</div></section>')
map_body = f'''<section class="section shell" style="padding-top:90px"><div class="eyebrow">Website Experience OS V2</div><h1 style="font-size:clamp(52px,7vw,104px);line-height:.88;letter-spacing:-.08em;margin:20px 0">One website. One proof journey. Every page findable.</h1><p class="copy">This map turns the growing GoalOS public-alpha website into a usable institution: start, evidence, review, missions, demos, adoption, trust, and docs.</p><div class="actions"><a class="btn" href="pathfinder.html">Choose a path</a><a class="btn secondary" href="demo-ecosystem-registry.html">Open registry</a><button class="btn secondary" data-open-palette>Search</button></div><div class="boundary">No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.</div></section>{''.join(sections)}'''
(PUBLIC/'website-operating-system.html').write_text(html_doc('GoalOS Website Operating System', map_body, 'website-operating-system.html'), encoding='utf-8')

# Pathfinder page
path_body = '''<section class="section shell" style="padding-top:90px"><div class="eyebrow">Pathfinder</div><h1 style="font-size:clamp(52px,7vw,100px);line-height:.9;letter-spacing:-.08em;margin:18px 0">Choose your role. Get the route.</h1><p class="copy">GoalOS is now large enough to deserve role-based navigation. Pick the route closest to your intent and open each station in order.</p><select id="roleSelect" class="searchbox" aria-label="Choose your role"><option value="new">I am new to GoalOS</option><option value="reviewer">I want to review proof</option><option value="mission">I want to propose a mission</option><option value="developer">I am a developer</option><option value="institution">I represent an institution</option></select><div id="roleRoute" class="journey" style="margin-top:20px"></div></section>'''
(PUBLIC/'pathfinder.html').write_text(html_doc('GoalOS Pathfinder', path_body, 'pathfinder.html'), encoding='utf-8')

# Registry page
cats = ['all'] + [c for c in SECTION_ORDER if any(r['category']==c for r in routes)]
filters = ''.join(f'<button class="filter {"active" if c=="all" else ""}" data-filter="{html.escape(c)}">{html.escape(c.title())}</button>' for c in cats)
registry_body = f'''<section class="section shell" style="padding-top:90px"><div class="eyebrow">Canonical demo ecosystem registry</div><h1 style="font-size:clamp(52px,7vw,100px);line-height:.9;letter-spacing:-.08em;margin:18px 0">Every demo has a route.</h1><p class="copy">Search the live website by workflow category, input, output, gates, and next allowed state. This registry is generated from the public page inventory and curated GoalOS route metadata.</p><input id="routeSearch" class="searchbox" placeholder="Search validator, docket, mission, action, token, proof, benchmark…"><div class="filters">{filters}</div><p><b id="routeCount">{len(live_routes)}</b> live routes indexed.</p><div id="routeRegistry" class="registry-grid"></div></section>'''
(PUBLIC/'demo-ecosystem-registry.html').write_text(html_doc('GoalOS Demo Ecosystem Registry', registry_body, 'demo-ecosystem-registry.html'), encoding='utf-8')

# Site map page
site_map_body = f'''<section class="section shell" style="padding-top:90px"><div class="eyebrow">Complete site map</div><h1 style="font-size:clamp(52px,7vw,100px);line-height:.9;letter-spacing:-.08em;margin:18px 0">All public pages.</h1><p class="copy">No demos removed. Every live top-level public page remains available.</p><div class="registry-grid">{''.join(f'<article class="route-list-card"><h4>{html.escape(r["title"])}</h4><p>{html.escape(r["description"])}</p><small>{html.escape(r["category"])} · {html.escape(r["status"])}</small><br>{"<a class=\"btn small secondary\" href=\""+html.escape(r["path"])+"\">Open</a>" if r["status"]=="live" else "<span class=\"btn small secondary\">Expected</span>"}</article>' for r in routes)}</div></section>'''
(PUBLIC/'site-map.html').write_text(html_doc('GoalOS Site Map', site_map_body, 'site-map.html'), encoding='utf-8')

# Trust boundary page if helpful
trust_body = '''<section class="section shell" style="padding-top:90px"><div class="eyebrow">Public-alpha trust boundary</div><h1 style="font-size:clamp(52px,7vw,100px);line-height:.9;letter-spacing:-.08em;margin:18px 0">No user data. No user funds. Human review required.</h1><p class="copy">GoalOS public pages and demos are designed to be public-safe, browser-local proof demonstrations. They are not data intake forms, wallet surfaces, transaction systems, production authorization systems, or legal/financial/tax/regulatory advice.</p><div class="path-grid"><article class="card"><div class="tag">Data</div><h3>Do not submit sensitive data.</h3><p>No personal, customer, confidential, regulated, credential, private-key, seed-phrase, trade-secret, proprietary, or payment data.</p></article><article class="card"><div class="tag">Funds</div><h3>Do not send funds.</h3><p>No wallet support, transaction support, custody, sales, liquidity, bridge, exchange, or market services.</p></article><article class="card"><div class="tag">Claims</div><h3>Claim-bounded public alpha.</h3><p>Not achieved AGI, not achieved ASI, not empirical SOTA, not production certification, and not autonomous authority.</p></article><article class="card"><div class="tag">Review</div><h3>Human review required.</h3><p>External reviewers may accept, reject, revise, or dissent. Proof gates decide what can be promoted.</p></article></div></section>'''
(PUBLIC/'trust-boundary.html').write_text(html_doc('GoalOS Trust Boundary', trust_body, 'trust-boundary.html'), encoding='utf-8')

# Create or update docs
DOCS.mkdir(exist_ok=True, parents=True)
(DOCS/'WEBSITE_EXPERIENCE_OS_V2.md').write_text(f'''# GoalOS Website Experience OS V2\n\nGenerated: {NOW}\n\n## Purpose\n\nWebsite Experience OS V2 makes the GoalOS public-alpha site navigable as one institution rather than a long list of demos. It keeps existing pages, refreshes the homepage, builds a route registry, adds a role-based Pathfinder, and preserves the public-alpha boundary.\n\n## Canonical route\n\nStart Here → Proof Experience Atlas → Demo Ecosystem Registry → Public Proof Ledger → Proof Mission Forge → Proof Mission Control → Proof Run 001 Docket → External Reviewer Replay Room.\n\n## Boundary\n\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n\n## Generated pages\n\n- `public/index.html`\n- `public/website-operating-system.html`\n- `public/pathfinder.html`\n- `public/demo-ecosystem-registry.html`\n- `public/site-map.html`\n- `public/trust-boundary.html`\n\n## Route count\n\n- Total routes: {len(routes)}\n- Live routes: {len(live_routes)}\n- Core journey stations: {len(journey)}\n''', encoding='utf-8')
(ROOT/'docs'/'reviewer').mkdir(parents=True, exist_ok=True)
(ROOT/'docs'/'reviewer'/'HOW_TO_REVIEW_WEBSITE_EXPERIENCE_OS_V2.md').write_text('''# How to review Website Experience OS V2\n\n1. Open `public/index.html`.\n2. Confirm the top navigation exposes Start, Atlas, Proof Ledger, Proof Run 001, Registry, Reviewer Room, and Search.\n3. Press `/` and verify the command palette opens.\n4. Search for `validator`, `docket`, `mission`, `action`, `token`, and `privacy`.\n5. Open `website-operating-system.html`, `pathfinder.html`, `demo-ecosystem-registry.html`, and `site-map.html`.\n6. Confirm no user data, no user funds, no wallet, no transaction, no network call, no production authority, and human review required are visible.\n7. Confirm existing public demo pages are still reachable through the registry or site map.\n\nA reviewer may accept, reject, revise, or dissent. Missing routes should be treated as remediation items, not hidden.\n''', encoding='utf-8')

# Issue body
(ISSUES/'website-experience-os-v2.md').write_text(f'''## Website Experience OS V2 installed\n\nGenerated: {NOW}\n\nThis update consolidates the growing GoalOS website into a navigable public proof institution.\n\nReview pages:\n\n- `/index.html`\n- `/website-operating-system.html`\n- `/pathfinder.html`\n- `/demo-ecosystem-registry.html`\n- `/site-map.html`\n- `/trust-boundary.html`\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n''', encoding='utf-8')

# Update README with a concise section.
readme = ROOT / 'README.md'
block = '''\n\n<!-- GOALOS_WEBSITE_EXPERIENCE_OS_V2_START -->\n## Website Experience OS V2\n\nThe public website is now organized as a complete proof journey, not a loose list of demos.\n\nPrimary paths:\n\n| Path | Purpose |\n|---|---|\n| [Start](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/index.html) | Main public front door. |\n| [Website Operating System](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/website-operating-system.html) | Complete navigation map. |\n| [Pathfinder](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/pathfinder.html) | Role-based route for new users, reviewers, mission authors, developers, and institutions. |\n| [Demo Ecosystem Registry](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/demo-ecosystem-registry.html) | Canonical route registry for demos, inputs, outputs, gates, and next states. |\n| [Public Proof Ledger](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-ledger.html) | Registry of dockets, reports, and proof surfaces. |\n| [Proof Run 001 Docket](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-docket.html) | First repository-readiness Evidence Docket. |\n| [External Reviewer Replay Room](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/external-reviewer-replay-room.html) | Independent review and replay path. |\n\nPublic-alpha boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n<!-- GOALOS_WEBSITE_EXPERIENCE_OS_V2_END -->\n'''
if readme.exists():
    txt = readme.read_text(encoding='utf-8')
    txt = re.sub(r'\n?<!-- GOALOS_WEBSITE_EXPERIENCE_OS_V2_START -->.*?<!-- GOALOS_WEBSITE_EXPERIENCE_OS_V2_END -->\n?', '\n', txt, flags=re.S)
    txt = txt.rstrip() + block + '\n'
else:
    txt = '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n\nAI creates output. GoalOS creates proof.\n' + block
readme.write_text(txt, encoding='utf-8')

# Search index and sitemap
search_index = [{'title':r['title'],'url':r['path'],'description':r['description'],'category':r['category'],'status':r['status']} for r in routes if r['status']=='live']
(PUBLIC/'search-index.json').write_text(json.dumps(search_index, indent=2), encoding='utf-8')
base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
urls='\n'.join(f'  <url><loc>{base}{html.escape(r["path"])}</loc></url>' for r in routes if r['status']=='live' and not r['path'].endswith('/'))
(PUBLIC/'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding='utf-8')
(PUBLIC/'.nojekyll').write_text('', encoding='utf-8')

# Social preview if missing
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffe96f"/><stop offset=".45" stop-color="#62ffd6"/><stop offset=".75" stop-color="#83d9ff"/><stop offset="1" stop-color="#b799ff"/></linearGradient></defs><rect width="1200" height="630" fill="#030812"/><path d="M0 0h1200v630H0z" fill="url(#g)" opacity=".12"/><text x="80" y="150" fill="#ffe96f" font-family="Arial" font-size="34" font-weight="800" letter-spacing="10">GOALOS AGIALPHA ASCENSION</text><text x="80" y="290" fill="#f7fbff" font-family="Arial" font-size="82" font-weight="900">AI creates output.</text><text x="80" y="390" fill="url(#g)" font-family="Arial" font-size="82" font-weight="900">GoalOS creates proof.</text><text x="80" y="505" fill="#c8d5e6" font-family="Arial" font-size="30">No user data · No user funds · Human review required</text><circle cx="980" cy="315" r="112" fill="url(#g)"/><text x="938" y="350" fill="#030812" font-family="Arial" font-size="100" font-weight="900">α</text></svg>'''
(ASSETS/'social-preview.svg').write_text(svg, encoding='utf-8')
(ROOT/'docs'/'assets').mkdir(parents=True, exist_ok=True)
(ROOT/'docs'/'assets'/'social-preview.svg').write_text(svg, encoding='utf-8')

# Reports
report = {
    'status': 'installed', 'generatedAt': NOW, 'routes': len(routes), 'liveRoutes': len(live_routes), 'coreJourneyStations': len(journey),
    'changedFiles': ['public/index.html','public/website-operating-system.html','public/pathfinder.html','public/demo-ecosystem-registry.html','public/site-map.html','public/trust-boundary.html','public/assets/goalos-website-os-v2.css','public/assets/goalos-website-os-v2.js','public/assets/goalos-site-index-data-v2.js','public/search-index.json','public/sitemap.xml','README.md'],
    'boundary': site_meta['boundary'],
    'noRemovalPolicy': 'No public pages are deleted by this installer. Existing top-level public pages are indexed and preserved.'
}
(REPORTS/'website-experience-os-v2-install-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
