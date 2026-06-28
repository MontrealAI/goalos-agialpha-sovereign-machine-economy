from pathlib import Path
import json, datetime
root=Path.cwd()
(root/'reports').mkdir(exist_ok=True)
# Patch README with a stable section.
readme=root/'README.md'
section='''\n\n## Capability Compounding Lab\n\n**Verified work becomes reusable capability.**\n\nThe browser-local Capability Compounding Lab demonstrates the GoalOS compounding loop:\n\n```text\nMission → Work → Proof → Validation → Chronicle → Capability Package → Harder Mission\n```\n\nOpen: [`capability-compounding-lab.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/capability-compounding-lab.html)\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n'''
if readme.exists():
    txt=readme.read_text(encoding='utf-8')
    if '## Capability Compounding Lab' not in txt:
        readme.write_text(txt.rstrip()+section+'\n',encoding='utf-8')
# Patch homepage with a link card.
idx=root/'public/index.html'
card='''\n<section class="ux-card" style="margin:32px auto;max-width:1120px;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:rgba(255,255,255,.06)">\n  <p style="letter-spacing:.2em;text-transform:uppercase;color:#ffdf77;font-weight:900">New public demo</p>\n  <h2>Capability Compounding Lab</h2>\n  <p>Run the browser-local loop where verified work becomes Chronicle memory, reusable capability, and a harder future mission.</p>\n  <p><a href="capability-compounding-lab.html">Open Capability Compounding Lab →</a></p>\n</section>\n'''
if idx.exists():
    html=idx.read_text(encoding='utf-8')
    if 'capability-compounding-lab.html' not in html:
        if '</main>' in html:
            html=html.replace('</main>',card+'</main>',1)
        elif '</body>' in html:
            html=html.replace('</body>',card+'</body>',1)
        else:
            html+=card
        idx.write_text(html,encoding='utf-8')
# Patch search index.
search=root/'public/search-index.json'
entry={"title":"Capability Compounding Lab","url":"capability-compounding-lab.html","description":"Browser-local demo showing verified work becoming reusable capability."}
if search.exists():
    try:
        data=json.loads(search.read_text(encoding='utf-8'))
        if isinstance(data,list) and not any(x.get('url')==entry['url'] for x in data):
            data.append(entry); search.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    except Exception:
        pass
# Patch sitemap.
sitemap=root/'public/sitemap.xml'
url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/capability-compounding-lab.html'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    if 'capability-compounding-lab.html' not in sm:
        if '</urlset>' in sm:
            sm=sm.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>')
        else:
            sm += f'\n<url><loc>{url}</loc></url>\n'
        sitemap.write_text(sm,encoding='utf-8')
(root/'.nojekyll').write_text('',encoding='utf-8')
manifest={'schema':'goalos.capability_compounding_lab.v1.install','generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','status':'passed','page':'public/capability-compounding-lab.html'}
(root/'reports/capability-compounding-lab-v1-install-report.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Capability Compounding Lab V1 installed')
