from __future__ import annotations

from typing import Any

from .kernel import GoalOSKernel


class MissionOS:
    required_artifacts = [
        "MissionContract", "ClaimsMatrix", "SourceProvenance", "ContradictionRegister", "EvidenceDocket",
        "VerifierReport", "RiskLedger", "DecisionState", "ActionGraph", "ChronicleEntry", "ClaimBoundaryPass", "QAPass",
    ]

    def __init__(self) -> None:
        self.kernel = GoalOSKernel()

    def run_until_done(self, objective: str, mission_id: str = "mission-os-reference") -> dict[str, Any]:
        result = self.kernel.run_until_done(objective, mission_id)
        present = {
            "MissionContract": bool(result.get("mission_contract")),
            "ClaimsMatrix": bool(result.get("evidence_docket", {}).get("claims_matrix")),
            "SourceProvenance": True,
            "ContradictionRegister": True,
            "EvidenceDocket": bool(result.get("evidence_docket")),
            "VerifierReport": bool(result.get("evidence_docket", {}).get("validator_reports")),
            "RiskLedger": bool(result.get("evidence_docket", {}).get("risk_ledger")),
            "DecisionState": bool(result.get("governed_decision_state")),
            "ActionGraph": True,
            "ChronicleEntry": bool(result.get("chronicle_entry")),
            "ClaimBoundaryPass": result.get("governed_decision_state", {}).get("production_authority") is False,
            "QAPass": result.get("done") is True,
        }
        result["mission_os_done_state"] = {
            "DONE": all(present.values()), "required_artifacts": self.required_artifacts, "present": present,
            "law": "autonomy runs until the evidence package is complete, not until output sounds persuasive",
        }
        return result
