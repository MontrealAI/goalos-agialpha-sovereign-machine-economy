#!/usr/bin/env python3
"""Deterministic local-only site route and boundary QA for GoalOS."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]; PUBLIC=ROOT/'public'; REPORTS=ROOT/'reports'
issues=[]
def add(k,p,m): issues.append({'kind':k,'path':str(p),'message':m})
class P(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.title=''; self.in_title=False; self.viewport=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and a.get('href'): self.links.append(a['href'])
  if tag=='meta' and a.get('name','').lower()=='viewport': self.viewport=True
  if tag=='title': self.in_title=True
 def handle_data(self,d):
  if self.in_title: self.title+=d
 def handle_endtag(self,tag):
  if tag=='title': self.in_title=False
html=list(PUBLIC.glob('*.html'))
key=['index.html','pathfinder.html','demo-ecosystem-registry.html','site-health.html','proof-ledger.html','public-proof-ledger.html','proof-run-001-docket.html','external-reviewer-replay-room.html','proof-mission-forge.html','proof-mission-control.html','no-data-no-funds.html','agialpha-token-boundary.html','404.html']
for k in key:
 if not (PUBLIC/k).exists(): add('missing_key_page',PUBLIC/k,'Key public page is missing')
for f in html:
 text=f.read_text(encoding='utf-8',errors='ignore'); parser=P(); parser.feed(text)
 if not parser.title.strip(): add('empty_title',f.relative_to(ROOT),'Missing or empty title tag')
 if not parser.viewport: add('missing_viewport',f.relative_to(ROOT),'Missing viewport meta tag')
 low=text.lower();
 if not (('no user data' in low and 'no user funds' in low and 'human review required' in low) or 'no-data-no-funds.html' in low or 'trust-boundary' in low):
  add('boundary_link_gap',f.relative_to(ROOT),'Page lacks direct or linked no-data/no-funds/human-review boundary language')
 for href in parser.links:
  if href.startswith(('http://','https://','mailto:','#','tel:')): continue
  target=href.split('#',1)[0].split('?',1)[0]
  if not target or target.startswith(('javascript:','data:')): continue
  if target.endswith('.html'):
   cand=(f.parent/target).resolve()
   if not cand.exists(): add('broken_html_link',f.relative_to(ROOT),f'Broken local HTML link: {href}')
 if f.name!='404.html' and 'window.ethereum' in text: add('forbidden_browser_api',f.relative_to(ROOT),'window.ethereum is not allowed in public demos')
 for api in ['sendBeacon','XMLHttpRequest','localStorage','sessionStorage']:
  if api in text: add('browser_api_review',f.relative_to(ROOT),f'{api} appears and should be reviewed')
if (PUBLIC/'search-index.json').exists():
 try: json.loads((PUBLIC/'search-index.json').read_text())
 except Exception as e: add('invalid_search_index','public/search-index.json',str(e))
if (PUBLIC/'sitemap.xml').exists():
 sm=(PUBLIC/'sitemap.xml').read_text(errors='ignore')
 for k in ['index.html','pathfinder.html','demo-ecosystem-registry.html','agialpha-token-boundary.html']:
  if k not in sm: add('sitemap_gap','public/sitemap.xml',f'{k} missing from sitemap')
blocking=[i for i in issues if i['kind'] not in ('boundary_link_gap','browser_api_review','sitemap_gap')]
route={'status':'passed' if not blocking else 'failed','html_pages_found':len(html),'key_pages':key,'issues':issues,'system_pages':['public/404.html']}
quality={**route,'boundary_gaps':[i for i in issues if i['kind']=='boundary_link_gap'],'broken_links':[i for i in issues if i['kind']=='broken_html_link'],'recommendations':['Keep 404 classified as a system page, not a demo.','Keep browser demos local-only unless explicitly reviewed.']}
REPORTS.mkdir(exist_ok=True)
(REPORTS/'site-route-health.json').write_text(json.dumps(route,indent=2)+'\n')
(REPORTS/'site-quality.json').write_text(json.dumps(quality,indent=2)+'\n')
print(json.dumps(quality,indent=2))
sys.exit(0 if route['status']=='passed' else 1)
