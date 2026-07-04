
(function(){
  const d=document;
  const routes=(window.GOALOS_ASK_ROUTES||[]).filter(r=>r&&r.url&&r.title);
  const boundary='No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.';
  const synonyms={
    start:['start','begin','new','first','guide','onboard','how'],
    proof:['proof','evidence','docket','claim','claims','review','verify','validator','ledger','audit'],
    mainnet:['mainnet','ethereum','contract','contracts','48','chainid','etherscan','address','rail'],
    token:['token','agialpha','$agialpha','wallet','investment','available','buy','sell'],
    trust:['trust','privacy','data','funds','wallet','transaction','gdpr','secret','boundary'],
    loop:['loop','prompt','contract','restart','trace','bottleneck','flight'],
    rsi:['rsi','omni','move37','move-37','state capacity','sovereign','invention','governance'],
    mission:['mission','action','objective','decision','chronicle','work'],
    all:['all','pages','map','registry','find','route','missing','search'],
    node:['node','agent','jobs','runtime','work','settlement']
  };
  function norm(s){return String(s||'').toLowerCase().replace(/[^a-z0-9$]+/g,' ').trim()}
  function toks(s){return norm(s).split(/\s+/).filter(Boolean)}
  function expand(q){let t=toks(q); Object.keys(synonyms).forEach(k=>{if(t.includes(k)||synonyms[k].some(x=>norm(q).includes(x))) t=t.concat(synonyms[k])}); return [...new Set(t)]}
  function scoreRoute(r, qtokens, raw){
    const hay=norm([r.title,r.url,r.category,r.description,(r.keywords||[]).join(' ')].join(' '));
    let s=0; qtokens.forEach(t=>{ if(!t)return; if(hay.includes(t)) s+= t.length>4?4:2; if(norm(r.title).includes(t)) s+=3; if(norm(r.url).includes(t)) s+=4; });
    if(raw.includes('contract') && r.url.includes('mainnet')) s+=10;
    if(raw.includes('48') && r.url.includes('mainnet')) s+=12;
    if(raw.includes('token') && r.url.includes('token')) s+=12;
    if(raw.includes('rsi') && r.url.includes('rsi')) s+=10;
    if(raw.includes('loop') && r.url.includes('loop')) s+=8;
    if(raw.includes('start') && r.url.includes('start')) s+=12;
    if(raw.includes('privacy') && (r.url.includes('privacy')||r.url.includes('trust'))) s+=10;
    return s;
  }
  function answerText(q, matches){
    const raw=norm(q);
    if(/wallet|fund|buy|sell|investment|token|agialpha/.test(raw)) return 'Boundary first: GoalOS does not sell, custody, support, or make available $AGIALPHA. I can route you to the token boundary and contract atlas.';
    if(/48|mainnet|ethereum|contract|etherscan/.test(raw)) return 'Best route: the Mainnet Contract Atlas. It explains the 48 GoalOS-created Ethereum Mainnet contracts, their proof rails, and the canonical external AGIALPHA entry.';
    if(/data|privacy|gdpr|secret|confidential|user data/.test(raw)) return 'GoalOS is proof-native, not data-hungry. Public demos are browser-local and should not receive personal, customer, confidential, wallet, credential, or regulated data.';
    if(/rsi|omni|move|sovereign invention/.test(raw)) return 'Best route: the Loop → RSI path. It shows how loops become deterministic invention governance: schema-bound artifacts, baselines, ECI, dossiers, and council review.';
    if(/loop|restart|trace|bottleneck|prompt/.test(raw)) return 'Best route: the Loop demos. They show why long-running agent systems need contracts, disk state, traces, restarts, and bottleneck visibility.';
    if(/proof run|docket|evidence|claim|validator|review/.test(raw)) return 'Best route: Proof Run 001 and the evidence rooms. They show claims, gates, validator review, replay paths, and public-safe dockets.';
    if(/start|begin|new|non technical|how/.test(raw)) return 'Start here: choose your role, then follow the shortest path. I will route you to onboarding, Pathfinder, or the demo registry.';
    if(!matches.length) return 'I did not find an exact route. Try “contracts”, “RSI”, “Proof Run 001”, “privacy”, “Loop”, “validator”, or “start”.';
    return 'I found the best public route for that question. Choose one below or ask a follow-up.';
  }
  function find(q){const raw=norm(q); const qtokens=expand(q); return routes.map(r=>({...r,_score:scoreRoute(r,qtokens,raw)})).filter(r=>r._score>0&&r.state!=='SYSTEM').sort((a,b)=>b._score-a._score).slice(0,5)}
  function el(tag, cls, text){const x=d.createElement(tag); if(cls)x.className=cls; if(text!==undefined)x.textContent=text; return x}
  function addMsg(kind, content){const body=d.getElementById('goalos-ask-body'); if(!body)return; const m=el('div','ga-ask-msg '+kind); if(typeof content==='string')m.textContent=content; else m.appendChild(content); body.appendChild(m); body.scrollTop=body.scrollHeight}
  function routeCards(matches){const wrap=el('div'); if(!matches.length){const quick=el('div','ga-quick'); ['Start','Proof Run 001','48 contracts','Loop to RSI','Privacy'].forEach(q=>{const b=el('button','ga-chip',q); b.type='button'; b.addEventListener('click',()=>ask(q)); quick.appendChild(b)}); wrap.appendChild(quick); return wrap}
    matches.forEach((r,i)=>{const card=el('div','ga-route-card'); card.appendChild(el('strong','',r.title)); card.appendChild(el('small','',r.description||r.category)); const actions=el('div','ga-route-actions'); const open=el('button','ga-open-route', i===0?'Open best route →':'Open →'); open.type='button'; open.addEventListener('click',()=>{window.location.href=r.url}); const copy=el('button','ga-copy-route','Copy path'); copy.type='button'; copy.addEventListener('click',()=>{try{navigator.clipboard&&navigator.clipboard.writeText(r.url)}catch(e){}}); actions.appendChild(open); actions.appendChild(copy); card.appendChild(actions); wrap.appendChild(card)}); return wrap}
  function ask(q){q=String(q||'').trim(); if(!q)return; addMsg('user',q); const matches=find(q); addMsg('bot',answerText(q,matches)); addMsg('bot',routeCards(matches)); if(/^(open|go|take me|redirect|send me)/i.test(q)&&matches[0]) setTimeout(()=>{window.location.href=matches[0].url},650)}
  function openPanel(){d.getElementById('goalos-ask-panel')?.classList.add('ga-open'); const inp=d.getElementById('goalos-ask-input'); setTimeout(()=>inp&&inp.focus(),80)}
  function closePanel(){d.getElementById('goalos-ask-panel')?.classList.remove('ga-open')}
  function init(){
    if(d.getElementById('goalos-ask-panel')) return;
    const btn=el('button','', 'Ask GoalOS'); btn.id='goalos-ask-launcher'; btn.type='button'; btn.setAttribute('aria-haspopup','dialog'); btn.addEventListener('click',openPanel); d.body.appendChild(btn);
    const panel=el('section',''); panel.id='goalos-ask-panel'; panel.setAttribute('role','dialog'); panel.setAttribute('aria-label','Ask GoalOS route assistant');
    panel.innerHTML='<div class="ga-ask-head"><div class="ga-ask-brand"><div class="ga-orb"></div><div><strong>Ask GoalOS</strong><span>browser-local route assistant</span></div></div><button class="ga-ask-close" type="button" aria-label="Close">×</button></div><div class="ga-ask-body" id="goalos-ask-body"></div><div class="ga-ask-foot"><p class="ga-boundary">'+boundary+'</p><form class="ga-ask-form" id="goalos-ask-form"><input id="goalos-ask-input" class="ga-ask-input" autocomplete="off" placeholder="Ask: where are the 48 contracts? how do I start? what is RSI?"/><button class="ga-send" type="submit">Ask</button></form></div>';
    d.body.appendChild(panel); panel.querySelector('.ga-ask-close').addEventListener('click',closePanel); panel.querySelector('form').addEventListener('submit',e=>{e.preventDefault(); const i=d.getElementById('goalos-ask-input'); const q=i.value; i.value=''; ask(q)});
    addMsg('bot','Ask me anything about GoalOS and I will route you to the right public page. I answer from the local site map only: no model call, no network call, no stored chat.');
    const quick=el('div','ga-quick'); ['Start in 60 seconds','48 Mainnet contracts','Proof Run 001','Loop → RSI','Token boundary','No user data'].forEach(q=>{const b=el('button','ga-chip',q); b.type='button'; b.addEventListener('click',()=>ask(q)); quick.appendChild(b)}); addMsg('bot',quick);
    d.addEventListener('keydown',e=>{if(e.key==='/'&&!e.metaKey&&!e.ctrlKey&&!e.altKey){const tag=(d.activeElement&&d.activeElement.tagName||'').toLowerCase(); if(!['input','textarea'].includes(tag)){e.preventDefault(); openPanel()}} if(e.key==='Escape') closePanel()});
  }
  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',init); else init();
})();
