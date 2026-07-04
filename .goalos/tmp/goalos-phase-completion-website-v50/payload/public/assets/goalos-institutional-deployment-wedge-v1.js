(() => {
  const $ = (id) => document.getElementById(id);
  const scenarios = {
    repo: {
      label: "Repository launch readiness",
      objective: "Convert one public-alpha repository workflow into a claim-bounded deployment wedge with Mission Contract, Evidence Docket plan, Selection Gate, canary monitor, rollback playbook, and reviewer packet.",
      class: "Public alpha", risk: "medium"
    },
    enterprise: {
      label: "Enterprise AI adoption review",
      objective: "Assess whether an enterprise AI workflow should move from report-only experimentation to proof-backed review, including claims matrix, source boundary, verifier mesh, risk ledger, and canary deployment plan.",
      class: "Institutional", risk: "high"
    },
    procurement: {
      label: "AI procurement / vendor diligence",
      objective: "Produce an evidence-backed vendor review package with claims matrix, source provenance, contradiction register, risk ledger, baseline comparison, and procurement decision state.",
      class: "Institutional", risk: "medium"
    },
    frontier: {
      label: "Frontier release governance",
      objective: "Evaluate whether a high-consequence AI release decision should proceed, pause, restrict, or require additional evidence under access, rollback, validator, and human authority gates.",
      class: "High consequence", risk: "critical"
    },
    policy: {
      label: "Public policy option review",
      objective: "Convert a public policy option into a claim-bounded Evidence Docket with source provenance, disagreement surface, risk ledger, decision state, and reviewer packet.",
      class: "Public interest", risk: "high"
    },
    security: {
      label: "Defensive security readiness",
      objective: "Review a repo-owned defensive security workflow for evidence quality, safe remediation boundaries, no external target scanning, no exploit execution, no unsafe automerge, and human-governed remediation readiness.",
      class: "Defensive", risk: "high"
    },
    science: {
      label: "Scientific discovery triage",
      objective: "Triage a scientific discovery workflow into a proof mission with hypothesis boundary, executable validation plan, baselines, risk ledger, delayed-outcome plan, and capability package path.",
      class: "Research", risk: "medium"
    }
  };

  const gateDefs = [
    ["workflow", "Repeatable workflow", "One bounded, repeated workflow is selected."],
    ["commit", "GoalOSCommit", "Objective, authority, constraints, success criteria, risk, and rollback obligations are explicit."],
    ["docket", "Evidence Docket", "Claims, baselines, proof packets, ledgers, and replay path are planned."],
    ["baselines", "Baseline ladder", "B0–B6 or appropriate comparators are declared."],
    ["replay", "Replay path", "A reviewer can reproduce or audit the result."],
    ["selection", "Selection Gate", "Score is advisory; gates are mandatory."],
    ["canary", "Canary monitor", "Expansion is limited, observed, and challengeable."],
    ["rollback", "Rollback ready", "A safe prior state or recovery plan exists."],
    ["boundary", "No-data / no-funds boundary", "No user data, funds, wallet, transaction, network call, or production authority."],
    ["human", "Human review", "The package is review-ready, not auto-authorized."]
  ];

  const state = {
    mode: "executive",
    stress: false,
    activeStep: 0,
    gates: {
      workflow: true, commit: true, docket: true, baselines: true, replay: true,
      selection: true, canary: false, rollback: false, boundary: true, human: true
    }
  };

  function scenario() { return scenarios[$("scenario").value] || scenarios.repo; }
  function values() {
    return {
      repeatability: +$("repeatability").value,
      impact: +$("impact").value,
      evidence: +$("evidence").value,
      validators: +$("validators").value,
      rollback: +$("rollbackLevel").value,
      risk: $("risk").value,
      objective: $("objective").value.trim() || scenario().objective
    };
  }

  function riskPenalty(risk) {
    return {low: 2, medium: 10, high: 22, critical: 36}[risk] || 12;
  }

  function compute() {
    const v = values();
    const gateCount = Object.values(state.gates).filter(Boolean).length;
    let base = Math.round(
      v.repeatability * .17 + v.impact * .13 + v.evidence * .20 +
      v.validators * .18 + v.rollback * .18 + gateCount * 5.2 - riskPenalty(v.risk)
    );
    let debt = Math.round(100 - (v.evidence * .32 + v.validators * .24 + v.rollback * .22 + gateCount * 2.2));
    if (state.stress) {
      base -= (v.risk === "critical" ? 16 : v.risk === "high" ? 10 : 6);
      base -= state.gates.rollback ? 0 : 10;
      base -= state.gates.canary ? 0 : 8;
      debt += (v.risk === "critical" ? 18 : 10);
    }
    base = Math.max(0, Math.min(100, base));
    debt = Math.max(0, Math.min(100, debt));
    let decision = "MISSION_DRAFT_REQUIRED";
    if (!state.gates.boundary) decision = "BLOCK_PRIVACY_BOUNDARY";
    else if (!state.gates.workflow || !state.gates.commit) decision = "MISSION_DRAFT_REQUIRED";
    else if (!state.gates.docket || !state.gates.baselines) decision = "EVIDENCE_DOCKET_REQUIRED";
    else if (!state.gates.replay) decision = "HOLD_REPLAY_REQUIRED";
    else if (!state.gates.selection) decision = "HOLD_SELECTION_GATE_REQUIRED";
    else if (!state.gates.rollback) decision = "HOLD_ROLLBACK_REQUIRED";
    else if (!state.gates.canary) decision = "HOLD_CANARY_REQUIRED";
    else if (!state.gates.human) decision = "HOLD_HUMAN_REVIEW_REQUIRED";
    else if (base >= 86) decision = "ROLLBACKABLE_EXPANSION_READY";
    else if (base >= 74) decision = "CANARY_READY";
    else if (base >= 62) decision = "SELECTION_GATE_REVIEW_READY";
    else decision = "HOLD_PENDING_REMEDIATION";

    const maturity = base >= 92 ? "L6" : base >= 84 ? "L5" : base >= 74 ? "L4" : base >= 64 ? "L3" : base >= 52 ? "L2" : "L1";
    return { ...v, readiness: base, proofDebt: debt, decision, maturity, gateCount };
  }

  function explainDecision(decision) {
    return {
      BLOCK_PRIVACY_BOUNDARY: "Deployment blocks because the public/private, no-data, or no-funds boundary is not intact.",
      MISSION_DRAFT_REQUIRED: "The workflow still needs a signed, scoped, claim-bounded mission commitment.",
      EVIDENCE_DOCKET_REQUIRED: "The workflow cannot advance until the Evidence Docket and baseline ladder are present.",
      HOLD_REPLAY_REQUIRED: "The workflow cannot scale because reviewers need a replay or audit path.",
      HOLD_SELECTION_GATE_REQUIRED: "Score alone cannot authorize expansion; the Selection Gate must pass.",
      HOLD_ROLLBACK_REQUIRED: "No rollback, no release. Add a rollback target and recovery playbook.",
      HOLD_CANARY_REQUIRED: "Expansion is held until a canary and monitoring plan exists.",
      HOLD_HUMAN_REVIEW_REQUIRED: "The package is not authorized until a human reviewer can inspect it.",
      HOLD_PENDING_REMEDIATION: "Some gates are present, but the workflow is not yet ready for canary.",
      SELECTION_GATE_REVIEW_READY: "The package is ready for Selection Gate review, not production authority.",
      CANARY_READY: "A limited canary can be reviewed, monitored, challenged, and rolled back.",
      ROLLBACKABLE_EXPANSION_READY: "The workflow has earned a limited, review-ready, rollbackable expansion path."
    }[decision] || "Review required.";
  }

  function renderToggles() {
    const wrap = $("gateControls");
    wrap.innerHTML = "";
    gateDefs.forEach(([key, title, desc]) => {
      const row = document.createElement("div");
      row.className = "toggle" + (state.gates[key] ? " on" : "");
      row.innerHTML = `<div><b>${title}</b><small>${desc}</small></div><button type="button" class="switch" aria-label="Toggle ${title}"></button>`;
      row.querySelector("button").addEventListener("click", () => {
        state.gates[key] = !state.gates[key];
        render();
      });
      wrap.appendChild(row);
    });
  }

  function renderLedger(result) {
    const wrap = $("gateLedger");
    wrap.innerHTML = "";
    gateDefs.forEach(([key, title, desc]) => {
      const pass = !!state.gates[key];
      const div = document.createElement("div");
      div.className = "gate " + (pass ? "pass" : "fail");
      div.innerHTML = `<div class="status">${pass ? "✓" : "!"}</div><div><b>${title}</b><p>${desc}</p></div>`;
      wrap.appendChild(div);
    });
  }

  function renderNodes(result) {
    document.querySelectorAll(".node").forEach((n, i) => {
      n.classList.remove("active", "blocked");
      if (i <= state.activeStep) n.classList.add("active");
      if ((result.decision.includes("HOLD") || result.decision.includes("BLOCK") || result.decision.includes("REQUIRED")) && i === Math.min(6, state.activeStep + 1)) {
        n.classList.add("blocked");
      }
    });
  }

  function renderTrace(result) {
    const technical = state.mode === "technical";
    const lines = [
      `Scenario: ${scenario().label}`,
      `Objective hash: local-demo-${Math.abs(hash(result.objective)).toString(16).slice(0,8)}`,
      `Readiness: ${result.readiness}/100 · Proof debt: ${result.proofDebt}/100 · Conformance: ${result.maturity}`,
      `Gate result: ${result.gateCount}/10 gates enabled`,
      `Decision: ${result.decision}`,
      explainDecision(result.decision)
    ];
    if (state.stress) lines.splice(3, 0, "Stress mode: rollout risk, validator latency, rollback burden, and challenge pressure increased.");
    if (technical) {
      lines.push(`Formula: readiness = repeatability + impact + evidence + validators + rollback + gates - risk - stress`);
      lines.push(`Risk class: ${result.risk.toUpperCase()} · Boundary: browser-local · External actions: 0`);
    }
    $("trace").innerHTML = lines.map((l, i) => `<p>${String(i).padStart(2,"0")}: ${escapeHtml(l)}</p>`).join("");
  }

  function renderInsight(result) {
    const exec = `GoalOS starts safely: one repeatable workflow, one mission contract, one Evidence Docket, one Selection Gate, one canary, one rollback path. It earns scale instead of assuming it.`;
    const tech = `Protocol view: GoalOSCommit → RunCommitment → ProofPacket → Evidence Docket → SelectionCertificate → RolloutReceipt → RollbackReceipt. Promotion is blocked unless proof, replay, scope, canary, rollback, challenge, and human review gates pass.`;
    $("insightBox").innerHTML = `<h3>${state.mode === "technical" ? "Technical" : "Plain English"}</h3><p>${state.mode === "technical" ? tech : exec}</p>`;
  }

  function render() {
    const result = compute();
    $("readiness").textContent = result.readiness;
    $("proofDebt").textContent = result.proofDebt;
    $("maturity").textContent = result.maturity;
    $("canary").textContent = state.gates.canary ? "ready" : "blocked";
    $("rollback").textContent = state.gates.rollback ? "ready" : "required";
    $("external").textContent = "0";
    $("decisionState").textContent = result.decision;
    $("decisionExplain").textContent = explainDecision(result.decision);
    $("readyArc").style.strokeDashoffset = String(427 - (427 * result.readiness / 100));
    renderLedger(result);
    renderNodes(result);
    renderTrace(result);
    renderInsight(result);
  }

  function packageData(kind) {
    const r = compute();
    return {
      artifact: kind,
      generatedAt: new Date().toISOString(),
      page: "institutional-deployment-wedge.html",
      scenario: scenario().label,
      objective: r.objective,
      riskClass: r.risk,
      readiness: r.readiness,
      proofDebt: r.proofDebt,
      conformance: r.maturity,
      decisionState: r.decision,
      gates: state.gates,
      deploymentWedge: [
        "Choose repeatable workflow",
        "Convert to GoalOSCommit",
        "Execute bounded agents",
        "Capture Evidence Docket",
        "Run Selection Gate",
        "Canary and monitor",
        "Rollbackable expansion"
      ],
      boundary: {
        noUserData: true,
        noUserFunds: true,
        noWallet: true,
        noTransaction: true,
        noNetworkCall: true,
        noProductionAuthority: true,
        humanReviewRequired: true
      }
    };
  }

  function downloadJson(name, data) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function downloadMd(name, title, data) {
    const body = `# ${title}

Generated: ${data.generatedAt}

## Scenario
${data.scenario}

## Objective
${data.objective}

## Decision state
${data.decisionState}

## Readiness
${data.readiness}/100

## Boundary
- No user data
- No user funds
- No wallet
- No transaction
- No network call
- No production authority
- Human review required

## Wedge
${data.deploymentWedge.map((x, i) => `${i+1}. ${x}`).join("\n")}

## Gates
${Object.entries(data.gates).map(([k,v]) => `- ${k}: ${v ? "pass" : "hold"}`).join("\n")}
`;
    const blob = new Blob([body], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function issueText() {
    const d = packageData("github-ready-pilot-issue");
    return `## Proof mission pilot proposal

**Scenario:** ${d.scenario}

**Objective:** ${d.objective}

**Risk class:** ${d.riskClass}

**Current decision state:** ${d.decisionState}

**Requested package:**
- Mission Contract
- Evidence Docket plan
- Claims Matrix
- Baseline ladder
- Replay checklist
- Validator packet
- Risk ledger
- Canary monitor
- Rollback playbook
- Governed Decision State

**Boundary confirmation:**
No personal data, customer data, confidential data, regulated data, credentials, wallet information, funds, private keys, seed phrases, or trade secrets are included.

**Human review:** required.`;
  }

  function copyIssue() {
    const txt = issueText();
    const box = document.createElement("textarea");
    box.value = txt;
    document.body.appendChild(box);
    box.select();
    document.execCommand("copy");
    box.remove();
    $("trace").insertAdjacentHTML("afterbegin", `<p>copied: GitHub-ready pilot issue draft copied to clipboard.</p>`);
  }

  function escapeHtml(s) { return s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function hash(s) { let h = 0; for (let i=0;i<s.length;i++) h = ((h<<5)-h) + s.charCodeAt(i) | 0; return h; }

  $("scenario").addEventListener("change", () => {
    const s = scenario();
    $("objective").value = s.objective;
    $("risk").value = s.risk;
    state.stress = false;
    state.activeStep = 0;
    render();
  });
  ["objective","repeatability","impact","evidence","validators","rollbackLevel","risk"].forEach(id => $(id).addEventListener("input", render));
  $("execMode").addEventListener("click", () => { state.mode = "executive"; $("execMode").classList.add("active"); $("techMode").classList.remove("active"); render(); });
  $("techMode").addEventListener("click", () => { state.mode = "technical"; $("techMode").classList.add("active"); $("execMode").classList.remove("active"); render(); });
  $("runWedge").addEventListener("click", () => {
    state.stress = false;
    let i = 0;
    const timer = setInterval(() => {
      state.activeStep = i;
      render();
      i += 1;
      if (i > 6) clearInterval(timer);
    }, 190);
  });
  $("stressWedge").addEventListener("click", () => { state.stress = true; state.activeStep = 4; render(); });
  $("resetWedge").addEventListener("click", () => {
    state.stress = false; state.activeStep = 0;
    state.gates = { workflow: true, commit: true, docket: true, baselines: true, replay: true, selection: true, canary: false, rollback: false, boundary: true, human: true };
    renderToggles(); render();
  });

  $("downloadPlan").addEventListener("click", () => downloadJson("goalos-deployment-wedge-plan.json", packageData("deployment-wedge-plan")));
  $("downloadCommit").addEventListener("click", () => downloadJson("goaloscommit.json", packageData("goaloscommit")));
  $("downloadDocket").addEventListener("click", () => downloadJson("evidence-docket-plan.json", packageData("evidence-docket-plan")));
  $("downloadCanary").addEventListener("click", () => downloadJson("canary-monitor-plan.json", packageData("canary-monitor")));
  $("downloadRollback").addEventListener("click", () => downloadJson("rollback-playbook.json", packageData("rollback-playbook")));
  $("downloadBrief").addEventListener("click", () => downloadMd("goalos-deployment-wedge-reviewer-brief.md", "GoalOS Deployment Wedge Reviewer Brief", packageData("reviewer-brief")));
  $("copyIssue").addEventListener("click", copyIssue);

  renderToggles();
  render();
})();