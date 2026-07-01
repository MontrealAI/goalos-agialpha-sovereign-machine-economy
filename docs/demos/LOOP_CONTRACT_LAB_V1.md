# GoalOS Loop Contract Lab V1

**Tagline:** Write the loop, not the prompt.

GoalOS Loop Contract Lab is a browser-local public demo showing how long-running agent work becomes reviewable when the loop is treated as a first-class object.

The page demonstrates:

```text
Objective
→ Role Contracts
→ Disk State
→ Trace Reading
→ Restart
→ Evidence Docket
→ Bottleneck Report
→ Governed Decision State
```

## Why this demo exists

Long-running agents fail when they rely on hidden context and one-off prompts. They become governable when the work loop has:

- a bounded mission contract;
- separate planner / generator / evaluator roles;
- state written to disk;
- trace logs that can be read after failure;
- restart semantics;
- evaluator independence;
- a deletable harness;
- a visible next bottleneck;
- public-alpha boundaries.

## Public-alpha boundary

No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.

This page is a local demonstration. It does not execute model calls, external workflows, wallets, APIs, or transactions.
