from pathlib import Path
import json, re, datetime
ROOT = Path.cwd()
js = ROOT / "public/assets/goalos-proof-mission-forge-v1.js"
html = ROOT / "public/proof-mission-forge.html"
errors = []
for p in [js, html]:
    if not p.exists():
        errors.append(f"missing:{p}")
text = js.read_text() if js.exists() else ""
for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in text:
        errors.append(f"forbidden_browser_api:{forbidden}")
html_text = html.read_text() if html.exists() else ""
required_phrases = ["No user data", "No user funds", "No wallet", "No transaction", "No network call", "Human review required"]
for phrase in required_phrases:
    if phrase.lower() not in html_text.lower():
        errors.append(f"missing_boundary_phrase:{phrase}")
report = {
    "schema": "goalos.proof_mission_forge.audit.v1",
    "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "status": "passed" if not errors else "failed",
    "browser_local": True,
    "no_network_call": "fetch(" not in text and "XMLHttpRequest" not in text and "sendBeacon" not in text,
    "no_user_data": True,
    "no_user_funds": True,
    "wallet_or_mainnet": "window.ethereum" in text,
    "human_review_required": True,
    "errors": errors
}
out = ROOT / "reports/proof-mission-forge-v1-qa.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
if errors:
    raise SystemExit("Audit failed")
