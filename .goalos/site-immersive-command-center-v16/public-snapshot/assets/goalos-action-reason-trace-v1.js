(function(){
  'use strict';
  const scenarios = {
    repo_patch:{name:'Repository patch proposal', intent:'Propose a public-safe documentation patch that improves the GoalOS proof ledger navigation without touching secrets, credentials, wallets, or production settings.', risk:'LOW', tool:'patch proposal'},
    reviewer_note:{name:'Reviewer response draft', intent:'Draft a reviewer response explaining which Evidence Docket gates passed, which remain pending, and what remediation is required before stronger claims can be made.', risk:'LOW', tool:'read-only repository'},
    browser_workflow:{name:'Browser workflow rehearsal', intent:'Rehearse a browser workflow for opening a public proof page, downloading the Evidence Docket, and checking the no-data/no-funds boundary.', risk:'MEDIUM', tool:'browser workflow'},
    database_write:{name:'Database write request', intent:'Request a database update for a public proof index only after validator review, replay path, rollback pointer, and human approval are present.', risk:'HIGH', tool:'database write'},
    wallet_attempt:{name:'Unsafe wallet action', intent:'Move user funds or request a wallet approval to settle a proof job without a replayed ProofBundle or human review.', risk:'CRITICAL', tool:'funds / wallet'}
  };
  const gateDefs = [
    ['objectiveScoped','Objective scoped','The action supports a bounded mission and explicit success/failure criteria.'],
    ['permissionGranted','Permission granted','Tool scope is least-privilege and allowed for the selected risk class.'],
    ['reasonRecorded','Reason recorded','The reason for action is stated before the action is attempted.'],
    ['expectedObservation','Expected observation','Expected observation is recorded before execution.'],
    ['actualObservation','Actual observation','Actual observation is recorded after execution or rehearsal.'],
    ['validatorStatus','Validator status','A validator, reviewer, test, or gate evaluates the action.'],
    ['costRiskLedger','Cost/risk ledger','Cost, latency, risk, and policy implications are visible.'],
    ['rollbackPointer','Rollback pointer','A rollback, undo, restore, or no-op safety path exists.'],
    ['evidencePointer','Evidence pointer','The action links to a docket, trace, evidence map, or review packet.'],
    ['boundaryPass','Public/private boundary','No private data, credentials, wallet approvals, funds, secrets, or production authority are involved.'],
    ['humanReview','Human review','High-impact action remains human-review-bound and non-production.']
  ];
  const state = {mode:'executive', stress:false, run:0, gates:{}};
  gateDefs.forEach(([k])=>state.gates[k]=true);
  state.gates.rollbackPointer = false;
  state.gates.validatorStatus = true;

  const $ = (id)=>document.getElementById(id);
  const scenarioSelect = $('scenarioSelect');
  Object.entries(scenarios).forEach(([key,s])=>{const o=document.createElement('option');o.value=key;o.textContent=s.name;scenarioSelect.appendChild(o);});

  function setScenario(key){const s=scenarios[key];$('actionIntent').value=s.intent;$('riskClass').value=s.risk;$('toolSurface').value=s.tool;state.stress=false;render();}
  scenarioSelect.addEventListener('change',()=>setScenario(scenarioSelect.value));
  $('riskClass').addEventListener('change',render);$('toolSurface').addEventListener('change',render);$('actionIntent').addEventListener('input',render);
  ['reversibility','validatorCoverage','evidenceCompleteness'].forEach(id=>$(id).addEventListener('input',render));
  $('runBtn').addEventListener('click',()=>{state.run++; state.stress=false; render(true);});
  $('stressBtn').addEventListener('click',()=>{state.run++; state.stress=true; render(true);});
  $('resetBtn').addEventListener('click',()=>{gateDefs.forEach(([k])=>state.gates[k]=true);state.gates.rollbackPointer=false;state.stress=false;state.run=0;setScenario('repo_patch');});
  $('execMode').addEventListener('click',()=>{state.mode='executive';render();});
  $('techMode').addEventListener('click',()=>{state.mode='technical';render();});
  document.querySelectorAll('[data-download]').forEach(b=>b.addEventListener('click',()=>download(b.dataset.download)));

  function claimFeatures(text){
    const t = text.toLowerCase(); const words = t.split(/\s+/).filter(Boolean); const len=words.length;
    const bounded = ['bounded','public-safe','no user data','no funds','review','human','replay','rollback','scope','docket','evidence','validator','non-production'].filter(x=>t.includes(x)).length;
    const risky = ['funds','wallet','private key','seed phrase','credential','production','database','payment','mainnet','customer','confidential','secret'].filter(x=>t.includes(x)).length;
    const overclaim = ['always','guarantee','fully autonomous','solves','unlimited','production-ready','no risk','surely'].filter(x=>t.includes(x)).length;
    const actiony = ['write','move','send','delete','deploy','merge','approve','settle','request','update','patch','draft','rehearse','download'].filter(x=>t.includes(x)).length;
    return {len,bounded,risky,overclaim,actiony,quality:Math.max(0,Math.min(1,(bounded*0.13+actiony*0.08+Math.min(len,40)/180)-(risky*0.16+overclaim*0.18)))};
  }
  function compute(){
    const text=$('actionIntent').value; const f=claimFeatures(text); const risk=$('riskClass').value; const tool=$('toolSurface').value;
    let rev=+$('reversibility').value, val=+$('validatorCoverage').value, ev=+$('evidenceCompleteness').value;
    if(state.stress){ rev-=18; val-=14; ev-=12; }
    const riskWeight={LOW:2,MEDIUM:12,HIGH:26,CRITICAL:48}[risk] || 12;
    const toolPenalty = tool.includes('wallet')?55:tool.includes('database')?30:tool.includes('browser')?16:tool.includes('patch')?8:3;
    const gatePass = Object.values(state.gates).filter(Boolean).length/gateDefs.length;
    const readiness = Math.max(0,Math.min(100, Math.round(20 + gatePass*42 + f.quality*26 + ev*.12 + val*.10 + rev*.08 - riskWeight - toolPenalty)));
    const traceIntegrity = Math.max(0,Math.min(1, (gatePass*.58)+(ev/100*.16)+(val/100*.14)+(rev/100*.12) - (toolPenalty/240) - (state.stress?.08:0)));
    let decision='ACTION_REVIEW_READY';
    if(!state.gates.boundaryPass || tool.includes('wallet')) decision='BLOCK_PRIVACY_OR_FUNDS_BOUNDARY';
    else if(!state.gates.permissionGranted) decision='REJECT_SCOPE_NOT_AUTHORIZED';
    else if(!state.gates.reasonRecorded) decision='REJECT_NO_REASON_RECORDED';
    else if(!state.gates.expectedObservation || !state.gates.actualObservation) decision='HOLD_OBSERVATION_REQUIRED';
    else if(!state.gates.validatorStatus || val<55) decision='HOLD_VALIDATOR_REQUIRED';
    else if(!state.gates.rollbackPointer || rev<55) decision='HOLD_ROLLBACK_REQUIRED';
    else if(!state.gates.evidencePointer || ev<60) decision='HOLD_EVIDENCE_POINTER_REQUIRED';
    else if(risk==='CRITICAL') decision='HOLD_HUMAN_AUTHORITY_REQUIRED';
    else if(state.stress && readiness<76) decision='HOLD_STRESS_REVIEW_REQUIRED';
    return {text,f,risk,tool,rev,val,ev,readiness,traceIntegrity,decision,gatePass,stress:state.stress,run:state.run};
  }
  function render(animated){
    const c=compute();
    $('revOut').textContent=$('reversibility').value; $('valOut').textContent=$('validatorCoverage').value; $('evOut').textContent=$('evidenceCompleteness').value;
    $('readiness').textContent=c.readiness; $('traceScore').textContent=c.traceIntegrity.toFixed(2); $('riskScore').textContent=c.risk; $('decisionState').textContent=c.decision;
    $('execMode').classList.toggle('selected',state.mode==='executive'); $('techMode').classList.toggle('selected',state.mode==='technical'); $('technicalPanel').classList.toggle('hidden',state.mode!=='technical');
    renderGates(c); renderLanes(c); renderSvg(c); renderTerminal(c); renderFormula(c);
  }
  function renderGates(c){
    const list=$('gateList'); list.innerHTML='';
    gateDefs.forEach(([k,label,desc])=>{
      const on=state.gates[k]; const div=document.createElement('div'); div.className='gate '+(on?'':'off');
      div.innerHTML='<div class="icon">'+(on?'✓':'!')+'</div><div><b>'+label+'</b><small>'+desc+'</small><div class="gate-toggle"><span>'+(on?'gate passing':'gate blocked')+'</span><button class="switch" aria-label="toggle '+label+'"></button></div></div>';
      div.querySelector('button').addEventListener('click',()=>{state.gates[k]=!state.gates[k];render();}); list.appendChild(div);
    });
  }
  function renderLanes(c){
    const lanes=[
      ['Reason', c.f.quality>.28?'ok':'warn', 'Intent is '+(c.f.quality>.28?'specific enough to review.':'too broad or risky; narrow the action and evidence path.')],
      ['Permission', c.tool.includes('wallet')?'bad':(c.risk==='HIGH'||c.risk==='CRITICAL')?'warn':'ok', 'Tool surface: '+c.tool+' · Risk class: '+c.risk],
      ['Observation', state.gates.expectedObservation&&state.gates.actualObservation?'ok':'bad', 'Expected and actual observations must be recorded before validation.'],
      ['Validation', state.gates.validatorStatus?'ok':'bad', 'Validator coverage '+c.val+'%; dissent and review remain visible.'],
      ['Rollback', state.gates.rollbackPointer?'ok':'bad', 'Reversibility '+c.rev+'%; release is blocked until rollback is credible.'],
      ['Evidence', state.gates.evidencePointer?'ok':'warn', 'Evidence completeness '+c.ev+'%; trace exports are downloadable.']
    ];
    $('traceLanes').innerHTML=lanes.map(l=>'<div class="lane '+l[1]+'"><b>'+l[0]+'</b><p>'+l[2]+'</p></div>').join('');
  }
  function renderSvg(c){
    const labels=['REASON','SCOPE','ACTION','OBSERVE','VALIDATE','ROLLBACK','CHRONICLE'];
    const pts=[[100,250],[190,157],[290,300],[380,250],[480,200],[580,300],[670,250]];
    const nodes=$('nodes'); nodes.innerHTML='';
    labels.forEach((lab,i)=>{ const status = (lab==='ROLLBACK'&&!state.gates.rollbackPointer)?'bad':(lab==='VALIDATE'&&!state.gates.validatorStatus)?'bad':(lab==='SCOPE'&&!state.gates.permissionGranted)?'bad':'ok'; const g=document.createElementNS('http://www.w3.org/2000/svg','g'); g.setAttribute('class','node '+(status==='bad'?'bad':'')); g.setAttribute('transform','translate('+pts[i][0]+','+pts[i][1]+')'); g.innerHTML='<circle r="38"></circle><text y="4">'+lab+'</text>'; nodes.appendChild(g); });
  }
  function renderTerminal(c){
    const lines=[]; lines.push('Action-Reason Trace Contract · run '+c.run); lines.push('Scenario: '+scenarios[scenarioSelect.value].name); lines.push('Decision: '+c.decision); lines.push('Readiness: '+c.readiness+'/100 · Trace integrity: '+c.traceIntegrity.toFixed(3)); lines.push('Claim sensitivity: bounded='+c.f.bounded+' risky='+c.f.risky+' overclaim='+c.f.overclaim+' action_terms='+c.f.actiony); lines.push(state.stress?'Stress: ACTIVE · adversarial pressure applied to reversibility, evidence, and validator coverage.':'Stress: inactive · normal review posture.'); lines.push(c.decision.includes('BLOCK')?'Resolution: action remains blocked.':'Resolution: action remains review-bound until human approval.'); $('terminal').textContent=lines.join('\n');
  }
  function renderFormula(c){
    $('contractFormula').textContent='TraceContract = (objective, permissionScope, reason, action, expectedObservation, actualObservation, validatorStatus, costRisk, rollbackPointer, evidencePointer, humanReview)\n\nAuthorize(action) iff scoped AND reasoned AND observed AND validated AND rollbackable AND evidence-linked AND boundary-pass.\n\nCurrent decision: '+c.decision;
  }
  function artifact(kind){
    const c=compute(); const base={kind, generatedAt:new Date().toISOString(), page:'action-reason-trace-contract.html', boundary:{noUserData:true,noUserFunds:true,noWallet:true,noTransaction:true,noNetworkCall:true,noProductionAuthority:true,humanReviewRequired:true}, decision:c.decision, readiness:c.readiness, riskClass:c.risk, toolSurface:c.tool, actionIntent:c.text, gates:state.gates, features:c.f};
    if(kind==='brief') return '# GoalOS Action-Reason Trace Review Brief\n\nDecision: '+c.decision+'\n\nReadiness: '+c.readiness+'/100\n\nAction intent:\n'+c.text+'\n\nBoundary: no user data, no funds, no wallet, no transaction, no network call, no production authority, human review required.\n';
    if(kind==='actionGraph') base.graph=['Reason','Scope','Action','Observe','Validate','Rollback','Chronicle'];
    if(kind==='rollback') base.rollback={required:true,reversibility:c.rev,playbook:['pause','restore previous state','record incident','publish rollback receipt','human review']};
    if(kind==='evidenceMap') base.evidence={expectedObservation:state.gates.expectedObservation,actualObservation:state.gates.actualObservation,evidencePointer:state.gates.evidencePointer,validatorStatus:state.gates.validatorStatus};
    return base;
  }
  function download(kind){
    const data=artifact(kind); const text= typeof data==='string'?data:JSON.stringify(data,null,2); const ext= kind==='brief'?'md':'json'; const blob=new Blob([text],{type:'text/plain;charset=utf-8'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='goalos-action-reason-trace-'+kind+'.'+ext; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},0);
  }
  setScenario('repo_patch');
})();
