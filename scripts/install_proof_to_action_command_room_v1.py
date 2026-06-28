from pathlib import Path
import json, datetime
SNIPPET = '''

<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_START -->
<section class="proof-to-action-command-room" style="margin:32px 0;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:linear-gradient(135deg,rgba(98,255,217,.08),rgba(255,224,113,.08));">
  <p style="letter-spacing:.18em;text-transform:uppercase;color:#ffe071;font-weight:900;font-size:12px;margin:0 0 8px;">New public demo</p>
  <h2 style="margin:0 0 10px;font-size:clamp(28px,4vw,54px);line-height:.95;">Proof-to-Action Command Room</h2>
  <p style="max-width:850px;color:#b7c2dc;line-height:1.6;">A browser-local demonstration of the Mission OS loop: Objective → Evidence Docket → Governed Decision State → Action Graph → Chronicle → Capability Package.</p>
  <p><a href="proof-to-action-command-room.html" style="display:inline-block;padding:12px 16px;border-radius:999px;background:#ffe071;color:#07101e;font-weight:900;text-decoration:none;">Open the Command Room</a></p>
</section>
<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_END -->
'''
def patch_text(path: Path, marker: str, snippet: str, fallback: str = ''):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(fallback, encoding='utf-8')
    text = path.read_text(encoding='utf-8')
    start = f'<!-- {marker}_START -->'
    end = f'<!-- {marker}_END -->'
    if start in text and end in text:
        before = text.split(start)[0]
        after = text.split(end)[1]
        path.write_text(before + snippet.strip() + after, encoding='utf-8')
    else:
        if '</main>' in text:
            text = text.replace('</main>', snippet + '\n</main>', 1)
        else:
            text += '\n' + snippet
        path.write_text(text, encoding='utf-8')
def patch_readme():
    p = Path('README.md')
    fallback = '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'
    block = '''
<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_README_START -->
## Proof-to-Action Command Room

The repository now includes a browser-local **Proof-to-Action Command Room**:

- Website: `public/proof-to-action-command-room.html`
- Live page: `/proof-to-action-command-room.html`
- Demo report: `reports/proof-to-action-command-room-v1-demo-run.json`
- QA report: `reports/proof-to-action-command-room-v1-qa.json`

This page demonstrates the Mission OS loop: Objective → Mission Contract → Evidence Docket → Governed Decision State → Action Graph → Chronicle → Capability Package.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, and human review required.
<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_README_END -->
'''
    if not p.exists(): p.write_text(fallback, encoding='utf-8')
    text = p.read_text(encoding='utf-8')
    start = '<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_README_START -->'
    end = '<!-- GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1_README_END -->'
    if start in text and end in text:
        text = text.split(start)[0] + block.strip() + text.split(end)[1]
    else:
        text += '\n\n' + block.strip() + '\n'
    p.write_text(text, encoding='utf-8')
def patch_search():
    p = Path('public/search-index.json')
    data = []
    if p.exists():
        try: data = json.loads(p.read_text(encoding='utf-8'))
        except Exception: data = []
    data = [x for x in data if x.get('url') != 'proof-to-action-command-room.html']
    data.append({'title':'Proof-to-Action Command Room','url':'proof-to-action-command-room.html','description':'Browser-local GoalOS demo: Objective to Evidence Docket to Governed Decision State to Action Graph to Chronicle to Capability Package.','tags':['goalos','mission-os','governed-decision-state','evidence-docket','action-graph','chronicle','capability-package']})
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
def patch_sitemap():
    p = Path('public/sitemap.xml')
    url = '<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-to-action-command-room.html</loc></url>'
    if not p.exists():
        p.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n', encoding='utf-8')
    text = p.read_text(encoding='utf-8')
    if 'proof-to-action-command-room.html' not in text:
        text = text.replace('</urlset>', f'  {url}\n</urlset>')
    p.write_text(text, encoding='utf-8')
patch_text(Path('public/index.html'), 'GOALOS_PROOF_TO_ACTION_COMMAND_ROOM_V1', SNIPPET)
patch_readme()
patch_search()
patch_sitemap()
Path('.nojekyll').write_text('', encoding='utf-8')
manifest = {'status':'installed','generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','page':'public/proof-to-action-command-room.html','browser_local':True,'no_user_data':True,'no_user_funds':True,'human_review_required':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/proof-to-action-command-room-v1-install-report.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print('Installed Proof-to-Action Command Room V1')
