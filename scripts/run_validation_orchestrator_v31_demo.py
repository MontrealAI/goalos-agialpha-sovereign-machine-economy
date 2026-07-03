#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
html=(PUBLIC/'validation-orchestrator.html').read_text(encoding='utf-8')
checks={'has_textbox':'id="objective"' in html,'has_agi_node':'AGI Node' in html,'has_human':'Human' in html,'has_hybrid':'Hybrid' in html,'has_council':'Council' in html,'has_ask_goalos':'Ask GoalOS' in html,'has_downloads':'Certificate JSON' in html,'has_playbooks':'playbooks' in html}
status='passed' if all(checks.values()) else 'failed'
out={'version':'v31','status':status,'checks':checks}
(REPORTS/'validation-orchestrator-v31-demo-run.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
