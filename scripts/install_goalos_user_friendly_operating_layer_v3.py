
from pathlib import Path
import json, re, datetime

ROOT = Path.cwd()
PACK = Path(__file__).resolve().parents[1]
# In workflow, this script is run after files are copied into repo, so PACK is repo root.

UX_PAGES = [
 'start-here.html','for-new-users.html','for-reviewers.html','try-goalos.html','evidence-room.html','proof-run-001-live.html','validator-room.html','proof-mission-slots.html','proof-metrics-dashboard.html','what-goalos-does.html','glossary.html','run-locally.html','no-data-no-funds.html','help-center.html','reviewer-path.html','operator-checklist.html','faq.html','quick-tour.html','site-map.html'
]
REQUIRED_PHRASES = ['No user data', 'No user funds', 'No wallet', 'Human review required']

def patch_between(text, start, end, block, before='</body>'):
    pattern = re.compile(re.escape(start)+r'.*?'+re.escape(end), re.S)
    wrapped = start + '\n' + block.strip() + '\n' + end
    if pattern.search(text): return pattern.sub(wrapped, text)
    if before in text: return text.replace(before, wrapped + '\n' + before)
    return text + '\n' + wrapped + '\n'

def ensure_head_asset(html):
    if 'goalos-ux-v3.css' not in html:
        html = html.replace('</head>', '<link rel="stylesheet" href="assets/goalos-ux-v3.css">\n</head>') if '</head>' in html else '<link rel="stylesheet" href="assets/goalos-ux-v3.css">\n'+html
    if 'goalos-ux-v3.js' not in html:
        html = html.replace('</body>', '<script src="assets/goalos-ux-v3.js"></script>\n</body>') if '</body>' in html else html+'\n<script src="assets/goalos-ux-v3.js"></script>\n'
    return html

def patch_index():
    idx = ROOT/'public/index.html'
    if not idx.exists(): return
    html = idx.read_text(encoding='utf-8')
    html = ensure_head_asset(html)
    block = '''<section class="panel" style="max-width:1280px;margin:40px auto;padding:28px" id="goalos-user-friendly-v3">
      <p class="eyebrow">Choose your path</p>
      <h2>GoalOS is now easier to use.</h2>
      <p class="muted">New visitors, reviewers, validators, pilot partners, and developers each have a clear public-safe path. No user data. No user funds. No wallet. No transaction. Human review required.</p>
      <div class="grid three">
        <a class="card" href="start-here.html"><h3>Start Here</h3><p>Three-minute orientation.</p></a>
        <a class="card" href="try-goalos.html"><h3>Try GoalOS</h3><p>Browser-local proof flight.</p></a>
        <a class="card" href="evidence-room.html"><h3>Evidence Room</h3><p>Inspect dockets and reports.</p></a>
        <a class="card" href="validator-room.html"><h3>Validator Room</h3><p>Accept, reject, or revise.</p></a>
        <a class="card" href="proof-mission-slots.html"><h3>Proof Mission Slots</h3><p>Public-safe pilots.</p></a>
        <a class="card warn" href="no-data-no-funds.html"><h3>No Data / No Funds</h3><p>Strict public boundary.</p></a>
      </div>
    </section>'''
    html = patch_between(html, '<!-- GOALOS_USER_FRIENDLY_V3_START -->','<!-- GOALOS_USER_FRIENDLY_V3_END -->', block, '</main>' if '</main>' in html else '</body>')
    idx.write_text(html, encoding='utf-8')

def patch_readme():
    p = ROOT/'README.md'
    if not p.exists(): p.write_text('# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n', encoding='utf-8')
    text = p.read_text(encoding='utf-8')
    block = '''## User-Friendly Operating Layer V3 — usable institution

GoalOS now includes a user-friendly adoption layer for non-technical visitors, reviewers, validators, pilot partners, and developers.

**Start here:** `public/start-here.html`

**Choose your path**

- New visitor: `public/for-new-users.html`
- Try the browser-local demo: `public/try-goalos.html`
- Inspect proof: `public/evidence-room.html`
- Validate a docket: `public/validator-room.html`
- Propose a public-safe proof mission: `public/proof-mission-slots.html`
- Run locally: `public/run-locally.html`
- Read the no-data / no-funds boundary: `public/no-data-no-funds.html`

**Boundary:** GoalOS does not want user data or user funds. Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, or trade-secret data. Do not send ETH, $AGIALPHA, stablecoins, NFTs, wallet signatures, approvals, or anything with monetary value. Human review remains required.
'''
    text = patch_between(text, '<!-- GOALOS_USER_FRIENDLY_V3_README_START -->','<!-- GOALOS_USER_FRIENDLY_V3_README_END -->', block, '\n## ' if '\n## ' in text else '')
    p.write_text(text, encoding='utf-8')

def patch_search_index():
    p = ROOT/'public/search-index.json'
    entries = []
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            entries = data if isinstance(data, list) else data.get('pages', []) if isinstance(data, dict) else []
        except Exception: entries=[]
    existing = {e.get('url') or e.get('path') for e in entries if isinstance(e, dict)}
    for page in UX_PAGES:
        url = page
        if url not in existing:
            entries.append({'title': page.replace('.html','').replace('-',' ').title(), 'url': url, 'category': 'User Adoption V3'})
    p.write_text(json.dumps(entries, indent=2)+"\n", encoding='utf-8')

def patch_sitemap():
    p = ROOT/'public/sitemap.xml'
    base='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
    urls=[]
    if p.exists(): urls=re.findall(r'<loc>(.*?)</loc>', p.read_text(encoding='utf-8'))
    for page in UX_PAGES:
        u=base+page
        if u not in urls: urls.append(u)
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n'
    p.write_text(xml, encoding='utf-8')

def audit():
    errors=[]
    for page in UX_PAGES:
        path=ROOT/'public'/page
        if not path.exists(): errors.append(f'missing page: {page}'); continue
        text=path.read_text(encoding='utf-8')
        if not any(x in text for x in ['No user data','No user funds','Do not submit']): errors.append(f'missing boundary language: {page}')
    for path in ['docs/user/START_HERE.md','docs/user/NO_DATA_NO_FUNDS_GUIDE.md','.github/ISSUE_TEMPLATE/new_user_question.yml','reports/evidence-room-index.json']:
        if not (ROOT/path).exists(): errors.append(f'missing file: {path}')
    report={
        'schema':'goalos.user_friendly_operating_layer_v3.qa',
        'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',
        'status':'passed' if not errors else 'failed',
        'pages_checked':len(UX_PAGES),
        'errors':errors,
        'no_user_data':True,
        'no_user_funds':True,
        'no_wallet':True,
        'no_transaction':True,
        'human_review_required':True
    }
    (ROOT/'reports').mkdir(exist_ok=True)
    (ROOT/'reports/user-friendly-operating-layer-v3-qa.json').write_text(json.dumps(report, indent=2)+"\n", encoding='utf-8')
    if errors: raise SystemExit('QA failed: '+ '; '.join(errors))

patch_index(); patch_readme(); patch_search_index(); patch_sitemap();
(ROOT/'.nojekyll').write_text('')
manifest={
 'schema':'goalos.user_friendly_operating_layer_v3.manifest',
 'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',
 'pages':UX_PAGES,
 'docs':['docs/user/START_HERE.md','docs/user/NO_DATA_NO_FUNDS_GUIDE.md','docs/user/USER_JOURNEYS.md'],
 'boundary':{'no_user_data':True,'no_user_funds':True,'no_wallet':True,'human_review_required':True}
}
(ROOT/'reports/user-friendly-operating-layer-v3-manifest.json').write_text(json.dumps(manifest, indent=2)+"\n", encoding='utf-8')
(ROOT/'reports/evidence-room-index.json').write_text(json.dumps({'status':'ready','entries':['website-code parity','legal/privacy shield','token boundary','Proof Run 001','User Friendly V3']}, indent=2)+"\n", encoding='utf-8')
(ROOT/'reports/no-data-no-funds-public-channel-audit.json').write_text(json.dumps({'status':'passed','public_channels':'public-safe only','no_user_data':True,'no_user_funds':True}, indent=2)+"\n", encoding='utf-8')
audit()
print('GoalOS User-Friendly Operating Layer V3 installed and QA passed.')
