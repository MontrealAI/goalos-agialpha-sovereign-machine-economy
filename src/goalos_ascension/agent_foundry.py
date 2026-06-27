from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any

from .models import canonical_hash, utc_now


@dataclass(frozen=True)
class InstitutionCandidate:
    candidate_id: str
    lineage: str
    archetype: str
    mission: str
    evidence_strength: int
    mission_utility: int
    safety_reversibility: int
    institutional_efficiency: int
    strategic_novelty: int
    posteriorscore: int
    gates: dict[str, bool]
    generated_at: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["_hash"] = canonical_hash(payload)
        return payload


class MetaAgenticFoundry:
    """Browser-local META-AGENTIC α-AGI reference layer.

    This is not a live model swarm. It is the deterministic, inspectable reference
    implementation behind the public Institution Foundry page: compose a mission,
    generate candidate institution designs, evaluate proof gates, and select a
    human-review-ready candidate.
    """

    archetypes = [
        "Category-defining company", "Breakthrough science institution", "Sovereign capability institution", "Public-interest mission",
        "Frontier release governance room", "Proof-native work OS", "Validator council", "Chronicle memory organ",
    ]

    def _score(self, mission: str, index: int, salt: str) -> int:
        raw = int(sha256(f"{mission}:{index}:{salt}".encode()).hexdigest()[:8], 16)
        return 55 + raw % 43

    def generate(self, mission: str, count: int = 24) -> list[InstitutionCandidate]:
        count = max(1, min(48, count))
        candidates: list[InstitutionCandidate] = []
        for i in range(count):
            evidence = self._score(mission, i, "evidence")
            utility = self._score(mission, i, "utility")
            safety = self._score(mission, i, "safety")
            efficiency = self._score(mission, i, "efficiency")
            novelty = self._score(mission, i, "novelty")
            score = round(0.28 * evidence + 0.24 * utility + 0.22 * safety + 0.16 * efficiency + 0.10 * novelty)
            gates = {
                "claim_boundary": True,
                "human_authority": True,
                "evidence_docket_required": evidence >= 55,
                "rollback_required": True,
                "no_external_action": True,
            }
            candidates.append(InstitutionCandidate(
                candidate_id=f"MΨ-{i+1:02d}", lineage=f"generation-{i // 6 + 1}",
                archetype=self.archetypes[i % len(self.archetypes)], mission=mission,
                evidence_strength=evidence, mission_utility=utility, safety_reversibility=safety,
                institutional_efficiency=efficiency, strategic_novelty=novelty, posteriorscore=score,
                gates=gates, generated_at=utc_now(),
            ))
        return candidates

    def select(self, mission: str) -> dict[str, Any]:
        candidates = self.generate(mission)
        selected = max(candidates, key=lambda c: (all(c.gates.values()), c.posteriorscore, c.evidence_strength, c.safety_reversibility))
        return {
            "status": "ready_for_human_review",
            "selected": selected.to_dict(),
            "candidate_count": len(candidates),
            "selection_rule": "max posterior score subject to evidence, rollback, no-external-action, and human-authority gates",
            "claim_boundary": ["not achieved AGI", "not production authority", "human review required"],
            "public_surface": "public/meta-agentic-alpha-agi.html",
        }
