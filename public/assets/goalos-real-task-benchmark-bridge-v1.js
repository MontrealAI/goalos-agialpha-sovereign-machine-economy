(() => {
  "use strict";
  const $ = (q, root=document) => root.querySelector(q);
  const $$ = (q, root=document) => Array.from(root.querySelectorAll(q));

  const scenarioNames = {
    repo: "Repository launch readiness",
    software: "Software repair",
    web: "Web / desktop workflow",
    policy: "Policy-bound tool use",
    science: "Scientific / data workflow",
    agijobs: "Protocol-native AGI Jobs"
  };

  const baseScores = {
    repo: [44, 55, 61, 58, 70, 82, 89],
    software: [49, 57, 64, 59, 74, 86, 92],
    web: [41, 53, 59, 57, 68, 79, 87],
    policy: [47, 56, 62, 58, 73, 84, 90],
    science: [38, 49, 54, 52, 66, 77, 84],
    agijobs: [42, 51, 58, 56, 71, 83, 91]
  };

  const labels = [
    ["B0", "single agent"],
    ["B1", "report-only"],
    ["B2", "static workflow"],
    ["B3", "unstructured swarm"],
    ["B4", "fixed crew"],
    ["B5", "routed constellation"],
    ["B6", "GoalOS proof-governed"]
  ];

  const gates = ["task","budget","baselines","proof","replay","costrisk","validator","delayed","external"];
  let stress = false;
  let ran = false;

  const state = () => {
    const scenario = $("#scenario").value;
    const claim = $("#claimText").value.trim();
    const active = Object.fromEntries(gates.map(g => [g, $(`[data-gate="${g}"]`).checked]));
    const passed = gates.filter(g => active[g]).length;
    let scores = [...baseScores[scenario]];
    if (stress) {
      scores = scores.map((s, i) => {
        if (i === 4) return Math.min(96, s + 15);
        if (i === 5) return Math.min(98, s + 9);
        if (i === 6) return Math.max(36, s - 18);
        return Math.min(92, s + 4);
      });
    }
    let readiness = Math.round((passed / gates.length) * 72 + (scores[6] > Math.max(...scores.slice(0,6)) ? 18 : 0) + (ran ? 10 : 0));
    readiness = Math.max(0, Math.min(100, readiness));
    const leaderIndex = scores.indexOf(Math.max(...scores));
    let decision = "EMPIRICAL_BRIDGE_READY";
    if (!active.task) decision = "REJECT_NO_REAL_TASK";
    else if (!active.budget) decision = "REJECT_NO_EQUAL_BUDGET";
    else if (!active.baselines) decision = "REJECT_NO_BASELINES";
    else if (!active.proof) decision = "REJECT_NO_PROOFBUNDLE";
    else if (!active.replay) decision = "REJECT_UNREPLAYABLE";
    else if (!active.costrisk) decision = "HOLD_COST_RISK_LEDGER_REQUIRED";
    else if (!active.validator) decision = "HOLD_VALIDATOR_REPORT_REQUIRED";
    else if (!active.delayed) decision = "HOLD_DELAYED_OUTCOME_PLAN_REQUIRED";
    else if (!active.external) decision = "HOLD_EXTERNAL_REVIEW_REQUIRED";
    else if (leaderIndex !== 6) decision = "REJECT_BASELINES_WIN";
    else if (stress) decision = "HOLD_STRESS_REVIEW_REQUIRED";

    return {scenario, claim, active, passed, scores, leaderIndex, readiness, decision};
  };

  const explainDecision = (s) => {
    const map = {
      EMPIRICAL_BRIDGE_READY: "All bridge gates are present. The result is ready for human and external review, not automatic promotion.",
      REJECT_NO_REAL_TASK: "A strong claim cannot advance without a real task manifest.",
      REJECT_NO_EQUAL_BUDGET: "Baseline comparison is invalid without equal model/tool/budget constraints.",
      REJECT_NO_BASELINES: "A benchmark claim is blocked until strong baselines are present.",
      REJECT_NO_PROOFBUNDLE: "No ProofBundle / Evidence Docket, no stronger claim.",
      REJECT_UNREPLAYABLE: "If a reviewer cannot replay or audit the run, the claim is blocked.",
      HOLD_COST_RISK_LEDGER_REQUIRED: "Cost and risk ledgers are required before the claim can move forward.",
      HOLD_VALIDATOR_REPORT_REQUIRED: "A validator report is required before review-ready status.",
      HOLD_DELAYED_OUTCOME_PLAN_REQUIRED: "The bridge is close, but delayed-outcome tracking is still required.",
      HOLD_EXTERNAL_REVIEW_REQUIRED: "The bridge is internally ready but still needs an independent reviewer path.",
      REJECT_BASELINES_WIN: "A baseline currently beats the proof-governed architecture under stress. Revise the claim or improve the system.",
      HOLD_STRESS_REVIEW_REQUIRED: "Stress mode changed the benchmark landscape. Human review should inspect the stressed result."
    };
    return map[s.decision] || "Review required.";
  };

  function renderBars(scores, leaderIndex){
    $("#baselineBars").innerHTML = labels.map(([id,name],i)=>`
      <div class="bar ${i===leaderIndex?'leader':''}">
        <span>${id}</span>
        <div class="track"><div class="fill" style="width:${scores[i]}%"></div></div>
        <strong>${scores[i]}</strong>
      </div>
    `).join("");
  }

  function render(){
    const s = state();
    document.body.classList.toggle("stress", stress);
    $("#taskFamily").textContent = scenarioNames[s.scenario];
    $("#baselineWinner").textContent = labels[s.leaderIndex][0];
    $("#gatesPassed").textContent = `${s.passed}/${gates.length}`;
    $("#proofDebt").textContent = String(Math.max(0, 100 - s.readiness));
    $("#riskState").textContent = stress ? "stressed" : ($("#riskClass").value || "bounded").toLowerCase();
    $("#readinessNumber").textContent = s.readiness;
    $("#readinessRing").style.strokeDashoffset = String(440 - 440*(s.readiness/100));
    $("#decisionState").textContent = s.decision;
    $("#decisionExplain").textContent = explainDecision(s);
    $("#verdictTitle").textContent = s.decision === "EMPIRICAL_BRIDGE_READY" ? "Benchmark bridge is review-ready." : "Bridge is blocked or held.";
    $("#verdictCopy").textContent = explainDecision(s);
    renderBars(s.scores, s.leaderIndex);
    const events = [
      `Task family: ${scenarioNames[s.scenario]}.`,
      `Claim preserved: ${s.claim.slice(0, 130)}${s.claim.length>130?'…':''}`,
      `Baseline leader: ${labels[s.leaderIndex][0]} / ${labels[s.leaderIndex][1]} with score ${s.scores[s.leaderIndex]}.`,
      `Mandatory gates passed: ${s.passed}/${gates.length}.`,
      stress ? "Stress mode: stronger baselines, higher overhead, delayed-outcome burden enforced." : "Normal mode: bridge assembled under public-safe constraints.",
      `Decision state: ${s.decision}.`
    ];
    $("#chronicle").innerHTML = events.map((e,i)=>`<p>${String(i+1).padStart(2,'0')} · ${e}</p>`).join("");
  }

  function download(name, text, type="application/json"){
    const blob = new Blob([text], {type});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();}, 0);
  }

  function artifact(kind){
    const s = state();
    const now = new Date().toISOString();
    const common = {
      artifact: kind,
      generated_at: now,
      public_safe: true,
      browser_local: true,
      no_user_data: true,
      no_user_funds: true,
      no_wallet: true,
      no_transaction: true,
      no_network_call: true,
      human_review_required: true,
      scenario: scenarioNames[s.scenario],
      claim_under_test: s.claim,
      decision_state: s.decision,
      readiness: s.readiness,
      gates: s.active,
      baselines: labels.map(([id,name],i)=>({id,name,score:s.scores[i],leader:i===s.leaderIndex}))
    };
    if (kind === "matrix") {
      return "baseline,name,score,leader\n" + common.baselines.map(b=>`${b.id},${b.name},${b.score},${b.leader}`).join("\n");
    }
    if (kind === "brief") {
      return `# GoalOS Real-Task Benchmark Bridge Review Brief\n\nGenerated: ${now}\n\n## Scenario\n${common.scenario}\n\n## Claim under test\n${s.claim}\n\n## Decision state\n${s.decision}\n\n## Reviewer checks\n- Confirm task manifest is real and public-safe.\n- Confirm equal-budget baselines.\n- Confirm ProofBundle / Evidence Docket.\n- Confirm replay path.\n- Confirm cost and risk ledgers.\n- Confirm validator report.\n- Confirm delayed-outcome plan.\n- Confirm external review path.\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. Human review required.\n`;
    }
    return JSON.stringify(common, null, 2);
  }

  $("#runBridge").addEventListener("click",()=>{ran=true; render();});
  $("#stressBridge").addEventListener("click",()=>{stress=!stress; ran=true; render();});
  $("#resetBridge").addEventListener("click",()=>{stress=false; ran=false; gates.forEach(g=>$(`[data-gate="${g}"]`).checked = ["task","budget","baselines","proof","replay","costrisk","validator"].includes(g)); render();});
  $("#scenario").addEventListener("change",()=>{ran=true; render();});
  $("#riskClass").addEventListener("change",render);
  $("#claimText").addEventListener("input",render);
  $$("[data-gate]").forEach(el=>el.addEventListener("change",()=>{ran=true; render();}));
  $$(".mode").forEach(btn=>btn.addEventListener("click",()=>{
    $$(".mode").forEach(b=>b.classList.remove("active"));
    btn.classList.add("active");
    document.body.classList.toggle("technical", btn.dataset.mode === "technical");
  }));
  $$(".download").forEach(btn=>btn.addEventListener("click",()=>{
    const k = btn.dataset.download;
    if(k === "matrix") download("goalos-baseline-matrix.csv", artifact(k), "text/csv");
    else if(k === "brief") download("goalos-benchmark-reviewer-brief.md", artifact(k), "text/markdown");
    else if(k === "plan") download("goalos-benchmark-plan.json", artifact(k));
    else download("goalos-evidence-docket-plan.json", artifact(k));
  }));
  render();
})();
