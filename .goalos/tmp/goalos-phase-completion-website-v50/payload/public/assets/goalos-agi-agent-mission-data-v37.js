window.GOALOS_AGENT_MISSION_DATA_V37 = {
  "version": "v37",
  "agents": [
    {
      "id": "architect",
      "name": "Architect Agent",
      "short": "ARCH",
      "lane": "Aim",
      "desc": "Frames objective, scope, success criteria, authority, and claim boundary."
    },
    {
      "id": "planner",
      "name": "Planner Agent",
      "short": "PLAN",
      "lane": "Plan",
      "desc": "Builds Mission Contract, workstreams, proof gates, budgets, and done condition."
    },
    {
      "id": "research",
      "name": "Research Agent",
      "short": "RES",
      "lane": "Evidence",
      "desc": "Maps public-safe sources, routes, contradictions, and provenance."
    },
    {
      "id": "builder",
      "name": "Builder Agent",
      "short": "BUILD",
      "lane": "Work",
      "desc": "Creates bounded artifacts, pages, briefs, and proof-safe outputs."
    },
    {
      "id": "verifier",
      "name": "Verifier Agent",
      "short": "VERIFY",
      "lane": "Check",
      "desc": "Checks claim support, baselines, replay readiness, and missing evidence."
    },
    {
      "id": "node_worker",
      "name": "AGI Node Worker",
      "short": "NODE-W",
      "lane": "Runtime",
      "desc": "Prepares deterministic runtime handoff, manifests, and replayable work packages."
    },
    {
      "id": "node_validator",
      "name": "AGI Node Validator",
      "short": "NODE-V",
      "lane": "Validate",
      "desc": "Validates deterministic public-safe checks: schemas, routes, boundaries, and docket completeness."
    },
    {
      "id": "sentinel",
      "name": "Sentinel Agent",
      "short": "SENT",
      "lane": "Safety",
      "desc": "Watches drift, unsafe scope, stale claims, missing rollback, and escalation triggers."
    },
    {
      "id": "docket",
      "name": "Evidence Docket Agent",
      "short": "DOCKET",
      "lane": "Proof",
      "desc": "Packages claims, evidence, baselines, risk/cost ledgers, replay, and reviewer notes."
    },
    {
      "id": "chronicle",
      "name": "Chronicle Agent",
      "short": "CHRON",
      "lane": "Memory",
      "desc": "Turns accepted proof into institutional memory and reusable capability."
    },
    {
      "id": "human",
      "name": "Human Reviewer",
      "short": "HUMAN",
      "lane": "Authority",
      "desc": "Reviews judgment-heavy, high-impact, publication, legal, financial, security, or external-action decisions."
    },
    {
      "id": "council",
      "name": "Architect / Validator Council",
      "short": "COUNCIL",
      "lane": "Governance",
      "desc": "Reviews RSI, Move-37, strategic, high-novelty, or governance-changing claims."
    }
  ],
  "stages": [
    "Objective",
    "Agent Roles",
    "AGI Job",
    "AGI Node Handoff",
    "ProofBundle",
    "Evidence Docket",
    "Validation",
    "Chronicle"
  ],
  "routes": [
    {
      "url": "agi-agent-mission-control.html",
      "title": "AGI Agent Mission Control"
    },
    {
      "url": "agi-agent-playbooks.html",
      "title": "AGI Agent Playbooks"
    },
    {
      "url": "agent-flow-academy.html",
      "title": "Agent Flow Academy"
    },
    {
      "url": "goalos.html",
      "title": "Tell GoalOS"
    },
    {
      "url": "ask-goalos.html",
      "title": "Ask GoalOS"
    },
    {
      "url": "validation-control-tower.html",
      "title": "Validation Control Tower"
    },
    {
      "url": "validation-command-center.html",
      "title": "Validation Command Center"
    },
    {
      "url": "mainnet-contract-atlas.html",
      "title": "Mainnet Contract Atlas"
    },
    {
      "url": "mainnet-proof-rail.html",
      "title": "Mainnet Proof Rail"
    },
    {
      "url": "contract-academy.html",
      "title": "Contract Academy"
    },
    {
      "url": "proof-run-001-docket.html",
      "title": "Proof Run 001 Docket"
    },
    {
      "url": "from-loop-to-rsi-state-capacity.html",
      "title": "Loop → RSI State Capacity"
    },
    {
      "url": "trust-boundary.html",
      "title": "Trust Boundary"
    },
    {
      "url": "token-boundary.html",
      "title": "Token Boundary"
    },
    {
      "url": "site-map.html",
      "title": "All Pages"
    },
    {
      "url": "search.html",
      "title": "Search"
    },
    {
      "url": "demo-ecosystem-registry.html",
      "title": "Demo Registry"
    },
    {
      "url": "site-health.html",
      "title": "Site Health"
    }
  ],
  "playbooks": [
    {
      "id": "contracts",
      "num": 1,
      "title": "Understand the 48 Ethereum Mainnet contracts",
      "prompt": "I want AGI agents to help me understand the 48 Ethereum Mainnet contracts.",
      "why": "Learn the proof rail by purpose, route, and boundary before trusting claims.",
      "agents": [
        "architect",
        "research",
        "docket",
        "node_validator"
      ],
      "authority": "AGI Node + Human",
      "gates": "claim boundary, route fit, contract learning path, token boundary",
      "routes": [
        "mainnet-contract-atlas.html",
        "mainnet-proof-rail.html",
        "contract-academy.html",
        "token-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "proof",
      "num": 2,
      "title": "Run a public-safe proof mission",
      "prompt": "I want AGI agents to run a public-safe proof mission from objective to Evidence Docket.",
      "why": "Converts a plain objective into a reviewable proof package.",
      "agents": [
        "architect",
        "planner",
        "builder",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "mission contract, evidence docket, validation, human boundary",
      "routes": [
        "goalos.html",
        "proof-run-001-docket.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "vendor",
      "num": 3,
      "title": "Evaluate an AI vendor with evidence",
      "prompt": "I want AGI agents to evaluate an AI vendor or tool using evidence, not marketing claims.",
      "why": "Turns a vendor decision into claims, evidence, contradictions, risk, and action.",
      "agents": [
        "planner",
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "claim support, source provenance, contradiction register, risk ledger",
      "routes": [
        "validation-control-tower.html",
        "proof-run-001-docket.html",
        "trust-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "pilot",
      "num": 4,
      "title": "Design a controlled pilot program",
      "prompt": "I want AGI agents to design a controlled pilot where every serious pilot ends with a docket.",
      "why": "Makes adoption bounded: success criteria, acceptance gates, rollback, and proof.",
      "agents": [
        "architect",
        "planner",
        "builder",
        "verifier",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "pilot scope, success criteria, rollback, evidence docket",
      "routes": [
        "goalos.html",
        "demo-ecosystem-registry.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "rsi",
      "num": 5,
      "title": "Understand Loop to RSI governance",
      "prompt": "I want AGI agents to explain how loops become deterministic RSI governance.",
      "why": "Connects long loops to replay, drift sentinels, baselines, ECI, Move-37, and dossiers.",
      "agents": [
        "architect",
        "research",
        "sentinel",
        "docket",
        "council"
      ],
      "authority": "Council",
      "gates": "replay integrity, baselines, persistence, dossier",
      "routes": [
        "from-loop-to-rsi-state-capacity.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "boundary",
      "num": 6,
      "title": "Check privacy, token, and data boundaries",
      "prompt": "I want AGI agents to check privacy, token, and no-data boundaries across the website.",
      "why": "Prevents confusion around data, funds, wallets, token availability, and unsupported claims.",
      "agents": [
        "sentinel",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "AGI Node",
      "gates": "no data, no funds, no wallet, token boundary, claim boundary",
      "routes": [
        "trust-boundary.html",
        "token-boundary.html",
        "privacy.html",
        "data-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "council",
      "num": 7,
      "title": "Prepare a Validator Council review",
      "prompt": "I want AGI agents to prepare a Validator Council review session for a strategic GoalOS claim.",
      "why": "Creates evidence questions, dissent lanes, and authority path for important claims.",
      "agents": [
        "architect",
        "verifier",
        "docket",
        "council"
      ],
      "authority": "Council",
      "gates": "strategic claim boundary, independent review, dissent, action graph",
      "routes": [
        "validation-control-tower.html",
        "proof-run-001-docket.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "cyber",
      "num": 8,
      "title": "Plan a defensive cybersecurity proof mission",
      "prompt": "I want AGI agents to plan a defensive, repo-owned cybersecurity proof mission with no external scans.",
      "why": "Shows safe security use: defensive, bounded, no secrets, no exploitation.",
      "agents": [
        "sentinel",
        "research",
        "builder",
        "verifier",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "defensive-only scope, no external targets, no secrets, human review",
      "routes": [
        "validation-control-tower.html",
        "trust-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "procurement",
      "num": 9,
      "title": "Create a proof-backed procurement record",
      "prompt": "I want AGI agents to create a proof-backed procurement record for an AI system decision.",
      "why": "Makes procurement inspectable and less dependent on demos or persuasion.",
      "agents": [
        "planner",
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "vendor claims, evidence matrix, risk/cost ledger, decision state",
      "routes": [
        "goalos.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "siteaudit",
      "num": 10,
      "title": "Audit website and repository completeness",
      "prompt": "I want AGI agents to audit whether the GoalOS website and repository are complete and navigable.",
      "why": "Checks routes, sitemap, search, boundaries, downloads, and missing pages.",
      "agents": [
        "research",
        "builder",
        "verifier",
        "sentinel"
      ],
      "authority": "AGI Node",
      "gates": "route integrity, all pages, search, sitemap, boundary coverage",
      "routes": [
        "site-map.html",
        "site-health.html",
        "search.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "executive",
      "num": 11,
      "title": "Prepare an executive decision brief",
      "prompt": "I want AGI agents to prepare an executive decision brief with evidence, risks, options, and next actions.",
      "why": "Turns proof into executive options and next actions.",
      "agents": [
        "architect",
        "planner",
        "research",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "decision state, options, risks, action graph, review requirement",
      "routes": [
        "goalos.html",
        "proof-run-001-docket.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "replay",
      "num": 12,
      "title": "Prepare external reviewer replay",
      "prompt": "I want AGI agents to prepare an external reviewer replay packet.",
      "why": "Makes work inspectable by someone outside the builder loop.",
      "agents": [
        "verifier",
        "docket",
        "sentinel",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "replay path, manifests, artifacts, baselines, reviewer brief",
      "routes": [
        "proof-run-001-docket.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "nodehandoff",
      "num": 13,
      "title": "Create an AGI Node handoff packet",
      "prompt": "I want AGI agents to create an AGI Node handoff packet for deterministic validation.",
      "why": "Shows what a node receives: objective, artifacts, validators, risks, replay instructions.",
      "agents": [
        "planner",
        "node_worker",
        "node_validator",
        "sentinel"
      ],
      "authority": "AGI Node",
      "gates": "schema, runtime pins, proof bundle, validation gates",
      "routes": [
        "agi-agent-mission-control.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "proofrail",
      "num": 14,
      "title": "Build a Mainnet proof-rail learning path",
      "prompt": "I want AGI agents to build a guided learning path for the Mainnet proof rail.",
      "why": "Helps non-technical users learn contracts by purpose, not by code first.",
      "agents": [
        "architect",
        "research",
        "docket",
        "node_validator"
      ],
      "authority": "AGI Node",
      "gates": "contract purpose, route order, token boundary, reviewer checklist",
      "routes": [
        "mainnet-contract-atlas.html",
        "contract-academy.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "publicclaim",
      "num": 15,
      "title": "Review a public claim before posting",
      "prompt": "I want AGI agents to review a public GoalOS claim before I post it.",
      "why": "Protects credibility by separating thesis, evidence, and claim boundary.",
      "agents": [
        "verifier",
        "sentinel",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "claim support, overclaim check, evidence route, public boundary",
      "routes": [
        "claim-boundary.html",
        "trust-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "capability",
      "num": 16,
      "title": "Promote accepted work into reusable capability",
      "prompt": "I want AGI agents to turn accepted proof into reusable capability.",
      "why": "Shows how verified work compounds instead of disappearing as one-off output.",
      "agents": [
        "docket",
        "chronicle",
        "verifier",
        "council"
      ],
      "authority": "Hybrid",
      "gates": "selection gate, proof history, rollback, Chronicle entry",
      "routes": [
        "capability-compounding-lab.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "launch",
      "num": 17,
      "title": "Prepare an Evidence Docket for public launch",
      "prompt": "I want AGI agents to prepare an Evidence Docket for a public demo launch.",
      "why": "Turns a demo from marketing into a claim-bound evidence room.",
      "agents": [
        "builder",
        "verifier",
        "docket",
        "sentinel",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "claims matrix, proof packets, risk ledger, reviewer brief",
      "routes": [
        "proof-run-001-docket.html",
        "demo-ecosystem-registry.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "askrouting",
      "num": 18,
      "title": "Validate Ask GoalOS routing",
      "prompt": "I want AGI agents to validate that Ask GoalOS routes users correctly.",
      "why": "Improves onboarding and prevents route confusion.",
      "agents": [
        "verifier",
        "node_validator",
        "sentinel"
      ],
      "authority": "AGI Node",
      "gates": "route matching, fallback routes, no backend, no storage",
      "routes": [
        "ask-goalos.html",
        "search.html",
        "site-map.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "strategy",
      "num": 19,
      "title": "Map a strategic opportunity into a proof mission",
      "prompt": "I want AGI agents to map a strategic opportunity into a proof mission.",
      "why": "Converts high-level opportunity into scope, evidence, risks, and next actions.",
      "agents": [
        "architect",
        "planner",
        "research",
        "human"
      ],
      "authority": "Human",
      "gates": "decision objective, success criteria, risks, action graph",
      "routes": [
        "goalos.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "partner",
      "num": 20,
      "title": "Run partnership diligence",
      "prompt": "I want AGI agents to run partnership diligence with evidence and risk boundaries.",
      "why": "Makes partnership review concrete: claims, evidence, risks, and open questions.",
      "agents": [
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "source provenance, contradiction register, risk ledger",
      "routes": [
        "goalos.html",
        "proof-run-001-docket.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "topology",
      "num": 21,
      "title": "Choose the right agent topology",
      "prompt": "I want AGI agents to recommend the simplest sufficient agent topology for my objective.",
      "why": "Avoids the swarm trap by selecting only roles that reduce proof debt.",
      "agents": [
        "architect",
        "planner",
        "verifier",
        "sentinel"
      ],
      "authority": "AGI Node",
      "gates": "role fit, tool scope, validator set, stopping rule",
      "routes": [
        "agent-flow-academy.html",
        "agi-agent-mission-control.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "agijobs",
      "num": 22,
      "title": "Create an AGI Jobs-style work package",
      "prompt": "I want AGI agents to convert my objective into an AGI Jobs-style bounded work package.",
      "why": "Makes request, acceptance tests, proof, validation, and Chronicle explicit.",
      "agents": [
        "planner",
        "node_worker",
        "node_validator",
        "docket"
      ],
      "authority": "Hybrid",
      "gates": "job spec, acceptance tests, proof bundle, validation route",
      "routes": [
        "agi-agent-mission-control.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "hybrid",
      "num": 23,
      "title": "Hybrid validation before publication",
      "prompt": "I want AGI Node precheck and human final review before publishing a claim.",
      "why": "Combines autonomy with accountability for important public work.",
      "agents": [
        "node_validator",
        "human",
        "docket",
        "sentinel"
      ],
      "authority": "Hybrid",
      "gates": "node precheck, human signoff, challenge window, rollback",
      "routes": [
        "validation-control-tower.html",
        "claim-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "securityboundary",
      "num": 24,
      "title": "Security boundary audit",
      "prompt": "I want AGI agents to audit the security boundary of a public-safe demo.",
      "why": "Keeps demos useful without becoming unsafe actuation surfaces.",
      "agents": [
        "sentinel",
        "verifier",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "no secrets, no external scans, no unsafe automation, no widened permissions",
      "routes": [
        "trust-boundary.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "policy",
      "num": 25,
      "title": "Compare AI policy options",
      "prompt": "I want AGI agents to compare AI policy options with evidence and uncertainty.",
      "why": "Produces decision-ready options rather than persuasive policy prose.",
      "agents": [
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "sources, assumptions, contradictions, impact/risk map",
      "routes": [
        "goalos.html",
        "proof-run-001-docket.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "researchclaim",
      "num": 26,
      "title": "Audit a research or strategic claim",
      "prompt": "I want AGI agents to audit whether a research claim is supported by evidence.",
      "why": "Separates theory, implementation evidence, and empirical proof.",
      "agents": [
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "claim matrix, baselines, evidence threshold, uncertainty",
      "routes": [
        "proof-run-001-docket.html",
        "claim-boundary.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "buildbuy",
      "num": 27,
      "title": "Build vs buy AI decision",
      "prompt": "I want AGI agents to prepare a build-vs-buy AI decision state.",
      "why": "Converts an expensive strategic decision into evidence, options, and risks.",
      "agents": [
        "architect",
        "research",
        "verifier",
        "docket",
        "human"
      ],
      "authority": "Human",
      "gates": "decision options, costs, risks, claim support, action graph",
      "routes": [
        "goalos.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "sop",
      "num": 28,
      "title": "Turn a workflow into reusable SOP",
      "prompt": "I want AGI agents to turn a repeatable workflow into a proof-backed SOP.",
      "why": "Converts one-off work into a reusable capability package.",
      "agents": [
        "planner",
        "builder",
        "verifier",
        "chronicle"
      ],
      "authority": "Hybrid",
      "gates": "SOP, gates, rollback, evidence history, capability package",
      "routes": [
        "capability-compounding-lab.html",
        "goalos.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "education",
      "num": 29,
      "title": "Teach a new team member GoalOS",
      "prompt": "I want AGI agents to create a 30-minute onboarding path for a new GoalOS user.",
      "why": "Makes the system easier to adopt and reduces cognitive load.",
      "agents": [
        "architect",
        "research",
        "builder",
        "docket"
      ],
      "authority": "AGI Node",
      "gates": "route order, simple explanations, boundary reminders",
      "routes": [
        "start-here.html",
        "pathfinder.html",
        "site-map.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "release",
      "num": 30,
      "title": "Prepare a release readiness packet",
      "prompt": "I want AGI agents to prepare a release readiness packet for a new public page.",
      "why": "Reduces broken routes, stale claims, missing downloads, and unsupported launches.",
      "agents": [
        "builder",
        "verifier",
        "sentinel",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "route QA, download QA, boundary QA, reviewer checklist",
      "routes": [
        "site-health.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "market",
      "num": 31,
      "title": "Explain AGI Jobs + Nodes + Chronicle",
      "prompt": "I want AGI agents to explain how AGI Jobs, Nodes, validation, and Chronicle become a proof-gated work market.",
      "why": "Shows why agents, nodes, validation, and proof matter as one system.",
      "agents": [
        "architect",
        "research",
        "docket",
        "council"
      ],
      "authority": "Council",
      "gates": "AGI Jobs lifecycle, ProofBundle, validation, settlement boundary",
      "routes": [
        "agi-agent-mission-control.html",
        "agent-flow-academy.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "dossier",
      "num": 32,
      "title": "Prepare a Sovereign Dossier outline",
      "prompt": "I want AGI agents to prepare a Sovereign Dossier outline for a high-stakes proof mission.",
      "why": "Uses the strongest institutional packaging path for strategic work.",
      "agents": [
        "architect",
        "docket",
        "council",
        "human"
      ],
      "authority": "Council",
      "gates": "dossier index, reproduction, stress tests, boundaries, decision note",
      "routes": [
        "from-loop-to-rsi-state-capacity.html",
        "validation-control-tower.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "metrics",
      "num": 33,
      "title": "Define proof metrics dashboard",
      "prompt": "I want AGI agents to define the metrics that show whether proof quality is improving.",
      "why": "Keeps focus on verified work, not activity volume.",
      "agents": [
        "verifier",
        "docket",
        "chronicle",
        "sentinel"
      ],
      "authority": "AGI Node",
      "gates": "replayability, evidence quality, gate pass rate, proof debt",
      "routes": [
        "proof-metrics-dashboard.html",
        "site-health.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    },
    {
      "id": "frontier",
      "num": 34,
      "title": "Plan an end-to-end autonomous example",
      "prompt": "I want AGI agents to show a complete end-to-end example from objective to proof to validation to Chronicle.",
      "why": "Demonstrates the whole system in one concrete path.",
      "agents": [
        "architect",
        "planner",
        "node_worker",
        "node_validator",
        "docket",
        "chronicle",
        "human"
      ],
      "authority": "Hybrid",
      "gates": "mission contract, node handoff, evidence docket, validation, chronicle",
      "routes": [
        "agi-agent-mission-control.html",
        "validation-control-tower.html",
        "proof-run-001-docket.html"
      ],
      "outputs": [
        "Mission Contract JSON",
        "AGI Node Handoff JSON",
        "Evidence Docket Plan JSON",
        "Reviewer Brief Markdown",
        "Action Graph CSV"
      ],
      "steps": [
        "State the objective",
        "Select authority or auto-select",
        "Generate agent constellation",
        "Open recommended route",
        "Download review artifacts",
        "Validate before action"
      ]
    }
  ],
  "boundaries": [
    "No user data",
    "No user funds",
    "No wallet",
    "No transaction",
    "No network call",
    "No production authority",
    "Human review required for high-impact outcomes"
  ]
};
