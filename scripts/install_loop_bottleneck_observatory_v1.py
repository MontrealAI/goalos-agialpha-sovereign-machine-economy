#!/usr/bin/env python3
from pathlib import Path
import json, re, datetime
ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
PAGE = "loop-bottleneck-observatory.html"
TITLE = "GoalOS Loop Bottleneck Observatory"
DESC = "The bottleneck always moves. A browser-local loop demo for contract, state, trace, restart, evaluator, rubric, harness, and proof-boundary gates."
changed=[]

def read(p):
    return p.read_text(encoding='utf-8') if p.exists() else ''
def write(p,s):
    p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding='utf-8'); changed.append(str(p))

def patch_readme():
    p=ROOT/'README.md'; s=read(p)
    block='''\n\n## GoalOS Loop Bottleneck Observatory V1\n\n**The bottleneck always moves.** This browser-local public demo shows how a long-running GoalOS loop exposes its next bottleneck: contract, roles, disk state, trace reading, restartability, evaluator independence, taste rubric, harness overhead, or proof boundary.\n\nOpen: [`public/loop-bottleneck-observatory.html`](public/loop-bottleneck-observatory.html)\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n'''
    if 'Loop Bottleneck Observatory V1' not in s:
        write(p,(s.rstrip()+block+'\n') if s else '# GoalOS AGIALPHA Ascension\n'+block)

def patch_index():
    p=ROOT/'public/index.html'; s=read(p)
    if not s or PAGE in s: return
    card='''\n<section class="goalos-loop-bottleneck-card" style="max-width:1100px;margin:40px auto;padding:28px;border:1px solid rgba(255,255,255,.18);border-radius:28px;background:rgba(255,255,255,.07);color:#fff;">\n  <p style="color:#ffe66d;letter-spacing:.24em;font-weight:900;text-transform:uppercase;">New loop demo</p>\n  <h2 style="font-size:clamp(32px,5vw,64px);line-height:.95;margin:0 0 12px;">The bottleneck always moves.</h2>\n  <p style="font-size:18px;line-height:1.55;color:#cfe0f3;max-width:820px;">Run the Loop Bottleneck Observatory: expose the next bottleneck in a long-running agent loop, then download the contract, trace ledger, replay pack, bottleneck report, and reviewer brief.</p>\n  <a href="loop-bottleneck-observatory.html" style="display:inline-block;margin-top:10px;padding:14px 18px;border-radius:999px;background:linear-gradient(110deg,#ffe66d,#6dffd3);color:#071015;text-decoration:none;font-weight:900;">Open Loop Bottleneck Observatory</a>\n</section>\n'''
    if '</main>' in s: s=s.replace('</main>',card+'</main>',1)
    elif '</body>' in s: s=s.replace('</body>',card+'</body>',1)
    else: s+=card
    write(p,s)

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'; s=read(p)
    url=f'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{PAGE}'
    if not s:
        s=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>{url}</loc></url>\n</urlset>\n'
    elif PAGE not in s and '</urlset>' in s:
        s=s.replace('</urlset>',f'  <url><loc>{url}</loc><lastmod>{NOW[:10]}</lastmod></url>\n</urlset>')
    write(p,s)

def patch_search_index():
    p=ROOT/'public/search-index.json'
    try: data=json.loads(read(p) or '[]')
    except Exception: data=[]
    entry={"title":TITLE,"url":PAGE,"path":PAGE,"description":DESC,"category":"loop governance","keywords":["loop","bottleneck","agent","trace","restart","contract","docket"]}
    if isinstance(data,list):
        if not any((x.get('url')==PAGE or x.get('path')==PAGE) for x in data if isinstance(x,dict)): data.append(entry)
    elif isinstance(data,dict):
        arr=data.get('items') or data.get('pages') or data.get('routes') or []
        if not any((x.get('url')==PAGE or x.get('path')==PAGE) for x in arr if isinstance(x,dict)): arr.append(entry)
        key='items' if 'items' in data else ('pages' if 'pages' in data else 'routes')
        data[key]=arr
    write(p,json.dumps(data,indent=2,ensure_ascii=False)+"\n")

def patch_registry_json():
    p=ROOT/'content/goalos/demo-ecosystem-registry.json'
    try: data=json.loads(read(p) or '{}')
    except Exception: data={}
    entry={"name":TITLE,"path":PAGE,"canonical_url":PAGE,"description":DESC,"primary_workflow_category":"loop governance","expected_inputs":["public-safe objective","scenario","risk class","loop horizon","loop gates","quality sliders"],"generated_outputs":["bottleneck report","loop contract","trace ledger","replay pack","reviewer brief"],"proof_gates":["contract before code","role separation","disk state","trace reading","restartability","independent evaluator","taste rubric","harness deletion plan","public/private boundary","human review"],"state_transitions":["LOOP_DRAFT","LOOP_REVIEW_READY","REJECT_NO_CONTRACT","HOLD_STATE_FILES_REQUIRED","REJECT_SELF_GRADED_LOOP","BLOCK_PRIVACY_BOUNDARY"],"role":"UI demo / scoring module / reviewer module"}
    if isinstance(data,dict):
        key='routes' if 'routes' in data else 'demos'
        arr=data.get(key,[])
        if not any((x.get('path')==PAGE or x.get('canonical_url')==PAGE) for x in arr if isinstance(x,dict)): arr.append(entry)
        data[key]=arr
    else: data={"demos":[entry]}
    write(p,json.dumps(data,indent=2,ensure_ascii=False)+"\n")

def patch_html_listing(rel, heading):
    p=ROOT/rel; s=read(p)
    if not s or PAGE in s: return
    link=f'''\n<article style="padding:18px;border:1px solid rgba(255,255,255,.16);border-radius:20px;background:rgba(255,255,255,.06);margin:16px 0;">\n  <h3>{TITLE}</h3><p>{DESC}</p><a href="{PAGE}">Open →</a>\n</article>\n'''
    if '</main>' in s: s=s.replace('</main>',link+'</main>',1)
    elif '</body>' in s: s=s.replace('</body>',link+'</body>',1)
    else: s+=link
    write(p,s)

def main():
    (ROOT/'public/.nojekyll').parent.mkdir(parents=True, exist_ok=True)
    (ROOT/'public/.nojekyll').touch()
    patch_readme(); patch_index(); patch_sitemap(); patch_search_index(); patch_registry_json()
    for rel in ['public/demo-ecosystem-registry.html','public/site-map.html','public/website-operating-system.html']:
        patch_html_listing(rel,TITLE)
    report={"status":"passed","name":"GoalOS Loop Bottleneck Observatory V1","generated_at":NOW,"changed_files":sorted(set(changed)),"page":f"public/{PAGE}","boundary":"no user data; no user funds; no wallet; no transaction; no network call; human review required"}
    write(ROOT/'reports/loop-bottleneck-observatory-v1-install-report.json',json.dumps(report,indent=2)+"\n")
    print(json.dumps(report, indent=2))
if __name__=='__main__': main()
