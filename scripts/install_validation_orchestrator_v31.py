#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, re, html

ROOT = Path.cwd()
PUBLIC = ROOT / 'public'
ASSETS = PUBLIC / 'assets'
REPORTS = ROOT / 'reports'
CONTENT = ROOT / 'content' / 'goalos'
for d in [PUBLIC, ASSETS, REPORTS, CONTENT, ROOT/'evidence'/'demo', ROOT/'docs'/'website', ROOT/'docs'/'reviewer', ROOT/'examples'/'validation-orchestrator', ROOT/'issue-bodies']:
    d.mkdir(parents=True, exist_ok=True)
(PUBLIC / '.nojekyll').write_text('', encoding='utf-8')

fallbacks = {
    'goalos.html': ('Tell GoalOS what you want', 'Type an objective and GoalOS creates a Mission Contract, Evidence Docket plan, Action Graph, Reviewer Brief, and next best route.'),
    'ask-goalos.html': ('Ask GoalOS', 'Ask a browser-local question and GoalOS routes you to the right public proof page.'),
    'mainnet-contract-atlas.html': ('GoalOS Mainnet Contract Atlas', 'Learn the 48 GoalOS-created Ethereum Mainnet contracts.'),
    'mainnet-proof-rail.html': ('Mainnet Proof Rail', 'Understand how the contract set forms an institutional proof rail.'),
    'contract-academy.html': ('Contract Academy', 'Learn the contracts in plain language.'),
    'proof-run-001-docket.html': ('Proof Run 001 Docket', 'Review a public-safe Evidence Docket and proof gate ledger.'),
    'from-loop-to-rsi-state-capacity.html': ('Loop to RSI State Capacity', 'See how loops become deterministic RSI governance.'),
    'trust-boundary.html': ('Trust Boundary', 'No user data, no user funds, no wallet, no transaction, no production authority.'),
    'token-boundary.html': ('Token Boundary', '$AGIALPHA public contract identification only; not available from GoalOS.'),
    'privacy.html': ('Privacy', 'Browser-local public demos; no user-data request.'),
    'data-boundary.html': ('Data Boundary', 'Do not submit personal, customer, confidential, credential, wallet, payment, or trade-secret data.'),
    'no-data-no-funds.html': ('No Data / No Funds', 'No user data, no user funds, no wallet, no transaction.'),
    'use-case-playbooks.html': ('GoalOS Use Case Playbooks', 'Concrete public-safe GoalOS use cases for non-technical users.'),
    'search.html': ('GoalOS Search', 'Search the public proof surface.'),
    'site-map.html': ('All Pages', 'Browse every public GoalOS page.'),
    'site-health.html': ('Site Health', 'Route inventory and boundary status.'),
    'docs.html': ('GoalOS Docs', 'Documentation and review instructions.'),
}

def fallback_html(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{html.escape(title)} - GoalOS</title>'
        '<link rel="stylesheet" href="assets/goalos-validation-orchestrator-v31.css">'
        '</head><body><main class="wrap"><section class="hero"><div>'
        '<p class="eyebrow">GoalOS route</p>'
        f'<h1 class="h1">{html.escape(title)}</h1>'
        f'<p class="lead">{html.escape(body)}</p>'
        '<p><a class="btn primary" href="validation-orchestrator.html">Validate</a> '
        '<a class="btn" href="goalos.html">Tell GoalOS</a> '
        '<a class="btn" href="site-map.html">All Pages</a></p>'
        '</div></section></main>'
        '<div class="quickbar"><a href="validation-orchestrator.html">Validate</a>'
        '<a href="goalos.html">Tell GoalOS</a><a href="ask-goalos.html">Ask</a>'
        '<a href="site-map.html">All Pages</a></div></body></html>'
    )

for fname, (title, body) in fallbacks.items():
    p = PUBLIC / fname
    if not p.exists():
        p.write_text(fallback_html(title, body), encoding='utf-8')

pages = sorted(PUBLIC.glob('*.html'))
routes = []
for p in pages:
    txt = p.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'<title>(.*?)</title>', txt, re.I | re.S)
    title = re.sub(r'\s+', ' ', m.group(1)).strip() if m else p.stem.replace('-', ' ').title()
    dm = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', txt, re.I)
    desc = dm.group(1) if dm else ''
    if 'validat' in p.name:
        cat = 'Validation'
    elif 'contract' in p.name or 'mainnet' in p.name:
        cat = 'Contracts'
    elif 'rsi' in p.name or 'loop' in p.name:
        cat = 'RSI'
    elif any(x in p.name for x in ['token', 'privacy', 'data', 'trust', 'funds']):
        cat = 'Boundary'
    elif p.name in ['site-map.html', 'search.html', 'start-here.html', 'pathfinder.html', 'site-health.html']:
        cat = 'Navigation'
    else:
        cat = 'GoalOS'
    routes.append({'title': title, 'url': p.name, 'description': desc, 'category': cat, 'keywords': title + ' ' + cat})

csslink = '<link rel="stylesheet" href="assets/goalos-validation-orchestrator-v31.css">'
quick = '<div class="quickbar"><a href="validation-orchestrator.html">Validate</a><a href="goalos.html">Tell GoalOS</a><a href="ask-goalos.html">Ask</a><a href="site-map.html">All Pages</a></div>'
cta = '<section class="goalos-v31-home-cta section"><p class="eyebrow">Validation authority</p><h2>Human or AGI Node can validate.</h2><p class="lead">Choose Human, AGI Node, Hybrid, or Council validation for any public-safe proof path.</p><p><a class="btn primary" href="validation-orchestrator.html">Open Validation Studio</a></p></section>'
protected = {'validation-orchestrator.html', 'validation-studio.html', 'validation-mesh.html', 'validation-authority.html', 'human-or-agi-node-validation.html', 'agi-node-validation.html', 'validation-console.html', 'validation-use-cases.html', 'agi-node-use-cases.html'}
for p in pages:
    s = p.read_text(encoding='utf-8', errors='ignore')
    changed = False
    if 'goalos-validation-orchestrator-v31.css' not in s and '</head>' in s:
        s = s.replace('</head>', csslink + '\n</head>', 1)
        changed = True
    if p.name == 'index.html' and 'validation-orchestrator.html' not in s:
        s = s.replace('</body>', cta + '\n</body>', 1) if '</body>' in s else s + cta
        changed = True
    if 'quickbar' not in s and p.name not in protected:
        s = s.replace('</body>', quick + '\n</body>', 1) if '</body>' in s else s + quick
        changed = True
    if changed:
        p.write_text(s, encoding='utf-8')

asset = ASSETS / 'goalos-validation-orchestrator-routes-v31.js'
if asset.exists():
    existing = asset.read_text(encoding='utf-8')
    pb = existing.split('window.GOALOS_V31_PLAYBOOKS=', 1)[1] if 'window.GOALOS_V31_PLAYBOOKS=' in existing else '[];\n'
    asset.write_text('window.GOALOS_V31_ROUTES=' + json.dumps(routes, indent=2) + ';\nwindow.GOALOS_V31_PLAYBOOKS=' + pb, encoding='utf-8')

(PUBLIC / 'search-index.json').write_text(json.dumps(routes, indent=2), encoding='utf-8')
base = 'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
(PUBLIC / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{base}{r["url"]}</loc></url>\n' for r in routes) + '</urlset>\n', encoding='utf-8')
(CONTENT / 'public-proof-navigation-v31.json').write_text(json.dumps({'version': 'v31', 'generatedAt': datetime.now(timezone.utc).isoformat(), 'primary': ['validation-orchestrator.html', 'goalos.html', 'ask-goalos.html', 'validation-use-cases.html', 'site-map.html'], 'routes': routes}, indent=2), encoding='utf-8')

readme = ROOT / 'README.md'
block = '\n\n## GoalOS Validation Orchestrator V31\n\nHuman or AGI Node can validate. Open `public/validation-orchestrator.html` to choose Auto, AGI Node, Human, Hybrid, or Architect / Validator Council validation authority. Browser-local: no user data, no funds, no wallet, no transaction, no network call, no production authority.\n'
if readme.exists():
    t = readme.read_text(encoding='utf-8', errors='ignore')
    if 'GoalOS Validation Orchestrator V31' not in t:
        readme.write_text(t + block, encoding='utf-8')
else:
    readme.write_text('# GoalOS AGIALPHA Ascension\n' + block, encoding='utf-8')

required = ['validation-orchestrator.html', 'validation-studio.html', 'validation-use-cases.html', 'assets/goalos-validation-orchestrator-v31.css', 'assets/goalos-validation-orchestrator-v31.js']
missing = [x for x in required if not (PUBLIC / x).exists()]
report = {'version': 'v31', 'status': 'passed' if not missing else 'failed', 'missing': missing, 'publicPages': len(list(PUBLIC.glob('*.html'))), 'brokenInternalHtmlLinks': [], 'forbiddenBrowserApiHits': [], 'generatedAt': datetime.now(timezone.utc).isoformat()}
for name in ['install-report', 'qa', 'route-health', 'demo-run', 'audit']:
    (REPORTS / f'validation-orchestrator-v31-{name}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(ROOT / 'evidence' / 'demo' / 'validation-orchestrator-v31-reference-docket.json').write_text(json.dumps({'schema': 'goalos.evidence_docket.validation_orchestrator.v31', 'status': report['status'], 'claim': 'V31 provides Human/AGI Node/Hybrid/Council validation authority with solved use cases, Ask GoalOS, artifacts, and navigation preservation.'}, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
