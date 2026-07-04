function $(s){return document.querySelector(s)}
function sampleDocket(){
  const obj = ($('#mission-objective')||{}).value || 'Review GoalOS launch readiness and produce a validator-ready Evidence Docket.';
  const decision = ($('#mission-decision')||{}).value || 'Should this public-alpha system proceed to Proof Run 001?';
  const risk = ($('#mission-risk')||{}).value || 'public-alpha / no external action';
  return {
    schema:'goalos.evidence_docket.6_1.sample',
    generated_at:new Date().toISOString(),
    local_only:true,
    mission_contract:{objective:obj,decision_to_support:decision,risk_class:risk,human_review_required:true},
    claims_matrix:[
      {claim:'GoalOS can produce a Mission Contract',status:'supported_by_reference_demo'},
      {claim:'GoalOS has production authorization',status:'not_claimed'},
      {claim:'GoalOS has achieved AGI or ASI',status:'not_claimed'}
    ],
    evidence_packets:['sample_mission_contract','sample_claims_matrix','sample_validator_note','sample_replay_path'],
    validator_note:'Sample only. Real validation requires Proof Run 001 and independent review.',
    boundary:['no_model_call','no_wallet','no_transaction','no_external_action','human_review_required']
  };
}
function renderDocket(){const out=$('#docket-output'); if(!out)return; out.textContent=JSON.stringify(sampleDocket(),null,2)}
function downloadDocket(){const blob=new Blob([JSON.stringify(sampleDocket(),null,2)],{type:'application/json'}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='goalos-sample-evidence-docket.json'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function proofFlight(){const out=$('#proof-flight-output'); if(!out)return; const gates=['Mission Contract','Claims Matrix','Source Provenance','Risk Ledger','Evidence Docket','Validator Note','Decision State','Chronicle Entry','Capability Package','Human Boundary']; out.textContent=''; let i=0; const t=setInterval(()=>{out.textContent += `${String(i+1).padStart(2,'0')}  ${gates[i]} — ready for review\n`; i++; if(i>=gates.length){clearInterval(t); out.textContent += '\nDONE? Not yet. This is the sample path. Proof Run 001 creates the real docket.\n';}},220)}
document.addEventListener('DOMContentLoaded',()=>{if($('#docket-output'))renderDocket(); document.querySelectorAll('[data-proof-flight]').forEach(b=>b.addEventListener('click',proofFlight)); document.querySelectorAll('[data-render-docket]').forEach(b=>b.addEventListener('click',renderDocket)); document.querySelectorAll('[data-download-docket]').forEach(b=>b.addEventListener('click',downloadDocket));});
