# GoalOS AGIALPHA Ascension — Sovereign Machine Economy

**AI creates output. GoalOS creates proof.**

[Website](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/) · [Start Here](public/start-here.html) · [Pathfinder](public/pathfinder.html) · [Public Proof Ledger](public/public-proof-ledger.html) · [Proof Run 001 Docket](public/proof-run-001-docket.html) · [Demo Ecosystem Registry](public/demo-ecosystem-registry.html) · [External Reviewer Replay Room](public/external-reviewer-replay-room.html) · [Site Health](public/site-health.html) · [Trust Boundary](public/trust-boundary.html) · [Token Boundary](public/token-boundary.html)

[![Docs Quality](https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy/actions/workflows/goalos-docs-quality.yml/badge.svg)](https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy/actions/workflows/goalos-docs-quality.yml) [![Site Quality](https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy/actions/workflows/goalos-site-quality.yml/badge.svg)](https://github.com/MontrealAI/goalos-agialpha-sovereign-machine-economy/actions/workflows/goalos-site-quality.yml) ![Public Alpha](https://img.shields.io/badge/Public%20Alpha-claim--bounded-65e4c3) ![No User Data](https://img.shields.io/badge/No%20User%20Data-required-0d1b2f) ![No User Funds](https://img.shields.io/badge/No%20User%20Funds-required-0d1b2f) ![No Wallet](https://img.shields.io/badge/No%20Wallet-required-0d1b2f) ![Human Review Required](https://img.shields.io/badge/Human%20Review-required-f5c542) ![Browser Local](https://img.shields.io/badge/Browser--Local-demos-65e4c3)

## Start in under 60 seconds

1. Open [Start Here](public/start-here.html).
2. Use [Pathfinder](public/pathfinder.html) to choose a route.
3. Review [Proof Run 001](public/proof-run-001-docket.html) or browse the [Demo Registry](public/demo-ecosystem-registry.html).
4. Read [Trust Boundary](public/trust-boundary.html) and [No Data / No Funds](public/no-data-no-funds.html) before filing feedback.

## What this is

GoalOS is a public-alpha proof operating surface for autonomous AI work: it turns objectives into mission contracts, evidence dockets, governed decision states, reviewer paths, and reusable capability packages.

## What this is not

It is not achieved AGI/ASI, empirical SOTA, production certification, mainnet authorization, legal/tax/investment advice, wallet software, token distribution, or a system authorized to move user data or user funds.

## 30-second explanation

A model can answer and an agent can act, but an institution must prove. GoalOS preserves the boundary between private intelligence and public proof so reviewers can inspect claims, artifacts, gates, replay paths, and rollback readiness.

## 3-minute explanation

The canonical loop is Objective → Mission Contract → Autonomous Work → Verification → Evidence Docket → Governed Decision State → Action Graph → Chronicle → Reusable Capability. Scores are advisory; gates are mandatory. The current release focuses on repository-readiness, route health, public downloads, claim scanning, proof navigation, issue/PR safety, and human-review discipline.

## Choose your path

| You are | Start with | Outcome |
|---|---|---|
| Non-technical | [Non-Technical Guide](docs/NON_TECHNICAL_GUIDE.md) | Know what to click and what not to paste. |
| Trying demos | [Demo Ecosystem](docs/DEMO_ECOSYSTEM.md) | Understand inputs, outputs, gates, and next states. |
| Reviewing proof | [Reviewer Guide](docs/REVIEWER_GUIDE.md) | File accept/reject/revise/dissent. |
| Proposing a mission | [Mission Forge](docs/MISSION_FORGE.md) | Draft a bounded proof mission. |
| Developer | [Developer Guide](docs/DEVELOPER_GUIDE.md) | Run checks and serve the static site. |
| External reviewer | [External Review](docs/EXTERNAL_REVIEW.md) | Inspect public proof without private data. |
| Institution | [Executive Brief](docs/EXECUTIVE_BRIEF.md) | Understand readiness and limits. |

## Core doctrine

No proof, no evolution. No eval, no propagation. No rollback, no release. No Evidence Docket, no strong empirical claim. No ProofBundle, no settlement. Private intelligence stays private; public proof becomes inspectable.

## Current release health

| Layer | Status |
|---|---|
| Current label | Repository Excellence V8 |
| Source of truth | [release-state.json](content/goalos/release-state.json) |
| Public pages | 134 |
| Claim scan | 0 blockers in final local QA |
| Route health | 0 broken internal HTML links in final local QA |
| Download health | 0 broken public downloads in final local QA |
| Human review | Required |

## Website map

Start → Pathfinder → Atlas → Registry → Proof Ledger → Mission Forge → Mission Control → Proof Run 001 → External Reviewer Replay → Site Health. See [Website Map](docs/WEBSITE_MAP.md).

## Public proof journey

Open the docket, inspect the claims matrix, check evidence and validator packets, replay where available, review cost/risk and rollback notes, then file accept, reject, revise, or dissent.

## Demo ecosystem

The machine-readable registry is [content/goalos/demo-ecosystem-registry.json](content/goalos/demo-ecosystem-registry.json) with `routes[]` and compatible `demos[]` navigation.

<details><summary>Core routes</summary>

- [Start Here](public/start-here.html)
- [Pathfinder](public/pathfinder.html)
- [Website Operating System](public/website-operating-system.html)
- [Demo Ecosystem Registry](public/demo-ecosystem-registry.html)
- [Public Proof Ledger](public/public-proof-ledger.html)
- [Proof Run 001 Docket](public/proof-run-001-docket.html)
- [External Reviewer Replay Room](public/external-reviewer-replay-room.html)
- [Trust Boundary](public/trust-boundary.html)
- [Token Boundary](public/token-boundary.html)

</details>

## Proof Run 001

Proof Run 001 is a public-alpha proof docket for reviewer inspection. It is not production authorization and does not establish achieved AGI/ASI or empirical SOTA.

## Evidence Dockets and reports

Evidence lives under `evidence/`, public-safe mirrored downloads under `public/downloads/`, and QA/final reports under `reports/`.

## Reviewer / validator path

Use [docs/REVIEWER_GUIDE.md](docs/REVIEWER_GUIDE.md), [docs/VALIDATOR_GUIDE.md](docs/VALIDATOR_GUIDE.md), and the GitHub issue templates. Keep feedback public-safe.

## Developer quickstart

```bash
python -m pytest -q
python -m compileall -q scripts src tests
python scripts/validate_repo.py
python scripts/build_site.py
python scripts/verify_site.py
python scripts/validate_claims.py
python scripts/goalos_docs_quality.py
python scripts/goalos_site_quality.py
python -m http.server 8000 --directory public
```

## GitHub Web UI maintainer instructions

Open Actions, run docs/site/repository quality workflows with `workflow_dispatch`, download artifacts, compare them with `reports/`, and merge only after human review confirms boundaries remain intact.

## Claim boundaries

Do not claim achieved AGI, achieved ASI, empirical SOTA, production certification, external audit completion, mainnet authorization, production remediation, guaranteed ROI, revenue, yield, returns, investability, legal advice, financial advice, tax advice, trading advice, regulatory advice, medical advice, security advice, safety advice, or compliance advice.

## No data / no funds / privacy boundary

No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required. Do not paste personal, customer, confidential, regulated, credential, wallet, private-key, seed phrase, payment, trade-secret, proprietary, or privileged data.

## $AGIALPHA token boundary

$AGIALPHA may appear only as public-contract identification. It is not available from this repository, website, maintainers, GitHub Issues, demos, workflows, docs, or public dockets. No sale, custody, brokerage, recommendation, market support, listing, liquidity, bridge, exchange, wallet support, trading advice, investment advice, legal advice, tax advice, or regulatory advice.

## Security and responsible disclosure

See [SECURITY.md](SECURITY.md). Do not include secrets or sensitive data in reports.

## Contributing safely

See [CONTRIBUTING.md](CONTRIBUTING.md). Prefer small, reviewable changes with clear rollback.

## Research canon

See [REFERENCES.md](REFERENCES.md) and [docs/RESEARCH_CANON.md](docs/RESEARCH_CANON.md): AEP-001, GoalOS Mission OS, and AGI ALPHA substrate doctrine.

## Roadmap

Next burden: real tasks, baselines, replay, validator reports, cost/risk ledgers, delayed outcomes, and independent review.

## Release history

Earlier V3–V7 release-hardening layers are preserved in [CHANGELOG.md](CHANGELOG.md). The current editorial and QA layer is Repository Excellence V8.

## Maintainer checklist

- Run required local checks.
- Confirm 0 claim blockers, 0 broken internal HTML links, 0 root-escape artifact links, 0 broken public downloads.
- Confirm issue templates and PR template preserve boundaries.
- Confirm release-state, site-health, proof docket, and reports agree.
- Require human review before publication.

## GoalOS Loop Contract Lab V1

**Write the loop, not the prompt.**

The Loop Contract Lab adds a browser-local public demo showing how long-running agent work becomes reviewable through role contracts, disk state, readable traces, restart semantics, evaluator independence, Evidence Docket planning, and bottleneck reporting.

Open: `public/loop-contract-lab.html`

Boundary: No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.


<!-- GOALOS_LOOP_FLIGHT_RECORDER_V1_START -->
## GoalOS Loop Flight Recorder V1

**Write the loop. Not the prompt.**

New browser-local public demonstration: [`loop-flight-recorder.html`](public/loop-flight-recorder.html).

It shows how long-running agent loops become review-ready by separating roles, writing state to disk, reading traces, restarting cleanly, scoring subjective quality, deleting harness overhead, exposing the next bottleneck, and emitting downloadable review artifacts.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
<!-- GOALOS_LOOP_FLIGHT_RECORDER_V1_END -->

## GoalOS Loop Bottleneck Observatory V1

**The bottleneck always moves.** This browser-local public demo shows how a long-running GoalOS loop exposes its next bottleneck: contract, roles, disk state, trace reading, restartability, evaluator independence, taste rubric, harness overhead, or proof boundary.

Open: [`public/loop-bottleneck-observatory.html`](public/loop-bottleneck-observatory.html)

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.

## GoalOS From Loop to RSI Governance Lab V1

**Page:** [`public/from-loop-to-rsi-governance.html`](public/from-loop-to-rsi-governance.html)

A browser-local public demo showing how a restartable loop becomes deterministic RSI governance: `TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE`.

It demonstrates the rule: **search control is not outcome authority**. OMNI-style interestingness may allocate exploration, but promotion still requires risk, evidence, baseline, replay, persistence, dossier, rollback, and human-review gates.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.

<!-- GOALOS_FROM_LOOP_TO_RSI_SOVEREIGN_CONSOLE_V2:START -->

## From Loop to RSI Sovereign Console V2

A browser-local public demonstration showing how restartable loops become deterministic RSI governance: schema-bound artifacts, state hashes, ECI evidence discipline, baseline gates, Move-37 dossiers, and Architect/Validator Council review.

- Public page: `public/from-loop-to-rsi-sovereign-console.html`
- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
- Decision states include `RSI_REVIEW_READY`, `MOVE37_DOSSIER_REVIEW_READY`, `REJECT_OMNI_OUTCOME_AUTHORITY`, and `BLOCK_PRIVACY_BOUNDARY`.

<!-- GOALOS_FROM_LOOP_TO_RSI_SOVEREIGN_CONSOLE_V2:END -->

<!-- GOALOS_FROM_LOOP_TO_RSI_STATE_CAPACITY_V3 -->
## New public demo: From Loop to RSI State-Capacity Command Room V3

**Build the governance institution first.**

Open: [`public/from-loop-to-rsi-state-capacity.html`](public/from-loop-to-rsi-state-capacity.html)

This browser-local demo shows how a long-running agent loop becomes deterministic RSI governance: drift sentinel, ECI evidence, baseline gate, Move-37 dossier, Architect / Validator Council, and governed decision state.
