(()=>{"use strict";
const $=id=>document.getElementById(id);
const state={mode:"executive",stress:false,ran:false,stage:0,activePreset:"repo"};
const stages=[
  ["AIM","Mission Contract"],["CLAIM","Claims Matrix"],["SOURCE","Source Boundary"],["BASE","Baselines"],
  ["DOCKET","Evidence Plan"],["REPLAY","Replay Path"],["VALID","Validator Packet"],["RISK","Risk Ledger"],
  ["DECIDE","Decision State"],["HUMAN","Human Review"]
];
const presets={
  repo:"Evaluate whether the GoalOS public-alpha repository and website are ready for Proof Run 001 by checking claim boundaries, evidence surfaces, code parity reports, user paths, and replay readiness.",
  frontier:"Produce a public-safe frontier release governance review plan that turns the release question into claims, evidence requirements, validator seats, rollback conditions, and a governed decision state.",
  demo:"Review the GoalOS public demo series for user clarity, browser-local safety, evidence downloads, no-data/no-funds boundaries, and readiness for non-technical visitors.",
  pilot:"Design a founding proof mission pilot intake package for one public-safe institutional objective, including mission contract, claims matrix, evidence docket, review path, and validator packet.",
  custom:"Describe one public-safe objective here. Do not include personal, customer, confidential, regulated, credential, wallet, payment, or trade-secret data."
};
function now(){return new Date().toISOString().slice(11,19)}
function log(msg,type=""){const p=document.createElement("p");p.innerHTML=`<b>${now()}</b> ${msg}`; if(type)p.className=type; $("console").prepend(p)}
function gates(){return Array.from(document.querySelectorAll("[data-gate]")).reduce((a,i)=>(a[i.dataset.gate]=i.checked,a),{})}
function compute(){
  const g=gates(); const obj=$("objective").value.trim();
  let score=20;
  if(obj.length>80)score+=10; if(obj.length>220)score+=5;
  if(g.contract)score+=8;if(g.claims)score+=8;if(g.docket)score+=10;if(g.baselines)score+=9;if(g.replay)score+=10;if(g.validators)score+=12;if(g.risk)score+=8;if(g.boundary)score+=10;
  const risk=$("risk").value; if(risk==="moderate")score-=8; if(risk==="high")score-=25;
  if(state.stress)score-=18;
  score=Math.max(0,Math.min(99,score));
  const missing=[];
  if(!obj || obj.length<80)missing.push("objective too vague");
  Object.entries(g).forEach(([k,v])=>{if(!v)missing.push(k.replace(/_/g," "))});
  if(risk==="high")missing.push("private agreement required");
  if(state.stress)missing.push("stress condition active");
  let decision="DRAFT_NEEDS_EVIDENCE";
  if(score>=86 && missing.length===0)decision="MISSION_REVIEW_READY";
  else if(score>=72 && !missing.includes("replay") && !missing.includes("validator packet"))decision="HOLD_PENDING_HUMAN_REVIEW";
  else if(risk==="high")decision="BLOCK_PRIVATE_OR_REGULATED_SCOPE";
  else if(missing.includes("replay"))decision="REJECT_UNREPLAYABLE";
  else if(missing.includes("baselines"))decision="HOLD_BASELINE_REQUIRED";
  else if(missing.includes("validator packet"))decision="DRAFT_NEEDS_VALIDATOR_PACKET";
  return {score,missing,decision,risk,g};
}
function updateVisual(){
  const {score,missing,decision,risk,g}=compute();
  $("readiness").textContent=score; $("scoreText").textContent=score; $("docketStatus").textContent=score>=86?"ready":"draft"; $("riskState").textContent=risk; $("missingCount").textContent=missing.length; $("decisionState").textContent=decision;
  $("scoreCircle").style.strokeDashoffset=308-(308*score/100);
  $("stateList").innerHTML=[
    ["Mission contract",g.contract],["Claims matrix",g.claims],["Evidence docket",g.docket],["Baseline ladder",g.baselines],["Replay path",g.replay],["Validator packet",g.validators],["Boundary",g.boundary]
  ].map(([k,v])=>`<li><span>${k}</span><b>${v?"ready":"missing"}</b></li>`).join("");
  $("pipeline").innerHTML=stages.map((s,i)=>{
    const gateMap=["contract","claims","boundary","baselines","docket","replay","validators","risk","docket","boundary"];
    const ok=!!g[gateMap[i]] && i<=state.stage;
    const missingClass=!g[gateMap[i]]?" missing":"";
    return `<div class="gate ${ok?"ok":""}${missingClass}"><b>${String(i+1).padStart(2,"0")} ${s[0]}</b><span>${s[1]}</span></div>`;
  }).join("");
  const nodes=$("stageNodes");
  const coords=[[310,76],[420,112],[485,220],[450,340],[332,380],[210,355],[135,236],[174,120]];
  nodes.innerHTML=coords.map((c,i)=>`<g class="node ${i<=Math.min(state.stage,7)?"active":""}" transform="translate(${c[0]},${c[1]})"><circle r="28"/><text text-anchor="middle" y="5">${stages[i][0].slice(0,2)}</text></g>`).join("");
  $("chars").textContent=$("objective").value.length;
}
function buildPackage(){
  const {score,missing,decision,risk,g}=compute();
  const id="GMF-"+Math.abs(hash($("objective").value)).toString(16).slice(0,8).toUpperCase();
  const obj=$("objective").value.trim();
  return {
    schema:"goalos.proof_mission_forge.v1",
    mission_id:id,
    generated_at:new Date().toISOString(),
    public_safe_boundary:{
      no_user_data:true,no_user_funds:true,no_wallet:true,no_transaction:true,no_network_call:true,human_review_required:true,
      forbidden:"personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, trade-secret, proprietary, privileged data"
    },
    mission_contract:{
      objective:obj,
      decision_to_support:$("decision").value,
      risk_class:risk,
      source_boundary:$("sources").value,
      success_criteria:[
        "Mission Contract is clear and bounded",
        "Claims Matrix identifies supported, unsupported, and deferred claims",
        "Evidence Docket plan includes baselines, proof packets, replay, validators, cost/risk ledger, and claim boundary",
        "Human reviewer can accept, reject, or request revision"
      ],
      failure_criteria:[
        "Private or regulated data required",
        "No replay path",
        "No baseline comparison",
        "No validator packet",
        "Claim boundary missing or overbroad"
      ]
    },
    claims_matrix:[
      {claim:"The objective can be converted into a public-safe proof mission",required_evidence:"Mission Contract + data boundary",status:g.contract&&g.boundary?"supported_by_template":"needs_revision"},
      {claim:"The mission can be reviewed by validators",required_evidence:"Validator packet + replay checklist",status:g.validators&&g.replay?"review_ready":"incomplete"},
      {claim:"The mission should advance to Proof Run 001",required_evidence:"Evidence Docket, baselines, cost/risk ledger, human review",status:score>=86?"candidate":"not_yet"}
    ],
    evidence_docket_plan:["00_manifest","01_claims_matrix","02_mission_contract","03_environment_boundary","04_baselines","05_proof_packets","06_replay_instructions","07_validator_reports","08_cost_risk_ledger","09_decision_state","10_chronicle_entry","11_capability_package"],
    gates:g,
    readiness_score:score,
    missing_gates:missing,
    governed_decision_state:decision,
    validator_packet:{
      ask:"Review the mission package. Mark supported, unsupported, revise, or reject. Do not submit private data.",
      review_questions:[
        "Is the objective bounded?",
        "Are sources and data boundaries public-safe?",
        "Are baselines sufficient?",
        "Can the mission be replayed?",
        "Is the claim boundary clear?",
        "What would falsify the mission?"
      ]
    }
  };
}
function hash(s){let h=2166136261; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i); h=Math.imul(h,16777619)} return h|0}
function mdContract(){
  const p=buildPackage();
  return `# GoalOS Proof Mission Contract\n\nMission ID: ${p.mission_id}\n\n## Objective\n${p.mission_contract.objective}\n\n## Decision to support\n${p.mission_contract.decision_to_support}\n\n## Risk class\n${p.mission_contract.risk_class}\n\n## Source boundary\n${p.mission_contract.source_boundary}\n\n## Success criteria\n${p.mission_contract.success_criteria.map(x=>"- "+x).join("\n")}\n\n## Failure criteria\n${p.mission_contract.failure_criteria.map(x=>"- "+x).join("\n")}\n\n## Public boundary\nNo user data. No user funds. No wallet. No transaction. No network call. Human review required.\n`;
}
function mdIssue(){
  const p=buildPackage();
  return `## GoalOS Proof Mission Proposal\n\n**Mission ID:** ${p.mission_id}\n\n### Objective\n${p.mission_contract.objective}\n\n### Decision to support\n${p.mission_contract.decision_to_support}\n\n### Risk class\n${p.mission_contract.risk_class}\n\n### Source boundary\n${p.mission_contract.source_boundary}\n\n### Readiness\n${p.readiness_score}/100 — ${p.governed_decision_state}\n\n### Missing gates\n${p.missing_gates.length?p.missing_gates.map(x=>"- "+x).join("\n"):"- none"}\n\n### Requested review\n- [ ] Evidence Docket reviewer\n- [ ] Replay reviewer\n- [ ] Claim-boundary reviewer\n- [ ] Cost/risk ledger reviewer\n- [ ] Validator report reviewer\n\n### Boundary confirmation\n- [ ] I confirm this issue contains no personal data, customer data, confidential data, regulated records, credentials, wallet data, private keys, seed phrases, payment data, or trade secrets.\n- [ ] I understand this repository does not accept user data or user funds.\n`;
}
function download(name,content,type="application/json"){
  const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([content],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)
}
function runForge(){
  state.ran=true; state.stage=0; $("console").innerHTML="";
  const seq=["Mission Contract sealed","Claims Matrix drafted","Source and data boundary checked","Baseline ladder attached","Evidence Docket plan assembled","Replay checklist generated","Validator packet prepared","Cost/risk ledger initialized","Governed Decision State emitted","Human review boundary preserved"];
  seq.forEach((msg,i)=>setTimeout(()=>{state.stage=i; log(msg); updateVisual();},i*180));
}
function stressMission(){state.stress=!state.stress; log(state.stress?"Stress mode: proof debt, scope uncertainty, and validator burden increased.":"Stress mode cleared."); updateVisual()}
function reset(){state.stress=false; state.stage=0; $("preset").value="repo"; $("objective").value=presets.repo; Array.from(document.querySelectorAll("[data-gate]")).forEach(i=>i.checked=i.dataset.gate!=="validators"); log("Reset to public-safe repository readiness mission."); updateVisual()}
function copy(text){navigator.clipboard&&/* clipboard disabled in public-alpha */ console.log(text).then(()=>log("Copied to clipboard. Confirm no restricted data before posting."),()=>fallback(text)); if(!navigator.clipboard)fallback(text)}
function fallback(text){const t=document.createElement("textarea");t.value=text;document.body.appendChild(t);t.select();document.execCommand("copy");t.remove();log("Copied to clipboard.")}
function bind(){
  $("preset").addEventListener("change",e=>{$("objective").value=presets[e.target.value]||presets.repo; updateVisual()});
  $("objective").addEventListener("input",updateVisual); ["decision","risk","sources"].forEach(id=>$(id).addEventListener("change",updateVisual));
  document.querySelectorAll("[data-gate]").forEach(i=>i.addEventListener("change",updateVisual));
  document.querySelectorAll("[data-mode]").forEach(b=>b.addEventListener("click",()=>{state.mode=b.dataset.mode;document.querySelectorAll("[data-mode]").forEach(x=>x.classList.toggle("active",x===b));log(`Mode switched to ${state.mode}.`)}));
  ["runForge","runForgeTop"].forEach(id=>$(id).addEventListener("click",runForge));
  $("safePreset").addEventListener("click",()=>{$("preset").value="repo";$("objective").value=presets.repo;updateVisual();log("Loaded public-safe example.")});
  $("stress").addEventListener("click",stressMission); $("reset").addEventListener("click",reset);
  $("downloadContract").addEventListener("click",()=>download("goalos-mission-contract.md",mdContract(),"text/markdown"));
  $("downloadDocket").addEventListener("click",()=>download("goalos-evidence-docket-plan.json",JSON.stringify(buildPackage(),null,2)));
  $("downloadValidator").addEventListener("click",()=>download("goalos-validator-packet.json",JSON.stringify(buildPackage().validator_packet,null,2)));
  $("downloadBrief").addEventListener("click",()=>download("goalos-proof-mission-brief.md",`# GoalOS Proof Mission Brief\n\n${mdContract()}\n\n## Decision State\n${buildPackage().governed_decision_state}\n`,"text/markdown"));
  ["copyIssue","copyIssueTop"].forEach(id=>$(id).addEventListener("click",()=>copy(mdIssue())));
  $("copySummary").addEventListener("click",()=>copy(`GoalOS Proof Mission Forge turns an objective into a Mission Contract, Claims Matrix, Evidence Docket plan, validator packet, and review-ready issue draft. Boundary: no user data, no user funds, no wallet, no transaction, no network call, human review required.`));
}
bind(); updateVisual();
})();