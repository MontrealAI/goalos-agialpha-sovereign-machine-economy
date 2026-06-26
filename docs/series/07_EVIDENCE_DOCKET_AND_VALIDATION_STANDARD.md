# Evidence Docket and Validation Standard

---
**Project:** GoalOS AGIALPHA Ascension - Sovereign Machine Economy  
**Series:** Institutional Document Series  
**Status:** Public institutional scaffold; not production authorization.  
**Use:** GitHub-ready Markdown, public-site source, board/partner briefing source, and operator onboarding source.  

> **Plain-language promise:** GoalOS is presented as a proof-first operating surface for autonomous AI work. It is designed to help people see what was requested, what work was performed, what evidence was captured, what risks were controlled, what was validated, and what can be reused.

> **Claim boundary:** This document is claim-bounded. It does not assert unsupported AGI achievement, ASI, autonomous legal sovereignty, mainnet production readiness, security audit completion, financial return, legal approval, tax approval, user-fund authorization, or guaranteed adoption. Strong claims require Evidence Dockets, validator reports, replay logs, cost and risk ledgers, and human authorization where appropriate.
---

## Audience

Validators, maintainers, auditors, operators, and technical reviewers.

## Purpose

Define the standard for evidence, validation, and review quality.


## What an Evidence Docket is

An Evidence Docket is the review packet for a claim, mission, job, release, or capability. It connects a claim to the proof that supports it.

A useful docket answers:

```text
What is being claimed?
What evidence supports it?
What evidence is missing?
Who reviewed it?
What risks remain?
What decision was made?
```

## Minimum docket contents

| Section | Required content |
|---|---|
| Claim | A specific, bounded statement. |
| Scope | What the claim covers and does not cover. |
| Sources | Links, files, logs, examples, or generated artifacts. |
| ProofBundle | The collected proof objects. |
| Tool Traces | Records of tool or workflow activity. |
| Risk Ledger | Risks, mitigations, residual concerns. |
| Validator Reports | Structured review results. |
| Decision State | Accept, reject, revise, hold, or escalate. |
| Publication Boundary | What can and cannot be said publicly. |

## Evidence quality levels

| Level | Description | Use |
|---:|---|---|
| 0 | Assertion only | Do not use for strong claims. |
| 1 | Source-linked explanation | Suitable for light public copy. |
| 2 | Reproducible artifact | Suitable for technical documentation. |
| 3 | Validated docket | Suitable for strong project claims. |
| 4 | Independent reproduction | Suitable for high-confidence claims. |
| 5 | Operational audit trail | Suitable for production-candidate review. |

## Validator role

A validator is not a cheerleader. A validator asks whether the evidence supports the claim.

A good validator report includes:

- summary of review
- evidence inspected
- tests performed
- risks found
- unresolved questions
- recommendation
- confidence level

## Acceptable decision states

| State | Meaning |
|---|---|
| Accepted | Evidence supports the claim within scope. |
| Accepted with limits | Evidence supports a narrower claim. |
| Revise | More work is required. |
| Hold | Decision paused due to missing evidence or risk. |
| Escalate | Requires higher authority or specialist review. |
| Reject | Evidence does not support the claim. |

## Docket discipline

Never upgrade public language before upgrading the docket. Public claims should follow evidence maturity.

## Docket anti-patterns

Avoid:

- broad claims with narrow evidence
- claims that rely only on aesthetics
- missing cost or risk records
- no validator identity or review date
- no replay path
- no source provenance
- no publication boundary

## Simple docket checklist

Before publishing a strong claim, confirm:

```text
[ ] Claim is specific.
[ ] Evidence is listed.
[ ] Sources are traceable.
[ ] Risks are recorded.
[ ] Validator report exists.
[ ] Decision state is clear.
[ ] Public wording is narrower than or equal to the evidence.
```


## Document control

| Field | Value |
|---|---|
| Owner | MontrealAI / GoalOS maintainers |
| Review cadence | Review before every public release or major repository regeneration |
| Evidence expectation | Update only with traceable sources, reproducible artifacts, or explicitly marked strategy assumptions |
| Publication rule | Keep the claim boundary visible in every public-facing derivative |
