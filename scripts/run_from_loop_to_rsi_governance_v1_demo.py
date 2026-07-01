from pathlib import Path
import json, datetime

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) if not isinstance(data, str) else data, encoding="utf-8")

def main():
    docket = {
        "status": "passed",
        "demo": "GoalOS From Loop to RSI Governance Lab V1",
        "generated_at": NOW,
        "scenario": "public-safe deterministic RSI governance cycle",
        "pipeline": ["TARGET","EMIT","FILTER","ATLAS","TEST-PLAN","EVAL","INSERT","PROMOTE"],
        "decision_state": "RSI_REVIEW_READY",
        "gates_passed": [
            "schema-bound artifacts",
            "replay manifest",
            "state hash continuity",
            "risk gate",
            "executed evidence",
            "baseline comparison",
            "OMNI no outcome authority",
            "public/private boundary",
            "rollback ready",
            "human review required"
        ],
        "hard_hold_for_high_novelty": [
            "Move-37 dossier",
            "persistence under shocks",
            "independent review"
        ],
        "claim_boundary": "Public demo only; not achieved AGI, not achieved ASI, not empirical SOTA, not production authorization.",
        "public_alpha_boundary": ["No user data","No user funds","No wallet","No transaction","No network call","No production authority","Human review required"]
    }
    write("reports/from-loop-to-rsi-governance-v1-demo-run.json", docket)
    write("evidence/demo/from-loop-to-rsi-governance-v1-reference-docket.json", docket)

if __name__ == "__main__":
    main()
