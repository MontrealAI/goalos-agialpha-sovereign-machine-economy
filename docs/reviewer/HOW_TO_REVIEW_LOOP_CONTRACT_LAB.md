# How to Review GoalOS Loop Contract Lab V1

Open `public/loop-contract-lab.html`.

Review checklist:

1. Run the loop contract.
2. Stress the weak contract.
3. Restart from disk.
4. Toggle off contract / disk / evaluator / boundary gates and confirm the decision state changes.
5. Download the loop contract, disk-state pack, Evidence Docket plan, bottleneck report, and reviewer brief.
6. Confirm the page stays browser-local.
7. Confirm the public-alpha boundary is visible.

Expected hard-boundary language:

```text
No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.
```

A reviewer should reject the page if it requests private data, connects a wallet, performs a transaction, calls a network API, or implies production authority.
