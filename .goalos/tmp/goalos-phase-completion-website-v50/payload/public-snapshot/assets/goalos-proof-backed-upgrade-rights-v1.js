(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const qs = (sel) => [...document.querySelectorAll(sel)];

  const defaultState = {
    stage: 0,
    mode: 'executive',
    stress: false,
    gates: { proof: true, eval: true, baseline: true, scope: true, canary: true, rollback: true, challenge: false, privacy: true, human: true },
    metrics: { evidence: 84, value: 71, transfer: 63, cost: 31, risk: 42, overhead: 28, rollback: 34 }
  };

  let state = JSON.parse(JSON.stringify(defaultState));

  function val(id){ return Number($(id).value); }

  function gatesFromDom(){
    qs('[data-gate]').forEach(i => { state.gates[i.dataset.gate] = i.checked; });
  }

  function updateDomFromState(){
    $('evidence').value = state.metrics.evidence;
    $('value').value = state.metrics.value;
    $('transfer').value = state.metrics.transfer;
    $('rollback').value = state.metrics.rollback;
    $('evidenceOut').textContent = state.metrics.evidence;
    $('valueOut').textContent = state.metrics.value;
    $('transferOut').textContent = state.metrics.transfer;
    $('rollbackOut').textContent = state.metrics.rollback;
    qs('[data-gate]').forEach(i => { i.checked = state.gates[i.dataset.gate]; });
  }

  function proofGradient(){
    const m = state.metrics;
    let score = 0.26*m.evidence + 0.22*m.value + 0.18*m.transfer - 0.10*m.cost - 0.12*m.risk - 0.08*m.overhead - 0.12*m.rollback + 34;
    if(state.gates.challenge) score += 4;
    if(!state.gates.privacy) score -= 28;
    if(!state.gates.proof) score -= 24;
    if(!state.gates.rollback) score -= 18;
    if($('scope').value === 'network') score -= 8;
    if(state.stress) score -= 8;
    return Math.max(0, Math.min(100, Math.round(score)));
  }

  function decision(){
    const m = state.metrics, g = state.gates, score = proofGradient();
    if(!g.privacy) return ['BLOCK_PRIVACY_BOUNDARY','Public/private proof boundary failed. Private intelligence, customer data, prompts, or sensitive traces must never enter the public proof surface.'];
    if(!g.proof) return ['REJECT_NO_PROOF_HISTORY','No proof history exists. The artifact cannot earn reuse authority.'];
    if(!g.eval) return ['REJECT_NO_EVAL','The artifact lacks evaluator acceptance. Score cannot substitute for eval.'];
    if(!g.baseline) return ['REJECT_NO_BASELINE','The artifact has not beaten or matched required baselines under equal constraints.'];
    if(!g.human) return ['HOLD_HUMAN_REVIEW_REQUIRED','The upgrade remains blocked until a human-review path exists.'];
    if(!g.scope) return ['HOLD_SCOPE_NOT_AUTHORIZED','The requested scope is not authorized. Reduce the rollout or add governance approval.'];
    if(!g.rollback || m.rollback > 70) return ['HOLD_ROLLBACK_REQUIRED','Rollback readiness is insufficient. No rollback, no release.'];
    if(m.risk > 75) return ['PAUSE_RISK_ABOVE_THRESHOLD','Risk exceeds threshold. The artifact is paused for mitigation and reviewer escalation.'];
    if(!g.canary) return ['HOLD_CANARY_REQUIRED','Canary is not ready. The artifact may be reviewable but cannot influence future work yet.'];
    if(!g.challenge) return ['HOLD_CHALLENGE_WINDOW_OPEN','The challenge window remains open. External dissent or replay must be allowed.'];
    if(score >= 82) return ['UPGRADE_RIGHT_REVIEW_READY','The artifact earns a limited proof-backed upgrade right for the selected scope, pending final human approval.'];
    if(score >= 67) return ['HOLD_MORE_EVIDENCE_REQUIRED','The artifact is promising but needs stronger evidence, value, transfer, or lower proof debt.'];
    return ['REJECT_PROOF_GRADIENT_LOW','The Proof Gradient is too weak after cost, risk, overhead, and rollback debt.'];
  }

  function passedCount(){
    return Object.values(state.gates).filter(Boolean).length;
  }

  function render(){
    gatesFromDom();
    state.metrics.evidence = val('evidence');
    state.metrics.value = val('value');
    state.metrics.transfer = val('transfer');
    state.metrics.rollback = val('rollback');
    const score = proofGradient();
    const [d, txt] = decision();

    $('evidenceOut').textContent = state.metrics.evidence;
    $('valueOut').textContent = state.metrics.value;
    $('transferOut').textContent = state.metrics.transfer;
    $('rollbackOut').textContent = state.metrics.rollback;

    $('scoreLabel').textContent = score;
    $('ringProgress').style.strokeDashoffset = String(364 - 364 * score/100);
    $('decisionState').textContent = d;
    $('decisionText').textContent = txt;
    $('passedGates').textContent = passedCount() + '/9';
    $('scopeLabel').textContent = $('scope').value;
    $('riskLabel').textContent = state.metrics.risk;
    $('rollbackLabel').textContent = state.metrics.rollback;
    $('mQuality').textContent = state.metrics.evidence + '%';
    $('mValue').textContent = state.metrics.value + '%';
    $('mTransfer').textContent = state.metrics.transfer + '%';
    $('mCost').textContent = state.metrics.cost;
    $('mChallenge').textContent = state.gates.challenge ? 'cleared' : 'open';

    const title = {
      UPGRADE_RIGHT_REVIEW_READY: 'Limited proof-backed upgrade right is review-ready.',
      HOLD_CHALLENGE_WINDOW_OPEN: 'Challenge window remains open.',
      HOLD_CANARY_REQUIRED: 'Canary upgrade right is not yet cleared.',
      HOLD_ROLLBACK_REQUIRED: 'Rollback debt blocks promotion.',
      REJECT_NO_PROOF_HISTORY: 'No proof, no upgrade right.',
      REJECT_NO_EVAL: 'No eval, no propagation.',
      REJECT_NO_BASELINE: 'No baseline, no strong claim.',
      BLOCK_PRIVACY_BOUNDARY: 'Privacy boundary failure blocks public promotion.',
      HOLD_SCOPE_NOT_AUTHORIZED: 'Scope is not authorized.',
      PAUSE_RISK_ABOVE_THRESHOLD: 'Risk pause triggered.',
      HOLD_MORE_EVIDENCE_REQUIRED: 'More evidence required.',
      REJECT_PROOF_GRADIENT_LOW: 'Proof Gradient too low.'
    }[d] || 'Upgrade right held for review.';

    $('rightTitle').textContent = title;
    $('rightBody').textContent = txt;

    const gateLabels = {
      proof: 'Proof history',
      eval: 'Evaluator pass',
      baseline: 'Baseline comparison',
      scope: 'Scope authorization',
      canary: 'Canary readiness',
      rollback: 'Rollback readiness',
      challenge: 'Challenge window',
      privacy: 'Public/private boundary',
      human: 'Human review path'
    };

    $('gateList').innerHTML = Object.entries(gateLabels).map(([k,label]) => {
      const ok = state.gates[k];
      return `<li><span>${label}</span><b class="${ok?'pass':'fail'}">${ok?'PASS':'BLOCK'}</b></li>`;
    }).join('');

    qs('.stage').forEach((el, i) => el.classList.toggle('active', i <= state.stage));
    qs('.node').forEach((el, i) => {
      const gateKeys = ['proof','eval','baseline','scope','canary','rollback','challenge','privacy'];
      const k = gateKeys[i] || 'human';
      el.classList.toggle('pass', !!state.gates[k]);
      el.classList.toggle('fail', !state.gates[k]);
    });

    $('techBlock').classList.toggle('hidden', state.mode !== 'technical');
  }

  function runReview(){
    state.stage = 0;
    const interval = setInterval(() => {
      state.stage += 1;
      if(state.stage >= 7) clearInterval(interval);
      render();
    }, 260);
    render();
  }

  function stressRollout(){
    state.stress = true;
    state.metrics.risk = Math.min(100, state.metrics.risk + 18);
    state.metrics.overhead = Math.min(100, state.metrics.overhead + 20);
    state.metrics.rollback = Math.min(100, state.metrics.rollback + 24);
    if($('scope').value === 'network') state.gates.scope = false;
    state.gates.challenge = false;
    state.stage = 4;
    updateDomFromState();
    render();
  }

  function reset(){
    state = JSON.parse(JSON.stringify(defaultState));
    $('artifactText').value = 'Repository Launch Readiness Pack: a reusable capability package for turning GoalOS public-alpha architecture into a review-ready Evidence Docket and Proof Run 001 path.';
    $('artifactClass').value = 'capability';
    $('scope').value = 'canary';
    updateDomFromState();
    render();
  }

  function artifact(kind){
    const [d, txt] = decision();
    const now = new Date().toISOString();
    const base = {
      id: 'goalos-upgrade-right-' + now.replace(/[^0-9]/g,'').slice(0,14),
      kind,
      generated_at: now,
      browser_local: true,
      no_user_data: true,
      no_user_funds: true,
      no_wallet: true,
      no_transaction: true,
      no_network_call: true,
      human_review_required: true,
      candidate: $('artifactText').value,
      artifact_class: $('artifactClass').value,
      requested_scope: $('scope').value,
      proof_gradient_score: proofGradient(),
      decision_state: d,
      decision_rationale: txt,
      gates: state.gates,
      metrics: state.metrics
    };
    if(kind === 'selection_certificate') base.selection = {status: d, allowed_scope: d === 'UPGRADE_RIGHT_REVIEW_READY' ? $('scope').value : 'none', canary_required: true, challenge_window_required: true};
    if(kind === 'rollback_receipt') base.rollback = {rollback_target: 'last accepted artifact version', rollback_debt: state.metrics.rollback, rollback_required_before_release: true};
    if(kind === 'reviewer_brief') base.review = {questions: ['What evidence supports the candidate?', 'Which baselines were compared?', 'Is the scope authorized?', 'Can it be rolled back?', 'What dissent remains?']};
    return base;
  }

  function downloadJSON(filename, obj){
    const blob = new Blob([JSON.stringify(obj, null, 2)], {type:'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function downloadMarkdown(filename, obj){
    const md = `# GoalOS Proof-Backed Upgrade Rights Review\n\n**Decision:** ${obj.decision_state}\n\n**Candidate:** ${obj.candidate}\n\n**Score:** ${obj.proof_gradient_score}\n\n**Rationale:** ${obj.decision_rationale}\n\n## Boundary\n\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n`;
    const blob = new Blob([md], {type:'text/markdown'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  $('runReview').addEventListener('click', runReview);
  $('stressRollout').addEventListener('click', stressRollout);
  $('resetRoom').addEventListener('click', reset);
  $('execMode').addEventListener('click', () => { state.mode='executive'; $('execMode').classList.add('active'); $('techMode').classList.remove('active'); render(); });
  $('techMode').addEventListener('click', () => { state.mode='technical'; $('techMode').classList.add('active'); $('execMode').classList.remove('active'); render(); });
  $('downloadRight').addEventListener('click', () => downloadJSON('goalos-proof-backed-upgrade-right.json', artifact('upgrade_right')));
  $('downloadCert').addEventListener('click', () => downloadJSON('goalos-selection-certificate.json', artifact('selection_certificate')));
  $('downloadRollback').addEventListener('click', () => downloadJSON('goalos-rollback-receipt.json', artifact('rollback_receipt')));
  $('downloadBrief').addEventListener('click', () => downloadMarkdown('goalos-upgrade-right-reviewer-brief.md', artifact('reviewer_brief')));

  ['evidence','value','transfer','rollback','artifactClass','scope'].forEach(id => $(id).addEventListener('input', render));
  qs('[data-gate]').forEach(i => i.addEventListener('change', render));
  updateDomFromState();
  render();
})();