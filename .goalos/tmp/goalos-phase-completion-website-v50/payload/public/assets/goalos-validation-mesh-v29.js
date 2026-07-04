(()=>{
  const $=(q)=>document.querySelector(q); const $$=(q)=>Array.from(document.querySelectorAll(q));
  const routes=window.GOALOS_VALIDATION_MESH_ROUTES_V29||[];
  const forbidden=['seed phrase','private key','password','api key','secret key','customer data','personal data','passport','credit card','bank account','wire transfer','wallet connect','connect wallet','transaction','trade','investment advice','legal advice','medical advice','exploit','malware','phishing','attack a target','scan external'];
  const playbooks=[
    ['AGI Node validates a public proof route','Validate whether the Evidence Docket route for the 48 Ethereum Mainnet contracts is complete, public-safe, and ready for AGI Node precheck.','node'],
    ['Human validates a public claim','Prepare a human review packet for a high-impact public claim before publication.','human'],
    ['Hybrid validation for Loop → RSI','Run AGI Node precheck and human review for a Loop to RSI governance dossier.','hybrid'],
    ['Council review for Move‑37','Prepare an Architect / Validator Council review packet for a high-novelty Move‑37 candidate.','council'],
    ['Token boundary validation','Validate the token boundary: public contract identification only, no sale, no custody, no wallet support, no investment advice.','node'],
    ['Contract atlas validation','Validate the Mainnet Contract Atlas for completeness, route fit, claim boundary, and reviewer readiness.','node'],
    ['Evidence Docket completeness','Validate that an Evidence Docket has claims matrix, baselines, proof packets, risk/cost ledgers, replay path, and boundary.','node'],
    ['Defensive cybersecurity mission','Prepare hybrid validation for a repo-owned defensive cybersecurity proof mission with no exploit execution and human review.','hybrid'],
    ['Controlled pilot program','Prepare human validation for a controlled pilot where every serious pilot ends with a docket and acceptance record.','human'],
    ['Vendor evidence review','Validate a vendor/tool claim using evidence, baselines, contradiction register, and reviewer packet.','hybrid'],
    ['Website route integrity','Let the AGI Node validate public site route integrity, missing pages, search index, and all-pages navigation.','node'],
    ['Strategic opportunity proof mission','Prepare Council validation for a strategic opportunity mapped into a proof mission, dossier, and review session.','council']
  ];
  const sensitive=()=>{const q=($('#objective')?.value||'').toLowerCase(); return forbidden.some(t=>q.includes(t));};
  function digest(s){let h=2166136261>>>0; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i); h=Math.imul(h,16777619)} return 'GOALOS-'+(h>>>0).toString(16).toUpperCase().padStart(8,'0')}
  function classify(q){q=q.toLowerCase(); if(q.includes('contract')||q.includes('mainnet')||q.includes('ethereum')) return 'CONTRACT_ATLAS'; if(q.includes('rsi')||q.includes('loop')||q.includes('omni')||q.includes('move')) return 'LOOP_RSI'; if(q.includes('token')||q.includes('wallet')||q.includes('privacy')||q.includes('data')) return 'BOUNDARY_REVIEW'; if(q.includes('proof')||q.includes('docket')||q.includes('evidence')) return 'EVIDENCE_DOCKET'; if(q.includes('cyber')||q.includes('security')) return 'DEFENSIVE_SECURITY'; return 'GENERAL_MISSION'}
  function scoreRoute(r,q){q=q.toLowerCase(); let s=0; (r.tags||[]).forEach(t=>{if(q.includes(t))s+=3}); if(q.includes(r.title.toLowerCase().split(' ')[0]))s+=1; return s}
  function bestRoutes(q){return routes.map(r=>({...r,score:scoreRoute(r,q)})).sort((a,b)=>b.score-a.score).filter((r,i)=>r.score>0||i<4).slice(0,5)}
  function recommendedAuthority(q, requested, risk, target){
    const high = risk==='HIGH'||risk==='CRITICAL'||/external action|production/i.test(target)||/legal|financial|security posture|publication|deploy|release|settlement/i.test(q);
    const strategic = /rsi|move.?37|strategic|council|sovereign|frontier|high novelty/i.test(q);
    if(requested!=='auto') return requested;
    if(strategic || risk==='CRITICAL') return 'council';
    if(high) return 'hybrid';
    if(/human|judgment|publication|claim/i.test(q) && !/schema|route|docket completeness|boundary/i.test(q)) return 'human';
    return 'node';
  }
  function gate(name, state, detail){return {name,state,ok:state==='PASS'||state==='WARN',detail}}
  let packet=null;
  function run(modeOverride){
    const q=($('#objective').value||'').trim(); const requested=modeOverride||$('#authorityMode').value; const risk=$('#riskClass').value; const target=$('#targetType').value; const intent=classify(q); const bad=sensitive();
    const hasObjective=q.length>=24; const publicSafe=!bad; const fundsOk=!/(funds|wallet|transaction|trade|investment|custody|liquidity)/i.test(q)||/(no funds|no wallet|no transaction|not available|boundary)/i.test(q); const evidenceHint=/(proof|evidence|docket|review|validate|contract|route|boundary|mission|replay|baseline|attestation)/i.test(q);
    const auth=recommendedAuthority(q,requested,risk,target); const highRisk=risk==='HIGH'||risk==='CRITICAL'||/external action|production/i.test(target)||/deploy|release|security posture|legal|financial/i.test(q);
    const nodeEligible=hasObjective&&publicSafe&&fundsOk&&evidenceHint&&!highRisk;
    let decision='VALIDATION_PACKET_READY';
    if(!publicSafe||!fundsOk) decision='BLOCK_BOUNDARY'; else if(auth==='node'&&!nodeEligible) decision='ESCALATE_TO_HUMAN'; else if(auth==='node') decision='AGI_NODE_VALIDATION_READY'; else if(auth==='human') decision='HUMAN_REVIEW_READY'; else if(auth==='hybrid') decision='HYBRID_VALIDATION_READY'; else if(auth==='council') decision='COUNCIL_REVIEW_READY';
    const gates=[
      gate('Bounded objective', hasObjective?'PASS':'FAIL', 'A usable validation needs a specific public-safe objective or claim.'),
      gate('Public/private boundary', publicSafe?'PASS':'FAIL', 'No private data, credentials, customer material, wallet secrets, or confidential work.'),
      gate('No funds / wallet / transaction', fundsOk?'PASS':'FAIL', 'The site does not process funds, wallets, trades, custody, or transactions.'),
      gate('Evidence path present', evidenceHint?'PASS':'WARN', 'Strong validation should route to proof, docket, replay, baseline, or boundary evidence.'),
      gate('Authority fit', (auth==='node'?nodeEligible:true)?'PASS':'WARN', 'AGI Node is for deterministic public-safe checks; humans/council handle judgment and high impact.'),
      gate('Human escalation preserved', (!highRisk||auth!=='node')?'PASS':'WARN', 'High-impact or sensitive validation escalates to human or council review.'),
      gate('Challenge window / rollback noted', /challenge|rollback|review|docket|certificate|attestation/i.test(q)?'PASS':'WARN', 'Important promotions need challenge windows, rollback, or explicit review notes.'),
      gate('Claim boundary visible', /boundary|no data|no funds|no wallet|no transaction|claim/i.test(q)?'PASS':'WARN', 'Public-facing validation should state what is not claimed.')
    ];
    const pass=gates.filter(g=>g.state==='PASS').length; const readiness=Math.max(0,Math.min(100,Math.round(pass/gates.length*100)));
    const selectedRoutes=bestRoutes(q);
    packet={schema:'goalos.validation_mesh.v29', generatedAt:new Date().toISOString(), validationId:digest(q+auth+risk+target), objective:q, requestedAuthority:requested, selectedAuthority:auth, riskClass:risk, targetType:target, intent, decision, readiness, gates, routes:selectedRoutes.map(r=>({title:r.title,url:r.url,description:r.description})), boundary:{userData:false,userFunds:false,wallet:false,transaction:false,networkCall:false,productionAuthority:false,humanReviewRequired:auth!=='node'||highRisk}, attestations:{node:{allowed:nodeEligible, profile:'AGI-NODE-BROWSER-LOCAL-V29', digest:digest(q+'node')}, human:{required:auth==='human'||auth==='hybrid'||auth==='council'||highRisk, digest:digest(q+'human')}, council:{required:auth==='council', quorum:'architect-validator-council', digest:digest(q+'council')}}};
    render(packet);
  }
  function render(p){
    $('#authorityBadge').textContent=p.selectedAuthority.toUpperCase(); $('#decisionState').textContent=p.decision; $('#boundaryState').textContent=p.decision==='BLOCK_BOUNDARY'?'blocked':'preserved'; $('#readiness').textContent=p.readiness; $('.v29-dial').style.setProperty('--p',p.readiness+'%');
    $('#consoleLog').textContent=`validation: ${p.validationId}\nauthority: ${p.selectedAuthority}\nintent: ${p.intent}\ndecision: ${p.decision}\nnetwork calls: 0`;
    $('#gateSummary').textContent=`${p.gates.filter(g=>g.state==='PASS').length}/${p.gates.length} pass`;
    $('#gates').innerHTML=p.gates.map(g=>`<div class="v29-gate"><span><b>${g.name}</b><small>${g.detail}</small></span><b class="${g.state==='FAIL'?'fail':g.state==='WARN'?'warn':'pass'}">${g.state}</b></div>`).join('');
    $('#routes').innerHTML=p.routes.map(r=>`<div class="v29-route"><span><h4>${r.title}</h4><p>${r.description}</p></span><a href="${r.url}">Open →</a></div>`).join('');
    $('#explain').textContent = p.selectedAuthority==='node' ? 'AGI Node can validate this as a public-safe deterministic check. Human review remains available.' : p.selectedAuthority==='human' ? 'Human review is the appropriate authority because judgment, publication, or high-impact context is involved.' : p.selectedAuthority==='hybrid' ? 'Hybrid mode lets the AGI Node prepare a deterministic precheck while a human reviewer remains the final authority.' : 'Council mode prepares an Architect / Validator Council packet for strategic or high-novelty validation.';
  }
  function download(kind){ if(!packet) run(); let name='goalos-validation'; let data=''; let type='application/json';
    if(kind==='certificate'){name='validation-certificate-v29.json';data=JSON.stringify(packet,null,2)}
    if(kind==='attestation'){name='validation-attestation-v29.json';data=JSON.stringify({validationId:packet.validationId,decision:packet.decision,authority:packet.selectedAuthority,attestations:packet.attestations,boundary:packet.boundary},null,2)}
    if(kind==='brief'){name='validation-reviewer-brief-v29.md';type='text/markdown';data=`# GoalOS Validation Brief V29\n\n## Objective\n${packet.objective}\n\n## Decision\n${packet.decision}\n\n## Authority\n${packet.selectedAuthority}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority.\n\n## Gates\n${packet.gates.map(g=>`- ${g.state}: ${g.name} — ${g.detail}`).join('\n')}\n\n## Routes\n${packet.routes.map(r=>`- [${r.title}](${r.url}) — ${r.description}`).join('\n')}\n`}
    if(kind==='matrix'){name='validation-authority-matrix-v29.csv';type='text/csv';data='authority,best_for,limits\nAGI Node,public-safe deterministic validation,not high-impact final authority\nHuman,judgment and publication decisions,manual review required\nHybrid,node precheck plus human signoff,slower but safer\nCouncil,strategic high-novelty RSI or institutional decisions,requires quorum\n'}
    if(kind==='graph'){name='validation-action-graph-v29.csv';type='text/csv';data='step,action,owner,status\n1,Check public/private boundary,GoalOS,done\n2,Select authority,GoalOS,done\n3,Run deterministic gates,AGI Node,ready\n4,Prepare reviewer packet,GoalOS,ready\n5,Human or council final decision,Reviewer,pending\n6,Route to proof surface,User,ready\n'}
    if(kind==='nodehandoff'){name='agi-node-validation-handoff-v29.json';data=JSON.stringify({validationId:packet.validationId,nodeProfile:'AGI-NODE-HANDOFF-V29',objective:packet.objective,allowedChecks:['schema','route_fit','boundary','docket_completeness','replay_readiness','claim_boundary'],prohibited:['wallet','transaction','private_data','external_action_without_human_review'],decision:packet.decision},null,2)}
    const blob=new Blob([data],{type}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; a.click(); URL.revokeObjectURL(a.href);
  }
  function chatAnswer(q){const l=q.toLowerCase(); let chosen=bestRoutes(q)[0]||routes[0]; let answer='I can route you to the closest public proof surface. '; if(l.includes('node')||l.includes('validate')) answer='AGI Node validation is best for public-safe deterministic checks. Human or council review is required for high-impact, sensitive, or final authority decisions. '; if(l.includes('human')) answer='Human review is appropriate for judgment-heavy, high-impact, publication, legal, financial, security, or external-action decisions. '; if(l.includes('contract')||l.includes('48')) answer='The 48 Mainnet contracts are best explored through the Mainnet Contract Atlas and Proof Rail. '; if(l.includes('token')||l.includes('agialpha')) answer='$AGIALPHA is public contract identification only here; not available from GoalOS, no sale, no custody, no wallet support, and no investment advice. '; if(l.includes('data')||l.includes('privacy')) answer='GoalOS public demos are browser-local and do not ask for user data, user funds, wallets, transactions, or production authority. '; return {answer,route:chosen}; }
  function maybeOpen(q,url){ if(/\b(open|go|show|launch|redirect|take me)\b/i.test(q)) location.href=url; }
  function addMsg(text,cls){const div=document.createElement('div'); div.className='v29-msg '+cls; div.textContent=text; $('#chatLog').appendChild(div); $('#chatLog').scrollTop=$('#chatLog').scrollHeight;}
  function init(){
    $('#runBtn')?.addEventListener('click',()=>run()); $('#nodeBtn')?.addEventListener('click',()=>{ $('#authorityMode').value='node'; run('node')}); $('#humanBtn')?.addEventListener('click',()=>{ $('#authorityMode').value='human'; run('human')});
    $$('.v29-mode').forEach(btn=>btn.addEventListener('click',()=>{$('#authorityMode').value=btn.dataset.mode; run(btn.dataset.mode)}));
    $$('[data-download]').forEach(btn=>btn.addEventListener('click',()=>download(btn.dataset.download)));
    $('#playbooks').innerHTML=playbooks.map((p,i)=>`<button class="v29-playbook" data-i="${i}"><b>${i+1}. ${p[0]}</b><small>${p[1]}</small></button>`).join('');
    $$('.v29-playbook').forEach(btn=>btn.addEventListener('click',()=>{const p=playbooks[Number(btn.dataset.i)]; $('#objective').value=p[1]; $('#authorityMode').value=p[2]; run(p[2]); window.scrollTo({top:document.querySelector('.v29-composer').offsetTop-20,behavior:'smooth'});}));
    $('#examplesBtn')?.addEventListener('click',()=>document.getElementById('use-cases')?.scrollIntoView({behavior:'smooth'}));
    $('#chatToggle')?.addEventListener('click',()=>{const p=$('#chatPanel'); p.hidden=!p.hidden});
    $('#chatForm')?.addEventListener('submit',(e)=>{e.preventDefault(); const q=$('#chatInput').value.trim(); if(!q)return; addMsg(q,'user'); const a=chatAnswer(q); addMsg(a.answer+'Best route: '+a.route.title+' → '+a.route.url,'bot'); maybeOpen(q,a.route.url); $('#chatInput').value='';});
    document.addEventListener('keydown',e=>{ if(e.key==='/' && !/textarea|input|select/i.test(document.activeElement.tagName)){e.preventDefault(); $('#chatPanel').hidden=false; $('#chatInput').focus();}});
    run();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
