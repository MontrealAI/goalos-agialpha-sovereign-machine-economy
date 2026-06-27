from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Literal
import json


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def canonical_hash(payload: Any) -> str:
    return "sha256:" + sha256(canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Serializable:
    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["_hash"] = canonical_hash(data)
        return data


@dataclass(frozen=True)
class MissionContract(Serializable):
    mission_id: str
    objective: str
    success_criteria: list[str]
    failure_criteria: list[str]
    constraints: list[str]
    authority: str = "human_review_required"
    risk_class: Literal["low", "medium", "high", "consequential"] = "medium"
    allowed_tools: list[str] = field(default_factory=lambda: ["read_repository", "inspect_files", "generate_docket"])
    required_artifacts: list[str] = field(default_factory=lambda: [
        "claims_matrix", "evidence_docket", "validator_report", "risk_ledger", "cost_ledger", "decision_state", "chronicle_entry", "capability_package"
    ])
    claim_boundary: list[str] = field(default_factory=lambda: [
        "public_alpha_reference_implementation", "no_production_authorization", "no_user_fund_authorization", "no_mainnet_activation", "human_review_required"
    ])
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class ProofJob(Serializable):
    job_id: str
    mission_id: str
    objective: str
    acceptance_criteria: list[str]
    proof_requirements: list[str]
    allowed_tools: list[str]
    risk_class: str = "medium"
    status: Literal["created", "executed", "validated", "rejected"] = "created"


@dataclass(frozen=True)
class ToolTrace(Serializable):
    trace_id: str
    job_id: str
    tool_name: str
    action_reason: str
    permission_scope: str
    expected_observation: str
    actual_observation: str
    reversible: bool = True
    external_action: bool = False
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class ProofBundle(Serializable):
    proof_id: str
    job_id: str
    trace_root: str
    output_hash: str
    policy_decision_root: str
    tool_history_root: str
    cost: dict[str, Any]
    latency_ms: int
    signatures: list[str]
    replay_path: str
    evidence_uri: str


@dataclass(frozen=True)
class ValidatorReport(Serializable):
    validator_id: str
    docket_id: str
    verdict: Literal["accept", "revise", "reject", "escalate"]
    checks: dict[str, bool]
    notes: list[str]
    signed_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class GovernedDecisionState(Serializable):
    decision_id: str
    mission_id: str
    state: Literal["READY_FOR_HUMAN_REVIEW", "NEEDS_REVISION", "BLOCKED", "ACCEPTED_FOR_SIMULATED_SETTLEMENT"]
    rationale: str
    evidence_hash: str | None
    human_review_required: bool = True
    production_authority: bool = False
    external_actions_authorized: bool = False
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class SettlementReceipt(Serializable):
    receipt_id: str
    mission_id: str
    simulated: bool
    decision: str
    settled_claim: str
    evidence_hash: str | None
    limitations: list[str]
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class ChronicleEntry(Serializable):
    entry_id: str
    mission_id: str
    summary: str
    decision_state: str
    evidence_hash: str | None
    capability_package_id: str | None = None
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class CapabilityPackage(Serializable):
    package_id: str
    mission_id: str
    name: str
    initiation_conditions: list[str]
    tool_contracts: list[str]
    validators: list[str]
    risk_class: str
    evidence_history: list[str]
    replay_path: str
    rollback_plan: str
    promotion_status: Literal["draft", "candidate", "accepted_for_reuse", "rejected"] = "candidate"


@dataclass(frozen=True)
class EvidenceDocket(Serializable):
    id: str
    mission_id: str
    claim_boundary: list[str]
    claims_matrix: list[dict[str, Any]]
    proof_bundles: list[dict[str, Any]]
    validator_reports: list[dict[str, Any]]
    risk_ledger: list[dict[str, Any]]
    cost_ledger: dict[str, Any]
    decision_state: dict[str, Any]
    replay_path: str
    public_private_boundary: dict[str, Any]
    created_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class GoalOSCommit(Serializable):
    objective: str
    success_criteria: list[str]
    failure_criteria: list[str]
    constraints: list[str]
    authority: str
    risk_class: str
    budget: dict[str, Any]
    allowed_tools: list[str]
    required_evaluators: list[str]
    approval_rules: list[str]
    data_boundary: str
    rollback_obligations: list[str]
    claim_boundary: list[str]


@dataclass(frozen=True)
class RunCommitment(Serializable):
    goalos_commit_hash: str
    agent_set: list[str]
    plan_graph_hash: str
    artifact_version_roots: list[str]
    tool_permission_root: str
    context_root: str
    policy_root: str
    runtime_environment: str
    budget_limit: dict[str, Any]
    latency_limit_ms: int
    signer_set: list[str]


@dataclass(frozen=True)
class ProofPacket(Serializable):
    run_id: str
    run_commitment_hash: str
    trace_root: str
    output_hash: str
    policy_decision_root: str
    tool_history_root: str
    eval_result_root: str
    cost: dict[str, Any]
    latency_ms: int
    errors: list[str]
    credit_assignment: dict[str, float]
    evidence_uri: str
    signature_bundle: list[str]


@dataclass(frozen=True)
class EvalAttestation(Serializable):
    schema_id: str
    proof_ref: str
    baseline: str
    candidate: str
    verdict: Literal["pass", "fail", "revise"]
    evaluator: str
    signature: str


@dataclass(frozen=True)
class SelectionCertificate(Serializable):
    candidate_id: str
    decision: Literal["promote", "canary", "reject", "pause", "rollback"]
    scope: str
    canary_ready: bool
    rollback_target: str
    challenge_window_cleared: bool
    hard_gates: dict[str, bool]


@dataclass(frozen=True)
class EvolutionLedgerEntry(Serializable):
    entry_type: str
    public_fields: dict[str, Any]
    private_counterpart: str
    previous_hash: str | None = None


@dataclass(frozen=True)
class ProofCarryingArtifact(Serializable):
    artifact_id: str
    version_hash: str
    artifact_class: str
    proof_history: list[str]
    scope: str
    rollback_target: str
    selection_status: Literal["draft", "candidate", "canary", "active", "rejected", "rolled_back", "deprecated"]
