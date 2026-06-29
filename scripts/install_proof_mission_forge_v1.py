from pathlib import Path
import json, datetime

ROOT = Path.cwd()
required = [
    "public/proof-mission-forge.html",
    "public/assets/goalos-proof-mission-forge-v1.css",
    "public/assets/goalos-proof-mission-forge-v1.js",
    "docs/demos/PROOF_MISSION_FORGE_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_PROOF_MISSION_FORGE.md",
    "docs/pilot/FOUNDING_PROOF_MISSION_INTAKE.md",
    "reports/proof-mission-forge-v1-manifest.json"
]
missing = [p for p in required if not (ROOT / p).exists()]
report = {
    "schema": "goalos.proof_mission_forge.install_report.v1",
    "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "status": "passed" if not missing else "failed",
    "missing": missing,
    "page": "public/proof-mission-forge.html",
    "browser_local": True,
    "no_user_data": True,
    "no_user_funds": True,
    "human_review_required": True
}
out = ROOT / "reports/proof-mission-forge-v1-install-report.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2))
if missing:
    raise SystemExit("Missing required files: " + ", ".join(missing))
print(json.dumps(report, indent=2))
