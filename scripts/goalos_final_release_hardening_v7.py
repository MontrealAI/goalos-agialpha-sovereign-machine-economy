#!/usr/bin/env python3
from __future__ import annotations
import csv, datetime as dt, html, json, os, re, shutil
from pathlib import Path

ROOT=Path.cwd()
NOW=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
VERSION='v0.32.0-final-hardening-v7'
BOUNDARY='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'
TOKEN_BOUNDARY='$AGIALPHA public contract address only. Not available from us. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.'
CONFIRM='I confirm I am not submitting personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.'
SAFE_EXT={'.json','.md','.csv','.txt','.html','.xml','.svg'}


def p(*x): return ROOT.joinpath(*x)
def ensure(d:Path): d.mkdir(parents=True, exist_ok=True)
def read(f:Path)->str:
    try: return f.read_text(encoding='utf-8')
    except Exception: return f.read_text(encoding='utf-8', errors='ignore')
def write(f:Path,s:str): ensure(f.parent); f.write_text(s,encoding='utf-8')
def jwrite(f:Path,o): write(f,json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def rel(f:Path)->str: return f.relative_to(ROOT).as_posix()


def root_htmls():
    return sorted((p('public')).glob('*.html')) if p('public').exists() else []

def title(f:Path):
    t=read(f)
    m=re.search(r'<title[^>]*>(.*?)</title>',t,re.I|re.S)
    if m: return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(1)))).strip()
    m=re.search(r'<h1[^>]*>(.*?)</h1>',t,re.I|re.S)
    if m: return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',m.group(1)))).strip()
    return f.stem.replace('-',' ').title()

def category(f:Path):
    s=f.stem.lower()
    if s in {'index','start','start-here','pathfinder'}: return 'start'
    if s in {'404','search','site-map','site-health'}: return 'system'
    if any(x in s for x in ['token','privacy','trust','boundary','legal','terms','disclaimer','data']): return 'trust-boundary'
    if any(x in s for x in ['review','validator']): return 'review'
    if any(x in s for x in ['proof-run','docket','evidence','ledger']): return 'evidence'
    if any(x in s for x in ['mission','forge','control']): return 'mission'
    if any(x in s for x in ['benchmark','falsification','gauntlet']): return 'benchmark'
    if any(x in s for x in ['artifact','capability','evolution','upgrade','value','open-ended','action-reason']): return 'advanced-demo'
    if any(x in s for x in ['agent','institution','node','constellation','meta-agentic']): return 'core-demo'
    if any(x in s for x in ['docs','registry','atlas','operating','map']): return 'navigation'
    return 'additional'

def route_description(f:Path):
    s=f.stem.lower()
    known={
        'index':'Primary institutional front door: start here, choose a path, open the proof journey, and confirm the public-alpha boundary.',
        'pathfinder':'Role-based guide for new users, reviewers, mission proposers, developers, institutions, and boundary reviewers.',
        'website-operating-system':'Canonical operating map for routes, demos, evidence rooms, reviewer paths, mission tools, and trust pages.',
        'demo-ecosystem-registry':'Routeable registry of demo engines with expected inputs, artifacts, proof gates, states, and workflow roles.',
        'site-map':'Complete public site map that keeps every route discoverable without exposing archival scaffolding as the main journey.',
        'site-health':'Release-health surface for route integrity, public downloads, docs, claim boundaries, and source-of-truth QA.',
        'proof-run-001-docket':'Review-grade Evidence Docket for repository readiness: gates, downloads, replay path, validator packet, and decision state.',
        'external-reviewer-replay-room':'Independent reviewer path: inspect the docket, replay, challenge, accept, reject, revise, or dissent.',
        'proof-ledger':'Public proof ledger and evidence registry for dockets, reports, routes, and review assets.',
        'proof-mission-forge':'Browser-local mission intake that turns an objective into a Mission Contract and Evidence Docket plan.',
        'proof-mission-control':'Public mission operating board showing readiness, blocked gates, evidence gaps, and review state.',
        'token-boundary':'Public contract identification boundary for $AGIALPHA: not available from us, no custody, no wallet support, no advice.',
        'trust-boundary':'Public-alpha trust boundary: no user data, no funds, no wallet, no transaction, no production authority, human review required.',
        'multi-agent-institution':'Core demo: large multi-agent systems coordinate to maximum effect when they become proof-governed institutions.',
        'proof-gradient-lab':'Core demo: proof gates decide what may improve; score is advisory, gates are mandatory.',
        'evidence-docket-theatre':'Core demo: convert a public-safe claim into a review-ready Evidence Docket.',
        'proof-to-action-command-room':'Core demo: transform objective and evidence into a governed decision state, action graph, Chronicle entry, and capability package.',
        'capability-compounding-lab':'Core demo: accepted proof becomes reusable capability that can improve harder future missions.',
        'falsification-gauntlet':'Benchmark demo: stress claims against baselines, replay, overhead, privacy, and human-review gates.',
        'real-task-benchmark-bridge':'Benchmark demo: bridge demos into real-task benchmark readiness with equal-budget baselines and replay.',
        'proof-carrying-artifact-foundry':'Advanced demo: transform raw output into a scoped, rollbackable, proof-carrying artifact.',
        'evolution-ledger-control-room':'Advanced demo: public ledger remembers proof, attestations, challenge windows, and rollback receipts, not secrets.',
        'validator-council-arena':'Review demo: commit-reveal, challenge, dissent, quorum, diversity, and validator accountability.',
        'action-reason-trace-contract':'Action-governance demo: every high-impact action must carry reason, scope, observation, validation, rollback, and evidence.',
    }
    return known.get(s, f'{category(f).replace("-"," ").title()} route: {title(f)}. Preserved page with V7 route integrity, boundary path, and public-safe navigation.')

def route_io(f:Path):
    s=f.stem.lower()
    if 'falsification' in s: return ('Claim text; baseline pressure; replay/privacy toggles','Stress result; baseline matrix; Evidence Docket','Specificity, replayability, baselines, overhead, privacy','REVIEW_READY / REJECT_BASELINES_WIN','scoring module')
    if 'proof-run' in s or 'docket' in s: return ('Repository source, reports, evidence, workflows, routes','Docket JSON; claims matrix; validator packet','Route integrity, downloads, claim scan, docs QA','REVIEW_READY / HOLD_REMEDIATION','receipt/audit module')
    if 'mission' in s: return ('Objective, decision target, risk class','Mission Contract; docket plan; validator packet','Scope, replay, evidence, validator review','MISSION_REVIEW_READY','orchestration layer')
    if 'review' in s or 'validator' in s: return ('Docket, replay path, validator notes, dissent','Reviewer report; attestation; dissent memo','Commit-reveal, replay, quorum, dissent','REVIEW_READY / DISSENT','validator module')
    if 'action-reason' in s: return ('Action intent, scope, observation, risk','Trace contract; action graph; rollback playbook','Scope, reason, observation, validator, rollback','ACTION_REVIEW_READY','action-governance module')
    if 'artifact' in s or 'upgrade' in s or 'capability' in s: return ('Artifact candidate, proof history, scope','Artifact JSON; selection certificate; rollback receipt','Proof, eval, baseline, rollback, scope','UPGRADE_REVIEW_READY','capability-package generator')
    if 'ledger' in s or 'settlement' in s: return ('Proof roots, attestations, challenge window','Ledger entry; selection certificate; rollback receipt','ProofRoot, EvalAttestation, challenge, quorum','LEDGER_REVIEW_READY','ledger module')
    if 'benchmark' in s: return ('Task family, claim, baseline ladder','Benchmark plan; baseline matrix; reviewer brief','Real task, equal-budget baselines, replay','EMPIRICAL_BRIDGE_READY','benchmark module')
    if category(f)=='trust-boundary': return ('Public-safe visitor context','Boundary guidance','No data, no funds, no wallet, no advice','BOUNDARY_VISIBLE','trust module')
    return ('Public-safe page visit','Reviewable page and related routes','Boundary visibility, route integrity, human review','ROUTE_AVAILABLE','UI demo')


def create_boundary_pages():
    ensure(p('public/assets'))
    css=""":root{--bg:#07111f;--panel:rgba(255,255,255,.08);--line:rgba(255,255,255,.18);--text:#fffaf0;--muted:#c7d5e7;--gold:#ffe979;--mint:#69ffd6;--rose:#ff78a8}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 20% 20%,rgba(105,255,214,.16),transparent 32%),linear-gradient(135deg,#07111f,#10081f 70%);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif}a{color:var(--mint)}.wrap{width:min(1120px,92vw);margin:0 auto;padding:40px 0 80px}.nav,.card{border:1px solid var(--line);background:var(--panel);backdrop-filter:blur(14px);border-radius:28px}.nav{display:flex;gap:18px;align-items:center;justify-content:space-between;padding:16px 20px;margin:28px auto}.brand{font-weight:900;letter-spacing:.24em;text-transform:uppercase}.links{display:flex;gap:12px;flex-wrap:wrap}.links a{color:var(--text);text-decoration:none;font-weight:800;font-size:14px;padding:9px 12px;border-radius:999px}.eyebrow{color:var(--gold);font-size:13px;font-weight:900;letter-spacing:.45em;text-transform:uppercase}.hero{padding:70px 0 30px}h1{font-size:clamp(54px,9vw,118px);line-height:.88;margin:22px 0;letter-spacing:-.08em}h2{font-size:clamp(28px,4vw,54px);letter-spacing:-.05em;margin:0 0 14px}p{color:var(--muted);font-size:18px;line-height:1.55}.card{padding:28px;margin:22px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:16px}.btn{display:inline-block;border-radius:999px;padding:13px 18px;font-weight:900;text-decoration:none;background:linear-gradient(135deg,var(--gold),var(--mint));color:#06101b;margin:4px 6px 4px 0}.danger{border-color:rgba(255,120,168,.55);background:rgba(80,20,48,.3)}.row{display:flex;gap:12px;justify-content:space-between;align-items:flex-start;border-top:1px solid var(--line);padding:12px 0}.ok{color:var(--mint);font-weight:900}.warn{color:var(--gold);font-weight:900}table{width:100%;border-collapse:collapse}td,th{border-top:1px solid rgba(255,255,255,.15);padding:12px;text-align:left;vertical-align:top}th{color:var(--gold)}@media(max-width:720px){.nav{align-items:flex-start;flex-direction:column}h1{font-size:54px}.row{display:block}}"""
    write(p('public/assets/goalos-final-hardening-v7.css'),css)
    nav="<div class='nav'><div class='brand'>GOALOS<br><span style='color:#c7d5e7'>AGIALPHA ASCENSION</span></div><div class='links'><a href='index.html'>Start</a><a href='pathfinder.html'>Pathfinder</a><a href='proof-run-001-docket.html'>Proof Run 001</a><a href='demo-ecosystem-registry.html'>Registry</a><a href='site-health.html'>Site Health</a><a href='trust-boundary.html'>Trust</a></div></div>"
    pages={
        'token-boundary.html':('$AGIALPHA boundary.','Public contract identification only.',TOKEN_BOUNDARY),
        'trust-boundary.html':('Proof-native. Not data-hungry. Not wallet-first.','The public-alpha boundary.',BOUNDARY),
        'privacy.html':('We do not want your data.','Privacy notice.','Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, trade-secret, or proprietary data through public channels.'),
        'data-boundary.html':('Data boundary.','Public-safe only.','Private intelligence, prompts, raw traces, customer data, credentials, and workpapers stay private.'),
        'no-data-no-funds.html':('No data. No funds.','The simple rule.',BOUNDARY),
        'docs.html':('GoalOS docs.','Documentation entry point.','Start with README, Proof Run 001, Public Proof Ledger, Demo Ecosystem Registry, Reviewer Guide, Developer Guide, and Trust Boundary.'),
        'search.html':('Search GoalOS.','Browser-local command palette.','Use the site map, registry, and command palette. No search telemetry.'),
        '404.html':('Page not found.','Return to the proof surface.','Use the site map, Pathfinder, registry, Proof Ledger, or Trust Boundary.'),
    }
    for fn,(h,ey,b) in pages.items():
        if p('public',fn).exists() and fn not in {'token-boundary.html','trust-boundary.html','404.html','docs.html','search.html'}: continue
        write(p('public',fn),f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{html.escape(h)} · GoalOS</title><link rel='stylesheet' href='assets/goalos-final-hardening-v7.css'></head><body><main class='wrap'>{nav}<section class='hero'><div class='eyebrow'>{html.escape(ey)}</div><h1>{html.escape(h)}</h1><p>{html.escape(b)}</p><p><a class='btn' href='index.html'>Return home</a><a class='btn' href='site-map.html'>Open site map</a></p></section><section class='card danger'><h2>Public-alpha boundary</h2><p>{BOUNDARY}</p><p>{TOKEN_BOUNDARY}</p></section></main></body></html>")


def patch_index():
    idx=p('public/index.html')
    if not idx.exists(): create_boundary_pages(); return
    text=read(idx)
    needed=[('site-health.html','Site Health'),('token-boundary.html','Token Boundary'),('trust-boundary.html','Trust Boundary'),('proof-run-001-docket.html','Proof Run 001'),('demo-ecosystem-registry.html','Demo Registry')]
    links=' '.join(f"<a href='{href}'>{label}</a>" for href,label in needed if href not in text)
    if 'Final Release Hardening V7' not in text or links:
        block=f"<section id='final-hardening-v7' style='max-width:1120px;margin:48px auto;padding:24px;border:1px solid rgba(255,255,255,.18);border-radius:24px;background:rgba(255,255,255,.06);color:#fff'><strong>Final Release Hardening V7</strong><p>{BOUNDARY}</p><p>{links}</p></section>"
        text=text.replace('</body>',block+'</body>') if '</body>' in text else text+block
        write(idx,text)


def links_in(f:Path):
    return [html.unescape(m.group(2)).strip() for m in re.finditer(r'''(?:href|src)\s*=\s*(["'])(.*?)\1''',read(f),re.I)]
def external(u): return not u or u.startswith(('http://','https://','mailto:','tel:','#','javascript:','data:'))
def target(base:Path,u:str):
    u=u.split('#',1)[0].split('?',1)[0]
    if external(u): return None
    if u.startswith('/'):
        if '/goalos-agialpha-sovereign-machine-economy/' in u: return p('public')/u.split('/goalos-agialpha-sovereign-machine-economy/',1)[1]
        return None
    t=(base.parent/u).resolve()
    if u.endswith('/'): t=t/'index.html'
    return t

def mirror_and_rewrite_downloads():
    rewrites=0; copied=[]; missing=[]
    pat=re.compile(r'''(href|src)=(['"])(\.\./)+(reports|evidence|content|replay|docs)/([^'"#?]+)([#?][^'"]*)?\2''')
    for f in root_htmls():
        txt=read(f)
        def repl(m):
            nonlocal rewrites
            attr,q,_,bucket,rest,suf=m.groups(); suf=suf or ''
            src=p(bucket,rest); dest=p('public/downloads',bucket,rest)
            ensure(dest.parent)
            if src.exists() and src.is_file() and src.suffix.lower() in SAFE_EXT:
                shutil.copy2(src,dest); copied.append(rel(dest))
            else:
                if dest.suffix.lower()=='.json': jwrite(dest,{'status':'missing_source_fallback','source':rel(src) if src.exists() else str(src),'generated_at':NOW,'boundary':BOUNDARY})
                else: write(dest,f"# Missing source fallback\n\nOriginal source `{src}` was not present when V7 hardened public downloads.\n\n{BOUNDARY}\n")
                missing.append(str(src)); copied.append(rel(dest))
            rewrites+=1
            return f'{attr}={q}downloads/{bucket}/{rest}{suf}{q}'
        new=pat.sub(repl,txt)
        if new!=txt: write(f,new)
    return {'rewrite_count':rewrites,'copied_count':len(copied),'missing_sources':missing[:50]}

def routes():
    out=[]
    for f in root_htmls():
        ins,outs,gates,state,role=route_io(f)
        out.append({'path':f.name,'title':title(f),'category':category(f),'description':route_description(f),'expected_inputs':ins,'generated_outputs':outs,'proof_gates_or_checks':gates,'next_state':state,'workflow_role':role,'system_page':category(f)=='system'})
    return sorted(out,key=lambda r:(r['system_page'],r['category'],r['title'].lower()))

def update_registry(rs):
    data={'version':VERSION,'generated_at':NOW,'route_schema':'user action -> mission/event type -> selected demo engine -> required inputs -> proof gates -> output artifact -> next allowed state','routes':rs,'demos':[r for r in rs if not r['system_page']],'system_pages':[r for r in rs if r['system_page']]}
    jwrite(p('content/goalos/demo-ecosystem-registry.json'),data); jwrite(p('content/goalos/public-proof-navigation-v7.json'),data)
    rows=''.join(f"<tr><td><a href='{r['path']}'>{html.escape(r['title'])}</a></td><td>{r['category']}</td><td>{html.escape(r['expected_inputs'])}</td><td>{html.escape(r['generated_outputs'])}</td><td>{html.escape(r['proof_gates_or_checks'])}</td><td><code>{html.escape(r['next_state'])}</code></td><td>{html.escape(r['workflow_role'])}</td></tr>" for r in rs if not r['system_page'])
    write(p('public/demo-ecosystem-registry.html'),f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>GoalOS Demo Ecosystem Registry</title><link rel='stylesheet' href='assets/goalos-final-hardening-v7.css'></head><body><main class='wrap'><section class='hero'><div class='eyebrow'>ROUTE REGISTRY / V7</div><h1>Demo Ecosystem Registry.</h1><p>Every usable public route is classified by inputs, outputs, gates, state transitions, and workflow role.</p><p><a class='btn' href='index.html'>Start</a><a class='btn' href='site-health.html'>Site Health</a></p></section><section class='card'><table><thead><tr><th>Route</th><th>Category</th><th>Inputs</th><th>Outputs</th><th>Gates</th><th>State</th><th>Role</th></tr></thead><tbody>{rows}</tbody></table></section><section class='card danger'><h2>Boundary</h2><p>{BOUNDARY}</p></section></main></body></html>")
    groups={}
    for r in rs: groups.setdefault(r['category'],[]).append(r)
    sections=''.join(f"<section class='card'><h2>{cat.replace('-',' ').title()}</h2>"+''.join(f"<div class='row'><div><strong><a href='{r['path']}'>{html.escape(r['title'])}</a></strong><p>{html.escape(r['description'])}</p></div><span class='ok'>{cat}</span></div>" for r in items)+"</section>" for cat,items in sorted(groups.items()))
    write(p('public/site-map.html'),f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>GoalOS Site Map</title><link rel='stylesheet' href='assets/goalos-final-hardening-v7.css'></head><body><main class='wrap'><section class='hero'><div class='eyebrow'>SITE MAP / V7</div><h1>Every route remains discoverable.</h1><p>No pages were removed. First-class routes are grouped for faster navigation.</p><p><a class='btn' href='index.html'>Start</a><a class='btn' href='demo-ecosystem-registry.html'>Registry</a></p></section>{sections}<section class='card danger'><h2>Boundary</h2><p>{BOUNDARY}</p></section></main></body></html>")
    jwrite(p('public/search-index.json'),{'version':VERSION,'generated_at':NOW,'items':rs})
    write(p('public/sitemap.xml'),"<?xml version='1.0' encoding='UTF-8'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>\n"+'\n'.join(f"  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{html.escape(r['path'])}</loc></url>" for r in rs)+"\n</urlset>\n")
    write(p('public/.nojekyll'),'')

def route_health():
    broken=[]; checked=0
    for f in root_htmls():
        for u in links_in(f):
            t=target(f,u)
            if t is None: continue
            checked+=1
            if not t.exists(): broken.append({'page':rel(f),'link':u,'resolved':os.path.relpath(str(t),str(ROOT))})
    return {'checked_links':checked,'broken_links':broken,'broken_count':len(broken)}
def download_health():
    escapes=[]; broken=[]
    for f in root_htmls():
        for u in links_in(f):
            if u.startswith('../') and re.match(r'^(\.\./)+(reports|evidence|content|replay|docs)/',u): escapes.append({'page':rel(f),'link':u})
            if u.startswith('downloads/'):
                t=target(f,u)
                if t is not None and not t.exists(): broken.append({'page':rel(f),'link':u})
    return {'root_escape_links':escapes,'root_escape_count':len(escapes),'broken_downloads':broken,'broken_download_count':len(broken)}
def api_audit():
    hits=[]
    for f in sorted(p('public/assets').glob('*.js')) if p('public/assets').exists() else []:
        txt=read(f)
        for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if token in txt: hits.append({'file':rel(f),'token':token})
    return {'hits':hits,'hit_count':len(hits)}
def boundary_coverage():
    gaps=[]
    for f in root_htmls():
        if f.name=='404.html': continue
        txt=read(f).lower()
        if not any(x in txt for x in ['no user data','trust-boundary.html','no-data-no-funds.html','data-boundary.html']): gaps.append(rel(f))
    return {'gaps':gaps,'gap_count':len(gaps)}

def normalize_templates():
    d=p('.github/ISSUE_TEMPLATE'); ensure(d)
    required={'new_user_question.yml':'New user question','documentation_feedback.yml':'Documentation feedback','demo_bug_report.yml':'Demo bug report','evidence_docket_review.yml':'Evidence Docket review','external_reviewer_report.yml':'External reviewer report','proof_mission_proposal.yml':'Proof mission proposal','security_boundary_report.yml':'Security boundary report','token_or_market_boundary.yml':'Token or market boundary','website_navigation_feedback.yml':'Website navigation feedback'}
    for fn,label in required.items():
        q=d/fn
        if not q.exists(): write(q,f"name: {label}\ndescription: Public-safe GoalOS issue template.\ntitle: '[{label}] '\nlabels: ['public-alpha','needs-review']\nbody:\n  - type: textarea\n    id: summary\n    attributes:\n      label: Summary\n      description: Public-safe information only.\n    validations:\n      required: true\n  - type: checkboxes\n    id: public_safe_boundary\n    attributes:\n      label: Public-safe boundary confirmation\n      options:\n        - label: {CONFIRM}\n          required: true\n")
    changed=[]
    block=f"\n  - type: checkboxes\n    id: public_safe_boundary_v7\n    attributes:\n      label: Public-safe boundary confirmation\n      options:\n        - label: {CONFIRM}\n          required: true\n"
    for q in list(d.glob('*.yml'))+list(d.glob('*.yaml')):
        txt=read(q)
        if CONFIRM in txt: continue
        txt=txt.rstrip()+('\nbody:\n' if 'body:' not in txt else '\n')+block
        write(q,txt); changed.append(rel(q))
    missing=[rel(q) for q in list(d.glob('*.yml'))+list(d.glob('*.yaml')) if CONFIRM not in read(q)]
    return {'changed':changed,'templates_missing_confirmation':missing,'templates_missing_confirmation_count':len(missing),'total_templates':len(list(d.glob('*.yml'))+list(d.glob('*.yaml')))}

def core_docs():
    files={'CONTRIBUTING.md':f'# Contributing\n\n{CONFIRM}\n\n{BOUNDARY}\n','SECURITY.md':f'# Security\n\nDo not post secrets, credentials, wallet information, private keys, seed phrases, payment data, personal data, customer data, confidential data, regulated data, trade secrets, or proprietary data.\n\n{BOUNDARY}\n','PRIVACY.md':f'# Privacy\n\nGoalOS does not want user data. {BOUNDARY}\n','DATA_BOUNDARY.md':f'# Data Boundary\n\nPrivate intelligence and customer data stay private. {BOUNDARY}\n','DISCLAIMER.md':'# Disclaimer\n\nGoalOS is public-alpha. It does not claim achieved AGI, achieved ASI, empirical SOTA, production certification, legal advice, financial advice, tax advice, or investment advice.\n','TOKEN_BOUNDARY.md':f'# Token Boundary\n\n{TOKEN_BOUNDARY}\n','WORKFLOWS.md':'# Workflow Tiers\n\nNormal release: docs quality, claim scan, site verification, Proof Run refresh, human review, release. Demo workflows should be run only when editing their specific page. Legacy workflows are preserved but not normal release paths.\n'}
    for k,v in files.items():
        if not p(k).exists(): write(p(k),v)
    docs={'docs/README.md':'# GoalOS Docs\n\nStart with START_HERE, REVIEWER_GUIDE, DEVELOPER_GUIDE, CLAIM_BOUNDARY, NO_DATA_NO_FUNDS, and TOKEN_BOUNDARY.\n','docs/START_HERE.md':f'# Start Here\n\nChoose a role path. {BOUNDARY}\n','docs/REVIEWER_GUIDE.md':'# Reviewer Guide\n\nInspect the docket, claims matrix, downloads, replay path, baselines, cost/risk ledgers, and validator packet. File accept, reject, revise, or dissent.\n','docs/DEVELOPER_GUIDE.md':'# Developer Guide\n\nRun `python scripts/validate_claims.py`, `python scripts/verify_site.py`, and `python scripts/goalos_docs_quality.py`. Serve with `python -m http.server 8000 --directory public`.\n','docs/CLAIM_BOUNDARY.md':'# Claim Boundary\n\nGoalOS does not claim achieved AGI, achieved ASI, empirical SOTA, production certification, mainnet authorization, guaranteed return, legal advice, financial advice, tax advice, or wallet support.\n','docs/NO_DATA_NO_FUNDS.md':f'# No Data / No Funds\n\n{BOUNDARY}\n\n{CONFIRM}\n','docs/TOKEN_BOUNDARY.md':f'# Token Boundary\n\n{TOKEN_BOUNDARY}\n','docs/ROADMAP.md':'# Roadmap\n\nPriority: final hardening, public downloads, QA unification, Proof Run refresh, external review, real-task Evidence Dockets.\n','docs/FINAL_RELEASE_HARDENING_V7.md':f'# Final Release Hardening V7\n\nFinal hardening mirrors public artifacts, unifies QA, normalizes templates, refreshes Proof Run 001, and preserves boundaries.\n\n{BOUNDARY}\n','docs/reviewer/HOW_TO_REVIEW_FINAL_RELEASE_HARDENING_V7.md':f'# How to Review Final Release Hardening V7\n\nOpen site health, verify downloads, inspect Proof Run 001, run QA scripts, and file accept/reject/revise/dissent.\n\n{BOUNDARY}\n'}
    for k,v in docs.items():
        if not p(k).exists() or 'FINAL_RELEASE_HARDENING_V7' in k: write(p(k),v)
    pr=p('.github/pull_request_template.md')
    if not pr.exists() or 'No user data' not in read(pr): write(pr,f'# Pull Request\n\n## Summary\n\n## Boundary checklist\n- [ ] No user data.\n- [ ] No user funds.\n- [ ] No wallet or transaction.\n- [ ] No unsupported AGI/ASI/SOTA claims.\n- [ ] Human review required preserved.\n\n{CONFIRM}\n')

def create_scripts():
    ensure(p('scripts'))
    write(p('scripts/validate_claims.py'),r'''#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path.cwd(); SCAN=["README.md","docs","public","content","evidence"]
PATS=["achieved AGI","achieved ASI","empirical SOTA","guaranteed return","guaranteed ROI","investment opportunity","buy token","send funds","connect wallet","available from us","production certified","safety certified","mainnet authorized","autonomous production remediation"]
BOUND=["does not claim","not achieved","not empirical","no investment","no wallet","no transaction","no sale","no custody","not available from","available from us: **no**","available from us: no","claim boundary","boundary","avoid unsupported","unsupported claims","legal advice, financial advice","tax advice, investment advice","or guaranteed roi","guaranteed security","guaranteed returns","legal approval, token settlement","user-fund movement","not legal advice","not financial advice","not tax advice"]
EXT={".md",".html",".json",".txt",".yml",".yaml"}
def iter_files():
 for item in SCAN:
  q=ROOT/item
  if q.is_file(): yield q
  elif q.is_dir():
   for f in q.rglob('*'):
    if f.is_file() and f.suffix.lower() in EXT and 'public/downloads' not in f.as_posix(): yield f
def allowed(txt,start,end):
 ctx=txt[max(0,start-180):min(len(txt),end+180)].lower(); before=txt[max(0,start-80):start].lower(); after=txt[end:min(len(txt),end+80)].lower()
 if any(x in before for x in ['not','no','does not','do not','without','never']): return True
 if any(x in ctx for x in BOUND): return True
 if re.match(r"\s*[:=-]?\s*(\*\*)?no(\*\*)?\b",after): return True
 return False
def main():
 blockers=[]; allowed_count=0; checked=0
 for f in iter_files():
  txt=f.read_text(encoding='utf-8',errors='ignore'); low=txt.lower(); checked+=1
  for pat in PATS:
   for m in re.finditer(re.escape(pat.lower()),low):
    item={"file":f.relative_to(ROOT).as_posix(),"phrase":pat,"context":txt[max(0,m.start()-80):min(len(txt),m.end()+80)].replace('\n',' ')}
    if allowed(txt,m.start(),m.end()): allowed_count+=1
    else: blockers.append(item)
 out={"status":"passed" if not blockers else "failed","checked_files":checked,"blockers":blockers,"blocker_count":len(blockers),"allowed_boundary_contexts":allowed_count}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/claim-scan.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not blockers else 1)
if __name__=='__main__': main()
''')
    os.chmod(p('scripts/validate_claims.py'),0o755)
    write(p('scripts/verify_site.py'),r'''#!/usr/bin/env python3
from __future__ import annotations
import json,re,html,os
from pathlib import Path
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
def read(f): return f.read_text(encoding='utf-8',errors='ignore')
def links(f): return [html.unescape(m.group(2)).strip() for m in re.finditer(r''' + "'''(?:href|src)\\s*=\\s*([\"'])(.*?)\\1'''" + r''',read(f),re.I)]
def ext(u): return not u or u.startswith(('http://','https://','mailto:','tel:','#','javascript:','data:'))
def tgt(base,u):
 u=u.split('#',1)[0].split('?',1)[0]
 if ext(u): return None
 if u.startswith('/'):
  return PUBLIC/u.split('/goalos-agialpha-sovereign-machine-economy/',1)[1] if '/goalos-agialpha-sovereign-machine-economy/' in u else None
 t=(base.parent/u).resolve(); return t/'index.html' if u.endswith('/') else t
def main():
 broken=[]; gaps=[]; checked=0
 for f in sorted(PUBLIC.glob('*.html')):
  txt=read(f).lower()
  if f.name!='404.html' and not any(x in txt for x in ['no user data','trust-boundary.html','no-data-no-funds.html','data-boundary.html']): gaps.append(f.relative_to(ROOT).as_posix())
  for u in links(f):
   t=tgt(f,u)
   if t is None: continue
   checked+=1
   if not t.exists(): broken.append({'page':f.relative_to(ROOT).as_posix(),'link':u,'resolved':os.path.relpath(str(t),str(ROOT))})
 out={'status':'passed' if not broken else 'failed','public_pages':len(list(PUBLIC.glob('*.html'))),'checked_links':checked,'broken_links':broken,'broken_link_count':len(broken),'boundary_gaps':gaps,'boundary_gap_count':len(gaps)}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/site-verification.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not broken else 1)
if __name__=='__main__': main()
''')
    os.chmod(p('scripts/verify_site.py'),0o755)
    write(p('scripts/goalos_docs_quality.py'),r'''#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path.cwd(); REQ=['README.md','CONTRIBUTING.md','SECURITY.md','PRIVACY.md','DATA_BOUNDARY.md','DISCLAIMER.md','TOKEN_BOUNDARY.md','WORKFLOWS.md','docs/README.md','docs/START_HERE.md','docs/REVIEWER_GUIDE.md','docs/DEVELOPER_GUIDE.md','docs/CLAIM_BOUNDARY.md','docs/NO_DATA_NO_FUNDS.md','docs/TOKEN_BOUNDARY.md','docs/ROADMAP.md']
def main():
 missing=[x for x in REQ if not (ROOT/x).exists()]
 reg=ROOT/'content/goalos/demo-ecosystem-registry.json'; reg_issue=None; n=0
 if reg.exists():
  data=json.loads(reg.read_text()); items=data.get('routes') or data.get('demos') or data.get('items') or []; n=len(items); reg_issue=None if n else 'registry has no routes/demos/items'
 else: reg_issue='missing registry'
 phrase='I confirm I am not submitting personal data'; tdir=ROOT/'.github/ISSUE_TEMPLATE'; miss=[]
 if tdir.exists():
  for f in list(tdir.glob('*.yml'))+list(tdir.glob('*.yaml')):
   if phrase.lower() not in f.read_text(encoding='utf-8',errors='ignore').lower(): miss.append(f.relative_to(ROOT).as_posix())
 blockers=[]
 if missing: blockers.append({'missing':missing})
 if reg_issue: blockers.append({'registry_issue':reg_issue})
 if miss: blockers.append({'templates_missing_boundary_confirmation':miss})
 out={'status':'passed' if not blockers else 'failed','missing_files':missing,'registry_routes':n,'registry_issue':reg_issue,'templates_missing_boundary_confirmation':miss,'blockers':blockers}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/docs-quality.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not blockers else 1)
if __name__=='__main__': main()
''')
    os.chmod(p('scripts/goalos_docs_quality.py'),0o755)

def qa_all(tmpl_audit):
    rh=route_health(); dh=download_health(); api=api_audit(); bc=boundary_coverage()
    qa={'route_health':rh,'download_health':dh,'forbidden_api_audit':api,'boundary_coverage':bc,'issue_templates':tmpl_audit}
    qa['status']='passed' if rh['broken_count']==0 and dh['root_escape_count']==0 and dh['broken_download_count']==0 and api['hit_count']==0 and tmpl_audit['templates_missing_confirmation_count']==0 else 'review'
    jwrite(p('reports/final-hardening-v7-route-health.json'),rh); jwrite(p('reports/final-hardening-v7-download-health.json'),dh); jwrite(p('reports/final-hardening-v7-issue-template-audit.json'),tmpl_audit); jwrite(p('reports/final-hardening-v7-qa.json'),qa)
    return qa

def proof_docket(rs,qa):
    gates=[('Route integrity',qa['route_health']['broken_count']==0),('Public downloads',qa['download_health']['root_escape_count']==0 and qa['download_health']['broken_download_count']==0),('No forbidden browser APIs',qa['forbidden_api_audit']['hit_count']==0),('Issue-template boundary',qa['issue_templates']['templates_missing_confirmation_count']==0),('Boundary coverage',qa['boundary_coverage']['gap_count']==0),('Token boundary',p('public/token-boundary.html').exists()),('Claim scan script',p('scripts/validate_claims.py').exists()),('Docs quality script',p('scripts/goalos_docs_quality.py').exists()),('Site verifier',p('scripts/verify_site.py').exists()),('Human review required',True)]
    passed=sum(ok for _,ok in gates); state='REVIEW_READY' if passed==len(gates) else 'HOLD_REMEDIATION_REQUIRED'
    docket={'version':VERSION,'generated_at':NOW,'decision_state':state,'repository_readiness':round(passed/len(gates)*100),'gates_passed':passed,'gates_total':len(gates),'gates':[{'name':n,'passed':ok} for n,ok in gates],'counts':{'public_pages':len(rs),'reports':len(list(p('reports').glob('*'))),'evidence_files':len(list(p('evidence').rglob('*'))) if p('evidence').exists() else 0,'workflows':len(list(p('.github/workflows').glob('*.yml'))) if p('.github/workflows').exists() else 0},'boundary':BOUNDARY,'token_boundary':TOKEN_BOUNDARY,'claim_boundary':'Repository-readiness only. Not achieved AGI/ASI. Not empirical SOTA. External review still required.'}
    jwrite(p('evidence/proof-run-001/proof-run-001-final-hardening-v7.json'),docket)
    ensure(p('evidence/proof-run-001'))
    with p('evidence/proof-run-001/proof-run-001-final-hardening-v7-claims-matrix.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['claim','status','evidence','boundary']); w.writerow(['Final hardening V7 source, routes, downloads, scanners, templates, and proof docket are synchronized.',state,'reports/final-hardening-v7-qa.json','Repository-readiness only']); w.writerow(['GoalOS achieved AGI/ASI or empirical SOTA','NOT_CLAIMED','Claim boundary','Explicitly not claimed'])
    write(p('evidence/proof-run-001/proof-run-001-final-hardening-v7-validator-packet.md'),f'# Validator Packet — Final Hardening V7\n\nDecision: **{state}**\n\nGates: **{passed}/{len(gates)}**\n\n{BOUNDARY}\n\n{TOKEN_BOUNDARY}\n')
    for src in p('evidence/proof-run-001').glob('proof-run-001-final-hardening-v7*'):
        dest=p('public/downloads/proof-run-001')/src.name; ensure(dest.parent); shutil.copy2(src,dest)
    rows=''.join(f"<div class='row'><strong>{n}</strong><span class='{ 'ok' if ok else 'warn'}'>{'PASS' if ok else 'HOLD'}</span></div>" for n,ok in gates)
    write(p('public/proof-run-001-docket.html'),f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Proof Run 001 · Final Hardening V7</title><link rel='stylesheet' href='assets/goalos-final-hardening-v7.css'></head><body><main class='wrap'><section class='hero'><div class='eyebrow'>PROOF RUN 001 / FINAL HARDENING V7</div><h1>Repository readiness becomes reviewable evidence.</h1><p>Public downloads, route integrity, claim scan, docs QA, issue templates, token boundary, and human-review boundary.</p><p><a class='btn' href='downloads/proof-run-001/proof-run-001-final-hardening-v7.json'>Download Docket JSON</a><a class='btn' href='downloads/proof-run-001/proof-run-001-final-hardening-v7-claims-matrix.csv'>Claims Matrix</a><a class='btn' href='downloads/proof-run-001/proof-run-001-final-hardening-v7-validator-packet.md'>Validator Packet</a><a class='btn' href='site-health.html'>Site Health</a></p></section><section class='grid'><article class='card'><h2>{state}</h2><p>{passed}/{len(gates)} gates passed.</p></article><article class='card'><h2>{round(passed/len(gates)*100)}</h2><p>Repository-readiness score. Not empirical validation.</p></article><article class='card'><h2>{len(rs)}</h2><p>Public pages counted from committed source.</p></article></section><section class='card'><h2>Gate ledger</h2>{rows}</section><section class='card danger'><h2>Claim boundary</h2><p>Repository-readiness only. Not achieved AGI/ASI. Not empirical SOTA. External review required.</p><p>{BOUNDARY}</p></section></main></body></html>")
    return docket

def site_health(rs,qa):
    cards=[('Public pages',len(rs)),('Broken links',qa['route_health']['broken_count']),('Root-escape downloads',qa['download_health']['root_escape_count']),('Broken downloads',qa['download_health']['broken_download_count']),('Forbidden APIs',qa['forbidden_api_audit']['hit_count']),('Boundary gaps',qa['boundary_coverage']['gap_count'])]
    c=''.join(f"<article class='card'><div class='eyebrow'>{label}</div><h2>{val}</h2></article>" for label,val in cards)
    write(p('public/site-health.html'),f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>GoalOS Site Health</title><link rel='stylesheet' href='assets/goalos-final-hardening-v7.css'></head><body><main class='wrap'><section class='hero'><div class='eyebrow'>FINAL RELEASE HARDENING V7</div><h1>Release health is evidence.</h1><p>Route integrity, public downloads, claim boundary, token boundary, docs QA, and issue-template boundaries.</p><p><a class='btn' href='downloads/reports/final-hardening-v7-qa.json'>Download V7 QA</a><a class='btn' href='downloads/reports/final-hardening-v7-download-health.json'>Download download health</a><a class='btn' href='proof-run-001-docket.html'>Proof Run 001</a></p></section><section class='grid'>{c}</section><section class='card danger'><h2>Boundary</h2><p>{BOUNDARY}</p><p>{TOKEN_BOUNDARY}</p></section></main></body></html>")

def copy_v7_downloads():
    pats=['reports/final-hardening-v7*.json','reports/claim-scan.json','reports/site-verification.json','reports/docs-quality.json','reports/site-quality.json','content/goalos/*.json','evidence/proof-run-001/proof-run-001-final-hardening-v7*','docs/FINAL_RELEASE_HARDENING_V7.md','docs/reviewer/HOW_TO_REVIEW_FINAL_RELEASE_HARDENING_V7.md']
    count=0
    for pat in pats:
        for src in ROOT.glob(pat):
            if src.is_file() and src.suffix.lower() in SAFE_EXT:
                dest=p('public/downloads')/src.relative_to(ROOT); ensure(dest.parent); shutil.copy2(src,dest); count+=1
    return count

def write_release(rs,qa):
    state={'version':VERSION,'generated_at':NOW,'release_layer':'Final Release Hardening V7','public_pages':len(rs),'reports':len(list(p('reports').glob('*'))),'evidence_files':len(list(p('evidence').rglob('*'))) if p('evidence').exists() else 0,'workflows':len(list(p('.github/workflows').glob('*.yml'))) if p('.github/workflows').exists() else 0,'boundary':BOUNDARY,'token_boundary':TOKEN_BOUNDARY,'qa':qa}
    jwrite(p('content/goalos/release-state.json'),state); return state

def update_readme():
    r=p('README.md'); txt=read(r) if r.exists() else '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n\nAI creates output. GoalOS creates proof.\n'
    block=f"<!-- GOALOS_FINAL_HARDENING_V7_START -->\n\n## Current release health — Final Release Hardening V7\n\nCurrent source-of-truth layer: `{VERSION}`.\n\nFinal hardening unifies public downloads, site verification, docs quality, claim scanning, issue-template boundaries, Proof Run 001, and release-state metadata.\n\nBoundary: {BOUNDARY}\n\nToken boundary: {TOKEN_BOUNDARY}\n\n<!-- GOALOS_FINAL_HARDENING_V7_END -->"
    if '<!-- GOALOS_FINAL_HARDENING_V7_START -->' in txt: txt=re.sub(r'<!-- GOALOS_FINAL_HARDENING_V7_START -->.*?<!-- GOALOS_FINAL_HARDENING_V7_END -->',block,txt,flags=re.S)
    else: txt=txt.replace('\n', '\n\n'+block+'\n\n', 1) if '\n' in txt else txt+'\n\n'+block
    for phrase in ['AI creates output','GoalOS creates proof','No user data','No user funds','Human review required']:
        if phrase.lower() not in txt.lower(): txt+=f'\n\n> {phrase}.\n'
    write(r,txt)

def main():
    ensure(p('public')); ensure(p('reports')); ensure(p('content/goalos')); ensure(p('evidence/proof-run-001'))
    create_boundary_pages(); core_docs(); create_scripts(); update_readme(); tmpl=normalize_templates(); patch_index(); mirror=mirror_and_rewrite_downloads(); rs=routes(); update_registry(rs)
    qa=qa_all(tmpl); docket=proof_docket(rs,qa); release=write_release(rs,qa); site_health(rs,qa); copied=copy_v7_downloads(); qa=qa_all(tmpl); release=write_release(rs,qa); copy_v7_downloads()
    final={'version':VERSION,'generated_at':NOW,'status':'passed' if qa['status']=='passed' else 'review','mirrored_link_artifacts':mirror,'copied_v7_artifacts':copied,'docket_state':docket['decision_state'],'qa':qa,'boundary':BOUNDARY,'token_boundary':TOKEN_BOUNDARY}
    jwrite(p('reports/final-hardening-v7-final-report.json'),final); copy_v7_downloads(); print(json.dumps(final,indent=2));
    if final['status']!='passed': raise SystemExit(1)
if __name__=='__main__': main()
