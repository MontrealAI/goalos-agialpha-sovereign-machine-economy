from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "evidence-room-index.json"


def main() -> int:
    artifacts = []
    for path in sorted((ROOT / "evidence").rglob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        artifacts.append({
            "path": path.relative_to(ROOT).as_posix(),
            "id": item.get("id"),
            "artifact_type": item.get("artifact_type"),
            "category": item.get("category"),
            "evidence_status": item.get("evidence_status"),
            "confidentiality": item.get("confidentiality"),
            "public_claim_permission": item.get("public_claim_permission"),
            "summary": item.get("summary"),
        })
    payload = {
        "status": "pass",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Evidence room indexed: {len(artifacts)} artifacts")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
