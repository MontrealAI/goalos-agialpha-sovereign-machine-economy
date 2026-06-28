
from pathlib import Path
import json, datetime
ROOT=Path.cwd()
readme=ROOT/'README.md'
block='''\n\n## Proof-Settlement Chronicle Lab V1\n\n**No ProofBundle, no settlement.** The browser-local Proof-Settlement Chronicle Lab demonstrates the safe public lifecycle: Request -> Escrow -> Execute -> Proof -> Validate -> Settle -> Chronicle. It is simulation-only: no user data, no user funds, no wallet, no transaction, no network call, no production authority, and human review required.\n\n- Website: `public/proof-settlement-chronicle-lab.html`\n- QA report: `reports/proof-settlement-chronicle-lab-v1-qa.json`\n- Reference docket: `evidence/demo/proof-settlement-chronicle-lab-v1-reference-docket.json`\n'''
if readme.exists():
    text=readme.read_text()
    if '## Proof-Settlement Chronicle Lab V1' not in text:
        readme.write_text(text.rstrip()+block+'\n')
idx=ROOT/'public/index.html'
if idx.exists():
    text=idx.read_text(); link='<a href="proof-settlement-chronicle-lab.html">Proof-Settlement Lab</a>'
    if 'proof-settlement-chronicle-lab.html' not in text:
        text=text.replace('</nav>',link+'</nav>',1) if '</nav>' in text else text+'\n<p>'+link+'</p>\n'
        idx.write_text(text)
si=ROOT/'public/search-index.json'; entry={'title':'Proof-Settlement Chronicle Lab','url':'proof-settlement-chronicle-lab.html','description':'No ProofBundle, no settlement. Browser-local GoalOS proof-settlement simulation.'}; items=[]
if si.exists():
    try:
        data=json.loads(si.read_text()); items=data if isinstance(data,list) else data.get('items',[])
    except Exception: items=[]
if not any(isinstance(i,dict) and i.get('url')==entry['url'] for i in items): items.append(entry)
si.parent.mkdir(parents=True,exist_ok=True); si.write_text(json.dumps(items,indent=2))
sm=ROOT/'public/sitemap.xml'; url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-settlement-chronicle-lab.html'
if sm.exists():
    s=sm.read_text()
    if 'proof-settlement-chronicle-lab.html' not in s:
        s=s.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>') if '</urlset>' in s else s+'\n'+url+'\n'; sm.write_text(s)
else:
    sm.write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n')
(ROOT/'.nojekyll').write_text('')
report={'status':'passed','installed_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','page':'public/proof-settlement-chronicle-lab.html'}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/proof-settlement-chronicle-lab-v1-install-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
