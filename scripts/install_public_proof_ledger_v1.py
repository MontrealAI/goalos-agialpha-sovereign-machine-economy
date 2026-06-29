from __future__ import annotations
import json, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def sj(p):
    try: return json.loads(p.read_text(encoding='utf-8'))
    except Exception: return None
def st(o):
    if isinstance(o,dict):
        for k in ('status','conclusion','result'):
            if isinstance(o.get(k),str): return o[k]
        if o.get('errors')==[]: return 'passed'
    return 'registered'
def tt(p): return ' '.join(w.upper() if w in {'qa','v1','v2','v3','v4','v5','v6'} else w.capitalize() for w in p.stem.replace('_','-').split('-'))
stations=[('Multi-Agent Institution','Not a swarm. An institution.','multi-agent-institution.html'),('Proof Gradient Lab','No proof, no evolution.','proof-gradient-lab.html'),('Evidence Docket Theatre','A proof page is not a marketing page.','evidence-docket-theatre.html'),('Proof-to-Action Command Room','The deliverable is a governed decision state.','proof-to-action-command-room.html'),('Capability Compounding Lab','Verified work becomes reusable capability.','capability-compounding-lab.html'),('Sovereign Experience Stream Lab','Proof becomes governed experience.','sovereign-experience-stream-lab.html'),('Proof-Settlement Chronicle Lab','No ProofBundle, no settlement.','proof-settlement-chronicle-lab.html'),('Falsification Gauntlet','Strong claims survive baselines.','falsification-gauntlet.html'),('Proof Experience Atlas','One guided public proof journey.','proof-experience-atlas.html'),('Proof Mission Forge','Turn objective into docket.','proof-mission-forge.html'),('Proof Mission Control','Public mission operating board.','proof-mission-control.html'),('Proof Run 001 Execution Room','Architecture becomes first docket.','proof-run-001-execution-room.html'),('External Reviewer Replay Room','Independent review makes proof real.','external-reviewer-replay-room.html')]
entries=[]
for a,b,c in stations: entries.append({'title':a,'type':'page','group':'review' if 'Reviewer' in a else 'page','status':'live' if (ROOT/'public'/c).exists() else 'planned','path':c,'summary':b})
for base,typ in [('evidence','docket'),('reports','report')]:
    d=ROOT/base
    if d.exists():
        for p in sorted(d.rglob('*.json')): entries.append({'title':tt(p),'type':typ,'status':st(sj(p)),'path':p.relative_to(ROOT).as_posix(),'summary':'Registered public artifact generated from repository evidence.'})
for folder in ['docs/reviewer','docs/demos','docs/proof-runs','docs/proof-missions']:
    d=ROOT/folder
    if d.exists():
        for p in sorted(d.glob('*.md'))[:80]: entries.append({'title':tt(p),'type':'review' if 'reviewer' in folder else 'page','status':'available','path':p.relative_to(ROOT).as_posix(),'summary':'Human-readable review or demo documentation.'})
totals={'dockets':sum(e['type']=='docket' for e in entries),'reports':sum(e['type']=='report' for e in entries),'pages':sum(e['type']=='page' for e in entries),'review_paths':sum(e.get('type')=='review' or e.get('group')=='review' for e in entries),'missing':sum(e.get('status')=='planned' for e in entries)}
ledger={'schema':'goalos.public_proof_ledger.v1','generated_at':NOW,'boundary':{'no_user_data':True,'no_user_funds':True,'no_wallet':True,'no_transaction':True,'no_network_call':True,'human_review_required':True},'totals':totals,'stations':[{'title':a,'thesis':b,'href':c,'status':'live' if (ROOT/'public'/c).exists() else 'planned'} for a,b,c in stations],'entries':entries[:250]}
for d in ['content/goalos','reports','evidence/proof-ledger','public/assets']: (ROOT/d).mkdir(parents=True,exist_ok=True)
(ROOT/'content/goalos/public-proof-ledger-v1.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
(ROOT/'evidence/proof-ledger/public-proof-ledger-v1-reference-ledger.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
(ROOT/'public/assets/goalos-proof-ledger-data.js').write_text('window.GOALOS_PUBLIC_PROOF_LEDGER = '+json.dumps(ledger,indent=2)+';\n',encoding='utf-8')
manifest={'status':'installed','generated_at':NOW,'entries':len(entries),'totals':totals,'page':'public/proof-ledger.html'}
(ROOT/'reports/public-proof-ledger-v1-install-report.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
readme=ROOT/'README.md'
block="\n\n## Public Proof Ledger V1\n\nGoalOS now includes a browser-local Public Proof Ledger: a unified registry for Evidence Dockets, QA reports, public demo pages, reviewer paths, and Proof Run 001 readiness.\n\n- Website: `proof-ledger.html`\n- Rule: No Evidence Docket, no strong claim.\n- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n"
if readme.exists():
    txt=readme.read_text(encoding='utf-8')
    if '## Public Proof Ledger V1' not in txt: readme.write_text(txt.rstrip()+block+'\n',encoding='utf-8')
index=ROOT/'public/index.html'
if index.exists():
    txt=index.read_text(encoding='utf-8')
    if 'proof-ledger.html' not in txt:
        txt=txt.replace('</nav>','<a href="proof-ledger.html">Proof Ledger</a></nav>',1) if '</nav>' in txt else txt+'\n<!-- Proof Ledger: proof-ledger.html -->\n'
        index.write_text(txt,encoding='utf-8')
search_path=ROOT/'public/search-index.json'
try:
    search=json.loads(search_path.read_text(encoding='utf-8')) if search_path.exists() else []
    if isinstance(search,dict): search=search.get('pages',[])
except Exception: search=[]
if not any(isinstance(x,dict) and x.get('url')=='proof-ledger.html' for x in search): search.append({'title':'Public Proof Ledger','url':'proof-ledger.html','description':'Unified registry for GoalOS public proof surfaces, dockets, reports, review paths, and Proof Run 001 readiness.'})
search_path.write_text(json.dumps(search,indent=2),encoding='utf-8')
sitemap=ROOT/'public/sitemap.xml'
if sitemap.exists():
    s=sitemap.read_text(encoding='utf-8')
    if 'proof-ledger.html' not in s: sitemap.write_text(s.replace('</urlset>','  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-ledger.html</loc></url>\n</urlset>'),encoding='utf-8')
else: sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-ledger.html</loc></url>\n</urlset>\n',encoding='utf-8')
(ROOT/'.nojekyll').write_text('',encoding='utf-8')
print(json.dumps(manifest,indent=2))
