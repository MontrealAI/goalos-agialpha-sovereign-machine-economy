
import json, pathlib, re, sys
ROOT=pathlib.Path.cwd(); PUBLIC=ROOT/'public'; REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
required=[PUBLIC/'agi-agent-constellation.html',PUBLIC/'agi-agent-use-cases.html',PUBLIC/'meta-agentic-alpha-agi.html',PUBLIC/'assets/goalos-agi-agent-constellation-v34.js',PUBLIC/'assets/goalos-agi-agent-constellation-v34.css']
missing=[str(p) for p in required if not p.exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [PUBLIC/'assets/goalos-agi-agent-constellation-v34.js', PUBLIC/'assets/goalos-agi-agent-routes-v34.js']:
    if p.exists():
        txt=p.read_text(errors='ignore')
        for f in forbidden:
            if f in txt: hits.append({'file':str(p),'forbidden':f})
broken=[]
for p in PUBLIC.glob('*.html'):
    txt=p.read_text(errors='ignore')
    for href in re.findall(r'href=["\']([^"\']+\.html)["\']',txt):
        if href.startswith('http') or href.startswith('#'): continue
        target=(p.parent/href.split('#')[0]).resolve()
        if not target.exists(): broken.append({'page':p.name,'href':href})
status='passed' if not missing and not hits and not broken else 'failed'
report={'version':'v34','status':status,'missing':missing,'forbiddenBrowserApiHits':hits,'brokenInternalHtmlLinks':broken[:50]}
(REPORTS/'agi-agent-constellation-v34-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
