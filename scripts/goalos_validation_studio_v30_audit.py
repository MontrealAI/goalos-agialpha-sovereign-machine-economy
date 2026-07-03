#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, re, sys
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
required=[PUBLIC/'validation-studio.html', PUBLIC/'assets'/'goalos-validation-studio-v30.js', PUBLIC/'assets'/'goalos-validation-studio-v30.css']
missing=[str(p.relative_to(ROOT)) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [PUBLIC/'assets'/'goalos-validation-studio-v30.js', PUBLIC/'assets'/'goalos-validation-studio-routes-v30.js']:
    if p.exists():
        s=p.read_text(encoding='utf-8',errors='ignore')
        for f in forbidden:
            if f in s: hits.append({'file':str(p.relative_to(ROOT)),'pattern':f})
# internal html link audit
broken=[]
for p in PUBLIC.glob('*.html'):
    s=p.read_text(encoding='utf-8',errors='ignore')
    for m in re.finditer(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']',s):
        href=m.group(1)
        if href.startswith(('http://','https://','mailto:')): continue
        target=(PUBLIC/href).resolve()
        if not target.exists(): broken.append({'from':p.name,'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
out={'version':'v30','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken,'publicPages':len(list(PUBLIC.glob('*.html'))),'generatedAt':datetime.now(timezone.utc).isoformat()}
(REPORTS/'validation-studio-v30-audit.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
if status!='passed':
    print(json.dumps(out,indent=2)); sys.exit(1)
print(json.dumps(out,indent=2))
