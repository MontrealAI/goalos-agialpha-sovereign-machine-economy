
(function(){
  const profiles = window.GoalOSDemoProfilesV55 || {};
  const defaultProfile = profiles.command;
  const routeMap = window.GoalOSRouteRegistryV55 || [];
  const KEYWORDS = [
    ["contract", "mainnet-contract-atlas.html"], ["48", "mainnet-contract-atlas.html"], ["token", "token-boundary.html"],
    ["rsi", "from-loop-to-rsi-state-capacity.html"], ["loop", "loop-bottleneck-observatory.html"], ["move", "move37-dossier.html"],
    ["node", "agi-alpha-node-v0.html"], ["agent", "agi-agent-workbench.html"], ["validate", "validation-control-tower.html"],
    ["human", "human-or-agi-node-validation.html"], ["proof", "proof-run-001-docket.html"], ["docket", "evidence-docket-theatre.html"],
    ["search", "search.html"], ["all", "all-pages.html"], ["trust", "trust-boundary.html"], ["privacy", "privacy.html"], ["wallet", "token-boundary.html"]
  ];
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  function path(){ return (location.pathname.split('/').pop() || 'index.html').toLowerCase(); }
  function profile(){ return profiles[document.body.dataset.goalosProfile || window.GOALOS_V55_PROFILE_KEY] || classify() || defaultProfile; }
  function classify(){ const p=path(); if(p.includes('move37')) return profiles.move37; if(p.includes('loop')&&!p.includes('rsi')) return profiles.loop; if(p.includes('rsi')) return profiles.rsi; if(p.includes('playbook')||p.includes('use-case')) return profiles.playbooks; if(p.includes('agent')||p.includes('meta-agentic')) return profiles.agents; if(p.includes('node')) return profiles.node; if(p.includes('valid')||p.includes('validator')||p.includes('council')) return profiles.validation; if(p.includes('contract')||p.includes('mainnet')) return profiles.contracts; if(p.includes('proof')||p.includes('evidence')||p.includes('docket')||p.includes('ledger')) return profiles.proof; if(p.includes('search')||p.includes('site')||p.includes('all-pages')||p.includes('ask')) return profiles.navigation; if(p.includes('trust')||p.includes('privacy')||p.includes('boundary')||p.includes('token')) return profiles.boundary; return profiles.command; }
  function esc(s){return String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
  function artifactContent(name, p, objective){ return JSON.stringify({goalos:'Sovereign Experience OS V55', page:path(), mission:p.label, objective, artifact:name, boundary:'browser-local public-alpha demonstration; no wallet; no transaction; no backend call', generatedAt:new Date().toISOString(), stages:p.stages, agents:p.agents, nextRoutes:p.routes}, null, 2); }
  function downloadUrl(text){ const blob = new Blob([text], {type:'application/json;charset=utf-8'}); return URL.createObjectURL(blob); }
  function buildModal(){
    let m = $('#goalos-v55-modal'); if(m) return m;
    m = document.createElement('div'); m.id='goalos-v55-modal'; m.className='v55-modal goalos-v55';
    m.innerHTML = '<div class="v55-cockpit"><div class="v55-cockpit-head"><div><div class="v55-kicker">Autonomous Experience</div><h2 id="v55-modal-title">Run the proof path.</h2><p class="v55-subtitle" id="v55-modal-subtitle"></p></div><button class="v55-close" data-v55-close>Close</button></div><textarea id="v55-objective" class="v55-mission-input"></textarea><div class="v55-actions"><button class="v55-btn primary" id="v55-run-now">Run mission</button><button class="v55-btn" id="v55-ask-now">Ask GoalOS</button></div><div class="v55-cockpit-grid"><div><div id="v55-run-grid" class="v55-run-grid"></div><div class="v55-bars"><div class="v55-bar"><label>Readiness <span id="bar-readiness-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-readiness"></span></div></div><div class="v55-bar"><label>Replay <span id="bar-replay-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-replay"></span></div></div><div class="v55-bar"><label>Risk <span id="bar-risk-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-risk"></span></div></div><div class="v55-bar"><label>Reuse <span id="bar-reuse-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-reuse"></span></div></div></div><pre class="v55-log" id="v55-log"></pre><div class="v55-artifacts" id="v55-artifacts"></div></div><aside><h3>Agent constellation</h3><div id="v55-agentlist" class="v55-agentlist"></div><div class="v55-ask-panel"><input id="v55-ask-input" placeholder="Ask about agents, RSI, nodes, contracts, validation, proof..."><button class="v55-btn" id="v55-answer-btn" style="margin-top:10px">Answer</button><div class="v55-answer" id="v55-answer"></div></div></aside></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click', e=>{ if(e.target===m || e.target.matches('[data-v55-close]')) m.classList.remove('is-open'); });
    $('#v55-run-now',m).addEventListener('click',()=>runMission(profile()));
    $('#v55-ask-now',m).addEventListener('click',()=>answerAsk());
    $('#v55-answer-btn',m).addEventListener('click',()=>answerAsk());
    $('#v55-ask-input',m).addEventListener('keydown',e=>{if(e.key==='Enter') answerAsk();});
    return m;
  }
  function openMission(p=profile(), auto=true){
    const m = buildModal();
    $('#v55-modal-title',m).textContent = p.title || 'Run the full proof path.';
    $('#v55-modal-subtitle',m).textContent = p.subtitle || '';
    $('#v55-objective',m).value = p.objective || '';
    $('#v55-run-grid',m).innerHTML = (p.stages||[]).map((s,i)=>'<div class="v55-run-step" data-step="'+i+'"><b>'+String(i+1).padStart(2,'0')+'</b><br>'+esc(s)+'</div>').join('');
    $('#v55-agentlist',m).innerHTML = (p.agents||[]).map((a,i)=>'<div class="v55-agent-pill" data-agent="'+i+'">'+esc(a)+'</div>').join('');
    $('#v55-log',m).textContent = 'GoalOS mission cockpit ready.\nObjective: ' + (p.objective||'') + '\nClick Run mission or edit the objective first.';
    $('#v55-artifacts',m).innerHTML = '';
    ['readiness','replay','risk','reuse'].forEach(k=>{ $('#bar-'+k,m).style.width='0%'; $('#bar-'+k+'-v',m).textContent='0'; });
    m.classList.add('is-open');
    if(auto) setTimeout(()=>runMission(p), 180);
  }
  function runMission(p=profile()){
    const m = buildModal(); const objective = ($('#v55-objective',m)||{}).value || p.objective;
    const steps = p.stages || []; const agents = p.agents || [];
    $('#v55-log',m).textContent = 'GoalOS mission initialized.\nMission: '+p.label+'\nObjective: '+objective+'\nBoundary: browser-local; no wallet; no transaction; no backend call.\n';
    $('#v55-artifacts',m).innerHTML = '';
    $$('.v55-run-step',m).forEach(x=>x.classList.remove('active')); $$('.v55-agent-pill',m).forEach(x=>x.classList.remove('active'));
    let i=0;
    const timer = setInterval(()=>{
      if(i>=steps.length){ clearInterval(timer); finishMission(p, objective, m); return; }
      const st = $('[data-step="'+i+'"]',m); if(st) st.classList.add('active');
      const ag = $('[data-agent="'+(i%Math.max(agents.length,1))+'"]',m); if(ag) ag.classList.add('active');
      const pct = Math.round(((i+1)/steps.length)*100);
      $('#bar-readiness',m).style.width=pct+'%'; $('#bar-readiness-v',m).textContent=pct;
      $('#bar-replay',m).style.width=Math.min(100,Math.round(pct*.86+8))+'%'; $('#bar-replay-v',m).textContent=Math.min(100,Math.round(pct*.86+8));
      $('#bar-risk',m).style.width=Math.min(100,Math.round(100-pct*.18))+'%'; $('#bar-risk-v',m).textContent=Math.min(100,Math.round(100-pct*.18));
      $('#bar-reuse',m).style.width=Math.min(100,Math.round(pct*.74+12))+'%'; $('#bar-reuse-v',m).textContent=Math.min(100,Math.round(pct*.74+12));
      $('#v55-log',m).textContent += String(i+1).padStart(2,'0')+' · '+steps[i]+' · '+(agents[i%agents.length]||'GoalOS')+' · local pass\n';
      $('#v55-log',m).scrollTop = $('#v55-log',m).scrollHeight;
      i++;
    }, 320);
  }
  function finishMission(p, objective, m){
    $('#v55-log',m).textContent += 'DONE=true · Evidence Docket ready · validation path prepared · Chronicle draft available.\n';
    const arts = (p.artifacts||['mission-contract.json','evidence-docket.md','reviewer-brief.md']);
    $('#v55-artifacts',m).innerHTML = arts.map(name=>'<a download="'+esc(name)+'" href="'+downloadUrl(artifactContent(name,p,objective))+'"><span>'+esc(name)+'</span><b>Download</b></a>').join('');
    const routes = (p.routes||[]).map(r=>'<a class="v55-chip" href="'+esc(r)+'">'+esc(titleFromRoute(r))+'</a>').join(' ');
    $('#v55-log',m).textContent += 'Next best routes: '+(p.routes||[]).join(', ')+'\n';
    if(routes){ $('#v55-artifacts',m).insertAdjacentHTML('beforeend','<div style="grid-column:1/-1;margin-top:8px"><b>Next pages</b><div class="v55-actions">'+routes+'</div></div>'); }
  }
  function titleFromRoute(r){ const found=routeMap.find(x=>x.href===r); return found?found.title:r.replace(/\.html$/,'').replace(/-/g,' '); }
  function answerAsk(){
    const m = buildModal(); const q = (($('#v55-ask-input',m)||{}).value || $('#v55-objective',m).value || '').toLowerCase();
    let dest = 'site-map.html'; for(const [kw,href] of KEYWORDS){ if(q.includes(kw)){ dest=href; break; }}
    const prof = profile();
    $('#v55-answer',m).innerHTML = 'Best next page: <a href="'+dest+'">'+titleFromRoute(dest)+'</a>. For this page, run <b>'+esc(prof.label)+'</b> to create local artifacts and a reviewer-ready path.';
  }
  function installDock(){
    $$('.goalos-v55-legacy-hidden').forEach(x=>x.remove());
    $$('a,button').forEach(el=>{ try{ const s=getComputedStyle(el); const b=parseFloat(s.bottom||'999'); if(s.position==='fixed' && b<160 && !el.closest('.goalos-v55')){ el.style.display='none'; el.classList.add('goalos-v55-legacy-hidden'); }}catch(e){} });
    if($('#goalos-v55-dock')) return;
    const d=document.createElement('div'); d.id='goalos-v55-dock'; d.className='v55-dock goalos-v55';
    d.innerHTML='<button data-v55-run>Run end-to-end demo</button><a href="agi-agent-workbench.html">AGI Agents</a><a href="from-loop-to-rsi-state-capacity.html">RSI / Loop</a><a href="validation-control-tower.html">Validate</a><a href="mainnet-contract-atlas.html">48 Contracts</a><a href="all-pages.html">All Pages</a><button data-v55-ask>Ask GoalOS</button>';
    document.body.appendChild(d);
  }
  function bindClicks(){
    document.addEventListener('click', e=>{
      const el = e.target.closest('a,button'); if(!el) return;
      const txt = (el.textContent||'').toLowerCase().trim(); const href=(el.getAttribute('href')||'').toLowerCase();
      if(el.matches('[data-v55-run]') || txt.includes('run end-to-end') || txt==='run demo' || txt.includes('run mission')){ e.preventDefault(); openMission(profile(), true); }
      if(el.matches('[data-v55-ask]') || txt.includes('ask goalos') || txt.includes('tell goalos') || href.includes('ask-goalos')){ if(!href || href==='#'){ e.preventDefault(); openMission(profile(), false); setTimeout(()=>$('#v55-ask-input')?.focus(),80); } }
    }, true);
  }
  function initSearch(){
    const input = $('#v55-route-search'); const list = $('#v55-route-list'); if(!input||!list) return;
    function render(q=''){
      q=q.toLowerCase(); const rows=routeMap.filter(r=>!q||[r.title,r.category,r.description,r.href].join(' ').toLowerCase().includes(q));
      list.innerHTML = rows.map(r=>'<tr><td>'+esc(r.category)+'</td><td><b>'+esc(r.title)+'</b><br><span>'+esc(r.description)+'</span></td><td><a class="v55-chip" href="'+esc(r.href)+'">Open</a></td></tr>').join('');
    }
    input.addEventListener('input',()=>render(input.value)); render('');
  }
  window.GoalOSV55 = {openMission, runMission, profile, answerAsk};
  document.addEventListener('DOMContentLoaded',()=>{ installDock(); bindClicks(); initSearch(); });
})();
