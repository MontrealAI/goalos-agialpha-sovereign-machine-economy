#!/usr/bin/env python3
from goalos_common_quality import ROOT, PUBLIC, public_pages, html_links, resolve_link, write_report
import sys
broken=[]; escapes=[]
for f in public_pages():
 for u in html_links(f):
  if u.startswith(('../reports','../evidence','../content','../docs','../replay','../scripts')): escapes.append({'page':str(f.relative_to(ROOT)),'link':u})
  if u.startswith('downloads/'):
   t=resolve_link(f,u)
   if t is not None and not t.exists(): broken.append({'page':str(f.relative_to(ROOT)),'link':u,'resolved':str(t.relative_to(ROOT))})
out={'status':'passed' if not broken and not escapes else 'failed','broken_downloads':broken,'root_escape_links':escapes,'public_download_files':[str(p.relative_to(ROOT)) for p in (PUBLIC/'downloads').rglob('*') if p.is_file()] if (PUBLIC/'downloads').exists() else []}
write_report('download-health.json',out); sys.exit(0 if out['status']=='passed' else 1)
