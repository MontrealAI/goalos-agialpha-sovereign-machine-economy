(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const gates = [
    ['syntaxValid','Syntax valid', true],
    ['sandboxSafe','Sandbox safe', true],
    ['validatorBound','Validator-bound', true],
    ['replayable','Replayable', true],
    ['interesting','Interesting', true],
    ['learnable','Learnable', true],
    ['nonRedundant','Non-redundant', true],
    ['riskBounded','Risk-bounded', true],
    ['improvesWork','Improves future work', true],
    ['boundaryPass','Public/private boundary', true],
    ['humanReview','Human review', true]
  ];
  const scenarioData = {
    mission:{label:'Mission Foundry', artifact:'mission_variant', desc:'Generate public-safe proof missions with claims, baselines, and replay paths.'},
    validator:{label:'Validator Lattice', artifact:'validator_challenge', desc:'Generate evaluator challenges that make weak claims fail visibly.'},
    workflow:{label:'Agent Design Forge', artifact:'workflow_candidate', desc:'Generate role graphs and tool contracts before bounded execution.'},
    capability:{label:'Capability Package Foundry', artifact:'capability_candidate', desc:'Generate reusable capability packages only after proof history exists.'},
    curriculum:{label:'Curriculum Engine', artifact:'task_family', desc:'Generate learnable, interesting, replayable task variants for future proof missions.'}
  };
  const state = {ran:false,stress:false,mode:'exec',phase:0};

  function gateContainer(){
    const box = $('gateToggles');
    box.innerHTML = '';
    gates.forEach(([id,label,on]) => {
      const row = document.createElement('label');
      row.className = 'switch';
      row.innerHTML = `<span>${label}</span><input id="gate_${id}" type="checkbox" ${on?'checked':''} aria-label="${label}">`;
      box.appendChild(row);
      row.querySelector('input').addEventListener('change', render);
    });
  }
  function getGate(id){ const el = $('gate_'+id); return !!(el && el.checked); }
  function gateMap(){ return Object.fromEntries(gates.map(([id]) => [id, getGate(id)])); }
  function textMetrics(text){
    const words = (text.toLowerCase().match(/[a-z0-9]+/g)||[]);
    const has = (arr) => arr.some(w => words.includes(w) || text.toLowerCase().includes(w));
    const specificity = Math.min(1, words.length/42 + (has(['specific','bounded','public-safe','replay','validator','evidence','baseline','risk','claim']) ? .24 : 0));
    const replay = has(['replay','replayable','reproduce','audit','docket','evidence','proof']) ? .85 : .42;
    const boundary = has(['no data','public-safe','no funds','claim-bound','human review','private','boundary']) ? .88 : .46;
    const overclaim = has(['solves','guarantee','autonomous','agi','asi','superintelligence','always','fully','production']) ? .32 : .08;
    return {specificity, replay, boundary, overclaim, wordCount: words.length};
  }
  function compute(){
    const g = gateMap();
    const text = $('seedText').value || '';
    const m = textMetrics(text);
    const novelty = +$('novelty').value/100;
    const learn = +$('learnability').value/100;
    const risk = +$('risk').value/100;
    const gateScore = Object.values(g).filter(Boolean).length / Object.values(g).length;
    let score = 30 + 34*gateScore + 10*m.specificity + 8*m.replay + 8*m.boundary + 7*learn + 5*novelty - 19*risk - 18*m.overclaim;
    let generated = 8 + Math.round(novelty*10);
    let admitted = Math.max(0, Math.round(generated * (score/100) * .42));
    let quarantined = Math.max(0, Math.round(generated * (risk + m.overclaim + (state.stress? .2:0)) * .34));
    if(state.stress){
      score -= 10 + 13*risk + 8*m.overclaim;
      admitted = Math.max(0, admitted - 1 - Math.round(m.overclaim*3));
      quarantined = Math.min(generated, quarantined + 2);
    }
    score = Math.max(0, Math.min(100, Math.round(score)));
    let decision = 'ENGINE_REVIEW_READY';
    let explanation = 'Generated descendants are review-ready candidates only; no production authority exists.';
    if(!g.boundaryPass){ decision = 'BLOCK_PRIVACY_BOUNDARY'; explanation = 'Generated work is blocked because the public/private boundary failed.'; }
    else if(!g.syntaxValid || !g.sandboxSafe){ decision = 'REJECT_UNSAFE_GENERATION'; explanation = 'Generated objects must be schema-valid and sandbox-safe before review.'; }
    else if(!g.validatorBound){ decision = 'HOLD_VALIDATOR_BOUND_REQUIRED'; explanation = 'Generated tasks cannot enter the curriculum without validator anchoring.'; }
    else if(!g.replayable){ decision = 'REJECT_UNREPLAYABLE'; explanation = 'Generated descendants without replay paths cannot compound.'; }
    else if(!g.learnable){ decision = 'REJECT_NON_LEARNABLE'; explanation = 'The proposed generation is outside the learnable band.'; }
    else if(!g.interesting){ decision = 'REJECT_NON_INTERESTING'; explanation = 'The proposed generation lacks mission-relevant novelty.'; }
    else if(!g.improvesWork){ decision = 'HOLD_IMPROVES_WORK_REQUIRED'; explanation = 'Candidates must show how they improve future verified work.'; }
    else if(state.stress && score < 54){ decision = 'QUARANTINE_UNTETHERED'; explanation = 'Stress mode detected untethered generation: quarantine until external proof improves.'; }
    else if(!g.humanReview){ decision = 'HOLD_HUMAN_REVIEW_REQUIRED'; explanation = 'Human review remains mandatory for public-alpha generated work.'; }
    else if(score > 82 && admitted > 2){ decision = 'ADMIT_CANDIDATE_CANARY'; explanation = 'Candidates may become canary review artifacts, not production authority.'; }
    return {g, m, novelty, learn, risk, score, generated, admitted, quarantined, decision, explanation};
  }
  function drawSvg(){
    const labels = ['Mission','Env','Agent','Validator','Proof','Archive','Select','Next'];
    const coords = [[260,28],[394,70],[462,178],[395,292],[260,332],[126,292],[58,178],[126,70]];
    const group = $('svgNodes');
    group.innerHTML = '';
    coords.forEach((c,i) => {
      if(i>0){
        const p = coords[i-1];
        group.insertAdjacentHTML('beforeend', `<line class="edge ${state.ran && i<=state.phase?'hot':''}" x1="${p[0]}" y1="${p[1]}" x2="${c[0]}" y2="${c[1]}"></line>`);
      }
    });
    coords.forEach((c,i) => {
      group.insertAdjacentHTML('beforeend', `<g class="node ${state.ran && i<=state.phase?'active':''}"><circle cx="${c[0]}" cy="${c[1]}" r="27"></circle><text x="${c[0]}" y="${c[1]+4}" text-anchor="middle">${labels[i]}</text></g>`);
    });
  }
  function candidates(c){
    const scenario = scenarioData[$('scenario').value];
    const baseNames = ['Variant Alpha','Validator Echo','Workflow Delta','Proof Template Orion','Capability Nova','Curriculum Helix','Red-Team Quasar','Replay Atlas','Sandbox Lumen'];
    const arr = [];
    for(let i=0;i<6;i++){
      let status = i < c.admitted ? 'admit' : i < c.admitted + c.quarantined ? 'quarantine' : 'reject';
      const reason = status==='admit'?'admitted for review':status==='quarantine'?'quarantined for replay':'rejected by gate';
      arr.push({name:baseNames[i], status, reason, kind:scenario.artifact});
    }
    return arr;
  }
  function render(){
    const c = compute();
    $('noveltyOut').textContent = c.novelty.toFixed(2);
    $('learnOut').textContent = c.learn.toFixed(2);
    $('riskOut').textContent = c.risk.toFixed(2);
    $('readiness').textContent = c.score;
    $('score').textContent = c.score;
    $('generated').textContent = c.generated;
    $('admitted').textContent = c.admitted;
    $('quarantined').textContent = c.quarantined;
    $('decision').textContent = c.decision;
    $('stateTitle').textContent = c.decision;
    $('stateText').textContent = c.explanation;
    $('scoreArc').style.strokeDashoffset = String(339 - (339*c.score/100));
    document.querySelectorAll('.pipeline div').forEach((el,i)=>el.classList.toggle('active', state.ran && i <= Math.min(5,state.phase)));
    $('candidateGrid').innerHTML = candidates(c).map(x => `<article class="candidate ${x.status}"><strong>${x.name}</strong><em>${x.kind}</em><span class="pill">${x.reason}</span></article>`).join('');
    const scenario = scenarioData[$('scenario').value];
    const modeLine = state.mode === 'tech' ? `Admissibility = ${c.score}; specificity=${c.m.specificity.toFixed(2)} replay=${c.m.replay.toFixed(2)} boundary=${c.m.boundary.toFixed(2)} overclaim=${c.m.overclaim.toFixed(2)}` : `Generated ${c.generated} candidates; ${c.admitted} admitted for review; ${c.quarantined} quarantined.`;
    $('chronicle').textContent = [
      `GoalOS Open-Ended Work Engine`,
      `Scenario: ${scenario.label}`,
      `Seed: ${($('seedText').value||'').slice(0,108)}${($('seedText').value||'').length>108?'...':''}`,
      `Stress: ${state.stress ? 'ACTIVE — untethering pressure applied' : 'inactive'}`,
      modeLine,
      `Decision: ${c.decision}`,
      `Boundary: no data, no funds, no wallet, no transaction, no network call.`
    ].join('\n');
    $('technicalBlock').style.display = state.mode === 'tech' ? 'grid' : 'none';
    drawSvg();
  }
  function run(){
    state.ran = true;
    state.phase = 0;
    const timer = setInterval(() => {
      state.phase++;
      render();
      if(state.phase >= 7) clearInterval(timer);
    }, 170);
  }
  function payload(type){
    const c = compute();
    const scenario = scenarioData[$('scenario').value];
    const common = {
      product:'GoalOS AGIALPHA Ascension — Sovereign Machine Economy',
      demo:'Open-Ended Work Engine Lab V1',
      generatedAt:new Date().toISOString(),
      browserLocal:true,
      noNetworkCall:true,
      noUserData:true,
      noUserFunds:true,
      noWallet:true,
      noTransaction:true,
      humanReviewRequired:true,
      scenario:$('scenario').value,
      seedObjective:$('seedText').value,
      decisionState:c.decision,
      admissibilityScore:c.score,
      gates:c.g,
      claimSensitivity:c.m
    };
    if(type === 'reviewBrief'){
      return `# GoalOS Open-Ended Work Engine Review Brief\n\nDecision: ${c.decision}\n\nScore: ${c.score}\n\nScenario: ${scenario.label}\n\nSeed objective:\n${$('seedText').value}\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.\n`;
    }
    if(type === 'missionSet') return {...common, generatedMissionSet:candidates(c)};
    if(type === 'validatorLattice') return {...common, validators:['syntax','sandbox','replay','baseline','risk','privacy','human review'], quorum:'simulated public-alpha quorum'};
    if(type === 'proofTemplates') return {...common, templates:['claims matrix','environment manifest','baseline ladder','proof packet','cost/risk ledger','replay checklist','selection certificate']};
    return {...common, evidenceDocket:{claims:['Generated descendants remain candidates until proof gates pass.'], notClaims:['No live model call.','No production authority.','No external action.'], descendants:candidates(c)}};
  }
  function download(type){
    const p = payload(type);
    const isText = typeof p === 'string';
    const blob = new Blob([isText?p:JSON.stringify(p,null,2)], {type:isText?'text/markdown':'application/json'});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `goalos-open-ended-work-engine-${type}.${isText?'md':'json'}`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(()=>URL.revokeObjectURL(a.href), 1000);
  }
  function bind(){
    gateContainer();
    ['scenario','seedText','novelty','learnability','risk'].forEach(id => $(id).addEventListener('input', render));
    $('runEngine').addEventListener('click', run);
    $('stressUntethering').addEventListener('click', () => {state.stress = !state.stress; state.ran = true; state.phase = 7; render();});
    $('resetEngine').addEventListener('click', () => {state.stress=false; state.ran=false; state.phase=0; gateContainer(); render();});
    $('modeExec').addEventListener('click', () => {state.mode='exec'; $('modeExec').classList.add('active'); $('modeTech').classList.remove('active'); render();});
    $('modeTech').addEventListener('click', () => {state.mode='tech'; $('modeTech').classList.add('active'); $('modeExec').classList.remove('active'); render();});
    document.querySelectorAll('[data-download]').forEach(btn => btn.addEventListener('click', () => download(btn.dataset.download)));
    render();
  }
  document.addEventListener('DOMContentLoaded', bind);
})();
