from pathlib import Path
import json, datetime
ROOT = Path.cwd()
required = [
  'public/capability-compounding-lab.html',
  'public/assets/goalos-capability-compounding-lab-v2.css',
  'public/assets/goalos-capability-compounding-lab-v2.js',
  'docs/demos/CAPABILITY_COMPOUNDING_LAB_V2.md',
  'scripts/goalos_capability_compounding_lab_v2_audit.py'
]
# Patch README with a stable link block.
readme = ROOT / 'README.md'
block = '''\n\n<!-- GOALOS_CAPABILITY_COMPOUNDING_LAB_V2_START -->\n## Capability Compounding Lab V2\n\n**Verified work becomes reusable capability.**\n\nThe public demo at `public/capability-compounding-lab.html` shows how a GoalOS proof cycle becomes Chronicle memory, a reusable Capability Package, and a safer harder-mission path. It is browser-local: no user data, no user funds, no wallet, no transaction, no network call, no production authority, and human review required.\n\n<!-- GOALOS_CAPABILITY_COMPOUNDING_LAB_V2_END -->\n'''
if readme.exists():
    text = readme.read_text(encoding='utf-8')
    start='<!-- GOALOS_CAPABILITY_COMPOUNDING_LAB_V2_START -->'
    end='<!-- GOALOS_CAPABILITY_COMPOUNDING_LAB_V2_END -->'
    if start in text and end in text:
        pre=text.split(start)[0].rstrip()
        post=text.split(end,1)[1].lstrip()
        text=pre+block+'\n'+post
    else:
        text=text.rstrip()+block
    readme.write_text(text, encoding='utf-8')
else:
    readme.write_text('# GoalOS AGIALPHA Ascension\n'+block, encoding='utf-8')
# Patch homepage with a CTA, if present.
idx=ROOT/'public/index.html'
if idx.exists():
    text=idx.read_text(encoding='utf-8')
    marker='<!-- GOALOS_CAPABILITY_COMPOUNDING_LAB_V2_CTA -->'
    snippet=marker+'\n<section class="goalos-inline-cta" style="margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:rgba(255,255,255,.06)"><h2>Capability Compounding Lab V2</h2><p>Verified work becomes reusable capability. Run the browser-local compounding demo: no data, no funds, no wallet, no transaction.</p><p><a href="capability-compounding-lab.html">Open Capability Compounding Lab →</a></p></section>\n'
    if marker not in text:
        text=text.replace('</main>', snippet+'</main>') if '</main>' in text else text+snippet
    idx.write_text(text, encoding='utf-8')
# Search index and sitemap best-effort.
search=ROOT/'public/search-index.json'
entry={'title':'Capability Compounding Lab V2','url':'capability-compounding-lab.html','description':'Verified work becomes reusable capability.'}
try:
    data=json.loads(search.read_text(encoding='utf-8')) if search.exists() else []
    if isinstance(data, list):
        data=[x for x in data if not (isinstance(x,dict) and x.get('url')=='capability-compounding-lab.html')]+[entry]
        search.write_text(json.dumps(data, indent=2), encoding='utf-8')
except Exception:
    search.write_text(json.dumps([entry], indent=2), encoding='utf-8')
sitemap=ROOT/'public/sitemap.xml'
url='<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/capability-compounding-lab.html</loc></url>'
if sitemap.exists():
    s=sitemap.read_text(encoding='utf-8')
    if 'capability-compounding-lab.html' not in s:
        s=s.replace('</urlset>', url+'</urlset>') if '</urlset>' in s else s+'\n'+url
    sitemap.write_text(s, encoding='utf-8')
else:
    sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+url+'</urlset>', encoding='utf-8')
(ROOT/'.nojekyll').write_text('', encoding='utf-8')
report={'status':'installed','version':'v2','generated_at':datetime.datetime.now(datetime.UTC).isoformat(),'required_files':required}
Path('reports').mkdir(exist_ok=True)
Path('reports/capability-compounding-lab-v2-install-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
