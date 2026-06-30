# GoalOS Workflow Tiers

This file makes the Actions tab usable. Run current source-of-truth and QA workflows first; use older demo autopilots only when updating that specific surface.

## Recommended order

1. Source-of-truth / website QA workflows.
2. Docs quality and site quality workflows.
3. Proof Run / Evidence Docket workflows.
4. Demo-specific workflows only when changing that demo.
5. Boundary workflows whenever privacy, token, data, claim, or legal copy changes.

## Boundary / Trust
- `.github/workflows/goalos-agialpha-token-boundary-v2-1-production-autopilot.yml`
- `.github/workflows/goalos-agialpha-token-boundary-v2-autopilot.yml`
- `.github/workflows/goalos-legal-privacy-shield-autopilot.yml`

## Demo / Public Lab
- `.github/workflows/goalos-autonomous-demo-layer-v4-autopilot.yml`
- `.github/workflows/goalos-capability-compounding-lab-v1-autopilot.yml`
- `.github/workflows/goalos-capability-compounding-lab-v2-autopilot.yml`
- `.github/workflows/goalos-demo-registry-falsification-v1-2-autopilot.yml`
- `.github/workflows/goalos-external-reviewer-replay-room-v1-autopilot.yml`
- `.github/workflows/goalos-open-ended-work-engine-lab-v1-autopilot.yml`
- `.github/workflows/goalos-proof-backed-upgrade-rights-room-v1-autopilot.yml`
- `.github/workflows/goalos-proof-gradient-lab-v1-autopilot.yml`
- `.github/workflows/goalos-proof-mission-control-v1-autopilot.yml`
- `.github/workflows/goalos-proof-mission-forge-v1-autopilot.yml`
- `.github/workflows/goalos-proof-settlement-chronicle-lab-v1-autopilot.yml`
- `.github/workflows/goalos-proof-to-action-command-room-v1-autopilot.yml`
- `.github/workflows/goalos-sovereign-experience-stream-lab-v1-autopilot.yml`
- `.github/workflows/goalos-validator-council-arena-v1-autopilot.yml`
- `.github/workflows/goalos-value-realization-control-room-v1-autopilot.yml`

## Documentation
- `.github/workflows/goalos-docs-quality.yml`

## Evidence / Proof Run
- `.github/workflows/goalos-evidence-docket-theatre-v2-autopilot.yml`
- `.github/workflows/goalos-evolution-ledger-control-room-v1-autopilot.yml`
- `.github/workflows/goalos-evolution-ledger-control-room-v2-autopilot.yml`
- `.github/workflows/goalos-proof-run-001-docket-room-v2-autopilot.yml`
- `.github/workflows/goalos-proof-run-001-execution-room-v1-autopilot.yml`
- `.github/workflows/goalos-proof-run-001-real-docket-v1-autopilot.yml`
- `.github/workflows/goalos-public-proof-ledger-v1-autopilot.yml`

## Other / Legacy
- `.github/workflows/goalos-action-reason-trace-contract-v1-autopilot.yml`
- `.github/workflows/goalos-ascension-autopilot.yml`
- `.github/workflows/goalos-complete-sync-autopilot.yml`
- `.github/workflows/goalos-falsification-gauntlet-v1-1-hotfix-autopilot.yml`
- `.github/workflows/goalos-falsification-gauntlet-v1-autopilot.yml`
- `.github/workflows/goalos-historical-master-update-autopilot.yml`
- `.github/workflows/goalos-historical-opportunity-autopilot.yml`
- `.github/workflows/goalos-institutional-deployment-wedge-v1-autopilot.yml`
- `.github/workflows/goalos-multi-agent-institution-v6-autopilot.yml`
- `.github/workflows/goalos-proof-carrying-artifact-foundry-v1-autopilot.yml`
- `.github/workflows/goalos-proof-experience-atlas-v1-autopilot.yml`
- `.github/workflows/goalos-real-task-benchmark-bridge-v1-autopilot.yml`
- `.github/workflows/goalos-source-of-truth-v6-autopilot.yml`
- `.github/workflows/goalos-user-adoption-layer-v2-autopilot.yml`
- `.github/workflows/goalos-user-friendly-operating-layer-v3-autopilot.yml`

## QA / Parity
- `.github/workflows/goalos-ascension-visual-parity-v4-autopilot.yml`
- `.github/workflows/goalos-capability-parity-v2-implementation-autopilot.yml`

## Website / Pages
- `.github/workflows/goalos-latest-website-complete-update-autopilot.yml`
- `.github/workflows/goalos-site-quality.yml`
- `.github/workflows/goalos-website-code-parity-v3-autopilot.yml`
- `.github/workflows/goalos-website-experience-os-v1-autopilot.yml`
- `.github/workflows/goalos-website-experience-os-v2-autopilot.yml`
- `.github/workflows/goalos-website-experience-os-v3-autopilot.yml`
- `.github/workflows/goalos-website-experience-os-v4-autopilot.yml`
- `.github/workflows/goalos-website-experience-os-v5-autopilot.yml`


Boundary: No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.
