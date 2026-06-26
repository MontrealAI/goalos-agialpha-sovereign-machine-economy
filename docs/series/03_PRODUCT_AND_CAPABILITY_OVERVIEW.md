# Product and Capability Overview

---
**Project:** GoalOS AGIALPHA Ascension - Sovereign Machine Economy  
**Series:** Institutional Document Series  
**Status:** Public institutional scaffold; not production authorization.  
**Use:** GitHub-ready Markdown, public-site source, board/partner briefing source, and operator onboarding source.  

> **Plain-language promise:** GoalOS is presented as a proof-first operating surface for autonomous AI work. It is designed to help people see what was requested, what work was performed, what evidence was captured, what risks were controlled, what was validated, and what can be reused.

> **Claim boundary:** This document is claim-bounded. It does not assert unsupported AGI achievement, ASI, autonomous legal sovereignty, mainnet production readiness, security audit completion, financial return, legal approval, tax approval, user-fund authorization, or guaranteed adoption. Strong claims require Evidence Dockets, validator reports, replay logs, cost and risk ledgers, and human authorization where appropriate.
---

## Audience

Product leaders, maintainers, partners, technical evaluators, and non-technical operators who need a capability map.

## Purpose

Translate the architecture into clear product surfaces and practical capabilities.


## Product definition

GoalOS AGIALPHA Ascension is a repository-native product system for governing autonomous AI work. It combines documentation, schemas, examples, website generation, proof QA, and operating rituals into one public surface.

## Capability stack

| Capability | Plain meaning | Repository surface |
|---|---|---|
| Mission Contracts | A clear request with boundaries | `schemas/mission_contract.schema.json`, examples |
| Proof Jobs | Work packets that can be inspected | `schemas/proof_job.schema.json` |
| Tool Traces | Records of tool actions and outputs | `schemas/tool_trace.schema.json` |
| ProofBundles | Collected evidence for a claim or job | `schemas/proof_bundle.schema.json` |
| Evidence Dockets | The review packet for important claims | `schemas/evidence_docket.schema.json` |
| Validator Reports | Independent or role-based review | `schemas/validator_report.schema.json` |
| Risk Ledgers | Known risks, controls, residual concerns | `schemas/risk_ledger.schema.json` |
| Governed Decision States | Decision records: pass, revise, reject, hold | standards and examples |
| Settlement Receipts | Proof that accepted work reached a settlement state | `schemas/settlement_receipt.schema.json` |
| Chronicle Entries | Durable institutional memory | `schemas/chronicle_entry.schema.json` |
| Capability Packages | Reusable accepted work | `schemas/capability_package.schema.json` |

## Product surfaces

### 1. Public repository

The repository is the canonical trust surface. It shows the system map, standards, examples, schemas, governance, security posture, launch instructions, and QA reports.

### 2. Generated website

The website is the public front door. It should be generated from repository source and must preserve claim boundaries.

### 3. Proof artifact library

The proof artifacts demonstrate how a mission becomes reviewable. They are examples, not production proof.

### 4. Operator console blueprint

The operator console is the future practical interface: mission creation, evidence review, validator routing, release gates, pause/resume, and Chronicle publishing.

### 5. Trust Center blueprint

The Trust Center is the future review surface for security posture, governance, release history, claim boundaries, and public Evidence Dockets.

## Capability maturity levels

| Level | Name | Description |
|---:|---|---|
| 0 | Concept | Narrative exists, but proof objects are not structured. |
| 1 | Repository scaffold | Docs, schemas, examples, and website are public. |
| 2 | Proof loop demo | A demo mission produces evidence and validator artifacts. |
| 3 | Pilot ready | Real tasks are run with baselines, replay, cost/risk ledgers, and human review. |
| 4 | Institutional ready | Repeatable operating model, trust center, metrics, and governance cadence. |
| 5 | Production candidate | External review, security hardening, legal review, operational SLAs, and release approvals. |

The current repository should be described as a strong scaffold and pilot-readiness surface unless a specific Evidence Docket supports a stronger claim.

## Practical value

GoalOS is valuable because it gives autonomous work the missing institutional wrapper:

```text
bounded request + traceable execution + evidence + validation + release control + reuse
```

That wrapper is the practical bridge from AI output to organizational capability.


## Document control

| Field | Value |
|---|---|
| Owner | MontrealAI / GoalOS maintainers |
| Review cadence | Review before every public release or major repository regeneration |
| Evidence expectation | Update only with traceable sources, reproducible artifacts, or explicitly marked strategy assumptions |
| Publication rule | Keep the claim boundary visible in every public-facing derivative |
