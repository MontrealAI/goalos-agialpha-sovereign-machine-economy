# How to Review Falsification Gauntlet V1.1

The user-reported bug was: stress mode reverted the claim box to the default preset.

Review checklist:

- Custom claim survives stress toggle.
- Custom claim survives Run gauntlet.
- Stress mode changes baseline matrix.
- Stress mode changes active falsifiers.
- Stress mode changes decision state.
- Downloads contain the custom claim.
- No network, wallet, storage, or beacon APIs are used.
