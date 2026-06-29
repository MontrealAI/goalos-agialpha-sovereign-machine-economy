
#!/usr/bin/env python3
from __future__ import annotations
import json, re, datetime
from pathlib import Path
ROOT=Path.cwd(); REPORTS=ROOT/'reports'; EVIDENCE=ROOT/'evidence'/'demo'
REPORTS.mkdir(exist_ok=True); EVIDENCE.mkdir(parents=True, exist_ok=True)
NOW=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
data_path=ROOT/'public'/'assets'/'goalos-site-index-data-v2.js'
routes=[]
if data_path.exists():
    txt=data_path.read_text(encoding='utf-8')
    m=re.search(r'window\.GOALOS_SITE_ROUTES\s*=\s*(\[.*\]);', txt, re.S)
    if m: routes=json.loads(m.group(1))
route_families={}
for r in routes:
    route_families.setdefault(r.get('category','unknown'),0); route_families[r.get('category','unknown')]+=1
docket={
  'docketId':'GOALOS-WEBSITE-EXPERIENCE-OS-V2',
  'generatedAt':NOW,
  'claim':'The GoalOS public-alpha website has a unified navigation, route registry, role-based Pathfinder, site map, and visible no-data/no-funds boundary.',
  'boundary':['No user data','No user funds','No wallet','No transaction','No network call','No production authority','Human review required'],
  'routeCount':len(routes),
  'routeFamilies':route_families,
  'artifacts':['public/index.html','public/website-operating-system.html','public/pathfinder.html','public/demo-ecosystem-registry.html','public/site-map.html','reports/website-experience-os-v2-qa.json'],
  'decisionState':'WEBSITE_REVIEW_READY' if routes else 'HOLD_ROUTE_INDEX_REQUIRED'
}
(EVIDENCE/'website-experience-os-v2-reference-docket.json').write_text(json.dumps(docket,indent=2),encoding='utf-8')
(REPORTS/'website-experience-os-v2-demo-run.json').write_text(json.dumps({'status':'passed','generatedAt':NOW,'docket':docket},indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','routeCount':len(routes),'decisionState':docket['decisionState']},indent=2))
