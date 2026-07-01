# GoalOS Loop Flight Recorder V1

**Write the loop. Not the prompt.**

This browser-local public demo shows how long-running agentic work becomes review-ready when the loop is treated as the object of governance.

The demo demonstrates:

- role separation: planner, generator, evaluator, harness;
- disk state: `contract.json`, `state.json`, `progress.md`, `trace.log`, `scorecard.json`, `bottleneck.md`;
- restart from disk;
- trace reading;
- subjective scoring;
- harness deletion;
- bottleneck surfacing;
- Evidence Docket planning.

Boundary:

- No user data.
- No user funds.
- No wallet.
- No transaction.
- No network call.
- No production authority.
- Human review required.

Decision states include:

- `LOOP_REVIEW_READY`
- `REJECT_NO_CONTRACT`
- `HOLD_STATE_FILES_REQUIRED`
- `REJECT_SELF_GRADED_LOOP`
- `HOLD_RESTART_REQUIRED`
- `HOLD_TRACE_READING_REQUIRED`
- `HOLD_HARNESS_OVERHEAD_DOMINATES`
- `BLOCK_PRIVACY_BOUNDARY`
