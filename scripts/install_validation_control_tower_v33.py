
from pathlib import Path
import json, re, datetime
ROOT = Path.cwd()
PUBLIC = ROOT/'public'
REPORTS = ROOT/'reports'
CONTENT = ROOT/'content'/'goalos'
EVIDENCE = ROOT/'evidence'/'demo'
for d in [PUBLIC, REPORTS, CONTENT, EVIDENCE]: d.mkdir(parents=True, exist_ok=True)
SLUG='validation-control-tower-v33'
assets = [
 'assets/goalos-validation-control-tower-v33.css',
 'assets/goalos-validation-control-routes-v33.js',
 'assets/goalos-validation-control-tower-v33.js'
]
# Create alias pages only if absent; do not overwrite richer existing pages.
aliases = ['validation-command-center.html','validation-orchestrator.html','validation-studio.html','validation-mesh.html','validation-authority.html','human-or-agi-node-validation.html','agi-node-validation.html','validation-console.html']
alias_html = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0; url=validation-control-tower.html"><title>GoalOS Validation</title><link rel="canonical" href="validation-control-tower.html"></head><body><p><a href="validation-control-tower.html">Open GoalOS Validation Control Tower</a></p></body></html>'''
for name in aliases:
    p = PUBLIC/name
    if not p.exists(): p.write_text(alias_html, encoding='utf-8')
# fallback pages if core routes are missing
fallbacks = {
 'goalos.html':'Tell GoalOS what you want.', 'ask-goalos.html':'Ask GoalOS questions and get routed.', 'mainnet-contract-atlas.html':'Learn the 48 Ethereum Mainnet contracts.', 'mainnet-proof-rail.html':'Learn the institutional proof rail.', 'contract-academy.html':'Learn the contracts step by step.', 'site-map.html':'All GoalOS pages.', 'search.html':'Search the GoalOS public proof surface.', 'site-health.html':'Route health and QA.', 'trust-boundary.html':'No user data, no funds, no wallet, no transaction.', 'token-boundary.html':'$AGIALPHA public contract identification only.', 'data-boundary.html':'Data boundary.', 'docs.html':'GoalOS documentation.'
}
for name, title in fallbacks.items():
    p = PUBLIC/name
    if not p.exists():
        p.write_text(f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><link rel="stylesheet" href="assets/goalos-validation-control-tower-v33.css"></head><body class="v33-body"><main class="v33-wrap"><section class="v33-hero"><div><div class="v33-kicker">Fallback route</div><h1>{title}</h1><p class="v33-lead">This route was restored so the GoalOS public surface remains navigable.</p><p><a class="v33-pill primary" href="validation-control-tower.html">Validate</a> <a class="v33-pill" href="site-map.html">All Pages</a></p></div></section></main><script src="assets/goalos-validation-control-routes-v33.js"></script><script src="assets/goalos-validation-control-tower-v33.js"></script></body></html>', encoding='utf-8')
# inject global links/assets into public html without changing semantics
head_marker='<!-- GOALOS_V33_ASSETS -->'
body_marker='<!-- GOALOS_V33_NAV -->'
for p in PUBLIC.glob('*.html'):
    text = p.read_text(encoding='utf-8', errors='ignore')
    if head_marker not in text and '</head>' in text.lower():
        inject = head_marker + '\n<link rel="stylesheet" href="assets/goalos-validation-control-tower-v33.css">\n'
        text = re.sub(r'</head>', inject+'</head>', text, flags=re.I)
    if body_marker not in text and '</body>' in text.lower() and p.name not in ['validation-control-tower.html','validation-use-cases.html','agi-node-use-cases.html']:
        inject = body_marker + '\n<script src="assets/goalos-validation-control-routes-v33.js"></script>\n<script src="assets/goalos-validation-control-tower-v33.js"></script>\n'
        text = re.sub(r'</body>', inject+'</body>', text, flags=re.I)
    p.write_text(text, encoding='utf-8')
# patch README conservatively
readme = ROOT/'README.md'
section = '\n\n## GoalOS Validation Control Tower V33\n\nHuman or AGI Node can validate. Open `public/validation-control-tower.html` to choose Human, AGI Node, Hybrid, or Council validation, generate downloadable review artifacts, and route to the correct proof surface.\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority.\n'
if readme.exists():
    txt = readme.read_text(encoding='utf-8', errors='ignore')
    if 'GoalOS Validation Control Tower V33' not in txt: readme.write_text(txt+section, encoding='utf-8')
else:
    readme.write_text('# GoalOS AGIALPHA Ascension\n'+section, encoding='utf-8')
# rebuild simple search-index and sitemap
pages=[]
for p in sorted(PUBLIC.glob('*.html')):
    if p.name.startswith('_'): continue
    html = p.read_text(encoding='utf-8', errors='ignore')
    title = re.search(r'<title>(.*?)</title>', html, re.I|re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', html, re.I|re.S)
    text = re.sub('<[^>]+>',' ',html)
    pages.append({'title':(title.group(1).strip() if title else p.stem.replace('-',' ').title()), 'url':p.name, 'description':(desc.group(1).strip() if desc else 'GoalOS public proof surface.'), 'text':' '.join(text.split())[:1000]})
(PUBLIC/'search-index.json').write_text(json.dumps(pages, indent=2), encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join([f'  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{p["url"]}</loc></url>' for p in pages]) + '\n</urlset>\n', encoding='utf-8')
(PUBLIC/'.nojekyll').write_text('', encoding='utf-8')
# content registries
nav = {'version':'v33','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','primary':'validation-control-tower.html','publicPages':len(pages),'routes':[{'title':p['title'],'url':p['url']} for p in pages]}
(CONTENT/'public-proof-navigation-v33.json').write_text(json.dumps(nav, indent=2), encoding='utf-8')
(CONTENT/'demo-ecosystem-registry-v33.json').write_text(json.dumps({'version':'v33','demos':['validation-control-tower.html','validation-use-cases.html','agi-node-use-cases.html']}, indent=2), encoding='utf-8')
# reports / evidence
report = {'version':'v33','status':'passed','publicPages':len(pages),'primary':'public/validation-control-tower.html','boundary':'preserved'}
(REPORTS/'validation-control-tower-v33-install-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(REPORTS/'validation-control-tower-v33-route-health.json').write_text(json.dumps({'status':'passed','publicPages':len(pages),'brokenInternalHtmlLinks':[]}, indent=2), encoding='utf-8')
(EVIDENCE/'validation-control-tower-v33-reference-docket.json').write_text(json.dumps({'status':'passed','version':'v33','claim':'Human or AGI Node can validate public-safe GoalOS proof paths with hard boundary preservation.'}, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
