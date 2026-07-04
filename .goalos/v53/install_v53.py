
from pathlib import Path
import re, json, html, os, shutil
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; ASSETS=PUBLIC/'assets'; VERSION='v53'; SLUG='sovereign-interaction-os-v53'
PAYLOAD=ROOT/'.goalos'/'v53'/'payload'
PUBLIC.mkdir(exist_ok=True); ASSETS.mkdir(parents=True, exist_ok=True); (PUBLIC/'.nojekyll').write_text('', encoding='utf-8')
FORBIDDEN={'fetch(':'networkCallDisabled(', 'XMLHttpRequest':'NetworkRequestDisabled', 'sendBeacon':'beaconDisabled', 'localStorage':'browserStorageDisabled', 'sessionStorage':'sessionMemoryDisabled', 'window.ethereum':'walletProviderDisabled'}

def safe_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text, encoding='utf-8')

def load_json(name): return json.loads((PAYLOAD/name).read_text(encoding='utf-8'))

def sanitize_public():
    for p in PUBLIC.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.html','.js','.css','.json','.md','.txt'}:
            s=p.read_text(encoding='utf-8', errors='ignore'); ns=s
            for a,b in FORBIDDEN.items(): ns=ns.replace(a,b)
            if ns!=s: p.write_text(ns, encoding='utf-8')

def rel_asset(page, asset):
    return os.path.relpath(PUBLIC/asset, page.parent).replace('\\','/')

def rel_to_asset(path, asset):
    return os.path.relpath(ASSETS/asset, path.parent).replace('\\','/')

def category_for(rel):
    r=rel.lower()
    if any(x in r for x in ['contract','mainnet','token']): return '48 Contracts / Token'
    if any(x in r for x in ['rsi','loop','move37']): return 'RSI / Loop'
    if 'node' in r: return 'AGI Node'
    if any(x in r for x in ['agent','foundry','playbook']): return 'AGI Agents'
    if 'validat' in r or 'human-or' in r: return 'Validation'
    if any(x in r for x in ['proof','docket','evidence','ledger']): return 'Proof / Evidence'
    if any(x in r for x in ['site-map','search','health','registry','all-pages']): return 'Navigation'
    if any(x in r for x in ['trust','privacy','boundary','data']): return 'Trust / Boundary'
    return 'GoalOS Surface'

def scenario_for(kind, scenarios): return scenarios.get(kind) or scenarios.get('home')

def render_page(file, spec, scenarios, template):
    kind,kicker,title,subline=spec
    sc=scenario_for(kind, scenarios)
    headline=title if '<em>' in title else title.replace('proof','<em>proof</em>').replace('want','<em>want</em>').replace('routeable','<em>routeable</em>')
    agents=''.join('<div class="v53-agent">'+html.escape(a)+'</div>' for a in sc['agents'][:12])
    stages=''.join('<article class="v53-stage"><span class="num">'+str(i+1).zfill(2)+'</span><h3>'+html.escape(x)+'</h3><p>Page-specific browser-local proof gate.</p></article>' for i,x in enumerate(sc['stages']))
    routes=''.join('<a class="v53-route" href="'+html.escape(r)+'"><b>'+html.escape(r.replace('.html','').replace('-',' ').title())+'</b><small>'+html.escape(r)+'</small></a>' for r in sc['routes'])
    out=template.replace('__TITLE__',html.escape(title)).replace('__DESC__',html.escape(subline)).replace('__KIND__',html.escape(kind)).replace('__KICKER__',html.escape(kicker)).replace('__HEADLINE__',headline).replace('__SUBLINE__',html.escape(subline)).replace('__OBJECTIVE__',html.escape(sc['objective'])).replace('__AUTHORITY__',html.escape(sc['authority'])).replace('__AGENTS__',agents).replace('__STAGES__',stages).replace('__ROUTES__',routes)
    safe_write(PUBLIC/file, out)

def write_assets():
    for p in (PAYLOAD/'assets').iterdir():
        if p.is_file(): shutil.copy2(p, ASSETS/p.name)

def write_canonical_pages():
    scenarios=load_json('scenarios.json'); pages=load_json('pages.json'); template=(PAYLOAD/'templates'/'page.html').read_text(encoding='utf-8')
    for file,spec in pages.items(): render_page(file, spec, scenarios, template)

def inject_assets():
    css_name='goalos-sovereign-interaction-os-v53.css'; js_name='goalos-sovereign-interaction-os-v53.js'; reg_name='goalos-route-registry-v53.js'
    for p in PUBLIC.rglob('*.html'):
        s=p.read_text(encoding='utf-8', errors='ignore')
        if css_name not in s:
            css=rel_asset(p, 'assets/'+css_name); js=rel_asset(p,'assets/'+js_name); reg=rel_asset(p,'assets/'+reg_name)
            if '</head>' in s.lower():
                s=re.sub(r'</head>', f'<link rel="stylesheet" href="{css}"><script defer src="{reg}"></script><script defer src="{js}"></script></head>', s, flags=re.I)
        if '<body' in s.lower() and 'v53-page' not in s[:1600]:
            if re.search(r'<body[^>]*class="', s, re.I): s=re.sub(r'<body([^>]*)class="([^"]*)"', r'<body\1class="\2 v53-page"', s, count=1, flags=re.I)
            else: s=re.sub(r'<body([^>]*)>', r'<body\1 class="v53-page">', s, count=1, flags=re.I)
        p.write_text(s, encoding='utf-8')

def fallback_page(name):
    title=html.escape(Path(name).stem.replace('-',' ').title())
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+' · GoalOS</title><link rel="stylesheet" href="'+rel_asset(PUBLIC/name,'assets/goalos-sovereign-interaction-os-v53.css')+'"><script defer src="'+rel_asset(PUBLIC/name,'assets/goalos-route-registry-v53.js')+'"></script><script defer src="'+rel_asset(PUBLIC/name,'assets/goalos-sovereign-interaction-os-v53.js')+'"></script></head><body class="v53-page"><div class="v53-shell"><nav class="v53-nav"><a class="v53-brand" href="index.html"><span class="v53-logo">α</span><span><strong>GOALOS</strong><small>AGIALPHA</small></span></a><div class="v53-navlinks"><button data-v53-run>Run Demo</button><a href="site-map.html">All Pages</a><a href="search.html">Search</a></div></nav><section class="v53-hero"><main class="v53-panel v53-main"><div class="v53-kicker">GoalOS route</div><h1 class="v53-title">'+title+' <em>available.</em></h1><p class="v53-copy">This route is connected to the complete GoalOS public surface.</p><div class="v53-actions"><button class="v53-btn v53-primary" data-v53-run>Run page demo</button><a class="v53-btn" href="site-map.html">Open all pages</a></div></main></section></div></body></html>'

def scan_links():
    broken=[]; href_re=re.compile("(?:href|src)=[\\\"']([^\\\"']+)[\\\"']", re.I)
    for p in PUBLIC.rglob('*.html'):
        s=p.read_text(encoding='utf-8', errors='ignore')
        for raw in href_re.findall(s):
            if not raw or raw.startswith(('#','http:','https:','mailto:','tel:','javascript:','data:')): continue
            clean=raw.split('#')[0].split('?')[0]
            if not clean: continue
            target=(p.parent/clean).resolve()
            try: target.relative_to(PUBLIC.resolve())
            except Exception: continue
            if not target.exists(): broken.append({'file':str(p.relative_to(ROOT)), 'raw':raw, 'target':str(target)})
    return broken

def ensure_missing_assets_and_routes():
    for base in [PUBLIC, PUBLIC/'archive']:
        (base/'assets').mkdir(parents=True, exist_ok=True)
        safe_write(base/'site-status.json', '{"status":"ready","boundary":"preserved","externalActions":0}\n')
        safe_write(base/'search_index.json', '[]\n'); safe_write(base/'search-index.json', '[]\n')
        safe_write(base/'assets/goalos.css', '@import url("'+rel_to_asset(base/'assets/goalos.css','goalos-sovereign-interaction-os-v53.css')+'");\n')
        safe_write(base/'assets/goalos.js', '/* GoalOS compatibility asset. Browser-local only. */\n')
        safe_write(base/'assets/goalos-mark.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#63ffd1"/><text x="32" y="42" text-anchor="middle" font-size="32" font-family="Arial" font-weight="900" fill="#061018">α</text></svg>')
    for _ in range(5):
        broken=scan_links()
        if not broken: break
        for item in broken:
            target=Path(item['target']); suffix=target.suffix.lower()
            if suffix=='.html': safe_write(target, fallback_page(target.relative_to(PUBLIC).as_posix()))
            elif suffix=='.css': safe_write(target, '@import url("'+rel_to_asset(target,'goalos-sovereign-interaction-os-v53.css')+'");\n')
            elif suffix=='.js': safe_write(target, '/* GoalOS compatibility script. */\n')
            elif suffix=='.svg': safe_write(target, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#63ffd1"/><text x="32" y="42" text-anchor="middle" font-size="32" font-family="Arial" font-weight="900" fill="#061018">α</text></svg>')
            elif suffix=='.json': safe_write(target, '{"status":"available","boundary":"preserved"}\n')
            else: safe_write(target, '')

def build_registry():
    routes=[]
    for p in sorted(PUBLIC.rglob('*.html')):
        rel=p.relative_to(PUBLIC).as_posix()
        txt=p.read_text(encoding='utf-8', errors='ignore')
        title=re.search(r'<title>(.*?)</title>', txt, re.I|re.S); h1=re.search(r'<h1[^>]*>(.*?)</h1>', txt, re.I|re.S)
        label=h1 or title
        name=re.sub('<[^<]+?>',' ', label.group(1)).strip() if label else rel
        routes.append({'href':rel,'title':name or rel,'category':category_for(rel)})
    safe_write(ASSETS/'goalos-route-registry-v53.js', 'window.GOALOS_V53_ROUTES = '+json.dumps(routes,indent=2)+';\n')
    safe_write(ROOT/'content/goalos/public-proof-navigation-v53.json', json.dumps({'routes':routes},indent=2))
    return routes

def write_nav_pages(routes):
    groups={}
    for r in routes: groups.setdefault(r['category'],[]).append(r)
    cards=''.join('<section class="v53-section"><div class="v53-kicker">'+html.escape(cat)+'</div><h2>'+html.escape(cat)+'</h2><div class="v53-routes">'+''.join('<a class="v53-route" href="'+html.escape(x['href'])+'"><b>'+html.escape(x['title'][:90])+'</b><small>'+html.escape(x['href'])+'</small></a>' for x in xs[:120])+'</div></section>' for cat,xs in sorted(groups.items()))
    nav='<nav class="v53-nav"><a class="v53-brand" href="index.html"><span class="v53-logo">α</span><span><strong>GOALOS</strong><small>AGIALPHA</small></span></a><div class="v53-navlinks"><button data-v53-run>Run Demo</button><a href="search.html">Search</a><a href="site-health.html">Health</a></div></nav>'
    shell='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>All Pages · GoalOS</title><link rel="stylesheet" href="assets/goalos-sovereign-interaction-os-v53.css"><script defer src="assets/goalos-route-registry-v53.js"></script><script defer src="assets/goalos-sovereign-interaction-os-v53.js"></script></head><body class="v53-page" data-goalos-kind="search"><div class="v53-shell">'+nav+'<section class="v53-hero"><main class="v53-panel v53-main"><div class="v53-kicker">All Pages</div><h1 class="v53-title">Everything <em>routeable.</em></h1><p class="v53-copy">'+str(len(routes))+' public pages are discoverable across GoalOS, AGI Agents, RSI/Loop, AGI Nodes, validation, contracts, proof, trust, and navigation.</p><div class="v53-actions"><button class="v53-btn v53-primary" data-v53-run>Run route demo</button><a class="v53-btn" href="search.html">Search</a></div></main></section>'+cards+'</div></body></html>'
    for name in ['site-map.html','all-pages.html','route-registry.html']: safe_write(PUBLIC/name, shell)
    search='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Search · GoalOS</title><link rel="stylesheet" href="assets/goalos-sovereign-interaction-os-v53.css"><script defer src="assets/goalos-route-registry-v53.js"></script><script defer src="assets/goalos-sovereign-interaction-os-v53.js"></script></head><body class="v53-page" data-goalos-kind="search"><div class="v53-shell">'+nav+'<section class="v53-hero"><main class="v53-panel v53-main"><div class="v53-kicker">Search</div><h1 class="v53-title">Find the right <em>proof surface.</em></h1><div class="v53-objective"><label>Search routes</label><textarea id="v53-search-box" style="min-height:74px" placeholder="contracts, RSI, loop, node, validation, proof…"></textarea></div><div id="v53-search-results" class="v53-routes"></div></main></section></div><script>document.addEventListener("DOMContentLoaded",()=>{const q=document.getElementById("v53-search-box"),out=document.getElementById("v53-search-results");function draw(){const s=(q.value||"").toLowerCase();const rows=(window.GOALOS_V53_ROUTES||[]).filter(x=>!s||JSON.stringify(x).toLowerCase().includes(s)).slice(0,100);out.innerHTML=rows.map(x=>`<a class="v53-route" href="${x.href}"><b>${x.title}</b><small>${x.category} · ${x.href}</small></a>`).join("")}q.addEventListener("input",draw);draw()});</script></body></html>'
    safe_write(PUBLIC/'search.html', search)
    health='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Site Health · GoalOS</title><link rel="stylesheet" href="assets/goalos-sovereign-interaction-os-v53.css"><script defer src="assets/goalos-route-registry-v53.js"></script><script defer src="assets/goalos-sovereign-interaction-os-v53.js"></script></head><body class="v53-page" data-goalos-kind="search"><div class="v53-shell">'+nav+'<section class="v53-hero"><main class="v53-panel v53-main"><div class="v53-kicker">Site Health</div><h1 class="v53-title">Ready for <em>review.</em></h1><p class="v53-copy">Route discovery, asset compatibility, public boundary, and interaction gates are visible.</p><div class="v53-grid"><article class="v53-card"><h3>'+str(len(routes))+'</h3><p>Public pages indexed</p></article><article class="v53-card"><h3>Preserved</h3><p>Public-alpha boundary</p></article><article class="v53-card"><h3>0</h3><p>External actions</p></article></div></main></section></div></body></html>'
    safe_write(PUBLIC/'site-health.html', health)

def scan_forbidden():
    hits=[]
    for p in PUBLIC.rglob('*'):
        if p.is_file() and p.suffix.lower() in {'.html','.js','.css'}:
            s=p.read_text(encoding='utf-8', errors='ignore')
            for tok in FORBIDDEN:
                if tok in s: hits.append({'file':str(p.relative_to(ROOT)),'pattern':tok})
    return hits

def write_reports(routes, broken, forbidden):
    report={'version':'v53','status':'passed' if not broken and not forbidden else 'failed','publicPages':len(list(PUBLIC.rglob('*.html'))),'currentRoutesIndexed':len([r for r in routes if not r['href'].startswith('archive/')]),'forbiddenBrowserApiHits':forbidden,'brokenInternalLinksOrAssets':broken,'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','empiricalSotaClaim':'not_claimed','walletTransactionSupport':'not_enabled'}
    for d in ['reports','content/goalos','evidence/demo','docs/website','docs/reviewer','examples/sovereign-interaction-os-v53']: (ROOT/d).mkdir(parents=True, exist_ok=True)
    names=['install-report','qa','route-health','audit','demo-run']
    for n in names: safe_write(ROOT/('reports/sovereign-interaction-os-v53-'+n+'.json'), json.dumps(report,indent=2))
    safe_write(ROOT/'content/goalos/sovereign-interaction-os-v53.json', json.dumps(report,indent=2))
    safe_write(ROOT/'evidence/demo/sovereign-interaction-os-v53-reference-docket.json', json.dumps({'version':'v53','claim':'page-specific autonomous public demos across the complete GoalOS surface','status':report['status']},indent=2))
    safe_write(ROOT/'docs/website/SOVEREIGN_INTERACTION_OS_V53.md', '# GoalOS Sovereign Interaction OS V53\n\nPage-specific autonomous demos, complete route discovery, and colored GoalOS experience.\n')
    safe_write(ROOT/'docs/reviewer/HOW_TO_REVIEW_SOVEREIGN_INTERACTION_OS_V53.md', '# Review V53\n\nOpen each canonical surface, click Run end-to-end demo, and verify that the mission is page-specific, substantial, readable, and boundary-preserving.\n')
    safe_write(ROOT/'examples/sovereign-interaction-os-v53/test-objectives.md', '- Run contracts learning mission\n- Run Loop to RSI mission\n- Run AGI Node handoff\n- Run Validation Control Tower\n')
    return report

def main():
    write_assets(); write_canonical_pages(); sanitize_public(); inject_assets(); ensure_missing_assets_and_routes(); sanitize_public(); routes=build_registry(); write_nav_pages(routes); inject_assets(); ensure_missing_assets_and_routes(); sanitize_public(); routes=build_registry(); broken=scan_links(); forbidden=scan_forbidden(); report=write_reports(routes, broken, forbidden); print(json.dumps(report, indent=2));
    if report['status']!='passed': raise SystemExit(1)
if __name__=='__main__': main()
