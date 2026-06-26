# Developer and Repository Guide

---
**Project:** GoalOS AGIALPHA Ascension - Sovereign Machine Economy  
**Series:** Institutional Document Series  
**Status:** Public institutional scaffold; not production authorization.  
**Use:** GitHub-ready Markdown, public-site source, board/partner briefing source, and operator onboarding source.  

> **Plain-language promise:** GoalOS is presented as a proof-first operating surface for autonomous AI work. It is designed to help people see what was requested, what work was performed, what evidence was captured, what risks were controlled, what was validated, and what can be reused.

> **Claim boundary:** This document is claim-bounded. It does not assert unsupported AGI achievement, ASI, autonomous legal sovereignty, mainnet production readiness, security audit completion, financial return, legal approval, tax approval, user-fund authorization, or guaranteed adoption. Strong claims require Evidence Dockets, validator reports, replay logs, cost and risk ledgers, and human authorization where appropriate.
---

## Audience

Developers, maintainers, technical reviewers, and operators who need to understand the file structure.

## Purpose

Explain how the repository is organized and how the automation should be maintained.


## Repository map

| Path | Purpose |
|---|---|
| `README.md` | Main public front door. |
| `START_HERE.md` | Non-technical launch entry. |
| `docs/` | Architecture, strategy, operating guides, trust docs. |
| `docs/series/` | This institutional document series. |
| `standards/` | GoalOS object standards. |
| `schemas/` | JSON schemas for proof objects. |
| `examples/` | Example proof artifacts. |
| `scripts/` | Build, QA, validation, hashing, and demo scripts. |
| `src/` | Minimal proof kernel and reusable code. |
| `tests/` | Unit tests. |
| `public/` | Generated GitHub Pages website. |
| `.github/workflows/` | Automation workflows. |
| `reports/` | Generated QA and proof reports. |

## Developer principles

1. Keep public claims tied to artifacts.
2. Prefer explicit schemas over informal JSON.
3. Keep examples small, readable, and valid.
4. Make generated outputs reproducible.
5. Avoid secrets in examples.
6. Validate before publishing.
7. Preserve non-technical readability.

## Recommended checks

Before merging substantial changes, run or verify:

```text
python scripts/validate_repo.py
python scripts/validate_claims.py
python scripts/verify_site.py
python scripts/hash_artifacts.py
python -m pytest
```

The exact script names may vary by repository release, but the principle should remain: validate structure, validate claims, validate website, hash artifacts, and run tests.

## Schema discipline

A schema should be:

- specific enough to prevent ambiguity
- readable enough to explain the object
- stable enough for examples
- versioned when breaking changes occur
- aligned with standards docs

## Commit conventions

Recommended commit prefixes:

```text
docs: update document series
schema: refine evidence docket fields
examples: add validator report example
qa: update claim scan
site: regenerate website
security: clarify public boundary
release: prepare public launch
```

## Pull request review questions

A reviewer should ask:

```text
Does this change improve clarity?
Does it preserve the claim boundary?
Does it introduce unsupported claims?
Does it affect schemas or examples?
Does the site need regeneration?
Does an Evidence Docket need updating?
```

## Automation posture

Automation should help the operator, not surprise them. For public repositories, prefer workflows that:

- can be run manually
- show clear inputs
- avoid unnecessary permissions
- generate reports
- commit only expected files
- make failures readable

## Maintainer standard

A strong repository is not only a file collection. It is an operating system for trust. Keep it navigable, current, and evidence-aligned.


## Document control

| Field | Value |
|---|---|
| Owner | MontrealAI / GoalOS maintainers |
| Review cadence | Review before every public release or major repository regeneration |
| Evidence expectation | Update only with traceable sources, reproducible artifacts, or explicitly marked strategy assumptions |
| Publication rule | Keep the claim boundary visible in every public-facing derivative |
