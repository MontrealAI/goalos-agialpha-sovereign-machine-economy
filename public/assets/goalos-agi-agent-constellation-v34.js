
(function(){
  const agents = window.GOALOS_AGENTS || [];
  const playbooks = window.GOALOS_PLAYBOOKS || [];
  const routes = window.GOALOS_AGENT_ROUTES || [];
  let selectedAuthority = 'auto';
  let current = {
    objective: 'I want AGI agents to help me understand the 48 Ethereum Mainnet contracts, group them by purpose, explain the proof rail, and produce a reviewer-ready learning path.',
    intent: 'contract_atlas',
    selectedAgents: agents.filter(a=>a.default).map(a=>a.id),
    routes: [],
    state: 'AGENT_CONSTELLATION_READY'
  };
  const $ = sel => document.querySelector(sel);
  const $$ = sel => Array.from(document.querySelectorAll(sel));
  function words(s){return String(s||'').toLowerCase().replace(/[^a-z0-9$]+/g,' ').split(/\s+/).filter(Boolean)}
  const riskWords = ['private','secret','customer','personal','wallet','funds','payment','trade','investment','legal','tax','medical','credential','key','seed','password','deploy','transaction','mainnet transaction','external scan','exploit','malware'];
  function classify(text){
    const t = String(text||'').toLowerCase();
    if(/48|contract|mainnet|ethereum|atlas/.test(t)) return 'contract_atlas';
    if(/rsi|recursive|move.?37|omni|loop|baseline|eci/.test(t)) return 'rsi';
    if(/vendor|procurement|tool|diligence|buy|partner/.test(t)) return 'vendor_review';
    if(/pilot|program|controlled/.test(t)) return 'pilot';
    if(/privacy|data|token|agialpha|fund|wallet|boundary/.test(t)) return 'boundary';
    if(/site|website|navigation|page|route|search/.test(t)) return 'site_qa';
    if(/cyber|security|defensive|vulnerability/.test(t)) return 'defensive_cyber';
    if(/capability|reuse|package|upgrade/.test(t)) return 'capability';
    if(/council|strategic|high novelty|move/.test(t)) return 'council';
    if(/brief|executive|decision/.test(t)) return 'executive';
    return 'proof_mission';
  }
  function pickPlaybook(intent){return playbooks.find(p=>p.intent===intent)||playbooks[1]||playbooks[0]}
  function boundary(text){
    const t = String(text||'').toLowerCase();
    const hits = riskWords.filter(w=>t.includes(w));
    if(hits.some(w=>['wallet','funds','payment','trade','investment','legal','tax','medical','credential','key','seed','password','deploy','transaction','mainnet transaction','external scan','exploit','malware'].includes(w))) return {level:'human', hits, state:'HOLD_HUMAN_REVIEW_REQUIRED'};
    if(hits.length) return {level:'hybrid', hits, state:'HYBRID_REVIEW_READY'};
    return {level:'public-safe', hits:[], state:'AGI_NODE_PRECHECK_READY'};
  }
  function authorityFor(intent, b){
    if(selectedAuthority !== 'auto') return selectedAuthority;
    if(b.level==='human') return 'human';
    if(intent==='rsi'||intent==='council') return 'council';
    if(['vendor_review','pilot','defensive_cyber','procurement','capability'].includes(intent)) return 'hybrid';
    return 'node';
  }
  function agentSetFor(playbook, authority){
    const base = new Set(playbook.agents || []);
    if(authority==='human' || authority==='hybrid') base.add('operator');
    if(authority==='council') base.add('council');
    if(authority==='node' || authority==='hybrid') {base.add('validator'); base.add('nodeWorker');}
    base.add('sentinel');
    return Array.from(base);
  }
  function routeScore(q, r){
    const qs = words(q); const hay = words([r.title, r.url, (r.tags||[]).join(' ')].join(' '));
    return qs.reduce((n,w)=>n+(hay.some(h=>h.includes(w)||w.includes(h))?1:0),0);
  }
  function buildPackage(){
    const text = $('#objective') ? $('#objective').value.trim() : current.objective;
    current.objective = text || current.objective;
    current.intent = classify(current.objective);
    const pb = pickPlaybook(current.intent);
    const b = boundary(current.objective);
    const auth = authorityFor(current.intent,b);
    current.selectedAgents = agentSetFor(pb,auth);
    current.routes = (pb.routes||[]).map(url=>routes.find(r=>r.url===url)||{title:url.replace(/\.html$/,'').replace(/-/g,' '),url,tags:[]});
    if(!current.routes.length) current.routes = routes.map(r=>({...r, score:routeScore(current.objective,r)})).sort((a,b)=>b.score-a.score).slice(0,4);
    current.state = b.state === 'HOLD_HUMAN_REVIEW_REQUIRED' ? 'HOLD_HUMAN_REVIEW_REQUIRED' : (auth==='node'?'AGI_AGENT_NODE_RUN_READY':auth==='human'?'HUMAN_REVIEW_READY':auth==='hybrid'?'HYBRID_AGENT_REVIEW_READY':'COUNCIL_REVIEW_READY');
    render(pb,b,auth);
  }
  function render(pb,b,auth){
    const consoleText = [
      'mission: GOALOS-AGENT-'+hash(current.objective).slice(0,8).toUpperCase(),
      'intent: '+current.intent.replace(/_/g,' '),
      'authority: '+auth.toUpperCase(),
      'state: '+current.state,
      'boundary: '+(b.hits.length ? b.hits.join(', ') : 'public-safe'),
      'agents: '+current.selectedAgents.length,
      'external actions: 0'
    ].join('\n');
    if($('#stateConsole')) $('#stateConsole').textContent = consoleText;
    $$('.stage').forEach((el,i)=>{el.style.borderColor=i<6?'rgba(102,255,210,.55)':'rgba(255,255,255,.13)'});
    $$('.agent').forEach(el=>el.classList.toggle('on', current.selectedAgents.includes(el.dataset.agent)));
    if($('#resultTitle')) $('#resultTitle').textContent = 'Agent mission package ready';
    if($('#resultText')) $('#resultText').textContent = `GoalOS selected ${current.selectedAgents.length} agents and the ${auth} authority path for this objective.`;
    if($('#routes')) $('#routes').innerHTML = current.routes.map(r=>`<div class="route"><div><strong>${escapeHtml(r.title)}</strong><small>${escapeHtml((r.tags||[]).join(' · ')||r.url)}</small></div><a class="btn ghost" href="${escapeAttr(r.url)}">Open →</a></div>`).join('');
    if($('#artifactPreview')) $('#artifactPreview').textContent = JSON.stringify(makeMission(), null, 2);
  }
  function makeMission(){
    const auth = selectedAuthority;
    return {
      version:'v34',
      title:'GoalOS AGI Agent Constellation Run',
      objective: current.objective,
      intent: current.intent,
      state: current.state,
      authority_mode: auth,
      selected_agents: current.selectedAgents.map(id=>agents.find(a=>a.id===id)).filter(Boolean),
      recommended_routes: current.routes,
      boundaries:{public_alpha:true,no_user_data:true,no_user_funds:true,no_wallet:true,no_transaction:true,no_network_call:true,no_production_authority:true,human_review_for_high_impact:true},
      protocol_flow:['Aim','Agent constellation','Bounded work','Proof bundle','Validation','Evidence docket','Governed decision','Chronicle','Reusable capability'],
      artifacts:['Mission Contract','Agent Role Contracts','AGI Node Handoff','ProofBundle Manifest','Reviewer Brief','Action Graph','Evidence Docket Plan']
    }
  }
  function hash(str){let h=2166136261; for(let i=0;i<str.length;i++){h^=str.charCodeAt(i);h=Math.imul(h,16777619)} return (h>>>0).toString(16)}
  function escapeHtml(s){return String(s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
  function escapeAttr(s){return String(s||'').replace(/["<>]/g,'')}
  function download(name, text, type='application/json'){
    const blob = new Blob([text],{type}); const url = URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(url); a.remove()},0)
  }
  function reviewerBrief(){
    const m=makeMission(); return `# GoalOS AGI Agent Constellation Reviewer Brief\n\n## Objective\n${m.objective}\n\n## Decision State\n${m.state}\n\n## Authority\n${m.authority_mode}\n\n## Selected Agents\n${m.selected_agents.map(a=>`- ${a.name}: ${a.role}`).join('\n')}\n\n## Recommended Routes\n${m.recommended_routes.map(r=>`- ${r.title}: ${r.url}`).join('\n')}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.\n`;
  }
  function actionGraph(){
    const rows=[['step','actor','action','gate','output'],['1','Architect Agent','Bound objective','scope and authority','GoalOSCommit draft'],['2','Planner Agent','Create work graph','budget and done condition','RunCommitment draft'],['3','Research/Builder Agents','Create public-safe artifacts','sandbox and policy','ProofBundle manifest'],['4','Verifier / AGI Node Validator','Validate gates','schema/replay/claim boundary','Attestation'],['5','Evidence Docket Agent','Package proof','docket completeness','Evidence Docket plan'],['6','Human or Council if needed','Review high-impact claims','final authority','Governed decision state']]; return rows.map(r=>r.map(c=>'"'+String(c).replace(/"/g,'""')+'"').join(',')).join('\n')
  }
  function nodeHandoff(){const m=makeMission(); return JSON.stringify({version:'v34',kind:'AGI_NODE_HANDOFF',identity:'<name>.alpha.node.agi.eth',work_mode:'public_safe_simulation',roles:['Worker','Validator','Sentinel'],objective:m.objective,selected_agents:m.selected_agents.map(a=>a.name),required_gates:['schema','boundary','replay-readiness','claim support','no wallet','no transaction','human escalation if high impact'],no_external_actions:true},null,2)}
  function bind(){
    if($('#generate')) $('#generate').addEventListener('click', buildPackage);
    if($('#cycle')) $('#cycle').addEventListener('click',()=>{buildPackage(); const log=$('#stateConsole'); if(log) log.textContent += '\n\ncycle: Aim → Agents → Jobs → Proof → Validate → Docket → Chronicle';});
    if($('#openNext')) $('#openNext').addEventListener('click',()=>{buildPackage(); const url=(current.routes[0]||{}).url; if(url) location.href=url;});
    if($('#dlMission')) $('#dlMission').addEventListener('click',()=>{buildPackage(); download('goalos-agi-agent-mission-contract-v34.json', JSON.stringify(makeMission(),null,2));});
    if($('#dlBrief')) $('#dlBrief').addEventListener('click',()=>{buildPackage(); download('goalos-agi-agent-reviewer-brief-v34.md', reviewerBrief(), 'text/markdown');});
    if($('#dlGraph')) $('#dlGraph').addEventListener('click',()=>{buildPackage(); download('goalos-agi-agent-action-graph-v34.csv', actionGraph(), 'text/csv');});
    if($('#dlNode')) $('#dlNode').addEventListener('click',()=>{buildPackage(); download('goalos-agi-node-handoff-v34.json', nodeHandoff());});
    $$('.auth').forEach(b=>b.addEventListener('click',()=>{selectedAuthority=b.dataset.auth; $$('.auth').forEach(x=>x.classList.remove('sel')); b.classList.add('sel'); buildPackage();}));
    $$('.playbook').forEach(el=>el.addEventListener('click',()=>{const p=playbooks[Number(el.dataset.idx)]; if(p&&$('#objective')){$('#objective').value=p.objective; selectedAuthority='auto'; $$('.auth').forEach(x=>x.classList.toggle('sel',x.dataset.auth==='auto')); buildPackage(); location.hash='studio';}}));
    $$('.agent').forEach(el=>el.addEventListener('click',()=>{const id=el.dataset.agent; const s=new Set(current.selectedAgents); if(s.has(id)) s.delete(id); else s.add(id); current.selectedAgents=Array.from(s); el.classList.toggle('on');}));
    const askBtn=$('#askBtn'), drawer=$('#askDrawer'), close=$('#askClose'), form=$('#askForm'), input=$('#askInput'), log=$('#askLog');
    function say(text,user=false){const d=document.createElement('div'); d.className='msg '+(user?'user':''); d.textContent=text; log.appendChild(d); log.scrollTop=log.scrollHeight}
    if(askBtn) askBtn.addEventListener('click',()=>drawer.classList.toggle('open'));
    if(close) close.addEventListener('click',()=>drawer.classList.remove('open'));
    document.addEventListener('keydown',e=>{if(e.key==='/' && !['TEXTAREA','INPUT'].includes(document.activeElement.tagName)){e.preventDefault(); drawer.classList.add('open'); input.focus();}});
    if(form) form.addEventListener('submit',e=>{e.preventDefault(); const q=input.value.trim(); if(!q) return; say(q,true); input.value=''; const intent=classify(q); const pb=pickPlaybook(intent); const open=/\b(open|go|show|launch|take me|redirect)\b/i.test(q); const answer=`Use ${pb.title}. Best page: ${(pb.routes||['goalos.html'])[0]}. GoalOS will create a public-safe agent route, validation path, and review packet. ${open?'Opening it now.':'Ask “open it” to route automatically.'}`; say(answer,false); if(open && pb.routes && pb.routes[0]) setTimeout(()=>{location.href=pb.routes[0]},450);});
    buildPackage();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind); else bind();
})();
