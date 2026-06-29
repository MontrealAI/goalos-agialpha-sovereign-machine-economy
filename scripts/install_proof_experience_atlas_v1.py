from pathlib import Path
import json, datetime
ROOT=Path.cwd()

def insert_once(path, marker, block):
    p=ROOT/path
    if not p.exists(): return False
    s=p.read_text(encoding='utf-8')
    if marker in s: return False
    if '</body>' in s:
        s=s.replace('</body>', block+'\n</body>')
    else:
        s+='\n'+block+'\n'
    p.write_text(s,encoding='utf-8')
    return True

def patch_readme():
    p=ROOT/'README.md'
    block="""

## Proof Experience Atlas

The public website now includes the **Proof Experience Atlas**: a unified, browser-local path through the best GoalOS demonstrations.

Start here: [`/proof-experience-atlas.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-experience-atlas.html)

It maps: Multi-Agent Institution → Proof Gradient Lab → Evidence Docket Theatre → Proof-to-Action Command Room → Capability Compounding Lab → Sovereign Experience Stream Lab → Proof-Settlement Chronicle Lab → Falsification Gauntlet → Proof Run 001 Execution Room.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
"""
    if p.exists():
        s=p.read_text(encoding='utf-8')
        if '## Proof Experience Atlas' not in s:
            p.write_text(block+'\n'+s,encoding='utf-8')
    else:
        p.write_text('# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'+block,encoding='utf-8')

def patch_index():
    block="""
<section class="goalos-proof-experience-atlas-link" style="max-width:1120px;margin:48px auto;padding:32px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:linear-gradient(135deg,rgba(105,255,210,.12),rgba(157,136,255,.12));color:#fff;">
  <p style="letter-spacing:.32em;text-transform:uppercase;color:#ffe879;font-weight:900;">Unified public demo path</p>
  <h2 style="font-size:clamp(34px,5vw,68px);line-height:.95;margin:8px 0;">Proof Experience Atlas</h2>
  <p style="font-size:20px;line-height:1.45;max-width:860px;">Run the best GoalOS public demonstrations as one coherent browser-local proof journey: no data, no funds, no wallet, no transaction, human review required.</p>
  <a href="proof-experience-atlas.html" style="display:inline-block;margin-top:12px;padding:14px 20px;border-radius:999px;background:#ffe879;color:#061014;text-decoration:none;font-weight:900;">Open the Atlas</a>
</section>
"""
    insert_once(Path('public/index.html'),'goalos-proof-experience-atlas-link',block)

def patch_search():
    p=ROOT/'public/search-index.json'
    item={'title':'Proof Experience Atlas','url':'proof-experience-atlas.html','description':'Unified browser-local path through the best GoalOS public demos.'}
    data=[]
    if p.exists():
        try: data=json.loads(p.read_text(encoding='utf-8'))
        except Exception: data=[]
    if isinstance(data,dict): data=data.get('pages',[])
    if not any(isinstance(x,dict) and x.get('url')==item['url'] for x in data):
        data.append(item)
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,indent=2),encoding='utf-8')

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-experience-atlas.html'
    if p.exists():
        s=p.read_text(encoding='utf-8')
        if url not in s:
            if '</urlset>' in s:
                s=s.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>')
            else: s += f'\n{url}\n'
        p.write_text(s,encoding='utf-8')
    else:
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n',encoding='utf-8')

def write_report():
    reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
    report={'status':'installed','page':'public/proof-experience-atlas.html','installed_at':datetime.datetime.now(datetime.UTC).isoformat(),'boundary':{'no_user_data':True,'no_user_funds':True,'no_wallet':True,'no_transaction':True,'human_review_required':True}}
    (reports/'proof-experience-atlas-v1-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

patch_readme(); patch_index(); patch_search(); patch_sitemap(); (ROOT/'.nojekyll').write_text('',encoding='utf-8'); write_report()
print('GoalOS Proof Experience Atlas V1 installed')
