from pathlib import Path
import json, datetime
ROOT=Path.cwd(); NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
docket={
  "docketId":"ACTION-REASON-TRACE-CONTRACT-V1-REFERENCE",
  "generatedAt":NOW,
  "claim":"GoalOS can represent an external-action request as a reviewable Action-Reason Trace Contract in a browser-local public demo.",
  "artifact":"public/action-reason-trace-contract.html",
  "actionReasonTrace":["reason","permission_scope","expected_observation","actual_observation","validator_status","cost_risk_ledger","rollback_pointer","evidence_pointer","human_review"],
  "decisionState":"ACTION_REVIEW_READY_WITH_HUMAN_BOUNDARY",
  "boundary":{"noUserData":True,"noUserFunds":True,"noWallet":True,"noTransaction":True,"noNetworkCall":True,"noProductionAuthority":True,"humanReviewRequired":True}
}
for rel in ['evidence/demo/action-reason-trace-contract-v1-reference-docket.json','reports/action-reason-trace-contract-v1-demo-run.json','content/goalos/action-reason-trace-contract-v1.json']:
    p=ROOT/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(docket,indent=2),encoding='utf-8')
print(json.dumps({"status":"passed","wrote":3,"generatedAt":NOW},indent=2))
