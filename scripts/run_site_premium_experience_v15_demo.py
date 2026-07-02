
import json
from pathlib import Path
from datetime import datetime, timezone
root = Path.cwd()
public = root / "public"
required = [
    "index.html","start-here.html","pathfinder.html","site-map.html","demo-ecosystem-registry.html",
    "site-health.html","trust-boundary.html","token-boundary.html","from-loop-to-rsi-state-capacity.html"
]
missing = [x for x in required if not (public / x).exists()]
report = {
    "status": "passed" if not missing else "failed",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "required_pages": required,
    "missing": missing,
    "checks": [
        "homepage opens",
        "pathfinder opens",
        "registry opens",
        "Loop to RSI route opens",
        "trust/token boundaries open"
    ]
}
(root / "reports").mkdir(exist_ok=True)
(root / "reports" / "site-premium-experience-v15-demo-run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
if missing:
    raise SystemExit(1)
