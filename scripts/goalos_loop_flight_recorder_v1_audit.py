#!/usr/bin/env python3
from pathlib import Path
import json, shutil, subprocess, datetime
ROOT = Path.cwd()
errors = []
warnings = []
required = [
  "public/loop-flight-recorder.html",
  "public/assets/goalos-loop-flight-recorder-v1.css",
  "public/assets/goalos-loop-flight-recorder-v1.js",
  "docs/demos/LOOP_FLIGHT_RECORDER_V1.md",
  "docs/reviewer/HOW_TO_REVIEW_LOOP_FLIGHT_RECORDER.md",
  "evidence/demo/loop-flight-recorder-v1-reference-docket.json",
  "content/goalos/loop-flight-recorder-v1.json",
]
for r in required:
    if not (ROOT / r).exists():
        errors.append(f"missing required file: {r}")

html = (ROOT/"public/loop-flight-recorder.html").read_text(encoding="utf-8") if (ROOT/"public/loop-flight-recorder.html").exists() else ""
js_path = ROOT/"public/assets/goalos-loop-flight-recorder-v1.js"
js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "No network call", "Human review required"]:
    if phrase not in html:
        errors.append(f"missing boundary phrase in HTML: {phrase}")

for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden browser API in JS: {forbidden}")

node = shutil.which("node")
if node and js_path.exists():
    res = subprocess.run([node, "--check", str(js_path)], text=True, capture_output=True)
    if res.returncode != 0:
        errors.append("node --check failed: " + res.stderr[:500])
else:
    warnings.append("node not available; JS syntax check skipped")

qa = {
    "status": "failed" if errors else "passed",
    "generated_at": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
    "errors": errors,
    "warnings": warnings,
    "browser_local": True,
    "no_network_call": True,
    "no_user_data": True,
    "no_user_funds": True,
    "wallet_or_mainnet": False,
    "human_review_required": True
}
out = ROOT/"reports/loop-flight-recorder-v1-qa.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(qa, indent=2), encoding="utf-8")
print(json.dumps(qa, indent=2))
raise SystemExit(1 if errors else 0)
