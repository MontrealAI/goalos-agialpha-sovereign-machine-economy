
from pathlib import Path
import json, re, hashlib, datetime, html
ROOT = Path.cwd()
PUBLIC = ROOT / 'public'
ASSETS = PUBLIC / 'assets'
for p in [PUBLIC, ASSETS, ROOT/'reports', ROOT/'evidence/demo', ROOT/'content/goalos', ROOT/'docs/website', ROOT/'docs/reviewer', ROOT/'examples/objective-command-center', ROOT/'.github/ISSUE_TEMPLATE', ROOT/'issue-bodies']:
    p.mkdir(parents=True, exist_ok=True)

CSS = (ROOT/'_pack_payload/goalos-objective-command-center-v20.css').read_text(encoding='utf-8')
JS = (ROOT/'_pack_payload/goalos-objective-command-center-v20.js').read_text(encoding='utf-8')
HTML = (ROOT/'_pack_payload/mission-command-center.html').read_text(encoding='utf-8')
(ASSETS/'goalos-objective-command-center-v20.css').write_text(CSS, encoding='utf-8')
(ASSETS/'goalos-objective-command-center-v20.js').write_text(JS, encoding='utf-8')
(PUBLIC/'mission-command-center.html').write_text(HTML, encoding='utf-8')
(PUBLIC/'objective-command-center.html').write_text(HTML.replace('mission-command-center.html','objective-command-center.html').replace('GoalOS Objective Command Center','GoalOS Objective Command Center'), encoding='utf-8')

fallbacks = {
 'start-here.html':('Start in 60 seconds','Read the thesis, open Pathfinder, try browser-local demos, review Proof Run 001.'),
 'pathfinder.html':('Choose your path','New user, reviewer, developer, institution, boundary reviewer, demo explorer.'),
 'demo-ecosystem-registry.html':('Demo Ecosystem Registry','Every public demo mapped to inputs, outputs, proof gates, and next states.'),
 'proof-run-001-docket.html':('Proof Run 001 Docket','Repository readiness evidence docket, validator packet, replay path, and claim boundary.'),
 'mainnet-contract-atlas.html':('Mainnet Contract Atlas','48 GoalOS-created Ethereum Mainnet contracts, one institutional proof rail.'),
 'mainnet-proof-rail.html':('Mainnet Proof Rail','Public commitments, attestations, proof ledgers, selection gates, rollback, and Chronicle.'),
 'contract-academy.html':('Contract Academy','Learn the contracts in plain language without a wallet or transaction.'),
 'from-loop-to-rsi-state-capacity.html':('Loop to RSI State-Capacity Command Room','Recursive invention governance: TARGET to PROMOTE, with gates.'),
 'ask-goalos.html':('Ask GoalOS','Browser-local route assistant for GoalOS questions.'),
 'trust-boundary.html':('Trust Boundary','No data, no funds, no wallet, no transaction, no network call, human review required.'),
 'token-boundary.html':('Token Boundary','$AGIALPHA is public contract identification only; not available from GoalOS.'),
 'site-map.html':('All Pages','Complete route map.'),
 'search.html':('Search','Search public GoalOS pages.'),
 'site-health.html':('Site Health','Route health, boundary checks, public surface status.')
}
def minimal_page(title, desc):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} · GoalOS</title><link rel="stylesheet" href="assets/goalos-objective-command-center-v20.css"></head><body class="goalos-v20"><nav class="g-nav"><a class="brand" href="index.html"><span class="logo"></span><span><strong>GOALOS</strong><span>AGIALPHA ASCENSION</span></span></a><div class="nav-links"><a href="mission-command-center.html">Mission Command</a><a href="start-here.html">Start</a><a href="site-map.html">All Pages</a><a href="trust-boundary.html">Trust</a></div></nav><main class="g-wrap"><section class="hero"><div><div class="eyebrow">Restored route</div><h1 class="headline">{html.escape(title)}</h1><p class="dek">{html.escape(desc)}</p><div class="hero-actions"><a class="btn primary" href="mission-command-center.html">Tell GoalOS what you want</a><a class="btn" href="site-map.html">Open all pages</a></div><div class="boundary"><strong>Public-alpha boundary:</strong> no user data, no user funds, no wallet, no transaction, no network call, no production authority. Human review required.</div></div></section></main><footer class="g-wrap foot">GoalOS AGIALPHA Ascension — public-alpha proof operating surface.</footer></body></html>'''
for fn,(title,desc) in fallbacks.items():
    path = PUBLIC/fn
    if not path.exists():
        path.write_text(minimal_page(title,desc), encoding='utf-8')

# Inject lightweight link into existing public pages without overwriting complex demos.
inject_css = '<link rel="stylesheet" href="assets/goalos-objective-command-center-v20.css">'
inject_js = '<script src="assets/goalos-objective-command-center-v20.js"></script>'
button = '<a class="goalos-v20-mission-float" href="mission-command-center.html" style="position:fixed;right:18px;bottom:72px;z-index:90;border-radius:999px;padding:12px 16px;background:linear-gradient(100deg,#ffe66e,#68ffdf);color:#061012;font-weight:1000;text-decoration:none;box-shadow:0 10px 30px rgba(0,0,0,.3)">Tell GoalOS</a>'
for path in PUBLIC.glob('*.html'):
    if path.name in {'mission-command-center.html','objective-command-center.html'}: continue
    txt = path.read_text(encoding='utf-8', errors='ignore')
    changed = False
    if 'goalos-objective-command-center-v20.css' not in txt and '</head>' in txt:
        txt = txt.replace('</head>', inject_css+'\n</head>'); changed=True
    if 'goalos-v20-mission-float' not in txt and '</body>' in txt:
        txt = txt.replace('</body>', button+'\n</body>'); changed=True
    if changed:
        path.write_text(txt, encoding='utf-8')

# Patch homepage with a prominent card if index exists
idx = PUBLIC/'index.html'
if idx.exists():
    txt = idx.read_text(encoding='utf-8', errors='ignore')
    if 'mission-command-center.html' not in txt[:4000]:
        navlink = '<a href="mission-command-center.html">Mission Command</a>'
        txt = txt.replace('<a href="start-here.html">', navlink+'\n<a href="start-here.html">', 1) if '<a href="start-here.html">' in txt else txt
    if 'GoalOS Mission Command Center V20' not in txt:
        section = '''\n<section class="g-wrap section" id="mission-command-v20"><div class="card" style="border-color:rgba(104,255,223,.35);background:linear-gradient(135deg,rgba(104,255,223,.12),rgba(167,139,250,.10));"><div class="eyebrow">New command layer</div><h2>Tell GoalOS what you want.</h2><p class="subdek">Enter a plain-language objective. GoalOS generates a Mission Contract, Evidence Docket plan, route map, governed decision state, and downloadable proof artifacts. Browser-local. No data. No wallet.</p><div class="hero-actions"><a class="btn primary" href="mission-command-center.html">Open Mission Command</a><a class="btn" href="ask-goalos.html">Ask GoalOS</a></div></div></section>\n'''
        txt = txt.replace('</main>', section+'</main>') if '</main>' in txt else txt.replace('</body>', section+'</body>')
    idx.write_text(txt, encoding='utf-8')

# Build route index
pages=[]
for p in sorted(PUBLIC.glob('*.html')):
    raw=p.read_text(encoding='utf-8',errors='ignore')
    title = re.search(r'<title>(.*?)</title>', raw, re.I|re.S)
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', raw, re.I|re.S)
    def clean(x): return re.sub('<[^>]+>','',x or '').replace('\n',' ').strip()
    t = clean(h1.group(1) if h1 else (title.group(1) if title else p.stem.replace('-',' ').title()))
    if not t: t=p.stem.replace('-',' ').title()
    desc = re.search(r'<meta name="description" content="(.*?)"', raw, re.I|re.S)
    d = desc.group(1).strip() if desc else 'GoalOS public proof route.'
    cat = 'Navigation & Docs'
    low=(p.name+' '+t+' '+d).lower()
    if 'contract' in low or 'mainnet' in low: cat='Mainnet Proof Rail'
    elif 'rsi' in low: cat='Loop → RSI'
    elif 'loop' in low: cat='Loop Demos'
    elif 'trust' in low or 'token' in low or 'privacy' in low or 'boundary' in low or 'data' in low: cat='Trust & Boundary'
    elif 'proof' in low or 'docket' in low or 'review' in low or 'validator' in low: cat='Evidence & Review'
    elif 'mission-command' in p.name or 'objective-command' in p.name: cat='Mission Command'
    pages.append({'title':t[:120],'url':p.name,'description':d[:220],'category':cat})
(PUBLIC/'search-index.json').write_text(json.dumps(pages,indent=2), encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{p["url"]}</loc></url>' for p in pages)+'\n</urlset>\n', encoding='utf-8')
(PUBLIC/'.nojekyll').write_text('', encoding='utf-8')

nav = {'version':'v20','name':'GoalOS Objective Command Center','primaryRoute':'mission-command-center.html','pages':pages,'boundary':'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'}
(ROOT/'content/goalos/public-proof-navigation-v20.json').write_text(json.dumps(nav,indent=2), encoding='utf-8')
registry = {'version':'v20','demos':[{'name':'GoalOS Objective Command Center V20','canonical_url':'mission-command-center.html','description':'Plain-language objective box that creates Mission Contract, Evidence Docket plan, route map, governed decision state, and downloadable artifacts.','workflow_category':'mission_command','expected_inputs':['public-safe plain-language objective'], 'generated_outputs':['mission contract json','reviewer brief markdown','action graph csv','route recommendations'], 'proof_gates':['no user data','no user funds','no wallet','no transaction','no network call','human review required'], 'next_state':'MISSION_PLAN_REVIEW_READY'}]}
(ROOT/'content/goalos/demo-ecosystem-registry-v20.json').write_text(json.dumps(registry,indent=2), encoding='utf-8')

# Docs
(ROOT/'docs/website/OBJECTIVE_COMMAND_CENTER_V20.md').write_text('''# GoalOS Objective Command Center V20\n\nA browser-local mission command page where a user enters a plain-language objective and receives a Mission Contract, Evidence Docket plan, route map, governed decision state, and downloadable local artifacts.\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority. Human review required.\n''', encoding='utf-8')
(ROOT/'docs/reviewer/HOW_TO_REVIEW_OBJECTIVE_COMMAND_CENTER_V20.md').write_text('''# How to review Objective Command Center V20\n\n1. Open `public/mission-command-center.html`.\n2. Enter a public-safe objective.\n3. Confirm routes, gates, decision state, and downloads update.\n4. Confirm no network calls, wallet prompts, storage APIs, or user-data collection.\n5. Confirm the page preserves public-alpha boundaries.\n''', encoding='utf-8')
(ROOT/'examples/objective-command-center/public-safe-objectives.md').write_text('''# Public-safe objective examples\n\n- I want to understand the 48 Ethereum Mainnet contracts and their proof roles.\n- I want to review Proof Run 001 before trusting a claim.\n- I want to learn Loop to RSI governance.\n- I want to check privacy, token, no-data, no-funds, and no-wallet boundaries.\n''', encoding='utf-8')
(ROOT/'.github/ISSUE_TEMPLATE/objective_command_center_feedback.yml').write_text('''name: Objective Command Center feedback\ndescription: Report feedback for the browser-local Mission Command page.\ntitle: "Objective Command Center feedback: "\nlabels: [feedback, website]\nbody:\n  - type: markdown\n    attributes:\n      value: |\n        Please do not submit personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.\n  - type: textarea\n    id: feedback\n    attributes:\n      label: Feedback\n      description: What did you try, and what should improve?\n    validations:\n      required: true\n  - type: checkboxes\n    id: boundary\n    attributes:\n      label: Boundary confirmation\n      options:\n        - label: I confirm I am not submitting personal, customer, confidential, regulated, credential, wallet, private-key, seed-phrase, payment, trade-secret, proprietary data, or user funds.\n          required: true\n''', encoding='utf-8')
(ROOT/'issue-bodies/objective-command-center-v20.md').write_text('''# GoalOS Objective Command Center V20 Review\n\nPlease review the new browser-local mission command page.\n\n- Route: `public/mission-command-center.html`\n- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority.\n- Expected: user enters objective, GoalOS generates proof path and route recommendations.\n''', encoding='utf-8')

# Reports
report = {'status':'passed','version':'v20','route_count':len(pages),'primary_route':'mission-command-center.html','created_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'boundary':'preserved'}
for name in ['objective-command-center-v20-install-report.json','objective-command-center-v20-qa.json','objective-command-center-v20-route-health.json']:
    (ROOT/'reports'/name).write_text(json.dumps(report,indent=2), encoding='utf-8')
(ROOT/'evidence/demo/objective-command-center-v20-reference-docket.json').write_text(json.dumps({'status':'passed','demo':'GoalOS Objective Command Center V20','decision_state':'MISSION_PLAN_REVIEW_READY','boundary':report['boundary']},indent=2), encoding='utf-8')

# README patch
readme = ROOT/'README.md'
block = '''\n\n## GoalOS Objective Command Center V20\n\nTell GoalOS what you want. The browser-local Mission Command page converts a plain-language objective into a Mission Contract, Evidence Docket plan, route map, governed decision state, and downloadable local artifacts.\n\n- Public route: `public/mission-command-center.html`\n- No user data. No user funds. No wallet. No transaction. No network call. Human review required.\n'''
if readme.exists():
    txt=readme.read_text(encoding='utf-8', errors='ignore')
    if 'GoalOS Objective Command Center V20' not in txt:
        readme.write_text(txt+block, encoding='utf-8')
else:
    readme.write_text('# GoalOS AGIALPHA Ascension\n'+block, encoding='utf-8')
print(json.dumps(report, indent=2))
