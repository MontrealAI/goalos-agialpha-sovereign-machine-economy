window.GOALOS_AGENT_V36 = {
  "routes": [
    {
      "title": "AGI Agent Command Center V36",
      "url": "agi-agent-command-center.html",
      "category": "AGI Agents",
      "summary": "One-box meta-agentic AGI agent mission surface."
    },
    {
      "title": "AGI Agent Use Cases",
      "url": "agi-agent-use-cases.html",
      "category": "AGI Agents",
      "summary": "Solved end-to-end AGI Agent and AGI Node playbooks."
    },
    {
      "title": "GoalOS Mission Studio",
      "url": "goalos.html",
      "category": "Mission",
      "summary": "Tell GoalOS what you want and get a proof path."
    },
    {
      "title": "Ask GoalOS",
      "url": "ask-goalos.html",
      "category": "Concierge",
      "summary": "Browser-local route assistant and question window."
    },
    {
      "title": "Validation Control Tower",
      "url": "validation-control-tower.html",
      "category": "Validation",
      "summary": "Human, AGI Node, Hybrid, or Council validation path."
    },
    {
      "title": "Mainnet Contract Atlas",
      "url": "mainnet-contract-atlas.html",
      "category": "Contracts",
      "summary": "48 Ethereum Mainnet contracts as one institutional proof rail."
    },
    {
      "title": "Proof Run 001 Docket",
      "url": "proof-run-001-docket.html",
      "category": "Evidence",
      "summary": "Repository readiness Evidence Docket."
    },
    {
      "title": "Loop to RSI State Capacity",
      "url": "from-loop-to-rsi-state-capacity.html",
      "category": "Loop \u2192 RSI",
      "summary": "Loop becomes deterministic invention governance."
    },
    {
      "title": "Trust Boundary",
      "url": "trust-boundary.html",
      "category": "Boundary",
      "summary": "No data, no funds, no wallet, human-review boundary."
    },
    {
      "title": "Token Boundary",
      "url": "token-boundary.html",
      "category": "Boundary",
      "summary": "$AGIALPHA public contract identification only; not available from GoalOS."
    },
    {
      "title": "Demo Registry",
      "url": "demo-ecosystem-registry.html",
      "category": "Navigation",
      "summary": "All public demos and proof routes."
    },
    {
      "title": "Site Map",
      "url": "site-map.html",
      "category": "Navigation",
      "summary": "Complete all-pages route inventory."
    },
    {
      "title": "Search",
      "url": "search.html",
      "category": "Navigation",
      "summary": "Browser-local site search."
    }
  ],
  "agents": [
    {
      "id": "ARCH",
      "name": "Architect Agent",
      "role": "Frames objective, proof burden, and institutional authority.",
      "lane": "Strategy"
    },
    {
      "id": "PLAN",
      "name": "Planner Agent",
      "role": "Turns objective into a Mission Contract and bounded task graph.",
      "lane": "Mission"
    },
    {
      "id": "RES",
      "name": "Research Agent",
      "role": "Maps public-safe sources, assumptions, and unknowns.",
      "lane": "Evidence"
    },
    {
      "id": "BUILD",
      "name": "Builder Agent",
      "role": "Creates artifacts, pages, packets, demos, and implementation plans.",
      "lane": "Execution"
    },
    {
      "id": "VERIFY",
      "name": "Verifier Agent",
      "role": "Checks claims, boundaries, evidence completeness, and replay readiness.",
      "lane": "Validation"
    },
    {
      "id": "NODE",
      "name": "AGI Node Worker",
      "role": "Prepares deterministic runtime handoff, work unit, and replay requirements.",
      "lane": "Runtime"
    },
    {
      "id": "VAL",
      "name": "AGI Node Validator",
      "role": "Runs deterministic public-safe checks and produces attestation-ready output.",
      "lane": "Validation"
    },
    {
      "id": "SENT",
      "name": "Sentinel Agent",
      "role": "Monitors drift, boundary risk, unsafe requests, and escalation triggers.",
      "lane": "Safety"
    },
    {
      "id": "DOCKET",
      "name": "Evidence Docket Agent",
      "role": "Packages claims, baselines, proof packets, ledgers, and review path.",
      "lane": "Proof"
    },
    {
      "id": "CHRON",
      "name": "Chronicle Agent",
      "role": "Turns accepted work into institutional memory and reusable capability.",
      "lane": "Memory"
    },
    {
      "id": "HUMAN",
      "name": "Human Operator",
      "role": "Approves high-impact, sensitive, external, or publication decisions.",
      "lane": "Authority"
    },
    {
      "id": "COUNCIL",
      "name": "Architect / Validator Council",
      "role": "Reviews high-novelty RSI, Move-37, or governance-changing claims.",
      "lane": "Governance"
    }
  ],
  "playbooks": [
    {
      "id": "PB01",
      "title": "Understand the 48 Ethereum Mainnet contracts",
      "prompt": "I want AGI agents to help me understand the 48 Ethereum Mainnet contracts in plain English, with the proof rail, roles, and review path.",
      "intent": "Mainnet Contract Atlas",
      "agents": [
        "ARCH",
        "RES",
        "DOCKET",
        "VAL"
      ],
      "authority": "AGI Node precheck + human review",
      "outputs": "Contract learning map, proof rail briefing, token boundary reminder, reviewer packet",
      "routes": [
        "mainnet-contract-atlas.html",
        "mainnet-proof-rail.html",
        "contract-academy.html",
        "token-boundary.html"
      ]
    },
    {
      "id": "PB02",
      "title": "Run a public-safe proof mission",
      "prompt": "I want to run a public-safe proof mission from objective to Evidence Docket without user data, funds, wallet, or external action.",
      "intent": "Proof Mission",
      "agents": [
        "PLAN",
        "BUILD",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Hybrid",
      "outputs": "Mission Contract, claims matrix, Evidence Docket plan, action graph",
      "routes": [
        "goalos.html",
        "proof-run-001-docket.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB03",
      "title": "Evaluate an AI vendor or tool",
      "prompt": "I want AGI agents to evaluate an AI vendor using evidence, not marketing claims, and produce a reviewer-ready decision brief.",
      "intent": "Vendor Evidence Review",
      "agents": [
        "ARCH",
        "RES",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Human final review",
      "outputs": "Vendor claims matrix, source map, risk ledger, reviewer brief",
      "routes": [
        "validation-control-tower.html",
        "demo-ecosystem-registry.html",
        "trust-boundary.html"
      ]
    },
    {
      "id": "PB04",
      "title": "Design a controlled pilot program",
      "prompt": "I want to design a controlled pilot program where every serious pilot ends with an Evidence Docket and a decision state.",
      "intent": "Controlled Pilot",
      "agents": [
        "PLAN",
        "BUILD",
        "VERIFY",
        "DOCKET",
        "CHRON"
      ],
      "authority": "Hybrid",
      "outputs": "Pilot contract, success/failure criteria, review gates, controlled rollout plan",
      "routes": [
        "pilot-program.html",
        "goalos.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB05",
      "title": "Understand Loop \u2192 RSI governance",
      "prompt": "I want to understand how long-running loops become deterministic RSI governance with replay, baselines, and dossiers.",
      "intent": "Loop to RSI",
      "agents": [
        "ARCH",
        "PLAN",
        "SENT",
        "DOCKET",
        "COUNCIL"
      ],
      "authority": "Council for high novelty",
      "outputs": "RSI path, baseline gate, Move-37 dossier requirements",
      "routes": [
        "from-loop-to-rsi-state-capacity.html",
        "loop-bottleneck-observatory.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB06",
      "title": "Check privacy, token, and data boundaries",
      "prompt": "I want AGI agents to check the privacy, token, and no-data boundaries across the website and explain what is safe to submit.",
      "intent": "Boundary Audit",
      "agents": [
        "SENT",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "AGI Node precheck",
      "outputs": "Boundary checklist, red flags, recommended pages",
      "routes": [
        "trust-boundary.html",
        "token-boundary.html",
        "privacy.html",
        "data-boundary.html"
      ]
    },
    {
      "id": "PB07",
      "title": "Prepare a validator council review",
      "prompt": "I want to prepare an Architect / Validator Council review packet for a strategic GoalOS claim.",
      "intent": "Council Review",
      "agents": [
        "ARCH",
        "VERIFY",
        "DOCKET",
        "COUNCIL"
      ],
      "authority": "Council",
      "outputs": "Council packet, dossier class, open questions, gating checklist",
      "routes": [
        "validation-control-tower.html",
        "validator-council-arena.html",
        "from-loop-to-rsi-state-capacity.html"
      ]
    },
    {
      "id": "PB08",
      "title": "Defensive cybersecurity proof mission",
      "prompt": "I want to plan a defensive cybersecurity proof mission for repo-owned assets only, with no secrets, no external scans, and human review.",
      "intent": "Defensive Security",
      "agents": [
        "SENT",
        "RES",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Hybrid",
      "outputs": "Safe scope, risk ledger, evidence plan, remediation review path",
      "routes": [
        "validation-control-tower.html",
        "trust-boundary.html",
        "proof-run-001-docket.html"
      ]
    },
    {
      "id": "PB09",
      "title": "Proof-backed procurement record",
      "prompt": "I want a proof-backed procurement record that turns vendor options into a decision state and reviewer brief.",
      "intent": "Procurement",
      "agents": [
        "PLAN",
        "RES",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Human final review",
      "outputs": "Procurement claims matrix, tradeoff table, risk ledger, decision memo",
      "routes": [
        "goalos.html",
        "validation-control-tower.html",
        "proof-run-001-docket.html"
      ]
    },
    {
      "id": "PB10",
      "title": "Audit website and repository completeness",
      "prompt": "I want AGI agents to audit website and repository completeness, route integrity, docs, claim boundaries, and missing pages.",
      "intent": "Site and Repo QA",
      "agents": [
        "RES",
        "BUILD",
        "VERIFY",
        "SENT"
      ],
      "authority": "AGI Node validator",
      "outputs": "Route health, missing page report, QA packet, remediation actions",
      "routes": [
        "site-health.html",
        "site-map.html",
        "search.html"
      ]
    },
    {
      "id": "PB11",
      "title": "Executive decision brief",
      "prompt": "I want AGI agents to turn a strategic question into an executive decision brief with evidence, risk, and action graph.",
      "intent": "Executive Brief",
      "agents": [
        "ARCH",
        "RES",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Human final review",
      "outputs": "Executive brief, decision state, action graph, evidence docket outline",
      "routes": [
        "goalos.html",
        "validation-control-tower.html",
        "demo-ecosystem-registry.html"
      ]
    },
    {
      "id": "PB12",
      "title": "External reviewer replay",
      "prompt": "I want to prepare an external reviewer replay package for a public claim or demo.",
      "intent": "Reviewer Replay",
      "agents": [
        "VERIFY",
        "DOCKET",
        "SENT",
        "HUMAN"
      ],
      "authority": "Hybrid",
      "outputs": "Replay checklist, artifacts, baseline questions, reviewer brief",
      "routes": [
        "proof-run-001-docket.html",
        "external-reviewer-replay-room.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB13",
      "title": "AGI Node handoff packet",
      "prompt": "I want to create an AGI Node handoff packet for deterministic public-safe checks and validation.",
      "intent": "AGI Node Handoff",
      "agents": [
        "NODE",
        "VAL",
        "SENT",
        "DOCKET"
      ],
      "authority": "AGI Node validator",
      "outputs": "Node handoff JSON, replay requirements, validator tasks, authority limits",
      "routes": [
        "agi-agent-command-center.html",
        "validation-control-tower.html",
        "agi-node-use-cases.html"
      ]
    },
    {
      "id": "PB14",
      "title": "Mainnet proof-rail learning path",
      "prompt": "I want a non-technical learning path for the Mainnet proof rail and how it connects to agents, jobs, validation, and dockets.",
      "intent": "Mainnet Learning",
      "agents": [
        "RES",
        "DOCKET",
        "VAL"
      ],
      "authority": "AGI Node precheck",
      "outputs": "Learning path, route cards, glossary, token boundary",
      "routes": [
        "mainnet-contract-atlas.html",
        "mainnet-proof-rail.html",
        "contract-academy.html"
      ]
    },
    {
      "id": "PB15",
      "title": "Capability reuse promotion",
      "prompt": "I want to see when accepted work becomes reusable capability and what gates it must pass.",
      "intent": "Capability Reuse",
      "agents": [
        "VERIFY",
        "DOCKET",
        "CHRON",
        "COUNCIL"
      ],
      "authority": "Hybrid",
      "outputs": "Capability package stub, selection gates, rollback requirements",
      "routes": [
        "capability-compounding-lab.html",
        "validation-control-tower.html",
        "proof-run-001-docket.html"
      ]
    },
    {
      "id": "PB16",
      "title": "Research claim audit",
      "prompt": "I want AGI agents to audit a research or strategic claim with baselines, contradictions, evidence, uncertainty, and boundaries.",
      "intent": "Claim Audit",
      "agents": [
        "RES",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Human final review",
      "outputs": "Claims matrix, contradiction register, evidence plan, falsification questions",
      "routes": [
        "claim-boundary.html",
        "falsification-gauntlet.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB17",
      "title": "Partnership diligence",
      "prompt": "I want to evaluate a potential partner with evidence-backed diligence, boundaries, and a decision state.",
      "intent": "Partnership",
      "agents": [
        "ARCH",
        "RES",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Hybrid",
      "outputs": "Diligence docket, risk ledger, decision brief, next actions",
      "routes": [
        "goalos.html",
        "validation-control-tower.html",
        "trust-boundary.html"
      ]
    },
    {
      "id": "PB18",
      "title": "Agent route optimization",
      "prompt": "I want to choose the best AGI agent topology for a public-safe mission and understand which agents activate.",
      "intent": "Agent Topology",
      "agents": [
        "ARCH",
        "PLAN",
        "VAL",
        "SENT"
      ],
      "authority": "AGI Node precheck",
      "outputs": "Agent role plan, routing rationale, validator path",
      "routes": [
        "agi-agent-command-center.html",
        "agi-agent-use-cases.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB19",
      "title": "Risk ledger for strategic claim",
      "prompt": "I want a risk ledger for a strategic claim before it is published or promoted.",
      "intent": "Risk Ledger",
      "agents": [
        "SENT",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Human final review",
      "outputs": "Risk ledger, claim boundary, review notes, fallback path",
      "routes": [
        "trust-boundary.html",
        "claim-boundary.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB20",
      "title": "Evidence Docket for public launch",
      "prompt": "I want to prepare an Evidence Docket for a public launch so claims are clear, safe, and reviewable.",
      "intent": "Launch Docket",
      "agents": [
        "ARCH",
        "BUILD",
        "VERIFY",
        "DOCKET",
        "HUMAN"
      ],
      "authority": "Hybrid",
      "outputs": "Launch claims matrix, proof assets, QA checklist, human review path",
      "routes": [
        "proof-run-001-docket.html",
        "site-health.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB21",
      "title": "Mission to Chronicle conversion",
      "prompt": "I want accepted work to become Chronicle memory and a reusable capability path.",
      "intent": "Chronicle",
      "agents": [
        "DOCKET",
        "CHRON",
        "VERIFY"
      ],
      "authority": "AGI Node precheck",
      "outputs": "Chronicle stub, capability package, reuse conditions",
      "routes": [
        "capability-compounding-lab.html",
        "goalos.html",
        "validation-control-tower.html"
      ]
    },
    {
      "id": "PB22",
      "title": "AGI Jobs work package",
      "prompt": "I want an AGI Jobs-style work package: bounded request, proof bundle plan, validation, and settlement boundary.",
      "intent": "AGI Jobs",
      "agents": [
        "PLAN",
        "NODE",
        "VAL",
        "DOCKET"
      ],
      "authority": "Hybrid",
      "outputs": "Job spec, ProofBundle requirements, validator checklist, no-settlement boundary",
      "routes": [
        "agi-agent-command-center.html",
        "validation-control-tower.html",
        "mainnet-proof-rail.html"
      ]
    },
    {
      "id": "PB23",
      "title": "Council review for Move-37",
      "prompt": "I want a Council review plan for a high-novelty Move-37 candidate with reproduction, stress tests, persistence, and dossier.",
      "intent": "Move-37",
      "agents": [
        "ARCH",
        "SENT",
        "VERIFY",
        "DOCKET",
        "COUNCIL"
      ],
      "authority": "Council",
      "outputs": "Move-37 dossier outline, stress plan, persistence gate, decision packet",
      "routes": [
        "from-loop-to-rsi-state-capacity.html",
        "validation-control-tower.html",
        "agi-agent-command-center.html"
      ]
    },
    {
      "id": "PB24",
      "title": "Build a safe proof demo",
      "prompt": "I want AGI agents to help me build a safe public proof demo from an objective, with no user data or funds.",
      "intent": "Proof Demo",
      "agents": [
        "ARCH",
        "PLAN",
        "BUILD",
        "VERIFY",
        "DOCKET"
      ],
      "authority": "Hybrid",
      "outputs": "Demo mission contract, public-safe constraints, route map, review package",
      "routes": [
        "goalos.html",
        "agi-agent-command-center.html",
        "site-health.html"
      ]
    }
  ],
  "boundary": "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.",
  "tokenBoundary": "$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice."
};
