#!/usr/bin/env python3
from pathlib import Path
import json, shutil, re, datetime
ROOT=Path.cwd(); PACK=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'; PUBLIC.mkdir(exist_ok=True)
CSS='assets/goalos-agi-agent-mission-control-v37.css'; DATA='assets/goalos-agi-agent-mission-data-v37.js'; JS='assets/goalos-agi-agent-mission-control-v37.js'
def copy(src,dst,overwrite=True):
    src=Path(src); dst=Path(dst)
    if src.is_dir():
        for p in src.rglob('*'):
            if p.is_file():
                t=dst/p.relative_to(src); t.parent.mkdir(parents=True,exist_ok=True)
                if overwrite or not t.exists(): shutil.copy2(p,t)
    elif src.exists():
        dst.parent.mkdir(parents=True,exist_ok=True)
        if overwrite or not dst.exists(): shutil.copy2(src,dst)
copy(PACK/'public/assets', PUBLIC/'assets', True)
for page in ['agi-agent-mission-control.html','agi-agent-command-center-v37.html','agi-agent-playbooks.html','agent-flow-academy.html']:
    copy(PACK/'public'/page, PUBLIC/page, True)
for d in ['docs','examples','reports','evidence','content','scripts','issue-bodies','.github']:
    copy(PACK/d, ROOT/d, True)
def fallback(filename,title,summary,target='agi-agent-mission-control.html'):
    p=PUBLIC/filename
    if p.exists(): return
    html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="{CSS}"></head><body><nav class="nav"><a class="brand" href="index.html"><span class="logo"></span><span>GoalOS</span></a><div class="navlinks"><a href="{target}">AGI Agents</a><a href="site-map.html">All Pages</a><a href="search.html">Search /</a></div></nav><main class="wrap"><section class="hero"><div><div class="eyebrow">Route preserved</div><h1 class="h1">{title}</h1><p class="lead">{summary}</p><p><a class="btn primary" href="{target}">Open AGI Agent Mission Control</a> <a class="btn" href="site-map.html">All Pages</a></p></div></section></main><script src="{DATA}"></script><script src="{JS}"></script></body></html>'
    p.write_text(html,encoding='utf-8')
for fn,title,summary in [('ask-goalos.html','Ask GoalOS','Browser-local question window and route assistant.'),('goalos.html','Tell GoalOS','One-box mission interface.'),('validation-control-tower.html','Validation Control Tower','Human, AGI Node, Hybrid, or Council validation.'),('validation-command-center.html','Validation Command Center','Visual validation interface.'),('site-map.html','All Pages','Complete public route inventory.'),('search.html','Search','Browser-local search and command palette.'),('mainnet-contract-atlas.html','Mainnet Contract Atlas','48 Ethereum Mainnet contracts proof rail.'),('mainnet-proof-rail.html','Mainnet Proof Rail','Contract journey and proof rail.'),('contract-academy.html','Contract Academy','Learn the 48 contracts.'),('trust-boundary.html','Trust Boundary','No user data, no funds, no wallet, no transaction.'),('token-boundary.html','Token Boundary','$AGIALPHA public contract identification only.'),('proof-run-001-docket.html','Proof Run 001 Docket','Repository readiness evidence docket.'),('demo-ecosystem-registry.html','Demo Registry','All demos and routes.'),('from-loop-to-rsi-state-capacity.html','Loop to RSI State Capacity','Long-running loop to deterministic invention governance.'),('start-here.html','Start Here','Quick onboarding.'),('pathfinder.html','Pathfinder','Role-based navigation.'),('site-health.html','Site Health','Route health and boundary checks.'),('privacy.html','Privacy','No-data privacy boundary.'),('data-boundary.html','Data Boundary','No private data boundary.')]: fallback(fn,title,summary)
callout='<section id="goalos-v37-agent-front-door" class="wrap section"><div class="eyebrow">New · AGI Agent Mission Control</div><h2>Tell AGI agents what you want.</h2><p class="lead">One box turns an objective into roles, AGI Node handoff, Evidence Docket plan, validation route, Reviewer Brief, Action Graph, flowcharts, and next best page.</p><p><a class="btn primary" href="agi-agent-mission-control.html">Open AGI Agent Mission Control</a> <a class="btn" href="agi-agent-playbooks.html">Solved use cases</a> <a class="btn" href="agent-flow-academy.html">Flowcharts</a></p></section>'
idx=PUBLIC/'index.html'
if idx.exists():
    t=idx.read_text(encoding='utf-8',errors='ignore')
    if 'goalos-v37-agent-front-door' not in t:
        t=re.sub(r'(<body[^>]*>)', r'\1\n'+callout, t, count=1, flags=re.I) if re.search(r'<body[^>]*>',t,re.I) else callout+t
        idx.write_text(t,encoding='utf-8')
else: shutil.copy2(PACK/'public'/'agi-agent-mission-control.html',idx)
def inject(t):
    if 'goalos-agi-agent-mission-control-v37.css' not in t:
        t=t.replace('</head>',f'<link rel="stylesheet" href="{CSS}">\n</head>') if '</head>' in t else f'<link rel="stylesheet" href="{CSS}">\n'+t
    if 'goalos-agi-agent-mission-data-v37.js' not in t:
        s=f'<script src="{DATA}"></script>\n<script src="{JS}"></script>'
        t=t.replace('</body>',s+'\n</body>') if '</body>' in t else t+'\n'+s
    if 'goalos-v37-floating-path' not in t:
        f='<div id="goalos-v37-floating-path" class="ask-launch"><a class="btn primary" href="agi-agent-mission-control.html">AGI Agents</a><button class="btn askOpen">Ask</button><a class="btn" href="site-map.html">All Pages</a></div>'
        t=t.replace('</body>',f+'\n</body>') if '</body>' in t else t+f
    return t
for h in PUBLIC.glob('*.html'):
    try: h.write_text(inject(h.read_text(encoding='utf-8',errors='ignore')),encoding='utf-8')
    except Exception: pass
entries=[{'title':'AGI Agent Mission Control V37','url':'agi-agent-mission-control.html','description':'Visual one-box AGI Agent mission control with flowcharts and AGI Node handoff.'},{'title':'AGI Agent Playbooks V37','url':'agi-agent-playbooks.html','description':'Solved end-to-end AGI Agent playbooks.'},{'title':'Agent Flow Academy V37','url':'agent-flow-academy.html','description':'Visual maps for AGI Agents, AGI Nodes, Mission OS, and AEP.'}]
sidx=PUBLIC/'search-index.json'
try: data=json.loads(sidx.read_text(encoding='utf-8')) if sidx.exists() else []
except Exception: data=[]
arr=data.get('pages',[]) if isinstance(data,dict) else data
seen={x.get('url') for x in arr if isinstance(x,dict)}
for e in entries:
    if e['url'] not in seen: arr.append(e)
if isinstance(data,dict): data['pages']=arr
else: data=arr
sidx.write_text(json.dumps(data,indent=2),encoding='utf-8')
urls=sorted(p.name for p in PUBLIC.glob('*.html'))
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'+u+'</loc></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
readme=ROOT/'README.md'
base=readme.read_text(encoding='utf-8',errors='ignore') if readme.exists() else '# GoalOS AGIALPHA Ascension\n'
block='\n\n## GoalOS AGI Agent Mission Control V37\n\nA browser-local AGI Agent Mission Control layer has been added at `public/agi-agent-mission-control.html`. It preserves existing pages and adds one-box objective input, visual flowcharts, AGI Node handoff, Evidence Docket plan, validation route, Reviewer Brief, Action Graph, Ask GoalOS, and use-case playbooks.\n'
if 'GoalOS AGI Agent Mission Control V37' not in base: readme.write_text(base+block,encoding='utf-8')
report={'version':'v37','status':'passed','primaryPage':'public/agi-agent-mission-control.html','publicPages':len(list(PUBLIC.glob('*.html'))),'installedAt':datetime.datetime.utcnow().isoformat()+'Z'}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/agi-agent-mission-control-v37-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
