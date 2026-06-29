# GoalOS Falsification Gauntlet V1.1

User-feedback hotfix for `/falsification-gauntlet.html`.

## Fixed

- Stress mode no longer overwrites a user-edited claim with the preset claim.
- Stress mode now visibly changes baseline pressure, B6 score, overhead, readiness, active falsifiers, and Governed Decision State.
- Downloads preserve the exact claim under test.
- The page remains browser-local: no user data, no user funds, no wallet, no transaction, no network call, no production authority.

## Review test

1. Edit the claim text.
2. Click **Stress claim**.
3. Confirm the edited claim remains unchanged.
4. Confirm the readiness, baselines, falsifiers, and decision state update.
5. Download the Evidence Docket and confirm it contains the edited claim.
