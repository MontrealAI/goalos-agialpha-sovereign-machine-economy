# Repository Excellence V8 Preflight

Generated: 2026-06-30T18:27:57Z

## Inventory counts

| Area | Count |
|---|---:|
| Public HTML pages | 134 |
| Reports | 196 |
| Evidence files | 62 |
| Workflows | 52 |
| Issue templates | 50 |
| Docs | 294 |
| Scripts | 117 |

## Preflight QA

- `python -m pytest -q`: passed, 18 tests.
- `python -m compileall -q scripts src tests`: passed.
- `python scripts/validate_repo.py`: initially failed because `.pytest_cache` existed; V8 removes that generated cache.
- `python scripts/validate_claims.py`: passed, 0 blockers.
- `python scripts/verify_site.py`: passed, 0 broken links and 0 boundary gaps.
- `python scripts/goalos_docs_quality.py`: passed.
- `python scripts/goalos_site_quality.py`: passed.
