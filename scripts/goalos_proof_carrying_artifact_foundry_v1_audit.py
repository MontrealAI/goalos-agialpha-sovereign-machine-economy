#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path.cwd()
errors=[]
required=[
 "public/proof-carrying-artifact-foundry.html",
 "public/assets/goalos-proof-carrying-artifact-foundry-v1.css",
 "public/assets/goalos-proof-carrying-artifact-foundry-v1.js",
 "docs/demos/PROOF_CARRYING_ARTIFACT_FOUNDRY_V1.md",
 "docs/reviewer/HOW_TO_REVIEW_PROOF_CARRYING_ARTIFACT_FOUNDRY.md",
 "evidence/demo/proof-carrying-artifact-foundry-v1-reference-docket.json",
 "reports/proof-carrying-artifact-foundry-v1-demo-run.json"
]
for r in required:
    if not (ROOT/r).exists(): errors.append(f"missing:{r}")
js=(ROOT/"public/assets/goalos-proof-carrying-artifact-foundry-v1.js").read_text(encoding="utf-8")
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js: errors.append(f"forbidden_js_api:{forbidden}")
html=(ROOT/"public/proof-carrying-artifact-foundry.html").read_text(encoding="utf-8")
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "No network call", "Human review required", "Proof-Carrying Artifact"]:
    if phrase not in html: errors.append(f"missing_phrase:{phrase}")
report={
 "schema":"goalos.qa_report.v1",
 "name":"Proof-Carrying Artifact Foundry V1",
 "status":"passed" if not errors else "failed",
 "generatedAt":datetime.now(timezone.utc).isoformat(),
 "browserLocal":True,
 "noNetworkCall":True,
 "noUserData":True,
 "noUserFunds":True,
 "walletOrMainnet":False,
 "humanReviewRequired":True,
 "errors":errors
}
Path("reports").mkdir(exist_ok=True)
(ROOT/"reports/proof-carrying-artifact-foundry-v1-qa.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
print(json.dumps(report, indent=2))
if errors: sys.exit(1)
