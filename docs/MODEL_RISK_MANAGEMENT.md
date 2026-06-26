# Model Risk Management

GoalOS treats model outputs as inputs to an institutional control loop, not as final truth.

## Control pattern

1. The model or agent proposes work.
2. The system records the mission, job, tool trace, and evidence.
3. Validators review claims against evidence.
4. Risk ledgers record uncertainty, contradictions, and limitations.
5. Release gates determine what may be published or reused.

## Practical mitigations

- require source provenance for factual claims;
- record contradictions instead of hiding them;
- separate demonstration from production;
- keep human approval for high-impact release states;
- require replay logs or independent review for stronger claims;
- retire capabilities that fail repeated evaluation.
