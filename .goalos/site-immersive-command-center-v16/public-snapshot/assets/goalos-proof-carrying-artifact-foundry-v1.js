(() => {
  "use strict";
  const gates = [
    ["proofValid", "Proof history"],
    ["evalPass", "Eval pass"],
    ["baselineCompared", "Baseline compared"],
    ["rollbackReady", "Rollback ready"],
    ["scopeAuthorized", "Scope authorized"],
    ["challengeCleared", "Challenge cleared"],
    ["privacyBoundary", "Public/private boundary"],
    ["replayPath", "Replay path"]
  ];
  const state = {
    mode: "exec",
    stress: false,
    ran: false,
    gate: Object.fromEntries(gates.map(([k]) => [k, true]))
  };
  const $ = id => document.getElementById(id);
  const artifactClass = $("artifactClass");
  const artifactText = $("artifactText");
  const riskClass = $("riskClass");
  const gateControls = $("gateControls");
  const timeline = $("timeline");
  const orbitNodes = $("orbitNodes");
  const readiness = $("readiness");
  const maturity = $("maturity");
  const debt = $("debt");
  const stateEl = $("state");
  const donutVal = $("donutVal");
  const decisionText = $("decisionText");
  const decisionExplain = $("decisionExplain");

  function artifactId() {
    const seed = `${artifactClass.value}:${artifactText.value}`;
    let h = 2166136261;
    for (let i = 0; i < seed.length; i++) { h ^= seed.charCodeAt(i); h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24); }
    return "pca-" + (h >>> 0).toString(16).padStart(8, "0");
  }
  function score() {
    const passed = gates.filter(([k]) => state.gate[k]).length;
    const required = passed / gates.length;
    const riskPenalty = riskClass.value === "restricted" ? 24 : riskClass.value === "review-required" ? 8 : 0;
    const stressPenalty = state.stress ? 18 : 0;
    const base = Math.round(32 + required * 76 - riskPenalty - stressPenalty);
    return Math.max(0, Math.min(100, base));
  }
  function rollbackDebt() {
    let val = 20 + (state.gate.rollbackReady ? 0 : 34) + (state.gate.replayPath ? 0 : 18) + (state.stress ? 24 : 0) + (riskClass.value === "restricted" ? 18 : 0);
    return Math.min(100, val);
  }
  function decision() {
    if (!state.gate.privacyBoundary) return ["BLOCK_PRIVACY_BOUNDARY", "Public proof must not expose private intelligence, customer data, credentials, secrets, or privileged workpapers."];
    if (riskClass.value === "restricted") return ["REJECT_SCOPE_RESTRICTED", "Restricted artifacts are quarantined and cannot be promoted by a public demo."];
    if (!state.gate.proofValid) return ["REJECT_NO_PROOF_HISTORY", "The artifact has no valid proof history, so it cannot earn reuse authority."];
    if (!state.gate.evalPass) return ["REJECT_EVAL_NOT_PASSED", "The artifact cannot propagate until the evaluation gate passes."];
    if (!state.gate.baselineCompared) return ["HOLD_BASELINE_REQUIRED", "A reusable artifact must be compared to a baseline before promotion."];
    if (!state.gate.rollbackReady) return ["HOLD_ROLLBACK_REQUIRED", "No rollback target means no release."];
    if (!state.gate.scopeAuthorized) return ["HOLD_SCOPE_NOT_AUTHORIZED", "The artifact scope must be explicitly authorized before propagation."];
    if (!state.gate.challengeCleared) return ["HOLD_CHALLENGE_WINDOW_OPEN", "Challenge window is still open; promotion remains paused."];
    if (!state.gate.replayPath) return ["HOLD_REPLAY_PATH_REQUIRED", "A replay path is required before reviewer-ready promotion."];
    if (state.stress) return ["CANARY_REVIEW_REQUIRED", "Stress review increased rollback debt. The artifact may enter canary review only."];
    return ["ACTIVE_REVIEW_READY", "The artifact is proof-carrying, rollbackable, scoped, and ready for human review as reusable capability."];
  }
  function conformance() {
    const [d] = decision();
    if (d.startsWith("ACTIVE")) return "L4";
    if (d.startsWith("CANARY")) return "L3";
    if (d.includes("ROLLBACK") || d.includes("REPLAY") || d.includes("SCOPE")) return "L2";
    if (d.includes("PROOF") || d.includes("EVAL")) return "L1";
    return "L0";
  }
  function logs() {
    const [d] = decision();
    const id = artifactId();
    const lines = [
      `[00] Artifact family resolved: ${id}`,
      `[01] Artifact class: ${artifactClass.value}`,
      `[02] Immutable version hash prepared: v.${id.slice(-6)}.001`,
      `[03] Proof history: ${state.gate.proofValid ? "present" : "missing"}`,
      `[04] Evaluation: ${state.gate.evalPass ? "passed" : "blocked"}`,
      `[05] Baseline comparison: ${state.gate.baselineCompared ? "recorded" : "required"}`,
      `[06] Rollback target: ${state.gate.rollbackReady ? "available" : "missing"}`,
      `[07] Scope authorization: ${state.gate.scopeAuthorized ? "bounded" : "not authorized"}`,
      `[08] Challenge window: ${state.gate.challengeCleared ? "cleared" : "open"}`,
      `[09] Replay path: ${state.gate.replayPath ? "published" : "missing"}`,
      `[10] Decision: ${d}`
    ];
    if (state.stress) lines.splice(6,0,"[stress] Rollback debt shock applied. Canary-only review enforced unless debt clears.");
    return lines;
  }
  function renderGates() {
    gateControls.innerHTML = "";
    gates.forEach(([k,label]) => {
      const el = document.createElement("button");
      el.className = "gate " + (state.gate[k] ? "on" : "");
      el.type = "button";
      el.innerHTML = `<b>${label}</b><i class="switch" aria-hidden="true"></i>`;
      el.addEventListener("click", () => { state.gate[k] = !state.gate[k]; state.ran = true; render(); });
      gateControls.appendChild(el);
    });
  }
  function renderOrbit() {
    const nodes = [
      ["Draft",108,160,"proofValid"],["Proof",218,96,"proofValid"],["Eval",360,72,"evalPass"],["Baseline",504,98,"baselineCompared"],["Rollback",614,168,"rollbackReady"],["Scope",594,332,"scopeAuthorized"],["Challenge",482,428,"challengeCleared"],["Replay",360,450,"replayPath"],["Boundary",228,424,"privacyBoundary"],["Canary",110,326,"rollbackReady"]
    ];
    orbitNodes.innerHTML = nodes.map(([label,x,y,g]) => `<g class="svgNode ${state.gate[g] ? "active" : "blocked"}" transform="translate(${x} ${y})"><circle r="34"/><text text-anchor="middle" y="5">${label}</text></g>`).join("");
  }
  function render() {
    renderGates(); renderOrbit();
    const s = score(); const rb = rollbackDebt(); const [d,ex] = decision();
    readiness.textContent = s; donutVal.textContent = s; debt.textContent = rb; maturity.textContent = conformance(); stateEl.textContent = d.replace(/_.*/, "");
    document.querySelector(".donut").style.setProperty("--p", s);
    decisionText.textContent = d; decisionExplain.textContent = ex;
    timeline.innerHTML = logs().map(line => `<div class="${line.includes("missing") || line.includes("blocked") || line.includes("required") || line.includes("not authorized") ? "logBad" : line.includes("stress") ? "logWarn" : ""}">${line}</div>`).join("");
  }
  function artifactObject() {
    const [d,ex] = decision();
    return {
      schema: "goalos.proof_carrying_artifact.v1",
      generatedAt: new Date().toISOString(),
      publicAlpha: true,
      browserLocal: true,
      noNetworkCall: true,
      noUserData: true,
      noUserFunds: true,
      humanReviewRequired: true,
      artifactId: artifactId(),
      artifactClass: artifactClass.value,
      title: artifactText.value.trim().slice(0, 220),
      immutableVersionHash: `sha256:${artifactId().slice(4).repeat(8).slice(0,64)}`,
      scope: riskClass.value,
      gates: Object.fromEntries(gates.map(([k,label]) => [k, {label, passed: state.gate[k]}])),
      readiness: score(),
      rollbackDebt: rollbackDebt(),
      conformance: conformance(),
      selectionStatus: d,
      decisionExplanation: ex,
      claimBoundary: ["Not achieved AGI", "Not achieved ASI", "Not empirical SOTA", "Not production authorization", "Not legal or financial advice"],
      publicPrivateBoundary: "Public proof uses commitments, hashes, attestations, replay paths, and claim boundaries. Private intelligence remains private."
    };
  }
  function download(name, type, body) {
    const blob = new Blob([body], {type});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 200);
  }
  function mdBrief() {
    const art = artifactObject();
    return `# GoalOS Proof-Carrying Artifact Review Brief\n\nArtifact: ${art.artifactId}\n\nClass: ${art.artifactClass}\n\nDecision: ${art.selectionStatus}\n\nReadiness: ${art.readiness}\n\nRollback debt: ${art.rollbackDebt}\n\n## Artifact under review\n\n${art.title}\n\n## Gate summary\n\n${Object.values(art.gates).map(g => `- ${g.passed ? "PASS" : "BLOCK"}: ${g.label}`).join("\n")}\n\n## Boundary\n\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n`;
  }
  function certificate() {
    const a = artifactObject();
    return {...a, certificateType:"SelectionCertificate", canaryScope:a.selectionStatus.startsWith("ACTIVE") ? "public-alpha-review" : "blocked-or-held", promotionAuthorized:false};
  }
  function rollback() {
    const a = artifactObject();
    return {schema:"goalos.rollback_receipt.v1", artifactId:a.artifactId, rollbackTarget:`${a.artifactId}@previous-safe`, rollbackReady:state.gate.rollbackReady, rollbackDebt:a.rollbackDebt, productionRollback:false, humanReviewRequired:true};
  }
  function ledger() {
    const a = artifactObject();
    return {schema:"goalos.evolution_ledger_entry.v1", entryType:"ProofCarryingArtifactCandidate", artifactId:a.artifactId, proofRoot:a.immutableVersionHash, decision:a.selectionStatus, publicSafe:true, privateIntelligenceStored:false, timestamp:a.generatedAt};
  }
  $("runBtn").addEventListener("click", () => { state.ran = true; state.stress = false; gates.forEach(([k]) => state.gate[k] = true); if (riskClass.value === "restricted") state.gate.scopeAuthorized = false; render(); });
  $("stressBtn").addEventListener("click", () => { state.ran = true; state.stress = !state.stress; if (state.stress) { state.gate.rollbackReady = false; state.gate.challengeCleared = false; } render(); });
  $("resetBtn").addEventListener("click", () => { state.stress = false; state.ran = false; gates.forEach(([k]) => state.gate[k] = true); state.gate.proofValid = false; state.gate.evalPass = false; render(); });
  document.querySelectorAll(".mode").forEach(btn => btn.addEventListener("click", () => { document.querySelectorAll(".mode").forEach(b => b.classList.remove("active")); btn.classList.add("active"); state.mode = btn.dataset.mode; render(); }));
  [artifactClass, artifactText, riskClass].forEach(el => el.addEventListener("input", render));
  $("downloadArtifact").addEventListener("click", () => download("goalos-proof-carrying-artifact.json", "application/json", JSON.stringify(artifactObject(), null, 2)));
  $("downloadSelection").addEventListener("click", () => download("goalos-selection-certificate.json", "application/json", JSON.stringify(certificate(), null, 2)));
  $("downloadRollback").addEventListener("click", () => download("goalos-rollback-receipt.json", "application/json", JSON.stringify(rollback(), null, 2)));
  $("downloadLedger").addEventListener("click", () => download("goalos-evolution-ledger-entry.json", "application/json", JSON.stringify(ledger(), null, 2)));
  $("downloadBrief").addEventListener("click", () => download("goalos-proof-carrying-artifact-review-brief.md", "text/markdown", mdBrief()));
  state.gate.proofValid = false; state.gate.evalPass = false; render();
})();
