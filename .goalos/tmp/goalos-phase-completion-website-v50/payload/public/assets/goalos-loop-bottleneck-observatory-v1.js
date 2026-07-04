(function(){
  'use strict';
  const $ = (id)=>document.getElementById(id);
  const scenarios = [
    {id:'repo-release', name:'Repository release hardening loop', objective:'Run a restartable loop that turns the current public-alpha repository into a release-hardened proof surface: route health, docs QA, claim scan, public downloads, issue-template boundary, and proof-run refresh.'},
    {id:'demo-polish', name:'Public demo polish loop', objective:'Improve a browser-local public demo until it is legible, useful, accessible, bounded, and review-ready without adding user data, wallet flows, or network calls.'},
    {id:'proof-mission', name:'Proof mission loop', objective:'Convert a high-stakes objective into a Mission Contract, Evidence Docket plan, validator path, replay pack, and governed decision state.'},
    {id:'validator-loop', name:'Validator council loop', objective:'Run a validator council loop that separates planner, generator, evaluator, dissenter, and reviewer roles while preserving replay, challenge windows, and claim boundaries.'}
  ];
  const stages = [
    ['CON','Contract','success / failure criteria'], ['ROL','Roles','planner / generator / evaluator'], ['DSK','Disk','contract.md / state.json / trace.md'], ['RUN','Run','bounded work cycle'], ['TRC','Trace','read logs before vibe'], ['RST','Restart','state survives crash'], ['RUB','Rubric','taste becomes gradable'], ['BOT','Bottleneck','next fix becomes visible']
  ];
  const gates = [
    ['contractGate','Contract before code',true], ['rolesGate','Separate roles',true], ['diskGate','Write state to disk',true], ['traceGate','Trace reading',true], ['restartGate','Restartable loop',true], ['evaluatorGate','Independent evaluator',true], ['rubricGate','Taste rubric',true], ['harnessGate','Harness deletion plan',true], ['boundaryGate','Public/private proof boundary',true], ['humanGate','Human review required',true]
  ];
  const rules = [
    ['Write the loop','The prompt is not the unit of leverage. GoalOS turns the procedure into an inspectable loop contract.'],
    ['Separate the roles','Planner, generator, evaluator, dissenter, and reviewer remain distinct so the loop cannot quietly grade itself.'],
    ['Negotiate the contract','The contract defines what gets graded before work starts: assertions, evidence, success, failure, replay, and rollback.'],
    ['Write to disk','State lives in files: contract, state, trace, progress, decision, and bottleneck report. Hidden context is not authority.'],
    ['Let the loop restart','A good loop can crash, restart, and continue from disk without losing the mission boundary.'],
    ['Score the subjective','Taste becomes gradable through a written rubric: design, originality, craft, function, and proof usefulness.'],
    ['Read the traces','Debugging begins by reading what the loop actually did, not by guessing from the final output.'],
    ['Delete the harness','As models improve, the harness must shrink. GoalOS detects overhead that no longer buys proof.'],
    ['Expose the bottleneck','When coding stops being the bottleneck, planning, verification, taste, or governance becomes the work.']
  ];
  const links = [
    ['Proof Run 001','proof-run-001-docket.html','repository-readiness docket'], ['Loop Contract','loop-contract-lab.html','contract layer'], ['Flight Recorder','loop-flight-recorder.html','trace/restart layer'], ['Registry','demo-ecosystem-registry.html','route matrix'], ['Trust Boundary','trust-boundary.html','no data / no funds']
  ];
  const state = {cycle:0, stress:false, active:0, lastAction:'draft'};
  function init(){
    $('scenario').innerHTML = scenarios.map(s=>`<option value="${s.id}">${s.name}</option>`).join('');
    $('objective').value = scenarios[0].objective;
    $('scenario').addEventListener('change',()=>{ $('objective').value = scenarios.find(s=>s.id===$('scenario').value).objective; compute('scenario loaded'); });
    ['contract','state','trace','evaluator','taste','harness'].forEach(id=>$(id).addEventListener('input',()=>compute('slider changed')));
    renderGates(); renderStages(); renderRules(); renderPalette(); compute('loaded default loop');
    $('runLoop').addEventListener('click',()=>{state.stress=false; state.cycle++; animateLoop('run loop');});
    $('stressLoop').addEventListener('click',()=>{state.stress=true; $('contract').value=Math.min(100, Number($('contract').value)-18); $('trace').value=Math.max(0, Number($('trace').value)-10); $('harness').value=Math.min(100, Number($('harness').value)+22); state.cycle++; animateLoop('stress weak loop');});
    $('restartLoop').addEventListener('click',()=>{state.cycle++; $('restartGate').checked=true; animateLoop('restart from disk');});
    $('deleteHarness').addEventListener('click',()=>{ $('harness').value=Math.max(0, Number($('harness').value)-24); $('harnessGate').checked=true; state.cycle++; animateLoop('delete harness overhead');});
    ['downloadReport','downloadContract','downloadTrace','downloadReplay','downloadBrief'].forEach(id=>$(id).addEventListener('click',()=>download(id)));
    $('paletteButton').addEventListener('click',()=>openPalette()); document.addEventListener('keydown',e=>{ if(e.key==='/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();openPalette();} });
    $('paletteSearch').addEventListener('input',renderPalette);
  }
  function renderGates(){
    $('gateStack').innerHTML = gates.map(([id,label,on])=>`<div class="gate"><label for="${id}">${label}</label><input class="toggle" id="${id}" type="checkbox" ${on?'checked':''}/></div>`).join('');
    gates.forEach(([id])=>$(id).addEventListener('change',()=>compute('gate changed')));
  }
  function renderStages(){
    $('loopTrack').innerHTML = stages.map((s,i)=>`<div class="stage" id="stage${i}"><b>${s[0]} · ${s[1]}</b><small>${s[2]}</small></div>`).join('');
    const pts = [[320,52],[466,92],[512,210],[466,328],[320,368],[174,328],[128,210],[174,92]];
    $('orbitNodes').innerHTML = stages.map((s,i)=>`<g><circle class="node" cx="${pts[i][0]}" cy="${pts[i][1]}" r="30"/><text class="node-text" x="${pts[i][0]}" y="${pts[i][1]+7}" text-anchor="middle">${s[0]}</text></g>`).join('');
  }
  function renderRules(){
    $('ruleGrid').innerHTML = rules.map(r=>`<article class="rule"><b>${r[0]}</b><p>${r[1]}</p></article>`).join('');
  }
  function values(){
    const v = {contract:+$('contract').value, state:+$('state').value, trace:+$('trace').value, evaluator:+$('evaluator').value, taste:+$('taste').value, harness:+$('harness').value};
    gates.forEach(([id])=>v[id]=$(id).checked); v.objective=$('objective').value.trim(); v.risk=$('risk').value; v.horizon=$('horizon').value; v.scenario=$('scenario').value; return v;
  }
  function findBottleneck(v){
    const candidates = [
      ['Contract before code', 100-v.contract, 'Negotiate objective, success, failure, acceptance tests, replay, rollback, and claim boundary before generation.'],
      ['State compression', 100-v.state, 'If the loop state cannot fit in a small file pack, the loop is too complicated to restart safely.'],
      ['Trace readability', 100-v.trace, 'The loop must explain itself through readable traces, not hidden context or persuasive summaries.'],
      ['Evaluator independence', 100-v.evaluator, 'The generator cannot be the only judge. A separate evaluator must challenge the result.'],
      ['Taste rubric', 100-v.taste, 'Subjective quality must be scored through written axes before the loop can improve deliberately.'],
      ['Harness overhead', v.harness, 'Delete scaffolding that no longer buys proof. If overhead dominates, the harness is the bottleneck.']
    ];
    if(!v.contractGate) candidates.push(['Missing contract gate', 120, 'No contract, no reliable loop.']);
    if(!v.diskGate) candidates.push(['Missing disk-state gate', 118, 'No disk state, no restartable loop.']);
    if(!v.evaluatorGate) candidates.push(['Self-graded loop', 125, 'No independent evaluator, no trusted promotion.']);
    if(!v.boundaryGate) candidates.push(['Public/private boundary', 140, 'The loop is blocked until public proof and private intelligence are separated.']);
    candidates.sort((a,b)=>b[1]-a[1]); return candidates[0];
  }
  function compute(action){
    const v=values(); ['contract','state','trace','evaluator','taste','harness'].forEach(id=>$('v'+id[0].toUpperCase()+id.slice(1)).textContent=v[id]);
    const hardPenalty = gates.reduce((p,[id])=>p+(v[id]?0:18),0);
    const quality = Math.round((v.contract+v.state+v.trace+v.evaluator+v.taste+(100-v.harness))/6);
    let readiness = Math.max(0, Math.min(100, quality - hardPenalty - (state.stress?7:0) + Math.min(8,state.cycle)));
    const bn=findBottleneck(v);
    let decision='LOOP_REVIEW_READY'; let copy='The loop has enough contract, disk state, trace readability, evaluator independence, taste rubric, and proof boundary to prepare a reviewer docket.';
    if(!v.boundaryGate) {decision='BLOCK_PRIVACY_BOUNDARY'; copy='The loop cannot promote while public proof/private intelligence separation is disabled.';}
    else if(!v.contractGate || v.contract < 45) {decision='REJECT_NO_CONTRACT'; copy='The loop is rejected until the contract is explicit enough to grade.';}
    else if(!v.rolesGate) {decision='HOLD_ROLE_SEPARATION_REQUIRED'; copy='Planner, generator, evaluator, and reviewer roles must be separated.';}
    else if(!v.diskGate || v.state < 45) {decision='HOLD_STATE_FILES_REQUIRED'; copy='The loop must write contract, progress, trace, and decision state to disk.';}
    else if(!v.evaluatorGate || v.evaluator < 45) {decision='REJECT_SELF_GRADED_LOOP'; copy='A loop that grades itself cannot earn institutional trust.';}
    else if(!v.traceGate || v.trace < 45) {decision='HOLD_TRACE_READING_REQUIRED'; copy='The trace is not readable enough to debug or review.';}
    else if(!v.restartGate) {decision='HOLD_RESTART_REQUIRED'; copy='A long-running loop must be able to restart from disk.';}
    else if(!v.rubricGate || v.taste < 42) {decision='HOLD_TASTE_RUBRIC_REQUIRED'; copy='Subjective quality must be made gradable before improvement can be trusted.';}
    else if(v.harness > 82) {decision='HOLD_HARNESS_OVERHEAD_DOMINATES'; copy='The harness costs more than it buys. Delete or simplify scaffolding before promotion.';}
    else if(state.stress && readiness < 68) {decision='HOLD_BOTTLENECK_REVIEW_REQUIRED'; copy='Stress mode exposed a moving bottleneck. The loop should revise and rerun before review.';}
    const bidx = Math.max(0, stages.findIndex(s=>bn[0].toLowerCase().includes(s[1].toLowerCase().split(' ')[0])));
    state.active = bidx === -1 ? 0 : bidx;
    updateUI(v, readiness, bn, decision, copy, action);
    return {values:v, readiness, bottleneck:bn[0], decision, copy};
  }
  function updateUI(v, readiness, bn, decision, copy, action){
    $('readinessStat').textContent=readiness; $('scoreRing').textContent=readiness; $('scoreRing').parentElement.style.setProperty('--score', readiness); $('bottleneckStat').textContent=bn[0].split(' ')[0].toLowerCase(); $('loopsStat').textContent=state.cycle; $('decisionState').textContent=decision; $('decisionTop').textContent=decision; $('decisionCopy').textContent=copy; $('bottleneckName').textContent=bn[0]; $('bottleneckAdvice').textContent=bn[2]; $('bottleneckFill').style.height=Math.max(18,Math.min(100,bn[1]))+'%';
    stages.forEach((_,i)=>{const el=$('stage'+i); el.classList.toggle('active',i===state.active); el.classList.toggle('blocked',decision.includes('REJECT')||decision.includes('BLOCK'));});
    const point = [[320,52],[466,92],[512,210],[466,328],[320,368],[174,328],[128,210],[174,92]][state.active] || [320,52];
    $('bottleneckBeam').innerHTML = `<path d="M320 210L${point[0]} ${point[1]}" class="beam"/><circle cx="${point[0]}" cy="${point[1]}" r="28" class="hot-node"/><text x="${point[0]}" y="${point[1]+7}" class="node-text" text-anchor="middle">${stages[state.active]?.[0]||'BOT'}</text>`;
    $('stateFiles').innerHTML = ['contract.md','state.json','trace.md','progress.md','decision-state.json','bottleneck-report.json'].map((f,i)=>`<li>${f}<br><small>${i < 2 ? 'required for restart' : i < 4 ? 'required for review' : 'required for docket'}</small></li>`).join('');
    const verdicts = [
      ['Contract', v.contractGate && v.contract>=45], ['Disk state', v.diskGate && v.state>=45], ['Trace', v.traceGate && v.trace>=45], ['Evaluator', v.evaluatorGate && v.evaluator>=45], ['Taste rubric', v.rubricGate && v.taste>=42], ['Harness', v.harnessGate && v.harness<=82], ['Boundary', v.boundaryGate], ['Human review', v.humanGate]
    ];
    $('verdictList').innerHTML=verdicts.map(([k,ok])=>`<div class="verdict"><span>${k}</span><b>${ok?'PASS':'HOLD'}</b></div>`).join('');
    const lines = [
      `00 · ${new Date().toISOString().replace(/\.\d+Z$/,'Z')} · ${action}`,
      `01 · objective hash: ${hash(v.objective).slice(0,12)}`,
      `02 · contract=${v.contract} state=${v.state} trace=${v.trace} evaluator=${v.evaluator}`,
      `03 · bottleneck exposed: ${bn[0]}`,
      `04 · decision: ${decision}`,
      `05 · boundary: no data, no funds, no wallet, no transaction`,
      `06 · next loop must fix: ${bn[0]}`
    ];
    $('terminal').innerHTML = lines.map(x=>`<div>${escape(x)}</div>`).join('');
  }
  function animateLoop(action){
    let i=0; const timer=setInterval(()=>{state.active=i; stages.forEach((_,j)=>$('stage'+j).classList.toggle('active',j===i)); i++; if(i>=stages.length){clearInterval(timer); compute(action);}},130);
  }
  function payload(kind){
    const c=compute('export '+kind); return {schema:'goalos.loop.bottleneck.observatory.v1', kind, generated_at:new Date().toISOString(), objective:c.values.objective, scenario:c.values.scenario, risk:c.values.risk, horizon:c.values.horizon, readiness:c.readiness, bottleneck:c.bottleneck, decision:c.decision, boundary:{no_user_data:true,no_user_funds:true,no_wallet:true,no_transaction:true,no_network_call:true,no_production_authority:true,human_review_required:true}, gates:gates.map(([id,label])=>({id,label,pass:!!c.values[id]})), state_files:['contract.md','state.json','trace.md','progress.md','decision-state.json','bottleneck-report.json'], reviewer_route:['inspect contract','inspect disk state','read traces','restart from disk','verify evaluator independence','review bottleneck report','accept/reject/revise/dissent']};
  }
  function download(id){ const kind=id.replace('download','').toLowerCase(); const data=payload(kind); const ext=kind.includes('trace')||kind.includes('brief')||kind.includes('replay')?'md':'json'; let body=JSON.stringify(data,null,2); if(ext==='md') body=`# GoalOS Loop Bottleneck Observatory — ${kind}\n\n\`\`\`json\n${body}\n\`\`\`\n`; const blob=new Blob([body],{type:ext==='json'?'application/json':'text/markdown'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=`goalos-loop-bottleneck-${kind}-v1.${ext}`; a.click(); URL.revokeObjectURL(a.href); }
  function renderPalette(){ const q=($('paletteSearch')?.value||'').toLowerCase(); const rows=links.filter(x=>!q||x.join(' ').toLowerCase().includes(q)); $('paletteResults').innerHTML=rows.map(([name,href,desc])=>`<a class="result" href="${href}"><b>${name}</b><span>${desc}</span></a>`).join(''); }
  function openPalette(){ $('palette').showModal(); setTimeout(()=>$('paletteSearch').focus(),20); renderPalette(); }
  function hash(s){ let h=2166136261; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i); h+=(h<<1)+(h<<4)+(h<<7)+(h<<8)+(h<<24);} return (h>>>0).toString(16); }
  function escape(s){ return String(s).replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m])); }
  init();
})();
