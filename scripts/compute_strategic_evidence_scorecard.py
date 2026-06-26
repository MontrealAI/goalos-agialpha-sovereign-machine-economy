from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "strategic-evidence-scorecard.json"


def load(path: str) -> dict:
    p = ROOT / path
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def main() -> int:
    maturity = load("reports/evidence-maturity-score.json")
    institutional = load("reports/institutional-scorecard.json")
    proof_velocity = load("reports/proof-velocity.json")
    institutional_score = institutional.get("average_score", institutional.get("score", 0))
    infra_score = 100 if institutional_score >= 9 else int(institutional_score * 10)
    market_score = 0
    if maturity.get("counted_items", 0):
        market_score += min(30, maturity.get("counted_items", 0) * 5)
    market_score += min(40, len(maturity.get("verified_categories_present", [])) * 4)
    if maturity.get("public_scale_claim_allowed"):
        market_score = 100
    payload = {
        "status": "pass",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "institutional_infrastructure_score": infra_score,
        "market_evidence_score": market_score,
        "evidence_state": maturity.get("evidence_state", "unknown"),
        "public_scale_claim_allowed": bool(maturity.get("public_scale_claim_allowed")),
        "verified_categories_present": maturity.get("verified_categories_present", []),
        "required_categories_missing": maturity.get("required_categories_missing", []),
        "proof_velocity": proof_velocity.get("metrics", {}),
        "recommended_public_statement": "Institutional proof infrastructure is ready; strong market-scale claims require source-verifiable external evidence." if not maturity.get("public_scale_claim_allowed") else "Strategic scale evidence candidate; publish only with the attached evidence docket and reviewer notes.",
        "next_best_actions": [
            "Replace placeholder evidence with real dated customer discovery records.",
            "Run at least three bounded pilots with success criteria agreed before execution.",
            "Publish baseline comparisons with replayable evidence.",
            "Obtain independent validator reports for flagship Evidence Dockets.",
            "Add source-verifiable commercial and fair-value-support records when they exist."
        ],
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
