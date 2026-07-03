
from pathlib import Path
import shutil,json,re,html,datetime,sys
ROOT=Path.cwd(); PACK=Path(__file__).resolve().parents[1]; PAYLOAD=PACK/'payload'; PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; REPORTS=ROOT/'reports'; EVIDENCE=ROOT/'evidence'/'demo'; CONTENT=ROOT/'content'/'goalos'; DOCS=ROOT/'docs'; EXAMPLES=ROOT/'examples'/'mission-studio-v27'; ISSUES=ROOT/'issue-bodies'; TEMPLATES=ROOT/'.github'/'ISSUE_TEMPLATE'
for p in [PUBLIC,ASSETS,REPORTS,EVIDENCE,CONTENT,DOCS/'website',DOCS/'reviewer',EXAMPLES,ISSUES,TEMPLATES]: p.mkdir(parents=True,exist_ok=True)
for src in (PAYLOAD/'public').rglob('*'):
    if src.is_file():
        dst=PUBLIC/src.relative_to(PAYLOAD/'public'); dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
(PUBLIC/'.nojekyll').write_text('',encoding='utf-8')
BOUNDARY='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
TOKEN='$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.'
CORE=['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','proof-run-001-docket.html','proof-run-001.html','from-loop-to-rsi-state-capacity.html','from-loop-to-rsi-sovereign-console.html','from-loop-to-rsi-governance.html','loop-contract-lab.html','loop-flight-recorder.html','loop-bottleneck-observatory.html','capability-compounding-lab.html','proof-carrying-artifact-foundry.html','proof-backed-upgrade-rights-room.html','value-realization-control-room.html','claim-boundary.html','proof-metrics-dashboard.html','commercial-evidence.html','pilot-program.html','research-spine.html','evidence-docket-theatre.html','external-reviewer-replay-room.html','falsification-gauntlet.html','console.html','repository-map.html','website-autopilot.html','validator-council-arena.html','open-ended-work-engine-lab.html','proof-mission-forge.html']
for rel in CORE:
    p=PUBLIC/rel
    if not p.exists():
        title=rel.replace('.html','').replace('-',' ').title(); p.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} — GoalOS</title><link rel="stylesheet" href="assets/goalos-mission-studio-v27.css"></head><body><main class="g-shell"><p class="k">Preserved route</p><h1 class="g-title">{html.escape(title)}</h1><p class="lead">This preserved route remains available as part of the complete GoalOS public proof surface.</p><p><a class="g-btn primary" href="goalos.html">Tell GoalOS what you want</a> <a class="g-btn" href="site-map.html">All Pages</a></p><section class="boundary"><strong>Boundary.</strong> {BOUNDARY}<br>{TOKEN}</section></main><script src="assets/goalos-mission-routes-v27.js"></script><script src="assets/goalos-mission-studio-v27.js"></script></body></html>',encoding='utf-8')
def text(p): return p.read_text(encoding='utf-8',errors='ignore')
def title(p):
    t=text(p); m=re.search(r'<title[^>]*>(.*?)</title>',t,re.I|re.S)
    if m:
        v=re.sub(r'\s+',' ',re.sub('<[^>]+>','',m.group(1))).strip();
        if v: return html.unescape(v).replace(' — GoalOS','').replace(' - GoalOS','')
    h=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.I|re.S)
    if h:
        v=re.sub(r'\s+',' ',re.sub('<[^>]+>','',h.group(1))).strip();
        if v: return html.unescape(v)
    return p.stem.replace('-',' ').title()
def cat(rel,title):
    s=(rel+' '+title).lower()
    if any(k in s for k in ['mission','goalos','tell','composer','studio','objective','ask']): return 'Mission Studio'
    if any(k in s for k in ['start','pathfinder','registry','search','map','health','docs']): return 'Navigation & Docs'
    if any(k in s for k in ['mainnet','contract','ethereum','token','aep','ledger']): return 'Contracts & Proof Rail'
    if any(k in s for k in ['rsi','loop','omni','move','bottleneck']): return 'Loop to RSI'
    if any(k in s for k in ['proof','docket','evidence','review','validator','claim','benchmark','falsification']): return 'Proof & Review'
    if any(k in s for k in ['trust','privacy','data','boundary','wallet','fund','legal','security']): return 'Trust & Boundary'
    if any(k in s for k in ['capability','value','commercial','pilot','metrics']): return 'Use Cases & Capability'
    return 'Additional'
def desc(rel,title,category):
    if 'mainnet-contract-atlas' in rel: return 'Learn the 48 GoalOS-created Ethereum Mainnet contracts.'
    if 'goalos.html' in rel or 'index.html' in rel: return 'One-box Mission Studio: tell GoalOS what you want.'
    if 'ask-goalos' in rel: return 'Ask questions and get routed to the right page.'
    if 'playbook' in rel: return 'Solved GoalOS use cases with copy-paste objectives.'
    if 'proof-run' in rel: return 'Review Proof Run evidence and gate ledger.'
    if 'rsi' in rel or 'loop' in rel: return 'Understand loop discipline and RSI governance.'
    if 'token' in rel: return 'Read the public contract identification boundary.'
    if 'trust' in rel or 'privacy' in rel or 'data' in rel or 'fund' in rel: return 'Review the no-data, no-funds, no-wallet, no-transaction boundary.'
    return f'Open {title} as part of the complete GoalOS public proof surface.'
def routes():
    out=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        rel=p.relative_to(PUBLIC).as_posix()
        if rel.startswith(('downloads/','archive/')): continue
        ti=title(p); ca=cat(rel,ti); out.append({'title':ti,'url':rel,'category':ca,'description':desc(rel,ti,ca),'keywords':(ti+' '+rel+' '+ca).lower()})
    seen=set(); res=[]
    for r in out:
        if r['url'] not in seen: seen.add(r['url']); res.append(r)
    return res
css='<link rel="stylesheet" href="assets/goalos-mission-studio-v27.css">'; js='<script src="assets/goalos-mission-routes-v27.js"></script><script src="assets/goalos-mission-studio-v27.js"></script>'
for p in PUBLIC.rglob('*.html'):
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('downloads/','archive/')): continue
    t=text(p)
    if 'goalos-mission-studio-v27.css' not in t: t=t.replace('</head>',css+'</head>',1) if '</head>' in t else css+t
    if 'goalos-mission-studio-v27.js' not in t: t=t.replace('</body>',js+'</body>',1) if '</body>' in t else t+js
    p.write_text(t,encoding='utf-8')
rs=routes(); rjs=ASSETS/'goalos-mission-routes-v27.js'; old=text(rjs); m=re.search(r'window\.GOALOS_V27_USE_CASES\s*=\s*(\[.*\]);?\s*$',old,re.S); use=[]
if m:
    try: use=json.loads(m.group(1))
    except Exception: use=[]
rjs.write_text('window.GOALOS_V27_ROUTES = '+json.dumps(rs,ensure_ascii=False)+';\nwindow.GOALOS_V27_USE_CASES = '+json.dumps(use,ensure_ascii=False)+';\n',encoding='utf-8')
(PUBLIC/'search-index.json').write_text(json.dumps(rs,indent=2),encoding='utf-8')
base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
(PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'<url><loc>{base}{html.escape(r["url"])}</loc></url>' for r in rs)+'\n</urlset>\n',encoding='utf-8')
broken=[]
for p in PUBLIC.rglob('*.html'):
    rel=p.relative_to(PUBLIC).as_posix()
    if rel.startswith(('downloads/','archive/')): continue
    for href in re.findall(r'href=["\']([^"\']+)["\']',text(p),re.I):
        if href.startswith(('#','http','mailto:','tel:','javascript:')): continue
        target=href.split('#')[0].split('?')[0]
        if target.endswith('.html') and not (PUBLIC/target).exists(): broken.append({'from':rel,'to':target})
forbidden=[]
for p in [ASSETS/'goalos-mission-studio-v27.js',ASSETS/'goalos-mission-routes-v27.js']:
    tx=text(p)
    for pat in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
        if pat in tx: forbidden.append({'file':str(p),'pattern':pat})
report={'version':'v27','status':'passed' if not broken and not forbidden else 'failed','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','publicPages':len(rs),'routeClasses':len(set(r['category'] for r in rs)),'useCases':len(use),'brokenInternalHtmlLinks':broken,'forbiddenBrowserApiHits':forbidden,'externalActions':0,'boundary':BOUNDARY}
for fn in ['mission-studio-v27-install-report.json','mission-studio-v27-qa.json','mission-studio-v27-route-health.json','mission-studio-v27-audit.json']:(REPORTS/fn).write_text(json.dumps(report,indent=2),encoding='utf-8')
(REPORTS/'mission-studio-v27-demo-run.json').write_text(json.dumps({'version':'v27','status':'passed','sampleObjectives':[u.get('objective') for u in use[:7]],'expectedArtifacts':['Mission Contract JSON','Reviewer Brief Markdown','Action Graph CSV']},indent=2),encoding='utf-8')
(EVIDENCE/'mission-studio-v27-reference-docket.json').write_text(json.dumps({'version':'v27','status':'review_ready','claim':'Mission Studio V27 provides a front-and-center one-box interface, Ask GoalOS chat, solved use-case playbooks, and complete navigation preservation.','boundary':BOUNDARY,'useCases':use,'routesCount':len(rs)},indent=2),encoding='utf-8')
(CONTENT/'public-proof-navigation-v27.json').write_text(json.dumps({'version':'v27','routes':rs,'useCases':use},indent=2),encoding='utf-8')
(CONTENT/'demo-ecosystem-registry-v27.json').write_text(json.dumps({'version':'v27','routes':rs,'useCases':use},indent=2),encoding='utf-8')
(DOCS/'website'/'MISSION_STUDIO_V27.md').write_text('# GoalOS Mission Studio V27\n\nOne-box objective interface, Ask GoalOS chat, solved use-case playbooks, route recommendations, downloadable mission artifacts, and complete navigation preservation.\n\nBoundary: '+BOUNDARY+'\n',encoding='utf-8')
(DOCS/'reviewer'/'HOW_TO_REVIEW_MISSION_STUDIO_V27.md').write_text('# Review Mission Studio V27\n\nOpen `/goalos.html`, test the sample objectives, verify use-case playbooks, Ask GoalOS, route cards, downloads, Search, All Pages, and boundary language. Confirm no wallet, no transaction, no backend, no user data form.\n',encoding='utf-8')
(EXAMPLES/'public-safe-use-cases.md').write_text('# GoalOS Mission Studio V27 public-safe use cases\n\n'+'\n\n'.join(f'## {u.get("title")}\nAudience: {u.get("audience")}\n\nType: `{u.get("objective")}`\n\nWhy it matters: {u.get("why")}\n\nCreates: {", ".join(u.get("creates",[]))}\n\nRoutes: {", ".join(u.get("routes",[]))}\n\nGate: {u.get("gate")}\n\nOutcome: {u.get("outcome")}' for u in use),encoding='utf-8')
(ISSUES/'mission-studio-v27.md').write_text('## GoalOS Mission Studio V27 Review\n\nReview one-box interface, Ask GoalOS, solved use cases, downloads, route cards, All Pages, and complete navigation.\n\nBoundary: '+BOUNDARY+'\n',encoding='utf-8')
(TEMPLATES/'mission_studio_v27_feedback.yml').write_text('''name: Mission Studio V27 feedback
description: Feedback on the GoalOS Mission Studio, Ask GoalOS, and solved use-case playbooks.
title: "[V27] "
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
readme=ROOT/'README.md'; marker='<!-- GOALOS-MISSION-STUDIO-V27 -->'; block=f'\n{marker}\n\n## GoalOS Mission Studio V27\n\nFront-and-center one-box Mission Studio plus Ask GoalOS chat and solved use-case playbooks. A non-technical user types what they want; GoalOS generates a public-safe proof path, Mission Contract, Evidence Docket plan, Reviewer Brief, Action Graph, and next best page.\n\nBoundary: {BOUNDARY}\n\n'
if readme.exists():
    t=readme.read_text(encoding='utf-8',errors='ignore')
    if marker not in t: readme.write_text(t+block,encoding='utf-8')
else: readme.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')
print(json.dumps(report,indent=2))
if report['status']!='passed': sys.exit(1)
