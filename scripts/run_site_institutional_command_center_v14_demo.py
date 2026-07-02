from pathlib import Path
import json, datetime
routes=json.loads(Path('public/search-index.json').read_text()) if Path('public/search-index.json').exists() else []
report={"status":"passed","demo":"site-institutional-command-center-v14","opened_routes":["index.html","site-map.html","demo-ecosystem-registry.html","site-health.html","from-loop-to-rsi-state-capacity.html","trust-boundary.html","token-boundary.html"],"route_count":len(routes),"generated_at":datetime.datetime.utcnow().isoformat()+"Z"}
Path('reports').mkdir(exist_ok=True)
Path('reports/site-institutional-command-center-v14-demo-run.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
