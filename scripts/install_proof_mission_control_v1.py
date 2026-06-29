from pathlib import Path
import json, datetime
ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(path):
    p = ROOT / path
    return p.read_text(encoding='utf-8') if p.exists() else ''

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def inject_once(path, marker, block):
    text = read(path)
    if not text:
        text = '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n\n'
    if marker not in text:
        if path.lower().endswith('.md'):
            text = text.rstrip() + '\n\n' + marker + '\n' + block.strip() + '\n'
        else:
            text = text.replace('</body>', marker + '\n' + block.strip() + '\n</body>') if '</body>' in text else text.rstrip()+marker+'\n'+block.strip()
    write(path, text)

readme_block = """
## Proof Mission Control V1

GoalOS now includes a public operating board for turning public-safe proof missions into reviewable state.

- [Proof Mission Control](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-control.html)
- [Proof Mission Forge](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-forge.html)
- [Proof Run 001 Execution Room](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-execution-room.html)

Boundary: no user data, no user funds, no wallet, no transaction, no production authority, human review required.
"""
inject_once('README.md','<!-- GOALOS_PROOF_MISSION_CONTROL_V1 -->',readme_block)

home_block = """
<section class="proof-mission-control-entry" style="margin:48px auto;max-width:1120px;padding:28px;border:1px solid rgba(255,255,255,.18);border-radius:26px;background:rgba(255,255,255,.06);color:#f8f4e8">
  <p style="letter-spacing:.22em;text-transform:uppercase;color:#ffe66d;font-weight:900">Proof Mission Control</p>
  <h2 style="font-size:clamp(34px,5vw,72px);line-height:.95;margin:0 0 14px">Turn proof missions into reviewable operating state.</h2>
  <p style="font-size:18px;line-height:1.45;color:#dfe7fb">Mission Control is the bridge from public demo to Proof Run 001: choose a public-safe mission, inspect gates, download a docket, prepare a validator packet, and keep the no-data/no-funds boundary visible.</p>
  <p><a href="proof-mission-control.html" style="display:inline-block;margin-top:12px;padding:12px 16px;border-radius:999px;background:#ffe66d;color:#07101a;font-weight:900;text-decoration:none">Open Proof Mission Control</a></p>
</section>
"""
inject_once('public/index.html','<!-- GOALOS_PROOF_MISSION_CONTROL_V1 -->',home_block)

try:
    idx = json.loads(read('public/search-index.json') or '[]')
    if not isinstance(idx, list): idx = []
except Exception:
    idx = []
entry = {"title":"Proof Mission Control","url":"proof-mission-control.html","description":"Turn public-safe proof missions into reviewable operating state."}
idx = [x for x in idx if isinstance(x, dict) and x.get('url') != entry['url']] + [entry]
write('public/search-index.json', json.dumps(idx, indent=2))

sitemap = read('public/sitemap.xml')
url = 'https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-control.html'
if '<urlset' not in sitemap:
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
if url not in sitemap:
    sitemap = sitemap.replace('</urlset>', f'  <url><loc>{url}</loc></url>\n</urlset>')
write('public/sitemap.xml', sitemap)
write('.nojekyll','')

report = {
  "status":"installed",
  "installed_at": NOW,
  "page":"public/proof-mission-control.html",
  "boundary": {"no_user_data": True, "no_user_funds": True, "no_wallet": True, "no_transaction": True, "human_review_required": True},
  "files": ["public/proof-mission-control.html","docs/proof-missions/PROOF_MISSION_CONTROL_V1.md","reports/proof-mission-control-v1-install-report.json"]
}
write('reports/proof-mission-control-v1-install-report.json', json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
