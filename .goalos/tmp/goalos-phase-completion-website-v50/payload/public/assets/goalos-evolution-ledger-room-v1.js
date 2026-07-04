(() => {
  const $ = (id) => document.getElementById(id);
  const gateDefs = [
    ['commit', 'GoalOSCommit', 'Aim object is signed, scoped, and claim-bounded.'],
    ['run', 'RunRoot', 'Execution root pins agents, tools, context, policy, budget, and risk.'],
    ['proof', 'ProofRoot', 'Proof root binds outputs, trace roots, cost, latency, and signatures.'],
    ['eval', 'EvalAttestation', 'Registered evaluators attest to baselines, results, and challenge window.'],
    ['selection', 'SelectionCertificate', 'Selection admits, rejects, canaries, promotes, pauses, or rolls back.'],
    ['rollback', 'RollbackReceipt', 'A valid rollback target and monitoring trigger exist before release.'],
    ['boundary', 'Public/private boundary', 'Private prompts, raw traces, customer data, and sensitive work stay private.'],
    ['challenge', 'Challenge window', 'The public proof root remains challengeable before evolution rights activate.'],
    ['quorum', 'Validator quorum', 'Independent review capacity is sufficient for the selected risk class.'],
    ['human', 'Human review', 'High-impact evolution remains review-ready, not production-authorized.']
  ];
  const state = { running:false, stressed:false, mode:'executive', toggles:{}, lastStep:0 };
  gateDefs.forEach(g => state.toggles[g[0]] = !['challenge','rollback','quorum'].includes(g[0]));
  function claim(){ return $('claimText').value.trim(); }
  function claimProfile(){
    const t = claim().toLowerCase();
    const words = t.split(/\s+/).filter(Boolean).length;
    const bounded = ['bounded','scope','scoped','public-safe','public safe','claim-bound','review','human','no user data','no funds','no wallet'].filter(x=>t.includes(x)).length;
    const replay = ['replay','replayable','deterministic','hash','root','evidence','docket','validator','attestation','baseline'].filter(x=>t.includes(x)).length;
    const over = ['all','always','guarantee','guaranteed','proves everything','solves','fully autonomous','agi','asi','sota','production'].filter(x=>t.includes(x)).length;
    const specificity = Math.min(1, (words/26) + bounded*.08 + replay*.06 - over*.09);
    return {words,bounded,replay,over,specificity:Math.max(0,Math.min(1,specificity))};
  }
  function passedGates(){
    const gates = {...state.toggles};
    const q = +$('quorum').value;
    if(q >= 5) gates.quorum = true;
    if(state.stressed){
      const p = claimProfile();
      if(p.over > 1 || p.specificity < .35){ gates.selection = false; gates.challenge = false; }
      if(p.bounded < 2){ gates.boundary = false; }
      if(p.replay < 2){ gates.proof = false; }
      if($('riskClass').value === 'HIGH'){ gates.human = true; gates.rollback = gates.rollback && q >= 5; }
    }
    return gates;
  }
  function compute(){
    const gates = passedGates();
    const passed = Object.values(gates).filter(Boolean).length;
    const p = claimProfile();
    let readiness = Math.round((passed/gateDefs.length)*100 + p.specificity*8 - (state.stressed?8:0));
    readiness = Math.max(0, Math.min(100, readiness));
    let decision = 'LEDGER_REVIEW_READY';
    if(!gates.boundary) decision = 'BLOCK_PRIVACY_BOUNDARY';
    else if(!gates.proof) decision = 'REJECT_NO_PROOF_ROOT';
    else if(!gates.eval) decision = 'REJECT_NO_EVAL_ATTESTATION';
    else if(!gates.rollback) decision = 'HOLD_ROLLBACK_REQUIRED';
    else if(!gates.quorum) decision = 'HOLD_VALIDATOR_QUORUM_REQUIRED';
    else if(!gates.challenge) decision = 'HOLD_CHALLENGE_WINDOW';
    else if(!gates.selection) decision = 'REVISE_SELECTION_CERTIFICATE';
    return {gates,passed,readiness,decision,profile:p};
  }
  function render(){
    const c = compute();
    $('readiness').textContent = c.readiness;
    $('gateCount').textContent = `${c.passed} / ${gateDefs.length}`;
    $('privateState').textContent = c.gates.boundary ? 'sealed' : 'leak risk';
    $('challengeState').textContent = c.gates.challenge ? 'cleared' : 'open';
    $('evolutionRight').textContent = c.decision === 'LEDGER_REVIEW_READY' ? 'review-ready' : 'blocked';
    $('decisionState').textContent = c.decision;
    const explanations = {
      LEDGER_REVIEW_READY:'All hard gates are clear. The public proof rail is review-ready, still human-review-bound and not production authority.',
      BLOCK_PRIVACY_BOUNDARY:'The ledger attempted to expose too much. Private intelligence, customer data, raw traces, and sensitive outputs must stay private.',
      REJECT_NO_PROOF_ROOT:'The public sequence lacks a valid proof root. A claim cannot advance without an attestable evidence commitment.',
      REJECT_NO_EVAL_ATTESTATION:'The evaluation layer is missing. Score cannot substitute for evaluator attestation.',
      HOLD_ROLLBACK_REQUIRED:'Rollback is not ready. No rollback, no release.',
      HOLD_VALIDATOR_QUORUM_REQUIRED:'Validator quorum is insufficient for the selected risk posture.',
      HOLD_CHALLENGE_WINDOW:'The challenge window remains open. Evolution rights are not final until challenge clears.',
      REVISE_SELECTION_CERTIFICATE:'The selection certificate does not yet survive the current claim, stress, and gate profile.'
    };
    $('decisionExplain').textContent = explanations[c.decision];
    const circumference = 477;
    $('gauge').style.strokeDashoffset = String(circumference * (1 - c.readiness/100));
    $('toggles').innerHTML = gateDefs.map(([k,n,d]) => `<button class="toggle ${state.toggles[k]?'on':''}" data-toggle="${k}" type="button"><span>${n}</span><div class="switch" aria-hidden="true"></div></button>`).join('');
    $('gateLedger').innerHTML = gateDefs.map(([k,n,d]) => `<div class="gate ${c.gates[k]?'ok':''}"><i>${c.gates[k]?'✓':'!'}</i><div><strong>${n}</strong><small>${d}</small></div></div>`).join('');
    document.querySelectorAll('[data-toggle]').forEach(btn => btn.onclick = () => { state.toggles[btn.dataset.toggle] = !state.toggles[btn.dataset.toggle]; render(); });
    document.querySelectorAll('.node').forEach((node, idx) => {
      node.classList.toggle('active', state.running && idx < Math.max(1,state.lastStep));
      node.classList.toggle('blocked', state.running && idx === Math.max(0,state.lastStep-1) && c.decision !== 'LEDGER_REVIEW_READY' && state.lastStep >= 5);
    });
    const detail = state.mode === 'technical' ? `\nclaimProfile=${JSON.stringify(c.profile)}\nquorum=${$('quorum').value}\nrisk=${$('riskClass').value}\nstress=${state.stressed}` : '';
    $('terminal').textContent = [
      'Ledger sequence: Commit → Execute → Prove → Evaluate → Select → Rollout → Rollback',
      `Scenario: ${$('scenario').selectedOptions[0].textContent}`,
      `Claim: ${claim()}`,
      `Gate result: ${c.passed}/${gateDefs.length}`,
      `Decision: ${c.decision}`,
      c.decision === 'LEDGER_REVIEW_READY' ? 'Result: public proof is challengeable and review-ready; private intelligence remains sealed.' : 'Result: evolution rights blocked until the highlighted hard gates pass.',
      detail
    ].join('\n');
  }
  function payload(kind){
    const c = compute();
    const common = {kind, generatedAt:new Date().toISOString(), page:'evolution-ledger-control-room.html', scenario:$('scenario').value, claim:claim(), decision:c.decision, readiness:c.readiness, gates:c.gates, noUserData:true, noUserFunds:true, noWallet:true, noTransaction:true, noNetworkCall:true, humanReviewRequired:true};
    if(kind === 'reviewBrief') return `# GoalOS Evolution Ledger Review Brief\n\nDecision: ${c.decision}\nReadiness: ${c.readiness}\n\nClaim under review:\n${claim()}\n\nReviewer route:\n1. Inspect public proof root.\n2. Confirm private intelligence boundary.\n3. Verify evaluator attestations.\n4. Confirm challenge window.\n5. Confirm rollback target.\n6. Accept, reject, revise, or dissent.\n`;
    return JSON.stringify({...common, ledgerObjects:['JobCommit','RunRoot','ProofRoot','EvalAttestation','SelectionCertificate','RolloutReceipt','RollbackReceipt']}, null, 2);
  }
  function download(kind){
    const data = payload(kind);
    const ext = kind === 'reviewBrief' ? 'md' : 'json';
    const blob = new Blob([data], {type: kind === 'reviewBrief' ? 'text/markdown' : 'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `goalos-${kind}.${ext}`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 500);
  }
  $('runBtn').onclick = () => { state.running = true; state.stressed = false; let i=0; const timer=setInterval(()=>{state.lastStep=++i; render(); if(i>=7) clearInterval(timer);}, 260); };
  $('stressBtn').onclick = () => { state.running = true; state.stressed = true; state.lastStep = 7; render(); };
  $('resetBtn').onclick = () => { state.running=false; state.stressed=false; state.lastStep=0; gateDefs.forEach(g => state.toggles[g[0]] = !['challenge','rollback','quorum'].includes(g[0])); render(); };
  $('executiveMode').onclick = () => { state.mode='executive'; $('executiveMode').classList.add('active'); $('technicalMode').classList.remove('active'); render(); };
  $('technicalMode').onclick = () => { state.mode='technical'; $('technicalMode').classList.add('active'); $('executiveMode').classList.remove('active'); render(); };
  ['scenario','riskClass','quorum','claimText'].forEach(id => $(id).addEventListener('input', render));
  document.querySelectorAll('[data-download]').forEach(b => b.onclick = () => download(b.dataset.download));
  render();
})();
