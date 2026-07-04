(function(){
  'use strict';
  const $ = (q, root=document) => root.querySelector(q);
  const $$ = (q, root=document) => Array.from(root.querySelectorAll(q));
  const routes = Array.isArray(window.GOALOS_VALIDATION_ROUTES) ? window.GOALOS_VALIDATION_ROUTES : [];
  const routeByUrl = Object.fromEntries(routes.map(r => [r.url, r]));
  const defaults = {
    contracts: ['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','token-boundary.html'],
    proof: ['proof-run-001-docket.html','demo-ecosystem-registry.html','evidence-docket-theatre.html','site-health.html'],
    rsi: ['from-loop-to-rsi-state-capacity.html','from-loop-to-rsi-sovereign-console.html','from-loop-to-rsi-governance.html','loop-bottleneck-observatory.html'],
    trust: ['trust-boundary.html','token-boundary.html','privacy.html','data-boundary.html','no-data-no-funds.html'],
    start: ['goalos.html','start-here.html','pathfinder.html','use-case-playbooks.html','site-map.html'],
    validation: ['validation-studio.html','validation-mesh.html','validation-authority.html','proof-run-001-docket.html']
  };
  const playbooks = [
    {title:'AGI Node validates a public proof route', authority:'agi-node', text:'Validate that a public-safe Evidence Docket route for the 48 Ethereum Mainnet contracts is complete, claim-bounded, replay-ready, and ready for AGI Node precheck.', why:'Fast deterministic precheck for route, schema, replay, boundary, and docket completeness.', gate:'AGI_NODE_VALIDATION_READY'},
    {title:'Human validates a public claim', authority:'human', text:'Prepare human review for a high-impact public claim before publication. Check evidence, claim boundary, legal/financial/security wording, and human approval path.', why:'High-impact public claims need judgment, responsibility, and final human approval.', gate:'HUMAN_REVIEW_READY'},
    {title:'Hybrid review for Loop → RSI', authority:'hybrid', text:'Prepare hybrid validation for a Loop to RSI governance review packet: AGI Node precheck first, then human final review before public promotion.', why:'Combines deterministic precheck with human review for strategic governance.', gate:'HYBRID_VALIDATION_READY'},
    {title:'Council review for Move‑37', authority:'council', text:'Prepare Architect / Validator Council review for a Move‑37 candidate: reproduction, stress testing, persistence gate, baseline comparison, and dossier packaging.', why:'Novelty raises proof burden; council review handles strategic, high-novelty claims.', gate:'COUNCIL_REVIEW_READY'},
    {title:'Validate token boundary', authority:'agi-node', text:'Validate the $AGIALPHA token boundary page: public contract identification only, not available from GoalOS, no sale, no custody, no wallet support, no investment advice.', why:'A deterministic wording and route consistency check.', gate:'AGI_NODE_VALIDATION_READY'},
    {title:'Validate the 48-contract atlas', authority:'hybrid', text:'Validate whether the Mainnet Contract Atlas clearly explains the 48 GoalOS-created Ethereum Mainnet contracts to non-technical users while preserving token and production boundaries.', why:'AGI Node checks coverage and routes; human checks clarity and presentation.', gate:'HYBRID_VALIDATION_READY'},
    {title:'Evidence Docket completeness', authority:'agi-node', text:'Check an Evidence Docket for manifest, claims matrix, environment, baselines, proof packets, evaluator notes, selection certificate, safety ledger, replay path, and claim boundary.', why:'Docket completeness is a deterministic checklist before review.', gate:'AGI_NODE_VALIDATION_READY'},
    {title:'Controlled pilot program', authority:'hybrid', text:'Validate a controlled pilot program: bounded mission, success criteria, baseline, execution record, validator decision, follow-up status, and post-pilot acceptance record.', why:'Pilots should end with a docket, not a vague success claim.', gate:'HYBRID_VALIDATION_READY'},
    {title:'AI vendor evidence review', authority:'human', text:'Prepare human review of an AI vendor or tool using evidence, not marketing claims: supported claims, contradictions, risks, proof gaps, and next diligence steps.', why:'Vendor decisions are judgment-heavy and can involve legal, financial, or operational risk.', gate:'HUMAN_REVIEW_READY'},
    {title:'Defensive cybersecurity proof mission', authority:'hybrid', text:'Validate a defensive cybersecurity proof mission for repo-owned, sandbox-only work with no external scans, no exploit execution, no malware generation, and human review before remediation.', why:'Safety-sensitive defensive work needs AGI Node precheck plus human authority.', gate:'HYBRID_VALIDATION_READY'},
    {title:'Website route integrity', authority:'agi-node', text:'Validate website route integrity: all public pages are present, no broken internal HTML links, all pages route back to Tell GoalOS, Ask GoalOS, All Pages, and Search.', why:'A deterministic site-health check is ideal for AGI Node validation.', gate:'AGI_NODE_VALIDATION_READY'},
    {title:'Strategic opportunity proof mission', authority:'council', text:'Map a strategic opportunity into a proof mission with evidence requirements, risk gates, baseline comparisons, reviewer responsibilities, and council escalation if high impact.', why:'Strategic opportunities need institutional review and clear proof burden.', gate:'COUNCIL_REVIEW_READY'},
    {title:'Procurement proof record', authority:'human', text:'Create a proof-backed procurement review record with claims, evidence, risks, counterclaims, evaluation criteria, approval path, and rollback plan.', why:'Procurement affects budgets and obligations; human review is required.', gate:'HUMAN_REVIEW_READY'},
    {title:'Capability reuse validation', authority:'hybrid', text:'Validate whether accepted work can become reusable capability: proof history, transfer conditions, rollback target, scope, and future mission fit.', why:'AGI Node checks artifact structure; human checks strategic reuse.', gate:'HYBRID_VALIDATION_READY'},
    {title:'Claim-boundary audit', authority:'agi-node', text:'Validate a claim-boundary page for unsupported AGI/ASI/SOTA/production/investment/legal claims and confirm public-alpha boundary is visible.', why:'Claim-boundary checks are deterministic and public-safe.', gate:'AGI_NODE_VALIDATION_READY'},
    {title:'Council session prep', authority:'council', text:'Prepare a Validator Council review session with agenda, artifact packet, dissent questions, challenge window, decision standard, and escalation path.', why:'Council review creates durable authority for consequential validation.', gate:'COUNCIL_REVIEW_READY'}
  ];
  let selectedMode = 'auto';
  let lastPackage = null;
  function classify(text, forced){
    const t=(text||'').toLowerCase();
    const boundaryWords=['private key','seed phrase','password','credential','customer data','personal data','confidential','trade secret','payment','wallet','funds','bank','medical record'];
    const blocked=boundaryWords.some(w=>t.includes(w));
    const council=/move.?37|rsi|recursive|sovereign|strategic|council|high novelty|architect|breakthrough|state capacity/.test(t);
    const human=/legal|financial|investment|security posture|publication|public claim|procurement|vendor|external action|production|approve|approval|high-impact|high impact/.test(t);
    const node=/schema|route|docket|replay|contract|token|privacy|boundary|site map|link|sitemap|claim-boundary|claim boundary/.test(t);
    let authority='AGI Node validator', mode='agi-node', decision='AGI_NODE_VALIDATION_READY';
    if(blocked){authority='Boundary block'; mode='blocked'; decision='BLOCK_BOUNDARY';}
    else if(forced && forced!=='auto'){
      mode=forced; authority=label(forced); decision=forced==='human'?'HUMAN_REVIEW_READY':forced==='hybrid'?'HYBRID_VALIDATION_READY':forced==='council'?'COUNCIL_REVIEW_READY':'AGI_NODE_VALIDATION_READY';
    } else if(council){authority='Architect / Validator Council'; mode='council'; decision='COUNCIL_REVIEW_READY';}
    else if(human && node){authority='Hybrid: AGI Node + Human'; mode='hybrid'; decision='HYBRID_VALIDATION_READY';}
    else if(human){authority='Human reviewer'; mode='human'; decision='HUMAN_REVIEW_READY';}
    else {authority='AGI Node validator'; mode='agi-node'; decision='AGI_NODE_VALIDATION_READY';}
    const intent = /contract|48|mainnet|ethereum/.test(t) ? 'contracts' : /rsi|loop|move|recursive/.test(t) ? 'rsi' : /token|privacy|data|wallet|fund|boundary/.test(t) ? 'trust' : /proof|docket|evidence|claim/.test(t) ? 'proof' : 'validation';
    return {blocked, authority, mode, decision, intent};
  }
  function label(mode){return mode==='human'?'Human reviewer':mode==='hybrid'?'Hybrid: AGI Node + Human':mode==='council'?'Architect / Validator Council':'AGI Node validator';}
  function recommendedRoutes(intent, mode){
    let urls=[...(defaults[intent]||defaults.validation)];
    if(mode==='human') urls.unshift('proof-run-001-docket.html','trust-boundary.html');
    if(mode==='council') urls.unshift('from-loop-to-rsi-state-capacity.html','validation-studio.html');
    if(mode==='hybrid') urls.unshift('validation-studio.html','proof-run-001-docket.html');
    return [...new Set(urls)].map(u=> routeByUrl[u] || {title:u.replace(/\.html$/,'').replace(/-/g,' ').replace(/\b\w/g,c=>c.toUpperCase()),url:u,description:'Open this GoalOS route.',category:'GoalOS'}).slice(0,6);
  }
  function gatesFor(mode, blocked){
    const base=[['Public/private boundary', !blocked], ['No user data / no funds / no wallet', !blocked], ['Evidence Docket completeness', true], ['Claim-boundary check', true], ['Replay or route readiness', true]];
    if(mode==='human') base.push(['Human authority selected', true], ['AGI Node cannot finalize alone', true]);
    if(mode==='agi-node') base.push(['Deterministic public-safe checks only', true], ['Escalate high-impact claims', true]);
    if(mode==='hybrid') base.push(['AGI Node precheck', true], ['Human final review', true]);
    if(mode==='council') base.push(['Council packet required', true], ['Move‑37 / strategic dossier standard', true]);
    if(blocked) base.push(['Sensitive input blocked', false]);
    return base;
  }
  function buildPackage(){
    const text=$('#validationInput').value.trim();
    const c=classify(text, selectedMode);
    const recs=recommendedRoutes(c.intent, c.mode);
    const gates=gatesFor(c.mode,c.blocked);
    const id='GOALOS-VALIDATION-'+Math.random().toString(16).slice(2,10).toUpperCase();
    lastPackage={id,version:'v30',createdAt:new Date().toISOString(),request:text,authority:c.authority,mode:c.mode,decision:c.decision,intent:c.intent,boundary:{browserLocal:true,userData:false,userFunds:false,wallet:false,transaction:false,networkCall:false,productionAuthority:false},gates:gates.map(([name,pass])=>({name,pass})),routes:recs};
    renderPackage(lastPackage);
  }
  function renderPackage(pkg){
    $('#statusPill').textContent=pkg.decision.replace(/_.*/,'READY');
    $('#stateReadout').textContent=`mission: ${pkg.id}\nauthority: ${pkg.authority}\nstate: ${pkg.decision}\nboundary flags: none\nexternal actions: 0`;
    $('#decisionTitle').textContent=pkg.authority;
    $('#decisionSubtitle').textContent='GoalOS selected the validation authority and prepared a public-safe review packet.';
    $('#decisionBadge').textContent=pkg.decision;
    $('#whyBox').textContent=why(pkg);
    $('#gateList').innerHTML=pkg.gates.map(g=>`<div class="gate ${g.pass?'':'fail'}"><span>${esc(g.name)}</span><b>${g.pass?'PASS':'BLOCK'}</b></div>`).join('');
    $('#routeCards').innerHTML=pkg.routes.map(r=>`<article class="routeCard"><small>${esc(r.category||'GoalOS')}</small><h3>${esc(cleanTitle(r.title))}</h3><p>${esc(r.description||'Open this public GoalOS route.')}</p><a href="${esc(r.url)}">Open →</a></article>`).join('');
  }
  function why(pkg){
    if(pkg.decision==='BLOCK_BOUNDARY') return 'The request appears to include sensitive or prohibited input. Do not submit personal, customer, credential, wallet, payment, regulated, confidential, or trade-secret data through public demos.';
    if(pkg.mode==='agi-node') return 'AGI Node validation is appropriate because this looks like a public-safe deterministic check: schema, route, claim boundary, replay readiness, or Evidence Docket completeness.';
    if(pkg.mode==='human') return 'Human validation is appropriate because this appears judgment-heavy, high-impact, publication-related, legal/financial/security-related, or tied to final approval.';
    if(pkg.mode==='hybrid') return 'Hybrid validation is recommended: let the AGI Node precheck deterministic gates, then let a human make the final public or consequential decision.';
    if(pkg.mode==='council') return 'Council validation is recommended for Loop→RSI, Move‑37, strategic, high-novelty, or institutional promotion decisions. Novelty raises the burden of proof.';
    return 'GoalOS selected the safest appropriate authority path.';
  }
  function cleanTitle(s){return String(s||'GoalOS Route').replace(/\s+—\s+GoalOS.*$/,'');}
  function esc(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
  function download(kind){
    const pkg=lastPackage || (buildPackage(), lastPackage);
    let name='goalos-validation-certificate-v30.json', mime='application/json', body=JSON.stringify(pkg,null,2);
    if(kind==='attestation'){name='goalos-validation-attestation-v30.json'; body=JSON.stringify({attestationId:pkg.id+'-ATT',authority:pkg.authority,decision:pkg.decision,gates:pkg.gates,signature:'browser-local-demo'},null,2);}
    if(kind==='brief'){name='goalos-validation-reviewer-brief-v30.md'; mime='text/markdown'; body=`# GoalOS Validation Reviewer Brief V30\n\n**Request:** ${pkg.request}\n\n**Authority:** ${pkg.authority}\n\n**Decision:** ${pkg.decision}\n\n## Why\n${why(pkg)}\n\n## Gates\n${pkg.gates.map(g=>`- ${g.pass?'PASS':'BLOCK'} — ${g.name}`).join('\n')}\n\n## Recommended routes\n${pkg.routes.map(r=>`- [${cleanTitle(r.title)}](${r.url})`).join('\n')}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.\n`;}
    if(kind==='graph'){name='goalos-validation-action-graph-v30.csv'; mime='text/csv'; body='step,action,owner,status\n1,boundary check,GoalOS,done\n2,authority selection,GoalOS,done\n3,validation gates,'+pkg.authority+',ready\n4,review packet,GoalOS,ready\n5,next route,user,ready\n';}
    if(kind==='handoff'){name='goalos-agi-node-validation-handoff-v30.json'; body=JSON.stringify({handoffId:pkg.id+'-NODE',nodeRole:'validator',allowedChecks:['schema','route-fit','evidence-docket-completeness','claim-boundary','replay-readiness','token-boundary','site-route-integrity'],blockedChecks:['legal-advice','financial-advice','production-authorization','wallet-or-funds','private-data'],request:pkg.request},null,2);}
    if(kind==='council'){name='goalos-council-validation-packet-v30.md'; mime='text/markdown'; body=`# Architect / Validator Council Packet V30\n\n**Request:** ${pkg.request}\n\n**Decision state:** ${pkg.decision}\n\n## Council agenda\n1. Confirm public/private boundary.\n2. Confirm evidence burden.\n3. Confirm baselines and replay.\n4. Confirm rollback / challenge window.\n5. Record dissent and decision.\n\n## Dossier standard\nFor Move‑37 / RSI / strategic claims: reproduce, stress-test, persist, package dossier.\n`;}
    const blob=new Blob([body],{type:mime}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},1000);
  }
  function fillPlaybooks(){
    const grid=$('#playbookGrid'); if(!grid) return;
    grid.innerHTML=playbooks.map((p,i)=>`<article class="playbook"><small>${String(i+1).padStart(2,'0')} · ${esc(label(p.authority))}</small><h3>${esc(p.title)}</h3><p>${esc(p.why)}</p><button type="button" data-playbook="${i}">Use this</button></article>`).join('');
    grid.addEventListener('click',e=>{const b=e.target.closest('[data-playbook]'); if(!b) return; const p=playbooks[Number(b.dataset.playbook)]; $('#validationInput').value=p.text; selectedMode=p.authority; $$('.mode').forEach(x=>x.classList.toggle('active',x.dataset.mode===selectedMode)); buildPackage(); window.scrollTo({top:0,behavior:'smooth'});});
  }
  function askAnswer(q){
    const text=q.toLowerCase();
    let intent=/contract|48|mainnet|ethereum/.test(text)?'contracts':/rsi|loop|move|recursive/.test(text)?'rsi':/token|agialpha|wallet|fund|privacy|data/.test(text)?'trust':/proof|docket|evidence|claim/.test(text)?'proof':/human|node|validate|validator|authority/.test(text)?'validation':'start';
    const recs=recommendedRoutes(intent,'agi-node').slice(0,3);
    const wantsOpen=/\b(open|go|show|launch|redirect|take me)\b/.test(text);
    const answer=intent==='validation'?'Human, AGI Node, Hybrid, and Council validation are available. AGI Node handles deterministic public-safe checks; Human handles high-impact judgment; Hybrid combines both; Council handles strategic or RSI/Move‑37 cases.':intent==='contracts'?'The 48-contract path starts with the Mainnet Contract Atlas, then the proof rail and Contract Academy.':intent==='rsi'?'Loop → RSI governance uses deterministic artifacts, replay, baselines, persistence gates, and dossier packaging.':intent==='trust'?'GoalOS public demos are browser-local: no user data, no funds, no wallet, no transaction, no network call, and no production authority.':intent==='proof'?'Evidence Dockets are proof rooms: claims, baselines, proof packets, evaluator notes, risks, rollback, and replay path.':'Start with GoalOS, Pathfinder, or All Pages. You can type an objective and GoalOS will create the proof path.';
    if(wantsOpen && recs[0]) { location.href=recs[0].url; return 'Opening '+cleanTitle(recs[0].title)+'…'; }
    return answer+'\n\nSuggested routes: '+recs.map(r=>cleanTitle(r.title)).join(' · ');
  }
  function setupAsk(){
    const win=$('#askWindow'); const input=$('#askInput'); const log=$('#askLog');
    $$('[data-open-ask]').forEach(b=>b.addEventListener('click',()=>{win.hidden=false; input.focus();}));
    $('#closeAsk')?.addEventListener('click',()=>win.hidden=true);
    document.addEventListener('keydown',e=>{if(e.key==='/' && !['TEXTAREA','INPUT'].includes(document.activeElement.tagName)){e.preventDefault(); win.hidden=false; input.focus();}});
    $('#askForm')?.addEventListener('submit',e=>{e.preventDefault(); const q=input.value.trim(); if(!q) return; log.insertAdjacentHTML('beforeend',`<div class="user">${esc(q)}</div>`); const ans=askAnswer(q); log.insertAdjacentHTML('beforeend',`<div class="bot">${esc(ans).replace(/\n/g,'<br>')}</div>`); input.value=''; log.scrollTop=log.scrollHeight;});
  }
  $$('.mode').forEach(b=>b.addEventListener('click',()=>{selectedMode=b.dataset.mode; $$('.mode').forEach(x=>x.classList.toggle('active',x===b));}));
  $('#runValidation')?.addEventListener('click',buildPackage);
  $('#simulateNode')?.addEventListener('click',()=>{selectedMode='agi-node'; $$('.mode').forEach(x=>x.classList.toggle('active',x.dataset.mode==='agi-node')); buildPackage();});
  $('#openNext')?.addEventListener('click',()=>{const pkg=lastPackage || (buildPackage(),lastPackage); if(pkg.routes[0]) location.href=pkg.routes[0].url;});
  $$('[data-download]').forEach(b=>b.addEventListener('click',()=>download(b.dataset.download)));
  fillPlaybooks(); setupAsk(); buildPackage();
})();
