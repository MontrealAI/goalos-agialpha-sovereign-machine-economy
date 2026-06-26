# Security Policy

## Public-safety posture

This repository must not contain:

- private keys;
- seed phrases;
- API keys;
- treasury credentials;
- customer data;
- private buyer deliverables;
- live user-fund automation;
- production activation secrets.

## Reporting

Open a private security advisory on GitHub if available, or contact the maintainers through the repository owner’s preferred channel.

## Autopilot workflow safety

The autopilot is designed to generate documentation, examples, schemas, reports, and a static website. It does not deploy contracts, move funds, request secrets, or activate production systems.

## Operator checklist

Before publishing:

- verify no secrets were committed;
- review `CLAIMS.md`;
- review `reports/autopilot-summary.md`;
- review `reports/site-qa.json`;
- confirm GitHub Pages contains only public-safe content.
