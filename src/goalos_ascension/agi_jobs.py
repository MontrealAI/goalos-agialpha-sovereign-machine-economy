from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Literal

from .models import canonical_hash, utc_now


@dataclass(frozen=True)
class AGIJob:
    job_id: str
    objective: str
    acceptance_tests: list[str]
    risk_class: str
    allowed_tools: list[str]
    budget: dict[str, Any]
    status: Literal["requested", "executed", "validated", "settled_simulated"] = "requested"
    created_at: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["_hash"] = canonical_hash(payload)
        return payload


@dataclass(frozen=True)
class JobLifecycleRecord:
    request: dict[str, Any]
    escrow: dict[str, Any]
    execution: dict[str, Any]
    proof: dict[str, Any]
    validation: dict[str, Any]
    settlement: dict[str, Any]
    chronicle: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["_hash"] = canonical_hash(payload)
        return payload


class AGIJobsLedger:
    """Local reference AGI Jobs v0/v2 work OS.

    It implements Request -> Escrow -> Execute -> Proof -> Validate -> Settle -> Chronicle
    as a simulation-only public-alpha loop.
    """

    def create_job(self, objective: str, risk_class: str = "medium") -> AGIJob:
        return AGIJob(
            job_id="agijob-" + canonical_hash({"objective": objective})[-10:],
            objective=objective,
            acceptance_tests=["proof bundle present", "validator report present", "claim boundary preserved", "replay path present"],
            risk_class=risk_class,
            allowed_tools=["local_reference_engine", "read_repository", "generate_docket"],
            budget={"usd": 0, "mode": "simulation_only"},
        )

    def run_lifecycle(self, objective: str) -> JobLifecycleRecord:
        job = self.create_job(objective)
        request = job.to_dict()
        escrow = {"simulated": True, "amount": 0, "asset": "AGIALPHA-simulated", "locked": True, "external_funds": False}
        execution = {"status": "executed", "tool_calls": 1, "external_actions": 0, "network_calls": 0, "trace_root": canonical_hash({"job": job.job_id, "trace": "local"})}
        proof = {"proof_bundle": canonical_hash({"job": job.job_id, "execution": execution}), "replay_path": "scripts/run_agi_jobs_demo.py", "evidence_docket_required": True}
        validation = {"verdict": "accept_for_human_review", "validator": "local-reference-validator", "tests_passed": True, "human_review_required": True}
        settlement = {"status": "settled_simulated", "asset": "AGIALPHA-simulated", "amount": 0, "mainnet": False, "user_funds": False, "condition": "validator_acceptance"}
        chronicle = {"entry": "job lifecycle completed in local public-alpha simulation", "job_id": job.job_id, "capability_package": "candidate"}
        return JobLifecycleRecord(request, escrow, execution, proof, validation, settlement, chronicle)
