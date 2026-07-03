#!/usr/bin/env python3
import json, re, shutil
from pathlib import Path
from datetime import datetime, timezone
ROOT = Path.cwd()
PUBLIC = ROOT/'public'
REPORTS = ROOT/'reports'
CONTENT = ROOT/'content'/'goalos'
PUBLIC.mkdir(exist_ok=True)
REPORTS.mkdir(exist_ok=True, parents=True)
CONTENT.mkdir(exist_ok=True, parents=True)

VERSION='v28'
PAGE='validation-authority.html'
ALIASES=['human-or-node-validation.html','agi-node-validation.html','validation-console.html']
ENTRY={
  'title':'GoalOS Validation Authority V28 — Human or AGI Node',
  'url':'validation-authority.html',
  'category':'Validation Authority',
  'description':'Choose Human, AGI Node, or Hybrid validation for public-safe proof missions. Generates validation certificate, attestation, reviewer brief, and action graph.',
  'keywords':['validation','human','agi node','validator','attestation','review','proof','authority'],
  'external_actions':0,
  'boundary':'No user data, no user funds, no wallet, no transaction, no external call, no production authority.'
}

def copy_aliases():
    src=PUBLIC/PAGE
    for name in ALIASES:
        dst=PUBLIC/name
        if src.exists():
            shutil.copyfile(src,dst)

def inject(html_path):
    try: s=html_path.read_text(encoding='utf-8')
    except Exception: return False
    if 'goalos-v28-float' in s or html_path.name in {PAGE,*ALIASES}: return False
    snippet='''\n<div class="goalos-v28-float"><a href="validation-authority.html">Validate</a><a href="ask-goalos.html">Ask GoalOS</a></div>\n'''
    style='''\n<style id="goalos-v28-float-style">.goalos-v28-float{position:fixed;right:18px;bottom:18px;z-index:9999;display:flex;gap:10px}.goalos-v28-float a{font-family:Inter,system-ui,sans-serif;font-size:14px;font-weight:1000;text-decoration:none;color:#06110d;background:linear-gradient(135deg,#fff06a,#61ffd3);padding:12px 16px;border-radius:999px;box-shadow:0 12px 36px rgba(0,0,0,.35)}</style>\n'''
    if '</head>' in s and 'goalos-v28-float-style' not in s: s=s.replace('</head>',style+'</head>')
    if '</body>' in s: s=s.replace('</body>',snippet+'</body>')
    else: s+=snippet
    html_path.write_text(s,encoding='utf-8')
    return True

def patch_readme():
    p=ROOT/'README.md'
    block='''\n\n## GoalOS Validation Authority V28 — Human or AGI Node\n\nGoalOS now includes a browser-local validation authority console. Users can choose **Human reviewer**, **AGI Node validator**, or **Hybrid** validation for public-safe proof missions. The page generates a validation certificate, attestation, reviewer brief, action graph, and route recommendations while preserving the public-alpha boundary: no user data, no user funds, no wallet, no transaction, no external call, no production authority.\n\nOpen: `public/validation-authority.html`\n'''
    if p.exists():
        s=p.read_text(encoding='utf-8')
        if 'GoalOS Validation Authority V28' not in s:
            p.write_text(s+block,encoding='utf-8')
    else: p.write_text('# GoalOS AGIALPHA Ascension\n'+block,encoding='utf-8')

def patch_search_index():
    p=PUBLIC/'search-index.json'
    entries=[]
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
            entries=data if isinstance(data,list) else data.get('pages',[])
        except Exception: entries=[]
    urls={e.get('url') or e.get('path') for e in entries if isinstance(e,dict)}
    for u in [PAGE,*ALIASES]:
        if u not in urls and './'+u not in urls:
            e=dict(ENTRY); e['url']=u; e['path']=u; entries.append(e)
    p.write_text(json.dumps(entries,indent=2,ensure_ascii=False),encoding='utf-8')

def patch_sitemap():
    p=PUBLIC/'sitemap.xml'
    urls=[PAGE,*ALIASES]
    if p.exists(): s=p.read_text(encoding='utf-8')
    else: s='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    for u in urls:
        if u not in s:
            s=s.replace('</urlset>',f'  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{u}</loc></url>\n</urlset>')
    p.write_text(s,encoding='utf-8')

def write_content():
    (CONTENT/'validation-authority-v28.json').write_text(json.dumps({
        'version':'v28','createdAt':datetime.now(timezone.utc).isoformat(),'entry':ENTRY,
        'validationAuthorities':['human','agi_node','hybrid'],
        'decisionStates':['VALIDATED_BY_HUMAN','VALIDATED_BY_AGI_NODE','HYBRID_VALIDATION_READY','HOLD_HUMAN_REVIEW_REQUIRED','BLOCK_BOUNDARY'],
        'boundary':ENTRY['boundary']
    },indent=2),encoding='utf-8')


def fallback_page(title, subtitle):
    html = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title><style>body{{margin:0;background:linear-gradient(135deg,#03120f,#08091b);color:#fff8ea;font-family:Inter,system-ui,sans-serif}}main{{max-width:960px;margin:0 auto;padding:72px 24px}}a{{color:#61ffd3;font-weight:900}}.card{{border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.08);border-radius:28px;padding:28px}}h1{{font-size:clamp(44px,8vw,86px);line-height:.9;letter-spacing:-.07em}}p{{font-size:20px;line-height:1.35;color:#cbd7e7}}.btn{{display:inline-block;margin:8px 8px 0 0;border-radius:999px;padding:12px 16px;background:linear-gradient(135deg,#fff06a,#61ffd3);color:#06110d;text-decoration:none}}</style></head><body><main><div class="card"><h1>{title}</h1><p>{subtitle}</p><a class="btn" href="validation-authority.html">Validate with Human or AGI Node</a><a class="btn" href="site-map.html">All Pages</a><a class="btn" href="index.html">Home</a></div></main></body></html>"""
    return html.format(title=title, subtitle=subtitle)

def ensure_fallbacks():
    fallbacks={
      'goalos.html':('GoalOS Mission Studio','Tell GoalOS what you want. This fallback preserves the route until the richer Mission Studio is installed.'),
      'ask-goalos.html':('Ask GoalOS','Ask questions and route to the right GoalOS proof surface. This fallback preserves the chat route.'),
      'mainnet-contract-atlas.html':('Mainnet Contract Atlas','Explore the 48 GoalOS-created Ethereum Mainnet contracts. This fallback preserves the contract atlas route.'),
      'trust-boundary.html':('Trust Boundary','No user data, no user funds, no wallet, no transaction, no external call, no production authority.'),
      'token-boundary.html':('Token Boundary','$AGIALPHA public contract identification only. Not available from GoalOS. No sale, custody, wallet support, or advice.'),
      'site-map.html':('All Pages','Complete public route surface. This fallback preserves all-page navigation.'),
      'proof-run-001-docket.html':('Proof Run 001 Docket','Repository readiness becomes reviewable evidence. This fallback preserves the docket route.')
    }
    created=[]
    for name,(title,subtitle) in fallbacks.items():
        f=PUBLIC/name
        if not f.exists():
            f.write_text(fallback_page(title,subtitle),encoding='utf-8')
            created.append(name)
    return created

def main():
    created_fallbacks=ensure_fallbacks()
    copy_aliases()
    injected=0
    for hp in PUBLIC.glob('*.html'):
        if inject(hp): injected+=1
    patch_readme(); patch_search_index(); patch_sitemap(); write_content()
    report={'version':'v28','status':'passed','installedPage':PAGE,'aliases':ALIASES,'pagesInjected':injected,'fallbackPagesCreated':created_fallbacks,'generatedAt':datetime.now(timezone.utc).isoformat()}
    (REPORTS/'validation-authority-v28-install-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
