# Site Health

GoalOS site health is a deterministic, local-only route and boundary check for the public-alpha website. It does not use network calls, secrets, wallets, analytics, telemetry, user accounts, or fund movement.

## What it checks

- Local `.html` links resolve inside `public/`.
- Key public pages exist: Start, Pathfinder, Registry, Proof Ledger, Proof Run 001, Reviewer Room, Site Health, Trust Boundary, Token Boundary, No Data / No Funds.
- `404.html` exists and is treated as a system page, not a demo.
- HTML pages have non-empty titles and viewport metadata.
- Search index and sitemap files are parseable when present.
- Boundary language remains visible or linked: no user data, no user funds, and human review required.

## Command

```bash
python scripts/goalos_site_quality.py
```

Reports are written to `reports/site-quality.json` and `reports/site-route-health.json`.
