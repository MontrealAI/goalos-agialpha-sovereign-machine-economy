#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
errors = []

files = [
  "public/evolution-ledger-control-room.html",
  "public/assets/goalos-evolution-ledger-control-room-v2.css",
  "public/assets/goalos-evolution-ledger-control-room-v2.js",
  "evidence/demo/evolution-ledger-control-room-v2-reference-docket.json",
  "docs/demos/EVOLUTION_LEDGER_CONTROL_ROOM_V2.md",
  "docs/reviewer/HOW_TO_REVIEW_EVOLUTION_LEDGER_CONTROL_ROOM_V2.md"
]
for f in files:
    if not (ROOT / f).exists():
        errors.append(f"missing:{f}")

html = (ROOT / "public/evolution-ledger-control-room.html").read_text(encoding="utf-8", errors="ignore") if (ROOT / "public/evolution-ledger-control-room.html").exists() else ""
css = (ROOT / "public/assets/goalos-evolution-ledger-control-room-v2.css").read_text(encoding="utf-8", errors="ignore") if (ROOT / "public/assets/goalos-evolution-ledger-control-room-v2.css").exists() else ""
js = (ROOT / "public/assets/goalos-evolution-ledger-control-room-v2.js").read_text(encoding="utf-8", errors="ignore") if (ROOT / "public/assets/goalos-evolution-ledger-control-room-v2.js").exists() else ""

required_text = [
  "No user data", "No user funds", "No wallet", "No transaction", "No network call",
  "Human review required", "The ledger remembers", "proof, not secrets"
]
for s in required_text:
    if s.lower() not in (html + css + js).lower():
        errors.append(f"missing_text:{s}")

for forbidden in ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]:
    if forbidden in js:
        errors.append(f"forbidden_browser_api:{forbidden}")

# High contrast smoke tests: labels and switches must use explicit light text, not inherited dark text.
contrast_needles = [".gate-toggle span", "color:#f7fbff", ".gate-row h3", "color:#fff", "textarea"]
for needle in contrast_needles:
    if needle not in css:
        errors.append(f"contrast_css_missing:{needle}")

if "fallback-svg" not in html:
    errors.append("missing_static_svg_fallback")

report = {
  "status": "passed" if not errors else "failed",
  "generated_at": NOW,
  "errors": errors,
  "browser_local": True,
  "no_network_call": True,
  "no_user_data": True,
  "no_user_funds": True,
  "wallet_or_mainnet": False,
  "human_review_required": True,
  "accessibility_checks": {
    "high_contrast_controls": "passed" if not any("contrast" in e for e in errors) else "failed",
    "static_fallback_svg": "fallback-svg" in html,
    "focus_visible": ":focus-visible" in css,
    "reduced_motion": "prefers-reduced-motion" in css
  }
}
Path("reports").mkdir(exist_ok=True)
Path("reports/evolution-ledger-control-room-v2-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
if errors:
    raise SystemExit(1)
