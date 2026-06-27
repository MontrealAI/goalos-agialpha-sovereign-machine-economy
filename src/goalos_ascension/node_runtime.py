from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any

from .models import canonical_hash, utc_now


@dataclass(frozen=True)
class NodePeer:
    peer_id: str
    role: str
    quality: int
    evidence: int
    risk: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NodeReview:
    node_identity: str
    mission: str
    node_state: str
    primary_route: str
    chain_head: str
    authority: str
    review_readiness: int
    peers: list[dict[str, Any]]
    disposition: str
    external_actions: int
    network_calls: int
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["_hash"] = canonical_hash(payload)
        return payload


class SovereignNodeRuntime:
    """Local deterministic AGI Alpha Node v0 reference layer.

    Matches the website's Sovereign Node Theatre without granting live authority.
    """

    roles = ["planner", "route", "executor", "validator", "guardian", "chronicle", "risk", "settlement"]

    def _metric(self, mission: str, idx: int, salt: str) -> int:
        raw = int(sha256(f"node:{mission}:{idx}:{salt}".encode()).hexdigest()[:8], 16)
        return 61 + raw % 36

    def review_mission(self, mission: str, node_identity: str = "1.alpha.node.agi.eth") -> NodeReview:
        peers = [NodePeer(f"P{i+1:02d}", self.roles[i % len(self.roles)], self._metric(mission, i, "q"), self._metric(mission, i, "e"), 100 - self._metric(mission, i, "s")) for i in range(10)]
        evidence = round(sum(p.evidence for p in peers) / len(peers))
        quality = round(sum(p.quality for p in peers) / len(peers))
        risk = round(sum(p.risk for p in peers) / len(peers))
        readiness = max(0, min(99, round(0.44 * evidence + 0.40 * quality - 0.22 * risk + 18)))
        chain_head = "GOALOS-" + sha256(f"{node_identity}:{mission}:{readiness}".encode()).hexdigest()[:12]
        route = "ROUTE-" + sha256(f"route:{mission}".encode()).hexdigest()[:12].upper()
        disposition = "HUMAN_REVIEW_REQUIRED" if readiness >= 55 else "HOLD_PENDING_EVIDENCE"
        return NodeReview(node_identity, mission, disposition, route, chain_head, "NONE_GRANTED", readiness, [p.to_dict() for p in peers], disposition, 0, 0, utc_now())
