# How to Review GoalOS Loop Flight Recorder V1

Open `public/loop-flight-recorder.html`.

Review checklist:

1. Run the loop flight.
2. Stress a weak loop.
3. Restart from disk.
4. Disable "Contract before code" and confirm `REJECT_NO_CONTRACT`.
5. Disable "Write state to disk" and confirm `HOLD_STATE_FILES_REQUIRED`.
6. Disable "Independent evaluator" and confirm `REJECT_SELF_GRADED_LOOP`.
7. Disable "Public/private boundary" and confirm `BLOCK_PRIVACY_BOUNDARY`.
8. Download every artifact.
9. Confirm no user data, funds, wallet, transaction, network call, or production authority is involved.

Reviewer honesty box:

- What gate should block the loop?
- Which artifact is missing?
- What would make the loop replayable?
- What would reduce proof debt?
- What should be deleted from the harness?
