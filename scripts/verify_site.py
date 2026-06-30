#!/usr/bin/env python3
from __future__ import annotations
import json,re,html,os
from pathlib import Path
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
def read(f): return f.read_text(encoding='utf-8',errors='ignore')
def links(f): return [html.unescape(m.group(2)).strip() for m in re.finditer(r'''(?:href|src)\s*=\s*(["'])(.*?)\1''',read(f),re.I)]
def ext(u): return not u or u.startswith(('http://','https://','mailto:','tel:','#','javascript:','data:'))
def tgt(base,u):
 u=u.split('#',1)[0].split('?',1)[0]
 if ext(u): return None
 if u.startswith('/'):
  return PUBLIC/u.split('/goalos-agialpha-sovereign-machine-economy/',1)[1] if '/goalos-agialpha-sovereign-machine-economy/' in u else None
 t=(base.parent/u).resolve(); return t/'index.html' if u.endswith('/') else t
def main():
 broken=[]; gaps=[]; checked=0
 for f in sorted(PUBLIC.glob('*.html')):
  txt=read(f).lower()
  if f.name!='404.html' and not any(x in txt for x in ['no user data','trust-boundary.html','no-data-no-funds.html','data-boundary.html']): gaps.append(f.relative_to(ROOT).as_posix())
  for u in links(f):
   t=tgt(f,u)
   if t is None: continue
   checked+=1
   if not t.exists(): broken.append({'page':f.relative_to(ROOT).as_posix(),'link':u,'resolved':os.path.relpath(str(t),str(ROOT))})
 out={'status':'passed' if not broken else 'failed','public_pages':len(list(PUBLIC.glob('*.html'))),'checked_links':checked,'broken_links':broken,'broken_link_count':len(broken),'boundary_gaps':gaps,'boundary_gap_count':len(gaps)}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/site-verification.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not broken else 1)
if __name__=='__main__': main()
