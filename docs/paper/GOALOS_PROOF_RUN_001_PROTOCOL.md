# GoalOS Proof Run 001 Protocol

## Objective

Convert one AI vendor claim set into a buyer-ready Evidence Docket; create custom AGI Jobs for missing proof; obtain an independent reviewer verdict; admit one reusable skill if the Chronicle Gate passes; build a testnet graph-root packet; and measure whether that skill improves a second mission under equal constraints.

## Candidate validated skill

> Convert AI vendor claims into a buyer-ready proof room.

## Experimental baselines

- B0: manual / null workflow
- B1: report-only LLM
- B2: prompt-library reuse
- B3: ungated agent memory
- B4: GoalOS without Chronicle
- B5: GoalOS with Chronicle but no skill reuse
- B6: full GoalOS loop with VSG and Merkle root

## Required artifacts

```text
00_manifest.json
01_objective.md
02_mission-contract.json
03_proof-level-policy.json
04_claims-matrix.json
05_proof-debt-register.json
06_agi-job-queue.json
07_proofbundle-manifest.json
08_evidence-docket.json
09_replay-manifest.json
10_risk-ledger.json
11_cost-latency-ledger.json
12_validator-report.json
13_chronicle-decision.json
14_validated-skill-passport.json
15_graph-root-packet.json
16_future-mission-brief.json
17_action-graph.csv
18_reviewer-room.html
19_run-trace.md
```

## Primary metrics

- proof debt retired
- provenance coverage
- replay success
- reviewer agreement
- unsupported-claim leakage
- Chronicle false-admission rate
- skill reuse success
- scope violations and drift
- cost, time, and human-review change
- Merkle proof verification
- tamper detection
- unauthorized-write rejection
- privacy leakage
- second-mission quality and risk change

## Success condition

The full GoalOS loop must improve the second mission under controlled baselines without increasing unsupported-claim leakage, privacy exposure, scope drift, or review burden beyond the configured threshold.

## Failure / falsification conditions

The run fails if any of the following occurs:

- unsupported claims enter Chronicle;
- jobs are preloaded rather than mission-specific;
- reviewers cannot reconstruct the decision;
- replay fails under pinned inputs and versions;
- graph roots do not match admitted state;
- altered leaves or proofs still verify;
- private plaintext appears in public artifacts;
- direct-agent authorization is bypassed;
- future-mission improvement vanishes under controlled comparison;
- governance overhead exceeds the value of verified reuse.

## Publication rule

No strong claim is promoted until the public-safe Evidence Docket, external reviewer decision, replay instructions, root-verification record, and baseline comparison are available.
