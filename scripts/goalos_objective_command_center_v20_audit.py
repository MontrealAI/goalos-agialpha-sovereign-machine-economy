
from pathlib import Path
import json, re, sys
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
required=[PUBLIC/'mission-command-center.html', PUBLIC/'assets/goalos-objective-command-center-v20.css', PUBLIC/'assets/goalos-objective-command-center-v20.js', ROOT/'reports/objective-command-center-v20-demo-run.json']
missing=[str(p) for p in required if not p.exists()]
js=(PUBLIC/'assets/goalos-objective-command-center-v20.js').read_text(encoding='utf-8',errors='ignore') if (PUBLIC/'assets/goalos-objective-command-center-v20.js').exists() else ''
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[f for f in forbidden if f in js]
html=(PUBLIC/'mission-command-center.html').read_text(encoding='utf-8',errors='ignore') if (PUBLIC/'mission-command-center.html').exists() else ''
links=re.findall(r'href="([^"]+\.html)"', html)
broken=[]
for href in links:
    if href.startswith('http'): continue
    target=(PUBLIC/href.split('#')[0])
    if not target.exists(): broken.append(href)
status='passed' if not missing and not hits and not broken else 'failed'
report={'status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken}
(ROOT/'reports/objective-command-center-v20-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
