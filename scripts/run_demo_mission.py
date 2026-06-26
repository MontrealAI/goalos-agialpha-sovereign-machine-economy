from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.goalos_ascension import ProofKernel


def main() -> int:
    docket = json.loads((ROOT / "examples" / "evidence-docket.example.json").read_text(encoding="utf-8"))
    result = ProofKernel().settle(docket, "Repository scaffold accepted for public demonstration within the claim boundary.")
    out = ROOT / "reports" / "demo-settlement.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "accepted" else 1


if __name__ == "__main__":
    raise SystemExit(main())
