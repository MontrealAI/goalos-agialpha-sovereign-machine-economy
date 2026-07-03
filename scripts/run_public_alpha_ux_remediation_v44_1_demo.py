from pathlib import Path
import json
ROOT=Path.cwd(); PUBLIC=ROOT/'public'
expected=['ux-proof-check.html','visual-flow-proof.html','index.html','site-map.html','search.html','site-health.html']
missing=[p for p in expected if not (PUBLIC/p).exists()]
report={'version':'v44.1','status':'passed' if not missing else 'failed','missing':missing,'demo':'human-readable visual flow and QA gate installed'}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/public-alpha-ux-remediation-v44-1-demo-run.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
raise SystemExit(0 if not missing else 1)
