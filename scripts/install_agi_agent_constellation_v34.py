
from __future__ import annotations
import json, pathlib, re, hashlib
ROOT = pathlib.Path.cwd()
PUBLIC = ROOT / 'public'
ASSETS = PUBLIC / 'assets'
REPORTS = ROOT / 'reports'
CONTENT = ROOT / 'content' / 'goalos'
BOUNDARY = "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes."
PAGES = [
  ('agi-agent-constellation.html','GoalOS AGI Agent Constellation','Meta-agentic AGI agents, AGI Nodes, validation, proof routes.'),
  ('agi-agent-use-cases.html','GoalOS AGI Agent Use Cases','Solved end-to-end agent playbooks.'),
  ('meta-agentic-alpha-agi.html','META-AGENTIC α‑AGI','Lineage page for the meta-agentic agent layer.'),
]
NAV_BLOCK = '<a href="agi-agent-constellation.html">AGI Agents</a>'

def ensure_dirs():
    for d in [PUBLIC, ASSETS, REPORTS, CONTENT, ROOT/'evidence/demo']:
        d.mkdir(parents=True, exist_ok=True)
    (PUBLIC/'.nojekyll').write_text('')

def scan_pages():
    return sorted([p for p in PUBLIC.glob('*.html') if p.name != '404.html'])

def title_for(path):
    txt = path.read_text(errors='ignore')
    m = re.search(r'<title[^>]*>(.*?)</title>', txt, re.I|re.S)
    if m: return re.sub(r'\s+',' ',m.group(1)).strip()
    h = re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I|re.S)
    if h: return re.sub(r'<[^>]+>','',h.group(1)).strip()
    return path.stem.replace('-',' ').title()

def patch_readme():
    path = ROOT/'README.md'
    old = path.read_text(errors='ignore') if path.exists() else '# GoalOS AGIALPHA Sovereign Machine Economy\n'
    block = """\n\n<!-- GOALOS_AGI_AGENT_CONSTELLATION_V34_START -->\n## GoalOS AGI Agent Constellation V34\n\nAdds the Meta-agentic α‑AGI agent layer as a browser-local public demo: users type an objective, GoalOS selects an agent constellation, generates a Mission Contract, prepares AGI Node handoff, creates reviewer artifacts, and routes to the correct proof surface.\n\nPrimary page: `public/agi-agent-constellation.html`\n\nBoundary: No user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required for high-impact outcomes.\n<!-- GOALOS_AGI_AGENT_CONSTELLATION_V34_END -->\n"""
    old = re.sub(r'\n?<!-- GOALOS_AGI_AGENT_CONSTELLATION_V34_START -->.*?<!-- GOALOS_AGI_AGENT_CONSTELLATION_V34_END -->\n?', '', old, flags=re.S)
    path.write_text(old.rstrip()+block)

def inject_links():
    for page in PUBLIC.glob('*.html'):
        txt = page.read_text(errors='ignore')
        if 'agi-agent-constellation.html' in txt: continue
        snippet = '<div style="position:fixed;left:16px;bottom:16px;z-index:9999"><a style="display:inline-block;padding:10px 14px;border-radius:999px;background:#66ffd2;color:#051014;font-weight:900;text-decoration:none" href="agi-agent-constellation.html">AGI Agents</a></div>'
        if '</body>' in txt:
            txt = txt.replace('</body>', snippet+'</body>')
            page.write_text(txt)


def ensure_fallback_routes():
    fallback_names = {
        'goalos.html': ('GoalOS Mission Studio', 'Tell GoalOS what you want and generate a proof path.'),
        'ask-goalos.html': ('Ask GoalOS', 'Ask questions and get routed to the right proof surface.'),
        'validation-control-tower.html': ('GoalOS Validation Control Tower', 'Choose Human, AGI Node, Hybrid, or Council validation.'),
        'mainnet-contract-atlas.html': ('GoalOS Mainnet Contract Atlas', 'Learn the 48 GoalOS-created Ethereum Mainnet contracts.'),
        'mainnet-proof-rail.html': ('GoalOS Mainnet Proof Rail', 'Understand the contract proof rail.'),
        'contract-academy.html': ('GoalOS Contract Academy', 'Learn contracts in plain language.'),
        'proof-run-001-docket.html': ('Proof Run 001 Docket', 'Review repository-readiness evidence.'),
        'demo-ecosystem-registry.html': ('Demo Ecosystem Registry', 'Find all public demos and proof rooms.'),
        'trust-boundary.html': ('Trust Boundary', 'No user data, no user funds, no wallet, no transaction.'),
        'token-boundary.html': ('Token Boundary', '$AGIALPHA public contract identification only.'),
        'privacy.html': ('Privacy', 'Public-alpha privacy and data boundary.'),
        'data-boundary.html': ('Data Boundary', 'Do not submit personal, confidential, credential, wallet, or regulated data.'),
        'no-data-no-funds.html': ('No Data / No Funds', 'GoalOS does not want user data or user funds.'),
        'site-health.html': ('Site Health', 'Route inventory and QA surface.'),
        'search.html': ('GoalOS Search', 'Browser-local site navigation.'),
        'pathfinder.html': ('GoalOS Pathfinder', 'Choose your shortest path.'),
        'mission-studio.html': ('GoalOS Mission Studio', 'One-box objective interface.'),
        'capability-compounding-lab.html': ('Capability Compounding Lab', 'Verified work becomes reusable capability.'),
        'proof-backed-upgrade-rights-room.html': ('Proof-backed Upgrade Rights Room', 'Artifacts earn authority after proof gates pass.'),
        'from-loop-to-rsi-state-capacity.html': ('Loop to RSI State Capacity', 'Long-running loops become governed RSI state.'),
        'validation-use-cases.html': ('Validation Use Cases', 'Solved validation playbooks.'),
    }
    for name, pair in fallback_names.items():
        title, desc = pair
        path = PUBLIC / name
        if path.exists():
            continue
        html = (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><link rel="stylesheet" href="assets/goalos-agi-agent-constellation-v34.css">'
            '</head><body><div class="wrap"><nav class="nav">'
            '<a class="brand" href="index.html"><span class="logo">α</span><span>GOALOS</span></a>'
            '<div class="navlinks"><a class="active" href="agi-agent-constellation.html">AGI Agents</a>'
            '<a href="site-map.html">All Pages</a><a href="search.html">Search /</a></div></nav><main>'
            '<div class="eyebrow">Fallback route preserved</div>'
            f'<h1 class="title">{title}</h1><p class="subtitle">{desc}</p>'
            '<p class="body">This fallback page preserves navigation if a richer historical page is not present yet. Existing richer pages are never overwritten by this fallback.</p>'
            '<a class="btn primary" href="agi-agent-constellation.html">Open AGI Agent Constellation</a> '
            '<a class="btn secondary" href="site-map.html">Open all pages</a>'
            f'<div class="boundary">{BOUNDARY}</div></main></div></body></html>'
        )
        path.write_text(html)

def update_indices():
    pages = scan_pages()
    entries = []
    for p in pages:
        entries.append({'title':title_for(p),'url':p.name,'category':'AGI Agents' if p.name in [x[0] for x in PAGES] else 'Preserved','description':'Open '+title_for(p)})
    (PUBLIC/'search-index.json').write_text(json.dumps(entries, indent=2))
    base = 'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        sitemap.append(f'<url><loc>{base}{p.name}</loc></url>')
    sitemap.append('</urlset>')
    (PUBLIC/'sitemap.xml').write_text('\n'.join(sitemap))
    (CONTENT/'public-proof-navigation-v34.json').write_text(json.dumps({'version':'v34','pages':entries},indent=2))
    reg = CONTENT/'demo-ecosystem-registry.json'
    old = []
    if reg.exists():
        try:
            data=json.loads(reg.read_text())
            old=data.get('demos',data if isinstance(data,list) else [])
        except Exception: old=[]
    demos = old + [{'name':'GoalOS AGI Agent Constellation V34','url':'agi-agent-constellation.html','category':'AGI Agents','inputs':['plain-language objective'],'outputs':['Mission Contract','AGI Node Handoff','Reviewer Brief','Action Graph'],'gates':['boundary','agent role contract','validation authority','Evidence Docket plan'],'next_state':'AGENT_CONSTELLATION_READY'}]
    (CONTENT/'demo-ecosystem-registry.json').write_text(json.dumps({'version':'v34','demos':demos},indent=2))

def create_site_map_if_needed():
    sm=PUBLIC/'site-map.html'
    if not sm.exists():
        links=''.join(f'<li><a href="{p.name}">{title_for(p)}</a></li>' for p in scan_pages())
        sm.write_text('<!doctype html><title>GoalOS Site Map</title><h1>All Pages</h1><ul>'+links+'</ul>')

def report():
    pages=scan_pages()
    required=['agi-agent-constellation.html','agi-agent-use-cases.html','meta-agentic-alpha-agi.html']
    missing=[x for x in required if not (PUBLIC/x).exists()]
    data={'version':'v34','status':'passed' if not missing else 'failed','missing':missing,'publicPages':len(pages),'boundary':BOUNDARY}
    for name in ['install-report','qa','route-health']:
        (REPORTS/f'agi-agent-constellation-v34-{name}.json').write_text(json.dumps(data,indent=2))
    return data

if __name__ == '__main__':
    ensure_dirs(); ensure_fallback_routes(); patch_readme(); inject_links(); update_indices(); create_site_map_if_needed(); data=report(); print(json.dumps(data,indent=2))
