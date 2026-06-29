# Developer Guide

```bash
git clone https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy.git
cd goalos-agialpha-sovereign-machine-economy
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python scripts/goalos_docs_quality.py
python scripts/validate_repo.py
python scripts/build_site.py
python scripts/verify_site.py
python -m unittest discover -s tests
python -m http.server 8000 --directory public
```

Troubleshooting: if a workflow is missing, check Actions permissions; if Pages fails, check Settings > Pages; if a badge lags, wait for GitHub cache; if a link breaks, run docs QA; if Python is missing, install Python 3.11+.

## Public-alpha boundary

No user data. No user funds. No wallet. No transaction. No production authority. Human review required. Browser-local demos remain browser-local unless a page explicitly says otherwise. Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, trade-secret, or proprietary data. $AGIALPHA public contract identification only; $AGIALPHA is not available from us. No sale, custody, wallet support, bridge support, exchange support, market making, liquidity support, recommendation, trading advice, financial advice, tax advice, legal advice, or regulatory advice. Third parties are solely responsible for their own review and compliance.

