
(function(){
  const DATA = window.GOALOS_AGENT_V36 || {routes:[],agents:[],playbooks:[]};
  const $ = (id)=>document.getElementById(id);
  let current = {intent:'AGI Agent Mission', authority:'Hybrid', routes: DATA.routes.slice(0,3), agents: DATA.agents.slice(0,5), prompt:''};
  function text(s){return String(s||'').toLowerCase();}
  function pickPlaybook(q){
    const words = text(q);
    let best = DATA.playbooks[0], score = -1;
    DATA.playbooks.forEach(pb=>{
      let s=0; const blob=text(pb.title+' '+pb.prompt+' '+pb.intent+' '+pb.outputs+' '+(pb.routes||[]).join(' '));
      words.split(/[^a-z0-9$]+/).filter(w=>w.length>2).forEach(w=>{ if(blob.includes(w)) s += 2; });
      if(words.includes('contract') && blob.includes('contract')) s+=6;
      if(words.includes('rsi') && blob.includes('rsi')) s+=6;
      if(words.includes('vendor') && blob.includes('vendor')) s+=6;
      if(words.includes('privacy') && blob.includes('privacy')) s+=6;
      if(words.includes('token') && blob.includes('token')) s+=6;
      if(words.includes('cyber') && blob.includes('cyber')) s+=6;
      if(s>score){score=s; best=pb;}
    });
    return best;
  }
  function routesFor(pb){
    const set = new Set(pb.routes||[]), found=[];
    (pb.routes||[]).forEach(u=>{ const r=DATA.routes.find(x=>x.url===u) || {title:u.replace(/[-.html]/g,' ').trim(),url:u,summary:'Recommended GoalOS route.',category:'Recommended'}; found.push(r); });
    DATA.routes.forEach(r=>{ if(found.length<5 && !set.has(r.url) && text(r.title+' '+r.summary).includes(text(pb.intent).split(' ')[0])) found.push(r); });
    return found.slice(0,5);
  }
  function agentsFor(pb){
    const ids = new Set(pb.agents||[]);
    return DATA.agents.filter(a=>ids.has(a.id)).concat(DATA.agents.filter(a=>!ids.has(a.id))).slice(0,8);
  }
  function missionId(q){let h=0; for(let i=0;i<q.length;i++){h=(h*31+q.charCodeAt(i))>>>0;} return 'GOALOS-AGENT-MISSION-'+h.toString(16).toUpperCase().padStart(8,'0').slice(0,8);}
  function renderOrb(agents){
    const root=$('agentNodes'); if(!root) return; root.innerHTML='<div class="ring"></div><div class="core">α</div>';
    const n=agents.length, cx=50, cy=50, rx=38, ry=38;
    agents.forEach((a,i)=>{ const ang=(-90+i*360/n)*Math.PI/180; const d=document.createElement('div'); d.className='agent-dot '+(i<6?'active':''); d.style.left=`calc(${cx+Math.cos(ang)*rx}% - 27px)`; d.style.top=`calc(${cy+Math.sin(ang)*ry}% - 27px)`; d.textContent=a.id; d.title=a.name+' — '+a.role; root.appendChild(d); });
  }
  function renderStages(active){
    const el=$('stageRail'); if(!el) return; const stages=['Objective','Agents','Job','Node','Validate','Docket','Chronicle','Next'];
    el.innerHTML=stages.map((s,i)=>`<div class="stage ${i<=active?'active':''}"><b>${String(i+1).padStart(2,'0')} ${s}</b><span>${stageText(s)}</span></div>`).join('');
  }
  function stageText(s){return {Objective:'Understand request',Agents:'Select roles',Job:'Bound work',Node:'Prepare handoff',Validate:'Human/Node gates',Docket:'Package proof',Chronicle:'Store memory',Next:'Open route'}[s]||'';}
  function renderRoutes(routes){
    const el=$('routeCards'); if(!el) return; el.innerHTML=routes.map(r=>`<div class="route-card"><div><b>${r.title}</b><br><small>${r.summary||r.category||''}</small></div><a class="btn" href="${r.url}">Open →</a></div>`).join('');
  }
  function buildPackage(){
    const q=($('goalInput')&&$('goalInput').value.trim())||'I want AGI agents to help me run a public-safe proof mission.';
    const pb=pickPlaybook(q); const agents=agentsFor(pb); const routes=routesFor(pb);
    current={prompt:q, playbook:pb, agents, routes, authority:pb.authority, intent:pb.intent, id:missionId(q)};
    renderOrb(agents); renderStages(7); renderRoutes(routes);
    const term=$('consoleText'); if(term) term.textContent = `mission: ${current.id}\nintent: ${pb.intent}\nauthority: ${pb.authority}\nagents: ${agents.map(a=>a.id).join(' → ')}\nstate: AGI_AGENT_PROOF_PATH_READY\nexternal actions: 0\nboundary: preserved`;
    const st=$('missionState'); if(st) st.innerHTML = `<h3>Mission package ready</h3><p>GoalOS selected <b>${pb.intent}</b>, activated <b>${agents.slice(0,6).map(a=>a.name).join(', ')}</b>, and prepared a <b>${pb.authority}</b> validation path.</p><p><b>What you get:</b> ${pb.outputs}.</p>`;
  }
  function pkg(){
    const p=current.playbook || pickPlaybook(current.prompt||'');
    return {version:'v36', missionId:current.id||missionId(current.prompt||''), objective:current.prompt, intent:p.intent, authority:p.authority, boundary:DATA.boundary, agents:current.agents||[], routes:current.routes||[], outputs:p.outputs, generatedAt:new Date().toISOString(), claimBoundary:'Public-safe browser-local demonstration. No backend call, wallet, transaction, user data storage, or production authority.'};
  }
  function download(name, body, type){ const b=new Blob([body],{type:type||'text/plain'}); const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download=name; document.body.appendChild(a); a.click(); setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},50); }
  function mdBrief(){ const p=pkg(); return `# ${p.missionId} — AGI Agent Mission Brief\n\n## Objective\n${p.objective}\n\n## Intent\n${p.intent}\n\n## Authority\n${p.authority}\n\n## Agents\n${p.agents.map(a=>`- **${a.name}** — ${a.role}`).join('\n')}\n\n## Recommended Routes\n${p.routes.map(r=>`- [${r.title}](${r.url}) — ${r.summary}`).join('\n')}\n\n## Boundary\n${p.boundary}\n\n## Next Step\nOpen the top recommended route, review the proof path, then validate with AGI Node, Human, Hybrid, or Council authority as appropriate.\n`; }
  function csvGraph(){ const p=pkg(); const rows=[['step','object','authority','output'],['1','Objective','User','Plain-language objective'],['2','Agent constellation','GoalOS','Selected roles'],['3','AGI Job','Mission Contract','Bounded work'],['4','AGI Node handoff',p.authority,'Deterministic validation path'],['5','Evidence Docket','Verifier','Claims, baselines, proof packets'],['6','Next route','User review',p.routes[0]?p.routes[0].url:'agi-agent-command-center.html']]; return rows.map(r=>r.map(x=>`"${String(x).replaceAll('"','""')}"`).join(',')).join('\n'); }
  function renderPlaybooks(){
    const el=$('playbookGrid'); if(!el) return;
    el.innerHTML=DATA.playbooks.map(pb=>`<article class="card"><div class="num">${pb.id}</div><h3>${pb.title}</h3><p>${pb.outputs}</p><p><b>Authority:</b> ${pb.authority}</p><button class="btn" data-prompt="${pb.prompt.replaceAll('"','&quot;')}">Use this playbook</button></article>`).join('');
    el.querySelectorAll('button[data-prompt]').forEach(btn=>btn.addEventListener('click',()=>{const input=$('goalInput'); if(input){input.value=btn.getAttribute('data-prompt'); input.scrollIntoView({behavior:'smooth',block:'center'}); buildPackage();}}));
  }
  function askAnswer(q){
    const t=text(q); let pb=pickPlaybook(q); let intro='I found the best GoalOS route for that.';
    if(t.includes('agent')) intro='Use AGI Agents when you want a bounded constellation to plan, build, verify, package, and route a public-safe proof mission.';
    if(t.includes('node')) intro='Use an AGI Node for deterministic public-safe validation, replay-readiness checks, and handoff packets; use Human or Hybrid review for high-impact judgment.';
    if(t.includes('data')||t.includes('privacy')) intro='GoalOS public demos stay browser-local and do not ask for user data, funds, wallets, transactions, or production authority.';
    if(t.includes('token')||t.includes('$agialpha')) intro='The token boundary is public contract identification only; $AGIALPHA is not available from GoalOS and the site is not wallet support or investment advice.';
    const routes=routesFor(pb).slice(0,3);
    return {intro,pb,routes};
  }
  function openAsk(){ let p=document.querySelector('.ask-panel'); if(!p){createAsk(); p=document.querySelector('.ask-panel');} p.classList.add('open'); const i=p.querySelector('input'); if(i) i.focus(); }
  function createAsk(){
    if(document.querySelector('.ask-panel')) return;
    const p=document.createElement('div'); p.className='ask-panel'; p.innerHTML='<div class="ask-head"><span>Ask GoalOS</span><button class="btn" type="button" data-close>Close</button></div><div class="ask-log"><div class="msg bot">Ask about AGI agents, AGI Nodes, validation, contracts, RSI, Proof Run 001, token boundary, or where to go next.</div></div><form class="ask-form"><input placeholder="Ask GoalOS…"><button>Ask</button></form>';
    document.body.appendChild(p); p.querySelector('[data-close]').addEventListener('click',()=>p.classList.remove('open'));
    p.querySelector('form').addEventListener('submit',(e)=>{e.preventDefault(); const input=p.querySelector('input'); const q=input.value.trim(); if(!q)return; input.value=''; const log=p.querySelector('.ask-log'); log.insertAdjacentHTML('beforeend',`<div class="msg user">${escapeHtml(q)}</div>`); const a=askAnswer(q); const routeHtml=a.routes.map(r=>`<a class="btn" href="${r.url}">${r.title}</a>`).join(' '); log.insertAdjacentHTML('beforeend',`<div class="msg bot"><b>${a.intro}</b><br>${a.pb.outputs}<div style="margin-top:10px">${routeHtml}</div></div>`); if(/\b(open|go|show|launch|take me|redirect)\b/i.test(q) && a.routes[0]) location.href=a.routes[0].url; log.scrollTop=log.scrollHeight; });
  }
  function escapeHtml(s){return s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function init(){
    if(document.body){document.body.classList.add('goalos-v36');}
    renderPlaybooks(); renderOrb(DATA.agents.slice(0,8)); renderStages(0); renderRoutes(DATA.routes.slice(0,4));
    const input=$('goalInput'); if(input && !input.value) input.value='I want AGI agents to help me understand the 48 Ethereum Mainnet contracts.';
    if($('generateBtn')) $('generateBtn').addEventListener('click',buildPackage);
    if($('cycleBtn')) $('cycleBtn').addEventListener('click',()=>{renderStages(7); const t=$('consoleText'); if(t) t.textContent += '\ncycle: objective → agents → job → node → validate → docket → chronicle → route';});
    if($('openNextBtn')) $('openNextBtn').addEventListener('click',()=>{ if(!current.routes||!current.routes.length) buildPackage(); location.href=(current.routes&&current.routes[0]&&current.routes[0].url)||'site-map.html'; });
    if($('downloadMissionBtn')) $('downloadMissionBtn').addEventListener('click',()=>download('goalos-agent-mission-contract-v36.json', JSON.stringify(pkg(), null, 2), 'application/json'));
    if($('downloadBriefBtn')) $('downloadBriefBtn').addEventListener('click',()=>download('goalos-agent-reviewer-brief-v36.md', mdBrief(), 'text/markdown'));
    if($('downloadGraphBtn')) $('downloadGraphBtn').addEventListener('click',()=>download('goalos-agent-action-graph-v36.csv', csvGraph(), 'text/csv'));
    document.querySelectorAll('[data-ask-goalos]').forEach(b=>b.addEventListener('click',openAsk));
    document.addEventListener('keydown',e=>{ if(e.key==='/' && !/input|textarea/i.test(document.activeElement.tagName)){ e.preventDefault(); openAsk(); }});
    if(!document.querySelector('.ask-launch')){ const b=document.createElement('button'); b.className='ask-launch'; b.type='button'; b.textContent='Ask GoalOS'; b.addEventListener('click',openAsk); document.body.appendChild(b); }
    if(!document.querySelector('.tell-launch')){ const a=document.createElement('a'); a.className='tell-launch'; a.href='agi-agent-command-center.html'; a.textContent='AGI Agents'; document.body.appendChild(a); }
    createAsk(); buildPackage();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
