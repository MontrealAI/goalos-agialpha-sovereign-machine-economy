
// GOALOS_INCREMENTAL_ASCENSION_V65
(function(){
  const families = {
    ai:["Map top vendor claims to attached evidence", "Build buyer-readiness risk ledger", "Verify data/privacy/security boundaries", "Create external reviewer attestation packet"],
    energy:["Verify site/load/tariff assumptions", "Model resilience and outage baseline", "Check permitting/interconnection proof debt", "Validate financing sensitivity and savings claims"],
    contract:["Verify contract source/address map", "Map roles, permissions, upgrade surfaces", "Create non-technical contract atlas", "Prepare manual Etherscan reviewer packet"],
    privacy:["Create browser-local data-flow map", "Check storage/network/wallet exclusion", "Rewrite privacy boundary for non-technical users", "Confirm no hidden transaction or backend path"],
    research:["Build falsification ladder", "Map claims to baselines", "Prepare replay and external review packet", "Block unsupported novelty claims"],
    general:["Extract major claims and proof debt", "Define mission contract and success criteria", "Create ProofBundle return template", "Prepare Evidence Docket review questions"]
  };
  function pickDomain(text){const t=text.toLowerCase(); if(/solar|microgrid|hospital|energy|tariff|grid|climate/.test(t))return 'energy'; if(/vendor|procurement|trust room|buyer|soc|compliance/.test(t))return 'ai'; if(/contract|ethereum|mainnet|wallet|token|solidity|ens/.test(t))return 'contract'; if(/privacy|no-data|backend|network|storage/.test(t))return 'privacy'; if(/research|paper|benchmark|claim|experiment|sota/.test(t))return 'research'; return 'general'}
  function compile(){
    const el=document.querySelector('[data-goalos-v65-objective]'); const out=document.querySelector('[data-goalos-v65-output]'); if(!el||!out)return;
    const objective=(el.value||'Create a public-safe proof mission for GoalOS.').trim(); const domain=pickDomain(objective);
    const jobs=families[domain].map((title,i)=>({job_id:`AGIJOB-${domain.toUpperCase()}-${String(i+1).padStart(2,'0')}`,title,why_needed:'This closes proof debt before a claim can become authority.',acceptance_tests:['Evidence attached or explicitly marked missing','Replay/review path present','Unsupported claims remain blocked'],validator_role:'AGI Node Validator + human reviewer',promotion_rule:'No Chronicle promotion unless replay and validation pass.'}));
    const docket={version:'goalos.incremental.v65',objective,domain,proof_debt:jobs.map(j=>j.title),agi_jobs:jobs,claim_boundary:['No achieved AGI/ASI claim','No empirical SOTA claim','No live settlement in local mode','Human review required'],next_step:'Run Proof Run 001 and publish the Evidence Docket.'};
    out.innerHTML='<div class="joblist">'+jobs.map(j=>`<div class="job"><b>${j.job_id}</b><h3>${j.title}</h3><p>${j.why_needed}</p><small>Validator: ${j.validator_role}<br>${j.promotion_rule}</small></div>`).join('')+'</div><pre>'+JSON.stringify(docket,null,2)+'</pre><p><button data-goalos-v65-download>Download AGI Jobs JSON</button></p>';
    const btn=out.querySelector('[data-goalos-v65-download]'); btn&&btn.addEventListener('click',()=>{const blob=new Blob([JSON.stringify(docket,null,2)],{type:'application/json'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='goalos-v65-proof-debt-agijobs.json';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)});
  }
  document.addEventListener('click',e=>{if(e.target&&e.target.matches('[data-goalos-v65-compile]'))compile()});
  document.addEventListener('DOMContentLoaded',compile);
})();
