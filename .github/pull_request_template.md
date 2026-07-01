## Summary

## Changed public pages

## Changed docs

## Changed workflows

## Changed evidence/reports

## Screenshots if UI changed

## QA commands run
- [ ] `python -m compileall -q scripts src tests`
- [ ] `python -m pytest -q`
- [ ] `python scripts/validate_claims.py`
- [ ] `python scripts/verify_site.py`
- [ ] `python scripts/goalos_docs_quality.py`
- [ ] `python scripts/goalos_site_quality.py`
- [ ] `python scripts/goalos_download_health.py`
- [ ] `python scripts/goalos_workflow_quality.py`
- [ ] `python scripts/goalos_release_health.py`

## Boundary checklist
- [ ] No user data.
- [ ] No user funds.
- [ ] No wallet/transaction path.
- [ ] No unsupported AGI/ASI/SOTA claims.
- [ ] No investment/trading/legal/tax advice.
- [ ] No new forbidden browser APIs.
- [ ] No giant inline workflow payloads.
- [ ] No broken public downloads.
- [ ] Human review required.

## Rollback notes
