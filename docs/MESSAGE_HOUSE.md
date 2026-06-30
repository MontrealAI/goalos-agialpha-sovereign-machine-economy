# Message House

GoalOS is a public-alpha proof operating surface for autonomous AI work. AI output is abundant; reviewable proof is scarce. The current claim is architecture and repository-readiness, not achieved AGI/ASI, empirical SOTA, production certification, mainnet authorization, or investment value.

## Boundary

No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required. Do not submit personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.

## Token boundary

$AGIALPHA is public-contract identification only and is not available from this repository, website, maintainers, GitHub Issues, demos, workflows, docs, or public dockets. No sale, custody, wallet support, bridge support, exchange support, liquidity support, trading advice, investment advice, legal advice, tax advice, or regulatory advice.

## Reviewer path

Open Proof Run 001, inspect the claims matrix, evidence, validator packet, cost/risk notes, replay path, and governed decision state. File accept, reject, revise, or dissent with the smallest public-safe evidence necessary.

## Required local checks

- `python scripts/validate_repo.py`
- `python scripts/build_site.py`
- `python scripts/verify_site.py`
- `python -m unittest discover -s tests`
- `python -m pytest -q`
- `python -m compileall -q scripts src tests`
- `python scripts/validate_claims.py`
- `python scripts/goalos_docs_quality.py`
- `python scripts/goalos_site_quality.py`
