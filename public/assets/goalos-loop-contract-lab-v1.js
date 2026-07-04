(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const log = $("traceLog"), statePill = $("statePill"), gatesEl = $("gates"), flowEl = $("flow"), railEl = $("rail");
  const steps = [["Objective","Bind the work"],["Mission","Negotiate contract"],["Roles","Planner · generator · evaluator"],["Disk","Write state files"],["Trace","Read what happened"],["Restart","Resume from files"],["Docket","Package proof"],["Bottleneck","Expose next limit"]];
  const gates = [
    ["roleSeparation","Separate roles","Planner, generator, and evaluator do not collapse into one voice.",true],
    ["contractFirst","Contract before code","Done means testable assertions, not vibes.",true],
    ["diskState","Write state to disk","contract.md, progress.md, log.md, and feature_list.json exist.",true],
    ["restartable","Restartable loop","A sideways run can be discarded and resumed from state.",true],
    ["traceReadable","Readable traces","Debugging starts from logs, not memory or persuasion.",true],
    ["evaluatorIndependence","Independent evaluator","The generator cannot grade itself.",true],
    ["harnessMinimal","Deletable harness","Scaffolding shrinks when the model no longer needs it.",false],
    ["bottleneckVisible","Bottleneck visible","The next limiting factor is named before the next cycle.",true],
    ["proofBoundary","Public/private proof boundary","No user data, funds, wallet, transaction, or production authority.",true]
  ];
  const scenarios = {
    "repository-release": {short:"Release hardening", bottleneck:"download integrity", base:74},
    "proof-run-refresh": {short:"Proof Run refresh", bottleneck:"docket freshness", base:77},
    "documentation-qa": {short:"Docs QA sweep", bottleneck:"claim-boundary coverage", base:73},
    "demo-repair": {short:"Demo repair", bottleneck:"user feedback closure", base:70},
    "benchmark-bridge": {short:"Benchmark bridge", bottleneck:"equal-budget baselines", base:69}
  };
  const state = {stress:false, restarted:false, traceRead:false, harnessDeleted:false};
  const gateState = Object.fromEntries(gates.map(g => [g[0], g[3]]));

  function renderGates(){
    gatesEl.innerHTML = gates.map(g => `<button class="gate" type="button" data-gate="${g[0]}" aria-pressed="${gateState[g[0]]}"><span><strong>${g[1]}</strong><small>${g[2]}</small></span><span class="toggle ${gateState[g[0]] ? "on" : ""}" aria-hidden="true"></span></button>`).join("");
    gatesEl.querySelectorAll("[data-gate]").forEach(btn => btn.addEventListener("click", () => { gateState[btn.dataset.gate] = !gateState[btn.dataset.gate]; compute(); }));
  }
  function renderFlow(active=0){
    flowEl.innerHTML = steps.map((s,i)=>`<div class="step ${i<=active?"active":""}"><strong>${String(i+1).padStart(2,"0")} · ${s[0]}</strong><span>${s[1]}</span></div>`).join("");
    railEl.innerHTML = steps.map((s,i)=>`<div><strong>${s[0]}</strong><small>${i<=active?"passed":"queued"}</small></div>`).join("");
  }
  function shapeScore(text){
    const t = text.toLowerCase(); let score = 0;
    ["evidence","docket","replay","validator","risk","cost","rollback","human","boundary","claim","test","trace","contract","state"].forEach(w => { if(t.includes(w)) score += 3; });
    if(text.length > 160) score += 7; if(text.length > 360) score += 5;
    if(/all|always|guarantee|solves|autonomous production|achieved agi|achieved asi/i.test(text)) score -= 18;
    if(/public-safe|browser-local|no user data|human review|required/i.test(text)) score += 8;
    return Math.max(-25, Math.min(45, score));
  }
  function compute(){
    const scenario = scenarios[$("scenario").value] || scenarios["repository-release"];
    const objective = $("objective").value;
    let score = scenario.base + shapeScore(objective), penalties = 0;
    Object.entries(gateState).forEach(([k,v]) => { if(!v) penalties += k === "proofBoundary" ? 35 : 9; });
    if(state.stress) penalties += 14; if(state.traceRead) score += 6; if(state.restarted) score += 8; if(state.harnessDeleted) score += 5;
    score = Math.max(0, Math.min(100, score - penalties));
    let decision = "LOOP_REVIEW_READY";
    if(!gateState.proofBoundary) decision = "BLOCK_PRIVACY_BOUNDARY";
    else if(!gateState.contractFirst) decision = "REJECT_NO_CONTRACT";
    else if(!gateState.diskState) decision = "HOLD_STATE_FILES_REQUIRED";
    else if(!gateState.restartable) decision = "HOLD_RESTART_REQUIRED";
    else if(!gateState.evaluatorIndependence) decision = "REJECT_SELF_GRADED";
    else if(!gateState.traceReadable) decision = "HOLD_TRACE_REVIEW_REQUIRED";
    else if(state.stress && score < 70) decision = "HOLD_STRESS_REPAIR_REQUIRED";
    else if(!gateState.harnessMinimal) decision = "CANARY_REVIEW_ONLY";
    $("readiness").textContent = score;
    $("restartScore").textContent = Math.max(12, Math.min(99, score + (gateState.restartable ? 8 : -26))) + "%";
    $("traceScore").textContent = Math.max(10, Math.min(99, score + (state.traceRead ? 12 : -7))) + "%";
    $("overheadScore").textContent = Math.max(4, Math.min(80, 38 - (gateState.harnessMinimal ? 14 : 0) - (state.harnessDeleted ? 12 : 0) + (state.stress ? 18 : 0))) + "%";
    $("decision").textContent = decision;
    statePill.textContent = decision.includes("READY") ? "REVIEW READY" : decision.includes("BLOCK") || decision.includes("REJECT") ? "BLOCKED" : "HOLD";
    $("contractState").textContent = gateState.contractFirst ? "bounded" : "missing";
    $("progressState").textContent = state.restarted ? "resumed" : "active";
    $("logState").textContent = state.traceRead ? "reviewed" : "capturing";
    $("featureState").textContent = gateState.bottleneckVisible ? scenario.bottleneck : "unclear";
    $("loopHeadline").textContent = decision === "LOOP_REVIEW_READY" ? "The loop is review-ready." : decision.replaceAll("_"," ");
    $("loopExplanation").textContent = decision === "LOOP_REVIEW_READY" ? "The loop has role contracts, state files, restartability, trace review, evaluator independence, proof boundary, and a visible next bottleneck." : "One or more hard gates is blocking the loop. Score is advisory; gates are mandatory. Fix the highlighted contract before the next cycle.";
    renderGates();
    return {score, decision, scenario, objective};
  }
  function append(line){ log.textContent += "\n" + line; log.scrollTop = log.scrollHeight; }
  function runSequence(mode){
    if(mode==="stress") state.stress = true; if(mode==="restart") state.restarted = true;
    let i = 0;
    log.textContent = mode==="stress" ? "01 · Stress mode: weakening contract, evaluator, and restart assumptions." : mode==="restart" ? "01 · Restart mode: loading contract.md, progress.md, log.md, feature_list.json." : "01 · Loop started: objective committed.";
    const labels = ["Mission contract bounded.","Planner negotiated acceptance criteria.","Generator emitted candidate work package.","Evaluator challenged weak claims.","State written to disk.","Trace read for failure and drift.","Evidence Docket plan assembled.","Next bottleneck exposed."];
    const timer = setInterval(() => {
      i += 1; renderFlow(Math.min(i, steps.length-1)); append(String(i+1).padStart(2,"0") + " · " + labels[i-1]);
      if(i >= steps.length){ clearInterval(timer); state.traceRead = true; compute(); }
    }, 220);
  }
  function artifact(kind){
    const r = compute();
    const gateOut = Object.fromEntries(gates.map(g => [g[0], gateState[g[0]]]));
    const common = {title:"GoalOS Loop Contract Lab V1", kind, generatedAt:new Date().toISOString(), scenario:r.scenario.short, objective:r.objective, readiness:r.score, decisionState:r.decision, gates:gateOut, boundary:"No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."};
    if(kind==="contract") return `# GoalOS Loop Contract\n\nObjective: ${r.objective}\n\nScenario: ${r.scenario.short}\n\nRoles:\n- Planner: decomposes work and negotiates done criteria.\n- Generator: produces candidate artifacts.\n- Evaluator: reads traces and challenges unsupported claims.\n\nState files:\n- contract.md\n- progress.md\n- log.md\n- feature_list.json\n\nDecision state: ${r.decision}\n\nBoundary: ${common.boundary}\n`;
    if(kind==="state") return JSON.stringify({...common, files:["contract.md","progress.md","log.md","feature_list.json"], loopState:"restartable public-safe state pack"}, null, 2);
    if(kind==="docket") return JSON.stringify({...common, docket:["claims matrix","role contracts","trace summary","restart receipt","risk ledger","reviewer brief","claim boundary"]}, null, 2);
    if(kind==="bottleneck") return JSON.stringify({...common, bottleneck:r.scenario.bottleneck, recommendation:"Make the next bottleneck visible, then ship a smaller harness."}, null, 2);
    return `# Reviewer brief\n\nLoop Contract Lab V1 is a browser-local public demo. Inspect the objective, gates, trace log, restart behavior, downloads, and boundary.\n\nDecision: ${r.decision}\nReadiness: ${r.score}\n\nBoundary: ${common.boundary}\n`;
  }
  function download(kind){
    const data = artifact(kind), ext = kind === "contract" || kind === "review" ? "md" : "json";
    const blob = new Blob([data], {type: ext === "md" ? "text/markdown" : "application/json"});
    const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `goalos-loop-contract-lab-v1-${kind}.${ext}`;
    document.body.appendChild(a); a.click(); URL.revokeObjectURL(a.href); a.remove();
  }
  $("runLoop").addEventListener("click", () => runSequence("run"));
  $("stressLoop").addEventListener("click", () => runSequence("stress"));
  $("restartLoop").addEventListener("click", () => runSequence("restart"));
  $("readTraces").addEventListener("click", () => { state.traceRead = true; append("TRACE · evaluator found next bottleneck and preserved human-review boundary."); compute(); });
  $("deleteHarness").addEventListener("click", () => { state.harnessDeleted = true; gateState.harnessMinimal = true; append("HARNESS · deleted one unnecessary scaffold; kept proof boundary and restart files."); compute(); });
  $("copySummary").addEventListener("click", () => {
    const r = compute(); const text = `GoalOS Loop Contract Lab: ${r.decision} (${r.score}/100). A loop becomes institutional when it has role contracts, disk state, trace review, restart policy, and an Evidence Docket.`;
    if(navigator.clipboard && /* clipboard disabled in public-alpha */ console.log) /* clipboard disabled in public-alpha */ console.log(text);
    append("COPY · executive summary prepared.");
  });
  document.querySelectorAll("[data-download]").forEach(b => b.addEventListener("click", () => download(b.dataset.download)));
  $("scenario").addEventListener("change", () => { state.stress = false; compute(); });
  $("objective").addEventListener("input", compute);
  renderFlow(0); renderGates(); compute();
})();
