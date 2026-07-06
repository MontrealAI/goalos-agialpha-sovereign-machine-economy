# Chronicle Promotion Gate Standard v80

A result may become a Chronicle candidate only when the following are true:

```json
{
  "proofbundle_present": true,
  "replay_result": "passed",
  "validator_verdict": "approved",
  "claim_boundary_preserved": true,
  "human_review_hold": true,
  "rollback_target": "recorded"
}
```

If replay or validator approval is missing, status remains `HOLD`. If the claim boundary is missing, status becomes `BLOCKED`. If proof passes, status becomes `CHRONICLE_CANDIDATE`, not automatic production authority.
