# GoalOS Workflows

Purpose: help maintainers choose safe workflows. Audience: repository maintainers. What to do next: run the V11 workflow first for normal docs/site/release QA.

## Normal release path
| Filename | Purpose | When to run | Inputs | Outputs | Pages | Release | Pack | Risk notes |
|---|---|---|---|---|---|---|---|---|
| `.github/workflows/goalos-repository-website-excellence-v11.yml` | Deterministic repository, docs, site, download, claim, workflow, and release QA | Before PR merge or public Pages deploy | `deploy_pages` true/false | `reports/*.json`, optional Pages artifact | Optional | No | Requires human review; no secrets; no wallet; no transaction |

## Website / navigation / site health
Run only workflows whose names mention site, pages, navigation, or website when changing `public/`, `content/`, or website docs.

## Proof Run / Evidence Docket
Run proof/docket workflows only when evidence files, claims matrices, replay paths, or validator reports changed.

## Docs / QA / release hardening
Use V11 first. Legacy V3–V10 hardening workflows are prior-layer tools and should be run only for their exact layer.

## Demo-specific workflows
Run only for the demo being changed. Do not add network calls, wallet calls, transaction paths, or private-data collection.

## Loop → RSI workflows
Run only when Loop or RSI routes/docs change. OMNI remains allocation/search control only.

## Boundary / legal / token / privacy
Run or review boundary workflows whenever token, privacy, no-data/no-funds, disclaimer, or trust docs change.

## Legacy / prior layer / do not run unless needed
Any workflow with old V3/V4/V5/V6/V7/V8/V9/V10 labels is preserved for history. Prefer V11 unless a maintainer explicitly needs a prior-layer repair.

## Large pack pattern
Large generated packs must be stored as `.goalos/packs/*.zip`. Workflow YAML must stay small, verify the pack exists, unpack it at runtime, run QA, and deploy only after explicit workflow input and human review.

Boundary: No user data. No user funds. No wallet. No transaction. Human review required.
