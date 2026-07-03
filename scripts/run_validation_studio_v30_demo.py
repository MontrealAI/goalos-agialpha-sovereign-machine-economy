#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import json, re
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; REPORTS=ROOT/'reports'; REPORTS.mkdir(exist_ok=True)
page=PUBLIC/'validation-studio.html'
text=page.read_text(encoding='utf-8') if page.exists() else ''
checks={
 'page_exists': page.exists(),
 'has_one_box': 'What needs validation?' in text and '<textarea' in text,
 'has_authority_modes': all(x in text for x in ['AGI Node','Human','Hybrid','Council']),
 'has_ask_goalos': 'Ask GoalOS' in text,
 'has_playbooks': 'Solved use cases' in text,
 'has_downloads': 'Validation Certificate JSON' in text and 'Reviewer Brief' in text
}
status='passed' if all(checks.values()) else 'failed'
out={'version':'v30','status':status,'checks':checks,'generatedAt':datetime.now(timezone.utc).isoformat()}
(REPORTS/'validation-studio-v30-demo-run.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
