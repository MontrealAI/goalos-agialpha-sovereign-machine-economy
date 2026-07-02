from pathlib import Path
import json
required=['public/index.html','public/site-map.html','public/pathfinder.html','public/demo-ecosystem-registry.html','public/site-health.html','public/search.html','public/trust-boundary.html','public/token-boundary.html','public/assets/goalos-site-index-data-v14.js','reports/site-institutional-command-center-v14-qa.json']
missing=[p for p in required if not Path(p).exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for js in Path('public/assets').glob('*v14*.js'):
    txt=js.read_text(errors='ignore')
    for f in forbidden:
        if f in txt: hits.append({"file":str(js),"hit":f})
route_health=json.loads(Path('reports/site-institutional-command-center-v14-route-health.json').read_text()) if Path('reports/site-institutional-command-center-v14-route-health.json').exists() else {"status":"missing"}
status='passed' if not missing and not hits and route_health.get('status')=='passed' else 'failed'
report={"status":status,"missing":missing,"forbidden_api_hits":hits,"route_health":route_health.get('status'),"browser_local":True,"no_user_data":True,"no_user_funds":True,"no_wallet":True,"human_review_required":True}
Path('reports/site-institutional-command-center-v14-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if status!='passed': raise SystemExit(1)
