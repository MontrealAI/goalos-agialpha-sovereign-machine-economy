# Governance

GoalOS AGIALPHA Ascension uses proof-gated governance.

## Roles

| Role | Responsibility |
|---|---|
| Operator | Owns repository settings, release posture, and emergency response. |
| Maintainer | Reviews changes, preserves claim boundary, and merges validated work. |
| Validator | Reviews Evidence Dockets, risk ledgers, outputs, and reproduction notes. |
| Agent Author | Proposes agents, job templates, and capability packages. |
| Observer | Reviews public proof without private credentials or sensitive data. |

## Decision states

- `DRAFT`: incomplete proposal;
- `READY_FOR_VALIDATION`: evidence complete enough for review;
- `NEEDS_REVISION`: validation found gaps;
- `BLOCKED`: safety, legality, privacy, or claim-boundary issue;
- `ACCEPTED`: validated for the limited claim it makes;
- `SETTLED`: accepted and recorded with a settlement receipt;
- `REUSABLE`: accepted as a versioned capability package;
- `RETIRED`: withdrawn, superseded, or unsafe.

## Release rule

A release must include:

- passing QA report;
- claim boundary scan;
- evidence of generated website integrity;
- changelog entry;
- rollback plan;
- clear statement of what is and is not being claimed.
