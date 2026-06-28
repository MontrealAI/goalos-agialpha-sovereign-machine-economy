#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT = Path('.')
PUBLIC = ROOT / 'public'

def patch_readme():
    p = ROOT / 'README.md'
    section = '''\n\n## Evidence Docket Theatre V2 — A proof page is not a marketing page\n\nGoalOS now includes a browser-local Evidence Docket Theatre at [`/evidence-docket-theatre.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evidence-docket-theatre.html). It lets visitors convert a public-safe claim into a review-ready proof room: claims matrix, baselines, proof packets, evaluator notes, risk/cost ledgers, replay path, governed decision state, and reusable capability package.\n\nBoundary: no user data, no user funds, no wallet, no transaction, no external action, and human review remains required.\n'''
    if p.exists():
        s = p.read_text(encoding='utf-8')
        if 'Evidence Docket Theatre V2' not in s:
            p.write_text(s.rstrip()+section+'\n', encoding='utf-8')

def patch_index():
    p = PUBLIC / 'index.html'
    if not p.exists(): return
    s = p.read_text(encoding='utf-8')
    if 'evidence-docket-theatre.html' in s: return
    block = '''\n<section class="v4-section" id="evidence-docket-theatre-link">\n  <p class="eyebrow"><span></span>NEW PUBLIC DEMO</p>\n  <h2>Evidence Docket Theatre</h2>\n  <p>A proof page is not a marketing page. Convert a public-safe claim into a review-ready Evidence Docket: claims matrix, baselines, proof packets, evaluator notes, risk/cost ledgers, replay path, governed decision state, and capability package.</p>\n  <p><a class="button primary" href="evidence-docket-theatre.html">Open the Evidence Docket Theatre</a></p>\n</section>\n'''
    if '</main>' in s:
        s=s.replace('</main>', block+'</main>',1)
    else:
        s += block
    p.write_text(s, encoding='utf-8')

def patch_json(path, entry):
    p=ROOT/path
    data=[]
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(data, dict):
                data=data.get('pages', [])
        except Exception:
            data=[]
    if not any(x.get('url')==entry['url'] for x in data if isinstance(x,dict)):
        data.append(entry)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')

def patch_sitemap():
    p=PUBLIC/'sitemap.xml'
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evidence-docket-theatre.html'
    if p.exists():
        s=p.read_text(encoding='utf-8')
        if url not in s:
            s=s.replace('</urlset>', f'  <url><loc>{url}</loc></url>\n</urlset>') if '</urlset>' in s else s+f'\n{url}\n'
    else:
        s=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n'
    p.write_text(s, encoding='utf-8')

def main():
    patch_readme(); patch_index(); patch_json('public/search-index.json', {'title':'Evidence Docket Theatre','url':'evidence-docket-theatre.html','description':'A browser-local proof room that turns public-safe claims into review-ready Evidence Dockets.'}); patch_sitemap(); (ROOT/'.nojekyll').write_text('', encoding='utf-8')
    report={'status':'passed','installed_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','page':'public/evidence-docket-theatre.html','browser_local':True,'no_user_data':True,'no_user_funds':True,'human_review_required':True}
    (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/evidence-docket-theatre-v2-install-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()
