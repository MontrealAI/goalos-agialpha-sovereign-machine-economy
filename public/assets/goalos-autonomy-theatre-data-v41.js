window.GOALOS_V41 = {
  version: 'v41',
  title: 'GoalOS Autonomy Theatre V41',
  boundary: {
    noUserData: true,
    noFunds: true,
    noWallet: true,
    noTransaction: true,
    noNetworkCall: true,
    humanReviewForHighImpact: true
  },
  stages: [
    {id:'objective', label:'Objective', plain:'The user states what they want in normal language.', artifact:'Objective Card', gate:'Public-safe objective'},
    {id:'contract', label:'Mission Contract', plain:'GoalOS turns the request into scope, success criteria, constraints, risk class, outputs, and done condition.', artifact:'Mission Contract JSON', gate:'Claim boundary'},
    {id:'agents', label:'AGI Agents', plain:'A proof-governed agent constellation is selected: architect, planner, researcher, builder, verifier, node, sentinel, docket, chronicle, and human/council as needed.', artifact:'Agent Role Plan', gate:'Least sufficient topology'},
    {id:'job', label:'AGI Job', plain:'The work becomes a bounded job spec with allowed actions, proof requirements, cost/risk ledger, and validation path.', artifact:'AGI Job Spec JSON', gate:'Bounded work'},
    {id:'node', label:'AGI Node', plain:'A deterministic public-safe AGI Node handoff is prepared for schema, replay, docket, route, and boundary checks.', artifact:'AGI Node Handoff JSON', gate:'No wallet / no transaction'},
    {id:'proofbundle', label:'ProofBundle', plain:'Outputs are packaged as hashes, roots, manifests, replay instructions, cost/risk ledgers, and signatures placeholders.', artifact:'ProofBundle JSON', gate:'Replay-ready'},
    {id:'docket', label:'Evidence Docket', plain:'Claims, baselines, proof packets, contradictions, risks, costs, validator notes, and public/private boundary are organized into a proof room.', artifact:'Evidence Docket Plan', gate:'Docket completeness'},
    {id:'validate', label:'Validate', plain:'Human, AGI Node, Hybrid, or Council validation is selected based on risk, novelty, judgment, and impact.', artifact:'Validation Certificate', gate:'Human/AGI authority'},
    {id:'chronicle', label:'Chronicle', plain:'Accepted work becomes governed memory with lineage, reuse conditions, and rollback reminders.', artifact:'Chronicle Entry JSON', gate:'Append-only memory'},
    {id:'reuse', label:'Reusable Capability', plain:'The system emits what can be reused in the next mission and what must remain review-only.', artifact:'Capability Package Stub', gate:'No propagation without proof'}
  ],
  agents: [
    {id:'architect', name:'Architect Agent', role:'Frames the objective and success criteria.', short:'ARC'},
    {id:'planner', name:'Planner Agent', role:'Creates the Mission Contract and route plan.', short:'PLN'},
    {id:'research', name:'Research Agent', role:'Maps public-safe sources, pages, claims, and contradictions.', short:'RES'},
    {id:'builder', name:'Builder Agent', role:'Builds the public-safe artifact package.', short:'BLD'},
    {id:'verifier', name:'Verifier Agent', role:'Checks claim support, baselines, risks, and proof gaps.', short:'VER'},
    {id:'worker', name:'AGI Node Worker', role:'Prepares deterministic work-handoff and replay surface.', short:'WRK'},
    {id:'nodeValidator', name:'AGI Node Validator', role:'Validates public-safe deterministic gates.', short:'VAL'},
    {id:'sentinel', name:'Sentinel Agent', role:'Watches safety, privacy, token, route, and drift boundaries.', short:'SNT'},
    {id:'docket', name:'Evidence Docket Agent', role:'Packages claims, baselines, proof packets, routes, and reviewer notes.', short:'DOC'},
    {id:'chronicle', name:'Chronicle Agent', role:'Turns accepted work into append-only institutional memory.', short:'CHR'},
    {id:'human', name:'Human Reviewer', role:'Reviews judgment-heavy, high-impact, legal, financial, security, or publication decisions.', short:'HUM'},
    {id:'council', name:'Architect / Validator Council', role:'Handles RSI, Move-37, strategic, sovereign, or governance-changing claims.', short:'CNL'}
  ],
  routes: [
    {href:'autonomy-theatre.html', title:'Autonomy Theatre', desc:'Run the quintessential end-to-end autonomous proof mission demo.'},
    {href:'agi-agent-workbench.html', title:'AGI Agent Workbench', desc:'Tell AGI agents what you want and receive a proof-governed route.'},
    {href:'validation-control-tower.html', title:'Validation Control Tower', desc:'Choose Human, AGI Node, Hybrid, or Council validation.'},
    {href:'goalos.html', title:'Tell GoalOS', desc:'Use the one-box Mission Studio.'},
    {href:'ask-goalos.html', title:'Ask GoalOS', desc:'Ask questions and route to the right page.'},
    {href:'mainnet-contract-atlas.html', title:'48 Mainnet Contract Atlas', desc:'Learn the 48 GoalOS-created Ethereum Mainnet contracts.'},
    {href:'proof-run-001-docket.html', title:'Proof Run 001', desc:'Review a public proof docket.'},
    {href:'from-loop-to-rsi-state-capacity.html', title:'Loop → RSI', desc:'Understand deterministic invention governance.'},
    {href:'trust-boundary.html', title:'Trust Boundary', desc:'No user data, funds, wallet, transaction, network call, or production authority.'},
    {href:'token-boundary.html', title:'Token Boundary', desc:'$AGIALPHA public contract identification only; not available from GoalOS.'},
    {href:'site-map.html', title:'All Pages', desc:'Browse every public page.'},
    {href:'search.html', title:'Search', desc:'Search the public proof surface.'}
  ],
  demos: [
    {
      id:'complete',
      title:'Complete end-to-end demo',
      intent:'full-system',
      objective:'I want AGI agents to show a complete end-to-end example from objective to AGI Job to AGI Node to ProofBundle to Evidence Docket to validation to Chronicle to reusable capability.',
      why:'This is the fastest way for a non-technical user to understand the whole GoalOS system in one run.',
      agents:['architect','planner','research','builder','verifier','worker','nodeValidator','sentinel','docket','chronicle','human'],
      authority:'Hybrid: AGI Node precheck + Human final review',
      routes:['autonomy-theatre.html','agi-agent-workbench.html','validation-control-tower.html','proof-run-001-docket.html','site-map.html'],
      done:'A review-ready autonomous demo package with mission, job, node handoff, proof bundle, docket, validation, chronicle, and capability stub.'
    },
    {
      id:'contracts',
      title:'Learn the 48 Ethereum Mainnet contracts',
      intent:'contract-atlas',
      objective:'I want AGI agents to help me understand the 48 Ethereum Mainnet contracts and explain the proof rail in plain language.',
      why:'Users instantly see how GoalOS turns contracts into an institutional proof rail rather than a confusing list of addresses.',
      agents:['architect','research','docket','nodeValidator','sentinel','human'],
      authority:'AGI Node precheck + optional human review',
      routes:['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','token-boundary.html'],
      done:'A contract-learning map, boundary reminder, proof-rail route, and reviewer packet.'
    },
    {
      id:'vendor',
      title:'Evaluate an AI vendor using evidence',
      intent:'vendor-review',
      objective:'I want to evaluate an AI vendor using evidence, not marketing claims, and receive a decision-ready proof mission package.',
      why:'Shows how executives can turn vague vendor claims into a governed decision state.',
      agents:['architect','planner','research','verifier','docket','sentinel','human'],
      authority:'Human final review after AGI Node precheck',
      routes:['goalos.html','validation-control-tower.html','proof-run-001-docket.html','trust-boundary.html'],
      done:'A claims matrix, contradiction register, evidence docket plan, risk ledger, and executive reviewer brief.'
    },
    {
      id:'pilot',
      title:'Design a controlled pilot program',
      intent:'pilot',
      objective:'I want to design a controlled pilot where every serious pilot ends with an Evidence Docket and a clear review decision.',
      why:'Gives institutions a concrete adoption path: one workflow, one docket, one review gate, one rollback path.',
      agents:['architect','planner','builder','verifier','docket','human'],
      authority:'Hybrid validation',
      routes:['use-case-playbooks.html','validation-control-tower.html','trust-boundary.html','site-health.html'],
      done:'A pilot blueprint with success/failure criteria, artifacts, gates, and review-ready outputs.'
    },
    {
      id:'rsi',
      title:'Understand Loop → RSI governance',
      intent:'loop-rsi',
      objective:'I want to understand how long-running loops become deterministic RSI governance with replay, baselines, stress tests, dossiers, and no black-box outcome authority.',
      why:'Shows the core upgrade from agent loops to governed recursive invention.',
      agents:['architect','research','verifier','nodeValidator','sentinel','docket','council'],
      authority:'Architect / Validator Council',
      routes:['from-loop-to-rsi-state-capacity.html','agent-flow-academy-v38.html','validation-control-tower.html'],
      done:'A Loop→RSI learning route, Move-37 dossier reminder, and council review packet.'
    },
    {
      id:'boundary',
      title:'Audit privacy, token, and no-data boundaries',
      intent:'boundary-audit',
      objective:'I want AGI agents to check privacy, token, no-data, no-funds, no-wallet, no-transaction, and no-network-call boundaries across the website.',
      why:'Shows why GoalOS is proof-native, not data-hungry or wallet-first.',
      agents:['sentinel','verifier','nodeValidator','docket','human'],
      authority:'AGI Node deterministic checks + human boundary review',
      routes:['trust-boundary.html','token-boundary.html','privacy.html','data-boundary.html','no-data-no-funds.html'],
      done:'A boundary audit certificate and route list for trust/token/privacy review.'
    },
    {
      id:'cyber',
      title:'Plan a defensive cybersecurity proof mission',
      intent:'defensive-security',
      objective:'I want to plan a defensive, repo-owned, public-safe cybersecurity proof mission with no external scans, no exploit execution, no secrets, and human review before remediation.',
      why:'Shows how GoalOS handles high-risk domains by constraining scope, proof, and human review.',
      agents:['architect','planner','sentinel','verifier','docket','human','council'],
      authority:'Human + Council escalation',
      routes:['validation-control-tower.html','trust-boundary.html','proof-run-001-docket.html'],
      done:'A defensive mission plan with hard safety invariants and human-governed remediation boundary.'
    },
    {
      id:'procurement',
      title:'Create a proof-backed procurement record',
      intent:'procurement',
      objective:'I want to create a proof-backed procurement record for an AI product, with claims, baselines, risk ledger, reviewer brief, and decision state.',
      why:'Turns procurement from opinion and sales material into evidence-bound review.',
      agents:['architect','research','verifier','docket','human'],
      authority:'Human final review',
      routes:['goalos.html','validation-control-tower.html','trust-boundary.html'],
      done:'A procurement proof record with route cards, claims matrix, evidence docket plan, and executive brief.'
    }
  ]
};