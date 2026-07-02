#!/usr/bin/env python3
from pathlib import Path
import json
errors=[]
required=['public/index.html','public/site-map.html','public/demo-ecosystem-registry.html','public/site-health.html','public/pathfinder.html','public/search-index.json','public/assets/goalos-site-index-data-v13.js']
for r in required:
    if not Path(r).exists(): errors.append(f'missing {r}')
text='\n'.join(p.read_text(encoding='utf-8',errors='ignore') for p in Path('public/assets').glob('*v13*.js')) if Path('public/assets').exists() else ''
for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if token in text: errors.append(f'forbidden browser API in v13 assets: {token}')
routes=[]
if Path('public/search-index.json').exists():
    try: routes=json.loads(Path('public/search-index.json').read_text())
    except Exception as e: errors.append(f'bad search-index: {e}')
if len(routes)<100: errors.append(f'expected at least 100 indexed routes, found {len(routes)}')
idx=Path('public/index.html').read_text(encoding='utf-8',errors='ignore') if Path('public/index.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase not in idx: errors.append(f'missing boundary phrase on homepage: {phrase}')
status='passed' if not errors else 'failed'
Path('reports/site-experience-command-center-v13-audit.json').write_text(json.dumps({'status':status,'errors':errors,'route_count':len(routes)},indent=2))
if errors: raise SystemExit('\n'.join(errors))
print('audit passed')
