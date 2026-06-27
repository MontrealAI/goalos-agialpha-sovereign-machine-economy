from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import canonical_hash


@dataclass(frozen=True)
class FrontierReleaseReview:
    scenario: str
    readiness_score: int
    decision_state: str
    required_next_evidence: list[str]
    access_tier: str
    human_review_required: bool
    authority_granted: bool
    review_hash: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class FrontierReleaseRoom:
    evidence_weights = {
        "public_sources": 10,
        "capability_eval": 12,
        "safeguard_eval": 14,
        "redteam_summary": 13,
        "access_matrix": 10,
        "validator_memo": 15,
        "rollback_protocol": 9,
        "human_authority": 8,
    }

    def review(self, scenario: str, evidence_layers: list[str] | None = None) -> FrontierReleaseReview:
        evidence_layers = evidence_layers or ["public_sources", "access_matrix", "human_authority"]
        base = 24 if "public-source" in scenario.lower() else 30
        score = min(96, base + sum(self.evidence_weights.get(e, 0) for e in evidence_layers))
        missing = [e for e in self.evidence_weights if e not in set(evidence_layers)]
        if score >= 82:
            decision = "APPROVE_LIMITED_PREVIEW_WITH_CONTROLS"
            tier = "limited_preview"
        elif score >= 70:
            decision = "APPROVE_TRUSTED_ACCESS_REVIEW"
            tier = "trusted_access_review"
        elif score >= 55:
            decision = "HOLD_PENDING_STRUCTURED_REVIEW"
            tier = "hold_pending_review"
        else:
            decision = "HOLD_PENDING_EVIDENCE"
            tier = "hold_pending_evidence"
        payload = {"scenario": scenario, "evidence_layers": evidence_layers, "score": score, "decision": decision}
        return FrontierReleaseReview(scenario, score, decision, missing[:5], tier, True, False, canonical_hash(payload))
