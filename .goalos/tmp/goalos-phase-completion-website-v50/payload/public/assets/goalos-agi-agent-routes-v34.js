window.GOALOS_AGENTS = [
  {
    "id": "architect",
    "name": "Architect Agent",
    "role": "Turns the objective into a bounded institutional mission.",
    "lane": "Cognition",
    "default": true,
    "gates": [
      "scope",
      "authority",
      "claim boundary"
    ]
  },
  {
    "id": "planner",
    "name": "Planner Agent",
    "role": "Builds the work graph, milestones, dependencies, and done condition.",
    "lane": "Cognition",
    "default": true,
    "gates": [
      "mission contract",
      "budget",
      "deadline"
    ]
  },
  {
    "id": "researcher",
    "name": "Research Agent",
    "role": "Finds public-safe sources, contradictions, assumptions, and evidence needs.",
    "lane": "Evidence",
    "default": true,
    "gates": [
      "source provenance",
      "freshness",
      "contradiction register"
    ]
  },
  {
    "id": "builder",
    "name": "Builder Agent",
    "role": "Creates public-safe artifacts, demos, docs, code patches, or review packets.",
    "lane": "Execution",
    "default": true,
    "gates": [
      "sandbox",
      "artifact hash",
      "rollback target"
    ]
  },
  {
    "id": "verifier",
    "name": "Verifier Agent",
    "role": "Checks whether claims, routes, artifacts, and proof packets satisfy gates.",
    "lane": "Validation",
    "default": true,
    "gates": [
      "claim support",
      "eval pass",
      "risk ledger"
    ]
  },
  {
    "id": "validator",
    "name": "AGI Node Validator",
    "role": "Runs deterministic public-safe validation checks and creates node attestations.",
    "lane": "Node",
    "default": true,
    "gates": [
      "schema",
      "replay",
      "attestation"
    ]
  },
  {
    "id": "sentinel",
    "name": "Sentinel Agent",
    "role": "Watches for boundary drift, unsafe requests, missing rollback, and high-impact escalation.",
    "lane": "Safety",
    "default": true,
    "gates": [
      "boundary",
      "pause",
      "escalation"
    ]
  },
  {
    "id": "docket",
    "name": "Evidence Docket Agent",
    "role": "Packages the public-safe claims matrix, baselines, proof packets, risk/cost ledgers, and replay path.",
    "lane": "Evidence",
    "default": true,
    "gates": [
      "docket completeness",
      "baseline",
      "replay"
    ]
  },
  {
    "id": "chronicle",
    "name": "Chronicle Agent",
    "role": "Turns accepted proof into durable institutional memory and reusable capability stubs.",
    "lane": "Memory",
    "default": true,
    "gates": [
      "accepted state",
      "capability package",
      "lineage"
    ]
  },
  {
    "id": "operator",
    "name": "Human Operator",
    "role": "Approves high-impact, legal, financial, security, external-action, or publication decisions.",
    "lane": "Authority",
    "default": false,
    "gates": [
      "human review",
      "final authority",
      "publication"
    ]
  },
  {
    "id": "council",
    "name": "Architect / Validator Council",
    "role": "Reviews strategic, high-novelty, RSI, Move-37, or governance-changing proposals.",
    "lane": "Governance",
    "default": false,
    "gates": [
      "independent review",
      "dossier",
      "stop authority"
    ]
  },
  {
    "id": "nodeWorker",
    "name": "AGI Node Worker",
    "role": "Represents the deterministic runtime lane that executes bounded work and emits receipts.",
    "lane": "Node",
    "default": false,
    "gates": [
      "container pins",
      "metering",
      "artifact packaging"
    ]
  }
];
window.GOALOS_PLAYBOOKS = [
  {
    "title": "Understand the 48 Ethereum Mainnet contracts",
    "intent": "contract_atlas",
    "objective": "I want AGI agents to help me understand the 48 Ethereum Mainnet contracts, group them by purpose, explain the proof rail, and produce a reviewer-ready learning path.",
    "authority": "AGI Node + Human",
    "agents": [
      "architect",
      "researcher",
      "verifier",
      "validator",
      "docket",
      "sentinel"
    ],
    "routes": [
      "mainnet-contract-atlas.html",
      "mainnet-proof-rail.html",
      "contract-academy.html",
      "token-boundary.html"
    ],
    "artifact": "Contract learning dossier + route plan"
  },
  {
    "title": "Run a public-safe proof mission",
    "intent": "proof_mission",
    "objective": "I want AGI agents to turn my public-safe objective into a Mission Contract, Evidence Docket plan, validation path, Action Graph, and reviewer brief.",
    "authority": "Hybrid",
    "agents": [
      "architect",
      "planner",
      "researcher",
      "builder",
      "verifier",
      "docket",
      "chronicle"
    ],
    "routes": [
      "goalos.html",
      "proof-run-001-docket.html",
      "demo-ecosystem-registry.html",
      "validation-control-tower.html"
    ],
    "artifact": "Mission package"
  },
  {
    "title": "Evaluate an AI vendor or tool with evidence",
    "intent": "vendor_review",
    "objective": "I want AGI agents to evaluate an AI vendor or tool using evidence, claim boundaries, contradictions, risks, baselines, and a reviewer-ready decision packet.",
    "authority": "Human final review",
    "agents": [
      "architect",
      "researcher",
      "verifier",
      "sentinel",
      "docket",
      "operator"
    ],
    "routes": [
      "validation-control-tower.html",
      "trust-boundary.html",
      "proof-run-001-docket.html"
    ],
    "artifact": "Vendor evidence review"
  },
  {
    "title": "Design a controlled pilot program",
    "intent": "pilot",
    "objective": "I want AGI agents to design a controlled pilot where every serious pilot ends with an Evidence Docket, validation certificate, action graph, and rollback plan.",
    "authority": "Hybrid",
    "agents": [
      "architect",
      "planner",
      "builder",
      "verifier",
      "docket",
      "operator"
    ],
    "routes": [
      "pilot-program.html",
      "mission-studio.html",
      "validation-control-tower.html"
    ],
    "artifact": "Pilot mission contract"
  },
  {
    "title": "Understand Loop \u2192 RSI governance",
    "intent": "rsi",
    "objective": "I want AGI agents to explain how long-running loops become deterministic RSI governance with replay, baselines, ECI, Move-37 dossiers, and no OMNI outcome authority.",
    "authority": "Council for high novelty",
    "agents": [
      "architect",
      "researcher",
      "verifier",
      "sentinel",
      "council",
      "docket"
    ],
    "routes": [
      "from-loop-to-rsi-state-capacity.html",
      "validation-control-tower.html",
      "proof-run-001-docket.html"
    ],
    "artifact": "RSI governance brief"
  },
  {
    "title": "Prepare an executive decision brief",
    "intent": "executive",
    "objective": "I want AGI agents to produce an executive decision brief from a public-safe objective: options, evidence, risk, claim boundary, recommendation, and next actions.",
    "authority": "Human review",
    "agents": [
      "architect",
      "planner",
      "researcher",
      "verifier",
      "docket",
      "operator"
    ],
    "routes": [
      "goalos.html",
      "pathfinder.html",
      "proof-run-001-docket.html"
    ],
    "artifact": "Executive brief"
  },
  {
    "title": "Audit privacy, token, and data boundaries",
    "intent": "boundary",
    "objective": "I want AGI agents to validate the privacy, token, no-data, no-funds, no-wallet, and human-review boundaries across the website.",
    "authority": "AGI Node precheck + Human review",
    "agents": [
      "verifier",
      "validator",
      "sentinel",
      "docket",
      "operator"
    ],
    "routes": [
      "trust-boundary.html",
      "token-boundary.html",
      "privacy.html",
      "data-boundary.html",
      "no-data-no-funds.html"
    ],
    "artifact": "Boundary audit packet"
  },
  {
    "title": "Prepare a validator council review",
    "intent": "council",
    "objective": "I want AGI agents to prepare a council review packet for a high-novelty or strategic claim, including dossier, gates, risks, dissent, and stop-authority notes.",
    "authority": "Council",
    "agents": [
      "architect",
      "researcher",
      "verifier",
      "sentinel",
      "council",
      "docket"
    ],
    "routes": [
      "validation-control-tower.html",
      "from-loop-to-rsi-state-capacity.html",
      "proof-run-001-docket.html"
    ],
    "artifact": "Council packet"
  },
  {
    "title": "Create a proof-backed procurement record",
    "intent": "procurement",
    "objective": "I want AGI agents to turn a procurement decision into a proof-backed record: need, options, evidence, risks, validation, boundaries, and reviewer decision.",
    "authority": "Human final review",
    "agents": [
      "architect",
      "researcher",
      "verifier",
      "sentinel",
      "docket",
      "operator"
    ],
    "routes": [
      "validation-use-cases.html",
      "proof-run-001-docket.html",
      "trust-boundary.html"
    ],
    "artifact": "Procurement proof record"
  },
  {
    "title": "Audit website completeness and navigation",
    "intent": "site_qa",
    "objective": "I want AGI agents to validate that the website is complete, routeable, user-friendly, and claim-bounded, with no missing core pages.",
    "authority": "AGI Node precheck",
    "agents": [
      "verifier",
      "validator",
      "sentinel",
      "docket",
      "chronicle"
    ],
    "routes": [
      "site-health.html",
      "site-map.html",
      "search.html",
      "demo-ecosystem-registry.html"
    ],
    "artifact": "Site QA certificate"
  },
  {
    "title": "Plan a defensive cybersecurity proof mission",
    "intent": "defensive_cyber",
    "objective": "I want AGI agents to plan a defensive, repo-owned, public-safe cybersecurity proof mission with no external scans, no exploit execution, no malware, no secrets, and human review.",
    "authority": "Hybrid + Human",
    "agents": [
      "architect",
      "planner",
      "verifier",
      "sentinel",
      "docket",
      "operator"
    ],
    "routes": [
      "validation-control-tower.html",
      "trust-boundary.html",
      "proof-run-001-docket.html"
    ],
    "artifact": "Defensive mission packet"
  },
  {
    "title": "Turn accepted work into reusable capability",
    "intent": "capability",
    "objective": "I want AGI agents to package accepted work as reusable capability only after proof, validation, replay, risk review, and rollback readiness.",
    "authority": "Hybrid",
    "agents": [
      "architect",
      "builder",
      "verifier",
      "docket",
      "chronicle",
      "sentinel"
    ],
    "routes": [
      "capability-compounding-lab.html",
      "proof-backed-upgrade-rights-room.html",
      "validation-control-tower.html"
    ],
    "artifact": "Capability package stub"
  }
];
window.GOALOS_AGENT_ROUTES = [
  {
    "title": "GoalOS Mission Studio",
    "url": "goalos.html",
    "tags": [
      "mission",
      "one box",
      "objective",
      "proof path"
    ]
  },
  {
    "title": "Ask GoalOS",
    "url": "ask-goalos.html",
    "tags": [
      "chat",
      "question",
      "route",
      "assistant"
    ]
  },
  {
    "title": "Validation Control Tower",
    "url": "validation-control-tower.html",
    "tags": [
      "validate",
      "human",
      "agi node",
      "hybrid",
      "council"
    ]
  },
  {
    "title": "Mainnet Contract Atlas",
    "url": "mainnet-contract-atlas.html",
    "tags": [
      "48 contracts",
      "mainnet",
      "ethereum",
      "proof rail"
    ]
  },
  {
    "title": "Proof Run 001 Docket",
    "url": "proof-run-001-docket.html",
    "tags": [
      "evidence docket",
      "proof run",
      "review"
    ]
  },
  {
    "title": "Loop to RSI State Capacity",
    "url": "from-loop-to-rsi-state-capacity.html",
    "tags": [
      "rsi",
      "loop",
      "omni",
      "move-37"
    ]
  },
  {
    "title": "Trust Boundary",
    "url": "trust-boundary.html",
    "tags": [
      "privacy",
      "no data",
      "no funds",
      "no wallet"
    ]
  },
  {
    "title": "Token Boundary",
    "url": "token-boundary.html",
    "tags": [
      "agialpha",
      "token",
      "not available",
      "no advice"
    ]
  },
  {
    "title": "All Pages",
    "url": "site-map.html",
    "tags": [
      "routes",
      "all pages",
      "navigation"
    ]
  },
  {
    "title": "Search",
    "url": "search.html",
    "tags": [
      "search",
      "command palette"
    ]
  }
];
