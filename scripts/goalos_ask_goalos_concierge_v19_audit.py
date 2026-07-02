#!/usr/bin/env python3
import json, pathlib, sys, datetime
ROOT=pathlib.Path.cwd(); PUBLIC=ROOT/'public'
required=[PUBLIC/'ask-goalos.html',PUBLIC/'assets/goalos-ask-goalos-concierge-v19.js',PUBLIC/'assets/goalos-ask-goalos-concierge-v19.css',PUBLIC/'assets/goalos-ask-goalos-knowledge-v19.js']
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [PUBLIC/'assets/goalos-ask-goalos-concierge-v19.js',PUBLIC/'assets/goalos-ask-goalos-knowledge-v19.js']:
    if p.exists():
        s=p.read_text(encoding='utf-8',errors='ignore')
        for f in forbidden:
            if f in s: hits.append({'file':str(p),'term':f})
injected=sum(1 for p in PUBLIC.glob('*.html') if 'goalos-ask-goalos-concierge-v19.js' in p.read_text(encoding='utf-8',errors='ignore'))
status='passed' if not missing and not hits and injected>0 else 'failed'
rep={'status':status,'version':'v19','missing':missing,'forbiddenBrowserApiHits':hits,'pagesInjected':injected,'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
(ROOT/'reports').mkdir(exist_ok=True)
for name in ['ask-goalos-concierge-v19-qa.json','ask-goalos-concierge-v19-audit.json']:
    (ROOT/'reports'/name).write_text(json.dumps(rep,indent=2),encoding='utf-8')
print(json.dumps(rep,indent=2))
if status!='passed': sys.exit(1)
