# Threat Model

## Primary risks

- Unsupported claims create legal, reputational, or safety exposure.
- Public examples accidentally include private data.
- Autonomous publication ships pages without claim boundaries.
- Evidence Dockets are incomplete but still accepted.
- Validators become ceremonial rather than adversarial.
- Capability packages propagate stale or risky behavior.

## Controls

- Claim boundary appears in README, CLAIMS, docs, and every generated website page.
- QA checks for missing public pages and broken local links.
- Proof kernel blocks restricted claim phrases.
- Settlement requires docket fields, proof bundles, validator reports, risk ledger, and cost ledger.
- Release docs require rollback instructions.

## Residual risk

The repository is a scaffold. Real deployments need independent security review, legal review, privacy review, and production incident response.
