from pathlib import Path
import json, re, datetime

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

REQUIRED = [
    "public/from-loop-to-rsi-governance.html",
    "public/assets/goalos-from-loop-to-rsi-governance-v1.css",
    "public/assets/goalos-from-loop-to-rsi-governance-v1.js",
    "docs/demos/FROM_LOOP_TO_RSI_GOVERNANCE_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_FROM_LOOP_TO_RSI_GOVERNANCE.md",
    "content/goalos/from-loop-to-rsi-governance-v1.json"
]
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]

def main():
    errors = []
    for path in REQUIRED:
        if not (ROOT / path).exists():
            errors.append(f"missing required file: {path}")
    js_path = ROOT / "public/assets/goalos-from-loop-to-rsi-governance-v1.js"
    if js_path.exists():
        txt = js_path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in txt:
                errors.append(f"forbidden browser API in JS: {token}")
    html = (ROOT / "public/from-loop-to-rsi-governance.html").read_text(encoding="utf-8") if (ROOT / "public/from-loop-to-rsi-governance.html").exists() else ""
    for phrase in ["No user data", "No user funds", "No wallet", "No transaction", "Human review required", "Search control"]:
        if phrase not in html:
            errors.append(f"missing boundary or doctrine phrase: {phrase}")
    report = {
        "status": "failed" if errors else "passed",
        "generated_at": NOW,
        "errors": errors,
        "browser_local": True,
        "forbidden_browser_apis_absent": not errors,
        "page": "public/from-loop-to-rsi-governance.html"
    }
    p = ROOT / "reports/from-loop-to-rsi-governance-v1-qa.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
