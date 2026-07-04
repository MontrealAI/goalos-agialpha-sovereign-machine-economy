
(function(){
 const ROUTES = window.GOALOS_ROUTES_V42 || [];
 const $ = (s,root=document)=>root.querySelector(s);
 const $$ = (s,root=document)=>Array.from(root.querySelectorAll(s));
 function score(q,r){q=(q||'').toLowerCase().trim(); if(!q) return 0; const hay=(r.title+' '+r.slug+' '+r.category+' '+r.desc).toLowerCase(); let n=0; q.split(/\s+/).forEach(w=>{ if(hay.includes(w)) n+=2; if(r.title.toLowerCase().includes(w)) n+=3; }); return n;}
 function best(q){return ROUTES.map(r=>[score(q,r),r]).filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,6).map(x=>x[1]);}
 function renderRoutes(target, query=''){
   const el=$(target); if(!el) return; const rows=(query?best(query):ROUTES).slice(0,240);
   el.innerHTML=rows.map(r=>`<div class="route-row" data-route="${r.slug}"><div class="category">${r.category}</div><div><b>${r.title}</b><br><small>${r.desc}</small><br><small>${r.slug}</small></div><a class="btn" href="${r.slug}">Open →</a></div>`).join('') || '<p>No route found.</p>';
 }
 function answer(q){ const b=best(q); const lead=b[0];
   if(!q.trim()) return {text:'Ask a question or type an objective. I can route you to contracts, proof dockets, AGI agents, validation, demos, trust, token, docs, or all pages.', routes:ROUTES.slice(0,4)};
   let intent='I found the most relevant GoalOS proof routes.';
   if(/contract|48|mainnet/i.test(q)) intent='The 48 Mainnet contracts are best explored through the Contract Atlas, Proof Rail, and Contract Academy.';
   if(/validate|agi node|human|hybrid|council/i.test(q)) intent='Validation can be done by AGI Node, Human, Hybrid, or Council depending on risk and judgment needs.';
   if(/demo|end.?to.?end|autonom|theatre|run/i.test(q)) intent='The clearest end-to-end experience is Autonomy Theatre or AGI Agent Workbench.';
   if(/token|agialpha|wallet|fund|sale/i.test(q)) intent='Use the Token Boundary and Trust Boundary. GoalOS does not sell, custody, or support wallets.';
   if(/data|privacy|secret/i.test(q)) intent='Use the Trust, Privacy, and Data Boundary pages. Do not submit personal or sensitive data.';
   if(/start|new|begin/i.test(q)) intent='Start Here and Pathfinder are the fastest non-technical path.';
   return {text:intent, routes:b.length?b:ROUTES.slice(0,5)};
 }
 function maybeOpen(q, routes){ if(/\b(open|go|show|launch|take me|redirect)\b/i.test(q) && routes[0]) location.href=routes[0].slug; }
 document.addEventListener('DOMContentLoaded',()=>{
   renderRoutes('#route-list'); renderRoutes('#route-list-all');
   $$('.js-route-filter').forEach(inp=>inp.addEventListener('input',e=>renderRoutes('#route-list', e.target.value)));
   const box=$('#goalos-objective'); const term=$('#goalos-terminal'); const routeCards=$('#goalos-route-cards');
   function generate(){ if(!box||!term) return; const q=box.value||''; const routes=best(q); const mission='GOALOS-MISSION-'+Math.random().toString(16).slice(2,10).toUpperCase();
     term.textContent=`mission: ${mission}\nobjective: ${q.slice(0,90)||'public-safe GoalOS objective'}\nstate: ROUTE_PACKAGE_READY\nboundary: no data / no funds / no wallet / no transaction\nexternal actions: 0\nnext: ${(routes[0]&&routes[0].title)||'Start Here'}`;
     $$('.metric').forEach((m,i)=>{m.textContent=[96,93,100,88][i]+'%'});
     if(routeCards) routeCards.innerHTML=(routes.length?routes:ROUTES.slice(0,6)).slice(0,6).map(r=>`<div class="card"><h3>${r.title}</h3><p>${r.desc}</p><a href="${r.slug}">Open route →</a></div>`).join('');
   }
   $$('.js-generate').forEach(b=>b.addEventListener('click',generate));
   $$('.playbook').forEach(b=>b.addEventListener('click',()=>{ if(box){box.value=b.dataset.objective||b.textContent.trim(); generate(); window.scrollTo({top:0,behavior:'smooth'});}}));
   const askPanel=$('#ask-panel'); const askInput=$('#ask-input'); const askBody=$('#ask-body');
   function openAsk(){ if(askPanel) askPanel.classList.add('open'); if(askInput) setTimeout(()=>askInput.focus(),50);}
   function closeAsk(){ if(askPanel) askPanel.classList.remove('open');}
   $$('.js-ask').forEach(b=>b.addEventListener('click',openAsk)); $$('.js-close-ask').forEach(b=>b.addEventListener('click',closeAsk));
   document.addEventListener('keydown',e=>{ if(e.key==='/' && !/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault(); openAsk();}});
   function send(){ const q=askInput.value; const a=answer(q); askBody.insertAdjacentHTML('beforeend',`<div class="msg"><b>You</b><br>${q}</div><div class="msg bot"><b>Ask GoalOS</b><br>${a.text}<br>${a.routes.slice(0,4).map(r=>`<a class="pill" href="${r.slug}">${r.title}</a>`).join(' ')}</div>`); askInput.value=''; askBody.scrollTop=askBody.scrollHeight; maybeOpen(q,a.routes); }
   if(askInput) askInput.addEventListener('keydown',e=>{ if(e.key==='Enter') send();}); $$('.js-send-ask').forEach(b=>b.addEventListener('click',send));
 });
})();
