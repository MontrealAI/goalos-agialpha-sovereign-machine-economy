
#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
FORBIDDEN=[r'navigator\.clipboard\.write',r'ethereum\.request',r'web3',r'fetch\(\s*[\"\']https?://',r'XMLHttpRequest\(']
def main():
 root=Path.cwd(); public=root/'public'; broken=[]; forbidden=[]
 for p in public.rglob('*'):
  if not p.is_file(): continue
  rel=p.relative_to(public).as_posix(); txt=''
  if rel.startswith('archive/v61-originals/'):
   continue
  if p.suffix.lower() in ['.html','.js','.css','.json','.md','.txt']:
   txt=p.read_text(encoding='utf-8',errors='ignore')
   for pat in FORBIDDEN:
    if re.search(pat,txt): forbidden.append({'file':'public/'+rel,'pattern':pat})
  if p.suffix.lower()=='.html':
   for ref in re.findall(r'(?:href|src)=["\']([^"\'#?]+)',txt):
    if ref.startswith(('http:','https:','mailto:','tel:','data:','javascript:','#')): continue
    target=(p.parent/ref).resolve()
    try: target.relative_to(public.resolve())
    except Exception: continue
    if not target.exists(): broken.append({'file':'public/'+rel,'target':ref})
 report={'version':'v61','status':'passed' if not forbidden and not broken else 'failed','public_html_count':len(list(public.rglob('*.html'))),'forbidden_public_hits':forbidden,'broken_internal_links':broken}
 (root/'reports').mkdir(exist_ok=True); (root/'reports'/'autonomous-proof-factory-website-v61-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(json.dumps(report,indent=2))
 if report['status']!='passed': raise SystemExit(1)
if __name__=='__main__': main()
