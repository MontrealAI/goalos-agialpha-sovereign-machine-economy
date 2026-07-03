(()=>{
  const DATA = window.GOALOS_V41 || {};
  const $ = (s,r=document)=>r.querySelector(s);
  const $$ = (s,r=document)=>Array.from(r.querySelectorAll(s));
  const norm = s => (s||'').toLowerCase();
  const now = () => new Date().toISOString();
  const id = () => 'GOALOS-MISSION-' + Math.random().toString(16).slice(2,10).toUpperCase();
  let currentRun = null;

  function pickDemo(text){
    const q=norm(text);
    const demos=DATA.demos||[];
    if(q.includes('48')||q.includes('contract')||q.includes('mainnet')) return demos.find(d=>d.id==='contracts')||demos[0];
    if(q.includes('vendor')||q.includes('tool')||q.includes('marketing')) return demos.find(d=>d.id==='vendor')||demos[0];
    if(q.includes('pilot')) return demos.find(d=>d.id==='pilot')||demos[0];
    if(q.includes('rsi')||q.includes('move')||q.includes('loop')) return demos.find(d=>d.id==='rsi')||demos[0];
    if(q.includes('privacy')||q.includes('token')||q.includes('wallet')||q.includes('data')) return demos.find(d=>d.id==='boundary')||demos[0];
    if(q.includes('cyber')||q.includes('security')||q.includes('defensive')) return demos.find(d=>d.id==='cyber')||demos[0];
    if(q.includes('procurement')) return demos.find(d=>d.id==='procurement')||demos[0];
    return demos.find(d=>d.id==='complete')||demos[0];
  }
  function authorityFor(demo,text){
    const q=norm(text);
    if(q.includes('legal')||q.includes('financial')||q.includes('procurement')||q.includes('public claim')) return 'Human reviewer';
    if(q.includes('rsi')||q.includes('move-37')||q.includes('sovereign')||q.includes('council')) return 'Architect / Validator Council';
    if(q.includes('boundary')||q.includes('contract')||q.includes('route')||q.includes('docket')) return 'AGI Node validator + Human review available';
    return demo.authority || 'Hybrid: AGI Node precheck + Human final review';
  }
  function makeRun(text){
    const demo=pickDemo(text);
    const authority=authorityFor(demo,text);
    const risk = /legal|financial|security|cyber|public claim|procurement|rsi|move|sovereign/.test(norm(text)) ? 'MEDIUM_REVIEW_REQUIRED' : 'LOW_PUBLIC_SAFE';
    return {id:id(), version:DATA.version, objective:text, demoId:demo.id, title:demo.title, intent:demo.intent, why:demo.why, agents:demo.agents, authority, routes:demo.routes, done:demo.done, created:now(), decision: risk==='LOW_PUBLIC_SAFE'?'DEMO_PACKAGE_READY':'HUMAN_REVIEW_READY', risk, boundary:DATA.boundary};
  }
  function setText(id,text){const el=$(id); if(el) el.textContent=text;}
  function log(line){const el=$('#runLog'); if(!el)return; el.textContent += line+'\n'; el.scrollTop=el.scrollHeight;}
  function renderOrbit(run){
    const orbit=$('#agentOrbit'); if(!orbit)return;
    const selected = new Set(run.agents||[]);
    const agents=DATA.agents||[];
    orbit.innerHTML='<div class="ring"></div><div class="core">α</div>';
    agents.forEach((a,i)=>{
      const angle=(Math.PI*2*i/agents.length)-Math.PI/2;
      const rx=42, ry=42;
      const x=50+Math.cos(angle)*rx, y=50+Math.sin(angle)*ry;
      const n=document.createElement('div'); n.className='agent-node '+(selected.has(a.id)?'active':'');
      n.style.left=`calc(${x}% - 27px)`; n.style.top=`calc(${y}% - 27px)`; n.title=a.name+' — '+a.role; n.textContent=a.short; orbit.appendChild(n);
    });
    const legend=$('#agentLegend'); if(legend) legend.innerHTML=agents.filter(a=>selected.has(a.id)).map(a=>`<span class="tag" title="${a.role}">${a.name}</span>`).join('');
  }
  function renderStages(active=0){
    const rail=$('#stageRail'); if(!rail)return;
    rail.innerHTML=(DATA.stages||[]).map((s,i)=>`<div class="stage ${i<=active?'active':''}"><b>${String(i+1).padStart(2,'0')} ${s.label}</b><small>${s.artifact}</small></div>`).join('');
    const detail=$('#stageDetail'); if(detail){const s=DATA.stages[active]||DATA.stages[0]; detail.innerHTML=`<b>${s.label}</b><p>${s.plain}</p><span class="tag">Artifact: ${s.artifact}</span><span class="tag">Gate: ${s.gate}</span>`;}
  }
  function renderMetrics(run,active=0){
    const vals = {
      readiness: Math.min(100, 35 + active*7 + (run.routes.length*2)),
      replay: Math.min(100, 40 + active*6),
      risk: Math.min(100, run.risk==='LOW_PUBLIC_SAFE'?85:72),
      reuse: Math.min(100, 32 + active*6)
    };
    Object.entries(vals).forEach(([k,v])=>{setText('#m_'+k, v+'%'); const bar=$(`#bar_${k}`); if(bar)bar.style.width=v+'%';});
  }
  function renderRoutes(run){
    const h=$('#routeCards'); if(!h)return;
    const routes=(DATA.routes||[]); const selected=run.routes||[];
    const cards=selected.map(href=>routes.find(r=>r.href===href)||{href,title:href,desc:'Open this GoalOS route.'}).concat(routes.filter(r=>!selected.includes(r.href)).slice(0,3));
    h.innerHTML=cards.slice(0,7).map(r=>`<div class="route-card"><h4>${r.title}</h4><p class="copy">${r.desc}</p><a class="pill primary" href="${r.href}">Open →</a></div>`).join('');
  }
  function payload(type,run){
    const base={system:'GoalOS Autonomy Theatre V41',missionId:run.id,objective:run.objective,intent:run.intent,authority:run.authority,risk:run.risk,decision:run.decision,boundary:run.boundary,agents:run.agents,routes:run.routes,created:run.created};
    const commonGates=['public-safe boundary','no wallet','no transaction','no network call','claim boundary','human review for high-impact outcomes'];
    if(type==='mission')return {...base,artifact:'Mission Contract',successCriteria:['user can understand the path','public-safe proof package created','recommended route cards created','downloadable artifacts available'],failureCriteria:['sensitive user data requested','wallet or transaction attempted','unsupported empirical claim promoted'],doneCondition:run.done,gates:commonGates};
    if(type==='job')return {...base,artifact:'AGI Job Spec',job:{type:'browser-local public-safe demo',acceptanceTests:['all stages complete','all downloads generated','boundary visible','routes available'],prohibited:['external call','wallet','transaction','private data','production authority']}};
    if(type==='node')return {...base,artifact:'AGI Node Handoff',nodeChecks:['schema validity','route fit','docket completeness','replay readiness','boundary wording','no forbidden browser APIs'],allowedAuthority:'deterministic public-safe precheck only'};
    if(type==='proof')return {...base,artifact:'ProofBundle',roots:{missionRoot:'demo-mission-root',policyRoot:'public-alpha-boundary',outputRoot:'browser-local-artifacts',evidenceRoot:'docket-plan'},replay:'Deterministic browser-local simulation; no external system touched.'};
    if(type==='validation')return {...base,artifact:'Validation Certificate',verdict:run.decision,validatorAuthority:run.authority,gates:commonGates,notes:'High-impact, legal, financial, security, publication, or governance-changing outcomes require human/council review.'};
    if(type==='chronicle')return {...base,artifact:'Chronicle Entry',memory:'Accepted demo path can become onboarding memory after human review.',reuse:['explain GoalOS','teach agents/jobs/nodes/proof/docket/validation/chronicle','route non-technical users']};
    if(type==='replay')return {...base,artifact:'Demo Replay',stages:DATA.stages,events:DATA.stages.map((s,i)=>({t:i,label:s.label,artifact:s.artifact,gate:s.gate}))};
    if(type==='brief')return `# Reviewer Brief — ${run.id}\n\nObjective: ${run.objective}\n\nIntent: ${run.intent}\n\nAuthority: ${run.authority}\n\nDecision: ${run.decision}\n\n## Why this matters\n${run.why}\n\n## Recommended routes\n${run.routes.map(r=>'- '+r).join('\n')}\n\n## Boundary\nNo user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required for high-impact outcomes.\n`;
    if(type==='docket')return `# Evidence Docket Plan — ${run.id}\n\n## Claim\nGoalOS can create a public-safe demonstration proof path from one plain-language objective.\n\n## Objective\n${run.objective}\n\n## Claims Matrix\n- Claimed: browser-local mission package generated.\n- Claimed: route recommendations and review artifacts created.\n- Not claimed: achieved AGI/ASI, production authority, wallet support, transaction, external validation, empirical SOTA.\n\n## Required evidence\nMission Contract, AGI Job Spec, AGI Node Handoff, ProofBundle, Validation Certificate, Reviewer Brief, Action Graph, Chronicle Entry.\n`;
    if(type==='graph')return 'source,target,stage\nObjective,Mission Contract,1\nMission Contract,AGI Agents,2\nAGI Agents,AGI Job,3\nAGI Job,AGI Node,4\nAGI Node,ProofBundle,5\nProofBundle,Evidence Docket,6\nEvidence Docket,Validation,7\nValidation,Chronicle,8\nChronicle,Reusable Capability,9\n';
    return base;
  }
  function download(filename,content,mime){
    const text=typeof content==='string'?content:JSON.stringify(content,null,2);
    const blob=new Blob([text],{type:mime||'application/json'});
    const url=URL.createObjectURL(blob);
    const a=document.createElement('a'); a.href=url; a.download=filename; document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),500);
  }
  function renderDownloads(run){
    const h=$('#downloadGrid'); if(!h)return;
    const items=[['mission-contract.json','mission','Mission Contract'],['agi-job-spec.json','job','AGI Job Spec'],['agi-node-handoff.json','node','AGI Node Handoff'],['proofbundle.json','proof','ProofBundle'],['evidence-docket-plan.md','docket','Evidence Docket Plan'],['validation-certificate.json','validation','Validation Certificate'],['reviewer-brief.md','brief','Reviewer Brief'],['action-graph.csv','graph','Action Graph CSV'],['chronicle-entry.json','chronicle','Chronicle Entry'],['demo-replay.json','replay','Demo Replay']];
    h.innerHTML=items.map(([file,type,label])=>`<div class="artifact-card"><h4>${label}</h4><p class="copy">${file}</p><button class="btn secondary" data-dl="${type}" data-file="${file}">Download</button></div>`).join('');
    h.querySelectorAll('[data-dl]').forEach(btn=>btn.addEventListener('click',()=>{const f=btn.dataset.file; const mime=f.endsWith('.md')?'text/markdown':f.endsWith('.csv')?'text/csv':'application/json'; download(f,payload(btn.dataset.dl,run),mime);}));
  }
  function renderPlaybooks(){
    const h=$('#playbookGrid'); if(!h)return;
    h.innerHTML=(DATA.demos||[]).map(d=>`<div class="playbook"><div class="eyebrow">${d.intent}</div><h3>${d.title}</h3><p class="copy">${d.why}</p><p><span class="tag">${d.authority}</span></p><button class="btn secondary" data-demo="${d.id}">Use this demo</button></div>`).join('');
    h.querySelectorAll('[data-demo]').forEach(btn=>{const demo=DATA.demos.find(d=>d.id===btn.dataset.demo); btn.addEventListener('click',()=>{const input=$('#objectiveInput'); input.value=demo.objective; prepare(demo.objective); input.scrollIntoView({behavior:'smooth',block:'center'});});});
  }
  function prepare(text){
    currentRun = makeRun(text);
    setText('#missionId', currentRun.id);
    setText('#decisionState', currentRun.decision);
    setText('#authorityState', currentRun.authority);
    setText('#intentState', currentRun.intent);
    renderOrbit(currentRun); renderStages(0); renderMetrics(currentRun,0); renderRoutes(currentRun); renderDownloads(currentRun);
    const logEl=$('#runLog'); if(logEl) logEl.textContent='mission prepared: '+currentRun.id+'\n';
  }
  function run(){
    const input=$('#objectiveInput'); const text=(input&&input.value.trim())||DATA.demos[0].objective; prepare(text);
    let i=0; const stages=DATA.stages||[];
    const tick=()=>{
      const s=stages[i]; renderStages(i); renderMetrics(currentRun,i); log(String(i+1).padStart(2,'0')+' '+s.label+' → '+s.artifact+' | gate: '+s.gate);
      i++; if(i<stages.length) setTimeout(tick,420); else {setText('#decisionState',currentRun.decision); log('DONE: review-ready package generated. Open routes or download artifacts.');}
    };
    tick();
  }
  function initAsk(){
    const btn=$('#askButton'), panel=$('#askPanel'), close=$('#askClose'), send=$('#askSend'), input=$('#askInput'), body=$('#askBody'); if(!btn||!panel)return;
    const routeFor=q=>{q=norm(q); if(q.includes('48')||q.includes('contract'))return ['mainnet-contract-atlas.html','Open the 48 Contract Atlas.']; if(q.includes('rsi')||q.includes('loop')||q.includes('move'))return ['from-loop-to-rsi-state-capacity.html','Open Loop → RSI governance.']; if(q.includes('token')||q.includes('agialpha'))return ['token-boundary.html','Open the token boundary.']; if(q.includes('privacy')||q.includes('data')||q.includes('wallet'))return ['trust-boundary.html','Open the trust boundary.']; if(q.includes('validate')||q.includes('human')||q.includes('node'))return ['validation-control-tower.html','Open Validation Control Tower.']; if(q.includes('agent'))return ['agi-agent-workbench.html','Open AGI Agent Workbench.']; if(q.includes('demo')||q.includes('end'))return ['autonomy-theatre.html','Open the Autonomy Theatre.']; return ['site-map.html','Open All Pages.'];};
    const add=(text,cls='')=>{const b=document.createElement('div'); b.className='bubble '+cls; b.textContent=text; body.appendChild(b); body.scrollTop=body.scrollHeight;};
    const submit=()=>{const q=input.value.trim(); if(!q)return; add(q,'user'); const [href,msg]=routeFor(q); const should=/(open|go|show|launch|take me|redirect)/.test(norm(q)); add(msg+' GoalOS answers locally from the public route map.'); const a=document.createElement('a'); a.className='pill primary'; a.href=href; a.textContent='Open '+href; body.appendChild(a); if(should)setTimeout(()=>location.href=href,650); input.value='';};
    btn.addEventListener('click',()=>panel.classList.add('open')); close&&close.addEventListener('click',()=>panel.classList.remove('open')); send&&send.addEventListener('click',submit); input&&input.addEventListener('keydown',e=>{if(e.key==='Enter')submit();}); document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();panel.classList.add('open');input.focus();}});
  }
  function init(){
    renderPlaybooks(); const input=$('#objectiveInput'); if(input&&!input.value) input.value=(DATA.demos&&DATA.demos[0]&&DATA.demos[0].objective)||''; prepare(input?input.value:''); $('#runBtn')&&$('#runBtn').addEventListener('click',run); $('#prepareBtn')&&$('#prepareBtn').addEventListener('click',()=>prepare($('#objectiveInput').value)); $$('.chip[data-objective]').forEach(c=>c.addEventListener('click',()=>{const input=$('#objectiveInput'); input.value=c.dataset.objective; prepare(input.value);})); initAsk();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();