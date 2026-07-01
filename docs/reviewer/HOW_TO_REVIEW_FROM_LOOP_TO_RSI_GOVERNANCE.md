# How to Review the From Loop to RSI Governance Lab

This page is a public-safe demonstration. It is not an empirical AGI, ASI, SOTA, production, or deployment claim.

## Review questions

1. Does the demo distinguish loop behavior from RSI governance?
2. Does OMNI remain search control rather than outcome authority?
3. Does high novelty increase the proof burden?
4. Does the Move‑37 path require reproduction, stress testing, persistence, and a dossier?
5. Does the public/private boundary remain visible?
6. Do downloaded artifacts preserve the objective, gates, decision state, and boundary?
7. Does the page remain browser-local?

## Local audit

```bash
python scripts/goalos_from_loop_to_rsi_v1_audit.py
python scripts/run_from_loop_to_rsi_v1_demo.py
```

Expected result:

```json
{"status": "passed"}
```

## Reviewer verdicts

Use one of:

- Accept: the public demo behaves as described.
- Revise: the demo concept is useful but requires clearer gates or artifact output.
- Reject: the demo does not preserve boundary, replay, or decision-state logic.
- Dissent: the reviewer disagrees with the framing and explains why.
