# Institutional Capability Stack

GoalOS is organized as a practical capability stack rather than a slogan.

| Layer | Operator question | Repository surface |
|---|---|---|
| Mission Contract | What exactly are we asking the system to do? | `schemas/mission_contract.schema.json`, `examples/mission-contract.example.json` |
| Proof Job | What bounded work unit should be executed? | `schemas/proof_job.schema.json` |
| Tool Trace | What did the system actually touch or invoke? | `schemas/tool_trace.schema.json` |
| Evidence Docket | What evidence supports the result? | `schemas/evidence_docket.schema.json` |
| Validator Report | Who or what reviewed the evidence? | `schemas/validator_report.schema.json` |
| Risk Ledger | What could go wrong and how was it bounded? | `schemas/risk_ledger.schema.json` |
| Decision State | Is the work blocked, under review, accepted, or releasable? | `src/goalos_ascension/kernel.py` |
| Settlement Receipt | What accepted claim was settled against what proof? | `schemas/settlement_receipt.schema.json` |
| Chronicle Entry | What should the organization remember? | `schemas/chronicle_entry.schema.json` |
| Capability Package | What reusable capability emerged? | `schemas/capability_package.schema.json` |

The stack is intentionally modular: a team can adopt the schemas and dockets first, then add validators, release gates, settlement receipts, and capability registry flows over time.
