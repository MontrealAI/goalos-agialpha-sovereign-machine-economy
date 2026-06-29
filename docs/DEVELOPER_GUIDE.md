# Developer guide

## Setup

```bash
git clone https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy.git
cd goalos-agialpha-sovereign-machine-economy
python --version
```

This repository has `pyproject.toml` and `package.json`, but the required local checks are Python scripts. No secrets, wallets, paid APIs, or user accounts are required.

## Checks

```bash
python scripts/goalos_docs_quality.py
python scripts/validate_repo.py
python scripts/build_site.py
python scripts/verify_site.py
python -m unittest discover -s tests
```

## Serve site

```bash
python -m http.server 8000 --directory public
```

Open http://localhost:8000.

## Troubleshooting

If a check fails, inspect the JSON report under `reports/`, fix the smallest scoped issue, rerun the exact command, and include command output in the PR. GitHub Web UI maintainers can edit Markdown, open the Actions tab, run `GoalOS Docs Quality`, and review the uploaded artifact.
> Boundary: public-alpha only. No user data. No user funds. No wallet. No transaction. No production authority. Human review required. $AGIALPHA public contract identification only; $AGIALPHA is not available from us. No investment, trading, tax, legal, wallet, exchange, bridge, liquidity, or regulatory advice.
