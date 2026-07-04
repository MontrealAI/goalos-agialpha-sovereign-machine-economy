
(function(){
  const routes = window.GOALOS_V50_ROUTES || [];
  const stageNames = ['Objective','Mission Contract','AGI Agents','AGI Job','AGI Node','ProofBundle','Evidence Docket','Validate','Chronicle','Reuse'];
  function q(s, el=document){ return el.querySelector(s); }
  function qa(s, el=document){ return Array.from(el.querySelectorAll(s)); }
  function slug(s){ return String(s||'mission').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)||'mission'; }
  function payload(kind){
    const objective = (q('#gx50-objective') && q('#gx50-objective').value.trim()) || 'I want AGI agents to show a complete end-to-end example from objective to proof to validation to Chronicle.';
    return {
      version:'v50', kind:kind||'mission-contract', mission:'GOALOS-MISSION-'+slug(objective).toUpperCase().slice(0,18), objective,
      boundary:'browser-local public-alpha; no user data; no wallet; no transaction; no production authority',
      route:['objective','mission_contract','agi_agents','agi_job','agi_node_handoff','proofbundle','evidence_docket','validation','chronicle','reuse'],
      agents:['Architect','Planner','Research','Builder','Verifier','AGI Node Worker','AGI Node Validator','Sentinel','Docket','Chronicle','Human','Council'],
      artifacts:['Mission Contract','AGI Node Handoff','ProofBundle plan','Evidence Docket plan','Validation Certificate','Reviewer Brief','Action Graph','Chronicle Entry'],
      generatedAt:new Date().toISOString()
    };
  }
  function renderRun(){
    const out = q('#gx50-output');
    if(!out) return;
    const p = payload('demo-run');
    const lines = [
      'mission: '+p.mission,
      'objective: '+p.objective,
      'boundary: preserved',
      'external actions: 0',
      '',
      ...stageNames.map((s,i)=>String(i+1).padStart(2,'0')+' · '+s+': ready'),
      '',
      'next: open the recommended proof page, export artifacts, then run Human / AGI Node validation.'
    ];
    out.textContent = lines.join('\n');
    qa('[data-stage]').forEach((el,i)=>{ el.classList.add('active'); el.style.borderColor='rgba(103,255,210,.62)'; el.style.background='rgba(103,255,210,.12)'; });
  }
  function download(name, data){
    const blob = new Blob([typeof data==='string'?data:JSON.stringify(data,null,2)], {type:'application/json'});
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(a.href),4000);
  }
  function answer(text){
    const t = (text||'').toLowerCase();
    let hits = routes.filter(r => (r.title+' '+r.path+' '+r.category+' '+r.summary).toLowerCase().includes(t.split(/\s+/).find(w=>w.length>3)||t));
    if(t.includes('rsi')||t.includes('loop')) hits = routes.filter(r=>/rsi|loop/i.test(r.path+' '+r.title));
    if(t.includes('agent')) hits = routes.filter(r=>/agent|node/i.test(r.path+' '+r.title));
    if(t.includes('contract')||t.includes('48')) hits = routes.filter(r=>/contract|mainnet/i.test(r.path+' '+r.title));
    if(t.includes('validate')||t.includes('validation')) hits = routes.filter(r=>/validat|review/i.test(r.path+' '+r.title));
    if(t.includes('all')) hits = routes.filter(r=>/site-map|all-pages|route-registry/i.test(r.path));
    hits = hits.slice(0,5);
    if(!hits.length) hits = routes.slice(0,5);
    return 'Recommended route:\n' + hits.map(r=>'• '+r.title+' — '+r.path).join('\n');
  }
  document.addEventListener('click', function(e){
    const btn = e.target.closest('[data-run]');
    if(btn){ renderRun(); }
    const dl = e.target.closest('[data-download]');
    if(dl){ download('goalos-v50-'+(dl.getAttribute('data-download')||'mission')+'.json', payload(dl.getAttribute('data-download'))); }
    const ask = e.target.closest('[data-ask-toggle]');
    if(ask){ const p=q('.gx50-ask-panel'); if(p) p.classList.toggle('open'); }
    const load = e.target.closest('[data-objective]');
    if(load && q('#gx50-objective')){ q('#gx50-objective').value = load.getAttribute('data-objective'); renderRun(); window.scrollTo({top:0,behavior:'smooth'}); }
  });
  document.addEventListener('submit', function(e){
    if(e.target.matches('#gx50-ask-form')){ e.preventDefault(); const val=q('#gx50-ask-input').value; q('#gx50-ask-answer').textContent=answer(val); }
    if(e.target.matches('#gx50-search-form')){ e.preventDefault(); const term=q('#gx50-search-input').value.toLowerCase(); qa('.gx50-route').forEach(el=>{ el.style.display = el.textContent.toLowerCase().includes(term)?'grid':'none'; }); }
  });
  document.addEventListener('DOMContentLoaded', function(){
    if(q('#gx50-output')) renderRun();
    // Remove duplicated legacy floating stacks while preserving page content.
    qa('.float,.floating,.quickbar,.g24-float,.g25-float,.g23-float,.goalos-v41-float,.goalos-v28-float,.goalos-v20-mission-float,.goalos-contract-atlas-v17-button,.gx47-bottom-actions').forEach(el=>el.remove());
  });
})();
