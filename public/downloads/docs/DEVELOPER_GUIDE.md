# Developer Guide

Public-alpha boundary: no user data, no user funds, no wallet, no transaction, no production authority, browser-local where applicable, and human review required. Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, trade-secret, proprietary, or user-funds data. $AGIALPHA is public-contract identification only and is not available from this repository, website, maintainers, GitHub Issues, demos, or documentation. No trading, investment, financial, tax, legal, bridge, exchange, or regulatory advice.

## Purpose

This document is part of the V9 public-alpha institutional launch surface for GoalOS AGIALPHA Ascension. It gives a claim-bounded, review-ready path for users, maintainers, developers, validators, and institutions.

## Fast path

- Website: https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/index.html
- Pathfinder: ../public/pathfinder.html
- Site Health: ../public/site-health.html
- Proof Run 001: PROOF_RUN_001.md
- Demo Registry: DEMO_ECOSYSTEM.md

## Operating guidance

1. Keep claims inside evidence boundaries.
2. Preserve no-data, no-funds, no-wallet, no-transaction boundaries.
3. Treat scores as advisory and gates as mandatory.
4. Require replay, validator review, rollback readiness, and dissent paths before any stronger release claim.

## Local commands

```bash
python -m pytest -q
python -m compileall -q scripts src tests
python scripts/validate_repo.py
python scripts/validate_claims.py
python scripts/verify_site.py
python scripts/goalos_docs_quality.py
python scripts/goalos_site_quality.py
python scripts/goalos_public_downloads.py
python -m http.server 8000 --directory public
```

## Troubleshooting

If a workflow is missing, invalid, has expression length exceeded, or a pack file is missing, open Actions, read the failing line, and prefer pack-based workflows under `.goalos/packs/`. Quote `$AGIALPHA` in shell contexts so it is not treated as an environment variable.
