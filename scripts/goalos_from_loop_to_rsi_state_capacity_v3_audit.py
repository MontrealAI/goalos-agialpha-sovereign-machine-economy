#!/usr/bin/env python3
from pathlib import Path
import json, sys
required=['public/from-loop-to-rsi-state-capacity.html','public/assets/goalos-from-loop-to-rsi-state-capacity-v3.css','public/assets/goalos-from-loop-to-rsi-state-capacity-v3.js','reports/from-loop-to-rsi-state-capacity-v3-qa.json']
missing=[p for p in required if not Path(p).exists()]
js=Path('public/assets/goalos-from-loop-to-rsi-state-capacity-v3.js').read_text(encoding='utf-8') if Path('public/assets/goalos-from-loop-to-rsi-state-capacity-v3.js').exists() else ''
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[x for x in forbidden if x in js]
status='passed' if not missing and not hits else 'failed'
Path('reports').mkdir(exist_ok=True)
Path('reports/from-loop-to-rsi-state-capacity-v3-qa.json').write_text(json.dumps({'status':status,'missing':missing,'forbiddenBrowserApis':hits},indent=2),encoding='utf-8')
if status!='passed': sys.exit(1)
print('passed')
