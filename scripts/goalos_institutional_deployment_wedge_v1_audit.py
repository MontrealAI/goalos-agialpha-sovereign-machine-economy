from pathlib import Path
import json, datetime

required = [
  "public/institutional-deployment-wedge.html",
  "public/assets/goalos-institutional-deployment-wedge-v1.css",
  "public/assets/goalos-institutional-deployment-wedge-v1.js",
  "docs/demos/INSTITUTIONAL_DEPLOYMENT_WEDGE_V1.md",
  "docs/reviewer/HOW_TO_REVIEW_INSTITUTIONAL_DEPLOYMENT_WEDGE.md",
  "evidence/deployment-wedge/institutional-deployment-wedge-v1-reference-docket.json",
  "content/goalos/institutional-deployment-wedge-v1.json"
]
errors = []
for path in required:
    if not Path(path).exists():
        errors.append(f"missing:{path}")

js = Path("public/assets/goalos-institutional-deployment-wedge-v1.js").read_text(encoding="utf-8") if Path("public/assets/goalos-institutional-deployment-wedge-v1.js").exists() else ""
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden-browser-api:{forbidden}")

html = Path("public/institutional-deployment-wedge.html").read_text(encoding="utf-8") if Path("public/institutional-deployment-wedge.html").exists() else ""
for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "No network call", "human review required"]:
    if phrase.lower() not in html.lower():
        errors.append(f"missing-boundary-phrase:{phrase}")

report = {
  "status": "passed" if not errors else "failed",
  "generatedAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "page": "institutional-deployment-wedge.html",
  "browserLocal": True,
  "noNetworkCall": True,
  "noUserData": True,
  "noUserFunds": True,
  "walletOrMainnet": False,
  "humanReviewRequired": True,
  "errors": errors
}
Path("reports").mkdir(exist_ok=True)
Path("reports/institutional-deployment-wedge-v1-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
Path("reports/institutional-deployment-wedge-v1-install-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["status"] == "passed" else 1)
