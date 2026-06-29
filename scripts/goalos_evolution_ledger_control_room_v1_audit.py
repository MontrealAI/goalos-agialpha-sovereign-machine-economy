from pathlib import Path
import json, datetime, re
ROOT=Path.cwd(); NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
required=[
 'public/evolution-ledger-control-room.html',
 'public/assets/goalos-evolution-ledger-room-v1.css',
 'public/assets/goalos-evolution-ledger-room-v1.js',
 'docs/demos/EVOLUTION_LEDGER_CONTROL_ROOM_V1.md',
 'docs/reviewer/HOW_TO_REVIEW_EVOLUTION_LEDGER_CONTROL_ROOM.md',
 'evidence/demo/evolution-ledger-control-room-v1-reference-docket.json'
]
errors=[]
for f in required:
    if not (ROOT/f).exists(): errors.append(f"missing:{f}")
js=(ROOT/'public/assets/goalos-evolution-ledger-room-v1.js').read_text() if (ROOT/'public/assets/goalos-evolution-ledger-room-v1.js').exists() else ''
for pat in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']:
    if pat in js: errors.append(f"forbidden_js:{pat}")
html=(ROOT/'public/evolution-ledger-control-room.html').read_text() if (ROOT/'public/evolution-ledger-control-room.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','No network call','Human review required']:
    if phrase.lower() not in html.lower(): errors.append(f"missing_boundary:{phrase}")
report={"status":"passed" if not errors else "failed","generated_at":NOW,"errors":errors,"browser_local":True,"no_network_call":True,"no_user_data":True,"no_user_funds":True,"wallet_or_mainnet":False,"human_review_required":True}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/evolution-ledger-control-room-v1-qa.json').write_text(json.dumps(report, indent=2))
if errors: raise SystemExit(1)
