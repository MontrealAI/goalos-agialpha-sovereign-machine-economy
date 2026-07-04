(function(){
  const stages = ['Objective','Mission Contract','AGI Agents','AGI Job','AGI Node','ProofBundle','Evidence Docket','Validate','Chronicle','Reusable Capability'];
  const routes = window.GOALOS_V49_ROUTES || [];
  const qs = (s, r=document) => r.querySelector(s);
  const qsa = (s, r=document) => Array.from(r.querySelectorAll(s));
  function objective(){ return (qs('[data-v49-objective]')||{}).value || 'I want a public-safe GoalOS proof mission.'; }
  function log(text){ const box=qs('[data-v49-log]'); if(box) box.textContent=text; }
  function run(){
    const obj = objective();
    qsa('.v49-stage').forEach(x=>x.classList.remove('is-on'));
    let out = ['mission: GOALOS-V49','objective: '+obj,'boundary: preserved','external actions: 0',''];
    stages.forEach((s,i)=>{ out.push(String(i+1).padStart(2,'0')+' · '+s+' · local pass'); });
    log(out.join('\n'));
    let i=0; const cards=qsa('.v49-stage');
    const timer=setInterval(()=>{ if(cards[i]) cards[i].classList.add('is-on'); i++; if(i>=cards.length) clearInterval(timer); },120);
  }
  function packet(){
    const obj=objective();
    return {version:'v49', mission:'GOALOS-AURORA-FULL-SPECTRUM', objective:obj, stages, agents:['Architect','Planner','Research','Builder','Verifier','AGI Node Worker','AGI Node Validator','Sentinel','Evidence Docket','Chronicle','Human','Council'], boundary:{userData:false,userFunds:false,wallet:false,transaction:false,externalActions:0,productionAuthority:false}, next:['autonomy-theatre.html','agi-agent-workbench.html','validation-control-tower.html','mainnet-contract-atlas.html','site-map.html']};
  }
  function download(){ const data=JSON.stringify(packet(),null,2); const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([data],{type:'application/json'})); a.download='goalos-v49-mission-packet.json'; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),500); }
  function answer(){
    const q=(qs('[data-v49-question]')||{}).value||''; const low=q.toLowerCase(); let hit=routes.find(r=>low.includes((r.title||'').toLowerCase().split(' ')[0])||low.includes((r.category||'').toLowerCase().split(' ')[0]));
    if(low.includes('contract')) hit=routes.find(r=>r.url==='mainnet-contract-atlas.html')||hit;
    if(low.includes('valid')) hit=routes.find(r=>r.url==='validation-control-tower.html')||hit;
    if(low.includes('rsi')||low.includes('loop')) hit=routes.find(r=>r.url==='from-loop-to-rsi-state-capacity.html')||hit;
    if(low.includes('proof')) hit=routes.find(r=>r.url==='proof-run-001-docket.html')||hit;
    if(!hit) hit=routes.find(r=>r.url==='site-map.html')||routes[0];
    const box=qs('[data-v49-answer-box]'); if(box&&hit) box.innerHTML='Open <a href="'+hit.url+'">'+hit.title+'</a><br><small>'+hit.description+'</small>';
  }
  document.addEventListener('click', function(e){
    const load=e.target.closest('[data-v49-load]'); if(load){ const t=qs('[data-v49-objective]'); if(t) t.value=load.getAttribute('data-v49-load'); window.scrollTo({top:0,behavior:'smooth'}); run(); }
    if(e.target.closest('[data-v49-run]')) run();
    if(e.target.closest('[data-v49-download]')) download();
    if(e.target.closest('[data-v49-next]')) location.href='autonomy-theatre.html';
    if(e.target.closest('[data-v49-ask-open]')) qs('[data-v49-ask]')?.classList.add('is-open');
    if(e.target.closest('[data-v49-ask-close]')) qs('[data-v49-ask]')?.classList.remove('is-open');
    if(e.target.closest('[data-v49-answer]')) answer();
  });
  document.addEventListener('input', function(e){ if(e.target.matches('[data-v49-search]')){ const v=e.target.value.toLowerCase(); const res=qs('[data-v49-results]'); if(!res) return; const items=routes.filter(r=>(r.title+' '+r.category+' '+r.description+' '+r.url).toLowerCase().includes(v)).slice(0,160); res.innerHTML='<div class="v49-list">'+items.map(r=>'<a class="v49-row" href="'+r.url+'"><span>'+r.category+'</span><b>'+r.title+'</b><em>'+r.description+'</em></a>').join('')+'</div>'; }});
  window.addEventListener('keydown', function(e){ if(e.key==='/' && !/TEXTAREA|INPUT/.test(document.activeElement.tagName)){ e.preventDefault(); qs('[data-v49-ask]')?.classList.add('is-open'); }});
})();