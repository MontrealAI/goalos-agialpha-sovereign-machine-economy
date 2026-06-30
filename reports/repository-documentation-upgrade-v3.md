# Repository Documentation Upgrade v3

Status: implemented with blocking site-boundary failures intentionally exposed.

## Summary

Upgraded repository-readiness documentation surfaces, routeable demo metadata, social preview assets, Mermaid diagrams, local site QA automation, machine-readable repository indexes, and public-alpha QA reports while preserving claim boundaries.

## QA checks run

| Command | Result |
|---|---|
| `python scripts/goalos_docs_quality.py` | passed |
| `python scripts/goalos_site_quality.py` | failed as intended: 35 blocking `boundary_link_gap` issues are now surfaced |
| `python scripts/validate_repo.py` | previously passed with warnings |
| `python scripts/build_site.py` | previously passed; generated public pages |
| `python scripts/verify_site.py` | previously failed on existing generated page claim-boundary coverage and short search/start pages |
| `python -m unittest discover -s tests` | passed |
| `python -m compileall scripts src` | passed |

## Inline review fixes

- Missing no-data/no-funds/human-review boundary copy is now a blocking site-quality failure.
- Local `public/assets/**/*.js` files and locally referenced script assets are scanned for forbidden browser APIs.
- `fetch(` is now included in forbidden browser network-call detection.

## Known limitations

- Existing public pages need a compact public-alpha boundary footer or equivalent link before `scripts/goalos_site_quality.py` and `scripts/verify_site.py` can pass together.

## Next recommended move

Patch the site generator templates so every generated page includes a compact public-alpha boundary footer and then rerun `python scripts/build_site.py`, `python scripts/goalos_site_quality.py`, and `python scripts/verify_site.py`.
