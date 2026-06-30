# Repository Excellence V8 Preflight

Generated: 2026-06-30T19:22:24.902330+00:00

## Counts
- public_pages: 134
- reports: 203
- evidence_artifacts: 62
- workflows: 54
- issue_templates: 53
- docs_files: 326
- scripts: 234
- tests: 38

## Checks
- `python -m pytest -q`: passed (18 passed)
- `python -m compileall -q scripts src tests`: passed
- `python scripts/validate_repo.py`: failed initially: .pytest_cache present; fixed by removing .pytest_cache and rerun in final QA
- `python scripts/validate_claims.py`: passed (0 blockers)
- `python scripts/verify_site.py`: passed (0 broken links, 0 boundary gaps)
- `python scripts/goalos_docs_quality.py`: passed
- `python scripts/goalos_site_quality.py`: passed

## Workflows
- `goalos-action-reason-trace-contract-v1-autopilot.yml`
- `goalos-agialpha-token-boundary-v2-1-production-autopilot.yml`
- `goalos-agialpha-token-boundary-v2-autopilot.yml`
- `goalos-ascension-autopilot.yml`
- `goalos-ascension-visual-parity-v4-autopilot.yml`
- `goalos-autonomous-demo-layer-v4-autopilot.yml`
- `goalos-capability-compounding-lab-v1-autopilot.yml`
- `goalos-capability-compounding-lab-v2-autopilot.yml`
- `goalos-capability-parity-v2-implementation-autopilot.yml`
- `goalos-claims-boundary.yml`
- `goalos-complete-sync-autopilot.yml`
- `goalos-demo-registry-falsification-v1-2-autopilot.yml`
- `goalos-docs-quality.yml`
- `goalos-evidence-docket-theatre-v2-autopilot.yml`
- `goalos-evolution-ledger-control-room-v1-autopilot.yml`
- `goalos-evolution-ledger-control-room-v2-autopilot.yml`
- `goalos-external-reviewer-replay-room-v1-autopilot.yml`
- `goalos-falsification-gauntlet-v1-1-hotfix-autopilot.yml`
- `goalos-falsification-gauntlet-v1-autopilot.yml`
- `goalos-final-hardening-v7-production-autopilot.yml`
- `goalos-historical-master-update-autopilot.yml`
- `goalos-historical-opportunity-autopilot.yml`
- `goalos-institutional-deployment-wedge-v1-autopilot.yml`
- `goalos-latest-website-complete-update-autopilot.yml`
- `goalos-legal-privacy-shield-autopilot.yml`
- `goalos-multi-agent-institution-v6-autopilot.yml`
- `goalos-open-ended-work-engine-lab-v1-autopilot.yml`
- `goalos-proof-backed-upgrade-rights-room-v1-autopilot.yml`
- `goalos-proof-carrying-artifact-foundry-v1-autopilot.yml`
- `goalos-proof-experience-atlas-v1-autopilot.yml`
- `goalos-proof-gradient-lab-v1-autopilot.yml`
- `goalos-proof-mission-control-v1-autopilot.yml`
- `goalos-proof-mission-forge-v1-autopilot.yml`
- `goalos-proof-run-001-docket-room-v2-autopilot.yml`
- `goalos-proof-run-001-execution-room-v1-autopilot.yml`
- `goalos-proof-run-001-real-docket-v1-autopilot.yml`
- `goalos-proof-settlement-chronicle-lab-v1-autopilot.yml`
- `goalos-proof-to-action-command-room-v1-autopilot.yml`
- `goalos-public-proof-ledger-v1-autopilot.yml`
- `goalos-real-task-benchmark-bridge-v1-autopilot.yml`
- `goalos-repository-quality.yml`
- `goalos-site-quality.yml`
- `goalos-source-of-truth-v6-autopilot.yml`
- `goalos-sovereign-experience-stream-lab-v1-autopilot.yml`
- `goalos-user-adoption-layer-v2-autopilot.yml`
- `goalos-user-friendly-operating-layer-v3-autopilot.yml`
- `goalos-validator-council-arena-v1-autopilot.yml`
- `goalos-value-realization-control-room-v1-autopilot.yml`
- `goalos-website-code-parity-v3-autopilot.yml`
- `goalos-website-experience-os-v1-autopilot.yml`
- `goalos-website-experience-os-v2-autopilot.yml`
- `goalos-website-experience-os-v3-autopilot.yml`
- `goalos-website-experience-os-v4-autopilot.yml`
- `goalos-website-experience-os-v5-autopilot.yml`
