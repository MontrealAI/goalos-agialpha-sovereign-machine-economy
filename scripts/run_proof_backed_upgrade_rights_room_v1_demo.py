#!/usr/bin/env python3
from pathlib import Path
import json, datetime

ROOT = Path.cwd()
docket = {
    "id": "proof-backed-upgrade-rights-room-v1-demo-run",
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    "objective": "Demonstrate how a proof-backed upgrade right is earned by an artifact only after mandatory proof gates pass.",
    "decision_state": "HOLD_CHALLENGE_WINDOW_OPEN",
    "proof_gradient_score": 72,
    "gates": {
        "proof_history": True,
        "eval_pass": True,
        "baseline_comparison": True,
        "scope_authorized": True,
        "canary_ready": True,
        "rollback_ready": True,
        "challenge_window_cleared": False,
        "public_private_boundary": True,
        "human_review_path": True
    },
    "boundary": {
        "no_user_data": True,
        "no_user_funds": True,
        "no_wallet": True,
        "no_transaction": True,
        "no_network_call": True,
        "human_review_required": True
    }
}
Path("reports").mkdir(exist_ok=True)
Path("reports/proof-backed-upgrade-rights-room-v1-demo-run.json").write_text(json.dumps(docket, indent=2), encoding="utf-8")
print(json.dumps({"status":"passed","artifact":"reports/proof-backed-upgrade-rights-room-v1-demo-run.json"}, indent=2))
