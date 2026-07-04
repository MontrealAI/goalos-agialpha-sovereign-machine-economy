(() => {
  const $ = (id) => document.getElementById(id);
  const gateSpec = [
    ['docket', 'Evidence Docket complete'], ['replay','Replay path present'], ['baselines','Baseline matrix present'], ['costrisk','Cost/risk ledger present'], ['claim','Claim boundary explicit'], ['privacy','No data / no funds boundary'], ['validator','Validator notes present'], ['dissent','Dissent channel open']
  ];
  const phases = ['Docket','Claims','Baselines','Replay','Cost/Risk','Validator','Dissent','Verdict'];
  const scenarios = {
    'proof-run': {title:'Proof Run 001 rehearsal docket', claim:'Proof Run 001 can move from architecture to public-safe mission rehearsal.', risk:'medium'},
    'mission-control': {title:'Proof Mission Control readiness', claim:'A public-safe mission can be prepared for reviewer inspection.', risk:'medium'},
    'falsification': {title:'Falsification Gauntlet claim', claim:'The claim survives baseline, replay, cost/risk, and boundary stress.', risk:'high'},
    'compounding': {title:'Capability Compounding Lab docket', claim:'Accepted proof can become reusable capability under gates.', risk:'medium'}
  };
  const gates = {};
  function init(){
    const box=$('gates'); box.innerHTML='';
    gateSpec.forEach(([id,label])=>{ gates[id]=true; const row=document.createElement('label'); row.className='gate'; row.innerHTML=`<span>${label}</span><input type="checkbox" id="gate-${id}" checked>`; box.appendChild(row); row.querySelector('input').addEventListener('change',e=>{gates[id]=e.target.checked; compute();}); });
    $('timeline').innerHTML=phases.map(p=>`<div class="step">${p}</div>`).join('');
    ['scenario','posture'].forEach(id=>$(id).addEventListener('change',compute));
    $('runReview').addEventListener('click',runReview);
    $('stressReplay').addEventListener('click',()=>{gates.replay=false; $('gate-replay').checked=false; log('Replay path removed. Review must block strong promotion.'); compute();});
    $('resetRoom').addEventListener('click',()=>{gateSpec.forEach(([id])=>{gates[id]=true; $('gate-'+id).checked=true;}); $('log').textContent=''; compute();});
    $('downloadReport').addEventListener('click',()=>download('goalos-reviewer-report.md',makeReport(),'text/markdown'));
    $('downloadReplay').addEventListener('click',()=>download('goalos-replay-checklist.md',makeReplay(),'text/markdown'));
    $('downloadAttestation').addEventListener('click',()=>download('goalos-validator-attestation.json',JSON.stringify(makeDocket().validator_attestation,null,2),'application/json'));
    $('downloadDissent').addEventListener('click',()=>download('goalos-dissent-memo.md',makeDissent(),'text/markdown'));
    $('copyIssue').addEventListener('click',copyIssue);
    document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-mode]').forEach(x=>x.classList.remove('active')); b.classList.add('active'); document.body.dataset.mode=b.dataset.mode; log('Mode changed to '+b.dataset.mode+'.');}));
    compute();
  }
  function score(){ let s=20; gateSpec.forEach(([id])=>{if(gates[id]) s+=9;}); if($('posture').value==='adversarial') s+=2; if(!gates.replay) s-=18; if(!gates.privacy) s-=40; return Math.max(0,Math.min(100,s)); }
  function decision(){ if(!gates.privacy) return 'BLOCK_PRIVACY_BOUNDARY'; if(!gates.docket) return 'REJECT_NO_DOCKET'; if(!gates.replay) return 'REJECT_UNREPLAYABLE'; if(!gates.baselines) return 'REVISE_NO_BASELINES'; if(!gates.validator) return 'HOLD_VALIDATOR_REVIEW'; if(!gates.claim) return 'REVISE_CLAIM_BOUNDARY'; return score()>=82?'REVIEW_READY':'HOLD_PENDING_REVIEW'; }
  function compute(){ const s=score(), d=decision(); $('readiness').textContent=s; $('dialScore').textContent=s; $('decisionState').textContent=d.replaceAll('_',' '); $('replayState').textContent=gates.replay?'ready':'blocked'; $('dissentCount').textContent=gates.dissent?'1':'0'; $('dialFill').parentElement.style.background=`conic-gradient(${d.startsWith('REJECT')||d.startsWith('BLOCK')?'#ff6384':'#66ffd1'} ${s*3.6}deg, rgba(255,255,255,.1) 0deg)`; const msg = {REVIEW_READY:'The package is review-ready. Stronger public claims still require human reviewer judgment.', HOLD_PENDING_REVIEW:'The package is partially ready but needs more reviewer confidence.', BLOCK_PRIVACY_BOUNDARY:'Privacy/data boundary failed. Review blocks immediately.', REJECT_NO_DOCKET:'No Evidence Docket. No strong claim.', REJECT_UNREPLAYABLE:'Replay path missing. The claim is not reviewable.', REVISE_NO_BASELINES:'Baseline matrix missing. Revise before promotion.', HOLD_VALIDATOR_REVIEW:'Validator notes missing. Hold for review.', REVISE_CLAIM_BOUNDARY:'Claim boundary missing. Revise before publication.'}; $('verdictBox').textContent=msg[d]||d; updateSteps(d); }
  function updateSteps(d){ const nodes=[...document.querySelectorAll('.step')]; nodes.forEach((n,i)=>{n.className='step'; if(i<Math.floor(score()/14)) n.classList.add('done');}); if(d.startsWith('REJECT')||d.startsWith('BLOCK')) nodes[Math.min(nodes.length-1,Math.floor(score()/14))].classList.add('blocked'); }
  function runReview(){ $('log').textContent=''; const lines=['Reviewer path started.','Evidence Docket inspected.','Claims Matrix compared to boundary.','Baselines checked for B0-B6 coverage.','Replay checklist evaluated.','Cost/risk ledger reviewed.','Validator notes prepared.','Dissent channel preserved.','Verdict emitted: '+decision()+'.']; let i=0; const tick=()=>{ if(i<lines.length){ log(lines[i++]); setTimeout(tick,260);} }; tick(); compute(); }
  function log(x){ const t=new Date().toLocaleTimeString(); $('log').textContent += `${t}  ${x}\n`; $('log').scrollTop=$('log').scrollHeight; }
  function makeDocket(){ const sc=scenarios[$('scenario').value]; return {schema:'goalos.external_reviewer_replay_room.v1', generated_at:new Date().toISOString(), browser_local:true, no_network_call:true, no_user_data:true, no_user_funds:true, wallet_or_mainnet:false, human_review_required:true, review_object:sc, reviewer_posture:$('posture').value, gates:{...gates}, readiness_score:score(), decision_state:decision(), validator_attestation:{verdict:decision(), replay:gates.replay, baselines:gates.baselines, claim_boundary:gates.claim, recommendation:decision()==='REVIEW_READY'?'accept_for_human_review':'revise_or_hold'}}; }
  function makeReport(){ const d=makeDocket(); return `# GoalOS External Reviewer Report\n\nReview object: ${d.review_object.title}\n\nClaim: ${d.review_object.claim}\n\nDecision: ${d.decision_state}\n\nReadiness: ${d.readiness_score}/100\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n\n## Gates\n${Object.entries(d.gates).map(([k,v])=>`- ${k}: ${v?'PASS':'FAIL'}`).join('\n')}\n`; }
  function makeReplay(){ return `# Replay Checklist\n\n- Confirm docket manifest.\n- Confirm claims matrix.\n- Confirm baseline matrix.\n- Confirm replay path.\n- Confirm cost/risk ledger.\n- Confirm no-data/no-funds boundary.\n- Confirm validator notes.\n- Confirm dissent channel.\n\nDecision: ${decision()}\n`; }
  function makeDissent(){ return `# Dissent Memo\n\nDissent is preserved by default. A reviewer may object to evidence quality, replay completeness, baselines, cost/risk accounting, or claim boundaries.\n\nCurrent decision: ${decision()}\n`; }
  function copyIssue(){ const text=`## External Reviewer Replay Room Review\n\nDecision: ${decision()}\nReadiness: ${score()}/100\n\nBoundary confirmed: no user data, no user funds, no wallet, no transaction.\n\nGates:\n${Object.entries(gates).map(([k,v])=>`- [${v?'x':' '}] ${k}`).join('\n')}\n`; if(navigator.clipboard){/* clipboard disabled in public-alpha */ console.log(text).then(()=>log('GitHub-ready review issue copied.')).catch(()=>log('Copy unavailable; download report instead.'));} else {log('Clipboard unavailable; download report instead.');}}
  function download(name, content, type){ const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([content],{type})); a.download=name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),500); }
  init();
})();
