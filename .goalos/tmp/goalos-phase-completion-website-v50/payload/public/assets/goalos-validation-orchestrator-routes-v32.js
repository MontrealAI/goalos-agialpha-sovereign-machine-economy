window.GOALOS_VALIDATION_ROUTES_V32 = [
  {
    "title": "GoalOS Validation Command Center V32",
    "href": "validation-command-center.html",
    "category": "Validation",
    "tags": [
      "validate",
      "human",
      "agi node",
      "hybrid",
      "council"
    ],
    "description": "Choose Human, AGI Node, Hybrid, or Council validation and generate a public-safe validation packet."
  },
  {
    "title": "GoalOS Mission Studio",
    "href": "goalos.html",
    "category": "Mission",
    "tags": [
      "mission",
      "objective",
      "tell goalos"
    ],
    "description": "One-box mission interface: tell GoalOS what you want and get a proof path."
  },
  {
    "title": "Ask GoalOS",
    "href": "ask-goalos.html",
    "category": "Assistant",
    "tags": [
      "ask",
      "questions",
      "chat",
      "route"
    ],
    "description": "Browser-local question window that answers and routes users to the right page."
  },
  {
    "title": "48 Mainnet Contract Atlas",
    "href": "mainnet-contract-atlas.html",
    "category": "Contracts",
    "tags": [
      "48",
      "contracts",
      "ethereum",
      "mainnet",
      "atlas"
    ],
    "description": "Learn the GoalOS-created Ethereum Mainnet contract surface and proof rail."
  },
  {
    "title": "Mainnet Proof Rail",
    "href": "mainnet-proof-rail.html",
    "category": "Contracts",
    "tags": [
      "proof rail",
      "contracts",
      "mainnet"
    ],
    "description": "Understand how the contract surface maps to proof-bearing institutional work."
  },
  {
    "title": "Contract Academy",
    "href": "contract-academy.html",
    "category": "Contracts",
    "tags": [
      "learn",
      "academy",
      "contracts"
    ],
    "description": "Guided learning path for non-technical users who want to understand the contracts."
  },
  {
    "title": "Proof Run 001 Docket",
    "href": "proof-run-001-docket.html",
    "category": "Evidence",
    "tags": [
      "proof run",
      "docket",
      "evidence"
    ],
    "description": "Review the public repository-readiness Evidence Docket."
  },
  {
    "title": "Demo Ecosystem Registry",
    "href": "demo-ecosystem-registry.html",
    "category": "Registry",
    "tags": [
      "registry",
      "demos",
      "routes"
    ],
    "description": "Browse public demos, inputs, outputs, gates, and next states."
  },
  {
    "title": "Loop to RSI State-Capacity",
    "href": "from-loop-to-rsi-state-capacity.html",
    "category": "Loop \u2192 RSI",
    "tags": [
      "rsi",
      "loop",
      "governance",
      "state capacity"
    ],
    "description": "See how loops become deterministic RSI governance."
  },
  {
    "title": "Trust Boundary",
    "href": "trust-boundary.html",
    "category": "Boundary",
    "tags": [
      "trust",
      "privacy",
      "data",
      "funds"
    ],
    "description": "No user data, no user funds, no wallet, no transaction, no production authority."
  },
  {
    "title": "Token Boundary",
    "href": "token-boundary.html",
    "category": "Boundary",
    "tags": [
      "token",
      "agialpha",
      "boundary",
      "not available"
    ],
    "description": "Public contract identification only; not available from GoalOS; no advice."
  },
  {
    "title": "All Pages",
    "href": "site-map.html",
    "category": "Navigation",
    "tags": [
      "all pages",
      "site map",
      "navigation"
    ],
    "description": "Complete public route map."
  },
  {
    "title": "Search",
    "href": "search.html",
    "category": "Navigation",
    "tags": [
      "search",
      "command palette"
    ],
    "description": "Find any public route."
  },
  {
    "title": "Site Health",
    "href": "site-health.html",
    "category": "Navigation",
    "tags": [
      "health",
      "route integrity",
      "qa"
    ],
    "description": "Route inventory and health checks."
  },
  {
    "title": "Validation Use Cases",
    "href": "validation-use-cases.html",
    "category": "Validation",
    "tags": [
      "use cases",
      "playbooks",
      "examples"
    ],
    "description": "End-to-end validation examples for human, AGI Node, hybrid, and council review."
  },
  {
    "title": "AGI Node Use Cases",
    "href": "agi-node-use-cases.html",
    "category": "Validation",
    "tags": [
      "agi node",
      "examples",
      "validator"
    ],
    "description": "Concrete cases where AGI Node validation is useful."
  }
];
window.GOALOS_VALIDATION_PLAYBOOKS_V32 = [
  {
    "id": "UC-01",
    "title": "AGI Node validates the 48 Mainnet Contract Atlas",
    "authority": "AGI Node",
    "objective": "Validate that the 48 Ethereum Mainnet contract learning path is complete, claim-bounded, routeable, and ready for public review.",
    "why": "Users need a fast way to understand the contract rail without reading every page.",
    "creates": [
      "Contract Atlas validation certificate",
      "route checklist",
      "reviewer brief"
    ],
    "gate": "Route integrity + token boundary + evidence references",
    "routes": [
      "mainnet-contract-atlas.html",
      "mainnet-proof-rail.html",
      "contract-academy.html",
      "token-boundary.html"
    ]
  },
  {
    "id": "UC-02",
    "title": "Human validates a public claim before publication",
    "authority": "Human",
    "objective": "Prepare human review for a high-impact GoalOS public claim before publication.",
    "why": "Judgment-heavy public claims require human accountability and claim-boundary review.",
    "creates": [
      "human review brief",
      "claim matrix",
      "publication hold state"
    ],
    "gate": "Human authority + claim boundary + evidence docket",
    "routes": [
      "proof-run-001-docket.html",
      "trust-boundary.html",
      "claim-boundary.html"
    ]
  },
  {
    "id": "UC-03",
    "title": "Hybrid validates an AI vendor or tool",
    "authority": "Hybrid",
    "objective": "Evaluate an AI vendor or tool using evidence, not marketing claims, with AGI Node precheck and human final review.",
    "why": "Procurement decisions need repeatable evidence and human judgment.",
    "creates": [
      "vendor evidence checklist",
      "risk ledger",
      "review packet"
    ],
    "gate": "AGI Node precheck + human review",
    "routes": [
      "demo-ecosystem-registry.html",
      "proof-run-001-docket.html",
      "trust-boundary.html"
    ]
  },
  {
    "id": "UC-04",
    "title": "Council validates Loop \u2192 RSI governance",
    "authority": "Council",
    "objective": "Prepare Architect / Validator Council review for a Loop to RSI governance packet with replay, baselines, persistence, and Move-37 handling.",
    "why": "Recursive improvement needs more than a normal review; it needs governance-grade challenge.",
    "creates": [
      "council packet",
      "Move-37 dossier outline",
      "RSI gate plan"
    ],
    "gate": "Council + replay + baselines + persistence",
    "routes": [
      "from-loop-to-rsi-state-capacity.html",
      "validation-command-center.html"
    ]
  },
  {
    "id": "UC-05",
    "title": "AGI Node validates token-boundary wording",
    "authority": "AGI Node",
    "objective": "Validate the $AGIALPHA token boundary page: public contract identification only, not available from GoalOS, no sale, no custody, no wallet support, no investment advice.",
    "why": "Token confusion is a major user and compliance risk.",
    "creates": [
      "token boundary attestation",
      "wording checklist",
      "route card"
    ],
    "gate": "No sale + no custody + no wallet support + no advice",
    "routes": [
      "token-boundary.html",
      "trust-boundary.html"
    ]
  },
  {
    "id": "UC-06",
    "title": "Hybrid validates a controlled pilot program",
    "authority": "Hybrid",
    "objective": "Design and validate a controlled pilot program where every serious pilot ends with an Evidence Docket.",
    "why": "Institutions need a repeatable adoption path, not a one-off demo.",
    "creates": [
      "pilot validation plan",
      "docket requirements",
      "human review path"
    ],
    "gate": "AGI Node completeness check + human go/no-go",
    "routes": [
      "mission-studio.html",
      "proof-run-001-docket.html",
      "demo-ecosystem-registry.html"
    ]
  },
  {
    "id": "UC-07",
    "title": "AGI Node validates site route integrity",
    "authority": "AGI Node",
    "objective": "Validate that the website routes are complete, navigable, searchable, and not missing critical GoalOS pages.",
    "why": "A large proof surface is only useful if users can find every room.",
    "creates": [
      "route health certificate",
      "broken-link summary",
      "search map"
    ],
    "gate": "Route inventory + no missing core pages",
    "routes": [
      "site-map.html",
      "search.html",
      "site-health.html"
    ]
  },
  {
    "id": "UC-08",
    "title": "Hybrid validates a defensive cybersecurity proof mission",
    "authority": "Hybrid",
    "objective": "Validate a defensive cybersecurity proof mission with no secrets, no exploit execution, no external scans, and human final review.",
    "why": "Defensive security work must be helpful without becoming unsafe or autonomous remediation.",
    "creates": [
      "security boundary checklist",
      "safe remediation brief",
      "human review hold"
    ],
    "gate": "Defensive-only + no external scan + human review",
    "routes": [
      "trust-boundary.html",
      "proof-run-001-docket.html"
    ]
  },
  {
    "id": "UC-09",
    "title": "Human validates a procurement proof record",
    "authority": "Human",
    "objective": "Prepare a procurement proof record so an institution can compare options using evidence, risk, and reviewer notes.",
    "why": "Executives need decision-ready packets, not unsupported AI recommendations.",
    "creates": [
      "procurement brief",
      "claims matrix",
      "risk ledger"
    ],
    "gate": "Human authority + decision owner",
    "routes": [
      "mission-studio.html",
      "proof-run-001-docket.html"
    ]
  },
  {
    "id": "UC-10",
    "title": "AGI Node validates Evidence Docket completeness",
    "authority": "AGI Node",
    "objective": "Check whether an Evidence Docket includes claims matrix, baselines, proof packets, evaluator notes, risk ledger, replay path, and claim boundary.",
    "why": "Most proof failures are missing components, not deep philosophical failures.",
    "creates": [
      "docket completeness certificate",
      "missing-items list",
      "next route"
    ],
    "gate": "Docket structure + replay readiness",
    "routes": [
      "proof-run-001-docket.html",
      "demo-ecosystem-registry.html"
    ]
  },
  {
    "id": "UC-11",
    "title": "Council validates a Move-37 candidate",
    "authority": "Council",
    "objective": "Prepare Council review for a high-novelty Move-37 candidate requiring reproduction, stress testing, persistence gates, and dossier packaging.",
    "why": "High novelty should increase skepticism, not reduce proof burden.",
    "creates": [
      "Move-37 council packet",
      "stress plan",
      "dossier index"
    ],
    "gate": "Reproduce + stress + persist + dossier",
    "routes": [
      "from-loop-to-rsi-state-capacity.html",
      "validation-command-center.html"
    ]
  },
  {
    "id": "UC-12",
    "title": "AGI Node validates privacy and data boundary",
    "authority": "AGI Node",
    "objective": "Validate the public no-data, no-funds, no-wallet, no-transaction, no-network-call boundary across the website.",
    "why": "User trust depends on an obvious and consistent boundary.",
    "creates": [
      "privacy boundary attestation",
      "route checklist",
      "wording map"
    ],
    "gate": "No data + no funds + no wallet + no network call",
    "routes": [
      "trust-boundary.html",
      "privacy.html",
      "data-boundary.html",
      "no-data-no-funds.html"
    ]
  },
  {
    "id": "UC-13",
    "title": "Human validates a strategic opportunity proof mission",
    "authority": "Human",
    "objective": "Prepare a human-reviewed strategic opportunity proof mission with claims, evidence, risks, and action graph.",
    "why": "Strategy needs judgment and accountability, even when AGI Nodes can precheck evidence.",
    "creates": [
      "executive decision brief",
      "action graph",
      "human review state"
    ],
    "gate": "Human review + evidence docket + risk ledger",
    "routes": [
      "mission-studio.html",
      "proof-run-001-docket.html"
    ]
  },
  {
    "id": "UC-14",
    "title": "Hybrid validates reusable capability promotion",
    "authority": "Hybrid",
    "objective": "Validate whether accepted work can become a reusable capability after gates pass.",
    "why": "Reusable capability is the compounding object; it should not propagate without proof.",
    "creates": [
      "capability promotion brief",
      "selection-gate checklist",
      "rollback reminder"
    ],
    "gate": "Proof + eval + rollback + scope",
    "routes": [
      "capability-compounding-lab.html",
      "proof-run-001-docket.html"
    ]
  },
  {
    "id": "UC-15",
    "title": "AGI Node validates Mainnet proof-rail learning path",
    "authority": "AGI Node",
    "objective": "Validate that a non-technical user can learn the Mainnet proof rail from start to contract atlas to proof rail to token boundary.",
    "why": "The 48 contracts must be understandable, not just deployed.",
    "creates": [
      "learning-path certificate",
      "route sequence",
      "review brief"
    ],
    "gate": "Learnability + routeability + boundary clarity",
    "routes": [
      "mainnet-contract-atlas.html",
      "mainnet-proof-rail.html",
      "contract-academy.html"
    ]
  },
  {
    "id": "UC-16",
    "title": "Hybrid prepares external reviewer replay",
    "authority": "Hybrid",
    "objective": "Prepare an external reviewer replay packet for a proof claim, with AGI Node completeness checks and human approval.",
    "why": "External review is how proof becomes credible beyond the project team.",
    "creates": [
      "replay packet",
      "reviewer brief",
      "challenge checklist"
    ],
    "gate": "Replay readiness + human approval",
    "routes": [
      "proof-run-001-docket.html",
      "reviewer-room.html"
    ]
  },
  {
    "id": "UC-17",
    "title": "Council validates governance escalation",
    "authority": "Council",
    "objective": "Prepare a governance escalation for a high-impact validation-authority change.",
    "why": "Changing who can validate is itself a governance decision.",
    "creates": [
      "council escalation packet",
      "authority matrix",
      "rollback condition"
    ],
    "gate": "Council + challenge window + rollback",
    "routes": [
      "validation-command-center.html",
      "trust-boundary.html"
    ]
  },
  {
    "id": "UC-18",
    "title": "AGI Node validates documentation completeness",
    "authority": "AGI Node",
    "objective": "Validate whether GoalOS docs, runbooks, reports, issue templates, and user paths are discoverable and complete.",
    "why": "A usable institution needs documentation that normal users can navigate.",
    "creates": [
      "documentation completeness certificate",
      "route map",
      "missing-items brief"
    ],
    "gate": "Docs + route map + user path",
    "routes": [
      "docs.html",
      "site-map.html",
      "search.html"
    ]
  },
  {
    "id": "UC-19",
    "title": "AGI Node validates a mission before human review",
    "authority": "AGI Node",
    "objective": "Run AGI Node precheck on a Mission Studio objective before a human reviewer signs off.",
    "why": "AGI Nodes can remove mechanical errors before human time is spent.",
    "creates": [
      "node precheck",
      "mission contract QA",
      "human review packet"
    ],
    "gate": "Schema + boundary + routes",
    "routes": [
      "goalos.html",
      "mission-studio.html",
      "validation-command-center.html"
    ]
  },
  {
    "id": "UC-20",
    "title": "Hybrid validates a public demo before launch",
    "authority": "Hybrid",
    "objective": "Validate that a new public demo is browser-local, claim-bounded, downloadable, routeable, and ready for human launch review.",
    "why": "Each demo should be useful without becoming an unsupported claim or data surface.",
    "creates": [
      "demo launch checklist",
      "AGI Node precheck",
      "human launch brief"
    ],
    "gate": "Browser-local + no forbidden APIs + human launch",
    "routes": [
      "demo-ecosystem-registry.html",
      "site-health.html"
    ]
  },
  {
    "id": "UC-21",
    "title": "Council validates RSI state-capacity claim",
    "authority": "Council",
    "objective": "Review an RSI state-capacity claim with baseline discipline, replay, ECI, persistence gates, and council authority.",
    "why": "State-capacity claims are strategic and should be treated as high-assurance dossiers.",
    "creates": [
      "state-capacity council packet",
      "RSI dashboard checklist",
      "dossier option"
    ],
    "gate": "Baselines + replay + ECI + council",
    "routes": [
      "from-loop-to-rsi-state-capacity.html"
    ]
  },
  {
    "id": "UC-22",
    "title": "Human validates legal/privacy boundary posture",
    "authority": "Human",
    "objective": "Prepare human review for legal, privacy, token, and claim-boundary posture before public distribution.",
    "why": "AGI Node can precheck wording, but legal/privacy posture needs human accountability.",
    "creates": [
      "human boundary review brief",
      "token/privacy checklist",
      "publication hold"
    ],
    "gate": "Human review required",
    "routes": [
      "trust-boundary.html",
      "token-boundary.html",
      "privacy.html"
    ]
  },
  {
    "id": "UC-23",
    "title": "AGI Node validates Ask GoalOS routing",
    "authority": "AGI Node",
    "objective": "Validate that Ask GoalOS answers common questions and routes users to correct public pages without network calls or data storage.",
    "why": "The chat window should help users without becoming a support-data intake system.",
    "creates": [
      "Ask GoalOS routing test",
      "intent map",
      "boundary certificate"
    ],
    "gate": "Route intent + no network + no storage",
    "routes": [
      "ask-goalos.html",
      "search.html",
      "site-map.html"
    ]
  },
  {
    "id": "UC-24",
    "title": "Hybrid validates end-to-end institution readiness",
    "authority": "Hybrid",
    "objective": "Validate whether GoalOS is ready as a public proof institution: mission input, ask window, contract atlas, proof run, validation studio, all pages, and boundaries.",
    "why": "This gives non-technical users the full end-to-end understanding of the system.",
    "creates": [
      "institution readiness brief",
      "AGI Node scorecard",
      "human review agenda"
    ],
    "gate": "AGI Node system check + human approval",
    "routes": [
      "goalos.html",
      "validation-command-center.html",
      "mainnet-contract-atlas.html",
      "proof-run-001-docket.html",
      "site-map.html"
    ]
  }
];
