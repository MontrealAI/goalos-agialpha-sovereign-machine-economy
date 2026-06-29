from pathlib import Path
import json, re
ROOT=Path('.')

def upsert(path, text):
    p=ROOT/path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def patch_readme():
    p=ROOT/'README.md'
    text=p.read_text(encoding='utf-8') if p.exists() else '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'
    marker='<!-- GOALOS:FALSIFICATION_GAUNTLET_V1_1 -->'
    block=f'''
{marker}

## Falsification Gauntlet V1.1 — user-feedback hotfix

The public Falsification Gauntlet now preserves custom edited claims during stress tests and visibly changes readiness, baselines, falsifiers, and Governed Decision State.

- Live page: [`/falsification-gauntlet.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-gauntlet.html)
- Boundary: browser-local, no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
- Rule: strong claims survive baselines, replay, privacy, safety, cost/risk, delayed-outcome, and human-review gates.

<!-- /GOALOS:FALSIFICATION_GAUNTLET_V1_1 -->
'''
    if marker in text:
        text=re.sub(r'<!-- GOALOS:FALSIFICATION_GAUNTLET_V1_1 -->.*?<!-- /GOALOS:FALSIFICATION_GAUNTLET_V1_1 -->', block.strip(), text, flags=re.S)
    else:
        text += '\n' + block
    p.write_text(text, encoding='utf-8')

def patch_index():
    p=ROOT/'public/index.html'
    if not p.exists(): return
    text=p.read_text(encoding='utf-8')
    marker='GOALOS:FALSIFICATION_GAUNTLET_V1_1_CARD'
    if marker in text: return
    card=f'''\n<section class="proof-demo-card" data-goalos="{marker}" style="max-width:1200px;margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.16);border-radius:24px;background:rgba(255,255,255,.055)">\n  <p style="color:#ffe98b;letter-spacing:.22em;text-transform:uppercase;font-weight:900">User-feedback fix / browser-local</p>\n  <h2 style="font-size:clamp(32px,4vw,58px);margin:.1em 0">Falsification Gauntlet V1.1</h2>\n  <p style="font-size:18px;line-height:1.6;color:#cbd6ee">Stress tests now preserve custom claims and visibly change baselines, readiness, falsifiers, and decision state. Strong claims survive baselines.</p>\n  <a href="falsification-gauntlet.html" style="display:inline-block;margin-top:10px;padding:13px 18px;border-radius:999px;background:#ffe98b;color:#06101c;text-decoration:none;font-weight:900">Open the fixed Gauntlet</a>\n</section>\n'''
    text=text.replace('</body>', card+'</body>') if '</body>' in text else text+card
    p.write_text(text, encoding='utf-8')

def patch_search_and_sitemap():
    s=ROOT/'public/search-index.json'
    if s.exists():
        try:
            data=json.loads(s.read_text(encoding='utf-8'))
            if isinstance(data, list) and not any(x.get('url')=='falsification-gauntlet.html' for x in data if isinstance(x,dict)):
                data.append({'title':'Falsification Gauntlet V1.1','url':'falsification-gauntlet.html','description':'Stress-test claims against baselines, replay, privacy, safety, and human review. Custom claims are preserved during stress.'})
                s.write_text(json.dumps(data, indent=2), encoding='utf-8')
        except Exception:
            pass
    sm=ROOT/'public/sitemap.xml'
    if sm.exists():
        text=sm.read_text(encoding='utf-8')
        url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-gauntlet.html'
        if url not in text:
            entry=f'  <url><loc>{url}</loc></url>\n'
            text=text.replace('</urlset>', entry+'</urlset>') if '</urlset>' in text else text+'\n'+entry
            sm.write_text(text, encoding='utf-8')

patch_readme(); patch_index(); patch_search_and_sitemap(); (ROOT/'.nojekyll').write_text('')
print('Installed GoalOS Falsification Gauntlet V1.1 hotfix')
