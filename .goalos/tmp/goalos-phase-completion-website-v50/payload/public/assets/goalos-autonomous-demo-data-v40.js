
window.GOALOS_V40 = {
  version: "v40",
  stages: [
    ["01", "Objective", "Turn a plain-language request into a bounded mission."],
    ["02", "Agents", "Activate the smallest sufficient agent constellation."],
    ["03", "AGI Job", "Convert the mission into a bounded work package."],
    ["04", "AGI Node", "Prepare deterministic handoff and validation surface."],
    ["05", "ProofBundle", "Package artifacts, hashes, cost, risk, and replay."],
    ["06", "Evidence Docket", "Make claims inspectable, bounded, and reviewable."],
    ["07", "Validate", "Human, AGI Node, Hybrid, or Council review."],
    ["08", "Chronicle", "Record accepted memory and reusable capability."],
    ["09", "Reuse", "Turn accepted proof into future capability."],
    ["10", "Next", "Open the best proof route and download artifacts."]
  ],
  agents: [
    {id:"ARC", name:"Architect", role:"Frames the objective and boundaries."},
    {id:"PLN", name:"Planner", role:"Writes the Mission Contract."},
    {id:"RES", name:"Research", role:"Maps public-safe sources and routes."},
    {id:"BLD", name:"Builder", role:"Creates artifacts and page outputs."},
    {id:"VER", name:"Verifier", role:"Checks claims, gates, and evidence."},
    {id:"NOD", name:"AGI Node", role:"Prepares deterministic handoff."},
    {id:"VAL", name:"Validator", role:"Runs public-safe deterministic checks."},
    {id:"SEN", name:"Sentinel", role:"Watches risk, drift, and boundary."},
    {id:"DOC", name:"Docket", role:"Packages Evidence Docket plan."},
    {id:"CHR", name:"Chronicle", role:"Records accepted memory and reuse."}
  ],
  routes: [
    {title:"AGI Agent Workbench", href:"agi-agent-workbench.html", keywords:"agents workbench mission objective constellation agi node"},
    {title:"Autonomous Proof Mission Demo", href:"autonomous-proof-mission-demo.html", keywords:"demo end to end proof mission autonomous"},
    {title:"Mainnet Contract Atlas", href:"mainnet-contract-atlas.html", keywords:"48 contracts ethereum mainnet contract atlas"},
    {title:"Validation Control Tower", href:"validation-control-tower.html", keywords:"validate human agi node hybrid council"},
    {title:"Ask GoalOS", href:"ask-goalos.html", keywords:"ask question chat help concierge"},
    {title:"Tell GoalOS", href:"goalos.html", keywords:"tell goalos objective mission studio"},
    {title:"Proof Run 001", href:"proof-run-001-docket.html", keywords:"proof run 001 evidence docket review"},
    {title:"Loop to RSI", href:"from-loop-to-rsi-state-capacity.html", keywords:"loop rsi state capacity governance move 37"},
    {title:"Trust Boundary", href:"trust-boundary.html", keywords:"privacy data no funds no wallet no data"},
    {title:"Token Boundary", href:"token-boundary.html", keywords:"token agialpha sale custody wallet investment"},
    {title:"All Pages", href:"site-map.html", keywords:"all pages site map navigation"},
    {title:"Search", href:"search.html", keywords:"search command routes"}
  ],
  demos: [
    {
      id:"contracts", title:"Learn the 48 Ethereum Mainnet contracts", intent:"CONTRACT_ATLAS_LEARNING", authority:"AGI_NODE_PRECHECK_PLUS_HUMAN_REVIEW", 
      type:"Learning Mission", prompt:"I want AGI agents to help me understand the 48 Ethereum Mainnet contracts.",
      why:"A non-technical user learns what each public contract rail does, what it does not do, and where the token boundary sits.",
      agents:["ARC","RES","DOC","VAL","SEN"], routes:["mainnet-contract-atlas.html","mainnet-proof-rail.html","contract-academy.html","token-boundary.html"],
      done:"User can explain the contract rail, download the review packet, and avoid wallet/token confusion.",
      metrics:{readiness:94,replay:96,risk:99,reuse:86}
    },
    {id:"vendor", title:"Evaluate an AI vendor with evidence", intent:"VENDOR_EVIDENCE_REVIEW", authority:"HYBRID_VALIDATION_READY", type:"Decision Mission", prompt:"I want to evaluate an AI vendor using evidence, not marketing claims.", why:"Turns a vendor claim into a claims matrix, proof requirements, risk ledger, and reviewer brief.", agents:["ARC","PLN","RES","VER","DOC","VAL"], routes:["validation-control-tower.html","proof-run-001-docket.html","demo-ecosystem-registry.html","trust-boundary.html"], done:"Decision maker sees supported claims, missing evidence, risks, and next review actions.", metrics:{readiness:88,replay:82,risk:91,reuse:72}},
    {id:"proof", title:"Run a public-safe proof mission", intent:"PUBLIC_SAFE_PROOF_MISSION", authority:"AGI_NODE_VALIDATION_READY", type:"Proof Mission", prompt:"I want to run a public-safe proof mission from objective to Evidence Docket.", why:"Shows how output becomes proof, proof becomes a decision state, and accepted work becomes reusable capability.", agents:["ARC","PLN","BLD","VER","DOC","CHR"], routes:["autonomous-proof-mission-demo.html","proof-run-001-docket.html","validation-control-tower.html","site-health.html"], done:"Mission package includes contract, proof bundle, docket plan, validation certificate, and Chronicle entry.", metrics:{readiness:92,replay:93,risk:95,reuse:89}},
    {id:"rsi", title:"Understand Loop → RSI governance", intent:"LOOP_TO_RSI_REVIEW", authority:"COUNCIL_REVIEW_READY", type:"Governance Mission", prompt:"I want to understand Loop to RSI governance and Move-37 handling.", why:"Explains deterministic invention governance: target, emit, filter, atlas, test-plan, eval, insert, promote.", agents:["ARC","RES","VER","SEN","DOC","CHR"], routes:["from-loop-to-rsi-state-capacity.html","validation-control-tower.html","proof-mission-demo-academy.html"], done:"User understands why search control is not outcome authority and why breakthroughs require dossiers.", metrics:{readiness:86,replay:90,risk:98,reuse:80}},
    {id:"boundary", title:"Audit privacy, token, and no-data boundaries", intent:"BOUNDARY_AUDIT", authority:"AGI_NODE_VALIDATION_READY", type:"Trust Mission", prompt:"I want AGI agents to check privacy, token, and no-data boundaries across the website.", why:"Demonstrates how AGI Node checks can validate public-safe wording without collecting data or touching wallets.", agents:["SEN","VAL","VER","DOC"], routes:["trust-boundary.html","token-boundary.html","privacy.html","data-boundary.html","no-data-no-funds.html"], done:"Boundary report confirms no data, no funds, no wallet, no transaction, no network call posture.", metrics:{readiness:97,replay:95,risk:100,reuse:84}},
    {id:"complete", title:"Complete end-to-end autonomous example", intent:"FULL_DEMO_OBJECTIVE_TO_CHRONICLE", authority:"HYBRID_VALIDATION_READY", type:"Quintessential Demo", prompt:"I want AGI agents to show a complete end-to-end example from objective to proof to validation to Chronicle.", why:"The canonical demo for non-technical users: watch the whole GoalOS proof loop and download every artifact.", agents:["ARC","PLN","RES","BLD","VER","NOD","VAL","SEN","DOC","CHR"], routes:["autonomous-mission-studio.html","agi-agent-workbench.html","validation-control-tower.html","site-map.html"], done:"User sees the full system and leaves with replayable demo artifacts.", metrics:{readiness:95,replay:97,risk:96,reuse:93}}
  ]
};
