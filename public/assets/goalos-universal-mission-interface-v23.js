
(function(){
  'use strict';
  const routes = (window.GOALOS_V23_ROUTES || []).slice();
  const routeByHref = Object.fromEntries(routes.map(r => [r.href, r]));
  const intents = [
    {id:'contracts', label:'48 Mainnet contracts', state:'CONTRACT_ATLAS_READY', keys:['contract','contracts','mainnet','ethereum','chain','atlas','etherscan','agialpha'], routes:['mainnet-contract-atlas.html','mainnet-proof-rail.html','contract-academy.html','token-boundary.html']},
    {id:'proof', label:'Proof Run / Evidence Docket', state:'PROOF_MISSION_REVIEW_READY', keys:['proof','docket','evidence','mission','run','validator','validate','review'], routes:['proof-run-001-docket.html','proof-run-001.html','evidence-docket-theatre.html','validator-room.html']},
    {id:'rsi', label:'Loop → RSI governance', state:'RSI_GOVERNANCE_PATH_READY', keys:['rsi','loop','omni','move','move-37','baseline','breakthrough','dossier','state capacity'], routes:['from-loop-to-rsi-state-capacity.html','from-loop-to-rsi-sovereign-console.html','from-loop-to-rsi-governance.html','loop-bottleneck-observatory.html']},
    {id:'trust', label:'Trust / Privacy / Token Boundary', state:'BOUNDARY_REVIEW_READY', keys:['privacy','data','token','wallet','fund','funds','agialpha','legal','terms','trust','boundary','safe'], routes:['trust-boundary.html','token-boundary.html','no-data-no-funds.html','privacy.html','data-boundary.html']},
    {id:'start', label:'New user onboarding', state:'START_PATH_READY', keys:['start','begin','new','learn','understand','intro','quick','what is','guide'], routes:['start-here.html','pathfinder.html','demo-ecosystem-registry.html','site-map.html']},
    {id:'build', label:'Build / Developer path', state:'BUILD_PATH_READY', keys:['github','repo','workflow','action','run','developer','docs','local','repository'], routes:['docs.html','run-locally.html','repository-map.html','website-autopilot.html','site-health.html']},
  ];
  const risky = ['private key','seed phrase','password','secret','credential','customer data','personal data','user funds','wallet','buy','sell','trade','investment advice','tax advice','legal advice','medical advice','payment'];
  const qs = s => document.querySelector(s);
  const qsa = s => Array.from(document.querySelectorAll(s));
  let currentMission = null;
  let currentMode = 'simple';
  function scoreIntent(text, intent){ const t=text.toLowerCase(); let score=0; intent.keys.forEach(k => { if(t.includes(k)) score += k.length > 6 ? 3 : 2; }); return score; }
  function pickIntent(text){ const ranked=intents.map(i=>[scoreIntent(text,i),i]).sort((a,b)=>b[0]-a[0]); return ranked[0][0] ? ranked[0][1] : intents[4]; }
  function routeObjects(intent){ return intent.routes.map(h => routeByHref[h] || {href:h,title:h.replace(/[-.]/g,' '),category:intent.label,description:'Open the relevant GoalOS route.'}).slice(0,4); }
  function boundaryFlags(text){ const t=text.toLowerCase(); return risky.filter(x => t.includes(x)); }
  function missionId(text){ let h=0; for(let i=0;i<text.length;i++){ h=((h<<5)-h)+text.charCodeAt(i); h|=0; } return 'GOALOS-MISSION-' + Math.abs(h).toString(16).toUpperCase().padStart(8,'0').slice(0,8); }
  function now(){ return new Date().toISOString(); }
  function buildMission(text){
    const objective = (text || '').trim() || 'I want to understand GoalOS and choose the right proof path.';
    const intent = pickIntent(objective);
    const flags = boundaryFlags(objective);
    const routes = routeObjects(intent);
    const state = flags.length ? 'HOLD_BOUNDARY_REWRITE_REQUIRED' : intent.state;
    return {version:'v23',mission_id:missionId(objective),generated_at:now(),objective,intent:intent.id,intent_label:intent.label,decision_state:state,boundary_flags:flags,boundary:'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.',routes,mission_contract:{objective,success_criteria:['User receives a clear proof path','Relevant pages are opened before trust is assumed','Any claim is tied to evidence or boundary language'],failure_criteria:['Sensitive data requested','Wallet or transaction requested','Unsupported empirical claim requested'],risk_class:flags.length?'BOUNDARY_REVIEW':'PUBLIC_SAFE',human_review_required:true},claims_matrix:[{claim:'GoalOS can route this objective to public proof surfaces',evidence:'local route index + deterministic intent map',status:'supported locally'},{claim:'This public demo executes production actions',evidence:'not applicable',status:'not claimed'}],evidence_docket_plan:['Mission Contract','Claims Matrix','Route Map','Reviewer Brief','Action Graph','Chronicle Stub','Capability Package Stub'],action_graph:[['Objective','Mission Contract'],['Mission Contract','Evidence Docket Plan'],['Evidence Docket Plan','Route Recommendation'],['Route Recommendation','Human Review']],chronicle_stub:{entry:'Objective converted into public-safe mission package',memory:'browser-local only'},capability_package_stub:{name:intent.label,scope:'public-safe navigation and mission planning'}};
  }
  function setSteps(n){ qsa('.g23-step').forEach((el,i)=>el.classList.toggle('active',i<=n)); }
  function renderMission(m){
    currentMission=m; setSteps(m.boundary_flags.length?1:6);
    const state = qs('#g23-state'); if(state) state.textContent = `mission: ${m.mission_id}\nintent: ${m.intent_label}\nstate: ${m.decision_state}\nboundary flags: ${m.boundary_flags.length ? m.boundary_flags.join(', ') : 'none'}\nexternal actions: 0`;
    const answer = qs('#g23-answer');
    if(answer){
      const modeText = currentMode === 'executive' ? 'Executive path: review the recommended route and download the brief before making decisions.' : currentMode === 'builder' ? 'Builder path: inspect the generated Mission Contract, Action Graph, and route matrix.' : currentMode === 'reviewer' ? 'Reviewer path: verify boundaries, claims, evidence, and next route before trusting the result.' : 'GoalOS created a public-safe proof path from your objective.';
      answer.innerHTML = `<h3>${m.boundary_flags.length ? 'Boundary review needed' : 'Mission package ready'}</h3><p>${modeText}</p><div class="g23-routes">${m.routes.map(r=>`<a class="g23-route" href="${r.href}"><div><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.description||r.category||'GoalOS route')}</small></div><span>Open →</span></a>`).join('')}</div>`;
    }
    const open = qs('#g23-open-next'); if(open){ open.disabled=false; open.textContent='Open next best page'; }
  }
  function escapeHtml(s){ return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
  function download(name, type, content){ const blob = new Blob([content],{type}); const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{ URL.revokeObjectURL(a.href); a.remove(); },300); }
  function missionMarkdown(m){ return `# GoalOS Mission Brief\n\nMission: ${m.mission_id}\n\nObjective: ${m.objective}\n\nDecision state: ${m.decision_state}\n\nBoundary: ${m.boundary}\n\n## Recommended routes\n${m.routes.map(r=>`- ${r.title}: ${r.href}`).join('\n')}\n\n## Evidence Docket Plan\n${m.evidence_docket_plan.map(x=>`- ${x}`).join('\n')}\n`; }
  function actionCsv(m){ return 'from,to\n' + m.action_graph.map(r => r.map(x => '"'+String(x).replace(/"/g,'""')+'"').join(',')).join('\n') + '\n'; }
  function initOneBox(){
    const input=qs('#g23-objective');
    const generate=qs('#g23-generate');
    const simulate=qs('#g23-simulate');
    if(generate) generate.addEventListener('click',()=>{ renderMission(buildMission(input && input.value)); });
    if(simulate) simulate.addEventListener('click',()=>{ const m=buildMission(input && input.value); renderMission(m); let i=0; const timer=setInterval(()=>{ setSteps(i++); if(i>6){clearInterval(timer); renderMission(m);} },260); });
    qsa('[data-g23-suggest]').forEach(b=>b.addEventListener('click',()=>{ if(input){input.value=b.getAttribute('data-g23-suggest'); input.focus(); renderMission(buildMission(input.value)); }}));
    qsa('[data-g23-mode]').forEach(b=>b.addEventListener('click',()=>{ currentMode=b.getAttribute('data-g23-mode'); qsa('[data-g23-mode]').forEach(x=>x.classList.toggle('active',x===b)); if(currentMission) renderMission(currentMission); }));
    qsa('[data-g23-download]').forEach(b=>b.addEventListener('click',()=>{ const m=currentMission || buildMission(input && input.value); const kind=b.getAttribute('data-g23-download'); if(kind==='json') download(`${m.mission_id}.json`,'application/json',JSON.stringify(m,null,2)); if(kind==='md') download(`${m.mission_id}-reviewer-brief.md`,'text/markdown',missionMarkdown(m)); if(kind==='csv') download(`${m.mission_id}-action-graph.csv`,'text/csv',actionCsv(m)); }));
    const open=qs('#g23-open-next'); if(open) open.addEventListener('click',()=>{ const m=currentMission || buildMission(input && input.value); window.location.href = (m.routes[0] && m.routes[0].href) || 'site-map.html'; });
    if(input){ input.addEventListener('keydown', ev => { if((ev.metaKey || ev.ctrlKey) && ev.key === 'Enter') renderMission(buildMission(input.value)); }); }
  }
  function initModal(){
    const modal=qs('#g23-allpages-modal'); const list=qs('#g23-allpages-list'); const filter=qs('#g23-allpages-filter');
    function render(q=''){ if(!list) return; const s=q.toLowerCase(); list.innerHTML=routes.filter(r => !r.system && (`${r.title} ${r.href} ${r.category} ${r.description}`).toLowerCase().includes(s)).slice(0,300).map(r=>`<div class="g23-row"><small>${escapeHtml(r.category)}</small><div><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.description)}</small></div><a href="${r.href}">Open</a></div>`).join('') || '<p>No route found.</p>'; }
    qsa('[data-g23-open-pages]').forEach(b=>b.addEventListener('click',e=>{ e.preventDefault(); if(modal){modal.classList.add('open'); render(''); if(filter) filter.focus(); }}));
    qsa('[data-g23-close]').forEach(b=>b.addEventListener('click',()=>modal&&modal.classList.remove('open')));
    if(filter) filter.addEventListener('input',()=>render(filter.value));
  }
  function initSlash(){ document.addEventListener('keydown', ev => { if(ev.key === '/' && !['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){ ev.preventDefault(); const modal=qs('#g23-allpages-modal'); if(modal){ modal.classList.add('open'); const f=qs('#g23-allpages-filter'); if(f) f.focus(); } else { window.location.href='goalos.html'; } } }); }
  function init(){ initOneBox(); initModal(); initSlash(); const defaultObjective='I am new and want the fastest path to understand GoalOS.'; if(qs('#g23-objective') && !qs('#g23-objective').value){ renderMission(buildMission(defaultObjective)); } }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
