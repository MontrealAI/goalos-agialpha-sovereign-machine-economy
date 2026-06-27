# Capability Parity

This repository now includes a local reference implementation for the capabilities presented on the public website.

The implementation is intentionally scoped:

- local Python reference implementation;
- no external model call;
- no wallet;
- no transaction;
- no production activation;
- no user-fund authorization;
- no mainnet activation;
- human review remains required.

Run:

```bash
python -m unittest discover -s tests
python scripts/run_capability_parity_audit.py
python scripts/run_proof_run_001.py
```

Then inspect:

```text
reports/capability-parity-audit.json
evidence/proof-run-001/proof-run-001-docket.json
evidence/proof-run-001/proof-run-001-report.json
```
