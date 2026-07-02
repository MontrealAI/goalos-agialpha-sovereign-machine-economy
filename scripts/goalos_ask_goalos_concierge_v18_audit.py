
from __future__ import annotations
import pathlib, json, re, datetime
root=pathlib.Path.cwd(); public=root/'public'
required=[public/'ask-goalos.html', public/'assets/goalos-ask-goalos-concierge-v18.js', public/'assets/goalos-ask-goalos-concierge-v18.css', public/'assets/goalos-ask-goalos-knowledge-v18.js']
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']
hits=[]
for f in [public/'assets/goalos-ask-goalos-concierge-v18.js', public/'assets/goalos-ask-goalos-knowledge-v18.js']:
    tx=f.read_text(encoding='utf-8', errors='ignore') if f.exists() else ''
    for bad in forbidden:
        if bad in tx: hits.append({'file':str(f),'pattern':bad})
injected=0
for p in public.rglob('*.html'):
    tx=p.read_text(encoding='utf-8', errors='ignore')
    if 'goalos-ask-goalos-concierge-v18.js' in tx: injected+=1
route_count=0
ki=public/'assets/goalos-ask-goalos-knowledge-v18.js'
if ki.exists():
    tx=ki.read_text(encoding='utf-8', errors='ignore')
    try:
        data=json.loads(tx[tx.find('['):tx.rfind(']')+1]); route_count=len(data)
    except Exception: route_count=0
status='passed' if not missing and not hits and route_count>=1 and injected>=1 else 'failed'
out={'status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'routes':route_count,'pagesInjected':injected,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
(root/'reports').mkdir(exist_ok=True)
(root/'reports/ask-goalos-concierge-v18-audit.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
raise SystemExit(0 if status=='passed' else 1)
