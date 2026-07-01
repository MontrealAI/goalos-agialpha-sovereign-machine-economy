#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]; PUB=ROOT/'public'; REPORT=ROOT/'reports/public-download-health.json'
class P(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]
 def handle_starttag(self,tag,attrs):
  for k,v in attrs:
   if k in ('href','src') and v: self.links.append(v)
forbidden=re.compile(r'\.\./(reports|evidence|content|docs|replay)')
issues=[]; checked=[]
for f in PUB.rglob('*.html'):
 if 'archive' in f.parts:
  continue
 txt=f.read_text(errors='ignore'); checked.append(str(f.relative_to(ROOT)))
 if forbidden.search(txt): issues.append({'file':str(f.relative_to(ROOT)),'issue':'link escapes public root'})
 p=P(); p.feed(txt)
 for link in p.links:
  if link.startswith(('http:','https:','mailto:','#','javascript:')): continue
  target=(f.parent/link.split('#')[0].split('?')[0]).resolve()
  try: target.relative_to(PUB.resolve())
  except Exception: issues.append({'file':str(f.relative_to(ROOT)),'link':link,'issue':'not under public'})
  if link and not target.exists() and not link.endswith('/'):
   issues.append({'file':str(f.relative_to(ROOT)),'link':link,'issue':'missing local target'})
required=[PUB/'downloads/index.html',PUB/'downloads/content/release-state.json',PUB/'downloads/content/demo-ecosystem-registry.json']
for r in required:
 if not r.exists(): issues.append({'file':str(r.relative_to(ROOT)),'issue':'required mirror missing'})
REPORT.parent.mkdir(exist_ok=True); REPORT.write_text(json.dumps({'status':'passed' if not issues else 'failed','checked':checked,'issues':issues},indent=2)+"\n")
print(REPORT)
sys.exit(0 if not issues else 1)
