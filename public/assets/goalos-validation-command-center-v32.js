(function(){
  const V='v32';
  const routes = window.GOALOS_VALIDATION_ROUTES_V32 || [];
  const playbooks = window.GOALOS_VALIDATION_PLAYBOOKS_V32 || [];
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  const lower = s => String(s||'').toLowerCase();
  const dangerous = ['private key','seed phrase','mnemonic','customer data','personal data','confidential','secret','wallet connect','transaction','send funds','invest','investment return','legal advice','tax advice','medical advice','production deployment','automatic merge','external scan','exploit','malware','phishing'];
  const councilWords = ['council','move-37','move37','rsi','recursive','sovereign','state-capacity','strategic autonomy','breakthrough','high novelty','omni','persistence'];
  const humanWords = ['human','publish','publication','public claim','legal','financial','security posture','procurement','vendor','investment','token sale','external action','high-impact','approval','press'];
  const nodeWords = ['schema','route','site','search','contract atlas','48','token boundary','privacy','data boundary','evidence docket','replay','documentation','completeness','proof run'];
  const routeKeywords = [
    ['mainnet-contract-atlas.html',['48','contract','contracts','mainnet','atlas','ethereum']],
    ['mainnet-proof-rail.html',['proof rail','contract rail','mainnet proof']],
    ['contract-academy.html',['academy','learn contracts','non technical contract']],
    ['proof-run-001-docket.html',['proof run','docket','evidence docket','proof claim','review proof']],
    ['from-loop-to-rsi-state-capacity.html',['rsi','loop','move-37','recursive','state capacity','omni']],
    ['trust-boundary.html',['trust','privacy','data','funds','wallet','no data','no funds']],
    ['token-boundary.html',['token','agialpha','$agialpha','not available','no sale']],
    ['demo-ecosystem-registry.html',['demo','registry','ecosystem']],
    ['site-map.html',['all pages','site map','route','navigation']],
    ['search.html',['search','find']],
    ['goalos.html',['mission','objective','tell goalos']],
    ['ask-goalos.html',['ask','question','chat']]
  ];
  function pickRoutes(text){
    const t = lower(text);
    const picked = [];
    routeKeywords.forEach(([href,keys]) => {
      if(keys.some(k => t.includes(k))) {
        const r = routes.find(x => x.href === href) || {href,title:href.replace('.html',''),description:'Open this route.'};
        picked.push(r);
      }
    });
    if(!picked.length) picked.push(...routes.filter(r => ['goalos.html','demo-ecosystem-registry.html','site-map.html','search.html'].includes(r.href)));
    return [...new Map(picked.map(r => [r.href,r])).values()].slice(0,5);
  }
  function classify(text, mode){
    const t = lower(text || '');
    const hasBoundary = dangerous.some(w => t.includes(w));
    let authority = mode || 'auto';
    let rationale = [];
    if(authority === 'auto'){
      if(hasBoundary){ authority = 'human'; rationale.push('Boundary-sensitive language detected; human review required.'); }
      else if(councilWords.some(w => t.includes(w))){ authority = 'council'; rationale.push('Strategic / RSI / high-novelty language detected; Council review is appropriate.'); }
      else if(humanWords.some(w => t.includes(w))){ authority = 'hybrid'; rationale.push('Judgment-heavy or public-impact language detected; use AGI Node precheck plus human final review.'); }
      else if(nodeWords.some(w => t.includes(w))){ authority = 'agi-node'; rationale.push('Deterministic public-safe validation detected; AGI Node validation is appropriate.'); }
      else { authority = 'hybrid'; rationale.push('Defaulting to AGI Node precheck plus human final review for a balanced path.'); }
    }
    const score = {
      boundary: hasBoundary ? 28 : 96,
      schema: t.length > 20 ? 92 : 72,
      replay: /replay|docket|proof|route|contract|validation|validate/.test(t) ? 88 : 76,
      evidence: /evidence|proof|docket|claim|contract|rsi|vendor|pilot/.test(t) ? 91 : 73,
      human: (authority==='human'||authority==='hybrid'||authority==='council') ? 96 : 72,
      node: (authority==='agi-node'||authority==='hybrid'||authority==='council') ? 96 : 70
    };
    let decision = 'HYBRID_VALIDATION_READY';
    if(hasBoundary) decision = 'HOLD_HUMAN_REVIEW_REQUIRED';
    else if(authority==='agi-node') decision = 'AGI_NODE_VALIDATION_READY';
    else if(authority==='human') decision = 'HUMAN_REVIEW_READY';
    else if(authority==='council') decision = 'COUNCIL_REVIEW_READY';
    else decision = 'HYBRID_VALIDATION_READY';
    const gates = [
      ['Public/private boundary', hasBoundary ? 'hold' : 'pass', hasBoundary ? 'Human review required before any use.' : 'Public-safe boundary preserved.'],
      ['No data / funds / wallet', hasBoundary ? 'hold' : 'pass', hasBoundary ? 'Sensitive wording detected; do not submit private data.' : 'No user data, funds, wallet, transaction, or network call.'],
      ['Authority selected', 'pass', authorityLabel(authority)],
      ['Evidence Docket path', score.evidence>80 ? 'pass' : 'hold', score.evidence>80 ? 'Evidence route found.' : 'Add claim/evidence/docket wording for stronger route.'],
      ['Replay readiness', score.replay>80 ? 'pass' : 'hold', score.replay>80 ? 'Replay-oriented wording detected.' : 'Replay plan recommended.'],
      ['Human escalation', (authority==='agi-node'&&!hasBoundary) ? 'hold':'pass', (authority==='agi-node'&&!hasBoundary) ? 'Optional for low-risk deterministic checks.' : 'Human escalation included or required.']
    ];
    const rs = pickRoutes(t);
    return {authority, decision, rationale, score, gates, routes:rs};
  }
  function authorityLabel(a){
    return ({
      'agi-node':'AGI Node validator',
      'human':'Human reviewer',
      'hybrid':'Hybrid: AGI Node precheck + Human final review',
      'council':'Architect / Validator Council',
      'auto':'Auto-select best authority'
    })[a] || a;
  }
  function artifact(kind, text, state){
    const now = new Date().toISOString();
    const base = {
      goalos_artifact: kind,
      version: 'v32',
      created_at: now,
      objective: text,
      authority: authorityLabel(state.authority),
      decision_state: state.decision,
      boundary: 'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.',
      recommended_routes: state.routes.map(r => r.href),
      gates: state.gates.map(([name,status,note]) => ({name,status,note}))
    };
    if(kind==='validation_certificate') return JSON.stringify({...base, certificate_id:'GOALOS-VAL-'+Math.random().toString(16).slice(2,10).toUpperCase(), scope:'public-safe validation path'}, null, 2);
    if(kind==='agi_node_handoff') return JSON.stringify({...base, node_role:'validator', checks:['schema','route-fit','evidence-docket-completeness','claim-boundary','replay-readiness','no-forbidden-browser-api'], allowed:'deterministic public-safe validation only'}, null, 2);
    if(kind==='attestation') return JSON.stringify({...base, attestation:'Prepared for selected authority. Not a production authorization.'}, null, 2);
    if(kind==='action_graph') return "step,owner,artifact,next_state\nBoundary check,GoalOS,"+state.decision+",Authority selection\nAuthority selection,"+authorityLabel(state.authority)+",Validation Certificate,Route review\nRoute review,Reviewer,Recommended routes,Review packet\nReview packet,Human/Node,Reviewer Brief,Decision state\n";
    const md = `# GoalOS Validation Brief\n\n**Objective:** ${text}\n\n**Authority:** ${authorityLabel(state.authority)}\n\n**Decision state:** ${state.decision}\n\n## Why this authority\n${state.rationale.map(x=>'- '+x).join('\n') || '- Selected by user.'}\n\n## Gates\n${state.gates.map(g=>`- ${g[0]}: ${g[1].toUpperCase()} — ${g[2]}`).join('\n')}\n\n## Recommended routes\n${state.routes.map(r=>`- ${r.title}: ${r.href}`).join('\n')}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.\n`;
    return md;
  }
  function download(name, content, type='text/plain'){
    const blob = new Blob([content], {type});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = name; document.body.appendChild(a); a.click();
    setTimeout(()=>{URL.revokeObjectURL(url); a.remove();}, 0);
  }
  function renderRoutes(container, rs){
    container.innerHTML = rs.map(r => `<a class="v32-route" href="${r.href}"><span><b>${escapeHtml(r.title)}</b>${escapeHtml(r.description||'Open this page.')}</span><b>Open →</b></a>`).join('');
  }
  function escapeHtml(s){return String(s||'').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));}
  function initPage(){
    const input = $('#v32-objective');
    if(!input) return;
    const modeButtons = $$('.v32-mode');
    let mode = 'auto';
    modeButtons.forEach(b => b.addEventListener('click', () => {
      modeButtons.forEach(x => x.classList.remove('active'));
      b.classList.add('active');
      mode = b.dataset.mode || 'auto';
      generate(false);
    }));
    const renderPlaybooks = () => {
      const host = $('#v32-playbooks');
      if(!host) return;
      host.innerHTML = playbooks.map((p,i) => `<article class="v32-playbook">
        <small>${p.id} · ${escapeHtml(p.authority)}</small><strong>${escapeHtml(p.title)}</strong>
        <p>${escapeHtml(p.why)}</p><div class="v32-mini"><b>Creates:</b> ${escapeHtml((p.creates||[]).slice(0,3).join(' · '))}</div>
        <button class="v32-btn secondary" data-playbook="${i}">Use this playbook</button>
      </article>`).join('');
      host.querySelectorAll('[data-playbook]').forEach(btn => btn.addEventListener('click', () => {
        const p = playbooks[Number(btn.dataset.playbook)];
        input.value = p.objective;
        const targetMode = p.authority === 'AGI Node' ? 'agi-node' : p.authority === 'Human' ? 'human' : p.authority === 'Council' ? 'council' : 'hybrid';
        const mb = modeButtons.find(x => x.dataset.mode === targetMode) || modeButtons[0];
        mb.click();
        input.scrollIntoView({behavior:'smooth',block:'center'});
        generate();
      }));
    };
    renderPlaybooks();
    function generate(scroll=true){
      const text = input.value.trim() || 'Validate whether a public-safe Evidence Docket route for the 48 Ethereum Mainnet contracts is complete, claim-bounded, replay-ready, and ready for AGI Node precheck plus human review.';
      const state = classify(text, mode);
      $('#v32-decision').textContent = state.decision;
      $('#v32-authority').textContent = authorityLabel(state.authority);
      $('#v32-rationale').textContent = state.rationale.join(' ') || 'Authority selected by the user.';
      const con = $('#v32-console');
      if(con) con.textContent = [
        'validation: GOALOS-VAL-'+Math.random().toString(16).slice(2,10).toUpperCase(),
        'authority: '+authorityLabel(state.authority),
        'state: '+state.decision,
        'boundary: public-safe / no data / no funds / no wallet',
        'routes: '+state.routes.map(r=>r.href).join(', '),
        'external actions: 0'
      ].join('\n');
      const gates = $('#v32-gates');
      if(gates) gates.innerHTML = state.gates.map(g => `<div class="v32-gate ${g[1]}"><span><b>${escapeHtml(g[0])}</b><br><small>${escapeHtml(g[2])}</small></span><b>${g[1].toUpperCase()}</b></div>`).join('');
      const routeHost = $('#v32-routes');
      if(routeHost) renderRoutes(routeHost, state.routes);
      const dl = $('#v32-downloads');
      if(dl) {
        const safe = text.toLowerCase().replace(/[^a-z0-9]+/g,'-').slice(0,42) || 'goalos-validation';
        dl.innerHTML = '';
        [
          ['Validation Certificate','validation_certificate',`${safe}-validation-certificate.json`,'application/json'],
          ['AGI Node Handoff','agi_node_handoff',`${safe}-agi-node-handoff.json`,'application/json'],
          ['Attestation','attestation',`${safe}-attestation.json`,'application/json'],
          ['Reviewer Brief','reviewer_brief',`${safe}-reviewer-brief.md`,'text/markdown'],
          ['Council Packet','council_packet',`${safe}-council-packet.md`,'text/markdown'],
          ['Action Graph','action_graph',`${safe}-action-graph.csv`,'text/csv']
        ].forEach(([label,kind,filename,type]) => {
          const b = document.createElement('button');
          b.className = 'v32-download';
          b.type = 'button';
          b.textContent = 'Download '+label;
          b.addEventListener('click', () => download(filename, artifact(kind,text,state), type));
          dl.appendChild(b);
        });
      }
      if(scroll && $('#v32-results')) $('#v32-results').scrollIntoView({behavior:'smooth',block:'start'});
      window.__goalosV32State = state;
    }
    $('#v32-generate')?.addEventListener('click', () => generate());
    $('#v32-cycle')?.addEventListener('click', () => {
      const steps = ['Boundary check','Authority selection','Gate evaluation','Certificate build','Review packet','Route handoff'];
      const con = $('#v32-console');
      let i = 0; con.textContent = '';
      const timer = setInterval(()=>{
        con.textContent += `${String(i+1).padStart(2,'0')} · ${steps[i]} passed.\n`;
        i++; if(i>=steps.length){clearInterval(timer); generate(false);}
      }, 160);
    });
    $('#v32-open-next')?.addEventListener('click', () => {
      const st = window.__goalosV32State || classify(input.value, mode);
      const r = st.routes[0]; if(r) location.href = r.href;
    });
    input.addEventListener('input', () => {
      clearTimeout(input.__t); input.__t = setTimeout(()=>generate(false), 260);
    });
    generate(false);
  }
  function answer(q){
    const t = lower(q);
    let text = 'GoalOS can route this through the public proof surface. I found the closest pages below.';
    if(/agi node|node|validate/.test(t)) text = 'AGI Node validation is best for deterministic public-safe checks: schema, route integrity, docket completeness, replay readiness, and boundary wording. Human review is required for high-impact or judgment-heavy outcomes.';
    if(/human/.test(t)) text = 'Human validation is best for public claims, publication approval, legal/financial/security posture, procurement, external actions, and high-impact decisions.';
    if(/48|contract|mainnet/.test(t)) text = 'Start with the Mainnet Contract Atlas, then the proof rail and academy. Use AGI Node validation to check route completeness and token-boundary clarity.';
    if(/token|agialpha|\$/.test(t)) text = '$AGIALPHA is public contract identification only here: not available from GoalOS, no sale, no custody, no wallet support, and no investment advice.';
    if(/data|privacy|wallet|fund/.test(t)) text = 'GoalOS public demos are browser-local and should not ask for user data, funds, wallets, transactions, or production authority.';
    if(/rsi|move|omni|recursive/.test(t)) text = 'Loop → RSI work should use Hybrid or Council validation: AGI Node precheck plus human or council review for replay, baselines, persistence, and dossier handling.';
    return {text, routes: pickRoutes(t)};
  }
  function ensureAsk(){
    if($('#v32-ask-panel')) return;
    const val = document.createElement('button');
    val.className='v32-validate-float'; val.textContent='Validate'; val.type='button';
    val.onclick=()=>{ location.href = (location.pathname.endsWith('/validation-command-center.html')?'#top':'validation-command-center.html'); };
    document.body.appendChild(val);
    const btn = document.createElement('button');
    btn.className='v32-ask-float'; btn.textContent='Ask GoalOS'; btn.type='button'; document.body.appendChild(btn);
    const panel = document.createElement('aside'); panel.className='v32-ask-panel'; panel.id='v32-ask-panel';
    panel.innerHTML = `<div class="v32-ask-head"><span>Ask GoalOS</span><button class="v32-chip" type="button" id="v32-ask-close">Close</button></div>
      <div class="v32-ask-body">
        <textarea class="v32-ask-input" id="v32-ask-input" placeholder="Ask: Can the AGI Node validate this? Where are the 48 contracts?"></textarea>
        <button class="v32-btn primary" id="v32-ask-run" type="button">Answer + route</button>
        <div class="v32-ask-answer" id="v32-ask-answer">Ask a question. I answer locally from the public site map and route only when asked.</div>
        <div class="v32-ask-routes" id="v32-ask-routes"></div>
      </div>`;
    document.body.appendChild(panel);
    const open = ()=>panel.classList.add('open');
    const close = ()=>panel.classList.remove('open');
    btn.addEventListener('click',open);
    $('#v32-ask-close').addEventListener('click',close);
    $('#v32-ask-run').addEventListener('click',()=>{
      const q = $('#v32-ask-input').value || 'Can the AGI Node validate this?';
      const a = answer(q);
      $('#v32-ask-answer').textContent = a.text;
      $('#v32-ask-routes').innerHTML = a.routes.map(r=>`<a href="${r.href}">${escapeHtml(r.title)} →</a>`).join('');
      if(/\b(open|go|show|launch|redirect|take me)\b/i.test(q) && a.routes[0]) setTimeout(()=>{location.href=a.routes[0].href;}, 650);
    });
    document.addEventListener('keydown', ev => {
      if(ev.key === '/' && !['TEXTAREA','INPUT'].includes(document.activeElement?.tagName)){
        ev.preventDefault(); open(); setTimeout(()=>$('#v32-ask-input')?.focus(), 0);
      }
    });
  }
  document.addEventListener('DOMContentLoaded', () => { initPage(); ensureAsk(); });
})();
