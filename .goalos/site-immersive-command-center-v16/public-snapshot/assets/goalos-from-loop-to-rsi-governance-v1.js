(function(){
  "use strict";
  const $ = (id) => document.getElementById(id);
  const gates = [
    ["schema", "Schema-bound artifacts", "Artifacts validate; failures hard-stop."],
    ["replay", "Replay manifest", "Cycles reproduce from manifest hashes."],
    ["hash", "State hash continuity", "No silent reset or unexplained drift."],
    ["risk", "Risk gate", "Prohibited or critical-risk candidates block."],
    ["evidence", "Executed evidence", "Confidence cannot inflate from simulation alone."],
    ["baseline", "Baseline comparison", "Candidate is compared against incumbent / neighbor / null / current stack."],
    ["persistence", "Persistence under shocks", "High novelty must survive policy shocks and replays."],
    ["dossier", "Move‑37 dossier", "Breakthrough claims require reproduction, stress, persistence, and package."],
    ["omni", "OMNI has no outcome authority", "Interestingness may allocate search but cannot promote outcomes."],
    ["boundary", "Public/private proof boundary", "Private intelligence stays private; public proof is safe."],
    ["rollback", "Rollback ready", "Promotion includes a rollback target and monitoring condition."],
    ["human", "Human review", "High-impact evolution remains review-ready, not production-authorized."]
  ];
  const defaults = {
    schema:true,replay:true,hash:true,risk:true,evidence:false,baseline:true,
    persistence:false,dossier:false,omni:true,boundary:true,rollback:true,human:true
  };
  const state = { gates:{...defaults}, mode:"idle", activeStage:0, trace:[] };

  const scenarios = {
    governance: "Turn a restartable GoalOS agent loop into a deterministic RSI governance cycle that can propose, test, replay, baseline, and package a public-safe invention candidate without giving search control outcome authority.",
    breakthrough: "Evaluate a high-novelty Move‑37 candidate with reproduction, stress tests, persistence gate, baseline comparison, and a public-safe sovereign dossier.",
    omni: "Use OMNI-style interestingness to allocate exploration pressure across bridge regions while proving it cannot override risk, evidence, baseline, replay, or validator gates.",
    dossier: "Package a public-safe RSI dossier for a candidate that crossed novelty and advantage thresholds, including replay instructions, evidence objects, and validator notes."
  };

  function clamp(x){ return Math.max(0, Math.min(1, x)); }
  function num(id){ return Number($(id).value) / 100; }
  function setTrace(lines){ state.trace = lines; $("terminal").textContent = lines.join("\n"); }
  function fmt(x){ return Number(x).toFixed(2); }

  function eciLabel(score){
    if(score < .20) return "E0";
    if(score < .40) return "E1";
    if(score < .60) return "E2";
    if(score < .78) return "E3";
    if(score < .92) return "E4";
    return "E5";
  }

  function decision(){
    const g = state.gates;
    const novelty = num("novelty");
    const advantage = num("advantage");
    const eci = num("eciScore");
    const drift = num("driftRisk");
    if(!g.boundary) return ["BLOCK_PRIVACY_BOUNDARY", 0.10];
    if(!g.schema) return ["REJECT_SCHEMA_DRIFT", 0.18];
    if(!g.hash || drift > .72) return ["HOLD_STATE_HASH_REQUIRED", 0.28];
    if(!g.risk) return ["REJECT_RISK_GATE_FAILED", 0.22];
    if(!g.omni) return ["REJECT_OMNI_OUTCOME_AUTHORITY", 0.25];
    if(!g.replay) return ["HOLD_REPLAY_REQUIRED", 0.34];
    if(!g.baseline) return ["HOLD_BASELINE_COMPARISON_REQUIRED", 0.42];
    if(!g.evidence || eci < .48) return ["HOLD_EXECUTED_EVIDENCE_REQUIRED", 0.46];
    if(advantage < .18) return ["REJECT_BASELINES_WIN", 0.48];
    if(novelty >= .80 && !g.dossier) return ["HOLD_MOVE37_DOSSIER_REQUIRED", 0.58];
    if(novelty >= .80 && !g.persistence) return ["HOLD_PERSISTENCE_REQUIRED", 0.61];
    if(!g.rollback) return ["HOLD_ROLLBACK_REQUIRED", 0.65];
    if(!g.human) return ["HOLD_HUMAN_REVIEW_REQUIRED", 0.68];
    const base = .55 + .16*advantage + .13*eci + .09*(1-drift) + .07*(g.dossier?1:0);
    return [novelty >= .80 ? "MOVE37_DOSSIER_REVIEW_READY" : "RSI_REVIEW_READY", clamp(base)];
  }

  function render(){
    $("noveltyOut").textContent = fmt(num("novelty"));
    $("advantageOut").textContent = fmt(num("advantage"));
    $("eciOut").textContent = fmt(num("eciScore"));
    $("driftOut").textContent = fmt(num("driftRisk"));
    const [d, readiness] = decision();
    $("readiness").textContent = Math.round(readiness * 100);
    $("decision").textContent = d;
    $("eci").textContent = eciLabel(num("eciScore"));
    $("move37").textContent = num("novelty") >= .80 ? (state.gates.dossier ? "dossier" : "probe") : "normal";

    document.querySelectorAll("#pipelineViz span").forEach((el, i) => {
      el.classList.toggle("active", i <= state.activeStage);
    });
    document.querySelectorAll(".flow-card").forEach((el, i) => {
      el.classList.toggle("active", i <= Math.min(6, Math.floor(state.activeStage * 0.9)));
    });

    const metrics = [
      ["Novelty", num("novelty")],
      ["Advantage", num("advantage")],
      ["Evidence", num("eciScore")],
      ["Drift resistance", 1 - num("driftRisk")]
    ];
    $("scoreMatrix").innerHTML = metrics.map(([name,val]) => `
      <div class="score"><b>${name}<span>${Math.round(val*100)}</span></b><div class="bar"><i style="width:${Math.round(val*100)}%"></i></div></div>
    `).join("");

    $("gateList").innerHTML = gates.map(([key,name,desc]) => `
      <div class="gate">
        <div><strong>${name}</strong><small>${desc}</small></div>
        <label class="switch" aria-label="${name}">
          <input type="checkbox" data-gate="${key}" ${state.gates[key] ? "checked" : ""}>
          <span class="slider"></span>
        </label>
      </div>
    `).join("");
    document.querySelectorAll("[data-gate]").forEach(input => {
      input.addEventListener("change", e => { state.gates[e.target.dataset.gate] = e.target.checked; render(); });
    });
  }

  function artifact(kind){
    const [d, readiness] = decision();
    return {
      artifact: kind,
      version: "from-loop-to-rsi-governance-v1",
      generated_at: new Date().toISOString(),
      objective: $("objective").value,
      scenario: $("scenario").value,
      decision_state: d,
      readiness: Math.round(readiness * 100),
      evidence_contact_level: eciLabel(num("eciScore")),
      metrics: {
        novelty_distance: num("novelty"),
        advantage_delta: num("advantage"),
        evidence_contact: num("eciScore"),
        drift_risk: num("driftRisk")
      },
      gates: {...state.gates},
      pipeline: ["TARGET","EMIT","FILTER","ATLAS","TEST-PLAN","EVAL","INSERT","PROMOTE"],
      public_alpha_boundary: [
        "No user data",
        "No user funds",
        "No wallet",
        "No transaction",
        "No network call",
        "No production authority",
        "Human review required"
      ],
      trace: state.trace
    };
  }

  function download(name, data){
    const blob = new Blob([typeof data === "string" ? data : JSON.stringify(data, null, 2)], {type:"application/json"});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  }

  function runCycle(){
    state.activeStage = 7;
    state.gates.evidence = true;
    if(num("eciScore") < .52) $("eciScore").value = "58";
    setTrace([
      "01 · TARGET: exploration pressure allocated to public-safe RSI governance.",
      "02 · EMIT: candidate governance artifact generated under schema.",
      "03 · FILTER: risk gate applied; OMNI may route, never authorize.",
      "04 · ATLAS: mechanism links and contradictions mapped.",
      "05 · TEST-PLAN: falsification ladder and cheap probes scheduled.",
      "06 · EVAL: baseline-comparative evidence object minted.",
      "07 · INSERT: append-only archive update prepared.",
      "08 · PROMOTE: selection gate waiting on dossier / persistence / review."
    ]);
    render();
  }

  function stressMove37(){
    $("novelty").value = "88";
    $("advantage").value = "54";
    if(num("eciScore") < .46) $("eciScore").value = "46";
    state.gates.dossier = false;
    state.gates.persistence = false;
    state.activeStage = 5;
    setTrace([
      "01 · Move‑37 stress: novelty crossed high-skepticism threshold.",
      "02 · High novelty does not lower proof burden; it raises it.",
      "03 · Required: reproduce, stress-test, persistence gate, dossier.",
      "04 · Promotion blocked until dossier and persistence pass."
    ]);
    render();
  }

  function restartDisk(){
    state.gates.hash = true;
    state.gates.replay = true;
    $("driftRisk").value = "12";
    state.activeStage = 3;
    setTrace([
      "01 · Restart from disk: prompt_pack_hash verified.",
      "02 · runner_config_hash verified.",
      "03 · state_payload_hash verified.",
      "04 · cycle_index continuity preserved; no silent reset."
    ]);
    render();
  }

  function omniOverreach(){
    state.gates.omni = false;
    state.activeStage = 2;
    setTrace([
      "01 · OMNI overreach simulation: interestingness attempted outcome authority.",
      "02 · Selection gate rejected the path.",
      "03 · Search control may allocate exploration; it cannot promote outcomes."
    ]);
    render();
  }

  function packageDossier(){
    state.gates.dossier = true;
    state.gates.persistence = true;
    state.gates.rollback = true;
    if(num("eciScore") < .66) $("eciScore").value = "72";
    state.activeStage = 7;
    setTrace([
      "01 · Dossier packaging started.",
      "02 · Reproduction manifest added.",
      "03 · Policy-shock deltas attached.",
      "04 · Persistence gate passed in local simulation.",
      "05 · Reviewer-ready dossier emitted; human review still required."
    ]);
    render();
  }

  function readTraces(){
    state.gates.evidence = true;
    if(num("eciScore") < .60) $("eciScore").value = "64";
    state.activeStage = 6;
    setTrace([
      "01 · Trace reading pass: candidate, baseline, risk, and cost logs inspected.",
      "02 · ECI upgraded from simulated/probed toward executed local evidence.",
      "03 · Contradictions preserved in reviewer route.",
      "04 · Next bottleneck exposed: external replay and independent validation."
    ]);
    render();
  }

  function init(){
    $("scenario").addEventListener("change", e => { $("objective").value = scenarios[e.target.value]; render(); });
    ["novelty","advantage","eciScore","driftRisk"].forEach(id => $(id).addEventListener("input", render));
    ["runCycle","runCycleTop"].forEach(id => $(id).addEventListener("click", runCycle));
    ["stressMove37","stressTop"].forEach(id => $(id).addEventListener("click", stressMove37));
    $("restartDisk").addEventListener("click", restartDisk);
    $("omniOverreach").addEventListener("click", omniOverreach);
    $("packageDossier").addEventListener("click", packageDossier);
    $("readTraces").addEventListener("click", readTraces);
    $("downloadState").addEventListener("click", () => download("goalos-rsi-state-v1.json", artifact("rsi_state")));
    $("downloadDossier").addEventListener("click", () => download("goalos-move37-dossier-v1.json", artifact("move37_dossier")));
    $("downloadEci").addEventListener("click", () => download("goalos-eci-ledger-v1.json", artifact("eci_ledger")));
    $("downloadBaseline").addEventListener("click", () => download("goalos-baseline-report-v1.json", artifact("baseline_report")));
    $("downloadBrief").addEventListener("click", () => {
      const a = artifact("reviewer_brief");
      download("goalos-rsi-reviewer-brief-v1.json", a);
    });
    render();
  }
  if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
