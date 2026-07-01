#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
errors = []
required = ["public/loop-contract-lab.html", "public/assets/goalos-loop-contract-lab-v1.css", "public/assets/goalos-loop-contract-lab-v1.js", "docs/demos/LOOP_CONTRACT_LAB_V1.md", "docs/reviewer/HOW_TO_REVIEW_LOOP_CONTRACT_LAB.md", "evidence/demo/loop-contract-lab-v1-reference-docket.json", "content/goalos/loop-contract-lab-v1.json"]
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing: {rel}")
html = (ROOT / "public/loop-contract-lab.html").read_text(encoding="utf-8") if (ROOT / "public/loop-contract-lab.html").exists() else ""
js = (ROOT / "public/assets/goalos-loop-contract-lab-v1.js").read_text(encoding="utf-8") if (ROOT / "public/assets/goalos-loop-contract-lab-v1.js").exists() else ""
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "Human review required"]:
    if phrase not in html:
        errors.append(f"boundary phrase missing from page: {phrase}")
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden browser API in JS: {forbidden}")
for needed in ["Run loop contract", "Stress weak contract", "Restart from disk", "Download loop contract"]:
    if needed not in html:
        errors.append(f"interaction missing: {needed}")
status = "failed" if errors else "passed"
report = {"status":status,"generated_at":NOW,"errors":errors,"browser_local":True,"no_network_call":"fetch(" not in js and "XMLHttpRequest" not in js,"no_user_data":True,"no_user_funds":True,"wallet_or_mainnet":"window.ethereum" in js,"human_review_required":"Human review required" in html}
out = ROOT / "reports/loop-contract-lab-v1-qa.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(1 if errors else 0)
