# How to Review the Evolution Ledger Control Room

1. Open `public/evolution-ledger-control-room.html`.
2. Run the ledger sequence.
3. Toggle public/private boundary off and confirm the decision becomes `BLOCK_PRIVACY_BOUNDARY`.
4. Toggle ProofRoot off and confirm the decision becomes `REJECT_NO_PROOF_ROOT`.
5. Toggle RollbackReceipt off and confirm the decision becomes `HOLD_ROLLBACK_REQUIRED`.
6. Raise quorum to 5+ and clear all gates.
7. Download the public ledger entry, selection certificate, rollback receipt, boundary map, and review brief.

Accept only if the page remains browser-local and the downloaded artifacts preserve the no-data/no-funds boundary.
