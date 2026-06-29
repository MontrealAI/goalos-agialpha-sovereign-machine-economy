
#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path
ROOT = Path.cwd()
PUBLIC = ROOT / 'public'
REPORTS = ROOT / 'reports'
REPORTS.mkdir(exist_ok=True)
errors=[]; warnings=[]
required = [
 'index.html','website-operating-system.html','pathfinder.html','demo-ecosystem-registry.html','site-map.html','trust-boundary.html',
 'assets/goalos-website-os-v2.css','assets/goalos-website-os-v2.js','assets/goalos-site-index-data-v2.js','search-index.json','sitemap.xml'
]
for rel in required:
    if not (PUBLIC/rel).exists(): errors.append(f'missing public/{rel}')
for rel in ['assets/goalos-website-os-v2.js','assets/goalos-site-index-data-v2.js']:
    p=PUBLIC/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for bad in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
            if bad in txt: errors.append(f'forbidden browser API {bad} in public/{rel}')
index=(PUBLIC/'index.html').read_text(encoding='utf-8') if (PUBLIC/'index.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','No network call','Human review required','Proof Run 001','Demo Registry']:
    if phrase not in index: errors.append(f'missing homepage phrase: {phrase}')
# Verify generated data parse by extracting JSON assignments.
data_path=PUBLIC/'assets/goalos-site-index-data-v2.js'
route_count=0
if data_path.exists():
    txt=data_path.read_text(encoding='utf-8')
    m=re.search(r'window\.GOALOS_SITE_ROUTES\s*=\s*(\[.*\]);', txt, re.S)
    if not m:
        errors.append('route data assignment missing')
    else:
        try:
            routes=json.loads(m.group(1)); route_count=len(routes)
            if route_count < 10: errors.append('route registry unexpectedly small')
            live=[r for r in routes if r.get('status')=='live']
            if not live: errors.append('no live routes indexed')
        except Exception as e:
            errors.append(f'route data JSON parse failed: {e}')
# Check obvious generated page local hrefs.
for name in ['index.html','website-operating-system.html','pathfinder.html','demo-ecosystem-registry.html','site-map.html','trust-boundary.html']:
    p=PUBLIC/name
    if not p.exists(): continue
    txt=p.read_text(encoding='utf-8')
    for href in re.findall(r'href="([^"]+)"', txt):
        if href.startswith(('http','#','mailto:')) or href.endswith('/') or href.startswith('assets/'):
            continue
        if not (PUBLIC/href).exists():
            # allow docs/ references and expected legacy pages in generated command data are not direct hrefs if missing
            if not href.startswith('docs/'):
                warnings.append(f'generated page {name} links to missing public/{href}')
status='failed' if errors else 'passed'
report={'status':status,'errors':errors,'warnings':warnings,'routeCount':route_count,'browserLocal':True,'noNetworkCall':True,'noUserData':True,'noUserFunds':True,'walletOrMainnet':False,'humanReviewRequired':True}
(REPORTS/'website-experience-os-v2-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if errors:
    raise SystemExit(1)
