# Non-Technical Operator Guide

---
**Project:** GoalOS AGIALPHA Ascension - Sovereign Machine Economy  
**Series:** Institutional Document Series  
**Status:** Public institutional scaffold; not production authorization.  
**Use:** GitHub-ready Markdown, public-site source, board/partner briefing source, and operator onboarding source.  

> **Plain-language promise:** GoalOS is presented as a proof-first operating surface for autonomous AI work. It is designed to help people see what was requested, what work was performed, what evidence was captured, what risks were controlled, what was validated, and what can be reused.

> **Claim boundary:** This document is claim-bounded. It does not assert unsupported AGI achievement, ASI, autonomous legal sovereignty, mainnet production readiness, security audit completion, financial return, legal approval, tax approval, user-fund authorization, or guaranteed adoption. Strong claims require Evidence Dockets, validator reports, replay logs, cost and risk ledgers, and human authorization where appropriate.
---

## Audience

Non-technical founders, operators, program leads, reviewers, and anyone using the GitHub web interface.

## Purpose

Explain how to understand and operate the repository without writing code.


## What you are operating

You are not operating a conventional software app. You are operating a public proof surface.

The repository has four jobs:

1. Explain the vision clearly.
2. Show the architecture and standards.
3. Provide examples of proof artifacts.
4. Generate a public website through GitHub automation.

## The five areas to know

| Area | What it means | Where to look |
|---|---|---|
| Front door | The main explanation | `README.md`, `START_HERE.md` |
| Documents | The institutional explanation | `docs/` and `docs/series/` |
| Proof examples | Example evidence objects | `examples/` |
| Standards | The rules for proof objects | `standards/` |
| Automation | The button that builds the repo/site | `.github/workflows/` |

## Your normal workflow

### Step 1: Read the front door

Start with `README.md` and `START_HERE.md`. These explain what the project is and how to run the GitHub Action.

### Step 2: Review public language

Open the documents in `docs/series/`. Make sure the public message is ambitious but not unsupported.

### Step 3: Run the autonomous action

Go to the GitHub **Actions** tab and run the GoalOS autopilot workflow. This creates or refreshes repository content, proof reports, and the public website.

### Step 4: Inspect the generated website

Go to **Settings -> Pages** and open the website URL. Review it as a visitor would.

### Step 5: Use the publication checklist

Before announcing the repository, open `19_PUBLICATION_CHECKLIST.md` and confirm every item.

## What not to edit first

If you are non-technical, avoid editing these until you are comfortable:

```text
schemas/
src/
scripts/
.github/workflows/
```

Start with these instead:

```text
README.md
START_HERE.md
docs/series/
content/site_manifest.json
```

## How to make a safe text edit on GitHub

1. Open the file on GitHub.
2. Click the pencil icon.
3. Make the edit.
4. Scroll to **Commit changes**.
5. Use a clear commit message, such as `docs: refine executive brief`.
6. Commit to a branch if you want review; commit to `main` only for simple safe edits.

## How to judge whether an edit is good

A good edit should pass three tests:

| Test | Question |
|---|---|
| Clarity | Would a smart non-technical reader understand it? |
| Credibility | Does it avoid claims that need evidence but lack proof? |
| Usefulness | Does it help someone operate, review, or trust the project? |

## Operator mindset

Your role is not to make the repository sound bigger. Your role is to make it easier to trust.

The best public posture is:

```text
Clear enough to understand.
Rigorous enough to inspect.
Ambitious enough to matter.
Bounded enough to trust.
```


## Document control

| Field | Value |
|---|---|
| Owner | MontrealAI / GoalOS maintainers |
| Review cadence | Review before every public release or major repository regeneration |
| Evidence expectation | Update only with traceable sources, reproducible artifacts, or explicitly marked strategy assumptions |
| Publication rule | Keep the claim boundary visible in every public-facing derivative |
