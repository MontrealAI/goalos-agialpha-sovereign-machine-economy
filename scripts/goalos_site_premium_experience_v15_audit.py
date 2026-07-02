
import json, re
from pathlib import Path
from datetime import datetime, timezone
root = Path.cwd()
public = root / "public"
forbidden = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]
hits = []
for p in [public / "assets" / "goalos-site-premium-experience-v15.js", public / "assets" / "goalos-site-index-data-v15.js"]:
    if p.exists():
        s = p.read_text(encoding="utf-8", errors="ignore")
        for token in forbidden:
            if token in s:
                hits.append({"file": str(p.relative_to(root)), "token": token})
required_text = ["No user data", "No user funds", "No wallet", "No transaction", "Human review required"]
missing_text = []
home = public / "index.html"
if home.exists():
    h = home.read_text(encoding="utf-8", errors="ignore")
    for t in required_text:
        if t not in h:
            missing_text.append(t)
else:
    missing_text.append("index.html")
report = {
    "status": "passed" if not hits and not missing_text else "failed",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "forbidden_browser_api_hits": hits,
    "missing_boundary_text": missing_text
}
(root / "reports").mkdir(exist_ok=True)
(root / "reports" / "site-premium-experience-v15-audit.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
if report["status"] != "passed":
    raise SystemExit(1)
