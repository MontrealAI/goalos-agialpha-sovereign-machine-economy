from pathlib import Path
import json, datetime, re
ROOT = Path.cwd()
PAGE = "from-loop-to-rsi-sovereign-console.html"
TITLE = "From Loop to RSI Sovereign Console"
MARK = "GOALOS_FROM_LOOP_TO_RSI_SOVEREIGN_CONSOLE_V2"
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def patch_between(path, block):
    p = ROOT/path
    text = read(p)
    start = f"<!-- {MARK}:START -->"
    end = f"<!-- {MARK}:END -->"
    wrapped = f"\n{start}\n{block}\n{end}\n"
    if start in text and end in text:
        text = re.sub(re.escape(start)+r".*?"+re.escape(end), wrapped.strip(), text, flags=re.S)
    else:
        text = text + wrapped
    write(p, text)

def patch_readme():
    block = '''
## From Loop to RSI Sovereign Console V2

A browser-local public demonstration showing how restartable loops become deterministic RSI governance: schema-bound artifacts, state hashes, ECI evidence discipline, baseline gates, Move-37 dossiers, and Architect/Validator Council review.

- Public page: `public/from-loop-to-rsi-sovereign-console.html`
- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
- Decision states include `RSI_REVIEW_READY`, `MOVE37_DOSSIER_REVIEW_READY`, `REJECT_OMNI_OUTCOME_AUTHORITY`, and `BLOCK_PRIVACY_BOUNDARY`.
'''
    patch_between(Path('README.md'), block)

def patch_index():
    p=ROOT/'public/index.html'
    if not p.exists(): return
    text=read(p)
    if MARK in text: return
    card=f'''
<section class="goalos-card goalos-rsi-console" id="from-loop-to-rsi-console" style="margin:48px auto;padding:32px;border:1px solid rgba(255,255,255,.18);border-radius:28px;background:linear-gradient(135deg,rgba(102,255,210,.12),rgba(154,119,255,.12));max-width:1100px;">
  <!-- {MARK}:START -->
  <p style="letter-spacing:.25em;text-transform:uppercase;color:#ffe66d;font-weight:900;">New public demo / Loop → RSI</p>
  <h2 style="font-size:clamp(34px,5vw,64px);line-height:.95;margin:10px 0;color:#fff;">Build the governance institution first.</h2>
  <p style="color:#dce7ff;font-size:18px;max-width:820px;">Run the browser-local From Loop to RSI Sovereign Console: TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE, with OMNI allocation-only, ECI evidence discipline, Move-37 dossiers, and Architect/Validator Council gates.</p>
  <p><a href="from-loop-to-rsi-sovereign-console.html" style="display:inline-block;padding:14px 18px;border-radius:999px;background:linear-gradient(135deg,#ffe66d,#66ffd2);color:#061018;font-weight:900;text-decoration:none;">Open RSI Console</a></p>
  <!-- {MARK}:END -->
</section>
'''
    if '</main>' in text:
        text=text.replace('</main>', card+'\n</main>',1)
    elif '</body>' in text:
        text=text.replace('</body>', card+'\n</body>',1)
    else:
        text += card
    write(p,text)

def patch_search_index():
    p=ROOT/'public/search-index.json'
    entry={"title":TITLE,"url":PAGE,"description":"Browser-local From Loop to RSI console: deterministic invention pipeline, OMNI allocation-only, ECI, Move-37 dossier, and Architect/Validator Council gates.","category":"Loop / RSI"}
    try:
        data=json.loads(read(p) or '[]')
    except Exception:
        data=[]
    if isinstance(data, dict):
        arr=data.get('pages') or data.get('routes') or []
        if not any((x.get('url') or x.get('path'))==PAGE for x in arr if isinstance(x,dict)):
            arr.append(entry)
        data['pages']=arr
    elif isinstance(data,list):
        if not any((x.get('url') or x.get('path'))==PAGE for x in data if isinstance(x,dict)):
            data.append(entry)
    else:
        data=[entry]
    write(p,json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'
    text=read(p)
    url=f"  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{PAGE}</loc></url>\n"
    if PAGE in text: return
    if '</urlset>' in text:
        text=text.replace('</urlset>',url+'</urlset>')
    else:
        text='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+url+'</urlset>\n'
    write(p,text)

def patch_registry_json():
    p=ROOT/'content/goalos/demo-ecosystem-registry.json'
    entry={"name":TITLE,"canonical_path":PAGE,"description":"Loop-to-RSI public demo for deterministic sovereign invention governance.","workflow_category":"Loop → RSI governance","expected_inputs":["objective","scenario","novelty","advantage","ECI","risk","baseline","persistence","gate toggles"],"generated_outputs":["RSI state","Move-37 dossier","ECI ledger","reviewer brief"],"proof_gates":["schema","state hash","ECI","baseline","risk","persistence","replay","OMNI allocation-only","dossier","council","boundary"],"state_transitions":["RSI_REVIEW_READY","MOVE37_DOSSIER_REVIEW_READY","REJECT_OMNI_OUTCOME_AUTHORITY","BLOCK_PRIVACY_BOUNDARY"],"role":"UI demo / governance console / reviewer module"}
    try: data=json.loads(read(p) or '{}')
    except Exception: data={}
    routes=data.get('routes') or data.get('demos') or []
    routes=[r for r in routes if not (isinstance(r,dict) and (r.get('canonical_path')==PAGE or r.get('url')==PAGE or r.get('path')==PAGE))]
    routes.append(entry)
    data['routes']=routes
    data['demos']=routes
    data['updated_at']=NOW
    write(p,json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def append_card(path, heading):
    p=ROOT/path
    if not p.exists(): return
    text=read(p)
    if MARK in text: return
    card=f'''\n<section id="from-loop-to-rsi-sovereign-console" style="margin:32px 0;padding:24px;border:1px solid rgba(255,255,255,.18);border-radius:24px;">\n<!-- {MARK}:START -->\n<h2>{heading}</h2>\n<p>Browser-local From Loop to RSI Sovereign Console: deterministic invention pipeline, ECI, baselines, Move-37 dossier, and Architect/Validator Council gates.</p>\n<p><a href="{PAGE}">Open the RSI Sovereign Console →</a></p>\n<!-- {MARK}:END -->\n</section>\n'''
    if '</main>' in text: text=text.replace('</main>',card+'</main>',1)
    elif '</body>' in text: text=text.replace('</body>',card+'</body>',1)
    else: text+=card
    write(p,text)

def reports():
    report={"status":"passed","installed_at":NOW,"page":PAGE,"no_user_data":True,"no_user_funds":True,"wallet":False,"network_call":False,"human_review_required":True,"files":[PAGE,"public/assets/goalos-from-loop-to-rsi-sovereign-console-v2.css","public/assets/goalos-from-loop-to-rsi-sovereign-console-v2.js"]}
    write(ROOT/'reports/from-loop-to-rsi-sovereign-console-v2-install-report.json',json.dumps(report,indent=2)+'\n')

patch_readme(); patch_index(); patch_search_index(); patch_sitemap(); patch_registry_json()
append_card(Path('public/demo-ecosystem-registry.html'), 'From Loop to RSI Sovereign Console')
append_card(Path('public/site-map.html'), 'From Loop to RSI Sovereign Console')
append_card(Path('public/website-operating-system.html'), 'From Loop to RSI Sovereign Console')
write(ROOT/'public/.nojekyll','')
reports()
print('Installed From Loop to RSI Sovereign Console V2')
