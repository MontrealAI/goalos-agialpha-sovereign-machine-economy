from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Any

from .models import canonical_hash


@dataclass(frozen=True)
class AgentProfile:
    agent_id: str
    role: str
    avg_cost: float
    risk_score: float
    expected_value: float
    allowed_tools: set[str]

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "allowed_tools": sorted(self.allowed_tools)}


@dataclass(frozen=True)
class CoordinationResult:
    selected_agents: list[str]
    rejected_agents: list[str]
    route_family: str
    route_score: float
    proof_debt: float
    settlement_ready: bool
    evidence_bundle_hash: str
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


class CoordinationEngine:
    def default_agents(self) -> list[AgentProfile]:
        return [
            AgentProfile("planner.v0", "planner", 0.12, 0.08, 0.78, {"read_repository", "inspect_files"}),
            AgentProfile("coder.v0", "executor", 0.18, 0.14, 0.82, {"read_repository", "inspect_files", "generate_docket"}),
            AgentProfile("tester.v0", "tester", 0.10, 0.05, 0.76, {"inspect_files", "generate_docket"}),
            AgentProfile("validator.v0", "validator", 0.16, 0.04, 0.88, {"inspect_files", "generate_docket"}),
            AgentProfile("redteam.v0", "risk", 0.22, 0.09, 0.70, {"inspect_files"}),
        ]

    def hamiltonian(self, team: list[AgentProfile], allowed_tools: set[str]) -> float:
        local_cost = sum(a.avg_cost for a in team)
        risk = sum(a.risk_score for a in team)
        value = sum(a.expected_value for a in team)
        roles = {a.role for a in team}
        synergy = 0.12 * len(roles) + (0.25 if "validator" in roles else -0.35)
        overhead = 0.08 * (len(team) ** 2)
        forbidden = any(not a.allowed_tools <= allowed_tools for a in team)
        score = local_cost + 2 * risk + overhead - value - synergy
        return 999.0 if forbidden else round(score, 4)

    def route(self, allowed_tools: set[str] | None = None) -> CoordinationResult:
        allowed_tools = allowed_tools or {"read_repository", "inspect_files", "generate_docket"}
        agents = self.default_agents()
        candidate_teams = [list(c) for r in (3, 4) for c in combinations(agents, r)]
        ranked = sorted(((self.hamiltonian(team, allowed_tools), ",".join(a.agent_id for a in team), team) for team in candidate_teams), key=lambda item: (item[0], item[1]))
        best_score, _team_key, best_team = ranked[0]
        selected = [a.agent_id for a in best_team]
        rejected = [a.agent_id for a in agents if a.agent_id not in selected]
        proof_debt = max(0.0, round(0.35 + best_score, 4))
        settlement_ready = any(a.role == "validator" for a in best_team) and best_score < -1.0
        payload = {"selected": selected, "rejected": rejected, "score": best_score, "proof_debt": proof_debt}
        return CoordinationResult(
            selected, rejected, "R0_hamiltonian_baseline", best_score, proof_debt, settlement_ready,
            canonical_hash(payload),
            ["R0 is the transparent baseline, not a production router.", "Promotion to R1-R5 requires equal-budget evidence and zero critical safety violations."],
        )
