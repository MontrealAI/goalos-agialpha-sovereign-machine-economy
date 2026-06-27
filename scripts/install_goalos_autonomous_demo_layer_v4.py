
from pathlib import Path
import json, re, datetime
ROOT=Path.cwd()
DEMO_PAGES=['demo-launcher.html','proof-flight-demo.html','docket-builder.html','agent-constellation-demo.html','proof-card-studio.html','local-autopilot-demo.html','demo-gallery.html','demo-safety.html']

def patch_between(text,start,end,block,before='</body>'):
    pattern=re.compile(re.escape(start)+r'.*?'+re.escape(end),re.S)
    wrapped=start+'\n'+block.strip()+'\n'+end
    if pattern.search(text): return pattern.sub(wrapped,text)
    if before and before in text: return text.replace(before,wrapped+'\n'+before)
    return text+'\n'+wrapped+'\n'

def patch_index():
    p=ROOT/'public/index.html'
    if not p.exists(): return
    html=p.read_text(encoding='utf-8')
    if 'goalos-demo-v4.css' not in html:
        html=html.replace('</head>','<link rel="stylesheet" href="assets/goalos-demo-v4.css">\n</head>') if '</head>' in html else html
    if 'goalos-demo-v4.js' not in html:
        html=html.replace('</body>','<script src="assets/goalos-demo-v4.js"></script>\n</body>') if '</body>' in html else html
    block='''<section class="panel" id="goalos-autonomous-demo-v4" style="max-width:1280px;margin:42px auto;padding:28px">
      <p class="eyebrow">Autonomous demos</p>
      <h2>Run GoalOS yourself.</h2>
      <p class="muted">Users can run the additions directly: proof flight, Evidence Docket builder, agent constellation demo, proof card studio, and local autopilot demo. Browser-local. No user data. No user funds. No wallet. No network call. Human review required.</p>
      <div class="grid three">
        <a class="card" href="demo-launcher.html"><h3>Demo Launcher</h3><p>One-click path to every autonomous demo.</p></a>
        <a class="card" href="proof-flight-demo.html"><h3>Proof Flight</h3><p>Run gates and download a docket.</p></a>
        <a class="card" href="docket-builder.html"><h3>Docket Builder</h3><p>Create public-safe sample dockets.</p></a>
        <a class="card" href="agent-constellation-demo.html"><h3>Constellation</h3><p>Watch proof-gated routing.</p></a>
        <a class="card" href="proof-card-studio.html"><h3>Proof Card</h3><p>Download a local SVG.</p></a>
        <a class="card" href="local-autopilot-demo.html"><h3>Run Locally</h3><p>Generate demo artifacts from scripts.</p></a>
      </div>
    </section>'''
    html=patch_between(html,'<!-- GOALOS_AUTONOMOUS_DEMO_V4_START -->','<!-- GOALOS_AUTONOMOUS_DEMO_V4_END -->',block,'</main>' if '</main>' in html else '</body>')
    p.write_text(html,encoding='utf-8')

def patch_readme():
    p=ROOT/'README.md'
    if not p.exists(): p.write_text('# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n',encoding='utf-8')
    text=p.read_text(encoding='utf-8')
    block='''## Autonomous Demo Layer V4 — self-run user delight

Users can now run the additions autonomously from the website:

- `public/demo-launcher.html` — one-click launcher
- `public/proof-flight-demo.html` — animated proof gates + docket download
- `public/docket-builder.html` — public-safe Evidence Docket builder
- `public/agent-constellation-demo.html` — proof-gated multi-agent routing demo
- `public/proof-card-studio.html` — local SVG proof-card generator
- `public/local-autopilot-demo.html` — copyable local commands

Boundary: browser-local demos; no user data; no user funds; no wallet; no transaction; no network call; no production authority; human review required.
'''
    text=patch_between(text,'<!-- GOALOS_AUTONOMOUS_DEMO_V4_README_START -->','<!-- GOALOS_AUTONOMOUS_DEMO_V4_README_END -->',block,'\n## ' if '\n## ' in text else '')
    p.write_text(text,encoding='utf-8')

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'; base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
    urls=[]
    if p.exists(): urls=re.findall(r'<loc>(.*?)</loc>',p.read_text(encoding='utf-8'))
    for page in DEMO_PAGES:
        u=base+page
        if u not in urls: urls.append(u)
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls)+'</urlset>\n'
    p.write_text(xml,encoding='utf-8')

def patch_search():
    p=ROOT/'public/search-index.json'; entries=[]
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            entries=data if isinstance(data,list) else data.get('pages',[]) if isinstance(data,dict) else []
        except Exception: entries=[]
    existing={e.get('url') or e.get('path') for e in entries if isinstance(e,dict)}
    for page in DEMO_PAGES:
        if page not in existing: entries.append({'title':page.replace('.html','').replace('-',' ').title(),'url':page,'category':'Autonomous Demos V4'})
    p.write_text(json.dumps(entries,indent=2)+'\n',encoding='utf-8')

patch_index(); patch_readme(); patch_sitemap(); patch_search(); (ROOT/'.nojekyll').write_text('')
# Ensure demo pack exists before audit
import sys
sys.path.insert(0,str((ROOT/'src').resolve()))
from goalos_ascension.demo_runner import write_demo_pack
write_demo_pack()
# Run audit
ns={}
exec((ROOT/'scripts/goalos_autonomous_demo_audit.py').read_text(encoding='utf-8'),ns)
manifest={'schema':'goalos.autonomous_demo_layer_v4.install','status':'passed','pages':DEMO_PAGES,'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'}
(ROOT/'reports/autonomous-demo-layer-v4-install-report.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('GoalOS Autonomous Demo Layer V4 installed.')
