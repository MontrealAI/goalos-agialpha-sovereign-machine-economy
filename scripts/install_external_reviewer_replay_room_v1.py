#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re
ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

def patch_readme():
    p = ROOT/'README.md'
    text = p.read_text(encoding='utf-8') if p.exists() else '# GoalOS AGIALPHA Ascension\n'
    marker = '<!-- GOALOS_EXTERNAL_REVIEWER_REPLAY_ROOM_V1 -->'
    block = f"""\n\n{marker}\n## External Reviewer Replay Room\n\nIndependent review is now a first-class public path. Open the browser-local **External Reviewer Replay Room** to inspect Evidence Dockets, replay checklists, validator notes, baselines, cost/risk ledgers, claim boundaries, and dissent.\n\n- Website: [`/external-reviewer-replay-room.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/external-reviewer-replay-room.html)\n- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n"""
    if marker not in text:
        text += block
    p.write_text(text, encoding='utf-8')

def patch_index():
    p = ROOT/'public/index.html'
    if not p.exists():
        return
    text = p.read_text(encoding='utf-8')
    marker = '<!-- GOALOS_EXTERNAL_REVIEWER_REPLAY_ROOM_V1_CARD -->'
    card = f"""\n{marker}\n<section class="goalos-reviewer-replay-card" style="max-width:1440px;margin:40px auto;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:rgba(255,255,255,.055);color:#fff;">\n  <p style="color:#ffe870;font-weight:900;letter-spacing:.24em;text-transform:uppercase;">Independent review path</p>\n  <h2 style="font-size:clamp(36px,4vw,72px);line-height:.95;margin:0 0 12px;">External Reviewer Replay Room</h2>\n  <p style="font-size:20px;max-width:850px;color:#d8def4;">Make proof inspectable: docket, replay, baselines, validator notes, cost/risk, claim boundary, dissent, and verdict. Browser-local. No data. No funds.</p>\n  <a href="external-reviewer-replay-room.html" style="display:inline-block;margin-top:12px;padding:14px 20px;border-radius:999px;background:#ffe870;color:#07101a;text-decoration:none;font-weight:900;">Open Reviewer Replay Room</a>\n</section>\n"""
    if marker not in text:
        if '</main>' in text:
            text = text.replace('</main>', card + '\n</main>', 1)
        elif '</body>' in text:
            text = text.replace('</body>', card + '\n</body>', 1)
        else:
            text += card
    p.write_text(text, encoding='utf-8')

def patch_search():
    p = ROOT/'public/search-index.json'
    item = {"title":"External Reviewer Replay Room","url":"external-reviewer-replay-room.html","description":"Independent review path for Evidence Dockets, replay, baselines, validator notes, claim boundaries, and dissent."}
    data=[]
    if p.exists():
        try: data=json.loads(p.read_text(encoding='utf-8'))
        except Exception: data=[]
    if isinstance(data, dict): data=data.get('items', [])
    if not any(x.get('url')==item['url'] for x in data if isinstance(x,dict)):
        data.append(item)
    p.write_text(json.dumps(data,indent=2), encoding='utf-8')

def patch_sitemap():
    p = ROOT/'public/sitemap.xml'
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/external-reviewer-replay-room.html'
    if not p.exists():
        p.write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n', encoding='utf-8')
        return
    text=p.read_text(encoding='utf-8')
    if url not in text:
        entry=f'  <url><loc>{url}</loc></url>\n'
        text=text.replace('</urlset>', entry+'</urlset>') if '</urlset>' in text else text+'\n'+entry
    p.write_text(text, encoding='utf-8')

patch_readme(); patch_index(); patch_search(); patch_sitemap()
(ROOT/'.nojekyll').write_text('', encoding='utf-8')
report={"status":"installed","installed_at":NOW,"page":"public/external-reviewer-replay-room.html","boundary":{"no_user_data":True,"no_user_funds":True,"wallet_or_mainnet":False,"human_review_required":True}}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/external-reviewer-replay-room-v1-install-report.json').write_text(json.dumps(report,indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
