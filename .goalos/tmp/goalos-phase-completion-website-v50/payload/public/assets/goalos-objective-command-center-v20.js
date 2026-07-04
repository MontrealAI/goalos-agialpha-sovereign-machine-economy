
(function(){
  'use strict';
  const ROUTES = [
    {title:'Start Here',url:'start-here.html',tags:'start beginner onboarding first 60 seconds',why:'Fast plain-language onboarding.'},
    {title:'Pathfinder',url:'pathfinder.html',tags:'role path user reviewer developer institution',why:'Choose the correct path for your role.'},
    {title:'Ask GoalOS Concierge',url:'ask-goalos.html',tags:'chat ask questions help route assistant',why:'Ask questions and route to the right page.'},
    {title:'Demo Ecosystem Registry',url:'demo-ecosystem-registry.html',tags:'registry demos inputs outputs gates states',why:'Find demos by workflow role.'},
    {title:'Proof Run 001 Docket',url:'proof-run-001-docket.html',tags:'proof run evidence docket review readiness',why:'Inspect the public proof run.'},
    {title:'Mainnet Contract Atlas',url:'mainnet-contract-atlas.html',tags:'48 contracts ethereum mainnet proof rail contract atlas',why:'Learn the 48 GoalOS-created contracts.'},
    {title:'Mainnet Proof Rail',url:'mainnet-proof-rail.html',tags:'contracts proof rail ethereum mainnet',why:'Understand the on-chain proof rail.'},
    {title:'Contract Academy',url:'contract-academy.html',tags:'learn contracts academy beginner',why:'Non-technical contract learning path.'},
    {title:'Loop Contract Lab',url:'loop-contract-lab.html',tags:'loop prompt contract state disk',why:'Write the loop, not the prompt.'},
    {title:'Loop Flight Recorder',url:'loop-flight-recorder.html',tags:'loop recorder trace restart disk',why:'See how long-running loops leave proof.'},
    {title:'Loop Bottleneck Observatory',url:'loop-bottleneck-observatory.html',tags:'loop bottleneck observatory trace',why:'Watch the next bottleneck surface.'},
    {title:'From Loop to RSI Governance',url:'from-loop-to-rsi-governance.html',tags:'rsi loop governance invention',why:'Bridge loops into RSI governance.'},
    {title:'RSI Sovereign Console',url:'from-loop-to-rsi-sovereign-console.html',tags:'rsi sovereign console omni move 37',why:'Control-plane view of RSI.'},
    {title:'RSI State-Capacity Command Room',url:'from-loop-to-rsi-state-capacity.html',tags:'rsi state capacity command room',why:'State capacity view of recursive invention.'},
    {title:'Trust Boundary',url:'trust-boundary.html',tags:'privacy no data no funds trust boundary',why:'Review public-alpha safety posture.'},
    {title:'Token Boundary',url:'token-boundary.html',tags:'agialpha token boundary no sale no custody',why:'Read the $AGIALPHA boundary.'},
    {title:'All Pages',url:'site-map.html',tags:'all pages site map routes',why:'Open the full route map.'},
    {title:'Site Health',url:'site-health.html',tags:'site health qa route integrity',why:'Inspect route and boundary health.'},
    {title:'Search',url:'search.html',tags:'search command palette routes',why:'Search the whole public site.'}
  ];
  const forbidden = ['private key','seed phrase','password','customer data','personal data','wallet support','send funds','transfer funds','investment advice','trade token','buy token','sell token','medical advice','legal advice'];
  const gateDefs = [
    ['dataBoundary','No user data'],['fundsBoundary','No user funds'],['walletBoundary','No wallet'],['networkBoundary','No network call'],['claimBoundary','Claim-bounded'],['humanReview','Human review'],['replayPath','Replay path'],['docket','Evidence Docket']
  ];
  function $(id){return document.getElementById(id)}
  function now(){return new Date().toISOString().replace(/\.\d+Z$/,'Z')}
  function hash(s){let h=2166136261; for(let i=0;i<s.length;i++){h^=s.charCodeAt(i); h=Math.imul(h,16777619)} return ('00000000'+(h>>>0).toString(16)).slice(-8)}
  function tokens(s){return (s||'').toLowerCase().replace(/[^a-z0-9$\-\s]/g,' ').split(/\s+/).filter(Boolean)}
  function classify(input){
    const q=(input||'').toLowerCase();
    const intents=[];
    if(/48|contract|mainnet|ethereum|etherscan|chain/.test(q)) intents.push('mainnet-contracts');
    if(/rsi|recursive|move.?37|omni|invention/.test(q)) intents.push('loop-rsi');
    if(/loop|restart|trace|bottleneck|flight/.test(q)) intents.push('loop');
    if(/proof|docket|review|evidence|validator|claim/.test(q)) intents.push('proof-review');
    if(/start|begin|new|learn|explain|guide/.test(q)) intents.push('onboarding');
    if(/token|\$agialpha|agialpha|wallet|buy|sell|trade/.test(q)) intents.push('token-boundary');
    if(/privacy|data|fund|wallet|transaction|gdpr|trust|boundary/.test(q)) intents.push('trust-boundary');
    if(/demo|registry|example|use case|page/.test(q)) intents.push('registry');
    if(/build|developer|github|workflow|repo|action/.test(q)) intents.push('developer');
    if(!intents.length) intents.push('mission');
    return [...new Set(intents)];
  }
  function risk(input){
    const q=(input||'').toLowerCase();
    const hits=forbidden.filter(f=>q.includes(f));
    if(hits.length) return {level:'BLOCKED_BOUNDARY_REVIEW',hits,score:92};
    if(/production|deploy|external|mainnet|payment|contract call|wallet|legal|financial|medical/.test(q)) return {level:'HIGH_REVIEW_REQUIRED',hits:[],score:74};
    if(/company|enterprise|pilot|commercial|customer|procurement/.test(q)) return {level:'MEDIUM_REVIEW_REQUIRED',hits:[],score:42};
    return {level:'LOW_PUBLIC_SAFE',hits:[],score:18};
  }
  function routeScore(route, objective, intents){
    const qs=tokens(objective).concat(intents.join(' ').split(/\s+/));
    const hay=(route.title+' '+route.tags+' '+route.why).toLowerCase();
    let score=0; qs.forEach(t=>{ if(t.length>2 && hay.includes(t)) score+=3; });
    if(intents.includes('mainnet-contracts') && /contract|mainnet/.test(hay)) score+=30;
    if(intents.includes('loop-rsi') && /rsi/.test(hay)) score+=26;
    if(intents.includes('proof-review') && /proof|docket|review/.test(hay)) score+=24;
    if(intents.includes('onboarding') && /start|pathfinder/.test(hay)) score+=22;
    if(intents.includes('token-boundary') && /token|agialpha/.test(hay)) score+=30;
    if(intents.includes('trust-boundary') && /trust|privacy|data|fund/.test(hay)) score+=28;
    if(intents.includes('registry') && /registry|all pages|search/.test(hay)) score+=18;
    return score;
  }
  function buildMission(objective){
    const obj=(objective||'').trim() || 'Understand GoalOS and produce a review-ready public-safe objective plan.';
    const intents=classify(obj);
    const r=risk(obj);
    const id='GOALOS-MISSION-'+hash(obj+'|'+now()).toUpperCase();
    const routes=ROUTES.map(rt=>({...rt,score:routeScore(rt,obj,intents)})).filter(r=>r.score>0).sort((a,b)=>b.score-a.score).slice(0,6);
    if(!routes.length) routes.push(ROUTES[0],ROUTES[1],ROUTES[3]);
    const gates=gateDefs.map(([key,label])=>({key,label,passed:key==='humanReview'?false:!r.level.startsWith('BLOCKED')}));
    const decision=r.level.startsWith('BLOCKED')?'BLOCK_BOUNDARY_REVISE_INPUT':(r.level==='HIGH_REVIEW_REQUIRED'?'HOLD_HUMAN_REVIEW_REQUIRED':'MISSION_PLAN_REVIEW_READY');
    const artifacts=[
      'Mission Contract','Claims Matrix','Evidence Docket Plan','Verifier Checklist','Risk Ledger','Action Graph','Chronicle Entry','Capability Package'
    ];
    const steps=[
      'Clarify objective and decision to support.',
      'Convert objective into a Mission Contract with success criteria and constraints.',
      'Generate claims matrix: what is claimed, not claimed, and what evidence is required.',
      'Route to the correct GoalOS pages, demos, proof rooms, or contract atlas.',
      'Assemble public-safe Evidence Docket plan and verifier checklist.',
      'Emit governed decision state, action graph, Chronicle stub, and reusable capability package.'
    ];
    return {schema:'goalos.objective-command-center.v20',id,createdAt:now(),objective:obj,intents,risk:r,decision,routes,gates,artifacts,steps,boundary:'No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.'};
  }
  let current=null, timer=null;
  function render(m){
    current=m;
    $('decision').textContent=m.decision;
    $('risk').textContent=m.risk.level;
    $('routes').textContent=m.routes.length+' routes';
    $('missionId').textContent=m.id.replace('GOALOS-MISSION-','');
    const lines=[];
    lines.push('01 Objective received.');
    lines.push('02 Mission Contract drafted.');
    lines.push('03 Claims Matrix prepared.');
    lines.push('04 Evidence Docket plan assembled.');
    lines.push('05 Route candidates scored.');
    if(m.risk.hits.length) lines.push('06 Boundary terms detected: '+m.risk.hits.join(', '));
    lines.push('07 Governed Decision State: '+m.decision);
    $('terminal').textContent=lines.join('\n');
    $('gateGrid').innerHTML=m.gates.map(g=>`<div class="state-card"><small>${g.passed?'PASS':'REVIEW'}</small><strong>${g.label}</strong><span>${g.key==='humanReview'?'required before authority':'browser-local gate'}</span></div>`).join('');
    $('routeList').innerHTML=m.routes.map(r=>`<a class="route-card" href="${r.url}"><span><strong>${escapeHtml(r.title)}</strong><br><small>${escapeHtml(r.why)}</small></span><small>${Math.min(99,r.score)}%</small></a>`).join('');
    $('planSteps').innerHTML=m.steps.map(s=>`<div class="step"><div><strong>${escapeHtml(s)}</strong><p>${explainStep(s,m)}</p></div></div>`).join('');
  }
  function explainStep(step,m){
    if(step.includes('Mission Contract')) return 'The objective becomes bounded work with success criteria, risk class, allowed actions, and done conditions.';
    if(step.includes('claims')) return 'Unsupported claims are kept out until evidence, baselines, replay, and review exist.';
    if(step.includes('Route')) return 'GoalOS sends the user to the correct existing proof room instead of making them browse blindly.';
    if(step.includes('Evidence')) return 'The proof package is prepared as a review surface, not a marketing page.';
    if(step.includes('decision')) return 'The output is an inspectable state: review-ready, blocked, or human-review-required.';
    return 'The user enters plain text; the console converts it into a governed proof path.';
  }
  function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  function toast(msg){const t=$('toast'); if(!t)return; t.textContent=msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'),1800)}
  function download(name, content, type){
    const blob=new Blob([content],{type:type||'application/json'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob); a.download=name; document.body.appendChild(a); a.click();
    setTimeout(()=>{URL.revokeObjectURL(a.href); a.remove();},200);
  }
  function markdown(m){return `# ${m.id}\n\n## Objective\n${m.objective}\n\n## Decision State\n${m.decision}\n\n## Risk\n${m.risk.level}\n\n## Boundary\n${m.boundary}\n\n## Recommended Routes\n${m.routes.map(r=>`- [${r.title}](${r.url}) — ${r.why}`).join('\n')}\n\n## Steps\n${m.steps.map((s,i)=>`${i+1}. ${s}`).join('\n')}\n`;}
  function csv(m){return 'step,artifact,status\n'+m.artifacts.map((a,i)=>`${i+1},"${a}",drafted`).join('\n')+'\n';}
  function run(){render(buildMission($('objective').value));}
  function animate(){
    if(!current) run();
    const phases=['OBJECTIVE_RECEIVED','MISSION_CONTRACT_BOUND','EVIDENCE_PLAN_READY','ROUTES_SELECTED','HUMAN_REVIEW_REQUIRED','CHRONICLE_READY'];
    let i=0; clearInterval(timer); $('terminal').textContent='00 Starting browser-local Mission OS cycle...\n';
    timer=setInterval(()=>{ $('terminal').textContent += String(i+1).padStart(2,'0')+' '+phases[i]+'\n'; i++; if(i>=phases.length){clearInterval(timer); $('terminal').textContent+='DONE '+current.decision+'\n';}},380);
  }
  function bind(){
    if(!$('objective')) return;
    document.querySelectorAll('[data-prompt]').forEach(b=>b.addEventListener('click',()=>{ $('objective').value=b.getAttribute('data-prompt'); run(); }));
    $('runMission').addEventListener('click',run);
    $('simulate').addEventListener('click',animate);
    $('downloadJson').addEventListener('click',()=>{if(!current)run(); download(current.id.toLowerCase()+'.json',JSON.stringify(current,null,2),'application/json')});
    $('downloadMd').addEventListener('click',()=>{if(!current)run(); download(current.id.toLowerCase()+'.md',markdown(current),'text/markdown')});
    $('downloadCsv').addEventListener('click',()=>{if(!current)run(); download(current.id.toLowerCase()+'-action-graph.csv',csv(current),'text/csv')});
    $('openNext').addEventListener('click',()=>{if(!current)run(); location.href=current.routes[0].url;});
    $('objective').addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key==='Enter')run();});
    document.addEventListener('keydown',e=>{ if(e.key==='/' && !/input|textarea/i.test(document.activeElement.tagName)){ e.preventDefault(); $('objective').focus(); }});
    run();
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',bind); else bind();
})();
