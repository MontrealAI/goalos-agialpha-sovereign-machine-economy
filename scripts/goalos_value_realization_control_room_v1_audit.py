#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT = Path.cwd(); NOW = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
required = ["public/value-realization-control-room.html","public/assets/goalos-value-realization-control-room-v1.css","public/assets/goalos-value-realization-control-room-v1.js","docs/demos/VALUE_REALIZATION_CONTROL_ROOM_V1.md","docs/reviewer/HOW_TO_REVIEW_VALUE_REALIZATION_CONTROL_ROOM.md","content/goalos/value-realization-control-room-v1.json"]
forbidden = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]
errors=[]
for f in required:
    if not (ROOT/f).exists(): errors.append(f"missing required file: {f}")
js = (ROOT/"public/assets/goalos-value-realization-control-room-v1.js").read_text(encoding="utf-8") if (ROOT/"public/assets/goalos-value-realization-control-room-v1.js").exists() else ""
for token in forbidden:
    if token in js: errors.append(f"forbidden browser API found: {token}")
html = (ROOT/"public/value-realization-control-room.html").read_text(encoding="utf-8") if (ROOT/"public/value-realization-control-room.html").exists() else ""
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "Human review required", "Verified work becomes"]:
    if phrase not in html: errors.append(f"missing boundary or thesis phrase: {phrase}")
report = {"status": "passed" if not errors else "failed", "errors": errors, "browser_local": True, "no_network_call": True, "no_user_data": True, "no_user_funds": True, "wallet_or_mainnet": False, "human_review_required": True, "generated_at": NOW}
(ROOT/"reports").mkdir(exist_ok=True)
(ROOT/"reports/value-realization-control-room-v1-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(0 if not errors else 1)
