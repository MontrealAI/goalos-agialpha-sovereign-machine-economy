#!/usr/bin/env python3
from pathlib import Path
import json, sys, subprocess
ROOT=Path(__file__).resolve().parents[1]
required=['index.html','pathfinder.html','demo-ecosystem-registry.html','site-map.html','site-health.html','trust-boundary.html','token-boundary.html','privacy.html','data-boundary.html','no-data-no-funds.html','docs.html','search.html','404.html','proof-run-001-docket.html']
issues=[]
for r in required:
 if not (ROOT/'public'/r).exists(): issues.append({'route':r,'issue':'missing'})
for f in (ROOT/'public').glob('*.html'):
 txt=f.read_text(errors='ignore')
 if any(api in txt for api in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']): issues.append({'file':f.name,'issue':'forbidden browser API signal'})
 if '../reports' in txt or '../evidence' in txt or '../content' in txt or '../docs' in txt or '../replay' in txt: issues.append({'file':f.name,'issue':'escapes public root'})
out={'status':'passed' if not issues else 'failed','public_html_pages':len(list((ROOT/'public').glob('*.html'))),'issues':issues}
(ROOT/'reports/site-quality.json').write_text(json.dumps(out,indent=2)+"\n"); print(ROOT/'reports/site-quality.json'); sys.exit(0 if not issues else 1)
