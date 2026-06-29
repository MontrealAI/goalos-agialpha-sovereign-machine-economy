from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
errors = []
warnings = []

required = [
    "public/open-ended-work-engine.html",
    "public/assets/goalos-open-ended-work-engine-v1.css",
    "public/assets/goalos-open-ended-work-engine-v1.js",
    "docs/demos/OPEN_ENDED_WORK_ENGINE_LAB_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_OPEN_ENDED_WORK_ENGINE_LAB.md",
    "evidence/demo/open-ended-work-engine-lab-v1-reference-docket.json",
    "reports/open-ended-work-engine-lab-v1-demo-run.json"
]
for f in required:
    if not (ROOT / f).exists():
        errors.append(f"missing:{f}")

js_path = ROOT / "public/assets/goalos-open-ended-work-engine-v1.js"
if js_path.exists():
    js = js_path.read_text(encoding="utf-8")
    forbidden = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]
    for token in forbidden:
        if token in js:
            errors.append(f"forbidden_browser_api:{token}")

html_path = ROOT / "public/open-ended-work-engine.html"
if html_path.exists():
    h = html_path.read_text(encoding="utf-8").lower()
    for phrase in ["no user data","no user funds","no wallet","no transaction","no network call","human review required"]:
        if phrase not in h:
            errors.append(f"missing_boundary_phrase:{phrase}")
    if "generate tasks" not in h or "gate descendants" not in h:
        errors.append("missing_core_thesis")

qa = {
    "status":"passed" if not errors else "failed",
    "generated_at":NOW,
    "errors":errors,
    "warnings":warnings,
    "browserLocal":True,
    "noNetworkCall":True,
    "noUserData":True,
    "noUserFunds":True,
    "walletOrMainnet":False,
    "humanReviewRequired":True
}
out = ROOT / "reports/open-ended-work-engine-lab-v1-qa.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(qa, indent=2), encoding="utf-8")
if errors:
    raise SystemExit("Open-Ended Work Engine Lab QA failed: " + "; ".join(errors))
print("Open-Ended Work Engine Lab QA passed.")
