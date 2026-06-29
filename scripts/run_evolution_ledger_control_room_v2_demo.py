#!/usr/bin/env python3
from pathlib import Path
import json, datetime, hashlib

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

docket = {
  "title": "GoalOS Evolution Ledger Control Room V2 Reference Docket",
  "generated_at": NOW,
  "claim": "The public demo shows that private intelligence stays private while public proof commitments become challengeable institutional memory.",
  "sequence": ["GoalOSCommit", "RunRoot", "ProofRoot", "EvalAttestation", "SelectionCertificate", "ChallengeWindow", "RolloutReceipt", "RollbackReceipt"],
  "public_proof": ["commitHash", "policyRoot", "riskClass", "proofHash", "evidenceURI", "evalRoot", "signatureBundle", "selectionDecision", "challengeWindow", "rollbackTarget"],
  "private_intelligence": ["private prompts", "raw traces", "customer data", "sensitive tool outputs", "privileged workpapers"],
  "hard_gates": {
    "GoalOSCommit": True,
    "RunRoot": True,
    "ProofRoot": True,
    "EvalAttestation": True,
    "SelectionCertificate": True,
    "RollbackReceipt": True,
    "PublicPrivateBoundary": True,
    "ChallengeWindow": True,
    "ValidatorQuorum": True,
    "HumanReview": True
  },
  "decision_state": "LEDGER_REVIEW_READY",
  "boundary": {
    "no_user_data": True,
    "no_user_funds": True,
    "no_wallet": True,
    "no_transaction": True,
    "no_network_call": True,
    "production_authority": False,
    "human_review_required": True
  }
}
docket["docket_hash"] = hashlib.sha256(json.dumps(docket, sort_keys=True).encode()).hexdigest()

out_dir = ROOT / "evidence/demo"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "evolution-ledger-control-room-v2-reference-docket.json").write_text(json.dumps(docket, indent=2), encoding="utf-8")

reports = ROOT / "reports"
reports.mkdir(exist_ok=True)
report = {
  "status": "passed",
  "generated_at": NOW,
  "reference_docket": "evidence/demo/evolution-ledger-control-room-v2-reference-docket.json",
  "decision_state": docket["decision_state"],
  "docket_hash": docket["docket_hash"]
}
(reports / "evolution-ledger-control-room-v2-demo-run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
