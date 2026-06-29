from pathlib import Path
import json, datetime, hashlib
ROOT = Path.cwd(); NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
claim = "Promote a proof-carrying workflow artifact from candidate to canary after public-safe proof roots, evaluator attestations, challenge window, and rollback receipt are ready."
docket = {
  "id":"EVOLUTION-LEDGER-ROOM-V1-REFERENCE",
  "generated_at":NOW,
  "claim":claim,
  "public_sequence":["GoalOSCommit","RunRoot","ProofRoot","EvalAttestation","SelectionCertificate","RolloutReceipt","RollbackReceipt"],
  "hard_gates":["proof_root","eval_attestation","selection_certificate","rollback_receipt","public_private_boundary","challenge_window","validator_quorum","human_review"],
  "decision_state":"HOLD_CHALLENGE_WINDOW",
  "boundary":{"no_user_data":True,"no_user_funds":True,"no_wallet":True,"no_transaction":True,"no_network_call":True,"human_review_required":True},
  "digest": hashlib.sha256(claim.encode()).hexdigest()
}
(ROOT/'evidence/demo').mkdir(parents=True, exist_ok=True)
(ROOT/'evidence/demo/evolution-ledger-control-room-v1-reference-docket.json').write_text(json.dumps(docket, indent=2))
(ROOT/'reports/evolution-ledger-control-room-v1-demo-run.json').write_text(json.dumps({"status":"passed","generated_at":NOW,"docket":"evidence/demo/evolution-ledger-control-room-v1-reference-docket.json"}, indent=2))
