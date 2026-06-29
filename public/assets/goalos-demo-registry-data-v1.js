window.GOALOS_DEMO_REGISTRY_V1 = [
  {
    "name": "Start Here",
    "url": "start-here.html",
    "description": "Three-minute orientation for non-technical users: what GoalOS is, what is real, what is simulated, and where to click next.",
    "category": "onboarding",
    "inputs": [
      "none"
    ],
    "artifacts": [
      "guided role path",
      "site route"
    ],
    "gates": [
      "no-data/no-funds boundary",
      "claim boundary visible"
    ],
    "transitions": [
      "visitor -> informed visitor",
      "informed visitor -> demo route"
    ],
    "role": "UI demo / onboarding layer",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/start-here.html",
    "id": "start-here"
  },
  {
    "name": "Proof Experience Atlas",
    "url": "proof-experience-atlas.html",
    "description": "Unified guided map across the full GoalOS public demo ecosystem.",
    "category": "orchestration",
    "inputs": [
      "user role",
      "tour mode"
    ],
    "artifacts": [
      "Atlas docket",
      "reviewer route",
      "executive summary"
    ],
    "gates": [
      "no network",
      "no user data",
      "human review boundary"
    ],
    "transitions": [
      "fragmented demos -> coherent proof journey",
      "tour -> selected station"
    ],
    "role": "orchestration layer / UI router",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-experience-atlas.html",
    "id": "proof-experience-atlas"
  },
  {
    "name": "Multi-Agent Institution",
    "url": "multi-agent-institution.html",
    "description": "Shows why large multi-agent systems coordinate to maximum effect only when they become proof-governed institutions.",
    "category": "multi-agent coordination",
    "inputs": [
      "mission preset",
      "agent count",
      "quorum",
      "budget discipline",
      "proof controls"
    ],
    "artifacts": [
      "Evidence Docket",
      "review brief",
      "capability package"
    ],
    "gates": [
      "mission contract",
      "claims matrix",
      "validator quorum",
      "risk ledger",
      "human boundary"
    ],
    "transitions": [
      "swarm activity -> accountable institutional state",
      "candidate route -> validated route"
    ],
    "role": "UI demo / orchestration layer / coordination engine",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/multi-agent-institution.html",
    "id": "multi-agent-institution"
  },
  {
    "name": "Proof Gradient Lab",
    "url": "proof-gradient-lab.html",
    "description": "Demonstrates the constitutional rule: score is advisory, gates are mandatory.",
    "category": "selection / evolution",
    "inputs": [
      "candidate upgrade",
      "proof gates",
      "stress level"
    ],
    "artifacts": [
      "Evidence Docket",
      "Selection Certificate",
      "Evolution Ledger entry",
      "Proof Card"
    ],
    "gates": [
      "ProofValid",
      "EvalPass",
      "Risk <= threshold",
      "RollbackReady",
      "CanaryReady",
      "ScopeAuthorized",
      "ChallengeWindowCleared"
    ],
    "transitions": [
      "draft -> candidate",
      "candidate -> canary",
      "canary -> active",
      "candidate -> rejected/held"
    ],
    "role": "scoring module / selection-gate simulator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-gradient-lab.html",
    "id": "proof-gradient-lab"
  },
  {
    "name": "Evidence Docket Theatre",
    "url": "evidence-docket-theatre.html",
    "description": "Turns a public-safe claim into a full reviewable proof room.",
    "category": "evidence / audit",
    "inputs": [
      "claim scenario",
      "docket element toggles",
      "mode"
    ],
    "artifacts": [
      "Evidence Docket JSON",
      "public report",
      "review checklist",
      "claims matrix CSV",
      "proof card"
    ],
    "gates": [
      "claims matrix",
      "environment boundary",
      "baselines",
      "proof packets",
      "evaluator notes",
      "replay path",
      "safety ledger"
    ],
    "transitions": [
      "claim -> docket",
      "docket -> governed decision state",
      "missing evidence -> revise/reject"
    ],
    "role": "receipt/audit module / evidence room",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evidence-docket-theatre.html",
    "id": "evidence-docket-theatre"
  },
  {
    "name": "Proof-to-Action Command Room",
    "url": "proof-to-action-command-room.html",
    "description": "Shows how evidence becomes a governed decision state and review-ready action graph.",
    "category": "decision / action",
    "inputs": [
      "mission",
      "proof controls",
      "stress mode"
    ],
    "artifacts": [
      "Governed Decision State",
      "Action Graph",
      "Chronicle Entry",
      "Capability Package",
      "Executive Brief"
    ],
    "gates": [
      "Evidence Docket",
      "Verifier Report",
      "Risk Ledger",
      "Action Graph",
      "Rollback Conditions",
      "Human Review"
    ],
    "transitions": [
      "proof -> decision state",
      "decision state -> action graph",
      "action graph -> capability package"
    ],
    "role": "orchestration layer / governed decision engine",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-to-action-command-room.html",
    "id": "proof-to-action-command-room"
  },
  {
    "name": "Capability Compounding Lab",
    "url": "capability-compounding-lab.html",
    "description": "Demonstrates that verified work becomes Chronicle memory and reusable capability for harder future missions.",
    "category": "capability compounding",
    "inputs": [
      "mission preset",
      "gate toggles",
      "proof debt stress"
    ],
    "artifacts": [
      "Evidence Docket",
      "Capability Package",
      "Chronicle Entry",
      "Compounding Report",
      "Proof Card"
    ],
    "gates": [
      "proof accepted",
      "validation passed",
      "Chronicle write",
      "capability package emitted",
      "harder mission gate"
    ],
    "transitions": [
      "one-off output -> accepted proof",
      "accepted proof -> capability",
      "capability -> harder mission"
    ],
    "role": "capability-package generator / Chronicle simulator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/capability-compounding-lab.html",
    "id": "capability-compounding-lab"
  },
  {
    "name": "Sovereign Experience Stream Lab",
    "url": "sovereign-experience-stream-lab.html",
    "description": "Shows how accepted proof becomes governed experience that may improve future routing only after gates pass.",
    "category": "experience / learning governance",
    "inputs": [
      "mission scenario",
      "experience gates",
      "reward-hacking stress"
    ],
    "artifacts": [
      "Experience Docket",
      "Grounded Reward Ledger",
      "Router Update Proposal",
      "Temporal Option Card",
      "Review Brief"
    ],
    "gates": [
      "replayable experience",
      "validator-reward separation",
      "reward provenance",
      "risk boundary",
      "human review"
    ],
    "transitions": [
      "proof event -> experience event",
      "experience stream -> router proposal",
      "proposal -> held/review-ready"
    ],
    "role": "scoring module / experience governance layer",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/sovereign-experience-stream-lab.html",
    "id": "sovereign-experience-stream-lab"
  },
  {
    "name": "Proof-Settlement Chronicle Lab",
    "url": "proof-settlement-chronicle-lab.html",
    "description": "Simulates Request -> Escrow -> Execute -> ProofBundle -> Validate -> Settle -> Chronicle with no wallet or funds.",
    "category": "settlement / chronicle",
    "inputs": [
      "public-safe job",
      "settlement gate toggles"
    ],
    "artifacts": [
      "ProofBundle docket",
      "simulated settlement receipt",
      "Chronicle entry",
      "review brief"
    ],
    "gates": [
      "ProofBundle complete",
      "Replay passed",
      "Validator clear",
      "Policy pass",
      "Dispute window closed"
    ],
    "transitions": [
      "job requested -> escrowed",
      "proof accepted -> settlement-ready",
      "failure -> no settlement"
    ],
    "role": "receipt/audit module / settlement simulator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-settlement-chronicle-lab.html",
    "id": "proof-settlement-chronicle-lab"
  },
  {
    "name": "Falsification Gauntlet",
    "url": "falsification-gauntlet.html",
    "description": "Tests whether a claim survives baselines, replay, safety, privacy, cost/risk, delayed-outcome burden, and human review.",
    "category": "falsification / baselines",
    "inputs": [
      "claim under test",
      "scenario preset",
      "proof gates",
      "stress mode"
    ],
    "artifacts": [
      "falsification report",
      "baseline matrix",
      "Evidence Docket",
      "reviewer brief"
    ],
    "gates": [
      "Evidence Docket",
      "Baseline Ladder",
      "Replay Path",
      "Privacy Boundary",
      "Cost/Risk Ledger",
      "Delayed Outcome Plan"
    ],
    "transitions": [
      "claim -> tested claim",
      "claim fails -> reject/revise/hold",
      "claim survives -> human-review-ready"
    ],
    "role": "scoring module / validator module / falsification harness",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/falsification-gauntlet.html",
    "id": "falsification-gauntlet"
  },
  {
    "name": "Proof Run 001 Execution Room",
    "url": "proof-run-001-execution-room.html",
    "description": "Rehearses the first public proof run: mission, gates, docket, replay, validator packet.",
    "category": "proof run execution",
    "inputs": [
      "mission preset",
      "proof gates"
    ],
    "artifacts": [
      "Evidence Docket",
      "Review Brief",
      "Replay Checklist",
      "Validator Packet"
    ],
    "gates": [
      "mission contract",
      "claims matrix",
      "source boundary",
      "baseline comparison",
      "proof packets",
      "replay path",
      "validator report",
      "cost/risk ledger"
    ],
    "transitions": [
      "mission candidate -> execution room",
      "gate pass -> review-ready",
      "gate fail -> remediation"
    ],
    "role": "workflow orchestration / proof-run operator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-execution-room.html",
    "id": "proof-run-001-execution-room"
  },
  {
    "name": "Proof Run 001 Docket Room",
    "url": "proof-run-001-docket.html",
    "description": "Real repository-readiness Evidence Docket generated by autonomous GitHub Action.",
    "category": "real docket / repository audit",
    "inputs": [
      "repository files",
      "site pages",
      "reports",
      "evidence artifacts",
      "legal/privacy/token boundary"
    ],
    "artifacts": [
      "real docket JSON",
      "claims matrix CSV",
      "governed decision state",
      "validator packet",
      "replay path"
    ],
    "gates": [
      "website pages present",
      "code parity modules present",
      "reports present",
      "evidence artifacts present",
      "legal/privacy boundary present",
      "no forbidden browser APIs"
    ],
    "transitions": [
      "architecture -> evidence",
      "evidence -> docket",
      "docket -> reviewer path"
    ],
    "role": "receipt/audit module / repository scanner",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-docket.html",
    "id": "proof-run-001-docket-room"
  },
  {
    "name": "Proof Mission Forge",
    "url": "proof-mission-forge.html",
    "description": "Turns a plain-language objective into a public-safe proof mission package.",
    "category": "mission intake",
    "inputs": [
      "objective",
      "decision to support",
      "risk class",
      "source boundary",
      "proof artifact toggles"
    ],
    "artifacts": [
      "Mission Contract",
      "Evidence Docket plan",
      "Validator Packet",
      "Executive Brief",
      "GitHub-ready issue draft"
    ],
    "gates": [
      "no private data",
      "source boundary",
      "risk class",
      "validator packet",
      "replay checklist"
    ],
    "transitions": [
      "objective -> mission contract",
      "mission package -> GitHub-ready issue"
    ],
    "role": "orchestration layer / mission package generator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-forge.html",
    "id": "proof-mission-forge"
  },
  {
    "name": "Proof Mission Control",
    "url": "proof-mission-control.html",
    "description": "Public operating board showing proof mission readiness, blockers, and next allowed state.",
    "category": "mission operations",
    "inputs": [
      "mission preset",
      "readiness gates"
    ],
    "artifacts": [
      "mission docket",
      "validator packet",
      "GitHub issue draft"
    ],
    "gates": [
      "contract ready",
      "docket ready",
      "review path",
      "replay path",
      "claim boundary"
    ],
    "transitions": [
      "proposal -> contract",
      "contract -> docket",
      "docket -> review",
      "review -> decision"
    ],
    "role": "orchestration layer / mission control",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-mission-control.html",
    "id": "proof-mission-control"
  },
  {
    "name": "External Reviewer Replay Room",
    "url": "external-reviewer-replay-room.html",
    "description": "Makes independent review, replay, dissent, accept/reject/revise easy and browser-local.",
    "category": "external review",
    "inputs": [
      "review package",
      "replay/baseline/validator toggles"
    ],
    "artifacts": [
      "reviewer report",
      "replay checklist",
      "validator attestation",
      "dissent memo",
      "GitHub-ready issue"
    ],
    "gates": [
      "docket",
      "claims",
      "baselines",
      "replay",
      "cost/risk",
      "validator notes",
      "dissent channel"
    ],
    "transitions": [
      "docket -> review",
      "review -> accept/reject/revise/dissent"
    ],
    "role": "validator module / reviewer interface",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/external-reviewer-replay-room.html",
    "id": "external-reviewer-replay-room"
  },
  {
    "name": "Public Proof Ledger",
    "url": "proof-ledger.html",
    "description": "Unified public registry of proof pages, dockets, QA reports, review assets, and replay paths.",
    "category": "registry / ledger",
    "inputs": [
      "repository evidence/**/*.json",
      "reports/**/*.json",
      "public pages",
      "review docs"
    ],
    "artifacts": [
      "public proof ledger index",
      "reviewer route",
      "evidence registry"
    ],
    "gates": [
      "evidence discoverable",
      "reports discoverable",
      "review path discoverable",
      "no-data/no-funds boundary"
    ],
    "transitions": [
      "fragmented artifacts -> public ledger",
      "ledger item -> review path"
    ],
    "role": "receipt/audit module / registry",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-ledger.html",
    "id": "public-proof-ledger"
  },
  {
    "name": "Real-Task Benchmark Bridge",
    "url": "real-task-benchmark-bridge.html",
    "description": "Shows the bridge from demo readiness to real-task benchmark evidence and baseline discipline.",
    "category": "benchmark bridge",
    "inputs": [
      "task family",
      "claim under test",
      "baseline ladder",
      "proof gates"
    ],
    "artifacts": [
      "Benchmark Plan",
      "Baseline Matrix CSV",
      "Evidence Docket Plan",
      "Reviewer Brief"
    ],
    "gates": [
      "real task manifest",
      "equal budget",
      "baselines",
      "ProofBundle",
      "replay",
      "cost/risk ledger",
      "validator report",
      "external review path"
    ],
    "transitions": [
      "demo -> benchmark plan",
      "benchmark plan -> empirical claim candidate"
    ],
    "role": "scoring module / benchmark harness",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/real-task-benchmark-bridge.html",
    "id": "real-task-benchmark-bridge"
  },
  {
    "name": "Proof-Carrying Artifact Foundry",
    "url": "proof-carrying-artifact-foundry.html",
    "description": "Shows how a reusable unit of intelligence earns limited reuse authority only as a proof-carrying artifact.",
    "category": "artifact promotion",
    "inputs": [
      "artifact candidate",
      "artifact class",
      "proof gates",
      "rollback stress"
    ],
    "artifacts": [
      "Proof-Carrying Artifact JSON",
      "Selection Certificate",
      "Rollback Receipt",
      "Evolution Ledger Entry",
      "Reviewer Brief"
    ],
    "gates": [
      "proof history",
      "eval pass",
      "baseline comparison",
      "rollback readiness",
      "scope authorization",
      "challenge window",
      "public/private boundary",
      "replay path"
    ],
    "transitions": [
      "draft -> candidate -> canary -> active",
      "candidate -> rejected/held"
    ],
    "role": "capability-package generator / selection-gate simulator",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-carrying-artifact-foundry.html",
    "id": "proof-carrying-artifact-foundry"
  },
  {
    "name": "Frontier Release Room",
    "url": "frontier-release-room.html",
    "description": "Evidence-governed decision room for frontier AI release, restriction, trusted access, rollback, and restore decisions.",
    "category": "frontier release governance",
    "inputs": [
      "release scenario",
      "access/risk/rollback controls"
    ],
    "artifacts": [
      "release docket",
      "review brief",
      "access matrix"
    ],
    "gates": [
      "identity",
      "capability",
      "safeguards",
      "access",
      "evidence",
      "validators",
      "risk",
      "rollback",
      "chronicle",
      "human authority"
    ],
    "transitions": [
      "release question -> review state",
      "review state -> hold/restrict/restore"
    ],
    "role": "UI demo / governance module",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/frontier-release-room.html",
    "id": "frontier-release-room"
  },
  {
    "name": "Proof Console",
    "url": "console.html",
    "description": "Interactive public console for running proof flights and seeing the proof chain.",
    "category": "proof console",
    "inputs": [
      "mission preset",
      "proof flight controls"
    ],
    "artifacts": [
      "Evidence Docket",
      "review brief",
      "executive summary"
    ],
    "gates": [
      "mission contract",
      "proof flight",
      "decision inspection",
      "human boundary"
    ],
    "transitions": [
      "objective -> proof flight",
      "proof flight -> docket"
    ],
    "role": "UI demo / proof console",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/console.html",
    "id": "proof-console"
  },
  {
    "name": "Try GoalOS",
    "url": "try-goalos.html",
    "description": "Simple browser-local guided demo for users who want to click, run, and download proof artifacts.",
    "category": "onboarding demo",
    "inputs": [
      "scenario selection"
    ],
    "artifacts": [
      "sample Evidence Docket",
      "sample JSON",
      "review brief"
    ],
    "gates": [
      "browser-local",
      "no user data",
      "no network call"
    ],
    "transitions": [
      "visitor -> first proof artifact"
    ],
    "role": "UI demo / onboarding layer",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/try-goalos.html",
    "id": "try-goalos"
  },
  {
    "name": "Docket Builder",
    "url": "docket-builder.html",
    "description": "Browser-local builder for sample Evidence Dockets.",
    "category": "evidence builder",
    "inputs": [
      "public-safe mission archetype"
    ],
    "artifacts": [
      "sample Evidence Docket JSON"
    ],
    "gates": [
      "no form submission",
      "no backend",
      "claim boundary"
    ],
    "transitions": [
      "mission archetype -> docket"
    ],
    "role": "receipt/audit module / evidence builder",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/docket-builder.html",
    "id": "docket-builder"
  },
  {
    "name": "Proof Flight Demo",
    "url": "proof-flight-demo.html",
    "description": "Runs a short browser-local proof flight with proof gates and downloadable output.",
    "category": "proof flight",
    "inputs": [
      "scenario"
    ],
    "artifacts": [
      "Evidence Docket JSON",
      "review brief"
    ],
    "gates": [
      "mission contract",
      "claims matrix",
      "allowed sources",
      "tool boundary",
      "evidence docket",
      "validator report",
      "risk ledger",
      "governed decision",
      "Chronicle",
      "capability package"
    ],
    "transitions": [
      "scenario -> proof flight -> review-ready package"
    ],
    "role": "UI demo / orchestration layer",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-flight-demo.html",
    "id": "proof-flight-demo"
  },
  {
    "name": "Agent Constellation Demo",
    "url": "agent-constellation-demo.html",
    "description": "Visualizes Planner, Executor, Validator, Critic, Chronicle, Risk, QA, and Human Boundary roles.",
    "category": "multi-agent visualization",
    "inputs": [
      "demo launch"
    ],
    "artifacts": [
      "constellation brief"
    ],
    "gates": [
      "role contracts",
      "validator gate",
      "human boundary"
    ],
    "transitions": [
      "agent list -> institution view"
    ],
    "role": "UI demo / orchestration visualization",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/agent-constellation-demo.html",
    "id": "agent-constellation-demo"
  },
  {
    "name": "Proof Card Studio",
    "url": "proof-card-studio.html",
    "description": "Creates shareable browser-local SVG proof cards with no upload or external image service.",
    "category": "communications artifact",
    "inputs": [
      "proof message",
      "card style"
    ],
    "artifacts": [
      "Proof Card SVG"
    ],
    "gates": [
      "no upload",
      "no external service",
      "no user data"
    ],
    "transitions": [
      "message -> shareable proof card"
    ],
    "role": "capability-package generator / communications module",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-card-studio.html",
    "id": "proof-card-studio"
  },
  {
    "name": "Local Autopilot Demo",
    "url": "local-autopilot-demo.html",
    "description": "Shows copyable commands for running local scripts, QA, and demo pack audits.",
    "category": "developer/reviewer replay",
    "inputs": [
      "copy commands"
    ],
    "artifacts": [
      "local run report",
      "QA JSON"
    ],
    "gates": [
      "local execution",
      "no external action",
      "review boundary"
    ],
    "transitions": [
      "website demo -> local replay"
    ],
    "role": "backend workflow guide / replay path",
    "canonical_url": "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/local-autopilot-demo.html",
    "id": "local-autopilot-demo"
  }
];