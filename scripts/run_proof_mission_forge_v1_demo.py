from pathlib import Path
import json, datetime, hashlib
mission = {
    "schema": "goalos.proof_mission_forge.reference_docket.v1",
    "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "mission_id": "GMF-REFERENCE-001",
    "objective": "Evaluate public repository and website readiness for Proof Run 001 using only public-safe artifacts.",
    "mission_contract": {
        "decision_to_support": "Proceed to Proof Run 001 rehearsal",
        "risk_class": "low",
        "source_boundary": "public repository + public website only"
    },
    "claims_matrix": [
        {"claim": "Mission is public-safe", "status": "template-supported", "required_evidence": "data boundary"},
        {"claim": "Mission is reviewable", "status": "template-supported", "required_evidence": "validator packet"},
        {"claim": "Mission is replay-ready", "status": "requires-human-review", "required_evidence": "replay instructions"}
    ],
    "docket_plan": [
        "00_manifest", "01_claims_matrix", "02_mission_contract", "03_environment_boundary", "04_baselines",
        "05_proof_packets", "06_replay_instructions", "07_validator_reports", "08_cost_risk_ledger",
        "09_decision_state", "10_chronicle_entry", "11_capability_package"
    ],
    "public_boundary": {
        "no_user_data": True,
        "no_user_funds": True,
        "no_wallet": True,
        "no_transaction": True,
        "no_network_call": True,
        "human_review_required": True
    },
    "governed_decision_state": "MISSION_REVIEW_READY_TEMPLATE"
}
raw = json.dumps(mission, sort_keys=True)
mission["docket_hash"] = hashlib.sha256(raw.encode()).hexdigest()
Path("evidence/demo").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(parents=True, exist_ok=True)
Path("evidence/demo/proof-mission-forge-v1-reference-docket.json").write_text(json.dumps(mission, indent=2))
Path("reports/proof-mission-forge-v1-demo-run.json").write_text(json.dumps({
    "schema": "goalos.proof_mission_forge.demo_run.v1",
    "generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    "status": "passed",
    "reference_docket": "evidence/demo/proof-mission-forge-v1-reference-docket.json",
    "docket_hash": mission["docket_hash"]
}, indent=2))
print("Proof Mission Forge demo run generated.")
