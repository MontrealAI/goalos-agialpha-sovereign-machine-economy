#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path.cwd(); REQ=['README.md','CONTRIBUTING.md','SECURITY.md','PRIVACY.md','DATA_BOUNDARY.md','DISCLAIMER.md','TOKEN_BOUNDARY.md','WORKFLOWS.md','docs/README.md','docs/START_HERE.md','docs/REVIEWER_GUIDE.md','docs/DEVELOPER_GUIDE.md','docs/CLAIM_BOUNDARY.md','docs/NO_DATA_NO_FUNDS.md','docs/TOKEN_BOUNDARY.md','docs/ROADMAP.md']
def main():
 missing=[x for x in REQ if not (ROOT/x).exists()]
 reg=ROOT/'content/goalos/demo-ecosystem-registry.json'; reg_issue=None; n=0
 if reg.exists():
  data=json.loads(reg.read_text()); items=data.get('routes') or data.get('demos') or data.get('items') or []; n=len(items); reg_issue=None if n else 'registry has no routes/demos/items'
 else: reg_issue='missing registry'
 phrase='I confirm I am not submitting personal data'; tdir=ROOT/'.github/ISSUE_TEMPLATE'; miss=[]
 if tdir.exists():
  for f in list(tdir.glob('*.yml'))+list(tdir.glob('*.yaml')):
   if phrase.lower() not in f.read_text(encoding='utf-8',errors='ignore').lower(): miss.append(f.relative_to(ROOT).as_posix())
 blockers=[]
 if missing: blockers.append({'missing':missing})
 if reg_issue: blockers.append({'registry_issue':reg_issue})
 if miss: blockers.append({'templates_missing_boundary_confirmation':miss})
 out={'status':'passed' if not blockers else 'failed','missing_files':missing,'registry_routes':n,'registry_issue':reg_issue,'templates_missing_boundary_confirmation':miss,'blockers':blockers}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/docs-quality.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not blockers else 1)
if __name__=='__main__': main()
