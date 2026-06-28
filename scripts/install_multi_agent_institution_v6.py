from pathlib import Path
import json, datetime, re
ROOT = Path('.')
PAGES = [
  'multi-agent-institution.html', 'coordination-console.html', 'evidence-room.html', 'start-here.html',
  'try-goalos.html', 'proof-run-001-live.html', 'no-data-no-funds.html'
]
SECTION = """
<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_START -->

## Multi-Agent Institution Experience V6 — Not a swarm. An institution.

The public website now includes a browser-local, no-data/no-funds interactive Multi-Agent Institution Lab:

- Live page: `public/multi-agent-institution.html`
- Assets: `public/assets/goalos-institution-v6.css`, `public/assets/goalos-institution-v6.js`
- Documentation: `docs/institution/MULTI_AGENT_INSTITUTION_EXPERIENCE_V6.md`
- Audit: `reports/multi-agent-institution-v6-qa.json`

The page lets non-technical and advanced users run a proof flight, compare an unstructured swarm against a proof-governed institution, inspect proof gates, generate a local Evidence Docket, and download a review brief — without model calls, wallets, transactions, backend calls, or user-data submission.

Boundary: no user data, no user funds, no wallet, no transaction, no production authority, human review required.

<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_END -->
"""
def patch_between(text, start, end, block):
    if start in text and end in text:
        return re.sub(re.escape(start)+r'.*?'+re.escape(end), block.strip(), text, flags=re.S)
    return text.rstrip() + "\n\n" + block.strip() + "\n"
readme = ROOT/'README.md'
if readme.exists():
    txt = readme.read_text(encoding='utf-8')
else:
    txt = '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'
readme.write_text(patch_between(txt, '<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_START -->', '<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_END -->', SECTION), encoding='utf-8')
# Patch index with a path card, safely append if no obvious marker.
index = ROOT/'public/index.html'
if index.exists():
    html = index.read_text(encoding='utf-8')
    card = """
<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_CARD_START -->
<section class="section" id="multi-agent-institution-v6" style="position:relative;z-index:2;max-width:1200px;margin:48px auto;padding:0 20px">
  <div style="border:1px solid rgba(255,255,255,.14);border-radius:28px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.035));padding:24px;box-shadow:0 24px 80px rgba(0,0,0,.35)">
    <p style="color:#ffe88b;letter-spacing:.28em;text-transform:uppercase;font-size:12px;font-weight:900">New interactive institution lab</p>
    <h2 style="font-size:clamp(34px,5vw,74px);line-height:.9;letter-spacing:-.06em;margin:0 0 12px;color:#f8f4ea">Not a swarm. An institution.</h2>
    <p style="max-width:860px;color:#bdc8e6;font-size:18px;line-height:1.65">Run the browser-local Multi-Agent Institution Lab: compare raw swarms with proof-governed institutions, inspect proof gates, generate an Evidence Docket, and download a review brief. No user data. No funds. No wallet. Human review required.</p>
    <p><a href="multi-agent-institution.html" style="display:inline-block;background:linear-gradient(135deg,#fff0a8,#ffcd5b);color:#07101e;font-weight:900;padding:13px 18px;border-radius:999px;text-decoration:none">Launch the Institution Lab</a></p>
  </div>
</section>
<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_CARD_END -->
"""
    html = patch_between(html, '<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_CARD_START -->', '<!-- GOALOS_MULTI_AGENT_INSTITUTION_V6_CARD_END -->', card)
    index.write_text(html, encoding='utf-8')
# Search index
search_path = ROOT/'public/search-index.json'
items = []
if search_path.exists():
    try:
        items = json.loads(search_path.read_text(encoding='utf-8'))
        if not isinstance(items, list): items = []
    except Exception: items = []
entry = {'title':'Multi-Agent Institution Lab','url':'multi-agent-institution.html','description':'Browser-local proof-governed multi-agent institution simulator with Evidence Docket download.'}
items = [i for i in items if i.get('url') != entry['url']] + [entry]
search_path.write_text(json.dumps(items, indent=2) + '\n', encoding='utf-8')
# Sitemap
sitemap = ROOT/'public/sitemap.xml'
urls = ['index.html','multi-agent-institution.html','coordination-console.html','evidence-room.html','start-here.html','try-goalos.html','proof-run-001-live.html','no-data-no-funds.html']
base = 'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
sitemap.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join([f'  <url><loc>{base}{u}</loc></url>\n' for u in urls]) + '</urlset>\n', encoding='utf-8')
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/multi-agent-institution-v6-install-report.json').write_text(json.dumps({'status':'installed','generated_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'page':'public/multi-agent-institution.html','browser_local':True,'no_user_data':True,'no_user_funds':True}, indent=2)+'\n', encoding='utf-8')
print('GoalOS Multi-Agent Institution V6 installed')
