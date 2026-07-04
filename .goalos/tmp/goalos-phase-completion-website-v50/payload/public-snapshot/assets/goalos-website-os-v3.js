
(()=>{
  const data = window.GOALOS_SITE_INDEX_V3 || {routes:[],journey:[],stats:{}};
  const $ = (s,root=document)=>root.querySelector(s);
  const $$ = (s,root=document)=>Array.from(root.querySelectorAll(s));
  const safeRoutes = (data.routes||[]).filter(r=>r.live!==false);
  function openPalette(){let p=$('#gos-palette'); if(p){p.classList.add('open'); const i=$('#gos-palette-input'); if(i){i.focus(); i.select(); renderPalette(i.value||'');}}}
  function closePalette(){let p=$('#gos-palette'); if(p)p.classList.remove('open')}
  function renderPalette(q=''){
    const box=$('#gos-palette-results'); if(!box)return;
    const query=q.trim().toLowerCase();
    const rs=safeRoutes.filter(r=>!query || [r.title,r.category,r.role,r.thesis,r.description].join(' ').toLowerCase().includes(query)).slice(0,70);
    box.innerHTML = rs.map((r,i)=>`<a class="gos-a11y-focus ${i===0?'active':''}" href="${r.url}"><b>${r.title}</b><span>${r.category} · ${r.thesis}</span></a>`).join('') || '<div style="padding:18px;color:#b7c6d8">No route found. Try “docket”, “validator”, “mission”, “token”, “action”, or “benchmark”.</div>';
  }
  function mountPalette(){
    if($('#gos-palette'))return;
    const p=document.createElement('div'); p.id='gos-palette'; p.className='gos-palette'; p.innerHTML=`<div class="gos-palette-box"><div class="gos-palette-header"><input id="gos-palette-input" aria-label="Search GoalOS routes" placeholder="Search GoalOS: docket, validator, mission, action, token, benchmark…"></div><div id="gos-palette-results" class="gos-palette-results"></div></div>`;
    document.body.appendChild(p);
    $('#gos-palette-input').addEventListener('input',e=>renderPalette(e.target.value));
    p.addEventListener('click',e=>{if(e.target===p)closePalette()});
    if(!$('.gos-map-button')){const b=document.createElement('button'); b.className='gos-map-button'; b.textContent='Open site map'; b.addEventListener('click',openPalette); document.body.appendChild(b)}
  }
  document.addEventListener('keydown',e=>{if(e.key==='/' && !/input|textarea|select/i.test(e.target.tagName)){e.preventDefault();openPalette()} if(e.key==='Escape')closePalette()});
  document.addEventListener('click',e=>{if(e.target.matches('[data-command-open]'))openPalette()});
  function proofConsole(){
    const steps=$$('.gos-step'); if(!steps.length)return;
    const log=$('#gos-console-log');
    const lines=['Objective received.','Mission Contract bounded.','Autonomous work simulated locally.','Evidence Docket assembled.','Validator route prepared.','Governed Decision State review-ready.','Chronicle + capability package linked.'];
    let idx=0;
    function tick(){steps.forEach((s,i)=>s.classList.toggle('active',i===idx)); if(log){log.innerHTML=lines.slice(0,idx+1).map((l,i)=>`<div>${String(i+1).padStart(2,'0')} · ${l}</div>`).join('')} idx=(idx+1)%steps.length;}
    tick(); setInterval(tick,1800);
  }
  function routeFilters(){
    const q=$('#gos-registry-query'); const c=$('#gos-registry-category'); const target=$('#gos-registry-list');
    if(!target)return;
    const cats=[...new Set(safeRoutes.map(r=>r.category))].sort(); if(c){c.innerHTML='<option value="">All categories</option>'+cats.map(x=>`<option>${x}</option>`).join('')}
    function render(){
      const query=(q?.value||'').toLowerCase(); const cat=c?.value||'';
      const rs=safeRoutes.filter(r=>(!cat||r.category===cat)&&(!query||[r.title,r.thesis,r.description,r.role,r.category].join(' ').toLowerCase().includes(query))).slice(0,120);
      target.innerHTML=rs.map(r=>`<article class="gos-route"><span class="gos-tag">${r.category}</span><h3>${r.title}</h3><p>${r.description}</p><div class="meta"><span>${r.role}</span><span>${r.thesis}</span></div><a class="gos-btn ghost" href="${r.url}">Open →</a></article>`).join('');
    }
    q?.addEventListener('input',render); c?.addEventListener('change',render); render();
  }
  function pathfinder(){
    const output=$('#gos-path-output'); if(!output)return;
    const paths={
      new:['start-here.html','proof-experience-atlas.html','demo-ecosystem-registry.html'],
      reviewer:['proof-ledger.html','proof-run-001-docket.html','external-reviewer-replay-room.html','validator-council-arena.html'],
      mission:['proof-mission-forge.html','proof-mission-control.html','proof-run-001-execution-room.html'],
      developer:['website-operating-system.html','demo-ecosystem-registry.html','site-map.html'],
      institution:['institutional-deployment-wedge.html','value-realization-control-room.html','trust-boundary.html']
    };
    function label(p){const r=safeRoutes.find(x=>x.path===p);return r?r.title:p}
    function draw(k){const ps=paths[k]||paths.new; output.innerHTML=ps.map((p,i)=>`<a class="gos-journey-item" href="${p}"><span class="gos-journey-num">${i+1}</span><span><h3>${label(p)}</h3><p>${(safeRoutes.find(x=>x.path===p)||{}).thesis||''}</p></span><span class="gos-arrow">Open →</span></a>`).join('')}
    $$('[data-path]').forEach(b=>b.addEventListener('click',()=>draw(b.dataset.path))); draw('new');
  }
  mountPalette(); proofConsole(); routeFilters(); pathfinder();
})();
