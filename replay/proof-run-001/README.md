# Replay Proof Run 001 Source-of-Truth V6

Run locally from the repository root:

```bash
python scripts/validate_claims.py
python scripts/goalos_docs_quality.py || true
python scripts/goalos_site_quality.py || true
python -m http.server 8000 --directory public
```

Then open:

```text
http://localhost:8000/index.html
http://localhost:8000/proof-run-001-docket.html
http://localhost:8000/site-health.html
```

Boundary: No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.
