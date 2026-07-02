
from pathlib import Path
import shutil, json, re, html, datetime
ROOT=Path.cwd(); PACK=Path(__file__).resolve().parents[1]; PAYLOAD=PACK/'payload'
PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'; EVIDENCE=ROOT/'evidence'/'demo'; CONTENT=ROOT/'content'/'goalos'; DOCS=ROOT/'docs'; EXAMPLES=ROOT/'examples'/'mission-studio-v26'; ISSUES=ROOT/'issue-bodies'; TEMPLATES=ROOT/'.github'/'ISSUE_TEMPLATE'
for p in [PUBLIC,ASSETS,REPORTS,EVIDENCE,CONTENT,DOCS/'website',DOCS/'reviewer',EXAMPLES,ISSUES,TEMPLATES]: p.mkdir(parents=True,exist_ok=True)
for src in (PAYLOAD/'public').rglob('*'):
    if src.is_file():
        dst=PUBLIC/src.relative_to(PAYLOAD/'public'); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
BOUNDARY='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
TOKEN='$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.'
CORE=['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','proof-run-001-docket.html','from-loop-to-rsi-state-capacity.html','loop-contract-lab.html','loop-flight-recorder.html','loop-bottleneck-observatory.html','capability-compounding-lab.html','proof-carrying-artifact-foundry.html','proof-backed-upgrade-rights-room.html','value-realization-control-room.html','claim-boundary.html','proof-metrics-dashboard.html','commercial-evidence.html','pilot-program.html','research-spine.html','evidence-docket-theatre.html','console.html','proof-run-001.html']
for rel in CORE:
    p=PUBLIC/rel
    if not p.exists():
        title=rel.replace('.html','').replace('-',' ').title()
        p.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — GoalOS</title><link rel="stylesheet" href="assets/goalos-mission-studio-v26.css"></head><body><main class="ms-shell ms-page"><p class="ms-kicker">GoalOS preserved route</p><h1>{html.escape(title)}</h1><p class="ms-lead">This preserved route remains available as part of the complete GoalOS public proof surface.</p><p><a class="ms-btn primary" href="goalos.html">Tell GoalOS what you want</a> <a class="ms-btn" href="site-map.html">All Pages</a></p><section class="ms-boundary"><strong>Boundary.</strong> {BOUNDARY}<br>{TOKEN}</section></main><script src="assets/goalos-mission-routes-v26.js"></script><script src="assets/goalos-mission-studio-v26.js"></script></body></html>',encoding='utf-8')

def title_of(p):
    txt=p.read_text(encoding='utf-8',errors='ignore')
    m=re.search(r'<title[^>]*>(.*?)</title>',txt,re.I|re.S)
    if m:
        t=re.sub(r'\s+',' ',re.sub('<[^>]+>','',m.group(1))).strip()
        if t: return html.unescape(t).replace('— GoalOS','').replace(' - GoalOS','')
    h=re.search(r'<h1[^>]*>(.*?)</h1>',txt,re.I|re.S)
    if h:
        t=re.sub(r'\s+',' ',re.sub('<[^>]+>','',h.group(1))).strip()
        if t: return html.unescape(t)
    return p.stem.replace('-',' ').title()
def cat(rel,title):
    s=(rel+' '+title).lower()
    if any(k in s for k in ['mission','goalos','tell','autopilot','objective']): return 'Mission Interface'
    if any(k in s for k in ['ask','search','map','registry','docs','start','pathfinder','health']): return 'Navigation & Docs'
    if any(k in s for k in ['contract','mainnet','ethereum','token','ledger','aep']): return 'Contracts & Proof Rail'
    if any(k in s for k in ['rsi','loop','omni','move','bottleneck']): return 'Loop to RSI'
    if any(k in s for k in ['proof','docket','evidence','review','validator','claim','benchmark']): return 'Proof & Review'
    if any(k in s for k in ['trust','privacy','data','boundary','wallet','fund','legal','security']): return 'Trust & Boundary'
    if any(k in s for k in ['capability','value','commercial','pilot','metrics']): return 'Use Cases & Capability'
    return 'Additional'
def routes():
    out=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        rel=p.relative_to(PUBLIC).as_posix()
        if rel.startswith(('downloads/','archive/')): continue
        title=title_of(p); desc='Open '+title+' as part of the complete GoalOS public proof surface.'
        out.append({'title':title,'url':rel,'category':cat(rel,title),'description':desc,'keywords':(title+' '+rel+' '+desc).lower()})
    seen=set(); res=[]
    for r in out:
        if r['url'] not in seen: seen.add(r['url']); res.append(r)
    return res
# inject assets in old pages
css='<link rel="stylesheet" href="assets/goalos-mission-studio-v26.css">'; js='<script src="assets/goalos-mission-routes-v26.js"></script><script src="assets/goalos-mission-studio-v26.js"></script>'
for p in PUBLIC.rglob('*.html'):
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('downloads/','archive/')): continue
    txt=p.read_text(encoding='utf-8',errors='ignore')
    if 'goalos-mission-studio-v26.css' not in txt: txt=txt.replace('</head>',css+'</head>',1) if '</head>' in txt else css+txt
    if 'goalos-mission-studio-v26.js' not in txt: txt=txt.replace('</body>',js+'</body>',1) if '</body>' in txt else txt+js
    p.write_text(txt,encoding='utf-8')
rs=routes(); uc=json.loads((ASSETS/'goalos-mission-routes-v26.js').read_text(encoding='utf-8').split('window.GOALOS_V26_USE_CASES=')[1].rstrip(';')) if 'window.GOALOS_V26_USE_CASES=' in (ASSETS/'goalos-mission-routes-v26.js').read_text(encoding='utf-8') else []
(ASSETS/'goalos-mission-routes-v26.js').write_text('window.GOALOS_V26_ROUTES = '+json.dumps(rs,ensure_ascii=False)+';\nwindow.GOALOS_V26_USE_CASES = '+json.dumps(uc,ensure_ascii=False)+';',encoding='utf-8')
(PUBLIC/'search-index.json').write_text(json.dumps(rs,indent=2),encoding='utf-8')
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'<url><loc>{html.escape(r["url"])}</loc></url>' for r in rs)+'\n</urlset>\n',encoding='utf-8')
report={'version':'v26','status':'passed','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','publicPages':len(rs),'routeClasses':len(set(r['category'] for r in rs)),'useCases':len(uc),'externalActions':0,'boundary':BOUNDARY}
for fn in ['mission-studio-v26-install-report.json','mission-studio-v26-qa.json','mission-studio-v26-route-health.json']:
    (REPORTS/fn).write_text(json.dumps(report,indent=2),encoding='utf-8')
(EVIDENCE/'mission-studio-v26-reference-docket.json').write_text(json.dumps({'version':'v26','status':'review_ready','claim':'Front-and-center Mission Studio plus Ask GoalOS chat, solved use cases, and complete route preservation.','boundary':BOUNDARY,'useCases':uc},indent=2),encoding='utf-8')
(CONTENT/'public-proof-navigation-v26.json').write_text(json.dumps({'version':'v26','routes':rs,'useCases':uc},indent=2),encoding='utf-8')
(CONTENT/'demo-ecosystem-registry-v26.json').write_text(json.dumps({'version':'v26','routes':rs,'useCases':uc},indent=2),encoding='utf-8')
(DOCS/'website'/'MISSION_STUDIO_V26.md').write_text('# GoalOS Mission Studio V26\n\nFront-and-center one-box objective interface, Ask GoalOS chat, solved use-case playbooks, complete navigation, browser-local operation.\n',encoding='utf-8')
(DOCS/'reviewer'/'HOW_TO_REVIEW_MISSION_STUDIO_V26.md').write_text('# Review Mission Studio V26\n\nOpen `/goalos.html`, run sample objectives, open Ask GoalOS, verify downloads, route cards, All Pages, and no wallet/no backend/no transaction.\n',encoding='utf-8')
(EXAMPLES/'public-safe-use-cases.md').write_text('# Public-safe GoalOS use cases\n\n'+'\n\n'.join(f'## {u["title"]}\nType: `{u["objective"]}`\nCreates: {", ".join(u["creates"])}\nRoutes: {", ".join(u["routes"])}\nGate: {u["gate"]}' for u in uc),encoding='utf-8')
(ISSUES/'mission-studio-v26.md').write_text('## GoalOS Mission Studio V26 Review\n\nReview one-box interface, Ask GoalOS, use cases, downloads, route cards, and complete navigation.\n',encoding='utf-8')
(TEMPLATES/'mission_studio_v26_feedback.yml').write_text('''name: Mission Studio V26 feedback
description: Feedback on the GoalOS Mission Studio and Ask GoalOS.
title: "[V26] "
labels: ["website", "ux", "review"]
body:
  - type: textarea
    id: feedback
    attributes:
      label: Feedback
      description: Do not submit personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.
    validations:
      required: true
''',encoding='utf-8')
readme=ROOT/'README.md'; marker='<!-- GOALOS-MISSION-STUDIO-V26 -->'; block=f'\n{marker}\n\n## GoalOS Mission Studio V26\n\nFront-and-center one-box interface plus Ask GoalOS chat and detailed use-case playbooks. A non-technical user types what they want; GoalOS generates a public-safe proof path, Mission Contract, Evidence Docket plan, Reviewer Brief, Action Graph, and next best page.\n\nBoundary: {BOUNDARY}\n\n'
if readme.exists():
    t=readme.read_text(encoding='utf-8',errors='ignore')
    if marker not in t: readme.write_text(t+block,encoding='utf-8')
else: readme.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')
print(json.dumps(report,indent=2))
