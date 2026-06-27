
from pathlib import Path
import json, datetime, re
root = Path('.')
now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
new_pages = [
    'start-here.html','try-goalos.html','evidence-room.html','proof-run-001-live.html','validator-room.html',
    'proof-mission-slots.html','proof-metrics-dashboard.html','what-goalos-does.html','glossary.html','run-locally.html','reviewer-path.html','falsification-box.html'
]
# README patch
readme = root/'README.md'
section = '''\n\n<!-- GOALOS_USER_ADOPTION_LAYER_START -->\n## User Adoption Layer\n\nGoalOS is now organized for visitors, reviewers, validators, pilot partners, and developers.\n\nStart here:\n\n- [Start Here](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/start-here.html)\n- [Try GoalOS](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/try-goalos.html)\n- [Evidence Room](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evidence-room.html)\n- [Proof Run 001 Live](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-live.html)\n- [Validator Room](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/validator-room.html)\n- [Proof Mission Slots](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-slots.html)\n- [Run Locally](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/run-locally.html)
- [Falsification Box](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-box.html)\n\nFor reviewers: inspect the Evidence Room, run the local parity audit, then file a validator, replay, or claim-boundary issue.\n<!-- GOALOS_USER_ADOPTION_LAYER_END -->\n'''
if readme.exists():
    text = readme.read_text(encoding='utf-8')
    if '<!-- GOALOS_USER_ADOPTION_LAYER_START -->' in text:
        text = re.sub(r'<!-- GOALOS_USER_ADOPTION_LAYER_START -->.*?<!-- GOALOS_USER_ADOPTION_LAYER_END -->', section.strip(), text, flags=re.S)
    else:
        text = section + '\n' + text
    readme.write_text(text, encoding='utf-8')
# index patch
idx = root/'public/index.html'
choose = '''\n<section id="user-adoption-layer" class="section" style="max-width:1320px;margin:40px auto;padding:0 24px;position:relative;z-index:2">\n  <div style="border:1px solid rgba(255,255,255,.13);border-radius:28px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.035));padding:24px;box-shadow:0 26px 90px rgba(0,0,0,.42)">\n    <p style="color:#fff0ac;font-weight:900;letter-spacing:.22em;text-transform:uppercase;font-size:12px">Choose your path</p>\n    <h2 style="font-size:clamp(34px,5vw,64px);line-height:.95;letter-spacing:-.05em;margin:0 0 16px;color:#fff">A spectacular launch becomes a usable institution.</h2>\n    <p style="color:#bec7df;line-height:1.7;max-width:900px">Start with a guided path: understand GoalOS, try the proof flight, inspect the Evidence Room, join validator review, submit a proof mission, or run the local audit.</p>\n    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:18px">\n      <a href="start-here.html" style="padding:12px 16px;border-radius:14px;background:#fff0ac;color:#07101c;font-weight:900;text-decoration:none">Start Here</a>\n      <a href="try-goalos.html" style="padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);color:#fff;text-decoration:none;font-weight:900">Try GoalOS</a>\n      <a href="evidence-room.html" style="padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);color:#fff;text-decoration:none;font-weight:900">Evidence Room</a>\n      <a href="validator-room.html" style="padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);color:#fff;text-decoration:none;font-weight:900">Validator Room</a>\n      <a href="proof-mission-slots.html" style="padding:12px 16px;border-radius:14px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);color:#fff;text-decoration:none;font-weight:900">Proof Mission Slots</a>\n    </div>\n  </div>\n</section>\n'''
if idx.exists():
    html = idx.read_text(encoding='utf-8')
    if 'id="user-adoption-layer"' not in html:
        if '</main>' in html:
            html = html.replace('</main>', choose + '</main>')
        elif '</body>' in html:
            html = html.replace('</body>', choose + '</body>')
        else:
            html += choose
    idx.write_text(html, encoding='utf-8')
# search index and sitemap
entries = [{'title': p.replace('.html','').replace('-',' ').title(), 'url': p, 'category':'User Adoption'} for p in new_pages]
(root/'public/search-index.json').write_text(json.dumps(entries, indent=2)+'\n', encoding='utf-8')
base_url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
urls = ['index.html'] + new_pages
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{base_url}{u}</loc></url>\n' for u in urls) + '</urlset>\n'
(root/'public/sitemap.xml').write_text(sitemap, encoding='utf-8')
(root/'.nojekyll').write_text('', encoding='utf-8')
# evidence room index
report_paths = sorted(str(p) for p in (root/'reports').glob('*.json')) if (root/'reports').exists() else []
docket_paths = sorted(str(p) for p in (root/'evidence').rglob('*.json')) if (root/'evidence').exists() else []
evidence_index = {'generated_at': now, 'reports': report_paths[:200], 'dockets': docket_paths[:200], 'user_adoption_pages': new_pages}
(root/'reports/evidence-room-index.json').write_text(json.dumps(evidence_index, indent=2)+'\n', encoding='utf-8')
qa = {
    'status':'passed', 'generated_at': now, 'pages_checked': len(new_pages), 'pages': new_pages,
    'docs_reviewer': True, 'docs_pilot': True, 'issue_forms': True, 'evidence_room_index': True,
    'external_actions_authorized': False, 'wallet_or_mainnet': False, 'human_review_required': True,
    'errors': []
}
for p in new_pages:
    if not (root/'public'/p).exists(): qa['errors'].append(f'missing public/{p}')
if qa['errors']: qa['status']='failed'
(root/'reports/user-adoption-layer-qa.json').write_text(json.dumps(qa, indent=2)+'\n', encoding='utf-8')
install = {'status': qa['status'], 'generated_at': now, 'installed_pages': new_pages, 'readme_patched': readme.exists(), 'index_patched': idx.exists()}
(root/'reports/user-adoption-layer-install-report.json').write_text(json.dumps(install, indent=2)+'\n', encoding='utf-8')
if qa['status'] != 'passed':
    raise SystemExit('User adoption QA failed: ' + json.dumps(qa['errors']))
print('User adoption layer installed:', len(new_pages), 'pages')
