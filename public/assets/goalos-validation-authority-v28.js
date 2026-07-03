(()=>{
  const $ = (q)=>document.querySelector(q);
  const $$ = (q)=>Array.from(document.querySelectorAll(q));
  const routes = window.GOALOS_VALIDATION_ROUTES_V28 || [];
  const forbiddenTerms = ['seed phrase','private key','password','secret key','customer data','personal data','passport','credit card','bank account','wire transfer','wallet connect','connect wallet','transaction','trade','investment advice','legal advice','medical advice','exploit','malware','phishing'];
  let lastPacket = null;
  function hash(s){let h=2166136261>>>0; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i); h=Math.imul(h,16777619);} return 'GOALOS-'+(h>>>0).toString(16).toUpperCase().padStart(8,'0');}
  function text(){return ($('#objective')?.value||'').trim();}
  function lower(){return text().toLowerCase();}
  function isSensitive(){const l=lower(); return forbiddenTerms.some(t=>l.includes(t));}
  function routeScore(r,q){const l=q.toLowerCase(); let score=0; r.keywords.forEach(k=>{ if(l.includes(k)) score+=3; }); if(l.includes((r.title||'').toLowerCase().split(' ')[0])) score+=1; return score;}
  function bestRoutes(q){return routes.map(r=>({...r,score:routeScore(r,q)})).sort((a,b)=>b.score-a.score).filter((r,i)=>r.score>0||i<3).slice(0,4);}
  function gate(name, ok, detail, forceWarn){return {name, ok, detail, state: ok ? (forceWarn?'WARN':'PASS') : 'FAIL'};}
  function classify(){const q=lower(); if(q.includes('contract')||q.includes('mainnet')||q.includes('ethereum')) return 'CONTRACT_ATLAS'; if(q.includes('rsi')||q.includes('loop')||q.includes('omni')) return 'LOOP_RSI'; if(q.includes('privacy')||q.includes('data')||q.includes('token')||q.includes('wallet')) return 'BOUNDARY_REVIEW'; if(q.includes('proof')||q.includes('docket')||q.includes('evidence')) return 'EVIDENCE_DOCKET'; return 'GENERAL_MISSION';}
  function validate(){
    const q=text(); const authority=$('#authority').value; const risk=$('#riskClass').value; const type=$('#claimType').value; const sensitive=isSensitive();
    const hasObjective=q.length>=18; const publicSafe=!sensitive; const noFunds=!/funds|wallet|transaction|trade|investment|custody/i.test(q) || /no funds|no wallet|no transaction|not available/i.test(q); const hasEvidence=/proof|evidence|docket|review|validate|contract|route|boundary|mission/i.test(q);
    const highRisk=(risk==='HIGH'||risk==='CRITICAL'||type==='External action request');
    const nodeEligible=hasObjective && publicSafe && noFunds && hasEvidence && !highRisk;
    const gates=[
      gate('Objective is specific enough',hasObjective,'GoalOS needs a bounded objective or claim.'),
      gate('Public/private proof boundary',publicSafe,'No private, customer, credential, wallet, or secret data.'),
      gate('No funds / no wallet / no transaction',noFunds,'The public site does not process funds, wallets, or transactions.'),
      gate('Evidence path present',hasEvidence,'Mission should produce or reference a docket, proof, route, or review artifact.'),
      gate('Risk class compatible with selected authority', authority==='node'?nodeEligible:true, authority==='node'?'AGI Node validates public-safe deterministic checks only.':'Human or hybrid can handle broader review.', authority==='hybrid'),
      gate('Human-review boundary preserved', authority!=='node'||!highRisk,'High-impact or sensitive claims remain human-review required.', authority==='node'&&!highRisk)
    ];
    let pass=gates.filter(g=>g.ok).length; let score=Math.round(pass/gates.length*100);
    let decision='READY_FOR_VALIDATION';
    if(!publicSafe || !noFunds) decision='BLOCK_BOUNDARY';
    else if(authority==='node' && !nodeEligible) decision='HOLD_HUMAN_REVIEW_REQUIRED';
    else if(authority==='node') decision='VALIDATED_BY_AGI_NODE';
    else if(authority==='human') decision='VALIDATED_BY_HUMAN';
    else decision='HYBRID_VALIDATION_READY';
    const intent=classify(); const chosen=bestRoutes(q);
    lastPacket={
      schema:'goalos.validation_authority.v28', generatedAt:new Date().toISOString(), missionId:hash(q+authority+risk), objective:q, authority, riskClass:risk, claimType:type, intent, decision, readiness:score,
      gates:gates.map(g=>({name:g.name,status:g.state,detail:g.detail})), routes:chosen.map(r=>({title:r.title,url:r.url,reason:r.description})),
      boundary:{userData:false,userFunds:false,wallet:false,transaction:false,externalCall:false,productionAuthority:false,humanReviewRequired:decision.includes('HUMAN')||authority!=='node'},
      attestation:{type:authority==='node'?'AGI_NODE_VALIDATION_ATTESTATION':authority==='human'?'HUMAN_REVIEW_DECISION':'HYBRID_VALIDATION_PACKET', validator:authority==='node'?'AGI-NODE-BROWSER-LOCAL-V28':'HUMAN-REVIEWER', digest:hash(JSON.stringify({q,authority,risk,type,decision}))}
    };
    render(lastPacket);
  }
  function render(p){
    $('#decisionState').textContent=p.decision; $('#scoreNum').textContent=p.readiness; $('.dial')?.style.setProperty('--pct',p.readiness); $('#authorityLabel').textContent=p.authority.replace('-', ' ').toUpperCase(); $('#gateSummary').textContent=`${p.gates.filter(g=>g.status==='PASS').length}/${p.gates.length} passed`;
    $('#miniConsole').textContent=`mission: ${p.missionId}\nintent: ${p.intent}\nauthority: ${p.authority}\nstate: ${p.decision}\nexternal actions: 0`;
    $('#gates').innerHTML=p.gates.map(g=>`<div class="gate ${g.status==='PASS'?'pass':g.status==='WARN'?'warn':'fail'}"><span><b>${escapeHtml(g.name)}</b><br><small>${escapeHtml(g.detail)}</small></span><b>${g.status}</b></div>`).join('');
    $('#routes').innerHTML=p.routes.map(r=>`<div class="route"><span><h4>${escapeHtml(r.title)}</h4><p>${escapeHtml(r.reason)}</p></span><a href="${escapeAttr(r.url)}">Open →</a></div>`).join('');
  }
  function escapeHtml(s){return String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
  function escapeAttr(s){return String(s).replace(/"/g,'&quot;');}
  function download(kind){ if(!lastPacket) validate(); const p=lastPacket; let name='goalos-validation-authority-v28'; let mime='application/json'; let body='';
    if(kind==='certificate'){name=`${p.missionId}-validation-certificate.json`; body=JSON.stringify(p,null,2);} 
    if(kind==='attestation'){name=`${p.missionId}-attestation.json`; body=JSON.stringify(p.attestation,null,2);} 
    if(kind==='brief'){name=`${p.missionId}-reviewer-brief.md`; mime='text/markdown'; body=`# GoalOS Validation Reviewer Brief\n\n**Mission:** ${p.missionId}\n\n**Authority:** ${p.authority}\n\n**Decision:** ${p.decision}\n\n## Objective\n${p.objective}\n\n## Gates\n${p.gates.map(g=>`- ${g.status}: ${g.name} — ${g.detail}`).join('\n')}\n\n## Recommended routes\n${p.routes.map(r=>`- [${r.title}](${r.url}) — ${r.reason}`).join('\n')}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No external call. No production authority. Human review required for high-impact outcomes.\n`;}
    if(kind==='graph'){name=`${p.missionId}-action-graph.csv`; mime='text/csv'; body='step,action,authority,artifact,next_state\n1,check boundary,'+p.authority+',boundary gate,'+p.decision+'\n2,select routes,'+p.authority+',route map,review\n3,emit certificate,'+p.authority+',validation certificate,download\n4,open next page,human,proof route,human review\n';}
    const blob=new Blob([body],{type:mime}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},0);
  }
  function ask(q){const l=q.toLowerCase(); let answer='I found the closest GoalOS proof routes. Use the route cards below, or type “open” with the page you want.'; if(l.includes('node')||l.includes('validate')) answer='AGI Node validation is available for public-safe deterministic checks: schema, boundary, route fit, docket completeness, replay readiness, and no-wallet/no-funds constraints. High-impact or sensitive claims stay human-review required.'; if(l.includes('human')) answer='Human validation remains the correct authority for high-impact, sensitive, legal, financial, security, external-action, or final publication decisions.'; if(l.includes('48')||l.includes('contract')) answer='The 48-contract route is the Mainnet Contract Atlas. GoalOS can generate a validation packet for contract-understanding or contract-review missions.'; if(l.includes('data')||l.includes('privacy')||l.includes('wallet')||l.includes('token')) answer='The trust and token boundary pages explain that GoalOS does not want user data, does not handle user funds, and does not provide wallet or transaction services.'; const cards=bestRoutes(q); addMsg(answer,cards,'bot'); const shouldOpen=/\b(open|go|show|take me|launch|redirect)\b/i.test(q); if(shouldOpen && cards[0]) setTimeout(()=>{location.href=cards[0].url},500);}
  function addMsg(text,cards,who){const log=$('#chatLog'); const div=document.createElement('div'); div.className='msg '+who; div.innerHTML=escapeHtml(text)+(cards&&cards.length?'<div class="routes">'+cards.slice(0,3).map(r=>`<div class="route"><span><h4>${escapeHtml(r.title)}</h4><p>${escapeHtml(r.description)}</p></span><a href="${escapeAttr(r.url)}">Open →</a></div>`).join('')+'</div>':''); log.appendChild(div); log.scrollTop=log.scrollHeight;}
  $('#validateBtn')?.addEventListener('click',validate); $('#packetBtn')?.addEventListener('click',()=>{validate(); download('certificate');}); $('#sampleBtn')?.addEventListener('click',()=>{$('#objective').value='I want the AGI Node to validate whether this public-safe Evidence Docket route is complete, claim-bounded, replayable, and ready for human review.'; validate();});
  $$('[data-download]').forEach(b=>b.addEventListener('click',()=>download(b.dataset.download))); $$('[data-fill]').forEach(c=>c.addEventListener('click',()=>{$('#authority').value=c.dataset.fill; validate();}));
  $('#askToggle')?.addEventListener('click',()=>{$('#chatPanel').hidden=!$('#chatPanel').hidden;}); $('#chatForm')?.addEventListener('submit',e=>{e.preventDefault(); const q=$('#chatInput').value.trim(); if(!q) return; addMsg(q,null,'user'); $('#chatInput').value=''; ask(q);}); document.addEventListener('keydown',e=>{if(e.key==='/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)){e.preventDefault(); $('#chatPanel').hidden=false; $('#chatInput')?.focus();}});
  validate();
})();