from pathlib import Path
import json, datetime
ROOT=Path.cwd(); now=datetime.datetime.now(datetime.timezone.utc).isoformat()
for d in ['reports','content/goalos','evidence/demo','docs/demos','docs/reviewer','examples/validator-council','issue-bodies','public/assets']:
    Path(d).mkdir(parents=True, exist_ok=True)
readme=ROOT/'README.md'
section='\n\n## GoalOS Validator Council Arena V1 — Trust is not one judge\n\nPublic demo: [`validator-council-arena.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/validator-council-arena.html)\n\nThis browser-local arena demonstrates commit-reveal validation, validator quorum, dissent preservation, challenge windows, replay checks, and public/private proof boundaries. Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n'
if readme.exists():
    txt=readme.read_text(encoding='utf-8')
    if 'GoalOS Validator Council Arena V1' not in txt: readme.write_text(txt+section,encoding='utf-8')
else: readme.write_text('# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'+section,encoding='utf-8')
idx=ROOT/'public/index.html'
if idx.exists():
    txt=idx.read_text(encoding='utf-8')
    link='<a href="validator-council-arena.html">Validator Council</a>'
    if 'validator-council-arena.html' not in txt:
        txt=txt.replace('</nav>',link+'\n</nav>',1) if '</nav>' in txt else txt+'\n<p><a href="validator-council-arena.html">Validator Council Arena</a></p>\n'
        idx.write_text(txt,encoding='utf-8')
entry={"title":"Validator Council Arena","url":"validator-council-arena.html","description":"Commit-reveal validation, quorum, dissent, challenge windows, replay, and public/private proof boundaries."}
search=ROOT/'public/search-index.json'; items=[]
if search.exists():
    try:
        data=json.loads(search.read_text(encoding='utf-8')); items=data if isinstance(data,list) else data.get('items',[])
    except Exception: items=[]
if not any(isinstance(x,dict) and x.get('url')==entry['url'] for x in items): items.append(entry)
search.write_text(json.dumps(items,indent=2),encoding='utf-8')
loc='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/validator-council-arena.html'; sitemap=ROOT/'public/sitemap.xml'
if sitemap.exists():
    xml=sitemap.read_text(encoding='utf-8')
    if loc not in xml:
        xml=xml.replace('</urlset>',f'<url><loc>{loc}</loc></url>\n</urlset>') if '</urlset>' in xml else xml+'\n'+loc+'\n'
        sitemap.write_text(xml,encoding='utf-8')
else: sitemap.write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{loc}</loc></url></urlset>',encoding='utf-8')
(ROOT/'public/.nojekyll').write_text('',encoding='utf-8')
report={"status":"passed","installedAt":now,"page":"public/validator-council-arena.html","browserLocal":True,"noUserData":True,"noUserFunds":True,"walletOrMainnet":False,"humanReviewRequired":True}
(ROOT/'reports/validator-council-arena-v1-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
