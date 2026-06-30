
(() => {
  const steps = Array.from(document.querySelectorAll('.step'));
  const terminal = document.querySelector('[data-proof-log]');
  const logs = [
    '01 · Objective received. Scope is public-alpha.',
    '02 · Mission contract bounded. No data, no funds.',
    '03 · Evidence route inspected from committed source.',
    '04 · Validator path remains human-review-ready.',
    '05 · Decision state is repository-readiness, not empirical SOTA.',
    '06 · Chronicle pointer and capability route refreshed.',
    '07 · Route integrity checked. Token boundary present.',
    '08 · Source, website, registry, and docket aligned.'
  ];
  let idx = 0;
  function tick(){
    if(steps.length){ steps.forEach((el,i)=>el.classList.toggle('active',i===idx%steps.length)); }
    if(terminal){ terminal.textContent = logs.slice(0,(idx%logs.length)+1).join('\n'); }
    idx += 1;
  }
  tick();
  setInterval(tick, 1800);
  const routes = (window.GOALOS_SITE_ROUTES_V6 || []);
  const modal = document.createElement('div');
  modal.className = 'palette-modal';
  modal.innerHTML = '<div class="palette-box" role="dialog" aria-label="GoalOS command palette"><input aria-label="Search GoalOS routes" placeholder="Search routes: docket, validator, token, action, benchmark..." /><div class="palette-results"></div></div>';
  document.body.appendChild(modal);
  const input = modal.querySelector('input');
  const results = modal.querySelector('.palette-results');
  function render(q=''){
    const term = q.trim().toLowerCase();
    const filtered = routes.filter(r => !term || (r.name + ' ' + r.path + ' ' + r.category + ' ' + r.description).toLowerCase().includes(term)).slice(0,24);
    results.innerHTML = filtered.map(r => `<a href="${r.path}"><strong>${r.name}</strong><br><small>${r.category} · ${r.description}</small></a>`).join('') || '<p>No route matched. Try “docket”, “token”, “validator”, “mission”, or “action”.</p>';
  }
  function openPalette(){ modal.classList.add('open'); render(''); setTimeout(()=>input.focus(),20); }
  function closePalette(){ modal.classList.remove('open'); }
  document.querySelectorAll('[data-open-palette]').forEach(b=>b.addEventListener('click', openPalette));
  document.addEventListener('keydown', e => { if(e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)){ e.preventDefault(); openPalette(); } if(e.key === 'Escape') closePalette(); });
  modal.addEventListener('click', e => { if(e.target === modal) closePalette(); });
  input.addEventListener('input', e => render(e.target.value));
})();
