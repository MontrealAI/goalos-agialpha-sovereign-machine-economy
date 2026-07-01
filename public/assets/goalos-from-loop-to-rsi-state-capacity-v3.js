(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const stages = [
    ['TARGET','Allocate exploration pressure across archive cells and strategic mandates.'],
    ['EMIT','Generate candidate artifacts, workflows, validators, dossiers, or invention candidates.'],
    ['FILTER','Apply risk gates, novelty checks, boringness checks, and OMNI interestingness without authority.'],
    ['ATLAS','Extract causal triples, mechanism chains, contradictions, side effects, and bridges.'],
    ['TEST‑PLAN','Build falsification ladders, cheap probes, policy shocks, and replay checks.'],
    ['EVAL','Run baseline-comparative evaluation, Evidence Contact Index updates, and cost/risk ledgers.'],
    ['INSERT','Append evidence-backed candidates to archive cells without silent mutation.'],
    ['PROMOTE','Queue a dossier for council review only after mechanical gates pass.']
  ];
  const gates = [
    ['schema','Schema-bound artifacts','Failures hard-stop. No silent corruption.', true],
    ['stateHash','State hash continuity','Prompt, runner, and state hashes bind continuation.', true],
    ['drift','Drift sentinel','Unexplained prompt/state/config drift halts the run.', true],
    ['executed','Executed evidence','Confidence cannot inflate from simulated reasoning alone.', true],
    ['baseline','Baseline comparison','Candidate must beat incumbent / neighbor / null baselines.', true],
    ['omni','OMNI allocation-only','Interestingness may allocate search; it cannot promote outcomes.', true],
    ['dossier','Move‑37 dossier','High-novelty candidates require reproduction, stress, persistence, and packaging.', true],
    ['persistenceGate','Shock persistence','Breakthrough advantage must persist under policy shocks.', true],
    ['council','Architect / Validator Council','Independent review with stop authority before strategic promotion.', true],
    ['rollback','Rollback ready','No release without rollback target and monitoring condition.', true],
    ['boundary','Public/private proof boundary','Private intelligence stays private; public proof stays inspectable.', true],
    ['human','Human review required','This public-alpha demo never grants production authority.', true]
  ];
  const scenarioText = {
    'rsi-pilot':'Design a public-alpha RSI governance pilot that converts a long-running agent loop into deterministic invention operations with replay, ECI evidence, baseline comparison, Move‑37 dossier packaging, and Architect / Validator Council review.',
    'move37':'Evaluate a high-novelty Move‑37 candidate and package it only if reproduction, policy-shock stress tests, baseline advantage, ECI evidence, and council review pass.',
    'darpa-gap':'Demonstrate why project-based R&D needs a durable RSI control plane: deterministic replay, mechanical gates, append-only ledgers, and dossier packaging that survives personnel churn.',
    'frontier-lab':'Show how RSI complements frontier labs: capability velocity stays valuable, but durable compounding advantage requires replay, evidence-first promotion, baseline discipline, and governance.',
    'redteam':'Run a red-team drill for false positives, normalization of deviance, metric capture, lost context, and governance capture; require hard-stop semantics and independent verification.'
  };
  const stageHost = $('pipeline');
  const miniRail = $('miniRail');
  stages.forEach((s, i) => {
    const el = document.createElement('button');
    el.className = 'stage'; el.dataset.i = String(i);
    el.innerHTML = `<small>${String(i+1).padStart(2,'0')}</small><strong>${s[0]}</strong><span>${s[1].split(' ').slice(0,5).join(' ')}...</span>`;
    el.addEventListener('click', () => setStage(i));
    stageHost.appendChild(el);
    const m = document.createElement('button');
    m.textContent = s[0]; m.dataset.i = String(i); m.addEventListener('click', () => setStage(i));
    miniRail.appendChild(m);
  });
  const gateHost = $('gateList');
  gates.forEach(([key, title, note, value]) => {
    const el = document.createElement('div');
    el.className = 'gate';
    el.innerHTML = `<label class="switch" aria-label="${title}"><input id="gate-${key}" type="checkbox" ${value?'checked':''}><span class="knob"></span></label><div><strong>${title}</strong><small>${note}</small></div>`;
    gateHost.appendChild(el);
    el.querySelector('input').addEventListener('change', update);
  });
  const dash = $('dashboard');
  const dashItems = ['Replayability','Evidence quality','Exploration quality','Advantage confirmation','Safety','State integrity'];
  dashItems.forEach(name => {
    const d = document.createElement('div'); d.className = 'dash-card'; d.innerHTML = `<span>${name}</span><div class="bar"><i style="--w:30%"></i></div>`; dash.appendChild(d);
  });
  const council = [
    ['Architect','scope / design authority','Reviews whether the RSI kernel belongs in the pilot scope.'],
    ['Validator','replay / baselines','Checks reproduction, baselines, ECI, and persistence.'],
    ['Red Team','failure modes','Assumes false positives, metric capture, drift, and capture attempts.'],
    ['Dossier Lead','public proof package','Packages public-safe evidence without leaking private intelligence.'],
    ['Human Authority','final boundary','May accept, reject, request revision, or keep the run review-ready only.']
  ];
  const councilGrid = $('councilGrid');
  council.forEach(c => { const el = document.createElement('div'); el.className = 'council-card'; el.innerHTML = `<strong>${c[0]}<span>${c[1]}</span></strong><p>${c[2]}</p>`; councilGrid.appendChild(el); });
  const failures = [
    ['False positives / hair triggers','Independent verification and mandatory reproduction before promotion.'],
    ['Normalization of deviance','Hard-stop semantics and non-bypassable gates.'],
    ['Model risk / metric capture','ECI caps, stress tests, and calibration drift monitoring.'],
    ['Stovepipes / lost context','Atlas, dossiers, schema-bound artifacts, and append-only ledgers.'],
    ['Political / contractor capture','Architect / Validator Council, stop authority, and public proof boundaries.']
  ];
  const failureList = $('failureList');
  failures.forEach(f => { const el = document.createElement('div'); el.className = 'failure'; el.innerHTML = `<strong>${f[0]}<span>hardening</span></strong><p>${f[1]}</p>`; failureList.appendChild(el); });

  const inputs = ['replayability','eci','novelty','advantage','persistence','risk'];
  inputs.forEach(id => $(id).addEventListener('input', update));
  $('scenario').addEventListener('change', () => { $('objective').value = scenarioText[$('scenario').value]; update(); });
  $('objective').addEventListener('input', update);
  ['runCycle','runCycleTop'].forEach(id => $(id).addEventListener('click', runCycle));
  ['stressMove37','stressTop'].forEach(id => $(id).addEventListener('click', stress));
  $('restartManifest').addEventListener('click', restart);
  $('packageTop').addEventListener('click', packageDossier);
  $('downloadState').addEventListener('click', () => download('rsi-state', stateObject()));
  $('downloadMove37').addEventListener('click', () => download('move37-dossier', dossierObject()));
  $('downloadECI').addEventListener('click', () => download('eci-ledger', eciObject()));
  $('downloadCouncil').addEventListener('click', () => download('council-memo', councilObject()));
  $('downloadPilot').addEventListener('click', () => download('rsi-90-day-pilot-plan', pilotObject()));
  $('downloadBrief').addEventListener('click', () => download('reviewer-brief', reviewerObject()));

  let activeStage = 0;
  let ran = false;
  let tick = null;
  function setStage(i){
    activeStage = i;
    document.querySelectorAll('.stage').forEach((el, idx) => { el.classList.toggle('active', idx === i); el.classList.toggle('done', idx < i); });
    miniRail.querySelectorAll('button').forEach((el, idx) => el.classList.toggle('active', idx === i));
    $('stageDetail').innerHTML = `<h3>${stages[i][0]}</h3><p>${stages[i][1]}</p>`;
  }
  function gate(key){ return $(`gate-${key}`).checked; }
  function vals(){
    return {
      scenario: $('scenario').value,
      objective: $('objective').value.trim(),
      replayability: +$('replayability').value,
      eci: +$('eci').value,
      novelty: +$('novelty').value,
      advantage: +$('advantage').value,
      persistence: +$('persistence').value,
      risk: +$('risk').value
    };
  }
  function decision(){
    const v = vals();
    if (!gate('boundary')) return ['BLOCK_PRIVACY_BOUNDARY','Private intelligence / public proof boundary is disabled.'];
    if (!gate('schema')) return ['REJECT_SCHEMA_DRIFT','Schema-bound artifact gate is disabled.'];
    if (!gate('stateHash')) return ['HOLD_STATE_HASH_REQUIRED','State hash continuity is required before continuation.'];
    if (!gate('drift')) return ['REJECT_DRIFT_UNDETECTED','Drift sentinel is required for RSI governance.'];
    if (!gate('executed') || v.eci < 2) return ['HOLD_EXECUTED_EVIDENCE_REQUIRED','ECI must reach executed evidence before promotion.'];
    if (!gate('baseline')) return ['HOLD_BASELINE_COMPARISON_REQUIRED','Baseline discipline is mandatory.'];
    if (!gate('omni')) return ['REJECT_OMNI_OUTCOME_AUTHORITY','OMNI was granted outcome authority. Search allocation only.'];
    if (v.risk >= 76) return ['REJECT_RISK_GATE_FAILED','Risk pressure exceeds the public-alpha threshold.'];
    if (!gate('persistenceGate') || (v.novelty >= 80 && v.persistence < 70)) return ['HOLD_PERSISTENCE_REQUIRED','High novelty increases skepticism and requires shock persistence.'];
    if (v.advantage <= 0) return ['REJECT_BASELINES_WIN','Candidate does not beat relevant baselines.'];
    if (v.novelty >= 75 && !gate('dossier')) return ['HOLD_MOVE37_DOSSIER_REQUIRED','Move‑37 candidates require dossier packaging.'];
    if (!gate('council')) return ['HOLD_COUNCIL_REVIEW_REQUIRED','Architect / Validator Council review is required.'];
    if (!gate('rollback')) return ['HOLD_ROLLBACK_REQUIRED','Rollback readiness is mandatory.'];
    if (!gate('human')) return ['HOLD_HUMAN_REVIEW_REQUIRED','Human review boundary must remain active.'];
    if (v.novelty >= 80 && v.advantage >= 20) return ['MOVE37_DOSSIER_REVIEW_READY','High-novelty candidate is ready for dossier review, not automatic promotion.'];
    return ['RSI_STATE_CAPACITY_REVIEW_READY','Pilot is review-ready under public-alpha boundaries.'];
  }
  function readiness(){
    const v = vals(); const [d] = decision();
    let score = 20 + v.replayability*.18 + v.eci*7 + Math.max(0,v.advantage)*.22 + v.persistence*.16 + (100-v.risk)*.14;
    ['schema','stateHash','drift','executed','baseline','omni','dossier','persistenceGate','council','rollback','boundary','human'].forEach(k => score += gate(k) ? 2.4 : -9);
    if (d.startsWith('REJECT') || d.startsWith('BLOCK')) score -= 24;
    return Math.max(0, Math.min(100, Math.round(score)));
  }
  function update(){
    const v = vals();
    $('replayabilityOut').textContent = `${v.replayability}%`;
    $('eciOut').textContent = `E${v.eci}`;
    $('noveltyOut').textContent = (v.novelty/100).toFixed(2);
    $('advantageOut').textContent = `${v.advantage >= 0 ? '+' : ''}${v.advantage}%`;
    $('persistenceOut').textContent = `${v.persistence}%`;
    $('riskOut').textContent = `${v.risk}%`;
    const [state, reason] = decision();
    const r = readiness();
    $('decisionState').textContent = state;
    $('consoleStatus').textContent = state;
    $('decisionReason').textContent = reason;
    $('readinessMetric').textContent = r;
    $('eciMetric').textContent = `E${v.eci}`;
    $('deltaMetric').textContent = `${v.advantage >= 0 ? '+' : ''}${v.advantage}%`;
    $('shockMetric').textContent = `${v.persistence}%`;
    $('authorityMetric').textContent = gate('omni') ? '0' : '1';
    $('decisionMetric').textContent = state.split('_')[0];
    const dashVals = [v.replayability, v.eci*20, Math.round((v.novelty + Math.max(0,v.advantage))/2), v.advantage > 0 ? Math.min(100, 50 + v.advantage) : 20, 100-v.risk, Math.min(100, r+5)];
    document.querySelectorAll('.dash-card i').forEach((bar, i) => bar.style.setProperty('--w', `${dashVals[i]}%`));
    if (!ran) $('heroLog').textContent = `01 · Objective: ${v.objective.slice(0,80)}${v.objective.length>80?'…':''}\n02 · ECI: E${v.eci}; novelty: ${(v.novelty/100).toFixed(2)}; advantage: ${v.advantage}%.\n03 · Decision: ${state}.`;
  }
  function append(line){
    const now = new Date().toTimeString().slice(0,8);
    $('traceLog').textContent += `\n${now} · ${line}`;
    $('traceLog').scrollTop = $('traceLog').scrollHeight;
  }
  function runCycle(){
    ran = true; clearInterval(tick); setStage(0); $('traceLog').textContent = '23:00:00 · RSI cycle started.';
    let i = 0; tick = setInterval(() => { setStage(i); append(`${stages[i][0]} complete: ${stages[i][1]}`); i += 1; if (i >= stages.length) { clearInterval(tick); update(); append(`Decision emitted: ${decision()[0]}.`); } }, 520);
  }
  function stress(){
    ran = true;
    $('novelty').value = 92; $('advantage').value = 34; $('persistence').value = 48; $('risk').value = 64; $('eci').value = 1;
    $('gate-dossier').checked = false; $('gate-omni').checked = false;
    update(); append('Stress injected: high novelty, low ECI, weak persistence, OMNI overreach.'); setStage(2);
  }
  function restart(){
    $('replayability').value = 98; $('eci').value = Math.max(2, +$('eci').value); $('gate-stateHash').checked = true; $('gate-drift').checked = true;
    update(); append('Restart from manifest: cycle index continuity and state hashes verified.'); setStage(0);
  }
  function packageDossier(){
    $('gate-dossier').checked = true; $('gate-omni').checked = true; $('gate-council').checked = true; $('eci').value = Math.max(3, +$('eci').value); $('persistence').value = Math.max(76, +$('persistence').value);
    update(); append('Dossier packaged: reproduction manifest, policy shocks, baseline report, ECI ledger, council memo.'); setStage(7);
  }
  function stateObject(){ const v=vals(); const [state, reason]=decision(); return {title:'GoalOS From Loop to RSI State-Capacity Command Room V3', generatedAt:new Date().toISOString(), publicAlphaBoundary:['no user data','no user funds','no wallet','no transaction','no network call','no production authority','human review required'], objective:v.objective, metrics:v, gates:Object.fromEntries(gates.map(g=>[g[0],gate(g[0])])), decisionState:state, decisionReason:reason, readiness:readiness(), pipeline:stages.map(s=>s[0])}; }
  function dossierObject(){ const v=vals(); return {dossierClass:v.novelty>=80?'Move-37 Dossier':'RSI Pilot Dossier', noveltyDistance:v.novelty/100, advantageDelta:v.advantage/100, requiredSteps:['recognize','reproduce','stress-test','persistence-gate','package','council-review'], baselines:['null','incumbent','nearest-neighbor','static workflow','single strongest agent','current GoalOS stack'], status:decision()[0]}; }
  function eciObject(){ const v=vals(); return {eciLevel:`E${v.eci}`, levels:['E0 SIMULATED','E1 PROBED','E2 EXECUTED','E3 REPLAYED','E4 STRESS-TESTED','E5 EXTERNALLY VALIDATED'], rule:'confidence cannot inflate without execution', executedEvidenceGate:gate('executed'), replayability:v.replayability}; }
  function councilObject(){ return {council:['Architect','Validator','Red Team','Dossier Lead','Human Authority'], stopAuthority:true, decision:decision()[0], notes:'Search control is allowed. Outcome authority is earned through gates.'}; }
  function pilotObject(){ return {phases:[{name:'Pilot 0-90 days',kpi:'>=95% cycles replayable',work:['deterministic runner','schema registry','baseline library','ECI ledger','drift sentinel']},{name:'Scale 3-12 months',kpi:'sustained AdvantageDelta vs incumbents',work:['archive coverage','bridge exploration','Move-37 dossier workflow','conservative budgets']},{name:'Strategic autonomy 12-24 months',kpi:'validated repeatable compounding discovery rate',work:['policy-shock suites','validator council','partner execution lanes','capacity allocation']}], boundary:'planning simulation only; no production authority'}; }
  function reviewerObject(){ return {reviewQuestions:['What real task was performed?','Which evidence was executed?','Which baselines were compared?','What changed under shocks?','What remains unproven?','Would you accept, reject, revise, or dissent?'], downloads:['RSI state','Move-37 dossier','ECI ledger','council memo','pilot plan'], decision:decision()[0]}; }
  function download(name, data){
    const blob = new Blob([JSON.stringify(data,null,2)], {type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `goalos-${name}.json`; document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url); append(`Downloaded ${name}.json.`);
  }
  setStage(0); update();
})();
