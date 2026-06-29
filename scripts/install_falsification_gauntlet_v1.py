from pathlib import Path
import json, datetime, re
ROOT=Path('.')
PAGE='falsification-gauntlet.html'
MARK='<!-- GOALOS_FALSIFICATION_GAUNTLET_V1 -->'

def patch_readme():
    p=ROOT/'README.md'
    text=p.read_text(encoding='utf-8') if p.exists() else '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'
    block=f"""\n{MARK}\n\n## GoalOS Falsification Gauntlet V1 — Strong Claims Survive Baselines\n\nNew public demo: [`/falsification-gauntlet.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-gauntlet.html)\n\nThis browser-local page demonstrates that GoalOS claims are not promoted by rhetoric. A claim must survive Evidence Docket checks, baselines, replay, cost/risk ledgers, validator notes, privacy boundaries, delayed-outcome planning, and human review.\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority.\n\n"""
    if MARK not in text:
        text = block + '\n' + text
    p.write_text(text,encoding='utf-8')

def patch_index():
    p=ROOT/'public/index.html'
    if not p.exists(): return
    text=p.read_text(encoding='utf-8')
    if 'falsification-gauntlet.html' in text: return
    card="""\n<section class="goalos-falsification-card" style="max-width:1100px;margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:24px;background:rgba(255,255,255,.06)">\n  <p style="letter-spacing:.22em;color:#ffe98b;font-weight:900;text-transform:uppercase">New public demo</p>\n  <h2 style="font-size:clamp(32px,5vw,64px);margin:.2em 0">Strong claims survive baselines.</h2>\n  <p style="font-size:18px;line-height:1.6;color:#cbd6ee">Run a claim through the GoalOS Falsification Gauntlet: baselines, replay, safety, privacy, cost/risk, delayed outcomes, and human review.</p>\n  <a href="falsification-gauntlet.html" style="display:inline-block;margin-top:12px;padding:13px 18px;border-radius:999px;background:#ffe98b;color:#07111f;font-weight:900;text-decoration:none">Open Falsification Gauntlet</a>\n</section>\n"""
    text=text.replace('</body>',card+'\n</body>') if '</body>' in text else text+card
    p.write_text(text,encoding='utf-8')

def patch_search():
    p=ROOT/'public/search-index.json'
    item={'title':'Falsification Gauntlet','url':'falsification-gauntlet.html','summary':'Strong claims survive baselines: browser-local claim-bound proof demo.'}
    data=[]
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(data,dict): data=data.get('pages',[])
        except Exception: data=[]
    if not any((x.get('url') if isinstance(x,dict) else '')==item['url'] for x in data): data.append(item)
    p.write_text(json.dumps(data,indent=2),encoding='utf-8')

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-gauntlet.html'
    if p.exists(): text=p.read_text(encoding='utf-8')
    else: text='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    if url not in text:
        entry=f'  <url><loc>{url}</loc></url>\n'
        text=text.replace('</urlset>',entry+'</urlset>')
    p.write_text(text,encoding='utf-8')

def main():
    patch_readme(); patch_index(); patch_search(); patch_sitemap()
    (ROOT/'reports').mkdir(exist_ok=True)
    report={'status':'installed','page':'public/falsification-gauntlet.html','installed_at':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z')}
    (ROOT/'reports/falsification-gauntlet-v1-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__': main()
