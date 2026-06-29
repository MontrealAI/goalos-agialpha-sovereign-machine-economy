(() => {
  "use strict";

  const qs = (s, root = document) => root.querySelector(s);
  const qsa = (s, root = document) => [...root.querySelectorAll(s)];

  const gates = [
    { id:"goalos", name:"GoalOSCommit", note:"Aim object is signed, scoped, and claim-bound.", hard:true },
    { id:"run", name:"RunRoot", note:"Execution root pins agents, tools, context, policy, budget, and risk.", hard:true },
    { id:"proof", name:"ProofRoot", note:"Proof root binds outputs, trace roots, costs, latency, signatures, and evidence URI.", hard:true },
    { id:"eval", name:"EvalAttestation", note:"Evaluator attests to baselines, result, challenge window, and review status.", hard:true },
    { id:"selection", name:"SelectionCertificate", note:"Selection admits, rejects, canaries, promotes, pauses, or rolls back.", hard:true },
    { id:"rollback", name:"RollbackReceipt", note:"A valid rollback target and monitoring trigger exist before release.", hard:true },
    { id:"boundary", name:"Public/private boundary", note:"Private prompts, raw traces, customer data, and sensitive work stay private.", hard:true },
    { id:"challenge", name:"Challenge window", note:"The public proof root remains challengeable before evolution rights activate.", hard:true },
    { id:"quorum", name:"Validator quorum", note:"Independent review capacity is sufficient for the selected risk class.", hard:true },
    { id:"human", name:"Human review", note:"High-impact evolution remains review-ready, not production-authorized.", hard:true }
  ];

  const scenarios = {
    artifact: {
      title:"Proof-carrying artifact promotion",
      candidate:"Promote a proof-carrying workflow artifact from candidate to canary after public-safe proof roots, evaluator attestations, challenge window, validator quorum, and rollback receipt are ready."
    },
    mission: {
      title:"Mission OS proof-to-action run",
      candidate:"Record a public-safe Mission OS run whose Evidence Docket, Governed Decision State, Action Graph, Chronicle entry, and capability package are ready for external human review."
    },
    settlement: {
      title:"AGI Jobs settlement-ready ProofBundle",
      candidate:"Prepare a settlement-ready ProofBundle with job spec, policy context, pinned environment, proof roots, validator commitments, replay result, simulated receipt, and Chronicle pointer."
    },
    frontier: {
      title:"Frontier release governance packet",
      candidate:"Commit a frontier release governance packet with identity boundary, access matrix, safety review, validator quorum, rollback route, and human authority gate."
    }
  };

  const state = {
    mode:"executive",
    running:false,
    stress:false,
    gates:Object.fromEntries(gates.map(g => [g.id, true])),
    step:0
  };

  const publicItems = [
    "artifact ID / version hash",
    "GoalOSCommit hash",
    "RunRoot / trace root",
    "ProofRoot / evidence pointer",
    "EvalAttestation",
    "SelectionCertificate",
    "Rollout / Rollback receipt",
    "challenge-window status"
  ];
  const privateItems = [
    "LLM prompts and private context",
    "raw traces and long logs",
    "customer or confidential data",
    "sensitive tool outputs",
    "privileged evaluator workpapers"
  ];

  function requiredQuorum(){
    const risk = qs("#risk").value;
    return risk === "HIGH" ? 5 : risk === "MEDIUM" ? 3 : 2;
  }

  function compute(){
    const q = Number(qs("#quorum").value);
    const required = requiredQuorum();
    state.gates.quorum = q >= required;
    const failed = gates.filter(g => !state.gates[g.id]);
    let decision = "LEDGER_REVIEW_READY";
    let why = "All hard gates are ready for human review. No private intelligence is exposed.";
    if (!state.gates.boundary){ decision = "BLOCK_PRIVACY_BOUNDARY"; why = "Public proof cannot proceed while private intelligence or customer data could leak."; }
    else if (!state.gates.proof){ decision = "REJECT_NO_PROOF_ROOT"; why = "No evolution ledger entry can be reviewed without a ProofRoot."; }
    else if (!state.gates.eval){ decision = "REJECT_NO_EVAL_ATTESTATION"; why = "Evaluator attestation is missing. Score cannot become authority."; }
    else if (!state.gates.rollback){ decision = "HOLD_ROLLBACK_REQUIRED"; why = "Rollback target and monitoring trigger are required before release or promotion."; }
    else if (!state.gates.challenge){ decision = "HOLD_CHALLENGE_WINDOW"; why = "The proof must remain challengeable before evolution rights activate."; }
    else if (!state.gates.quorum){ decision = "HOLD_VALIDATOR_QUORUM_REQUIRED"; why = `Selected risk class requires quorum ≥ ${required}.`; }
    else if (!state.gates.human){ decision = "HOLD_HUMAN_REVIEW_REQUIRED"; why = "Human review remains mandatory for public-alpha evolution."; }
    else if (!state.gates.goalos || !state.gates.run || !state.gates.selection){ decision = "REVISE_SELECTION_CERTIFICATE"; why = "Commitment, run root, and selection certificate must be coherent."; }
    const readiness = Math.round((gates.length - failed.length) / gates.length * 100);
    return { failed, readiness, decision, why, quorum:q, required };
  }

  function renderToggles(){
    const box = qs("#toggles");
    box.innerHTML = gates.map(g => `
      <button class="gate-toggle" type="button" role="switch" aria-checked="${state.gates[g.id] ? "true" : "false"}" data-gate="${g.id}">
        <span>${g.name}<small>${g.note}</small></span>
        <span class="switch" aria-hidden="true"></span>
      </button>`).join("");
    qsa(".gate-toggle", box).forEach(btn => btn.addEventListener("click", () => {
      const id = btn.dataset.gate;
      state.gates[id] = !state.gates[id];
      state.stress = false;
      render();
    }));
  }

  function renderRail(result){
    const steps = ["GoalOSCommit","RunRoot","ProofRoot","EvalAttestation","SelectionCertificate","ChallengeWindow","RolloutReceipt","RollbackReceipt"];
    const active = state.running ? state.step : steps.length - 1;
    qs("#rail").innerHTML = `
      <svg viewBox="0 0 1280 360" role="img" aria-label="Animated Evolution Ledger sequence">
        <defs>
          <linearGradient id="railGrad" x1="0" x2="1">
            <stop offset="0" stop-color="#69ffd9"/>
            <stop offset=".42" stop-color="#ffe66d"/>
            <stop offset="1" stop-color="#bca7ff"/>
          </linearGradient>
          <filter id="railGlow"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect x="22" y="22" width="1236" height="316" rx="34" fill="rgba(9,16,31,.86)" stroke="rgba(255,255,255,.18)"/>
        <path d="M110 180 C 260 70, 370 285, 520 176 S 780 60, 930 178 S 1090 268, 1190 174" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="5"/>
        <path d="M110 180 C 260 70, 370 285, 520 176 S 780 60, 930 178 S 1090 268, 1190 174" fill="none" stroke="url(#railGrad)" stroke-width="6" stroke-linecap="round" stroke-dasharray="${Math.max(120, (active+1)*155)} 1400" filter="url(#railGlow)"/>
        ${steps.map((s,i) => {
          const x = 105 + i*154;
          const y = i % 2 ? 210 : 128;
          const ok = i <= active && result.failed.length === 0;
          const warn = i <= active && result.failed.length > 0;
          return `<g>
            <circle cx="${x}" cy="${y}" r="36" fill="${ok ? "#193f3b" : warn ? "#3e2436" : "#101b32"}" stroke="${ok ? "#69ffd9" : warn ? "#ff7da8" : "rgba(255,255,255,.25)"}" stroke-width="3"/>
            <text x="${x}" y="${y+6}" text-anchor="middle" font-size="19" font-weight="900" fill="#ffffff">${String(i+1).padStart(2,"0")}</text>
            <text x="${x}" y="${y+62}" text-anchor="middle" font-size="15" font-weight="900" fill="#f7fbff">${s}</text>
          </g>`;
        }).join("")}
        <text x="640" y="308" text-anchor="middle" font-size="22" font-weight="900" fill="#ffe66d">The ledger stores public commitments, not private intelligence.</text>
      </svg>`;
  }

  function renderLists(){
    qs("#publicList").innerHTML = publicItems.map(x => `<li>${x}</li>`).join("");
    qs("#privateList").innerHTML = privateItems.map(x => `<li>${x}</li>`).join("");
  }

  function renderGateLedger(result){
    qs("#gateLedger").innerHTML = gates.map(g => {
      const ok = state.gates[g.id];
      return `<article class="gate-row ${ok ? "" : "fail"}">
        <span class="icon">${ok ? "✓" : "!"}</span>
        <div><h3>${g.name}</h3><p>${g.note}</p></div>
      </article>`;
    }).join("");
  }

  function renderConsole(result){
    const scenario = scenarios[qs("#scenario").value];
    const lines = [
      `Ledger sequence: Commit → Execute → Prove → Evaluate → Select → Rollout → Rollback`,
      `Scenario: ${scenario.title}`,
      `Candidate: ${qs("#candidate").value.trim()}`,
      `Risk: ${qs("#risk").value} · Scope: ${qs("#scope").value} · Quorum: ${result.quorum}/${result.required}`,
      `Gate result: ${gates.length - result.failed.length}/${gates.length}`,
      `Decision: ${result.decision}`,
      `Reason: ${result.why}`,
      result.failed.length ? `Blocked gates: ${result.failed.map(g => g.name).join(", ")}` : `All hard gates pass. Output is review-ready, not production-authorized.`
    ];
    if (state.mode === "technical") {
      lines.push("");
      lines.push(`Public fields emitted: commitHash, policyRoot, riskClass, proofHash, evidenceURI, evalRoot, cost, latency, signatureBundle, challengeWindow, rollbackTarget.`);
      lines.push(`Private counterpart retained off-ledger: prompts, raw traces, customer data, sensitive tool output, evaluator workpapers.`);
    }
    qs("#consoleText").textContent = lines.join("\n");
  }

  function render(){
    const result = compute();
    qs("#quorumOut").textContent = qs("#quorum").value;
    qs("#readiness").textContent = result.readiness;
    qs("#decisionHero").textContent = result.decision;
    qs("#decisionWhy").textContent = result.why;
    qs("#gateCount").textContent = `${gates.length - result.failed.length}/${gates.length}`;
    qs("#pubCount").textContent = publicItems.length;
    qs("#privCount").textContent = privateItems.length;
    const ring = qs("#ring");
    const dash = 339 - (339 * result.readiness / 100);
    ring.style.strokeDashoffset = dash;
    ring.style.stroke = result.readiness === 100 ? "var(--mint)" : result.readiness >= 70 ? "var(--warn)" : "var(--danger)";
    renderToggles();
    renderRail(result);
    renderLists();
    renderGateLedger(result);
    renderConsole(result);
    document.body.dataset.mode = state.mode;
    qsa(".technical").forEach(el => el.classList.toggle("hidden", state.mode !== "technical"));
  }

  function runSequence(){
    state.running = true;
    state.step = 0;
    const max = 7;
    const tick = () => {
      render();
      if (state.step < max) {
        state.step += 1;
        setTimeout(tick, 170);
      } else {
        state.running = false;
        render();
      }
    };
    tick();
  }

  function stress(){
    state.stress = true;
    state.gates.rollback = false;
    state.gates.challenge = false;
    if (qs("#risk").value === "HIGH") state.gates.quorum = Number(qs("#quorum").value) >= 5;
    runSequence();
  }

  function restore(){
    state.stress = false;
    Object.keys(state.gates).forEach(k => state.gates[k] = true);
    qs("#quorum").value = requiredQuorum();
    runSequence();
  }

  function data(){
    const result = compute();
    const now = new Date().toISOString();
    return {
      title:"GoalOS Evolution Ledger Control Room V2",
      generated_at: now,
      scenario: qs("#scenario").value,
      candidate_artifact: qs("#candidate").value.trim(),
      risk_class: qs("#risk").value,
      scope: qs("#scope").value,
      validator_quorum: Number(qs("#quorum").value),
      readiness: result.readiness,
      decision_state: result.decision,
      failed_gates: result.failed.map(g => g.name),
      public_proof_fields: publicItems,
      private_intelligence_classes: privateItems,
      boundary: {
        no_user_data: true,
        no_user_funds: true,
        no_wallet: true,
        no_transaction: true,
        no_network_call: true,
        production_authority: false,
        human_review_required: true
      }
    };
  }

  function download(name, content, type="application/json"){
    const blob = new Blob([content], {type});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function handleDownload(kind){
    const d = data();
    if (kind === "ledger") download("goalos-evolution-ledger-public-entry-v2.json", JSON.stringify(d,null,2));
    if (kind === "selection") download("goalos-selection-certificate-v2.json", JSON.stringify({certificate:"SelectionCertificate", decision_state:d.decision_state, scope:d.scope, challenge_window_cleared:!d.failed_gates.includes("Challenge window"), human_review_required:true, generated_at:d.generated_at},null,2));
    if (kind === "rollback") download("goalos-rollback-receipt-v2.json", JSON.stringify({receipt:"RollbackReceipt", rollback_ready:!d.failed_gates.includes("RollbackReceipt"), rollback_target:"prior-safe-artifact-version", monitoring_trigger:"validator or incident threshold", production_authority:false},null,2));
    if (kind === "boundary") download("goalos-public-private-boundary-map-v2.json", JSON.stringify({public_proof:d.public_proof_fields, private_intelligence:d.private_intelligence_classes, no_user_data:true, no_wallet:true, no_transaction:true},null,2));
    if (kind === "brief") download("goalos-evolution-ledger-review-brief-v2.md", `# GoalOS Evolution Ledger Review Brief\n\nDecision: ${d.decision_state}\nReadiness: ${d.readiness}\n\n## Candidate\n${d.candidate_artifact}\n\n## Public proof\n${d.public_proof_fields.map(x=>`- ${x}`).join("\n")}\n\n## Private intelligence not published\n${d.private_intelligence_classes.map(x=>`- ${x}`).join("\n")}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. Human review required.\n`, "text/markdown");
  }

  function init(){
    qs("#scenario").addEventListener("change", e => {
      qs("#candidate").value = scenarios[e.target.value].candidate;
      runSequence();
    });
    ["risk","scope","quorum","candidate"].forEach(id => qs("#"+id).addEventListener("input", render));
    qsa(".mode").forEach(btn => btn.addEventListener("click", () => {
      state.mode = btn.dataset.mode;
      qsa(".mode").forEach(b => b.classList.toggle("active", b === btn));
      render();
    }));
    [qs("#run"), qs("#runTop")].forEach(b => b.addEventListener("click", runSequence));
    [qs("#stress"), qs("#stressTop")].forEach(b => b.addEventListener("click", stress));
    [qs("#restore"), qs("#restoreTop")].forEach(b => b.addEventListener("click", restore));
    qsa("[data-download]").forEach(btn => btn.addEventListener("click", () => handleDownload(btn.dataset.download)));
    qs("#quorum").value = requiredQuorum();
    render();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
