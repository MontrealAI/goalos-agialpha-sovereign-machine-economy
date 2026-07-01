#!/usr/bin/env python3
from goalos_common_quality import ROOT, public_pages, write_report, FORBIDDEN_APIS
import re, sys
issues=[]
for f in public_pages():
 txt=f.read_text(errors='ignore')
 low=txt.lower()
 if '<title>' not in low: issues.append({'file':str(f.relative_to(ROOT)),'issue':'missing title'})
 if 'no user data' not in low and 'trust-boundary.html' not in low and f.name!='404.html': issues.append({'file':str(f.relative_to(ROOT)),'issue':'missing boundary or trust link'})
 for api in FORBIDDEN_APIS:
  if api in txt: issues.append({'file':str(f.relative_to(ROOT)),'issue':f'forbidden browser API signal: {api}'})
 if re.search(r'color:\s*#0[0-9a-f]{2,5}[^}]{0,120}background[^#]*#0[0-9a-f]{2,5}',txt,re.I): issues.append({'file':str(f.relative_to(ROOT)),'issue':'dark-on-dark heuristic review'})
 if 'overflow-x:auto' not in txt and '<table' in low: issues.append({'file':str(f.relative_to(ROOT)),'issue':'table may overflow mobile without overflow-x:auto'})
out={'status':'passed' if not issues else 'failed','pages_checked':len(public_pages()),'issue_count':len(issues),'issues':issues[:500]}
write_report('site-quality.json',out); sys.exit(0 if not issues else 1)
