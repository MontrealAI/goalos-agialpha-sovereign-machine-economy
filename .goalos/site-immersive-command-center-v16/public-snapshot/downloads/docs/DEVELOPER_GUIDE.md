# Developer Guide

Purpose: run and maintain the repository locally. Audience: developers and release maintainers. What to do next: run the QA commands below. Related reports/scripts: `reports/*.json`, `scripts/*.py`.

```bash
git clone https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy.git
cd goalos-agialpha-sovereign-machine-economy
python -m http.server 8000 -d public
python -m compileall -q scripts src tests
python -m pytest -q
python scripts/validate_claims.py
python scripts/verify_site.py
python scripts/goalos_docs_quality.py
python scripts/goalos_site_quality.py
python scripts/goalos_download_health.py
python scripts/goalos_workflow_quality.py
python scripts/goalos_release_health.py
```

Troubleshooting: if a workflow reports YAML max expression length, remove inline payloads and store generated packs under `.goalos/packs/*.zip`; workflow YAML should verify and unpack the pack at runtime. Add demos by updating `public/*.html`, `content/goalos/demo-ecosystem-registry.json`, sitemap/search if used, docs, and QA reports.


## Boundary reminder
No user data. No user funds. No wallet. No transaction. No production authority. Human review required. Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, trade-secret, proprietary, or user-funds data. $AGIALPHA is public-contract identification only and is not available from this repository, website, maintainers, GitHub Issues, demos, or docs.
