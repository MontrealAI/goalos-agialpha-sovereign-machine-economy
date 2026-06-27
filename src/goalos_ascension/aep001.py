from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import GoalOSCommit, ProofPacket, RunCommitment, SelectionCertificate, canonical_hash


class EvidenceDocket61:
    required_elements = [
        "manifest", "claims_matrix", "environment", "baselines", "proof_packets", "evaluator_attestations",
        "selection_certificate", "safety_ledger", "cost_ledger", "public_report", "replay_path",
    ]

    def validate(self, docket: dict[str, Any]) -> dict[str, Any]:
        missing = [key for key in self.required_elements if not docket.get(key)]
        return {"status": "passed" if not missing else "needs_revision", "missing": missing, "required_elements": self.required_elements}


@dataclass(frozen=True)
class ProofGradientResult:
    score: float
    promoted: bool
    hard_gates: dict[str, bool]
    reason: str


class ProofGradient:
    def score(self, *, quality_delta: float, transfer: float, verified_value: float, evidence_integrity: float,
              cost_delta: float, risk: float, coordination_overhead: float, rollback_debt: float) -> float:
        return round(
            0.24 * quality_delta + 0.18 * transfer + 0.24 * verified_value + 0.20 * evidence_integrity
            - 0.06 * cost_delta - 0.04 * risk - 0.02 * coordination_overhead - 0.02 * rollback_debt,
            4,
        )

    def promote(self, score: float, hard_gates: dict[str, bool], theta: float = 0.60) -> ProofGradientResult:
        missing = [k for k, v in hard_gates.items() if not v]
        if missing:
            return ProofGradientResult(score, False, hard_gates, "Hard gate failed: " + ", ".join(missing))
        if score < theta:
            return ProofGradientResult(score, False, hard_gates, "Proof Gradient below promotion threshold.")
        return ProofGradientResult(score, True, hard_gates, "Promotion candidate: proof, eval, scope, challenge, and rollback gates passed.")


def build_reference_commit(objective: str) -> GoalOSCommit:
    return GoalOSCommit(
        objective=objective,
        success_criteria=["Evidence Docket 6.1 elements present", "ProofPacket emitted", "Selection gate evaluated"],
        failure_criteria=["missing replay path", "unsupported claim", "rollback not specified"],
        constraints=["public/private proof boundary", "no external action", "human review"],
        authority="human_review_required", risk_class="medium", budget={"usd": 0, "mode": "local_reference"},
        allowed_tools=["local_reference_engine"], required_evaluators=["local-reference-validator"],
        approval_rules=["claim_boundary_pass", "rollback_ready", "human_review_required"],
        data_boundary="public-safe reference artifacts only",
        rollback_obligations=["revert generated artifacts", "preserve failed docket for review"],
        claim_boundary=["not achieved AGI", "not production authorization", "not mainnet activation"],
    )


def build_reference_run(commit: GoalOSCommit) -> dict[str, Any]:
    run = RunCommitment(
        goalos_commit_hash=commit.to_dict()["_hash"], agent_set=["planner.v0", "coder.v0", "tester.v0", "validator.v0"],
        plan_graph_hash=canonical_hash({"plan": "mission->proof->validation->decision"}),
        artifact_version_roots=[canonical_hash({"artifact": "proof-run-001-reference"})],
        tool_permission_root=canonical_hash({"tools": ["local_reference_engine"]}), context_root=canonical_hash({"context": "public-safe"}),
        policy_root=canonical_hash({"policy": "default_deny"}), runtime_environment="github-actions-local-python",
        budget_limit={"usd": 0, "external_services": 0}, latency_limit_ms=10000, signer_set=["github-actions[bot]"]
    )
    packet = ProofPacket(
        run_id="aep001-reference-run", run_commitment_hash=run.to_dict()["_hash"], trace_root=canonical_hash({"trace": "local"}),
        output_hash=canonical_hash({"output": "proof-run-001-reference"}), policy_decision_root=canonical_hash({"external_action": False}),
        tool_history_root=canonical_hash({"tools": ["local_reference_engine"]}), eval_result_root=canonical_hash({"eval": "passed"}),
        cost={"usd": 0}, latency_ms=1, errors=[], credit_assignment={"planner.v0": 0.25, "coder.v0": 0.25, "tester.v0": 0.25, "validator.v0": 0.25},
        evidence_uri="evidence/proof-run-001/proof-run-001-docket.json", signature_bundle=["local-reference-signature"]
    )
    gates = {"ProofValid": True, "EvalPass": True, "RiskOK": True, "RollbackReady": True, "CanaryReady": True, "ScopeAuthorized": True, "ChallengeWindowCleared": True}
    pg = ProofGradient()
    score = pg.score(quality_delta=0.72, transfer=0.64, verified_value=0.70, evidence_integrity=0.92, cost_delta=0.02, risk=0.08, coordination_overhead=0.10, rollback_debt=0.03)
    result = pg.promote(score, gates)
    cert = SelectionCertificate(
        candidate_id="proof-run-001-reference-capability", decision="canary" if result.promoted else "reject", scope="public-alpha-reference",
        canary_ready=True, rollback_target="previous-public-alpha-site", challenge_window_cleared=True, hard_gates=gates,
    )
    return {"goalos_commit": commit.to_dict(), "run_commitment": run.to_dict(), "proof_packet": packet.to_dict(), "proof_gradient": result.__dict__, "selection_certificate": cert.to_dict()}
