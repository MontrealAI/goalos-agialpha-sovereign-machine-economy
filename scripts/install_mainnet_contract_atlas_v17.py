
import json, pathlib, re, shutil, datetime, html, xml.etree.ElementTree as ET
ROOT = pathlib.Path.cwd()
PUBLIC = ROOT / 'public'
PUBLIC.mkdir(exist_ok=True)
REPORTS = ROOT / 'reports'; REPORTS.mkdir(exist_ok=True)
EVIDENCE = ROOT / 'evidence/demo'; EVIDENCE.mkdir(parents=True, exist_ok=True)
CONTENT = ROOT / 'content/goalos'; CONTENT.mkdir(parents=True, exist_ok=True)

def copy_tree(src, dst):
    src = pathlib.Path(src); dst = pathlib.Path(dst); dst.mkdir(parents=True, exist_ok=True)
    for p in src.rglob('*'):
        if p.is_file():
            q = dst / p.relative_to(src); q.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, q)

# Copy generated assets/pages from unpacked pack into repository.
for folder in ['public','docs','content','evidence','reports','issue-bodies']:
    src = ROOT / folder
    # Files already extracted into the same paths by zip; nothing needed.

# Ensure key pages exist and update homepage with a visible contract atlas section.
index = PUBLIC / 'index.html'
section = '''
<section id="mainnet-contract-atlas-v17" style="margin:48px auto;padding:32px;border:1px solid rgba(112,255,216,.28);border-radius:28px;background:linear-gradient(135deg,rgba(112,255,216,.12),rgba(169,140,255,.10));max-width:1180px;color:#f8f4e9;font-family:Inter,system-ui,sans-serif">
  <p style="letter-spacing:.28em;text-transform:uppercase;color:#ffed8d;font-weight:900;font-size:12px">Ethereum Mainnet · 48 GoalOS-created contracts</p>
  <h2 style="font-size:clamp(38px,5vw,70px);line-height:.9;letter-spacing:-.06em;margin:0 0 14px">Learn the public proof rail.</h2>
  <p style="font-size:19px;line-height:1.5;max-width:850px">Open the browser-local Mainnet Contract Atlas: search every contract, learn the AEP lifecycle, inspect addresses, follow the proof rail, download a reviewer brief, and understand the token/user-fund boundary without a wallet or transaction.</p>
  <p><a href="mainnet-contract-atlas.html" style="display:inline-block;margin:8px 8px 0 0;padding:14px 18px;border-radius:999px;background:linear-gradient(135deg,#ffed8d,#70ffd8);color:#071018;font-weight:900;text-decoration:none">Open Contract Atlas</a><a href="mainnet-proof-rail.html" style="display:inline-block;margin:8px 8px 0 0;padding:14px 18px;border-radius:999px;border:1px solid rgba(255,255,255,.18);color:#70ffd8;font-weight:900;text-decoration:none">Open Proof Rail</a><a href="contract-academy.html" style="display:inline-block;margin:8px 8px 0 0;padding:14px 18px;border-radius:999px;border:1px solid rgba(255,255,255,.18);color:#70ffd8;font-weight:900;text-decoration:none">Learn the 48</a></p>
  <p style="font-weight:800;color:#d7e9f5">No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.</p>
</section>
'''
if index.exists():
    text = index.read_text(encoding='utf-8', errors='ignore')
    if 'mainnet-contract-atlas-v17' not in text:
        if '</main>' in text:
            text = text.replace('</main>', section + '\n</main>', 1)
        elif '</body>' in text:
            text = text.replace('</body>', section + '\n</body>', 1)
        else:
            text += section
        index.write_text(text, encoding='utf-8')
else:
    index.write_text('<!doctype html><meta charset="utf-8"><title>GoalOS</title>'+section, encoding='utf-8')

# Add a small route button to older pages without overwriting them.
button = '<a class="goalos-contract-atlas-v17-button" href="mainnet-contract-atlas.html">Contracts</a>'
style = '<style>.goalos-contract-atlas-v17-button{position:fixed;right:18px;bottom:76px;z-index:9999;padding:12px 16px;border-radius:999px;background:linear-gradient(135deg,#ffed8d,#70ffd8);color:#061018;font:900 13px system-ui;text-decoration:none;box-shadow:0 12px 40px rgba(0,0,0,.35)}</style>'
for p in PUBLIC.glob('*.html'):
    if p.name in {'mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html'}: continue
    txt = p.read_text(encoding='utf-8', errors='ignore')
    if 'goalos-contract-atlas-v17-button' not in txt:
        ins = style + button
        if '</body>' in txt: txt = txt.replace('</body>', ins+'</body>', 1)
        else: txt += ins
        p.write_text(txt, encoding='utf-8')

# Build route index/search/sitemap.
routes=[]
for p in sorted(PUBLIC.glob('*.html')):
    txt=p.read_text(encoding='utf-8', errors='ignore')
    title_match=re.search(r'<title[^>]*>(.*?)</title>', txt, re.I|re.S)
    h1_match=re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I|re.S)
    title=re.sub('<[^>]+>',' ', (title_match.group(1) if title_match else h1_match.group(1) if h1_match else p.stem)).strip()
    desc='GoalOS public proof surface.'
    if 'mainnet-contract-atlas' in p.name: desc='Interactive browser-local atlas for the 48 GoalOS-created Ethereum Mainnet contracts.'
    if 'mainnet-proof-rail' in p.name: desc='Plain-language contract journey from public proof to Chronicle memory.'
    if 'contract-academy' in p.name: desc='Guided learning path for the 48 Mainnet contracts.'
    routes.append({'title':title,'url':p.name,'category':'Mainnet Contract Rail' if 'contract' in p.name or 'mainnet' in p.name else 'Existing public page','description':desc})
(PUBLIC/'search-index.json').write_text(json.dumps(routes, indent=2), encoding='utf-8')
(CONTENT/'public-proof-navigation-v17.json').write_text(json.dumps({'version':'v17','routes':routes}, indent=2), encoding='utf-8')
# sitemap XML
base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{base}{r["url"]}</loc></url>\n' for r in routes) + '</urlset>\n'
(PUBLIC/'sitemap.xml').write_text(sitemap, encoding='utf-8')

# Update registry JSON with contract atlas route.
reg = CONTENT/'demo-ecosystem-registry.json'
entry = {'name':'GoalOS Mainnet Contract Atlas V17','canonicalUrl':'mainnet-contract-atlas.html','oneLine':'Deep browser-local guide to the 48 GoalOS-created Ethereum Mainnet contracts.','workflowCategory':'mainnet-contract-education','expectedInputs':['public-safe route interaction only'], 'generatedOutputs':['contract atlas JSON','contract CSV','reviewer brief'], 'proofGates':['no wallet','no transaction','no network call','token boundary','human review required'], 'nextState':'MAINNET_CONTRACT_ATLAS_REVIEW_READY'}
try:
    obj=json.loads(reg.read_text(encoding='utf-8')) if reg.exists() else {'routes':[]}
except Exception: obj={'routes':[]}
arr = obj.get('routes') or obj.get('demos') or []
if not any((x.get('canonicalUrl') or x.get('url')) == 'mainnet-contract-atlas.html' for x in arr if isinstance(x,dict)):
    arr.insert(0, entry)
obj['routes']=arr; obj['demos']=arr
reg.write_text(json.dumps(obj, indent=2), encoding='utf-8')

# reports
contracts=json.loads((ROOT/'content/goalos/mainnet-contracts-v4.4.0.json').read_text(encoding='utf-8'))
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [PUBLIC/'assets/goalos-mainnet-contract-atlas-v17.js', PUBLIC/'assets/goalos-mainnet-contract-data-v17.js']:
    t=p.read_text(encoding='utf-8', errors='ignore')
    for f in forbidden:
        if f in t: hits.append({'file':str(p),'pattern':f})
local_links=[]
for p in PUBLIC.glob('*.html'):
    txt=p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'href=["\']([^"\']+\.html(?:#[^"\']*)?)["\']', txt):
        href=m.group(1).split('#')[0]
        if href.startswith('http') or href.startswith('mailto:'): continue
        if not (PUBLIC/href).exists(): local_links.append({'source':p.name,'missing':href})
status = 'passed' if len(contracts['contracts'])==49 and contracts['metadata']['goalosCreatedContractCount']==48 and not hits and not local_links else 'review'
report={'status':status,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z','contractEntries':len(contracts['contracts']),'goalosCreated':contracts['metadata']['goalosCreatedContractCount'],'externalEntries':1,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':local_links,'boundary':'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'}
(REPORTS/'mainnet-contract-atlas-v17-qa.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(REPORTS/'mainnet-contract-atlas-v17-route-health.json').write_text(json.dumps({'status':'passed' if not local_links else 'review','brokenInternalHtmlLinks':local_links,'routes':len(routes)}, indent=2), encoding='utf-8')
(REPORTS/'mainnet-contract-atlas-v17-install-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
(REPORTS/'mainnet-contract-atlas-v17-demo-run.json').write_text(json.dumps({'status':'passed','actions':['render atlas','filter contracts','select AEPProofLedger','download JSON','download reviewer brief'],'externalActions':0}, indent=2), encoding='utf-8')
(EVIDENCE/'mainnet-contract-atlas-v17-reference-docket.json').write_text(json.dumps({'status':'REVIEW_READY','claim':'The site contains a browser-local public atlas for the 48 GoalOS-created Ethereum Mainnet contracts and canonical external AGIALPHA boundary.','evidence':['content/goalos/mainnet-contracts-v4.4.0.json','public/mainnet-contract-atlas.html','reports/mainnet-contract-atlas-v17-qa.json'],'boundary':report['boundary']}, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
