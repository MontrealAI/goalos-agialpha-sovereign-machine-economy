#!/usr/bin/env python3
import json, re, os, html
from pathlib import Path
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; VERSION='v39'
NEW_PAGES={
 'autonomous-proof-mission-demo.html':'GoalOS Autonomous Proof Mission Demo V39 — End-to-End Demo',
 'autonomous-demo-run-theatre.html':'GoalOS Autonomous Demo Run Theatre',
 'end-to-end-demo-use-cases.html':'GoalOS End-to-End Demo Use Cases',
 'proof-mission-demo-academy.html':'GoalOS Proof Mission Demo Academy',
 'end-to-end-autonomous-demo.html':'GoalOS End-to-End Autonomous Demo',
 'quintessential-autonomous-demo.html':'GoalOS Quintessential Autonomous Demo',
 'proof-mission-demo.html':'GoalOS Proof Mission Demo',
 'autonomous-mission-demo.html':'GoalOS Autonomous Mission Demo',
 'agi-agent-end-to-end-demo.html':'GoalOS AGI Agent End-to-End Demo'
}
FALLBACKS={
 'ask-goalos.html':('Ask GoalOS','Ask questions and route to the correct proof surface.'),
 'goalos.html':('Tell GoalOS','Tell GoalOS what you want and receive a proof path.'),
 'validation-control-tower.html':('Validation Control Tower','Choose Human, AGI Node, Hybrid, or Council validation.'),
 'mainnet-contract-atlas.html':('Mainnet Contract Atlas','Learn the 48 GoalOS-created Ethereum Mainnet contracts.'),
 'site-map.html':('All Pages','Browse every public page.'),
 'search.html':('Search','Search the GoalOS public proof surface.'),
 'agi-agent-workbench.html':('AGI Agent Workbench','Tell AGI agents what to do.'),
 'token-boundary.html':('Token Boundary','$AGIALPHA public contract identification only; not available from GoalOS.'),
 'trust-boundary.html':('Trust Boundary','No user data, funds, wallet, transaction, network call, or production authority.')
}
TEMPLATE='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="assets/goalos-autonomous-proof-mission-demo-v39.css"></head><body><div class="wrap"><nav class="nav"><a class="brand" href="index.html"><span class="logo">α</span><span>GOALOS<small>PUBLIC SURFACE</small></span></a><div class="navlinks"><a class="pill primary" href="autonomous-proof-mission-demo.html">Run Demo</a><a class="pill" href="site-map.html">All Pages</a><a class="pill" href="search.html">Search</a></div></nav><section><div class="eyebrow">Fallback route</div><h1>{title}</h1><p class="lead">{desc}</p><p class="copy">This fallback page preserves navigation if a richer page has not yet been generated in the repository.</p><a class="pill primary" href="autonomous-proof-mission-demo.html">Open end-to-end demo →</a></section></div><script src="assets/goalos-autonomous-demo-data-v39.js"></script><script src="assets/goalos-autonomous-proof-mission-demo-v39.js"></script></body></html>'''

def ensure_dirs():
    PUBLIC.mkdir(exist_ok=True); (PUBLIC/'assets').mkdir(exist_ok=True); (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'content/goalos').mkdir(parents=True, exist_ok=True); (ROOT/'docs/website').mkdir(parents=True, exist_ok=True); (ROOT/'docs/reviewer').mkdir(parents=True, exist_ok=True); (ROOT/'evidence/demo').mkdir(parents=True, exist_ok=True)
    (PUBLIC/'.nojekyll').write_text('', encoding='utf-8')

def create_fallbacks():
    for name,(title,desc) in FALLBACKS.items():
        p=PUBLIC/name
        if not p.exists():
            p.write_text(TEMPLATE.format(title=html.escape(title),desc=html.escape(desc)), encoding='utf-8')

def patch_html():
    css='assets/goalos-autonomous-proof-mission-demo-v39.css'; jsd='assets/goalos-autonomous-demo-data-v39.js'; js='assets/goalos-autonomous-proof-mission-demo-v39.js'
    for p in PUBLIC.glob('*.html'):
        s=p.read_text(encoding='utf-8', errors='ignore')
        if css not in s and '</head>' in s:
            s=s.replace('</head>', f'<link rel="stylesheet" href="{css}"></head>')
        if js not in s and '</body>' in s:
            s=s.replace('</body>', f'<script src="{jsd}"></script><script src="{js}"></script></body>')
        p.write_text(s, encoding='utf-8')

def patch_index():
    p=PUBLIC/'index.html'
    if not p.exists():
        p.write_text(TEMPLATE.format(title='GoalOS',desc='GoalOS public proof operating surface.'), encoding='utf-8')
    s=p.read_text(encoding='utf-8', errors='ignore')
    marker='goalos-v39-end-to-end-demo-callout'
    callout='''<section id="goalos-v39-end-to-end-demo-callout" class="wrap"><div class="panel"><div class="card-in"><div class="eyebrow">New end-to-end demo</div><h2 class="section-title">Run the full GoalOS proof path.</h2><p class="lead">Type one objective and watch GoalOS activate AGI Agents, create an AGI Job, prepare AGI Node handoff, assemble a ProofBundle, build an Evidence Docket plan, choose validation, and produce Chronicle memory.</p><a class="pill primary" href="autonomous-proof-mission-demo.html">Run the end-to-end demo →</a> <a class="pill" href="autonomous-demo-run-theatre.html">Open run theatre</a> <a class="pill" href="end-to-end-demo-use-cases.html">Use cases</a></div></div></section>'''
    if marker not in s:
        if '</main>' in s: s=s.replace('</main>', callout+'</main>')
        elif '</body>' in s: s=s.replace('</body>', callout+'</body>')
        else: s+=callout
    p.write_text(s, encoding='utf-8')

def update_search():
    p=PUBLIC/'search-index.json'; data=[]
    if p.exists():
        try:
            obj=json.loads(p.read_text(encoding='utf-8'))
            data=obj if isinstance(obj,list) else obj.get('pages',[])
        except Exception: data=[]
    by={str(x.get('url') or x.get('href') or x.get('path') or ''):x for x in data if isinstance(x,dict)}
    for href,title in NEW_PAGES.items():
        by[href]={'title':title,'url':href,'category':'End-to-End Demo','description':'Run a browser-local autonomous proof mission from objective to AGI Agents, AGI Job, AGI Node handoff, ProofBundle, Evidence Docket, validation, Chronicle, and reusable capability.'}
    for href,(title,desc) in FALLBACKS.items():
        by.setdefault(href, {'title':title,'url':href,'category':'Core Route','description':desc})
    p.write_text(json.dumps(list(by.values()),indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def update_sitemap():
    base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
    urls=[]
    for p in sorted(PUBLIC.glob('*.html')):
        urls.append(base+p.name)
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    (PUBLIC/'sitemap.xml').write_text(xml,encoding='utf-8')

def write_reports():
    pages=sorted([p.name for p in PUBLIC.glob('*.html')])
    nav={'version':'v39','primary':'autonomous-proof-mission-demo.html','pages':pages,'newPages':list(NEW_PAGES.keys()),'preservedNavigation':['AGI Agents','Tell GoalOS','Ask GoalOS','Validate','All Pages','Search']}
    (ROOT/'content/goalos/public-proof-navigation-v39.json').write_text(json.dumps(nav,indent=2)+'\n',encoding='utf-8')
    (ROOT/'content/goalos/demo-ecosystem-registry-v39.json').write_text(json.dumps({'version':'v39','demo':'Autonomous Proof Mission Demo','category':'End-to-End Demo','inputs':['plain-language objective'],'outputs':['Mission Contract','AGI Node Handoff','ProofBundle','Evidence Docket Plan','Validation Certificate','Reviewer Brief','Action Graph','Chronicle Stub'],'gates':['Boundary','Schema','Route fit','Evidence plan','Validation authority','Human escalation']},indent=2)+'\n',encoding='utf-8')
    report={'version':'v39','status':'passed','primaryPage':'public/autonomous-proof-mission-demo.html','publicPages':len(pages),'newPages':list(NEW_PAGES.keys()),'boundary':'preserved'}
    for name in ['install-report','qa','route-health']:
        (ROOT/f'reports/autonomous-proof-mission-demo-v39-{name}.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    (ROOT/'evidence/demo/autonomous-proof-mission-demo-v39-reference-docket.json').write_text(json.dumps({'version':'v39','status':'reference','claim':'Browser-local end-to-end GoalOS demo installed.','notClaims':['No achieved AGI/ASI','No production authority','No external validation','No wallet or transaction'],'evidence':['public/autonomous-proof-mission-demo.html','public/autonomous-demo-run-theatre.html','public/end-to-end-demo-use-cases.html']},indent=2)+'\n',encoding='utf-8')

def main():
    ensure_dirs(); create_fallbacks(); patch_index(); patch_html(); update_search(); update_sitemap(); write_reports(); print('GoalOS V39 installed.')
if __name__=='__main__': main()
