
(() => {
  const ROUTES = window.GOALOS_VALIDATION_ROUTES_V33 || [];
  const PLAYBOOKS = window.GOALOS_VALIDATION_PLAYBOOKS_V33 || [];
  const $ = (s,r=document)=>r.querySelector(s);
  const $$ = (s,r=document)=>Array.from(r.querySelectorAll(s));
  const boundaryText = 'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.';
  const tokenText = '$AGIALPHA public contract identification only. Not available from GoalOS. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice.';
  const riskWords = ['private key','seed phrase','password','credential','customer data','personal data','confidential','trade secret','payment','wallet','funds','bank account','medical record','api key','secret key','mnemonic'];
  let mode = 'auto';
  let active = null;
  const modeCopy = {
    auto:'Auto-select chooses the safest useful authority: AGI Node for deterministic public-safe checks, Human for judgment-heavy decisions, Hybrid for important public proof paths, and Council for strategic / high-novelty validation.',
    'agi-node':'AGI Node validates deterministic public-safe checks: schema, route integrity, docket completeness, claim boundary, replay readiness, and no-wallet / no-data constraints.',
    human:'Human reviewer validates judgment-heavy and high-impact work: public claims, legal / financial / security posture, publication approval, procurement, and external action decisions.',
    hybrid:'Hybrid validation uses AGI Node precheck first and Human final review second. This is the best default for important public work.',
    council:'Architect / Validator Council validates Loop→RSI governance, Move‑37 candidates, institutional promotion, state-capacity claims, and high-novelty dossiers.'
  };
  const stateFor = { 'agi-node':'AGI_NODE_VALIDATION_READY', human:'HUMAN_REVIEW_READY', hybrid:'HYBRID_VALIDATION_READY', council:'COUNCIL_REVIEW_READY' };
  function slug(s){return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,64)||'goalos';}
  function includesAny(text, words){ const t=text.toLowerCase(); return words.some(w=>t.includes(w)); }
  function scoreRoutes(text){
    const t = text.toLowerCase();
    return ROUTES.map(r=>{
      let s=0;
      (r.keywords||[]).forEach(k=>{ if(t.includes(String(k).toLowerCase())) s+=5; });
      if(t.includes('48') && (r.href||'').includes('contract')) s+=10;
      if(t.includes('contract') && (r.href||'').includes('contract')) s+=7;
      if((t.includes('rsi')||t.includes('move')) && ((r.href||'').includes('rsi')||(r.keywords||[]).includes('rsi'))) s+=10;
      if(t.includes('token') && (r.href||'').includes('token')) s+=10;
      if((t.includes('privacy')||t.includes('data')||t.includes('wallet')) && (r.category||'').toLowerCase().includes('boundary')) s+=7;
      if(t.includes('proof') && ((r.href||'').includes('proof')||(r.desc||'').toLowerCase().includes('proof'))) s+=5;
      return {...r, score:s};
    }).sort((a,b)=>b.score-a.score).slice(0,4).filter(r=>r.score>0).concat(ROUTES.filter(r=>['validation-control-tower.html','site-map.html','search.html'].includes(r.href)).slice(0,2)).slice(0,4);
  }
  function autoAuthority(text){
    const t = text.toLowerCase();
    if(includesAny(t, riskWords)) return 'human';
    if(t.includes('move-37') || t.includes('move37') || t.includes('council') || t.includes('state-capacity') || t.includes('sovereign dossier') || t.includes('rsi governance')) return 'council';
    if(t.includes('legal') || t.includes('financial') || t.includes('investment') || t.includes('procurement') || t.includes('publication') || t.includes('public claim') || t.includes('security posture')) return 'human';
    if(t.includes('vendor') || t.includes('pilot') || t.includes('capability') || t.includes('partnership') || t.includes('strategic opportunity')) return 'hybrid';
    if(t.includes('route') || t.includes('schema') || t.includes('docket') || t.includes('token') || t.includes('privacy') || t.includes('data boundary') || t.includes('site') || t.includes('contract')) return 'agi-node';
    return 'hybrid';
  }
  function gateList(text, auth){
    const blocked = includesAny(text, riskWords);
    const high = /legal|financial|investment|security|procurement|publication|public claim|external action|move-?37|rsi|council/i.test(text);
    const gates = [
      ['Public-safe boundary', !blocked ? 'pass':'block'],
      ['Authority selected', 'pass'],
      ['Evidence Docket plan', 'pass'],
      ['Claim boundary visible', 'pass'],
      ['Replay / route readiness', 'pass'],
      ['Human escalation rule', (auth==='agi-node' && high) ? 'hold':'pass'],
      ['No wallet / no transaction', 'pass'],
      ['No network / no data intake', 'pass']
    ];
    return gates;
  }
  function createPackage(input){
    const auth = mode==='auto' ? autoAuthority(input) : mode;
    const blocked = includesAny(input, riskWords);
    const missionId = 'GOALOS-VALIDATION-' + Math.random().toString(16).slice(2,10).toUpperCase();
    const decision = blocked ? 'BLOCK_BOUNDARY' : stateFor[auth];
    const routes = scoreRoutes(input);
    const gates = gateList(input, auth);
    const certificate = {
      id: missionId, version:'v33', createdAt:new Date().toISOString(), authority:auth,
      decisionState:decision, request:input, boundary:boundaryText, tokenBoundary:tokenText,
      gates:gates.map(([name,status])=>({name,status})), recommendedRoutes:routes,
      artifacts:['Validation Certificate JSON','Attestation JSON','AGI Node Handoff JSON','Reviewer Brief Markdown','Council Packet Markdown','Action Graph CSV'],
      limitations:'Browser-local public-alpha validation planner. No backend call, no wallet, no transaction, no production authority.'
    };
    const actionGraph = [
      ['step','owner','artifact','gate','next'],
      ['01 Boundary','AGI Node','boundary-check.json','public/private proof boundary','authority'],
      ['02 Authority',auth,'authority-selection.json','human-or-node policy','gates'],
      ['03 Gates','AGI Node','gate-ledger.json','docket + replay + claim boundary','attestation'],
      ['04 Attestation',auth,'attestation.json','signature-ready packet','review'],
      ['05 Review',auth==='agi-node'?'AGI Node':'Human / Council','reviewer-brief.md','decision state','route'],
      ['06 Route','GoalOS','next-best-page','user opens route','done']
    ];
    return {certificate, actionGraph};
  }
  function updateUI(pkg){
    active = pkg;
    const c = pkg.certificate;
    const authLabel = c.authority==='agi-node'?'AGI NODE':c.authority.toUpperCase();
    const status = $('.v33-status'); if(status) status.textContent = c.decisionState.replaceAll('_',' ');
    const pre = $('#v33LivePre'); if(pre) pre.textContent = `validation: ${c.id}\nauthority: ${authLabel}\nstate: ${c.decisionState}\nboundary: preserved\nexternal actions: 0`;
    const out = $('#v33Decision');
    if(out){
      out.innerHTML = `<strong>${c.decisionState}</strong><span>${explainAuthority(c.authority)}</span><span>${c.limitations}</span>`;
    }
    const gates = $('#v33Gates');
    if(gates) gates.innerHTML = c.gates.map(g=>`<div class="v33-gate ${g.status}">${g.name}</div>`).join('');
    const routes = $('#v33Routes');
    if(routes){
      routes.innerHTML = c.recommendedRoutes.map(r=>`<div class="v33-route"><a href="${r.href}"><span><b>${r.title}</b><small>${r.desc}</small></span><b>Open →</b></a></div>`).join('');
    }
    const next = $('#v33OpenNext'); if(next) next.disabled = !c.recommendedRoutes.length;
  }
  function explainAuthority(a){
    if(a==='agi-node') return 'AGI Node selected: deterministic public-safe validation can be performed autonomously, with escalation if high-impact risk appears.';
    if(a==='human') return 'Human reviewer selected: this request involves judgment, public claim risk, legal/financial/security posture, or publication authority.';
    if(a==='hybrid') return 'Hybrid selected: AGI Node prechecks structure and completeness; Human reviewer makes the final decision.';
    if(a==='council') return 'Council selected: strategic, high-novelty, RSI, Move‑37, or institutional promotion review needs independent authority.';
    return 'Authority selected.';
  }
  function download(name, text, type='application/json'){
    const blob = new Blob([text], {type});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},1000);
  }
  function reviewerBrief(c){
    return `# GoalOS Validation Reviewer Brief\n\n## Request\n${c.request}\n\n## Authority\n${c.authority}\n\n## Decision State\n${c.decisionState}\n\n## Why this authority\n${explainAuthority(c.authority)}\n\n## Gates\n${c.gates.map(g=>`- ${g.status.toUpperCase()}: ${g.name}`).join('\n')}\n\n## Recommended Routes\n${c.recommendedRoutes.map(r=>`- ${r.title}: ${r.href}`).join('\n')}\n\n## Boundary\n${boundaryText}\n\n${tokenText}\n`;
  }
  function councilPacket(c){
    return `# Architect / Validator Council Packet\n\nRequest: ${c.request}\n\nDecision: ${c.decisionState}\n\nCouncil is required for high novelty, Loop→RSI, Move‑37, strategic promotion, or state-capacity claims.\n\nRequired dossier elements:\n- Claims matrix\n- Baselines\n- Reproduction manifest\n- Stress tests\n- Persistence gate\n- Risk report\n- Evidence objects\n- Replay instructions\n- Human / institutional decision note\n`;
  }
  function initMain(){
    if(!$('.v33-body')) return;
    $$('.v33-modes button').forEach(b=>b.addEventListener('click',()=>{
      mode = b.dataset.mode; $$('.v33-modes button').forEach(x=>x.classList.toggle('active',x===b));
      const note = $('#v33ModeNote'); if(note) note.textContent = modeCopy[mode];
    }));
    const pbGrid = $('#v33PlaybookGrid');
    if(pbGrid){
      pbGrid.innerHTML = PLAYBOOKS.map((p,i)=>`<article class="v33-playbook" data-i="${i}" data-mode="${p.mode}" data-intent="${p.intent}"><span class="v33-tag">${p.mode}</span><h3>${p.title}</h3><p>${p.why}</p><p><b>Creates:</b> ${(p.creates||[]).slice(0,3).join(', ')}</p><button>Use this playbook →</button></article>`).join('');
      pbGrid.addEventListener('click',e=>{
        const card = e.target.closest('.v33-playbook'); if(!card) return;
        const p = PLAYBOOKS[Number(card.dataset.i)]; const input = $('#v33Input'); if(input) input.value = p.request;
        mode = p.mode; $$('.v33-modes button').forEach(x=>x.classList.toggle('active',x.dataset.mode===mode));
        const note = $('#v33ModeNote'); if(note) note.textContent = modeCopy[mode];
        updateUI(createPackage(p.request)); location.hash = '#validate';
      });
    }
    $$('.v33-example').forEach(b=>b.addEventListener('click',()=>{ const input=$('#v33Input'); if(input){ input.value=b.dataset.text; updateUI(createPackage(input.value)); }}));
    $('#v33Generate')?.addEventListener('click',()=>{ const input=$('#v33Input'); if(input && input.value.trim()) updateUI(createPackage(input.value.trim())); });
    $('#v33Demo')?.addEventListener('click',()=>{ const p=PLAYBOOKS[0]; const input=$('#v33Input'); if(input) input.value=p.request; mode=p.mode; $$('.v33-modes button').forEach(x=>x.classList.toggle('active',x.dataset.mode===mode)); updateUI(createPackage(p.request)); });
    $('#v33OpenNext')?.addEventListener('click',()=>{ const r=active?.certificate?.recommendedRoutes?.[0]; if(r) location.href=r.href; });
    $('#v33DownloadCertificate')?.addEventListener('click',()=> active && download('goalos-validation-certificate-v33.json', JSON.stringify(active.certificate,null,2)));
    $('#v33DownloadAttestation')?.addEventListener('click',()=> active && download('goalos-validation-attestation-v33.json', JSON.stringify({attestationId:active.certificate.id+'-ATT', authority:active.certificate.authority, verdict:active.certificate.decisionState, gateCount:active.certificate.gates.length, signed:false, boundary:boundaryText},null,2)));
    $('#v33DownloadHandoff')?.addEventListener('click',()=> active && download('goalos-agi-node-handoff-v33.json', JSON.stringify({handoffId:active.certificate.id+'-NODE', allowed:['schema','route','docket','claim-boundary','replay-readiness','browser-local-safety'], forbidden:['wallet','transaction','network-call','production-action','user-data-storage'], escalation:'human review for high-impact outcomes', request:active.certificate.request},null,2)));
    $('#v33DownloadBrief')?.addEventListener('click',()=> active && download('goalos-validation-reviewer-brief-v33.md', reviewerBrief(active.certificate), 'text/markdown'));
    $('#v33DownloadCouncil')?.addEventListener('click',()=> active && download('goalos-council-packet-v33.md', councilPacket(active.certificate), 'text/markdown'));
    $('#v33DownloadGraph')?.addEventListener('click',()=> active && download('goalos-validation-action-graph-v33.csv', active.actionGraph.map(r=>r.map(x=>`"${String(x).replaceAll('"','""')}"`).join(',')).join('\n'), 'text/csv'));
    const input=$('#v33Input'); if(input) updateUI(createPackage(input.value.trim()||PLAYBOOKS[0].request));
  }
  function answer(q){
    const t=q.toLowerCase();
    let matches = scoreRoutes(q);
    let summary = 'I can route you through the public GoalOS proof surface. ';
    if(t.includes('validate')||t.includes('human')||t.includes('node')) summary='Use Validation Control Tower. Choose Auto, AGI Node, Human, Hybrid, or Council. AGI Node is best for deterministic public-safe checks; Human is best for judgment-heavy or high-impact decisions. ';
    else if(t.includes('48')||t.includes('contract')) summary='The 48-contract learning path starts with Mainnet Contract Atlas, then Mainnet Proof Rail, then Contract Academy. ';
    else if(t.includes('token')||t.includes('agialpha')) summary='The token boundary is public contract identification only: not available from GoalOS, no sale, no custody, no wallet support, no investment advice. ';
    else if(t.includes('data')||t.includes('privacy')||t.includes('wallet')) summary='GoalOS public demos are browser-local and do not ask for user data, funds, wallets, transactions, or production authority. ';
    else if(t.includes('rsi')||t.includes('move')) summary='Loop→RSI uses deterministic gates: replay, baselines, ECI discipline, stress tests, persistence, dossier packaging, and council review for high novelty. ';
    const links = matches.map(r=>`<a href="${r.href}">${r.title}</a>`).join(' · ');
    return summary + (links ? `<br><br>Recommended route: ${links}` : 'Open All Pages or Search.');
  }
  function initChat(){
    const btn=$('#v33AskButton'); const chat=$('#v33Chat'); const close=$('#v33ChatClose'); const form=$('#v33ChatForm'); const input=$('#v33ChatInput'); const log=$('#v33ChatLog');
    if(!btn||!chat||!form||!input||!log) return;
    btn.addEventListener('click',()=>chat.classList.add('open'));
    close?.addEventListener('click',()=>chat.classList.remove('open'));
    form.addEventListener('submit',e=>{e.preventDefault(); const q=input.value.trim(); if(!q) return; log.insertAdjacentHTML('beforeend',`<p><b>You:</b> ${escapeHTML(q)}</p><p><b>GoalOS:</b> ${answer(q)}</p>`); input.value=''; log.scrollTop=log.scrollHeight; if(/\b(open|go|show|launch|take me|redirect)\b/i.test(q)){ const r=scoreRoutes(q)[0]; if(r) setTimeout(()=>{location.href=r.href},350); }});
    document.addEventListener('keydown',e=>{ if(e.key==='/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)){ e.preventDefault(); chat.classList.add('open'); input.focus(); }});
  }
  function escapeHTML(s){ return s.replace(/[&<>"]/g, ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch])); }
  function initMini(){
    if($('.v33-body')) return;
    if(document.querySelector('.goalos-v33-global-link')) return;
    const div=document.createElement('div'); div.className='goalos-v33-global-link'; div.innerHTML='<a href="validation-control-tower.html">Validate</a><a href="goalos.html">Tell GoalOS</a><a href="ask-goalos.html">Ask</a><a href="site-map.html">All Pages</a>';
    document.body.appendChild(div);
    const b=document.createElement('button'); b.className='goalos-v33-ask-mini'; b.textContent='Ask GoalOS'; document.body.appendChild(b);
    const c=document.createElement('div'); c.className='goalos-v33-chat-mini'; c.innerHTML='<b>Ask GoalOS</b><p>Ask where to go. Browser-local route helper.</p><input placeholder="Where are the 48 contracts?"/><div class="ans"></div>'; document.body.appendChild(c);
    b.addEventListener('click',()=>c.classList.toggle('open'));
    const inp=c.querySelector('input'), ans=c.querySelector('.ans');
    inp.addEventListener('keydown',e=>{ if(e.key==='Enter'){ ans.innerHTML='<p>'+answer(inp.value)+'</p>'; if(/\b(open|go|show|launch|take me|redirect)\b/i.test(inp.value)){const r=scoreRoutes(inp.value)[0]; if(r) setTimeout(()=>{location.href=r.href},350);} }});
    document.addEventListener('keydown',e=>{ if(e.key==='/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)){ e.preventDefault(); c.classList.add('open'); inp.focus(); }});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>{initMain();initChat();initMini();}); else {initMain();initChat();initMini();}
})();
