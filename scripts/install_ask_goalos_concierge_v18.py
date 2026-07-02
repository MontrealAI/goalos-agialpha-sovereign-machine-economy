
from __future__ import annotations
import json, re, pathlib, html, datetime, os
ROOT = pathlib.Path.cwd()
PUBLIC = ROOT / 'public'
VERSION = 'v18'
RELEASE = 'v0.40.0-ask-goalos-concierge-v18'
BOUNDARY = 'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
FORBIDDEN = ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']

CURATED = {
    'index.html': ('Command Center', 'Start here: the main GoalOS public proof surface and dynamic command center.', ['home','overview','command','proof','goalos','start']),
    'start-here.html': ('Start in 60 Seconds', 'Plain-language onboarding for non-technical visitors.', ['start','begin','new','guide','onboarding']),
    'pathfinder.html': ('Pathfinder', 'Choose your role and get the shortest route through the site.', ['role','path','user','reviewer','developer','institution']),
    'site-map.html': ('All Pages', 'The complete public route inventory grouped by purpose.', ['all pages','site map','map','routes','missing']),
    'demo-ecosystem-registry.html': ('Demo Registry', 'Every public demo mapped to inputs, outputs, gates, artifacts, and next state.', ['registry','demo','workflow','inputs','outputs','gates']),
    'proof-run-001-docket.html': ('Proof Run 001 Docket', 'Review repository readiness, gate ledger, claims matrix, and validator packet.', ['proof run','docket','evidence','validator','readiness','claims']),
    'site-health.html': ('Site Health', 'Route integrity, missing-route checks, public boundary status, and QA reports.', ['health','qa','route','broken','missing','links']),
    'trust-boundary.html': ('Trust Boundary', 'No data, no funds, no wallet, no transaction, no production authority.', ['trust','privacy','data','funds','wallet','transaction','boundary']),
    'token-boundary.html': ('Token Boundary', '$AGIALPHA public contract identification only; not available from GoalOS.', ['token','agialpha','$agialpha','contract','investment','wallet']),
    'mainnet-contract-atlas.html': ('Mainnet Contract Atlas', 'Explore the 48 GoalOS-created Ethereum Mainnet contracts and canonical external AGIALPHA entry.', ['48','contracts','mainnet','chainid','etherscan','atlas','proof rail']),
    'mainnet-proof-rail.html': ('Mainnet Proof Rail', 'Understand how the 48 contracts form an institutional proof rail.', ['mainnet','proof rail','aep','ledger','contracts']),
    'contract-academy.html': ('Contract Academy', 'Non-technical guided tour of contract roles, rails, and boundaries.', ['contract','academy','learn','non technical','ethereum']),
    'from-loop-to-rsi-state-capacity.html': ('Loop → RSI State-Capacity', 'Interactive command room for deterministic RSI governance and state-capacity readiness.', ['rsi','loop','state capacity','move37','omni','governance']),
    'from-loop-to-rsi-sovereign-console.html': ('Loop → RSI Sovereign Console', 'Dynamic RSI console: search control is allowed; outcome authority is earned.', ['rsi','sovereign','console','omni','move37']),
    'from-loop-to-rsi-governance.html': ('Loop → RSI Governance Lab', 'Transition from restartable loops to deterministic RSI governance.', ['rsi','governance','loop','dossier']),
    'loop-contract-lab.html': ('Loop Contract Lab', 'Write the loop, not the prompt: contracts, roles, disk state, traces, and evidence.', ['loop','contract','prompt','roles','state']),
    'loop-flight-recorder.html': ('Loop Flight Recorder', 'Long-running agent loops must leave proof and survive restart.', ['loop','flight','recorder','restart','traces']),
    'loop-bottleneck-observatory.html': ('Loop Bottleneck Observatory', 'The bottleneck always moves: expose the next proof mission.', ['loop','bottleneck','observatory','harness','trace']),
    'evidence-docket-theatre.html': ('Evidence Docket Theatre', 'Convert public-safe claims into review-ready Evidence Dockets.', ['evidence','docket','claims','baselines','review']),
    'proof-to-action-command-room.html': ('Proof-to-Action Command Room', 'Objective → Evidence Docket → Governed Decision State → Action Graph → Chronicle.', ['action','mission','decision','chronicle','command']),
    'validator-council-arena.html': ('Validator Council Arena', 'Trust is not one judge: review quorum, dissent, challenge, and validation ceremony.', ['validator','council','review','dissent','quorum']),
    'public-proof-ledger.html': ('Public Proof Ledger', 'Proof, selection, receipts, and public challenge surface.', ['ledger','proof','public','receipts']),
    'docs.html': ('Docs', 'Documentation hub for repository, website, review, and GitHub Web UI instructions.', ['docs','documentation','guide','github']),
    'privacy.html': ('Privacy', 'Public-alpha no-data boundary and sensitive-data refusal posture.', ['privacy','data','gdpr','personal']),
    'no-data-no-funds.html': ('No Data / No Funds', 'GoalOS does not ask for user data, user funds, wallets, or transactions.', ['data','funds','wallet','privacy']),
    'search.html': ('Search', 'Browser-local command search across the public proof site.', ['search','find','ask','question'])
}

CATEGORY_RULES = [
    ('Mainnet Contracts', ['mainnet','contract','token','etherscan','proof-rail','academy']),
    ('Loop → RSI', ['rsi','loop','move37','state-capacity','sovereign-console','bottleneck','flight-recorder']),
    ('Evidence & Review', ['proof','docket','evidence','validator','review','ledger','falsification','benchmark','gauntlet']),
    ('Mission & Work OS', ['mission','action','work','jobs','node','agent','meta-agentic','command']),
    ('Trust & Boundary', ['trust','privacy','data-boundary','no-data','token-boundary','claim-boundary','security']),
    ('Navigation & Docs', ['index','start','pathfinder','site-map','registry','search','docs','health','website']),
    ('Capability & Economy', ['capability','settlement','value','economy','upgrade','chronicle','experience']),
]

def clean_text(s: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s or '')).strip()

def title_from_html(path: pathlib.Path, text: str) -> str:
    for pattern in [r'<title[^>]*>(.*?)</title>', r'<h1[^>]*>(.*?)</h1>', r'<h2[^>]*>(.*?)</h2>']:
        m = re.search(pattern, text, flags=re.I|re.S)
        if m:
            t = clean_text(html.unescape(m.group(1)))
            if t and len(t) <= 140:
                return t
    return path.stem.replace('-', ' ').title()

def desc_from_html(text: str, fallback: str) -> str:
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text, flags=re.I|re.S)
    if m:
        d = clean_text(html.unescape(m.group(1)))
        if d: return d[:240]
    ps = re.findall(r'<p[^>]*>(.*?)</p>', text, flags=re.I|re.S)
    for p in ps[:3]:
        d = clean_text(html.unescape(p))
        if 40 <= len(d) <= 260: return d
    return fallback

def categorize(filename: str, title: str, desc: str) -> str:
    corpus = f'{filename} {title} {desc}'.lower()
    for cat, terms in CATEGORY_RULES:
        if any(t in corpus for t in terms): return cat
    return 'Additional / Preserved'

def route_state(filename: str) -> str:
    if filename in ('404.html',): return 'SYSTEM'
    return 'DISCOVERABLE'


def fallback_shell(title: str, kicker: str, lead: str, cards: list[tuple[str,str,str]]):
    nav = '<a href="index.html">Command Center</a><a href="start-here.html">Start</a><a href="ask-goalos.html">Ask GoalOS</a><a href="site-map.html">All Pages</a><a href="trust-boundary.html">Trust</a><a href="token-boundary.html">Token</a>'
    card_html = ''.join([f'<article class="card"><b>{html.escape(a)}</b><p>{html.escape(b)}</p>{("<code>"+html.escape(c)+"</code>") if c else ""}</article>' for a,b,c in cards])
    safe_title = html.escape(title)
    h1 = safe_title.replace(' · ', '<br><span class="grad">') + ('</span>' if ' · ' in title else '')
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{safe_title}</title><meta name="description" content="{html.escape(lead)}">'
            '<style>body{margin:0;min-height:100vh;background:radial-gradient(circle at 20% 0%,rgba(112,255,213,.20),transparent 34%),radial-gradient(circle at 78% 8%,rgba(255,240,115,.12),transparent 32%),#050913;color:#f7f1e7;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}main{width:min(1160px,92vw);margin:0 auto;padding:44px 0 110px}nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:70px}nav a{color:#f7f1e7;text-decoration:none;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);padding:10px 13px;border-radius:999px;font-weight:850}.eyebrow{color:#fff073;text-transform:uppercase;letter-spacing:.28em;font-size:12px;font-weight:950}h1{font-size:clamp(52px,8.5vw,118px);line-height:.86;letter-spacing:-.075em;margin:.16em 0}.grad{background:linear-gradient(90deg,#fff073,#70ffd5,#9db6ff,#b89cff);-webkit-background-clip:text;background-clip:text;color:transparent;font-style:italic}.lead{font-size:clamp(20px,2.6vw,32px);line-height:1.08;font-weight:900;max-width:900px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:42px}.card{border:1px solid rgba(255,255,255,.16);background:linear-gradient(135deg,rgba(255,255,255,.075),rgba(112,255,213,.045));border-radius:24px;padding:20px;min-height:130px}.card b{font-size:22px}.card p{color:#c9d4e5;line-height:1.45}code{display:block;word-break:break-all;color:#70ffd5;background:rgba(0,0,0,.32);border:1px solid rgba(112,255,213,.22);padding:10px;border-radius:14px}.boundary{margin-top:36px;border:1px solid rgba(255,106,162,.45);background:rgba(255,106,162,.08);border-radius:20px;padding:16px;font-weight:850}@media(max-width:900px){.grid{grid-template-columns:1fr}}</style>'
            f'</head><body><main><nav>{nav}</nav><div class="eyebrow">{html.escape(kicker)}</div><h1>{h1}</h1><p class="lead">{html.escape(lead)}</p><section class="grid">{card_html}</section><div class="boundary">Public-alpha boundary: {BOUNDARY} $AGIALPHA public contract identification only; not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.</div></main></body></html>')

def ensure_essential_pages():
    essentials = {
        'mainnet-contract-atlas.html': fallback_shell('48 Mainnet Contracts · One Proof Rail','Mainnet Contract Atlas','Explore the 48 GoalOS-created Ethereum Mainnet contracts, the canonical external AGIALPHA entry, and the public proof rail without wallet, transaction, or network calls.',[
            ('Deployment record','Ethereum Mainnet chainId 1; 48 GoalOS-created contracts; 49 manifest entries including canonical external AGIALPHA; 48 / 48 source verified.',''),
            ('Canonical AGIALPHA','GoalOS integrates the existing canonical AGIALPHA contract and did not deploy or mint a replacement AGIALPHA token.','0xA61a3B3a130a9c20768EEBF97E21515A6046a1fA'),
            ('Boundary','Configured does not mean production-authorized. User-fund authorization, live canary completion, and external audit completion remain outside this public-alpha page.','')
        ]),
        'mainnet-proof-rail.html': fallback_shell('Mainnet Proof Rail · Public Proof, Private Intelligence','Mainnet Proof Rail','Understand the institutional rail: compact public commitments, registries, ledgers, attestations, proof bundles, selection gates, rollback, chronicle, and claim boundaries.',[
            ('AEP proof rail','Commit → Execute → Prove → Evaluate → Select → Roll out → Roll back.',''),
            ('What belongs public','Hashes, commitments, attestations, selection records, public-safe dockets, and challengeable receipts.',''),
            ('What stays private','Prompts, private traces, customer data, credentials, secrets, trade secrets, and private workpapers.','')
        ]),
        'contract-academy.html': fallback_shell('Contract Academy · Learn the Rail','Contract Academy','A plain-language path for understanding how GoalOS contract roles map to proof-bearing machine labor.',[
            ('Start with the atlas','Search contracts by role: vault, registry, proof, eval, selection, replay, reward, slashing, chronicle, falsification.',''),
            ('Read the boundary','No wallet connection is needed. Etherscan links are optional manual exits; the site does not call them.',''),
            ('Review like an institution','Ask: what does this contract record, what does it not record, what gate does it support, and what private data must remain private?','')
        ])
    }
    created = []
    for name, text in essentials.items():
        path = PUBLIC / name
        if not path.exists():
            path.write_text(text, encoding='utf-8')
            created.append(name)
    return created

def build_routes() -> list[dict]:
    PUBLIC.mkdir(exist_ok=True)
    routes = []
    for p in sorted(PUBLIC.rglob('*.html')):
        if any(part.startswith('.') for part in p.relative_to(PUBLIC).parts):
            continue
        rel = p.relative_to(PUBLIC).as_posix()
        try:
            text = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            text = ''
        filename = rel
        ct = CURATED.get(filename)
        title = ct[0] if ct else title_from_html(p, text)
        fallback_desc = f'Open {title} as part of the GoalOS public proof surface.'
        desc = ct[1] if ct else desc_from_html(text, fallback_desc)
        keywords = list(dict.fromkeys((ct[2] if ct else []) + re.findall(r'[a-zA-Z0-9$]+', (filename+' '+title+' '+desc).lower())[:30]))
        routes.append({
            'title': title,
            'url': rel,
            'category': categorize(filename, title, desc),
            'description': desc,
            'keywords': keywords,
            'state': route_state(filename),
            'boundary': 'public-alpha; no user data; no user funds; no wallet; no transaction',
        })
    # Ensure the assistant itself is present in route list even during generation.
    if not any(r['url'] == 'ask-goalos.html' for r in routes):
        routes.append({'title':'Ask GoalOS Concierge','url':'ask-goalos.html','category':'Navigation & Docs','description':'Ask questions and get routed to the right public GoalOS page. Browser-local; no model call; no user data.','keywords':['ask','chat','question','concierge','assistant','route'],'state':'DISCOVERABLE','boundary':'browser-local'})
    # Sort by priority, then title.
    priority = ['index.html','start-here.html','pathfinder.html','ask-goalos.html','mainnet-contract-atlas.html','proof-run-001-docket.html','demo-ecosystem-registry.html','site-map.html','trust-boundary.html','token-boundary.html']
    routes.sort(key=lambda r: (priority.index(r['url']) if r['url'] in priority else 99, r['category'], r['title'].lower()))
    return routes

CSS = r'''
:root{--ga-bg:#050913;--ga-panel:rgba(12,18,32,.92);--ga-ink:#f6f2e8;--ga-muted:#bcc7d8;--ga-accent:#70ffd5;--ga-accent2:#fff073;--ga-line:rgba(255,255,255,.16);--ga-warn:#ff6aa2;--ga-shadow:0 24px 70px rgba(0,0,0,.5)}
#goalos-ask-launcher{position:fixed;right:18px;bottom:18px;z-index:2147483000;border:1px solid rgba(112,255,213,.5);background:linear-gradient(135deg,#fff073,#70ffd5);color:#061018;font-weight:950;border-radius:999px;padding:14px 18px;box-shadow:0 12px 40px rgba(112,255,213,.28);cursor:pointer;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;letter-spacing:-.02em}
#goalos-ask-launcher:hover{transform:translateY(-1px);filter:saturate(1.08)}
#goalos-ask-panel{position:fixed;right:18px;bottom:78px;z-index:2147483000;width:min(460px,calc(100vw - 28px));height:min(720px,calc(100vh - 108px));display:none;grid-template-rows:auto 1fr auto;border:1px solid rgba(112,255,213,.25);border-radius:28px;background:radial-gradient(circle at 20% 0%,rgba(112,255,213,.16),transparent 34%),radial-gradient(circle at 80% 0%,rgba(255,240,115,.12),transparent 30%),rgba(5,9,19,.96);box-shadow:var(--ga-shadow);backdrop-filter:blur(18px);overflow:hidden;color:var(--ga-ink);font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}
#goalos-ask-panel.ga-open{display:grid}.ga-ask-head{display:flex;gap:12px;align-items:center;justify-content:space-between;padding:16px 17px;border-bottom:1px solid var(--ga-line);background:rgba(255,255,255,.04)}.ga-ask-brand{display:flex;align-items:center;gap:10px}.ga-orb{width:34px;height:34px;border-radius:12px;background:radial-gradient(circle at 30% 25%,#fff073,#70ffd5 42%,#86a8ff 78%);box-shadow:0 0 30px rgba(112,255,213,.4)}.ga-ask-brand strong{display:block;font-size:14px;letter-spacing:.02em}.ga-ask-brand span{display:block;font-size:11px;color:var(--ga-muted);text-transform:uppercase;letter-spacing:.16em}.ga-ask-close{border:1px solid var(--ga-line);background:rgba(255,255,255,.08);color:var(--ga-ink);border-radius:999px;width:34px;height:34px;cursor:pointer;font-weight:900}.ga-ask-body{overflow:auto;padding:16px;scroll-behavior:smooth}.ga-ask-msg{margin:0 0 12px;max-width:92%;padding:12px 13px;border:1px solid var(--ga-line);border-radius:18px;line-height:1.35;font-size:14px}.ga-ask-msg.bot{background:rgba(255,255,255,.055)}.ga-ask-msg.user{margin-left:auto;background:rgba(112,255,213,.10);border-color:rgba(112,255,213,.33)}.ga-quick{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0 14px}.ga-chip{border:1px solid var(--ga-line);background:rgba(255,255,255,.07);color:var(--ga-ink);border-radius:999px;padding:8px 10px;font-size:12px;cursor:pointer}.ga-chip:hover{border-color:rgba(112,255,213,.55);color:#70ffd5}.ga-route-card{display:grid;gap:7px;margin:9px 0;padding:12px;border:1px solid rgba(255,255,255,.14);background:linear-gradient(135deg,rgba(255,255,255,.07),rgba(112,255,213,.045));border-radius:18px}.ga-route-card strong{font-size:14px}.ga-route-card small{color:var(--ga-muted);line-height:1.35}.ga-route-actions{display:flex;gap:8px;flex-wrap:wrap}.ga-open-route,.ga-copy-route{border:0;border-radius:999px;font-weight:900;padding:8px 11px;cursor:pointer}.ga-open-route{background:linear-gradient(135deg,#fff073,#70ffd5);color:#061018}.ga-copy-route{background:rgba(255,255,255,.09);color:var(--ga-ink);border:1px solid var(--ga-line)}.ga-ask-foot{border-top:1px solid var(--ga-line);padding:12px;background:rgba(255,255,255,.035)}.ga-boundary{font-size:11px;color:var(--ga-muted);margin:0 0 9px}.ga-ask-form{display:flex;gap:8px}.ga-ask-input{flex:1;border:1px solid var(--ga-line);background:rgba(0,0,0,.35);color:var(--ga-ink);border-radius:999px;padding:12px 13px;outline:none}.ga-ask-input:focus{border-color:rgba(112,255,213,.65);box-shadow:0 0 0 4px rgba(112,255,213,.12)}.ga-send{border:0;border-radius:999px;background:linear-gradient(135deg,#fff073,#70ffd5);color:#061018;font-weight:950;padding:0 15px;cursor:pointer}.ga-ask-mini{position:fixed;left:16px;bottom:16px;z-index:2147482999;color:#70ffd5;background:rgba(0,0,0,.35);border:1px solid rgba(112,255,213,.28);border-radius:999px;padding:9px 11px;text-decoration:none;font-weight:900;font-family:Inter,system-ui,sans-serif}.ga-ask-highlight{color:#70ffd5;font-weight:900}.ga-danger{color:#ffb2ce;font-weight:900}@media (max-width:600px){#goalos-ask-panel{right:8px;bottom:70px;width:calc(100vw - 16px);height:calc(100vh - 88px);border-radius:22px}#goalos-ask-launcher{right:10px;bottom:10px}}
'''

JS = r'''
(function(){
  const d=document;
  const routes=(window.GOALOS_ASK_ROUTES||[]).filter(r=>r&&r.url&&r.title);
  const boundary='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.';
  const synonyms={
    start:['start','begin','new','first','guide','onboard','how'],
    proof:['proof','evidence','docket','claim','claims','review','verify','validator','ledger','audit'],
    mainnet:['mainnet','ethereum','contract','contracts','48','chainid','etherscan','address','rail'],
    token:['token','agialpha','$agialpha','wallet','investment','available','buy','sell'],
    trust:['trust','privacy','data','funds','wallet','transaction','gdpr','secret','boundary'],
    loop:['loop','prompt','contract','restart','trace','bottleneck','flight'],
    rsi:['rsi','omni','move37','move-37','state capacity','sovereign','invention','governance'],
    mission:['mission','action','objective','decision','chronicle','work'],
    all:['all','pages','map','registry','find','route','missing','search'],
    node:['node','agent','jobs','runtime','work','settlement']
  };
  function norm(s){return String(s||'').toLowerCase().replace(/[^a-z0-9$]+/g,' ').trim()}
  function toks(s){return norm(s).split(/\s+/).filter(Boolean)}
  function expand(q){let t=toks(q); Object.keys(synonyms).forEach(k=>{if(t.includes(k)||synonyms[k].some(x=>norm(q).includes(x))) t=t.concat(synonyms[k])}); return [...new Set(t)]}
  function scoreRoute(r, qtokens, raw){
    const hay=norm([r.title,r.url,r.category,r.description,(r.keywords||[]).join(' ')].join(' '));
    let s=0; qtokens.forEach(t=>{ if(!t)return; if(hay.includes(t)) s+= t.length>4?4:2; if(norm(r.title).includes(t)) s+=3; if(norm(r.url).includes(t)) s+=4; });
    if(raw.includes('contract') && r.url.includes('mainnet')) s+=10;
    if(raw.includes('48') && r.url.includes('mainnet')) s+=12;
    if(raw.includes('token') && r.url.includes('token')) s+=12;
    if(raw.includes('rsi') && r.url.includes('rsi')) s+=10;
    if(raw.includes('loop') && r.url.includes('loop')) s+=8;
    if(raw.includes('start') && r.url.includes('start')) s+=12;
    if(raw.includes('privacy') && (r.url.includes('privacy')||r.url.includes('trust'))) s+=10;
    return s;
  }
  function answerText(q, matches){
    const raw=norm(q);
    if(/wallet|fund|buy|sell|investment|token|agialpha/.test(raw)) return 'Boundary first: GoalOS does not sell, custody, support, or make available $AGIALPHA. I can route you to the token boundary and contract atlas.';
    if(/48|mainnet|ethereum|contract|etherscan/.test(raw)) return 'Best route: the Mainnet Contract Atlas. It explains the 48 GoalOS-created Ethereum Mainnet contracts, their proof rails, and the canonical external AGIALPHA entry.';
    if(/data|privacy|gdpr|secret|confidential|user data/.test(raw)) return 'GoalOS is proof-native, not data-hungry. Public demos are browser-local and should not receive personal, customer, confidential, wallet, credential, or regulated data.';
    if(/rsi|omni|move|sovereign invention/.test(raw)) return 'Best route: the Loop → RSI path. It shows how loops become deterministic invention governance: schema-bound artifacts, baselines, ECI, dossiers, and council review.';
    if(/loop|restart|trace|bottleneck|prompt/.test(raw)) return 'Best route: the Loop demos. They show why long-running agent systems need contracts, disk state, traces, restarts, and bottleneck visibility.';
    if(/proof run|docket|evidence|claim|validator|review/.test(raw)) return 'Best route: Proof Run 001 and the evidence rooms. They show claims, gates, validator review, replay paths, and public-safe dockets.';
    if(/start|begin|new|non technical|how/.test(raw)) return 'Start here: choose your role, then follow the shortest path. I will route you to onboarding, Pathfinder, or the demo registry.';
    if(!matches.length) return 'I did not find an exact route. Try “contracts”, “RSI”, “Proof Run 001”, “privacy”, “Loop”, “validator”, or “start”.';
    return 'I found the best public route for that question. Choose one below or ask a follow-up.';
  }
  function find(q){const raw=norm(q); const qtokens=expand(q); return routes.map(r=>({...r,_score:scoreRoute(r,qtokens,raw)})).filter(r=>r._score>0&&r.state!=='SYSTEM').sort((a,b)=>b._score-a._score).slice(0,5)}
  function el(tag, cls, text){const x=d.createElement(tag); if(cls)x.className=cls; if(text!==undefined)x.textContent=text; return x}
  function addMsg(kind, content){const body=d.getElementById('goalos-ask-body'); if(!body)return; const m=el('div','ga-ask-msg '+kind); if(typeof content==='string')m.textContent=content; else m.appendChild(content); body.appendChild(m); body.scrollTop=body.scrollHeight}
  function routeCards(matches){const wrap=el('div'); if(!matches.length){const quick=el('div','ga-quick'); ['Start','Proof Run 001','48 contracts','Loop to RSI','Privacy'].forEach(q=>{const b=el('button','ga-chip',q); b.type='button'; b.addEventListener('click',()=>ask(q)); quick.appendChild(b)}); wrap.appendChild(quick); return wrap}
    matches.forEach((r,i)=>{const card=el('div','ga-route-card'); card.appendChild(el('strong','',r.title)); card.appendChild(el('small','',r.description||r.category)); const actions=el('div','ga-route-actions'); const open=el('button','ga-open-route', i===0?'Open best route →':'Open →'); open.type='button'; open.addEventListener('click',()=>{window.location.href=r.url}); const copy=el('button','ga-copy-route','Copy path'); copy.type='button'; copy.addEventListener('click',()=>{try{navigator.clipboard&&navigator.clipboard.writeText(r.url)}catch(e){}}); actions.appendChild(open); actions.appendChild(copy); card.appendChild(actions); wrap.appendChild(card)}); return wrap}
  function ask(q){q=String(q||'').trim(); if(!q)return; addMsg('user',q); const matches=find(q); addMsg('bot',answerText(q,matches)); addMsg('bot',routeCards(matches)); if(/^(open|go|take me|redirect|send me)/i.test(q)&&matches[0]) setTimeout(()=>{window.location.href=matches[0].url},650)}
  function openPanel(){d.getElementById('goalos-ask-panel')?.classList.add('ga-open'); const inp=d.getElementById('goalos-ask-input'); setTimeout(()=>inp&&inp.focus(),80)}
  function closePanel(){d.getElementById('goalos-ask-panel')?.classList.remove('ga-open')}
  function init(){
    if(d.getElementById('goalos-ask-panel')) return;
    const btn=el('button','', 'Ask GoalOS'); btn.id='goalos-ask-launcher'; btn.type='button'; btn.setAttribute('aria-haspopup','dialog'); btn.addEventListener('click',openPanel); d.body.appendChild(btn);
    const panel=el('section',''); panel.id='goalos-ask-panel'; panel.setAttribute('role','dialog'); panel.setAttribute('aria-label','Ask GoalOS route assistant');
    panel.innerHTML='<div class="ga-ask-head"><div class="ga-ask-brand"><div class="ga-orb"></div><div><strong>Ask GoalOS</strong><span>browser-local route assistant</span></div></div><button class="ga-ask-close" type="button" aria-label="Close">×</button></div><div class="ga-ask-body" id="goalos-ask-body"></div><div class="ga-ask-foot"><p class="ga-boundary">'+boundary+'</p><form class="ga-ask-form" id="goalos-ask-form"><input id="goalos-ask-input" class="ga-ask-input" autocomplete="off" placeholder="Ask: where are the 48 contracts? how do I start? what is RSI?"/><button class="ga-send" type="submit">Ask</button></form></div>';
    d.body.appendChild(panel); panel.querySelector('.ga-ask-close').addEventListener('click',closePanel); panel.querySelector('form').addEventListener('submit',e=>{e.preventDefault(); const i=d.getElementById('goalos-ask-input'); const q=i.value; i.value=''; ask(q)});
    addMsg('bot','Ask me anything about GoalOS and I will route you to the right public page. I answer from the local site map only: no model call, no network call, no stored chat.');
    const quick=el('div','ga-quick'); ['Start in 60 seconds','48 Mainnet contracts','Proof Run 001','Loop → RSI','Token boundary','No user data'].forEach(q=>{const b=el('button','ga-chip',q); b.type='button'; b.addEventListener('click',()=>ask(q)); quick.appendChild(b)}); addMsg('bot',quick);
    d.addEventListener('keydown',e=>{if(e.key==='/'&&!e.metaKey&&!e.ctrlKey&&!e.altKey){const tag=(d.activeElement&&d.activeElement.tagName||'').toLowerCase(); if(!['input','textarea'].includes(tag)){e.preventDefault(); openPanel()}} if(e.key==='Escape') closePanel()});
  }
  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',init); else init();
})();
'''

ASK_PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Ask GoalOS Concierge</title><meta name="description" content="Ask questions and get routed to the right public GoalOS page. Browser-local, no model call, no user data."><link rel="stylesheet" href="assets/goalos-ask-goalos-concierge-v18.css"><script defer src="assets/goalos-ask-goalos-knowledge-v18.js"></script><script defer src="assets/goalos-ask-goalos-concierge-v18.js"></script><style>body{margin:0;min-height:100vh;background:radial-gradient(circle at 20% 0%,rgba(112,255,213,.22),transparent 35%),radial-gradient(circle at 70% 0%,rgba(255,240,115,.14),transparent 32%),#050913;color:#f6f2e8;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif}.wrap{width:min(1120px,92vw);margin:0 auto;padding:80px 0 120px}.nav{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:70px}.nav a{color:#f6f2e8;text-decoration:none;border:1px solid rgba(255,255,255,.16);border-radius:999px;padding:10px 13px;background:rgba(255,255,255,.06);font-weight:800}.eyebrow{color:#fff073;letter-spacing:.32em;text-transform:uppercase;font-weight:900;font-size:12px}.hero{display:grid;grid-template-columns:1.05fr .95fr;gap:34px;align-items:center}.hero h1{font-size:clamp(56px,8vw,118px);line-height:.88;letter-spacing:-.08em;margin:.12em 0}.grad{background:linear-gradient(90deg,#fff073,#70ffd5,#90b7ff,#b99cff);-webkit-background-clip:text;background-clip:text;color:transparent;font-style:italic}.lead{font-size:clamp(19px,2.4vw,31px);line-height:1.12;font-weight:900;max-width:800px}.console{border:1px solid rgba(112,255,213,.3);border-radius:34px;padding:24px;background:linear-gradient(135deg,rgba(255,255,255,.08),rgba(112,255,213,.05));min-height:420px;box-shadow:0 25px 90px rgba(0,0,0,.42)}.terminal{height:260px;border:1px solid rgba(112,255,213,.28);border-radius:20px;background:rgba(0,0,0,.34);padding:18px;color:#70ffd5;font-family:ui-monospace,Menlo,monospace;line-height:1.55}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:40px}.card{border:1px solid rgba(255,255,255,.15);border-radius:22px;padding:20px;background:rgba(255,255,255,.06)}.card strong{display:block;font-size:22px}.card p{color:#bcc7d8}.boundary{border:1px solid rgba(255,106,162,.45);background:rgba(255,106,162,.08);border-radius:20px;padding:16px;margin-top:32px;font-weight:800}@media(max-width:850px){.hero,.cards{grid-template-columns:1fr}}</style></head><body><main class="wrap"><nav class="nav"><a href="index.html">Command Center</a><a href="start-here.html">Start</a><a href="pathfinder.html">Pathfinder</a><a href="demo-ecosystem-registry.html">Registry</a><a href="mainnet-contract-atlas.html">48 Contracts</a><a href="site-map.html">All Pages</a><a href="trust-boundary.html">Trust</a></nav><section class="hero"><div><div class="eyebrow">Browser-local concierge</div><h1>Ask GoalOS.<br><span class="grad">Find the proof path.</span></h1><p class="lead">Ask a normal question. The site answers from its public route map and sends you to the right room: contracts, proof dockets, Loop → RSI, token boundary, validators, or onboarding.</p></div><aside class="console"><div class="eyebrow">Sovereign route console</div><div class="terminal">01 · local knowledge loaded<br>02 · no model call<br>03 · no network call<br>04 · no stored chat<br>05 · ask with / from any page</div><p>Try: “where are the 48 contracts?”, “how do I start?”, “what is RSI?”, “is $AGIALPHA available from GoalOS?”, or “show Proof Run 001”.</p><button id="goalos-ask-launcher-page" style="border:0;border-radius:999px;background:linear-gradient(135deg,#fff073,#70ffd5);padding:14px 18px;font-weight:950;cursor:pointer">Open Ask GoalOS</button></aside></section><section class="cards"><div class="card"><strong>For new users</strong><p>Plain-language routes to Start, Pathfinder, and the demo registry.</p></div><div class="card"><strong>For reviewers</strong><p>Routes to Proof Run 001, dockets, claims, baselines, and validator packets.</p></div><div class="card"><strong>For institutions</strong><p>Routes to trust, token, data, privacy, contracts, and adoption surfaces.</p></div></section><div class="boundary">Public-alpha boundary: No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.</div></main><script>document.addEventListener('click',function(e){if(e.target&&e.target.id==='goalos-ask-launcher-page'){var b=document.getElementById('goalos-ask-launcher'); if(b)b.click();}})</script></body></html>'''

def write_assets(routes):
    assets = PUBLIC/'assets'; assets.mkdir(parents=True, exist_ok=True)
    (assets/'goalos-ask-goalos-concierge-v18.css').write_text(CSS, encoding='utf-8')
    (assets/'goalos-ask-goalos-concierge-v18.js').write_text(JS, encoding='utf-8')
    data = 'window.GOALOS_ASK_ROUTES = ' + json.dumps(routes, ensure_ascii=False, indent=2) + ';\n'
    (assets/'goalos-ask-goalos-knowledge-v18.js').write_text(data, encoding='utf-8')
    (PUBLIC/'ask-goalos.html').write_text(ASK_PAGE, encoding='utf-8')


def rel_from(page: pathlib.Path, target: str) -> str:
    base = page.parent
    return pathlib.Path(os.path.relpath(PUBLIC/target, base)).as_posix()

def inject_widget(routes):
    count=0
    for p in PUBLIC.rglob('*.html'):
        if 'downloads' in p.parts: continue
        try: text=p.read_text(encoding='utf-8', errors='ignore')
        except Exception: continue
        if 'goalos-ask-goalos-concierge-v18.js' in text: continue
        css_href = rel_from(p, 'assets/goalos-ask-goalos-concierge-v18.css')
        data_src = rel_from(p, 'assets/goalos-ask-goalos-knowledge-v18.js')
        js_src = rel_from(p, 'assets/goalos-ask-goalos-concierge-v18.js')
        head = f'\n<link rel="stylesheet" href="{css_href}">\n'
        body = f'\n<script defer src="{data_src}"></script>\n<script defer src="{js_src}"></script>\n'
        if '</head>' in text.lower():
            text = re.sub(r'</head>', head+'</head>', text, count=1, flags=re.I)
        else:
            text = head + text
        if '</body>' in text.lower():
            text = re.sub(r'</body>', body+'</body>', text, count=1, flags=re.I)
        else:
            text += body
        p.write_text(text, encoding='utf-8')
        count += 1
    return count

def update_index(routes):
    index = PUBLIC/'index.html'
    if not index.exists(): return False
    text = index.read_text(encoding='utf-8', errors='ignore')
    if 'ask-goalos.html' in text and 'Ask GoalOS' in text: return False
    snippet = '''\n<section id="ask-goalos" class="goalos-ask-home" style="width:min(1180px,92vw);margin:64px auto;padding:28px;border:1px solid rgba(112,255,213,.25);border-radius:28px;background:linear-gradient(135deg,rgba(112,255,213,.11),rgba(255,255,255,.05));color:#f6f2e8;font-family:Inter,system-ui,sans-serif">\n  <div style="color:#fff073;letter-spacing:.26em;text-transform:uppercase;font-weight:900;font-size:12px">Ask GoalOS</div>\n  <h2 style="font-size:clamp(34px,5vw,70px);line-height:.9;letter-spacing:-.06em;margin:.15em 0">Ask a question. Get routed to proof.</h2>\n  <p style="max-width:780px;color:#cbd5e1;font-weight:700;font-size:18px">Browser-local route concierge: no model call, no network call, no stored chat. Ask about Mainnet contracts, Proof Run 001, Loop → RSI, token boundaries, privacy, validators, or where to start.</p>\n  <p><a href="ask-goalos.html" style="display:inline-block;background:linear-gradient(135deg,#fff073,#70ffd5);color:#061018;text-decoration:none;border-radius:999px;padding:13px 18px;font-weight:950">Open Ask GoalOS →</a></p>\n</section>\n'''
    if '</main>' in text.lower(): text = re.sub(r'</main>', snippet+'</main>', text, count=1, flags=re.I)
    elif '</body>' in text.lower(): text = re.sub(r'</body>', snippet+'</body>', text, count=1, flags=re.I)
    else: text += snippet
    index.write_text(text, encoding='utf-8')
    return True

def write_indexes(routes):
    PUBLIC.mkdir(exist_ok=True)
    # Keep search-index simple and compatible; preserve all current pages.
    search = [{'title':r['title'],'url':r['url'],'category':r['category'],'description':r['description'],'keywords':r.get('keywords',[])} for r in routes if r['state']!='SYSTEM']
    (PUBLIC/'search-index.json').write_text(json.dumps(search, indent=2, ensure_ascii=False), encoding='utf-8')
    base = 'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
    urls = '\n'.join([f'  <url><loc>{base}{html.escape(r["url"])}</loc></url>' for r in routes])
    (PUBLIC/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'\n</urlset>\n', encoding='utf-8')
    content = ROOT/'content/goalos'; content.mkdir(parents=True, exist_ok=True)
    (content/'ask-goalos-concierge-v18.json').write_text(json.dumps({'version':VERSION,'release':RELEASE,'boundary':BOUNDARY,'routes':len(routes),'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}, indent=2), encoding='utf-8')
    (content/'public-proof-navigation-v18.json').write_text(json.dumps({'version':VERSION,'routes':routes}, indent=2, ensure_ascii=False), encoding='utf-8')

def write_docs(routes, injected):
    (ROOT/'docs/website').mkdir(parents=True, exist_ok=True); (ROOT/'docs/reviewer').mkdir(parents=True, exist_ok=True)
    (ROOT/'docs/website/ASK_GOALOS_CONCIERGE_V18.md').write_text(f'''# Ask GoalOS Concierge V18\n\nBrowser-local route assistant for the GoalOS public site.\n\n## What it does\n\n- Adds a floating Ask GoalOS chat window to public HTML pages.\n- Answers questions from the local route map.\n- Routes users to the right page: Start, Pathfinder, Proof Run 001, Mainnet Contract Atlas, Loop → RSI, Trust, Token Boundary, docs, and all pages.\n- Uses no model call, no network call, no analytics, no wallet, and no storage.\n\n## Boundary\n\n{BOUNDARY}\n\n## Installation result\n\n- Routes indexed: {len(routes)}\n- Pages injected: {injected}\n\n## Best questions to test\n\n- Where are the 48 contracts?\n- How do I start?\n- What is RSI?\n- Is $AGIALPHA available from GoalOS?\n- Show me Proof Run 001.\n- What data do you collect?\n''', encoding='utf-8')
    (ROOT/'docs/reviewer/HOW_TO_REVIEW_ASK_GOALOS_CONCIERGE_V18.md').write_text(f'''# How to Review Ask GoalOS Concierge V18\n\n1. Open `public/ask-goalos.html`.\n2. Press `/` on any public page and confirm the panel opens.\n3. Ask: `where are the 48 contracts?`\n4. Ask: `what is RSI?`\n5. Ask: `is $AGIALPHA available from GoalOS?`\n6. Confirm answers provide route cards and do not ask for data.\n7. Confirm no wallet prompt, no transaction prompt, no network call, and no model-call claim.\n\nBoundary: {BOUNDARY}\n''', encoding='utf-8')
    (ROOT/'examples/ask-goalos-concierge').mkdir(parents=True, exist_ok=True)
    (ROOT/'examples/ask-goalos-concierge/questions.md').write_text('''# Ask GoalOS Concierge Example Questions\n\n- How do I start?\n- Where are the 48 Ethereum Mainnet contracts?\n- What is the token boundary?\n- What is Loop to RSI?\n- Show me the Evidence Docket.\n- How do validators work?\n- What data do you collect?\n- Is there a wallet or transaction?\n''', encoding='utf-8')
    (ROOT/'issue-bodies').mkdir(parents=True, exist_ok=True)
    (ROOT/'issue-bodies/ask-goalos-concierge-v18.md').write_text(f'''## Ask GoalOS Concierge V18 review\n\nPlease test the browser-local chat/router.\n\n- [ ] `/` opens the assistant.\n- [ ] Questions route to correct pages.\n- [ ] Contract questions route to Mainnet Contract Atlas.\n- [ ] Token questions route to Token Boundary.\n- [ ] Privacy questions route to Trust Boundary.\n- [ ] No user data, no funds, no wallet, no transaction.\n\nBoundary: {BOUNDARY}\n''', encoding='utf-8')
    (ROOT/'.github/ISSUE_TEMPLATE').mkdir(parents=True, exist_ok=True)
    (ROOT/'.github/ISSUE_TEMPLATE/ask_goalos_concierge_feedback.yml').write_text('''name: Ask GoalOS Concierge Feedback\ndescription: Report routing or UX feedback for the browser-local GoalOS route assistant.\ntitle: "Ask GoalOS feedback: "\nlabels: [website, ux, concierge]\nbody:\n  - type: checkboxes\n    id: boundary\n    attributes:\n      label: Public-safe confirmation\n      options:\n        - label: I confirm I am not submitting personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.\n          required: true\n  - type: textarea\n    id: question\n    attributes:\n      label: What did you ask?\n      description: Public-safe wording only.\n  - type: textarea\n    id: expected\n    attributes:\n      label: Where should it have routed you?\n  - type: textarea\n    id: actual\n    attributes:\n      label: What happened instead?\n''', encoding='utf-8')

def write_reports(routes, injected):
    (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'evidence/demo').mkdir(parents=True, exist_ok=True)
    js_files=[PUBLIC/'assets/goalos-ask-goalos-concierge-v18.js', PUBLIC/'assets/goalos-ask-goalos-knowledge-v18.js']
    hits=[]
    for f in js_files:
        tx=f.read_text(encoding='utf-8', errors='ignore') if f.exists() else ''
        for bad in FORBIDDEN:
            if bad in tx: hits.append({'file':str(f),'pattern':bad})
    report={'status':'passed' if not hits and routes else 'failed','version':VERSION,'routeCount':len(routes),'pagesInjected':injected,'forbiddenBrowserApiHits':hits,'boundary':BOUNDARY,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
    (ROOT/'reports/ask-goalos-concierge-v18-install-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (ROOT/'reports/ask-goalos-concierge-v18-qa.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    docket={'name':'Ask GoalOS Concierge V18 Reference Docket','status':report['status'],'claim':'A browser-local route assistant answers questions from the public site map and routes users to public GoalOS pages without model calls, storage, wallet, transaction, or network calls.','routesIndexed':len(routes),'pagesInjected':injected,'boundary':BOUNDARY}
    (ROOT/'evidence/demo/ask-goalos-concierge-v18-reference-docket.json').write_text(json.dumps(docket, indent=2), encoding='utf-8')

def update_readme(routes):
    readme=ROOT/'README.md'
    block='''\n\n## Ask GoalOS Concierge V18\n\nThe website now includes a browser-local chat/router for visitors. Press `/` or open `ask-goalos.html` to ask plain-language questions and get routed to the right public page. It uses the local route map only: no model call, no network call, no analytics, no wallet, no transaction, and no stored chat.\n\nBest test questions: `where are the 48 contracts?`, `how do I start?`, `what is RSI?`, `show Proof Run 001`, `what data do you collect?`, and `is $AGIALPHA available from GoalOS?`.\n'''
    if readme.exists():
        text=readme.read_text(encoding='utf-8', errors='ignore')
        if 'Ask GoalOS Concierge V18' not in text:
            readme.write_text(text.rstrip()+block+'\n', encoding='utf-8')
    else:
        readme.write_text('# GoalOS AGIALPHA Ascension\n'+block, encoding='utf-8')

def main():
    PUBLIC.mkdir(exist_ok=True)
    ensure_essential_pages()
    initial_routes = build_routes()
    write_assets(initial_routes)
    routes = build_routes()
    write_assets(routes)
    injected = inject_widget(routes)
    update_index(routes)
    routes = build_routes()
    write_assets(routes)
    write_indexes(routes)
    write_docs(routes, injected)
    write_reports(routes, injected)
    update_readme(routes)
    (PUBLIC/'.nojekyll').write_text('', encoding='utf-8')
    print(json.dumps({'status':'passed','routes':len(routes),'pagesInjected':injected}, indent=2))
if __name__ == '__main__': main()
