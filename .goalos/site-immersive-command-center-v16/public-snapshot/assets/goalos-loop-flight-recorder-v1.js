(() => {
  "use strict";

  const gates = [
    ["contractFirst", "Contract before code", "The planner negotiates done conditions before generation."],
    ["roleSeparation", "Separate roles", "Planner, generator, evaluator, and harness stay distinct."],
    ["writeState", "Write state to disk", "Loop state is recoverable from files, not hidden context."],
    ["independentEvaluator", "Independent evaluator", "The generator does not grade itself."],
    ["traceReading", "Trace reading", "Debugging uses traces, not vibes."],
    ["restartReady", "Restart ready", "The loop can crash, reload state, and continue."],
    ["subjectiveRubric", "Taste rubric", "Design, originality, craft, and functionality are scoreable."],
    ["harnessLean", "Harness lean", "The harness does not dominate the work."],
    ["bottleneckVisible", "Bottleneck visible", "The next bottleneck is named and actionable."],
    ["boundary", "Public/private boundary", "No user data, funds, wallet, transaction, or production authority."]
  ];

  const files = [
    ["contract.json", "mission, roles, success, failure, gates"],
    ["state.json", "cycle, decisions, hashes, restart pointer"],
    ["progress.md", "append-only cycle notes"],
    ["trace.log", "agent actions, evaluator pushes, errors"],
    ["scorecard.json", "design, originality, craft, functionality"],
    ["bottleneck.md", "current constraint and next move"]
  ];

  const scenarios = {
    repo: "Turn a public-alpha repository release into a review-ready Evidence Docket: contract first, state on disk, traces readable, evaluator separate, restart clean, bottleneck visible.",
    proof: "Convert a claim into an Evidence Docket loop: claims matrix, baselines, proof packets, verifier notes, replay path, claim boundary, and reviewer brief.",
    mission: "Run a public-safe proof mission until DONE: mission contract, bounded work, evidence, verifier report, risk ledger, action graph, Chronicle, capability package.",
    review: "Prepare an external reviewer replay loop: docket, replay checklist, validator packet, dissent path, verdict states, and remediation queue."
  };

  const state = {
    cycle: 0,
    restarts: 0,
    stage: 0,
    stress: false,
    overhead: 44,
    proofDebt: 58,
    bottleneck: "contract",
    logs: ["00 · Loop recorder loaded.", "01 · Awaiting contract negotiation."],
    trace: ["trace: ready — no run has started."],
    gates: Object.fromEntries(gates.map(([k]) => [k, true]))
  };

  const $ = (id) => document.getElementById(id);
  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));

  function scenarioObjective(){
    return $("objective").value.trim() || scenarios[$("scenario").value] || scenarios.repo;
  }

  function tasteScore(){
    const vals = ["designScore","originalityScore","craftScore","functionScore"].map(id => Number($(id).value));
    return Math.round(vals.reduce((a,b)=>a+b,0)/vals.length);
  }

  function compute(){
    const missing = gates.filter(([k]) => !state.gates[k]).map(([k]) => k);
    const taste = tasteScore();
    let readiness = 38 + (gates.length - missing.length) * 6 + Math.round((taste - 50)/5) - Math.round((state.overhead - 40)/5) - Math.round(state.proofDebt/12);
    readiness = clamp(readiness, 0, 100);
    let decision = "LOOP_REVIEW_READY";
    if(!state.gates.boundary) decision = "BLOCK_PRIVACY_BOUNDARY";
    else if(!state.gates.contractFirst) decision = "REJECT_NO_CONTRACT";
    else if(!state.gates.roleSeparation) decision = "HOLD_ROLE_SEPARATION_REQUIRED";
    else if(!state.gates.writeState) decision = "HOLD_STATE_FILES_REQUIRED";
    else if(!state.gates.independentEvaluator) decision = "REJECT_SELF_GRADED_LOOP";
    else if(!state.gates.restartReady) decision = "HOLD_RESTART_REQUIRED";
    else if(!state.gates.traceReading) decision = "HOLD_TRACE_READING_REQUIRED";
    else if(!state.gates.subjectiveRubric) decision = "HOLD_TASTE_RUBRIC_REQUIRED";
    else if(!state.gates.bottleneckVisible) decision = "HOLD_BOTTLENECK_UNKNOWN";
    else if(!state.gates.harnessLean || state.overhead > 64) decision = "HOLD_HARNESS_OVERHEAD_DOMINATES";
    else if(readiness < 72) decision = "HOLD_PROOF_DEBT_REVIEW";
    const bottleneck = chooseBottleneck(decision, taste);
    return {readiness, decision, missing, bottleneck, taste};
  }

  function chooseBottleneck(decision, taste){
    if(decision.includes("CONTRACT")) return "contract";
    if(decision.includes("STATE")) return "disk state";
    if(decision.includes("SELF_GRADED")) return "role separation";
    if(decision.includes("RESTART")) return "restart";
    if(decision.includes("TRACE")) return "trace reading";
    if(decision.includes("TASTE") || taste < 62) return "subjective scoring";
    if(decision.includes("HARNESS") || state.overhead > 64) return "harness overhead";
    if(decision.includes("BOUNDARY")) return "public/private boundary";
    if(decision.includes("PROOF_DEBT")) return "proof debt";
    return state.cycle < 2 ? "iteration evidence" : "next harder mission";
  }

  function renderGates(){
    const wrap = $("gateList");
    wrap.innerHTML = "";
    for(const [key,label,desc] of gates){
      const row = document.createElement("div");
      row.className = "gate";
      row.innerHTML = `<div><label for="gate-${key}">${label}</label><p>${desc}</p></div><label class="switch"><input id="gate-${key}" type="checkbox" ${state.gates[key] ? "checked" : ""}><span class="slider"></span></label>`;
      wrap.appendChild(row);
      row.querySelector("input").addEventListener("change", e => {
        state.gates[key] = e.target.checked;
        log(`gate · ${label} ${e.target.checked ? "enabled" : "disabled"}`);
        update();
      });
    }
  }

  function renderGatesStateOnly(){
    for(const [key] of gates){
      const input = $("gate-"+key);
      if(input) input.checked = state.gates[key];
    }
  }

  function renderFiles(){
    const wrap = $("stateFiles");
    wrap.innerHTML = "";
    const active = state.cycle > 0 || state.restarts > 0;
    for(const [name,desc] of files){
      const ok = active && (state.gates.writeState || name === "contract.json");
      const row = document.createElement("div");
      row.className = "file";
      row.innerHTML = `<div><b>${name}</b><br><span>${desc}</span></div><span class="status ${ok ? "ok" : ""}" title="${ok ? "present" : "pending"}"></span>`;
      wrap.appendChild(row);
    }
  }

  function log(line){
    const stamp = String(state.logs.length).padStart(2,"0");
    state.logs.push(`${stamp} · ${line}`);
    state.logs = state.logs.slice(-10);
  }

  function trace(line){
    const stamp = new Date().toISOString().slice(11,19);
    state.trace.push(`${stamp} ${line}`);
    state.trace = state.trace.slice(-60);
  }

  function runLoop(){
    state.cycle += 1;
    state.stage = (state.stage + 1) % 8;
    state.proofDebt = clamp(state.proofDebt - 9 + (state.stress ? 6 : 0), 0, 100);
    if(state.gates.harnessLean) state.overhead = clamp(state.overhead - 3, 14, 100);
    log(`cycle ${state.cycle} executed: contract → act → verify → trace`);
    trace(`cycle=${state.cycle} objective="${scenarioObjective().slice(0,86)}"`);
    trace("planner: contract checked; generator: bounded artifact emitted; evaluator: gate ledger updated");
    state.gates.bottleneckVisible = true;
    update();
  }

  function stressLoop(){
    state.stress = true;
    state.overhead = clamp(state.overhead + 24, 0, 100);
    state.proofDebt = clamp(state.proofDebt + 18, 0, 100);
    state.gates.harnessLean = false;
    log("stress · weak loop injected: overhead and proof debt increased");
    trace("stress: evaluator detected brittle harness, vague acceptance criteria, and fixed bottleneck");
    update();
  }

  function restartLoop(){
    if(!state.gates.writeState || !state.gates.restartReady){
      log("restart blocked: disk state or restart gate missing");
      trace("restart: failed because state pack is incomplete");
    } else {
      state.restarts += 1;
      state.stage = 5;
      state.proofDebt = clamp(state.proofDebt - 6, 0, 100);
      log(`restart ${state.restarts}: state reloaded from disk pack`);
      trace(`restart: restored contract.json + state.json + progress.md at cycle ${state.cycle}`);
    }
    update();
  }

  function readTraces(){
    state.gates.traceReading = true;
    state.stage = 4;
    state.proofDebt = clamp(state.proofDebt - 8, 0, 100);
    log("trace reader: hidden bottleneck surfaced");
    trace("trace-reader: evaluator found the next issue in trace.log, not in the prompt");
    update();
  }

  function deleteHarness(){
    state.overhead = clamp(state.overhead - 18, 0, 100);
    if(state.overhead < 62) state.gates.harnessLean = true;
    state.stage = 6;
    log("harness trimmed: deleted obsolete scaffolding");
    trace("harness: retained contract/state/trace/replay; removed decorative wrapper");
    update();
  }

  function reset(){
    state.cycle = 0; state.restarts = 0; state.stage = 0; state.stress = false; state.overhead = 44; state.proofDebt = 58; state.logs = ["00 · Loop recorder reset.", "01 · Awaiting contract negotiation."]; state.trace = ["trace: reset — no run has started."]; state.gates = Object.fromEntries(gates.map(([k]) => [k, true]));
    renderGates();
    update();
  }

  function update(){
    const {readiness, decision, bottleneck, taste} = compute();
    state.bottleneck = bottleneck;
    $("decisionState").textContent = decision;
    $("readinessText").textContent = readiness;
    $("readinessArc").style.strokeDashoffset = String(314 - (readiness/100)*314);
    $("cycleCount").textContent = state.cycle;
    $("restartCount").textContent = state.restarts;
    $("proofDebt").textContent = state.proofDebt;
    $("harnessOverhead").textContent = `${state.overhead}%`;
    $("bottleneck").textContent = bottleneck;
    $("terminal").textContent = state.logs.join("\n");
    $("traceLog").textContent = state.trace.join("\n");
    $("bottleneckTitle").textContent = `Current bottleneck: ${bottleneck}`;
    $("bottleneckBody").textContent = bottleneckBody(bottleneck, decision, taste);
    $("nextMoves").innerHTML = nextMoves(bottleneck).map(x => `<li>${x}</li>`).join("");
    document.querySelectorAll("#proofRail button").forEach((b,i)=>b.classList.toggle("active", i === state.stage));
    renderFiles();
    renderGatesStateOnly();
  }

  function bottleneckBody(b, decision, taste){
    const map = {
      "contract": "The loop is not ready to act until success, failure, scope, files, gates, and review obligations are explicit.",
      "disk state": "The loop cannot be trusted to run for long horizons unless it can reload its state from files.",
      "role separation": "The generator cannot be the sole judge. Evaluation must be independent enough to push back.",
      "restart": "A long-running loop should survive crashes, session loss, and context loss.",
      "trace reading": "Debugging requires trace inspection. The loop must expose what happened, not only final output.",
      "subjective scoring": "Taste can be graded if design, originality, craft, and functionality are written down.",
      "harness overhead": "The harness is helping less than it costs. Delete scaffolding that the model no longer needs.",
      "public/private boundary": "Public proof must not ask for user data, funds, wallets, secrets, or production authority.",
      "proof debt": "Some claims remain under-supported. Add evidence, replay, or claim narrowing before promotion.",
      "iteration evidence": "The loop needs more cycles before it can show continuity and stable improvement.",
      "next harder mission": "The current loop is review-ready. The next move is to package the capability and apply it to a harder mission."
    };
    return `${map[b] || map.contract} Decision: ${decision}. Taste score: ${taste}.`;
  }

  function nextMoves(b){
    const map = {
      "contract": ["Write success criteria.", "Write failure criteria.", "Write the disk-state contract."],
      "disk state": ["Create contract.json.", "Create state.json.", "Append progress.md and trace.log."],
      "role separation": ["Split planner/generator/evaluator prompts.", "Forbid self-grading.", "Make evaluator push back."],
      "restart": ["Simulate crash.", "Reload from files.", "Continue without hidden context."],
      "trace reading": ["Open trace.log.", "Find the first divergent judgment.", "Patch the loop, not the final answer."],
      "subjective scoring": ["Define reference examples.", "Score design/originality/craft/functionality.", "Record rubric in scorecard.json."],
      "harness overhead": ["Delete obsolete wrappers.", "Keep only contract/state/trace/replay.", "Measure overhead after deletion."],
      "public/private boundary": ["Remove private data requests.", "Keep public proof commitments only.", "Require human review."],
      "proof debt": ["Narrow claims.", "Add baselines.", "Add replay and evaluator notes."],
      "iteration evidence": ["Run more cycles.", "Check state continuity.", "Compare proof debt over time."],
      "next harder mission": ["Download recorder.", "Seal the docket.", "Promote as a proof-carrying loop pattern."]
    };
    return map[b] || map.contract;
  }

  function artifact(kind){
    const c = compute();
    return {
      kind,
      demo: "GoalOS Loop Flight Recorder V1",
      generated_at: new Date().toISOString(),
      browser_local: true,
      no_user_data: true,
      no_user_funds: true,
      no_wallet: true,
      no_transaction: true,
      no_network_call: true,
      production_authority: false,
      human_review_required: true,
      objective: scenarioObjective(),
      cycle: state.cycle,
      restarts: state.restarts,
      decision_state: c.decision,
      readiness: c.readiness,
      proof_debt: state.proofDebt,
      harness_overhead: state.overhead,
      bottleneck: c.bottleneck,
      taste_score: c.taste,
      gates: state.gates,
      files: files.map(([name,desc]) => ({name, desc, status: state.cycle > 0 ? "present-or-planned" : "pending"})),
      trace: state.trace
    };
  }

  function download(name, data, type="application/json"){
    const blob = new Blob([typeof data === "string" ? data : JSON.stringify(data,null,2)], {type});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(a.href);
    a.remove();
  }

  function downloadRecorder(){ download("goalos-loop-flight-recorder-v1.json", artifact("loop-flight-recorder")); }
  function downloadState(){ download("goalos-loop-state-pack-v1.json", {...artifact("state-pack"), contract_file: "contract.json", state_file: "state.json", progress_file: "progress.md", trace_file: "trace.log"}); }
  function downloadDocket(){ download("goalos-loop-evidence-docket-plan-v1.json", {...artifact("evidence-docket-plan"), docket_elements:["manifest","claims matrix","role contracts","disk state","trace log","scorecard","bottleneck report","replay path","claim boundary"]}); }
  function downloadBottleneck(){ download("goalos-loop-bottleneck-report-v1.md", `# GoalOS Loop Bottleneck Report\n\nCurrent bottleneck: ${state.bottleneck}\n\nDecision: ${compute().decision}\n\nObjective: ${scenarioObjective()}\n\nNext moves:\n${nextMoves(state.bottleneck).map(x=>"- "+x).join("\n")}\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n`, "text/markdown"); }
  function downloadBrief(){ download("goalos-loop-reviewer-brief-v1.md", `# GoalOS Loop Flight Recorder V1 — Reviewer Brief\n\nThis browser-local demo shows how a long-running agent loop becomes review-ready by writing state to disk, separating roles, reading traces, restarting cleanly, scoring subjective quality, trimming harness overhead, and surfacing the next bottleneck.\n\nDecision: ${compute().decision}\nReadiness: ${compute().readiness}\n\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n`, "text/markdown"); }

  function bind(){
    $("scenario").addEventListener("change", e => { $("objective").value = scenarios[e.target.value]; log(`scenario loaded: ${e.target.options[e.target.selectedIndex].text}`); update(); });
    ["runLoop","runLoopTop"].forEach(id => $(id).addEventListener("click", runLoop));
    ["restartLoop","restartTop"].forEach(id => $(id).addEventListener("click", restartLoop));
    $("stressLoop").addEventListener("click", stressLoop);
    $("readTraces").addEventListener("click", readTraces);
    $("deleteHarness").addEventListener("click", deleteHarness);
    $("resetLoop").addEventListener("click", reset);
    ["designScore","originalityScore","craftScore","functionScore"].forEach(id => $(id).addEventListener("input", update));
    $("downloadRecorder").addEventListener("click", downloadRecorder);
    $("downloadTop").addEventListener("click", downloadRecorder);
    $("downloadState").addEventListener("click", downloadState);
    $("downloadDocket").addEventListener("click", downloadDocket);
    $("downloadBottleneck").addEventListener("click", downloadBottleneck);
    $("downloadBrief").addEventListener("click", downloadBrief);
    document.querySelectorAll("#proofRail button").forEach(btn => btn.addEventListener("click", () => { state.stage = Number(btn.dataset.stage); log(`stage selected: ${btn.textContent}`); update(); }));
  }

  renderGates();
  bind();
  update();
})();