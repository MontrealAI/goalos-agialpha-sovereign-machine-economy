#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path.cwd()
ROUTE='from-loop-to-rsi-state-capacity.html'
TITLE='From Loop to RSI State-Capacity Command Room V3'
SUMMARY='Build the governance institution first: deterministic RSI pipeline, ECI evidence, Move-37 dossiers, council review, and governed decision state.'

def read(path):
    p=ROOT/path
    return p.read_text(encoding='utf-8') if p.exists() else ''

def write(path,text):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')

# README marker
marker='<!-- GOALOS_FROM_LOOP_TO_RSI_STATE_CAPACITY_V3 -->'
readme=read('README.md')
if readme and marker not in readme:
    block='\n'.join([marker,'## New public demo: From Loop to RSI State-Capacity Command Room V3','', '**Build the governance institution first.**','',f'Open: [`public/{ROUTE}`](public/{ROUTE})','', 'This browser-local demo shows how a long-running agent loop becomes deterministic RSI governance: drift sentinel, ECI evidence, baseline gate, Move-37 dossier, Architect / Validator Council, and governed decision state.'])
    write('README.md', readme.rstrip()+'\n\n'+block+'\n')
card=('<section class="goalos-added-route" style="margin:32px auto;max-width:1100px;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:rgba(255,255,255,.06);color:inherit">'
      '<p style="letter-spacing:.24em;color:#ffe976;font-weight:900;text-transform:uppercase">New public demo / From Loop to RSI</p>'
      '<h2 style="font-size:clamp(2rem,4vw,4.5rem);line-height:.95;margin:.2rem 0">Build the governance institution first.</h2>'
      '<p>Run the From Loop to RSI State-Capacity Command Room: deterministic pipeline, ECI evidence, baseline gates, Move-37 dossiers, council review, and governed decision state. Browser-local. No data. No funds.</p>'
      f'<p><a href="{ROUTE}" style="display:inline-block;padding:.9rem 1.1rem;border-radius:999px;background:linear-gradient(135deg,#ffe976,#69ffd0);color:#071016;font-weight:900;text-decoration:none">Open RSI Command Room</a></p></section>')
for page in ['public/index.html','public/demo-ecosystem-registry.html','public/site-map.html','public/website-operating-system.html']:
    txt=read(page)
    if txt and ROUTE not in txt:
        if '</main>' in txt: txt=txt.replace('</main>',card+'\n</main>')
        elif '</body>' in txt: txt=txt.replace('</body>',card+'\n</body>')
        else: txt += card
        write(page,txt)
entry={'title':TITLE,'url':ROUTE,'description':SUMMARY,'category':'From Loop to RSI'}
sp=ROOT/'public/search-index.json'
try: data=json.loads(sp.read_text(encoding='utf-8')) if sp.exists() else []
except Exception: data=[]
if isinstance(data,list): data=[x for x in data if not(isinstance(x,dict) and x.get('url')==ROUTE)]+[entry]
elif isinstance(data,dict):
    arr=data.get('items') or data.get('routes') or data.get('pages') or []
    if not isinstance(arr,list): arr=[]
    data['items']=[x for x in arr if not(isinstance(x,dict) and x.get('url')==ROUTE)]+[entry]
else: data=[entry]
write('public/search-index.json',json.dumps(data,indent=2))
rp=ROOT/'content/goalos/demo-ecosystem-registry.json'
try: reg=json.loads(rp.read_text(encoding='utf-8')) if rp.exists() else {'routes':[]}
except Exception: reg={'routes':[]}
key='routes' if 'routes' in reg else 'demos'
if not isinstance(reg.get(key),list): reg[key]=[]
reg_entry={'demo':TITLE,'canonicalPath':ROUTE,'description':SUMMARY,'workflowCategory':'From Loop to RSI / State-Capacity Governance','expectedInputs':['RSI scenario','public-safe objective','replayability target','ECI level','novelty distance','advantage delta','shock persistence','risk pressure','gate toggles'],'generatedArtifacts':['RSI state JSON','Move-37 dossier JSON','ECI ledger JSON','Council memo','90-day pilot plan','reviewer brief'],'proofGates':['schema-bound artifacts','state hash continuity','drift sentinel','executed evidence','baseline comparison','OMNI allocation-only','Move-37 dossier','shock persistence','council review','rollback ready','public/private boundary','human review'],'stateTransitions':['RSI_STATE_CAPACITY_REVIEW_READY','MOVE37_DOSSIER_REVIEW_READY','REJECT_SCHEMA_DRIFT','REJECT_OMNI_OUTCOME_AUTHORITY','BLOCK_PRIVACY_BOUNDARY'],'role':'UI demo / governance console / reviewer module / dossier generator'}
reg[key]=[x for x in reg[key] if x.get('canonicalPath')!=ROUTE and x.get('url')!=ROUTE]+[reg_entry]
write('content/goalos/demo-ecosystem-registry.json',json.dumps(reg,indent=2))
sm=read('public/sitemap.xml')
loc=f'<loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{ROUTE}</loc>'
if sm and loc not in sm:
    item=f'  <url>\n    {loc}\n  </url>\n'
    sm=sm.replace('</urlset>',item+'</urlset>') if '</urlset>' in sm else sm+'\n'+item
    write('public/sitemap.xml',sm)
print('GoalOS From Loop to RSI State-Capacity Command Room V3 installed.')
