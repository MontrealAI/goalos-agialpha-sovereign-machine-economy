#!/usr/bin/env python3
from goalos_common_quality import ROOT, write_report
import json, sys
names=['claim-scan.json','site-verification.json','docs-quality.json','site-quality.json','download-health.json','workflow-quality.json']
reports={}; failing=[]
for n in names:
 p=ROOT/'reports'/n
 if p.exists():
  try: reports[n]=json.loads(p.read_text());
  except Exception: reports[n]={'status':'failed','error':'invalid json'}
 else: reports[n]={'status':'missing'}
 if reports[n].get('status')!='passed': failing.append(n)
out={'status':'passed' if not failing else 'failed','release':'Repository + Website Excellence V11','reports':reports,'failing_reports':failing,'boundary':'public-alpha; no user data; no user funds; human review required; not production-authorized'}
write_report('release-health.json',out); sys.exit(0 if not failing else 1)
