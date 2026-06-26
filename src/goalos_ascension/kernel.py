from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any


def hash_payload(payload: Any) -> str:
    data = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256(data).hexdigest()


@dataclass(frozen=True)
class Decision:
    state: str
    reason: str
    evidence_hash: str | None = None
    missing: list[str] = field(default_factory=list)


class ProofKernel:
    required_docket_fields = (
        "id",
        "mission_id",
        "claim_boundary",
        "proof_bundles",
        "validator_reports",
        "risk_ledger",
        "cost_ledger",
        "decision_state",
    )

    blocked_phrases = (
        "guaranteed returns",
        "guaranteed profit",
        "achieved agi",
        "achieved asi",
        "user-fund authorization: yes",
        "production activated: yes",
    )

    def evaluate_docket(self, docket: dict[str, Any]) -> Decision:
        missing = [field for field in self.required_docket_fields if not docket.get(field)]
        if missing:
            return Decision("BLOCKED", "Evidence Docket is incomplete.", missing=missing)
        text = json.dumps(docket, ensure_ascii=False).lower()
        blocked = [phrase for phrase in self.blocked_phrases if phrase in text]
        if blocked:
            return Decision("BLOCKED", "Unsupported or unsafe claim phrase detected.", missing=blocked)
        reports = docket.get("validator_reports", [])
        bundles = docket.get("proof_bundles", [])
        if not reports or not bundles:
            return Decision("NEEDS_REVISION", "Docket needs proof bundles and validator reports.")
        return Decision("READY_FOR_SETTLEMENT", "Docket has minimum proof structure.", hash_payload(docket), [])

    def settle(self, docket: dict[str, Any], accepted_claim: str) -> dict[str, Any]:
        decision = self.evaluate_docket(docket)
        if decision.state != "READY_FOR_SETTLEMENT":
            return {"decision": "blocked", "reason": decision.reason, "missing": decision.missing}
        return {
            "decision": "accepted",
            "settled_claim": accepted_claim,
            "evidence_hash": decision.evidence_hash,
            "limitations": [
                "research and product scaffold only",
                "not production authorization",
                "not legal, tax, or financial advice",
                "not a claim of achieved AGI or ASI",
            ],
        }
