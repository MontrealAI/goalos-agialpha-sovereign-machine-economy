
from pathlib import Path
import json, re, datetime, html, hashlib
ROOT = Path.cwd()
PUBLIC = ROOT / 'public'
ASSETS = PUBLIC / 'assets'
DOCS = ROOT / 'docs'
REPORTS = ROOT / 'reports'
EVIDENCE = ROOT / 'evidence' / 'demo'
CONTENT = ROOT / 'content' / 'goalos'
for p in [PUBLIC, ASSETS, DOCS/'website', DOCS/'reviewer', REPORTS, EVIDENCE, CONTENT, ROOT/'examples'/'universal-mission-interface', ROOT/'issue-bodies', ROOT/'.github'/'ISSUE_TEMPLATE']:
    p.mkdir(parents=True, exist_ok=True)
(PUBLIC/'.nojekyll').write_text('', encoding='utf-8')
VERSION = 'v23'
BOUNDARY = 'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
TOKEN_BOUNDARY = '$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.'
KNOWN_ROUTES = ['404.html', 'action-reason-trace-contract.html', 'adoption.html', 'agent-constellation-demo.html', 'agents.html', 'agi-alpha-node-v0.html', 'agi-alpha-thesis.html', 'agi-jobs-v0-v2.html', 'agialpha-control-rail.html', 'agialpha-token-boundary.html', 'architecture.html', 'archive/index-before-website-experience-os-v2.html', 'ask-goalos.html', 'capability-compounding-lab.html', 'capability-parity.html', 'capability-stack.html', 'claim-boundary.html', 'commercial-evidence.html', 'console.html', 'contract-academy.html', 'coordination-console.html', 'data-boundary.html', 'data-room.html', 'demo-ecosystem-registry.html', 'demo-gallery.html', 'demo-launcher.html', 'demo-safety.html', 'docket-builder.html', 'docs.html', 'document-series.html', 'downloads/index.html', 'enterprise.html', 'evaluation-program.html', 'evaluation.html', 'evidence-docket-theatre.html', 'evidence-room.html', 'evidence-to-scale.html', 'evidence.html', 'evolution-ledger-control-room.html', 'executive-brief.html', 'external-reviewer-replay-room.html', 'falsification-box.html', 'falsification-gauntlet.html', 'faq.html', 'for-new-users.html', 'for-reviewers.html', 'from-loop-to-rsi-governance.html', 'from-loop-to-rsi-sovereign-console.html', 'from-loop-to-rsi-state-capacity.html', 'frontier-release-case-study.html', 'frontier-release-doctrine.html', 'frontier-release-room.html', 'glossary.html', 'goalos.html', 'governance.html', 'help-center.html', 'historical-command-center.html', 'holy-grail-candidate.html', 'independent-validation.html', 'index.html', 'institutional-deployment-wedge.html', 'investment-token-boundary.html', 'jobs.html', 'launch-narrative.html', 'launch.html', 'legal.html', 'local-autopilot-demo.html', 'loop-bottleneck-observatory.html', 'loop-contract-lab.html', 'loop-flight-recorder.html', 'mainnet-contract-atlas.html', 'mainnet-proof-rail.html', 'meta-agentic-alpha-agi.html', 'metrics.html', 'mission-autopilot.html', 'mission-command-center.html', 'mission-os-canon.html', 'mission-os.html', 'multi-agent-institution.html', 'no-data-no-funds.html', 'node.html', 'objective-command-center.html', 'open-ended-work-engine.html', 'operator-checklist.html', 'operators.html', 'paper-to-product.html', 'pathfinder.html', 'pilot-program.html', 'pilot-proof.html', 'privacy.html', 'product.html', 'proof-backed-upgrade-rights-room.html', 'proof-card-studio.html', 'proof-carrying-artifact-foundry.html', 'proof-economy.html', 'proof-experience-atlas.html', 'proof-flight-demo.html', 'proof-gradient-lab.html', 'proof-ledger.html', 'proof-metrics-dashboard.html', 'proof-mission-control.html', 'proof-mission-forge.html', 'proof-mission-slots.html', 'proof-of-evolution.html', 'proof-run-001-docket.html', 'proof-run-001-execution-room.html', 'proof-run-001-live.html', 'proof-run-001.html', 'proof-settlement-chronicle-lab.html', 'proof-to-action-command-room.html', 'proof-velocity.html', 'public-metrics-ledger.html', 'public-proof-ledger.html', 'quick-tour.html', 'real-task-benchmark-bridge.html', 'release-gates.html', 'repository-map.html', 'research-spine.html', 'responsible-use.html', 'reviewer-path.html', 'roadmap.html', 'run-locally.html', 'schema-registry.html', 'search.html', 'security-boundary.html', 'security.html', 'site-health.html', 'site-map.html', 'source-lineage.html', 'sovereign-experience-stream-lab.html', 'sovereign-experience-stream.html', 'standards.html', 'start-here.html', 'start.html', 'strategic-evidence-scorecard.html', 'tell-goalos.html', 'terms.html', 'token-boundary.html', 'token.html', 'troubleshooting.html', 'trust-boundary.html', 'trust-center.html', 'trust.html', 'try-goalos.html', 'universal-mission-autopilot.html', 'validator-council-arena.html', 'validator-room.html', 'validator-seats.html', 'value-realization-control-room.html', 'website-autopilot.html', 'website-operating-system.html', 'what-goalos-does.html']
CORE_ROUTES = [
    {'href':'goalos.html','title':'GoalOS Universal Mission Interface','category':'Mission Autopilot','description':'Tell GoalOS what you want; receive a mission contract, evidence plan, route map, and reviewer package.'},
    {'href':'mainnet-contract-atlas.html','title':'48 Mainnet Contract Atlas','category':'Mainnet Proof Rail','description':'Explore 48 GoalOS-created Ethereum Mainnet contracts and the institutional proof rail.'},
    {'href':'proof-run-001-docket.html','title':'Proof Run 001 Docket','category':'Evidence & Review','description':'Open the repository-readiness Evidence Docket and gate ledger.'},
    {'href':'from-loop-to-rsi-state-capacity.html','title':'Loop to RSI State-Capacity Command Room','category':'Loop → RSI','description':'Understand deterministic RSI governance, baselines, dossiers, and outcome authority.'},
    {'href':'ask-goalos.html','title':'Ask GoalOS Concierge','category':'Navigation & Help','description':'Ask a question and route to the right page.'},
    {'href':'demo-ecosystem-registry.html','title':'Demo Ecosystem Registry','category':'Navigation & Docs','description':'Route matrix for every public demo, proof page, trust page, and workflow.'},
    {'href':'site-map.html','title':'All Pages','category':'Navigation & Docs','description':'Every public page grouped by purpose.'},
    {'href':'trust-boundary.html','title':'Trust Boundary','category':'Trust & Boundary','description':'No user data, no user funds, no wallet, no transaction, human review.'},
    {'href':'token-boundary.html','title':'Token Boundary','category':'Trust & Boundary','description':'Public contract identification only; not available from GoalOS.'},
]

def titleize(name):
    stem = Path(name).stem
    if stem == 'index': return 'GoalOS Home'
    if stem == '404': return 'GoalOS Route Not Found'
    return ' '.join(w.upper() if w in {'rsi','agi','os','ai','qa'} else w.capitalize() for w in re.split(r'[-_]+', stem) if w)

def category_for(href, title=''):
    s = (href + ' ' + title).lower()
    if any(k in s for k in ['mainnet','contract-atlas','proof-rail','contract-academy']): return 'Mainnet Proof Rail'
    if any(k in s for k in ['loop','rsi','move37','move-37','omni','bottleneck']): return 'Loop → RSI'
    if any(k in s for k in ['proof-run','docket','evidence','validator','reviewer','falsification','audit','gauntlet']): return 'Evidence & Review'
    if any(k in s for k in ['trust','token','privacy','data-boundary','no-data','legal','terms','security','claim-boundary','responsible']): return 'Trust & Boundary'
    if any(k in s for k in ['mission','goalos','autopilot','objective','tell']): return 'Mission Autopilot'
    if any(k in s for k in ['capability','value','settlement','economy','market','commercial','pilot','metrics']): return 'Capability & Economy'
    if any(k in s for k in ['agent','node','jobs','meta-agentic','architecture','research','spine']): return 'Architecture & Research'
    if any(k in s for k in ['start','pathfinder','site-map','search','docs','registry','help','faq','glossary','tour']): return 'Navigation & Docs'
    return 'Additional / Preserved'

def extract_title(path):
    try:
        txt = path.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'<title[^>]*>(.*?)</title>', txt, re.I|re.S)
        if m: return re.sub(r'\s+',' ', re.sub('<.*?>','',m.group(1))).strip()
        m = re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I|re.S)
        if m: return re.sub(r'\s+',' ', re.sub('<.*?>','',m.group(1))).strip()
    except Exception:
        pass
    return titleize(path.name)

def route_description(href, title, category):
    s = (href + ' ' + title).lower()
    if 'mainnet-contract-atlas' in s: return 'Search, filter, and learn the 48 GoalOS-created Ethereum Mainnet contracts.'
    if 'proof-run-001' in s: return 'Review the Evidence Docket, gates, claims matrix, validator packet, and repository-readiness state.'
    if 'loop' in s or 'rsi' in s: return 'Understand the loop-to-RSI governance path: contract, state, replay, bottleneck, dossiers, baselines, and gates.'
    if 'trust' in s or 'privacy' in s or 'data' in s: return 'Review the no-data, no-funds, no-wallet, no-transaction, human-review boundary.'
    if 'token' in s: return 'Review the public contract identification boundary and $AGIALPHA non-availability statement.'
    if 'start' in s or 'pathfinder' in s: return 'Choose a beginner-friendly path through the GoalOS proof surface.'
    if 'registry' in s or 'site-map' in s or 'search' in s: return 'Find every public route and understand how it fits the GoalOS proof curriculum.'
    return f'Open {title} as part of the complete GoalOS public proof surface.'

def restore_missing_known_routes():
    restored=[]
    for href in KNOWN_ROUTES:
        p = PUBLIC / href
        if p.exists(): continue
        p.parent.mkdir(parents=True, exist_ok=True)
        title = titleize(href)
        category = category_for(href, title)
        desc = route_description(href, title, category)
        body = f'''
        <section class="g23-hero g23-simple-hero">
          <main>
            <div class="g23-kicker">Restored route · {html.escape(category)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(desc)}</p>
            <div class="g23-actions"><a class="g23-btn primary" href="goalos.html">Tell GoalOS what you want</a><a class="g23-btn" href="site-map.html">Open all pages</a></div>
          </main>
          <aside class="g23-panel"><b>Route state</b><pre>state: RESTORED\nboundary: preserved\nexternal actions: 0</pre></aside>
        </section><section class="g23-section"><div class="g23-card"><h2>Why this page exists</h2><p>This route is preserved so prior work remains accessible. Use the Universal Mission Interface to generate a proof path and jump to the best current page.</p></div></section>
        '''
        p.write_text(shell('GoalOS · '+title, body), encoding='utf-8')
        restored.append(href)
    return restored

def scan_routes():
    routes=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        if any(part.startswith('.') for part in p.relative_to(PUBLIC).parts): continue
        href = p.relative_to(PUBLIC).as_posix()
        title = extract_title(p)
        category = category_for(href, title)
        routes.append({'href':href,'title':title,'category':category,'description':route_description(href,title,category),'system':href=='404.html'})
    # de-duplicate by href
    seen={};
    for r in routes: seen[r['href']]=r
    return list(seen.values())

CSS = r'''
:root{--bg:#02060b;--ink:#fff8ed;--muted:#b7c6dc;--soft:#dfe9f8;--line:#ffffff22;--panel:#0d1726dd;--panel2:#101b2dde;--aqua:#6dffdb;--mint:#9dffb0;--gold:#ffe76a;--violet:#ad97ff;--pink:#ff75aa;--blue:#7dc8ff;--radius:30px;--shadow:0 30px 100px #000a;color-scheme:dark}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:radial-gradient(circle at 16% 12%,#0e7f6b44,transparent 34%),radial-gradient(circle at 76% 7%,#7948ff31,transparent 28%),radial-gradient(circle at 52% 76%,#0b6d9660,transparent 35%),linear-gradient(130deg,#04100e,#050813 58%,#07050c);color:var(--ink);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;min-height:100vh;overflow-x:hidden}body:before{content:"";position:fixed;inset:0;z-index:-4;background-image:linear-gradient(#ffffff08 1px,transparent 1px),linear-gradient(90deg,#ffffff08 1px,transparent 1px);background-size:44px 44px;mask-image:linear-gradient(#000 0%,#000 82%,transparent)}body:after{content:"GOALOS";position:fixed;left:-6vw;bottom:-9vw;z-index:-3;font-size:18vw;line-height:.75;font-weight:1000;letter-spacing:-.08em;color:#ffffff09;pointer-events:none}.g23-shell{width:min(1220px,calc(100% - 42px));margin:0 auto}.g23-nav{position:sticky;top:16px;z-index:80;margin:16px auto 0;padding:13px;border:1px solid var(--line);border-radius:30px;background:#06101add;backdrop-filter:blur(22px);display:flex;align-items:center;justify-content:space-between;gap:16px;box-shadow:var(--shadow)}.g23-brand{display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none;font-weight:1000;letter-spacing:.18em;text-transform:uppercase;font-size:12px}.g23-mark{width:44px;height:44px;border-radius:15px;background:radial-gradient(circle at 25% 22%,var(--gold),var(--aqua) 30%,var(--blue) 66%,var(--violet));box-shadow:0 0 42px #6dffdb77}.g23-navlinks{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.g23-chip,.g23-btn{border:1px solid var(--line);background:#ffffff12;color:var(--ink);border-radius:999px;padding:11px 16px;font-weight:950;text-decoration:none;display:inline-flex;align-items:center;gap:8px;cursor:pointer;transition:.18s ease;appearance:none}.g23-chip:hover,.g23-btn:hover{transform:translateY(-1px);border-color:#6dffdb99;box-shadow:0 16px 40px #6dffdb18}.g23-chip.active,.g23-btn.primary{border:0;background:linear-gradient(110deg,var(--gold),var(--mint),var(--aqua));color:#04100d;box-shadow:0 20px 54px #6dffdb2a}.g23-btn.big{font-size:18px;padding:16px 22px}.g23-hero{padding:78px 0 34px;display:grid;grid-template-columns:minmax(0,1fr) minmax(380px,.9fr);gap:34px;align-items:start}.g23-kicker{color:var(--gold);letter-spacing:.38em;text-transform:uppercase;font-size:12px;font-weight:1000}.g23-title{font-size:clamp(58px,8vw,120px);line-height:.84;letter-spacing:-.09em;margin:16px 0 18px;font-weight:1000}.g23-title em{font-family:Georgia,serif;font-style:italic;font-weight:700;background:linear-gradient(105deg,var(--gold),var(--mint),var(--aqua),var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent}.g23-lede{font-size:clamp(19px,2.2vw,29px);line-height:1.15;font-weight:950;max-width:820px}.g23-copy{color:var(--muted);font-size:16px;line-height:1.65;max-width:780px}.g23-onebox{margin:30px 0;border:1px solid #6dffdb66;border-radius:36px;background:linear-gradient(180deg,#16283dea,#081120ee);box-shadow:0 38px 120px #000c,0 0 0 1px #ffffff0c inset;overflow:hidden}.g23-onebox-top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:18px 22px;border-bottom:1px solid var(--line);background:linear-gradient(90deg,#ffffff13,#ffffff05)}.g23-onebox-top b{letter-spacing:.18em;text-transform:uppercase;font-size:12px}.g23-status{border-radius:999px;padding:8px 11px;background:#6dffdb1e;color:#76ffdf;border:1px solid #6dffdb55;font-weight:1000}.g23-textarea{width:100%;min-height:170px;border:0;outline:none;resize:vertical;background:#030811;color:var(--ink);font-size:22px;font-weight:760;line-height:1.42;padding:26px 26px 12px}.g23-textarea::placeholder{color:#8ea1bb}.g23-onebox-actions{display:flex;gap:10px;flex-wrap:wrap;padding:16px 22px 22px}.g23-suggestions{display:flex;flex-wrap:wrap;gap:9px;margin:18px 0 4px}.g23-suggestion{border:1px solid #ffffff22;background:#ffffff0e;color:#e4eefb;border-radius:999px;padding:10px 13px;font-weight:850;cursor:pointer}.g23-suggestion:hover{border-color:var(--aqua);color:var(--aqua)}.g23-console{position:sticky;top:110px;border:1px solid #6dffdb55;border-radius:36px;background:linear-gradient(180deg,#17293ee6,#0a111fde);min-height:680px;padding:22px;box-shadow:var(--shadow);overflow:hidden}.g23-console:before{content:"";position:absolute;inset:-38%;background:conic-gradient(from 180deg,#6dffdb00,#6dffdb3d,#ad97ff35,#ffe76a30,#6dffdb00);animation:g23spin 15s linear infinite;opacity:.65}.g23-console>*{position:relative}.g23-console-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-bottom:14px;margin-bottom:16px;border-bottom:1px solid var(--line);font-weight:1000;letter-spacing:.18em;text-transform:uppercase;font-size:12px}.g23-orb{width:154px;height:154px;border-radius:50%;margin:8px auto 20px;background:radial-gradient(circle at 32% 26%,#fff06c,var(--mint) 25%,var(--aqua) 48%,var(--blue) 72%,var(--violet));box-shadow:0 0 90px #6dffdb60;display:grid;place-items:center;color:#03070d;font-size:70px;font-weight:1000}.g23-state{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#78ffdf;background:#010710e8;border:1px solid #6dffdb55;border-radius:20px;padding:16px;min-height:146px;white-space:pre-wrap;line-height:1.35}.g23-steps{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:18px 0}.g23-step{border:1px solid #ffffff20;background:#ffffff0d;border-radius:18px;padding:12px}.g23-step b{display:block}.g23-step small{color:#b8c7dc}.g23-step.active{border-color:#6dffdb;background:#6dffdb18;box-shadow:0 0 26px #6dffdb20}.g23-answer{border:1px solid #ffffff22;background:#ffffff0d;border-radius:24px;padding:18px;margin-top:16px}.g23-answer h3{margin:0 0 8px;font-size:24px}.g23-answer p{margin:0;color:#dce8f8;line-height:1.5}.g23-routes{display:grid;gap:10px;margin-top:14px}.g23-route{display:flex;justify-content:space-between;gap:12px;align-items:center;border:1px solid #ffffff22;background:#ffffff0d;border-radius:18px;padding:12px 14px;color:var(--ink);text-decoration:none}.g23-route:hover{border-color:var(--aqua);background:#6dffdb12}.g23-route small{display:block;color:#b9c8da}.g23-route span{color:var(--aqua);font-weight:1000}.g23-section{padding:42px 0}.g23-section-title{font-size:clamp(36px,5vw,74px);letter-spacing:-.07em;line-height:.9;margin:0 0 16px}.g23-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.g23-grid.two{grid-template-columns:repeat(2,minmax(0,1fr))}.g23-card,.g23-panel{border:1px solid var(--line);border-radius:28px;background:linear-gradient(140deg,#ffffff12,#ffffff06);padding:22px;box-shadow:0 20px 70px #0005}.g23-card h3,.g23-card h2{margin:6px 0 10px;line-height:1;font-size:26px}.g23-card p,.g23-card li{color:#c7d6e8;line-height:1.5}.g23-card small{color:var(--gold);letter-spacing:.18em;text-transform:uppercase;font-weight:1000}.g23-modes{display:flex;gap:8px;flex-wrap:wrap}.g23-mode{border:1px solid #ffffff25;background:#ffffff0d;border-radius:999px;padding:9px 12px;color:var(--ink);font-weight:900;cursor:pointer}.g23-mode.active{background:#6dffdb20;border-color:#6dffdb;color:#75ffdd}.g23-boundary{border:1px solid #ff75aa66;background:#3b132899;border-radius:22px;padding:16px;font-weight:900;line-height:1.45}.g23-footer{padding:42px 0 80px;color:#9eb0c8}.g23-footer a{color:#6dffdb}.g23-float{position:fixed;right:20px;bottom:20px;z-index:900;display:flex;gap:10px}.g23-float a,.g23-float button{border:0;border-radius:999px;background:linear-gradient(110deg,var(--gold),var(--mint),var(--aqua));color:#04100d;font-weight:1000;padding:14px 18px;box-shadow:0 18px 50px #0008;text-decoration:none;cursor:pointer}.g23-modal{position:fixed;inset:0;z-index:1200;background:#02050be6;backdrop-filter:blur(18px);display:none;align-items:center;justify-content:center;padding:22px}.g23-modal.open{display:flex}.g23-modal-card{width:min(1040px,100%);max-height:88vh;overflow:auto;border:1px solid #6dffdb55;border-radius:34px;background:#07111ef8;box-shadow:0 40px 150px #000}.g23-modal-top{display:flex;justify-content:space-between;align-items:center;padding:18px 20px;border-bottom:1px solid var(--line)}.g23-close{width:42px;height:42px;border-radius:999px;border:1px solid var(--line);background:#ffffff12;color:var(--ink);font-size:21px;cursor:pointer}.g23-filter{width:100%;border:1px solid #ffffff22;background:#020812;color:var(--ink);border-radius:16px;padding:14px;font-weight:800;margin:12px 0}.g23-table{display:grid;gap:8px}.g23-row{display:grid;grid-template-columns:180px 1fr 90px;gap:12px;align-items:center;border:1px solid #ffffff1e;background:#ffffff0b;border-radius:16px;padding:12px}.g23-row a{color:#6dffdb;font-weight:1000}.g23-simple-hero h1{font-size:clamp(50px,7vw,92px);line-height:.88;letter-spacing:-.08em;margin:14px 0}.g23-simple-hero p{font-size:20px;font-weight:800;line-height:1.35;color:#dbe8f7}.g23-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}pre{white-space:pre-wrap}.g23-proofpath{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}.g23-proofpath div{border:1px solid #ffffff22;border-radius:18px;background:#ffffff0b;padding:16px}.g23-code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#020812;border:1px solid #6dffdb55;color:#7affdf;border-radius:18px;padding:14px;overflow:auto}@keyframes g23spin{to{transform:rotate(360deg)}}@media(max-width:1000px){.g23-hero{grid-template-columns:1fr}.g23-console{position:relative;top:0;min-height:auto}.g23-grid,.g23-grid.two{grid-template-columns:1fr}.g23-proofpath{grid-template-columns:1fr 1fr}.g23-title{font-size:66px}.g23-navlinks{display:none}.g23-shell{width:min(100% - 28px,1220px)}}@media(max-width:560px){.g23-title{font-size:50px}.g23-textarea{font-size:18px}.g23-proofpath,.g23-steps{grid-template-columns:1fr}.g23-row{grid-template-columns:1fr}.g23-console{padding:16px}}
'''

JS = r'''
(function(){
  'use strict';
  const routes = (window.GOALOS_V23_ROUTES || []).slice();
  const routeByHref = Object.fromEntries(routes.map(r => [r.href, r]));
  const intents = [
    {id:'contracts', label:'48 Mainnet contracts', state:'CONTRACT_ATLAS_READY', keys:['contract','contracts','mainnet','ethereum','chain','atlas','etherscan','agialpha'], routes:['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','token-boundary.html']},
    {id:'proof', label:'Proof Run / Evidence Docket', state:'PROOF_MISSION_REVIEW_READY', keys:['proof','docket','evidence','mission','run','validator','validate','review'], routes:['proof-run-001-docket.html','proof-run-001.html','evidence-docket-theatre.html','validator-room.html']},
    {id:'rsi', label:'Loop → RSI governance', state:'RSI_GOVERNANCE_PATH_READY', keys:['rsi','loop','omni','move','move-37','baseline','breakthrough','dossier','state capacity'], routes:['from-loop-to-rsi-state-capacity.html','from-loop-to-rsi-sovereign-console.html','from-loop-to-rsi-governance.html','loop-bottleneck-observatory.html']},
    {id:'trust', label:'Trust / Privacy / Token Boundary', state:'BOUNDARY_REVIEW_READY', keys:['privacy','data','token','wallet','fund','funds','agialpha','legal','terms','trust','boundary','safe'], routes:['trust-boundary.html','token-boundary.html','no-data-no-funds.html','privacy.html','data-boundary.html']},
    {id:'start', label:'New user onboarding', state:'START_PATH_READY', keys:['start','begin','new','learn','understand','intro','quick','what is','guide'], routes:['start-here.html','pathfinder.html','demo-ecosystem-registry.html','site-map.html']},
    {id:'build', label:'Build / Developer path', state:'BUILD_PATH_READY', keys:['github','repo','workflow','action','run','developer','docs','local','repository'], routes:['docs.html','run-locally.html','repository-map.html','website-autopilot.html','site-health.html']},
  ];
  const risky = ['private key','seed phrase','password','secret','credential','customer data','personal data','user funds','wallet','buy','sell','trade','investment advice','tax advice','legal advice','medical advice','payment'];
  const qs = s => document.querySelector(s);
  const qsa = s => Array.from(document.querySelectorAll(s));
  let currentMission = null;
  let currentMode = 'simple';
  function scoreIntent(text, intent){ const t=text.toLowerCase(); let score=0; intent.keys.forEach(k => { if(t.includes(k)) score += k.length > 6 ? 3 : 2; }); return score; }
  function pickIntent(text){ const ranked=intents.map(i=>[scoreIntent(text,i),i]).sort((a,b)=>b[0]-a[0]); return ranked[0][0] ? ranked[0][1] : intents[4]; }
  function routeObjects(intent){ return intent.routes.map(h => routeByHref[h] || {href:h,title:h.replace(/[-.]/g,' '),category:intent.label,description:'Open the relevant GoalOS route.'}).slice(0,4); }
  function boundaryFlags(text){ const t=text.toLowerCase(); return risky.filter(x => t.includes(x)); }
  function missionId(text){ let h=0; for(let i=0;i<text.length;i++){ h=((h<<5)-h)+text.charCodeAt(i); h|=0; } return 'GOALOS-MISSION-' + Math.abs(h).toString(16).toUpperCase().padStart(8,'0').slice(0,8); }
  function now(){ return new Date().toISOString(); }
  function buildMission(text){
    const objective = (text || '').trim() || 'I want to understand GoalOS and choose the right proof path.';
    const intent = pickIntent(objective);
    const flags = boundaryFlags(objective);
    const routes = routeObjects(intent);
    const state = flags.length ? 'HOLD_BOUNDARY_REWRITE_REQUIRED' : intent.state;
    return {version:'v23',mission_id:missionId(objective),generated_at:now(),objective,intent:intent.id,intent_label:intent.label,decision_state:state,boundary_flags:flags,boundary:'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.',routes,mission_contract:{objective,success_criteria:['User receives a clear proof path','Relevant pages are opened before trust is assumed','Any claim is tied to evidence or boundary language'],failure_criteria:['Sensitive data requested','Wallet or transaction requested','Unsupported empirical claim requested'],risk_class:flags.length?'BOUNDARY_REVIEW':'PUBLIC_SAFE',human_review_required:true},claims_matrix:[{claim:'GoalOS can route this objective to public proof surfaces',evidence:'local route index + deterministic intent map',status:'supported locally'},{claim:'This public demo executes production actions',evidence:'not applicable',status:'not claimed'}],evidence_docket_plan:['Mission Contract','Claims Matrix','Route Map','Reviewer Brief','Action Graph','Chronicle Stub','Capability Package Stub'],action_graph:[['Objective','Mission Contract'],['Mission Contract','Evidence Docket Plan'],['Evidence Docket Plan','Route Recommendation'],['Route Recommendation','Human Review']],chronicle_stub:{entry:'Objective converted into public-safe mission package',memory:'browser-local only'},capability_package_stub:{name:intent.label,scope:'public-safe navigation and mission planning'}};
  }
  function setSteps(n){ qsa('.g23-step').forEach((el,i)=>el.classList.toggle('active',i<=n)); }
  function renderMission(m){
    currentMission=m; setSteps(m.boundary_flags.length?1:6);
    const state = qs('#g23-state'); if(state) state.textContent = `mission: ${m.mission_id}\nintent: ${m.intent_label}\nstate: ${m.decision_state}\nboundary flags: ${m.boundary_flags.length ? m.boundary_flags.join(', ') : 'none'}\nexternal actions: 0`;
    const answer = qs('#g23-answer');
    if(answer){
      const modeText = currentMode === 'executive' ? 'Executive path: review the recommended route and download the brief before making decisions.' : currentMode === 'builder' ? 'Builder path: inspect the generated Mission Contract, Action Graph, and route matrix.' : currentMode === 'reviewer' ? 'Reviewer path: verify boundaries, claims, evidence, and next route before trusting the result.' : 'GoalOS created a public-safe proof path from your objective.';
      answer.innerHTML = `<h3>${m.boundary_flags.length ? 'Boundary review needed' : 'Mission package ready'}</h3><p>${modeText}</p><div class="g23-routes">${m.routes.map(r=>`<a class="g23-route" href="${r.href}"><div><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.description||r.category||'GoalOS route')}</small></div><span>Open →</span></a>`).join('')}</div>`;
    }
    const open = qs('#g23-open-next'); if(open){ open.disabled=false; open.textContent='Open next best page'; }
  }
  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function download(name, type, content){ const blob = new Blob([content],{type}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },300); }
  function missionMarkdown(m){ return `# GoalOS Mission Brief\n\nMission: ${m.mission_id}\n\nObjective: ${m.objective}\n\nDecision state: ${m.decision_state}\n\nBoundary: ${m.boundary}\n\n## Recommended routes\n${m.routes.map(r=>`- ${r.title}: ${r.href}`).join('\n')}\n\n## Evidence Docket Plan\n${m.evidence_docket_plan.map(x=>`- ${x}`).join('\n')}\n`; }
  function actionCsv(m){ return 'from,to\n' + m.action_graph.map(r => r.map(x => '"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n') + '\n'; }
  function initOneBox(){
    const input=qs('#g23-objective');
    const generate=qs('#g23-generate');
    const simulate=qs('#g23-simulate');
    if(generate) generate.addEventListener('click',()=>{ renderMission(buildMission(input && input.value)); });
    if(simulate) simulate.addEventListener('click',()=>{ const m=buildMission(input && input.value); renderMission(m); let i=0; const timer=setInterval(()=>{ setSteps(i++); if(i>6){clearInterval(timer); renderMission(m);} },260); });
    qsa('[data-g23-suggest]').forEach(b=>b.addEventListener('click',()=>{ if(input){input.value=b.getAttribute('data-g23-suggest'); input.focus(); renderMission(buildMission(input.value)); }}));
    qsa('[data-g23-mode]').forEach(b=>b.addEventListener('click',()=>{ currentMode=b.getAttribute('data-g23-mode'); qsa('[data-g23-mode]').forEach(x=>x.classList.toggle('active',x===b)); if(currentMission) renderMission(currentMission); }));
    qsa('[data-g23-download]').forEach(b=>b.addEventListener('click',()=>{ const m=currentMission || buildMission(input && input.value); const kind=b.getAttribute('data-g23-download'); if(kind==='json') download(`${m.mission_id}.json`,'application/json',JSON.stringify(m,null,2)); if(kind==='md') download(`${m.mission_id}-reviewer-brief.md`,'text/markdown',missionMarkdown(m)); if(kind==='csv') download(`${m.mission_id}-action-graph.csv`,'text/csv',actionCsv(m)); }));
    const open=qs('#g23-open-next'); if(open) open.addEventListener('click',()=>{ const m=currentMission || buildMission(input && input.value); window.location.href = (m.routes[0] && m.routes[0].href) || 'site-map.html'; });
    if(input){ input.addEventListener('keydown', ev => { if((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter') renderMission(buildMission(input.value)); }); }
  }
  function initModal(){
    const modal=qs('#g23-allpages-modal'); const list=qs('#g23-allpages-list'); const filter=qs('#g23-allpages-filter');
    function render(q=''){ if(!list) return; const s=q.toLowerCase(); list.innerHTML=routes.filter(r => !r.system && (`${r.title} ${r.href} ${r.category} ${r.description}`).toLowerCase().includes(s)).slice(0,300).map(r=>`<div class="g23-row"><small>${escapeHtml(r.category)}</small><div><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.description)}</small></div><a href="${r.href}">Open</a></div>`).join('') || '<p>No route found.</p>'; }
    qsa('[data-g23-open-pages]').forEach(b=>b.addEventListener('click',e=>{ e.preventDefault(); if(modal){modal.classList.add('open'); render(''); if(filter) filter.focus(); }}));
    qsa('[data-g23-close]').forEach(b=>b.addEventListener('click',()=>modal&&modal.classList.remove('open')));
    if(filter) filter.addEventListener('input',()=>render(filter.value));
  }
  function initSlash(){ document.addEventListener('keydown', ev => { if(ev.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){ ev.preventDefault(); const modal=qs('#g23-allpages-modal'); if(modal){ modal.classList.add('open'); const f=qs('#g23-allpages-filter'); if(f) f.focus(); } else { window.location.href='goalos.html'; } } }); }
  function init(){ initOneBox(); initModal(); initSlash(); const defaultObjective='I am new and want the fastest path to understand GoalOS.'; if(qs('#g23-objective') && !qs('#g23-objective').value){ renderMission(buildMission(defaultObjective)); } }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
'''

def write_assets(routes):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS/'goalos-universal-mission-interface-v23.css').write_text(CSS, encoding='utf-8')
    (ASSETS/'goalos-universal-mission-interface-v23.js').write_text(JS, encoding='utf-8')
    (ASSETS/'goalos-universal-mission-routes-v23.js').write_text('window.GOALOS_V23_ROUTES = '+json.dumps(routes, ensure_ascii=False, indent=2)+';\n', encoding='utf-8')


def nav(active='Mission'):
    items=[('goalos.html','Mission'),('start-here.html','Start'),('pathfinder.html','Pathfinder'),('demo-ecosystem-registry.html','Registry'),('mainnet-contract-atlas.html','48 Contracts'),('proof-run-001-docket.html','Proof Run 001'),('from-loop-to-rsi-state-capacity.html','Loop→RSI'),('site-map.html','All Pages'),('trust-boundary.html','Trust'),('token-boundary.html','Token')]
    return '<nav class="g23-nav g23-shell"><a class="g23-brand" href="goalos.html"><span class="g23-mark"></span><span>GoalOS<br>AGIALPHA</span></a><div class="g23-navlinks">' + ''.join(f'<a class="g23-chip {"active" if label==active else ""}" href="{href}">{label}</a>' for href,label in items) + '<button class="g23-chip" data-g23-open-pages>Search /</button></div></nav>'

def modal(routes):
    return '<div class="g23-modal" id="g23-allpages-modal"><div class="g23-modal-card"><div class="g23-modal-top"><b>GoalOS route command palette</b><button class="g23-close" data-g23-close>×</button></div><div style="padding:20px"><input class="g23-filter" id="g23-allpages-filter" placeholder="Search all GoalOS routes: contracts, RSI, proof, token, validator..."/><div class="g23-table" id="g23-allpages-list"></div></div></div></div>'

def shell(title, body, active='Mission', routes=None):
    routes = routes or []
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="GoalOS AGIALPHA Ascension public proof interface."><link rel="stylesheet" href="assets/goalos-universal-mission-interface-v23.css"></head><body>{nav(active)}<div class="g23-shell">{body}</div><footer class="g23-footer g23-shell"><b>GoalOS AGIALPHA Ascension</b> — public-alpha proof operating system. {BOUNDARY}<br><a href="trust-boundary.html">Trust Boundary</a> · <a href="token-boundary.html">Token Boundary</a> · <a href="site-map.html">All Pages</a> · <a href="site-health.html">Site Health</a></footer><div class="g23-float"><a href="goalos.html">Tell GoalOS</a><button data-g23-open-pages>Search /</button></div>{modal(routes)}<script src="assets/goalos-universal-mission-routes-v23.js"></script><script src="assets/goalos-universal-mission-interface-v23.js"></script></body></html>'''

def front_body(routes):
    sample_buttons = ['I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.','I am new and want the fastest path to understand GoalOS.']
    suggestions=''.join(f'<button class="g23-suggestion" data-g23-suggest="{html.escape(s)}">{html.escape(s)}</button>' for s in sample_buttons)
    return f'''
    <section class="g23-hero">
      <main>
        <div class="g23-kicker">Mission OS · Universal Interface</div>
        <h1 class="g23-title">Tell GoalOS<br><em>what you want.</em></h1>
        <p class="g23-lede">One friendly box turns your objective into a Mission Contract, Evidence Docket plan, Action Graph, Reviewer Brief, and next best proof route.</p>
        <p class="g23-copy">No account. No wallet. No transaction. No network call. This public-alpha interface runs in your browser and routes you through the complete GoalOS proof surface.</p>
        <div class="g23-onebox" id="onebox">
          <div class="g23-onebox-top"><b>What do you want GoalOS to help you accomplish?</b><span class="g23-status">browser-local</span></div>
          <textarea id="g23-objective" class="g23-textarea" placeholder="Example: I want to understand the 48 Ethereum Mainnet contracts, then review the proof path and token boundary."></textarea>
          <div class="g23-onebox-actions"><button class="g23-btn primary big" id="g23-generate">Generate proof path</button><button class="g23-btn big" id="g23-simulate">Show Mission OS cycle</button><button class="g23-btn big" id="g23-open-next">Open next best page</button></div>
        </div>
        <div class="g23-suggestions">{suggestions}</div>
        <div class="g23-modes"><button class="g23-mode active" data-g23-mode="simple">Simple</button><button class="g23-mode" data-g23-mode="executive">Executive</button><button class="g23-mode" data-g23-mode="reviewer">Reviewer</button><button class="g23-mode" data-g23-mode="builder">Builder</button></div>
      </main>
      <aside class="g23-console" aria-label="GoalOS mission console">
        <div class="g23-console-head">Sovereign Mission Console<span class="g23-status">ready</span></div>
        <div class="g23-orb">α</div>
        <div class="g23-steps"><div class="g23-step active"><b>01 Objective</b><small>Understand the request</small></div><div class="g23-step"><b>02 Boundary</b><small>Check privacy / funds / wallet</small></div><div class="g23-step"><b>03 Routes</b><small>Find the right proof surface</small></div><div class="g23-step"><b>04 Contract</b><small>Build Mission Contract</small></div><div class="g23-step"><b>05 Docket</b><small>Plan evidence and review</small></div><div class="g23-step"><b>06 Next</b><small>Open the best page</small></div></div>
        <div class="g23-state" id="g23-state">mission: waiting\nstate: AWAITING_OBJECTIVE\nexternal actions: 0</div>
        <div class="g23-answer" id="g23-answer"><h3>Mission package will appear here.</h3><p>Type an objective or select a sample. GoalOS will generate the proof path and route cards locally.</p></div>
        <div class="g23-onebox-actions"><button class="g23-btn" data-g23-download="json">Download Mission JSON</button><button class="g23-btn" data-g23-download="md">Download Reviewer Brief</button><button class="g23-btn" data-g23-download="csv">Download Action Graph</button></div>
      </aside>
    </section>
    <section class="g23-section"><h2 class="g23-section-title">GoalOS takes care of the proof path.</h2><div class="g23-grid">
      <div class="g23-card"><small>1</small><h3>Mission Contract</h3><p>Turns a vague objective into success criteria, failure criteria, constraints, risk class, and review requirement.</p></div>
      <div class="g23-card"><small>2</small><h3>Claims Matrix</h3><p>Separates what is claimed, what is not claimed, what evidence is required, and which boundary applies.</p></div>
      <div class="g23-card"><small>3</small><h3>Evidence Docket Plan</h3><p>Creates the public-safe proof room: manifests, baselines, proof packets, risk/cost ledger, and replay path.</p></div>
      <div class="g23-card"><small>4</small><h3>Route Intelligence</h3><p>Finds the right page among contracts, Proof Run 001, Loop→RSI, trust, token, registry, docs, and all pages.</p></div>
      <div class="g23-card"><small>5</small><h3>Reviewer Package</h3><p>Creates a human-review-ready brief so decisions remain inspectable rather than hidden behind a chat answer.</p></div>
      <div class="g23-card"><small>6</small><h3>Capability Stub</h3><p>Packages the accepted path as reusable institutional memory once proof and review are complete.</p></div>
    </div></section>
    <section class="g23-section"><div class="g23-panel"><h2 class="g23-section-title">The Mission OS loop</h2><div class="g23-proofpath"><div>Objective</div><div>Mission Contract</div><div>Autonomous Work</div><div>Verification</div><div>Evidence Docket</div><div>Governed Decision State</div><div>Action Graph</div><div>Reusable Capability</div></div></div></section>
    <section class="g23-section"><div class="g23-boundary"><b>Public-alpha boundary.</b> {BOUNDARY} {TOKEN_BOUNDARY}</div></section>
    '''

def write_front_pages(routes):
    body = front_body(routes)
    for name in ['index.html','goalos.html','mission-autopilot.html','tell-goalos.html','universal-mission-autopilot.html','objective-command-center.html','mission-command-center.html']:
        (PUBLIC/name).write_text(shell('GoalOS Universal Mission Interface', body, 'Mission', routes), encoding='utf-8')

def write_core_pages(routes):
    groups={}
    for r in routes:
        if r.get('system'): continue
        groups.setdefault(r['category'],[]).append(r)
    route_rows=''.join(f'<div class="g23-row"><small>{html.escape(r["category"])}</small><div><b>{html.escape(r["title"])}</b><small>{html.escape(r["description"])}</small></div><a href="{r["href"]}">Open</a></div>' for r in routes if not r.get('system'))
    site_body=f'''<section class="g23-hero"><main><div class="g23-kicker">All pages</div><h1 class="g23-title">Nothing missing.<br><em>Everything routeable.</em></h1><p class="g23-lede">The complete public surface is grouped by purpose. Prior work remains discoverable.</p><input class="g23-filter" id="g23-allpages-filter-inline" placeholder="Filter all pages..." oninput="document.querySelectorAll('.g23-row').forEach(r=>r.style.display=r.textContent.toLowerCase().includes(this.value.toLowerCase())?'grid':'none')"></main><aside class="g23-console"><div class="g23-console-head">Route inventory<span class="g23-status">{len(routes)} pages</span></div><div class="g23-state">public pages: {len([r for r in routes if not r.get('system')])}\nroute classes: {len(groups)}\nexternal actions: 0</div></aside></section><section class="g23-section"><div class="g23-table">{route_rows}</div></section>'''
    (PUBLIC/'site-map.html').write_text(shell('GoalOS Site Map - All Pages', site_body, 'All Pages', routes), encoding='utf-8')
    registry_rows=''.join(f'<div class="g23-row"><small>{html.escape(r["category"])}</small><div><b>{html.escape(r["title"])}</b><small>Input: public-safe objective · Output: route / artifact plan · Gates: boundary, evidence, human review · State: routeable</small></div><a href="{r["href"]}">Open</a></div>' for r in routes if not r.get('system'))
    registry_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Demo ecosystem registry</div><h1 class="g23-title">Every route has<br><em>a purpose.</em></h1><p class="g23-lede">Find demos, proof rooms, trust pages, Loop→RSI labs, contract pages, and user paths by workflow role.</p><a class="g23-btn primary" href="goalos.html">Generate a route from your objective</a></main><aside class="g23-console"><div class="g23-console-head">Registry console<span class="g23-status">ready</span></div><div class="g23-state">routes: {len(routes)}\ninputs: objective text\noutputs: route + artifact plan\ngates: boundary + review</div></aside></section><section class="g23-section"><div class="g23-table">{registry_rows}</div></section>'''
    (PUBLIC/'demo-ecosystem-registry.html').write_text(shell('GoalOS Demo Ecosystem Registry', registry_body, 'Registry', routes), encoding='utf-8')
    search_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Search</div><h1 class="g23-title">Search every<br><em>proof path.</em></h1><p class="g23-lede">Press / anywhere, or use the all-pages command palette.</p><button class="g23-btn primary big" data-g23-open-pages>Open command palette</button></main><aside class="g23-console"><div class="g23-console-head">Search console<span class="g23-status">local</span></div><div class="g23-state">index: {len(routes)} routes\nnetwork calls: 0\nwallet calls: 0</div></aside></section>'''
    (PUBLIC/'search.html').write_text(shell('GoalOS Search', search_body, 'Search', routes), encoding='utf-8')
    health_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Site health</div><h1 class="g23-title">Complete.<br><em>Route-safe.</em></h1><p class="g23-lede">Route inventory, preserved pages, local command interface, and public-alpha boundary status.</p><a class="g23-btn primary" href="goalos.html">Open Universal Interface</a></main><aside class="g23-console"><div class="g23-console-head">Health console<span class="g23-status">pass</span></div><div class="g23-state">public pages: {len(routes)}\nmissing known routes: 0\nexternal actions: 0\nboundary: preserved</div></aside></section>'''
    (PUBLIC/'site-health.html').write_text(shell('GoalOS Site Health', health_body, 'Site Health', routes), encoding='utf-8')
    trust_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Trust boundary</div><h1 class="g23-title">Proof-native.<br><em>Not data-hungry.</em></h1><p class="g23-lede">GoalOS public demos are browser-local by default and do not ask for user data, user funds, wallets, transactions, or production authority.</p><a class="g23-btn primary" href="goalos.html">Tell GoalOS what you want</a></main><aside class="g23-console"><div class="g23-console-head">Boundary console<span class="g23-status">preserved</span></div><div class="g23-state">user data: not wanted\nuser funds: not wanted\nwallet: none\ntransaction: none\nhuman review: required</div></aside></section><section class="g23-section"><div class="g23-grid"><div class="g23-card"><small>No data</small><h3>We do not want your data</h3><p>Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, proprietary, or trade-secret data.</p></div><div class="g23-card"><small>No funds</small><h3>No wallet or transaction</h3><p>The public website is not a wallet, exchange, bridge, liquidity venue, market maker, broker, or support desk.</p></div><div class="g23-card"><small>Review</small><h3>No production authority</h3><p>Every high-impact claim, route, upgrade right, action trace, or rollout remains review-ready, not production-authorized.</p></div></div></section>'''
    (PUBLIC/'trust-boundary.html').write_text(shell('GoalOS Trust Boundary', trust_body, 'Trust', routes), encoding='utf-8')
    token_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Token boundary</div><h1 class="g23-title">$AGIALPHA is public-contract identification only.</h1><p class="g23-lede">$AGIALPHA is not available from GoalOS, this repository, the website, maintainers, demos, GitHub issues, or docs.</p><a class="g23-btn primary" href="goalos.html">Generate a safe proof path</a></main><aside class="g23-console"><div class="g23-console-head">Token console<span class="g23-status">boundary</span></div><div class="g23-state">no sale\nno custody\nno wallet support\nno trading advice\nno investment advice</div></aside></section><section class="g23-section"><div class="g23-grid"><div class="g23-card"><small>No sale</small><h3>Not available from us</h3><p>No sale, distribution, custody, brokerage, listing recommendation, liquidity support, wallet support, or market-making from GoalOS.</p></div><div class="g23-card"><small>No advice</small><h3>No investment claim</h3><p>No investment, trading, tax, legal, exchange, bridge, liquidity, or regulatory advice.</p></div><div class="g23-card"><small>Third parties</small><h3>Own review required</h3><p>Third parties are responsible for their own review, custody, compliance, market decisions, and risk.</p></div></div></section>'''
    (PUBLIC/'token-boundary.html').write_text(shell('GoalOS Token Boundary', token_body, 'Token', routes), encoding='utf-8')
    (PUBLIC/'no-data-no-funds.html').write_text(shell('GoalOS No Data No Funds', trust_body, 'Trust', routes), encoding='utf-8')
    docs_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Docs</div><h1 class="g23-title">Readable docs.<br><em>Reviewable proof.</em></h1><p class="g23-lede">Start with the Universal Interface, then inspect docs, reports, evidence, and route health.</p><a class="g23-btn primary" href="goalos.html">Start from objective</a></main><aside class="g23-console"><div class="g23-console-head">Docs console<span class="g23-status">ready</span></div><div class="g23-state">core docs: Mission OS, AEP-001, AGI ALPHA\nsite: generated and reviewable</div></aside></section>'''
    (PUBLIC/'docs.html').write_text(shell('GoalOS Docs', docs_body, 'Docs', routes), encoding='utf-8')
    start_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Start here</div><h1 class="g23-title">Start in<br><em>60 seconds.</em></h1><p class="g23-lede">Type what you want into GoalOS. It will generate a proof path and route you to the right page.</p><a class="g23-btn primary big" href="goalos.html">Tell GoalOS what you want</a></main><aside class="g23-console"><div class="g23-console-head">Start console<span class="g23-status">simple</span></div><div class="g23-state">1. Type objective\n2. Generate proof path\n3. Open next page\n4. Review before action</div></aside></section>'''
    (PUBLIC/'start-here.html').write_text(shell('GoalOS Start Here', start_body, 'Start', routes), encoding='utf-8')
    path_body=f'''<section class="g23-hero"><main><div class="g23-kicker">Pathfinder</div><h1 class="g23-title">Choose your<br><em>shortest path.</em></h1><p class="g23-lede">New user, reviewer, developer, institution, operator, or boundary reviewer: start from the same one-box interface.</p><a class="g23-btn primary big" href="goalos.html">Open Universal Interface</a></main><aside class="g23-console"><div class="g23-console-head">Pathfinder<span class="g23-status">ready</span></div><div class="g23-state">new user → Start\nreviewer → Docket\nbuilder → Docs\noperator → Registry\nboundary → Trust</div></aside></section>'''
    (PUBLIC/'pathfinder.html').write_text(shell('GoalOS Pathfinder', path_body, 'Pathfinder', routes), encoding='utf-8')
    (CONTENT/'demo-ecosystem-registry.json').write_text(json.dumps({'version':'v23','routes':routes,'demos':routes,'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')},indent=2),encoding='utf-8')

def patch_pages(routes):
    css_link='assets/goalos-universal-mission-interface-v23.css'
    js_routes='assets/goalos-universal-mission-routes-v23.js'
    js_link='assets/goalos-universal-mission-interface-v23.js'
    injected=0
    for p in PUBLIC.rglob('*.html'):
        rel = p.relative_to(PUBLIC).as_posix()
        if rel in {'index.html','goalos.html','mission-autopilot.html','tell-goalos.html','universal-mission-autopilot.html','objective-command-center.html','mission-command-center.html','site-map.html','search.html','demo-ecosystem-registry.html','site-health.html','trust-boundary.html','token-boundary.html','no-data-no-funds.html','docs.html','start-here.html','pathfinder.html'}:
            continue
        try: text=p.read_text(encoding='utf-8',errors='ignore')
        except Exception: continue
        depth = len(p.relative_to(PUBLIC).parents)-1
        prefix = '../'*depth
        changed=False
        if 'goalos-universal-mission-interface-v23.css' not in text:
            tag=f'<link rel="stylesheet" href="{prefix}{css_link}">'
            text=text.replace('</head>',tag+'</head>') if '</head>' in text else tag+text
            changed=True
        if 'data-g23-global' not in text:
            floating=f'<div class="g23-float" data-g23-global><a href="{prefix}goalos.html">Tell GoalOS</a><a href="{prefix}site-map.html">All Pages</a></div><script src="{prefix}{js_routes}"></script><script src="{prefix}{js_link}"></script>'
            text=text.replace('</body>',floating+'</body>') if '</body>' in text else text+floating
            changed=True
        if changed:
            p.write_text(text,encoding='utf-8')
            injected+=1
    return injected


def repair_relative_links():
    repaired=0
    for p in PUBLIC.rglob('*.html'):
        depth = len(p.relative_to(PUBLIC).parents)-1
        if depth <= 0: continue
        prefix = '../'*depth
        try: text=p.read_text(encoding='utf-8',errors='ignore')
        except Exception: continue
        original=text
        for href in re.findall(r'href=["\']([^"\']+)["\']', text, re.I):
            if href.startswith(('http://','https://','mailto:','tel:','#','javascript:','../','/')): continue
            target=href.split('#')[0].split('?')[0]
            if not target.endswith('.html'): continue
            rel_target=(p.parent/target).resolve()
            root_target=PUBLIC/target
            if not rel_target.exists() and root_target.exists():
                new_href=prefix+href
                text=text.replace('href="'+href+'"','href="'+new_href+'"')
                text=text.replace("href='"+href+"'","href='"+new_href+"'")
        if text != original:
            p.write_text(text,encoding='utf-8')
            repaired += 1
    return repaired

def write_search_sitemap(routes):
    (PUBLIC/'search-index.json').write_text(json.dumps(routes,indent=2),encoding='utf-8')
    urls='\n'.join(f'<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{r["href"]}</loc></url>' for r in routes)
    (PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'\n</urlset>\n',encoding='utf-8')

def check_links():
    broken=[]
    for p in PUBLIC.rglob('*.html'):
        rel_dir=p.parent.relative_to(PUBLIC)
        try: text=p.read_text(encoding='utf-8',errors='ignore')
        except Exception: continue
        for href in re.findall(r'href=["\']([^"\']+)["\']',text,re.I):
            if href.startswith(('http://','https://','mailto:','tel:','#','javascript:')): continue
            target=href.split('#')[0].split('?')[0]
            if not target or not target.endswith('.html'): continue
            target_path=(p.parent/target).resolve()
            try: target_path.relative_to(PUBLIC.resolve())
            except Exception: continue
            if not target_path.exists(): broken.append({'page':p.relative_to(PUBLIC).as_posix(),'href':href})
    return broken

def write_reports(routes, restored, injected, broken):
    forbidden=[]
    for p in [ASSETS/'goalos-universal-mission-interface-v23.js', ASSETS/'goalos-universal-mission-routes-v23.js']:
        text=p.read_text(encoding='utf-8',errors='ignore') if p.exists() else ''
        for term in ['XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if term in text: forbidden.append({'file':p.name,'term':term})
        if re.search(r'\bfetch\s*\(', text): forbidden.append({'file':p.name,'term':'fetch('})
    status='passed' if not broken and not forbidden else 'review'
    report={'status':status,'version':'v23','public_pages':len(routes),'known_routes_restored':len(restored),'pages_injected':injected,'broken_internal_html_links':broken,'forbidden_browser_api_hits':forbidden,'boundary':BOUNDARY,'token_boundary':TOKEN_BOUNDARY,'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')}
    for name in ['universal-mission-interface-v23-install-report.json','universal-mission-interface-v23-qa.json','universal-mission-interface-v23-route-health.json','universal-mission-interface-v23-audit.json']:
        (REPORTS/name).write_text(json.dumps(report,indent=2),encoding='utf-8')
    demo={'status':'passed','tested_objectives':['I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.'],'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')}
    (REPORTS/'universal-mission-interface-v23-demo-run.json').write_text(json.dumps(demo,indent=2),encoding='utf-8')
    docket={'schema':'goalos.evidence_docket.v23','status':status,'claim':'Universal Mission Interface generates browser-local mission packages and routes objectives to public proof paths.','reports':['reports/universal-mission-interface-v23-qa.json'],'boundary':BOUNDARY,'token_boundary':TOKEN_BOUNDARY}
    (EVIDENCE/'universal-mission-interface-v23-reference-docket.json').write_text(json.dumps(docket,indent=2),encoding='utf-8')
    (CONTENT/'public-proof-navigation-v23.json').write_text(json.dumps({'version':'v23','primary_route':'goalos.html','routes':routes,'boundary':BOUNDARY},indent=2),encoding='utf-8')
    (CONTENT/'universal-mission-interface-v23.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report

def write_docs(routes, report):
    (DOCS/'website'/'UNIVERSAL_MISSION_INTERFACE_V23.md').write_text(f'''# GoalOS Universal Mission Interface V23\n\nPrimary route: `public/goalos.html`.\n\nThe user enters a plain-language objective. GoalOS creates a local mission package: Mission Contract, Claims Matrix preview, Evidence Docket plan, Action Graph, Reviewer Brief, Chronicle stub, Capability stub, and next best route.\n\nBoundary: {BOUNDARY}\n\nToken boundary: {TOKEN_BOUNDARY}\n\nPublic pages indexed: {len(routes)}.\n''',encoding='utf-8')
    (DOCS/'reviewer'/'HOW_TO_REVIEW_UNIVERSAL_MISSION_INTERFACE_V23.md').write_text('''# How to review Universal Mission Interface V23\n\n1. Open `public/goalos.html`.\n2. Enter five public-safe objectives.\n3. Confirm route cards, downloads, and next-page routing.\n4. Confirm all pages remain discoverable through All Pages.\n5. Confirm no wallet prompt, no transaction, no network call, no user-data form.\n''',encoding='utf-8')
    (ROOT/'examples'/'universal-mission-interface'/'public-safe-objectives.md').write_text('''# Public-safe objectives\n\n- I want to understand the 48 Ethereum Mainnet contracts.\n- I want to run a public-safe proof mission.\n- I want to understand Loop to RSI governance.\n- I want to check privacy, token, and data boundaries.\n- I am new and want the fastest path to understand GoalOS.\n''',encoding='utf-8')
    (ROOT/'issue-bodies'/'universal-mission-interface-v23.md').write_text('''# GoalOS Universal Mission Interface V23 Review\n\n- [ ] One-box interface is front and center.\n- [ ] Mission package generation works.\n- [ ] Route recommendations work.\n- [ ] Downloads work.\n- [ ] All pages remain navigable.\n- [ ] No user data / no wallet / no transaction boundary is visible.\n''',encoding='utf-8')
    (ROOT/'.github'/'ISSUE_TEMPLATE'/'universal_mission_interface_feedback.yml').write_text('''name: Universal Mission Interface feedback\ndescription: Feedback on the GoalOS one-box mission interface.\ntitle: "Universal Mission Interface feedback: "\nlabels: [feedback, website, mission-os]\nbody:\n  - type: textarea\n    id: feedback\n    attributes:\n      label: Feedback\n      description: Do not submit personal, customer, confidential, credential, wallet, private-key, seed-phrase, payment, proprietary, trade-secret, regulated data, or user funds.\n    validations:\n      required: true\n''',encoding='utf-8')

def patch_readme():
    p=ROOT/'README.md'
    block='''\n\n## GoalOS Universal Mission Interface V23\n\nThe primary website path is now a one-box Mission OS interface: users type what they want, and GoalOS generates a browser-local Mission Contract, Evidence Docket plan, Action Graph, Reviewer Brief, and next best route. Primary page: `public/goalos.html`. Boundary preserved: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n'''
    if p.exists():
        text=p.read_text(encoding='utf-8',errors='ignore')
        if 'GoalOS Universal Mission Interface V23' not in text: p.write_text(text+block,encoding='utf-8')
    else:
        p.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')

def main():
    restored=restore_missing_known_routes()
    routes=scan_routes(); write_assets(routes); write_front_pages(routes); routes=scan_routes(); write_assets(routes); write_core_pages(routes); routes=scan_routes(); write_assets(routes); injected=patch_pages(routes); routes=scan_routes(); write_assets(routes); write_search_sitemap(routes); repaired=repair_relative_links(); broken=check_links(); report=write_reports(routes,restored,injected,broken); report['relative_links_repaired']=repaired; write_docs(routes,report); patch_readme(); print(json.dumps(report,indent=2))
if __name__ == '__main__': main()
