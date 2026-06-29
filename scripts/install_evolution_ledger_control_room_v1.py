from pathlib import Path
import json, datetime, re
ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
FILES = [
 "public/evolution-ledger-control-room.html",
 "public/assets/goalos-evolution-ledger-room-v1.css",
 "public/assets/goalos-evolution-ledger-room-v1.js",
 "docs/demos/EVOLUTION_LEDGER_CONTROL_ROOM_V1.md",
 "docs/reviewer/HOW_TO_REVIEW_EVOLUTION_LEDGER_CONTROL_ROOM.md",
 "examples/evolution-ledger/public-safe-ledger-scenarios.md",
 "content/goalos/evolution-ledger-control-room-v1.json",
 ".github/ISSUE_TEMPLATE/evolution_ledger_control_room_feedback.yml",
 "issue-bodies/evolution-ledger-control-room-v1.md"
]
for d in ["reports","evidence/demo","public","content/goalos"]:
    (ROOT/d).mkdir(parents=True, exist_ok=True)
# homepage patch
index = ROOT/"public/index.html"
card = """\n<section class="goalos-ledger-room-card" style="margin:40px auto;padding:28px;border:1px solid rgba(255,255,255,.18);border-radius:24px;background:rgba(255,255,255,.06);max-width:1120px">\n  <p style="letter-spacing:.28em;color:#ffed79;font-weight:900">NEW PUBLIC DEMO</p>\n  <h2 style="font-size:clamp(32px,5vw,64px);line-height:.95;margin:0 0 12px">Evolution Ledger Control Room</h2>\n  <p style="font-size:18px;line-height:1.5;color:#dbe7ff">The ledger remembers proof, not secrets. Run the public proof sequence and see how commitments, attestations, selection, challenge windows, and rollback receipts become reviewable institutional state.</p>\n  <a href="evolution-ledger-control-room.html" style="display:inline-block;margin-top:12px;padding:14px 20px;border-radius:999px;background:#ffed79;color:#07111e;font-weight:900;text-decoration:none">Open Evolution Ledger Room</a>\n</section>\n"""
if index.exists():
    s = index.read_text()
    if 'evolution-ledger-control-room.html' not in s:
        s = s.replace('</body>', card + '\n</body>') if '</body>' in s else s + card
        index.write_text(s)
else:
    index.write_text('<!doctype html><meta charset="utf-8"><title>GoalOS</title><h1>GoalOS</h1><a href="evolution-ledger-control-room.html">Evolution Ledger Control Room</a>')
# README patch
readme = ROOT/"README.md"
block = """\n\n## Evolution Ledger Control Room V1\n\n**The ledger remembers proof, not secrets.**\n\nA browser-local public demo showing the AEP-style sequence: GoalOSCommit → RunRoot → ProofRoot → EvalAttestation → SelectionCertificate → RolloutReceipt → RollbackReceipt.\n\nOpen: `public/evolution-ledger-control-room.html`\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n"""
if readme.exists():
    s = readme.read_text()
    if 'Evolution Ledger Control Room V1' not in s:
        readme.write_text(s + block)
else:
    readme.write_text('# GoalOS AGIALPHA Ascension\n' + block)
# search index patch
search = ROOT/"public/search-index.json"
entry = {"title":"Evolution Ledger Control Room","url":"evolution-ledger-control-room.html","description":"The ledger remembers proof, not secrets. Browser-local public demo of commitments, attestations, selection certificates, challenge windows, and rollback receipts."}
try:
    data = json.loads(search.read_text()) if search.exists() else []
    if isinstance(data, dict) and 'items' in data: items = data['items']; container = data
    elif isinstance(data, list): items = data; container = data
    else: items=[]; container=items
    if not any((x.get('url') if isinstance(x,dict) else '') == entry['url'] for x in items):
        items.append(entry)
    if isinstance(container, dict): container['items'] = items
    search.write_text(json.dumps(container, indent=2))
except Exception:
    search.write_text(json.dumps([entry], indent=2))
# sitemap patch
site = ROOT/"public/sitemap.xml"
url = '<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evolution-ledger-control-room.html</loc></url>'
if site.exists():
    s = site.read_text()
    if 'evolution-ledger-control-room.html' not in s:
        s = s.replace('</urlset>', f'  {url}\n</urlset>') if '</urlset>' in s else s + '\n' + url
        site.write_text(s)
else:
    site.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  '+url+'\n</urlset>\n')
(ROOT/'.nojekyll').write_text('')
report = {"status":"installed","generated_at":NOW,"files":FILES,"page":"public/evolution-ledger-control-room.html","boundary":{"no_user_data":True,"no_user_funds":True,"no_wallet":True,"no_transaction":True,"no_network_call":True,"human_review_required":True}}
(ROOT/'reports/evolution-ledger-control-room-v1-install-report.json').write_text(json.dumps(report, indent=2))
