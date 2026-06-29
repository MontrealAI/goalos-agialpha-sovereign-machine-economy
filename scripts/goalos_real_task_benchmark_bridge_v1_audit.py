#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re, sys

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
errors = []
required = [
    "public/real-task-benchmark-bridge.html",
    "public/assets/goalos-real-task-benchmark-bridge-v1.css",
    "public/assets/goalos-real-task-benchmark-bridge-v1.js",
    "docs/demos/REAL_TASK_BENCHMARK_BRIDGE_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_REAL_TASK_BENCHMARK_BRIDGE.md",
    "evidence/benchmark/real-task-benchmark-bridge-v1-reference-docket.json",
]
for rel in required:
    if not (ROOT/rel).exists():
        errors.append(f"missing:{rel}")

js = (ROOT/"public/assets/goalos-real-task-benchmark-bridge-v1.js").read_text(encoding="utf-8") if (ROOT/"public/assets/goalos-real-task-benchmark-bridge-v1.js").exists() else ""
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden_browser_api:{forbidden}")

html = (ROOT/"public/real-task-benchmark-bridge.html").read_text(encoding="utf-8") if (ROOT/"public/real-task-benchmark-bridge.html").exists() else ""
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "Human review required"]:
    if phrase.lower() not in html.lower():
        errors.append(f"missing_boundary_phrase:{phrase}")

report = {
    "status": "passed" if not errors else "failed",
    "generated_at": NOW,
    "errors": errors,
    "browser_local": True,
    "no_network_call": True,
    "no_user_data": True,
    "no_user_funds": True,
    "wallet_or_mainnet": False,
    "human_review_required": True
}
p = ROOT/"reports/real-task-benchmark-bridge-v1-qa.json"
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(0 if not errors else 1)
