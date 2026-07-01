(function(){
  'use strict';
  const stages=['TARGET','EMIT','FILTER','ATLAS','TEST-PLAN','EVAL','INSERT','PROMOTE'];
  const gates=[
    ['schema','Schema-bound artifacts','Artifacts validate or hard-stop; no silent corruption.',true],
    ['state','State hash continuity','Prompt pack, runner config, and state payload hashes bind continuation.',true],
    ['eci','Executed evidence gate','Confidence cannot inflate from simulated reasoning alone.',true],
    ['baseline','Baseline comparison','Candidate must beat incumbent, nearest-neighbor, null, and current stack where relevant.',true],
    ['risk','Risk gate','Prohibited or critical-risk candidates cannot promote.',true],
    ['persistence','Persistence under shocks','High novelty requires reproduction, stress, and persistence checks.',true],
    ['replay','Replay path','Replayable manifest, deterministic seeds, and verifier-ready artifacts.',true],
    ['omni','OMNI allocation only','OMNI can target exploration but cannot grant outcome authority.',true],
    ['dossier','Dossier packaged','Move‑37 candidates require reproduction, stress, persistence, and executive note.',false],
    ['council','Architect/Validator Council','Human/institutional review remains required before authority.',true],
    ['boundary','Public/private proof boundary','No user data, no user funds, no wallet, no transaction, no network call.',true]
  ];
  const state={run:false,stress:false,restarted:false,packaged:false,trace:false,overreach:false,step:0,gates:{}};
  gates.forEach(g=>state.gates[g[0]]=g[3]);
  const $=id=>document.getElementById(id);
  const pipeline=$('pipeline'), gateBox=$('gates'), logbook=$('logbook'), heroRail=$('heroRail');
  const inputs=['novelty','advantage','eci','risk','baseline','persistence'];
  function init(){
    pipeline.innerHTML=stages.map((s,i)=>`<div class="stage" data-stage="${i}"><small>${String(i+1).padStart(2,'0')}</small><strong>${s}</strong><p>${stageCopy(s)}</p></div>`).join('');
    heroRail.innerHTML=stages.slice(0,4).map(s=>`<span>${s}</span>`).join('');
    gateBox.innerHTML=gates.map(g=>`<div class="gate"><div><b>${g[1]}</b><small>${g[2]}</small></div><button class="switch ${state.gates[g[0]]?'on':''}" data-gate="${g[0]}" aria-label="Toggle ${g[1]}"></button></div>`).join('');
    document.querySelectorAll('[data-gate]').forEach(btn=>btn.addEventListener('click',()=>{const k=btn.getAttribute('data-gate');state.gates[k]=!state.gates[k];btn.classList.toggle('on',state.gates[k]);render('gate toggled: '+k);}));
    document.querySelectorAll('[data-run]').forEach(b=>b.addEventListener('click',()=>{state.run=true;state.step=0;render('RSI cycle started');}));
    document.querySelector('[data-stress]').addEventListener('click',()=>{state.stress=true;state.run=true;$('novelty').value=91;$('advantage').value=77;$('eci').value=52;$('risk').value=58;$('baseline').value=82;$('persistence').value=45;render('Move‑37 stress: high novelty raises burden of proof');});
    document.querySelector('[data-restart]').addEventListener('click',()=>{state.restarted=true;state.run=true;render('restart from manifest: cycle index preserved');});
    document.querySelector('[data-overreach]').addEventListener('click',()=>{state.overreach=true;state.gates.omni=false;document.querySelector('[data-gate="omni"]').classList.remove('on');render('OMNI overreach simulated');});
    document.querySelector('[data-dossier]').addEventListener('click',()=>{state.packaged=true;state.gates.dossier=true;document.querySelector('[data-gate="dossier"]').classList.add('on');render('Move‑37 dossier packaged');});
    document.querySelector('[data-reset]').addEventListener('click',()=>{location.reload();});
    document.querySelectorAll('[data-download]').forEach(b=>b.addEventListener('click',()=>download(b.getAttribute('data-download'))));
    inputs.forEach(id=>$(id).addEventListener('input',()=>render('parameter changed: '+id)));
    $('scenario').addEventListener('change',scenario);
    setInterval(()=>{state.step=(state.step+1)%stages.length;paintStages();},1400);
    render('console ready');
  }
  function stageCopy(s){return {TARGET:'allocate exploration',EMIT:'generate candidates',FILTER:'risk + interest',ATLAS:'causal map', 'TEST-PLAN':'falsification ladders',EVAL:'executed evidence',INSERT:'append archive',PROMOTE:'dossier + queue'}[s]||'';}
  function values(){const o={};inputs.forEach(id=>{o[id]=Number($(id).value);$(id+'Out').textContent=o[id];});return o;}
  function decision(){const v=values(), g=state.gates;let blockers=[];
    if(!g.boundary) blockers.push('BLOCK_PRIVACY_BOUNDARY');
    if(!g.schema) blockers.push('REJECT_SCHEMA_DRIFT');
    if(!g.state) blockers.push('HOLD_STATE_HASH_REQUIRED');
    if(!g.eci || v.eci<45) blockers.push('HOLD_EXECUTED_EVIDENCE_REQUIRED');
    if(!g.baseline) blockers.push('HOLD_BASELINE_COMPARISON_REQUIRED');
    if(!g.risk || v.risk>76) blockers.push('REJECT_RISK_GATE_FAILED');
    if(!g.replay) blockers.push('HOLD_REPLAY_REQUIRED');
    if(!g.omni || state.overreach) blockers.push('REJECT_OMNI_OUTCOME_AUTHORITY');
    if(!g.council) blockers.push('HOLD_COUNCIL_REVIEW_REQUIRED');
    if(v.novelty>=80 && (!g.dossier || !state.packaged)) blockers.push('HOLD_MOVE37_DOSSIER_REQUIRED');
    if(v.novelty>=80 && (!g.persistence || v.persistence<62)) blockers.push('HOLD_PERSISTENCE_REQUIRED');
    if(v.advantage<=v.baseline-6) blockers.push('REJECT_BASELINES_WIN');
    if(!state.run) return ['AWAITING_RSI_RUN',0,blockers];
    let readiness=Math.round(Math.max(0,Math.min(100,(v.eci*.22)+(v.advantage*.24)+((100-v.risk)*.16)+(v.persistence*.18)+((100-Math.max(0,v.baseline-v.advantage))*.1)+10)));
    if(blockers.length) readiness=Math.min(readiness,74);
    let stateName=blockers[0]|| (v.novelty>=80?'MOVE37_DOSSIER_REVIEW_READY':'RSI_REVIEW_READY');
    return [stateName,readiness,blockers];
  }
  function render(reason){const v=values(), d=decision();
    $('decisionState').textContent=d[0];$('heroDecision').textContent=d[0];$('decisionPill').textContent=d[0];$('readiness').textContent=d[1];document.querySelector('.score-ring').style.setProperty('--score',(d[1]*3.6)+'deg');
    $('dashReplay').textContent=state.restarted?'98%':'95%';$('dashEvidence').textContent=v.eci>=84?'E4':v.eci>=66?'E3':v.eci>=45?'E2':'E1';$('dashNovelty').textContent=v.novelty;$('dashAdvantage').textContent='+'+v.advantage;$('dashSafety').textContent=v.risk>76?'BLOCK':'OK';$('dashState').textContent=state.gates.state?'HASHED':'HOLD';
    let lines=[];lines.push('00 · '+reason);lines.push('01 · objective: '+$('objective').value.slice(0,96)+( $('objective').value.length>96?'…':''));lines.push('02 · pipeline: TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE');lines.push('03 · OMNI: '+(state.gates.omni&&!state.overreach?'search allocation only':'attempted outcome authority blocked'));lines.push('04 · ECI: '+$('dashEvidence').textContent+' · novelty '+v.novelty+' · advantage '+v.advantage+' · risk '+v.risk);lines.push('05 · decision: '+d[0]+' · readiness '+d[1]);
    if(d[2].length) lines.push('06 · blockers: '+d[2].join(', ')); else lines.push('06 · no mandatory blockers; reviewer packet ready');
    logbook.textContent=lines.join('\n');$('heroLog').textContent=lines.slice(2).join('\n');
    paintStages();
  }
  function paintStages(){document.querySelectorAll('.stage').forEach((el,i)=>el.classList.toggle('active',i===state.step));heroRail.querySelectorAll('span').forEach((el,i)=>el.classList.toggle('active',i===state.step%4));}
  function scenario(){const s=$('scenario').value;if(s==='move37'){$('novelty').value=88;$('advantage').value=79;$('eci').value=58;$('persistence').value=51;$('risk').value=52;}if(s==='pilot'){$('novelty').value=52;$('advantage').value=59;$('eci').value=76;$('persistence').value=73;$('risk').value=26;}if(s==='council'){$('novelty').value=81;$('advantage').value=72;$('eci').value=68;$('persistence').value=70;$('risk').value=42;}if(s==='dossier'){$('novelty').value=90;$('advantage').value=84;$('eci').value=72;$('persistence').value=78;$('risk').value=38;state.packaged=true;state.gates.dossier=true;}render('scenario loaded: '+s);}
  function artifact(kind){const v=values(), d=decision();return {artifact:`goalos-${kind}`,page:'from-loop-to-rsi-sovereign-console.html',generated_at:new Date().toISOString(),objective:$('objective').value,scenario:$('scenario').value,decision_state:d[0],readiness:d[1],parameters:v,gates:state.gates,boundary:'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.',pipeline:stages,notes:{omni:'search control only; never outcome authority',move37:'high novelty raises skepticism and requires dossier',claim_boundary:'public-alpha browser-local demonstration; not achieved AGI/ASI; not production authorization'}}}
  function download(kind){let data=artifact(kind);let name='goalos-rsi-'+kind+'-'+Date.now()+'.json';if(kind==='brief'){data.reviewer_questions=['Does OMNI remain allocation-only?','Is ECI executed/replayed rather than simulated?','Which baseline wins?','Can the run restart from manifest?','Is a Move‑37 dossier packaged?'];}if(kind==='dossier'){data.dossier=['recognize','reproduce','stress-test','persistence gate','package','council review'];}const blob=new Blob([JSON.stringify(data,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove();},0);}
  init();
})();
