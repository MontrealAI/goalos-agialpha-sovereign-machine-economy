from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from goalos_ascension.evidence import load_json_files, proof_velocity

REPORT = ROOT / "reports" / "proof-velocity.json"


def main() -> int:
    events = load_json_files(ROOT, ["evidence/proof-velocity/events/*.json"])
    metrics = proof_velocity(events)
    payload = {
        "status": "pass",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics,
        "event_files_seen": len(events),
        "note": "Placeholder events do not count toward proof velocity.",
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
