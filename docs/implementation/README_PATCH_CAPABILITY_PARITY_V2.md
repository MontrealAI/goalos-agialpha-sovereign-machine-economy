<!-- GOALOS-CAPABILITY-PARITY-V2:START -->

## Capability Parity V2

The repository now includes local reference implementation code for the website’s public-alpha capability surface: Mission OS, AEP‑001 objects, Evidence Docket 6.1, Proof Gradient, Frontier Release Room, Multi-Agent Institution, Proof Run 001, and website-to-code parity audit.

Run:

```bash
python -m unittest discover -s tests
python scripts/run_capability_parity_audit.py
python scripts/run_proof_run_001.py
```

Inspect:

- `public/capability-parity.html`
- `reports/capability-parity-audit.json`
- `evidence/proof-run-001/proof-run-001-docket.json`
- `docs/implementation/CAPABILITY_PARITY.md`

Boundary: local public-alpha reference only. No wallet, no transaction, no production activation, no user-fund authorization, no mainnet activation, and no achieved AGI/ASI claim.

<!-- GOALOS-CAPABILITY-PARITY-V2:END -->
