
(function(){
  const routes = window.GOALOS_SITE_ROUTES || [];
  const meta = window.GOALOS_SITE_META || {};
  const $ = (s,root=document)=>root.querySelector(s);
  const $$ = (s,root=document)=>Array.from(root.querySelectorAll(s));
  function routeUrl(path){ return path.endsWith('/') ? path : path; }
  function card(route){
    const status = route.status === 'live' ? '' : ' · expected';
    return `<article class="route-list-card" data-category="${route.category}" data-search="${[route.title,route.description,route.category,route.audience,route.role].join(' ').toLowerCase()}">
      <h4>${route.title}</h4><p>${route.description}</p><small>${route.category} · ${route.audience}${status}</small><br>
      ${route.status==='live'?`<a class="btn small secondary" href="${routeUrl(route.path)}">Open</a>`:`<span class="btn small secondary" aria-disabled="true">Expected</span>`}
    </article>`;
  }
  function renderRegistry(){
    const host = $('#routeRegistry');
    if(!host) return;
    host.innerHTML = routes.filter(r=>r.path!=='index.html').map(card).join('');
    const count = $('#routeCount'); if(count) count.textContent = routes.filter(r=>r.status==='live').length;
  }
  function applyFilter(cat){
    $$('.filter').forEach(b=>b.classList.toggle('active', b.dataset.filter===cat));
    const q = ($('#routeSearch')?.value || '').toLowerCase().trim();
    $$('.route-list-card').forEach(c=>{
      const okCat = cat==='all' || c.dataset.category===cat;
      const okQ = !q || c.dataset.search.includes(q);
      c.style.display = okCat && okQ ? '' : 'none';
    });
  }
  function setupFilters(){
    if(!$('#routeRegistry')) return;
    $$('.filter').forEach(b=>b.addEventListener('click',()=>applyFilter(b.dataset.filter)));
    $('#routeSearch')?.addEventListener('input',()=>{
      const active = $('.filter.active')?.dataset.filter || 'all'; applyFilter(active);
    });
    applyFilter('all');
  }
  function openPalette(){ $('.palette')?.classList.add('open'); $('#paletteInput')?.focus(); renderPalette(''); }
  function closePalette(){ $('.palette')?.classList.remove('open'); }
  function renderPalette(q){
    const box = $('#paletteResults'); if(!box) return;
    const query = (q||'').toLowerCase().trim();
    const hits = routes.filter(r=>r.status==='live' && (!query || [r.title,r.description,r.category,r.audience,r.role].join(' ').toLowerCase().includes(query))).slice(0,40);
    box.innerHTML = hits.map(r=>`<a href="${routeUrl(r.path)}"><b>${r.title}</b><small>${r.description} · ${r.category}</small></a>`).join('') || '<div style="padding:18px;color:var(--muted)">No route found.</div>';
  }
  function setupPalette(){
    document.addEventListener('keydown', e=>{
      if(e.key==='/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();openPalette();}
      if(e.key==='Escape') closePalette();
    });
    $$('[data-open-palette]').forEach(b=>b.addEventListener('click',openPalette));
    $('.palette')?.addEventListener('click',e=>{ if(e.target.classList.contains('palette')) closePalette(); });
    $('#paletteInput')?.addEventListener('input',e=>renderPalette(e.target.value));
  }
  function setupPathfinder(){
    const select = $('#roleSelect'); const out = $('#roleRoute'); if(!select || !out) return;
    const paths = {
      new: ['start-here.html','proof-experience-atlas.html','try-goalos.html','demo-ecosystem-registry.html'],
      reviewer: ['proof-run-001-docket.html','proof-ledger.html','external-reviewer-replay-room.html','validator-council-arena.html'],
      mission: ['proof-mission-forge.html','proof-mission-control.html','proof-run-001-execution-room.html','evidence-docket-theatre.html'],
      developer: ['website-operating-system.html','demo-ecosystem-registry.html','action-reason-trace-contract.html','docs/'],
      institution: ['institutional-deployment-wedge.html','value-realization-control-room.html','proof-backed-upgrade-rights-room.html','trust-boundary.html']
    };
    function render(){
      const ids = paths[select.value] || paths.new;
      out.innerHTML = ids.map((p,i)=>{ const r=routes.find(x=>x.path===p)||{title:p,description:'Open page',path:p,status:'live'}; return `<article class="route-list-card"><div class="tag">Step ${i+1}</div><h4>${r.title}</h4><p>${r.description}</p><a class="btn small" href="${r.path}">Open</a></article>`; }).join('');
    }
    select.addEventListener('change',render); render();
  }
  document.addEventListener('DOMContentLoaded',()=>{renderRegistry(); setupFilters(); setupPalette(); setupPathfinder();});
})();
