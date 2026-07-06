# Architecture

The interface uses a single local state object for the simulation. Buttons mutate the gate state:

- Validated Lesson: ProofBundle, replay, validator verdict, Evidence Docket, Chronicle, and future-mission influence pass.
- Missing Replay: the lesson stays in proof debt and cannot propagate.
- Rejected Verdict: the lesson is quarantined and cannot influence future missions.

The charts render from the same state object: propagation network, proof gate funnel, network lift timeline, future mission influence graph, AGI Job table, and artifact workbench.
