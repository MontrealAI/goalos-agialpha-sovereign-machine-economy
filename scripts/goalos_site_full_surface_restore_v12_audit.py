#!/usr/bin/env python3
import json
from pathlib import Path
errors=[];public=Path('public')
required=['index.html','site-map.html','demo-ecosystem-registry.html','site-health.html','pathfinder.html','token-boundary.html','trust-boundary.html','search-index.json','sitemap.xml']
for r in required:
    if not (public/r).exists():errors.append(f'missing {r}')
data=json.loads((public/'search-index.json').read_text())
if len(data)<100:errors.append(f'expected at least 100 indexed pages, found {len(data)}')
for js in ['assets/goalos-site-full-surface-restore-v12.js','assets/goalos-command-palette-restore-v12.js']:
    p=public/js;txt=p.read_text() if p.exists() else ''
    for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
        if token in txt:errors.append(f'forbidden browser API {token} in {js}')
boundary=(public/'index.html').read_text()
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase not in boundary:errors.append(f'missing boundary phrase {phrase}')
out={'status':'failed' if errors else 'passed','errors':errors,'indexed_pages':len(data)}
Path('reports/site-full-surface-restore-v12-qa.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if errors:raise SystemExit(1)
