#!/usr/bin/env python3
from pathlib import Path
import json
root=Path.cwd(); page=root/'public'/'agi-agent-mission-control.html'
text=page.read_text(encoding='utf-8') if page.exists() else ''
missing=[s for s in ['What should the AGI agents help you accomplish?','Agent constellation','Evidence Docket','AGI Node Handoff','Ask GoalOS'] if s not in text]
report={'version':'v37','status':'passed' if not missing else 'failed','missing':missing}
(root/'reports').mkdir(exist_ok=True); (root/'reports/agi-agent-mission-control-v37-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
if missing: raise SystemExit(1)
