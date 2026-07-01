#!/usr/bin/env python3
from goalos_common_quality import ROOT, PUBLIC, public_pages, html_links, resolve_link, registry, write_report
import sys, os
broken=[]; gaps=[]
for f in public_pages():
 low=f.read_text(errors='ignore').lower()
 if f.name!='404.html' and not any(x in low for x in ['no user data','trust-boundary.html','no-data-no-funds.html','data-boundary.html']): gaps.append(str(f.relative_to(ROOT)))
 for u in html_links(f):
  t=resolve_link(f,u)
  if t is not None and not t.exists(): broken.append({'page':str(f.relative_to(ROOT)),'link':u,'resolved':os.path.relpath(str(t),str(ROOT))})
reg_missing=[r.get('canonical_path') for r in registry() if r.get('canonical_path') and not (PUBLIC/r.get('canonical_path')).exists()]
out={'status':'passed' if not broken and not reg_missing else 'failed','public_pages':len(public_pages()),'checked_links':sum(len(html_links(f)) for f in public_pages()),'broken_links':broken,'broken_link_count':len(broken),'boundary_gaps':gaps,'boundary_gap_count':len(gaps),'registry_missing_routes':reg_missing}
write_report('site-verification.json',out); print(out); sys.exit(0 if out['status']=='passed' else 1)
