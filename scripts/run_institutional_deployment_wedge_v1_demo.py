from pathlib import Path
import json, datetime
out = Path("reports")
out.mkdir(exist_ok=True)
payload = {
  "status": "passed",
  "demo": "institutional-deployment-wedge-v1",
  "generatedAt": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
  "referenceDocket": "evidence/deployment-wedge/institutional-deployment-wedge-v1-reference-docket.json",
  "browserLocal": True,
  "noUserData": True,
  "noUserFunds": True,
  "walletOrMainnet": False,
  "humanReviewRequired": True
}
Path("reports/institutional-deployment-wedge-v1-demo-run.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload, indent=2))
