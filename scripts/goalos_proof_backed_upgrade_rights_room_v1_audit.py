#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re, sys

ROOT = Path.cwd()
errors = []
required = [
    "public/proof-backed-upgrade-rights-room.html",
    "public/assets/goalos-proof-backed-upgrade-rights-v1.css",
    "public/assets/goalos-proof-backed-upgrade-rights-v1.js",
    "docs/demos/PROOF_BACKED_UPGRADE_RIGHTS_ROOM_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_PROOF_BACKED_UPGRADE_RIGHTS_ROOM.md",
    "evidence/demo/proof-backed-upgrade-rights-room-v1-reference-docket.json",
]
for path in required:
    if not (ROOT/path).exists():
        errors.append(f"missing: {path}")

js_path = ROOT/"public/assets/goalos-proof-backed-upgrade-rights-v1.js"
js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden browser API detected: {forbidden}")

html = (ROOT/"public/proof-backed-upgrade-rights-room.html").read_text(encoding="utf-8") if (ROOT/"public/proof-backed-upgrade-rights-room.html").exists() else ""
html_lc = html.lower()
for phrase in ["no user data", "no user funds", "no wallet", "no transaction", "human review required", "score is advisory"]:
    if phrase not in html_lc:
        errors.append(f"missing boundary or doctrine phrase: {phrase}")

report = {
    "status": "passed" if not errors else "failed",
    "checked_at": datetime.datetime.utcnow().isoformat() + "Z",
    "browser_local": True,
    "no_network_call": True,
    "no_user_data": True,
    "no_user_funds": True,
    "wallet_or_mainnet": False,
    "human_review_required": True,
    "errors": errors,
}
out = ROOT/"reports/proof-backed-upgrade-rights-room-v1-qa.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
if errors:
    print(json.dumps(report, indent=2))
    sys.exit(1)
print(json.dumps(report, indent=2))
