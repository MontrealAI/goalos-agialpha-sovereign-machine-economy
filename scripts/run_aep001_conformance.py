from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.aep001 import EvidenceDocket61, build_reference_commit, build_reference_run

commit = build_reference_commit("AEP-001 conformance reference run")
run = build_reference_run(commit)
docket = {
    "manifest": {"claim": "AEP-001 reference object model emitted"},
    "claims_matrix": [{"claim": "ProofPacket emitted", "status": "supported"}],
    "environment": {"runtime": "local_python"},
    "baselines": [{"baseline": "schema-only"}],
    "proof_packets": [run["proof_packet"]],
    "evaluator_attestations": [{"evaluator": "local-reference-validator", "verdict": "pass"}],
    "selection_certificate": run["selection_certificate"],
    "safety_ledger": [{"external_actions": 0}],
    "cost_ledger": {"usd": 0},
    "public_report": {"boundary": "public-alpha reference only"},
    "replay_path": "python scripts/run_aep001_conformance.py",
}
report = {"aep001_docket_61": EvidenceDocket61().validate(docket), "reference_run": run}
Path("reports").mkdir(exist_ok=True)
Path("reports/aep001-conformance.json").write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps(report["aep001_docket_61"], indent=2))
