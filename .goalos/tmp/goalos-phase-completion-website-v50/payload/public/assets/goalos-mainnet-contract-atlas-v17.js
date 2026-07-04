
(function(){
  const data = window.GOALOS_MAINNET_CONTRACTS_V17 || {metadata:{},contracts:[]};
  const $ = (s,r=document)=>r.querySelector(s); const $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
  const contracts = data.contracts || [];
  const byName = new Map(contracts.map(c=>[c.name,c]));
  const categories = [...new Set(contracts.map(c=>c.category))];
  const html = (s)=>String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
  function linesForMode(mode){
    const m = data.metadata || {};
    const base = [`GoalOS Mainnet Atlas V17`, `${m.goalosCreatedContractCount||48} GoalOS-created contracts · ${m.manifestEntryCount||49} manifest entries`, `Ethereum Mainnet chainId ${m.chainId||1}`, `0 external actions · browser-local inspection`];
    const extra = {
      Explore:['Map the rails by category: vaults, workflow, governance, proof, economy, memory.', 'Click any contract to learn role, address, purpose, proof status, and boundary.'],
      Proof:['AEP rail: Commit → Run → Proof → Eval → Attest → Select → Rollout → Rollback → Chronicle.', 'Proof stays public-safe; private intelligence stays off-chain.'],
      Token:['AGIALPHA is canonical external contract identification only.', 'GoalOS did not deploy or mint a replacement AGIALPHA token.'],
      Review:['Reviewer task: verify address, category, purpose, source verification, and claim boundary.', 'Production activation, user funds, and external audit completion remain NO.'],
      Learn:['Start with the guided tour, filter by category, then use the quiz to test comprehension.', 'The goal is deep familiarity without requiring Solidity expertise.'],
      Boundary:['No wallet. No transaction. No network call. No production authority. Human review required.', 'Etherscan links are optional manual exits from the public site.']
    }[mode]||[];
    return base.concat(extra).map((x,i)=>String(i+1).padStart(2,'0')+' · '+x).join('\n');
  }
  function setMode(mode){
    $$('.rail button').forEach(b=>b.classList.toggle('active', b.dataset.mode===mode));
    const t=$('#terminal'); if(t) t.textContent=linesForMode(mode);
  }
  function renderStats(){
    const el=$('#stats'); if(!el) return;
    const m=data.metadata||{};
    el.innerHTML=[['GoalOS contracts',m.goalosCreatedContractCount||48],['Verified', (m.verification&&m.verification.verified)||48],['Manifest entries',m.manifestEntryCount||49],['Grants active',m.phaseBGrantCount||14],['External actions',0]].map(([a,b])=>`<div class="stat"><strong>${html(b)}</strong><span>${html(a)}</span></div>`).join('');
  }
  const categoryLabels={external:'External anchor',vault:'Vaults',workflow:'Work registries',governance:'Governance',optional:'Disputes & credentials',proof:'AEP proof rail',economy:'Economy & accountability',memory:'Chronicle memory'};
  function renderFilters(){
    const sel=$('#categoryFilter'); if(sel) sel.innerHTML='<option value="all">All rails</option>'+categories.map(c=>`<option value="${html(c)}">${html(categoryLabels[c]||c)} (${contracts.filter(x=>x.category===c).length})</option>`).join('');
  }
  function renderCards(){
    const q=($('#contractSearch')?.value||'').trim().toLowerCase();
    const cat=$('#categoryFilter')?.value||'all';
    const onlyCreated=$('#createdOnly')?.checked;
    const list=contracts.filter(c=>(cat==='all'||c.category===cat)&&(!onlyCreated||c.goalosCreated)&&(c.name.toLowerCase().includes(q)||c.address.toLowerCase().includes(q)||String(c.purpose).toLowerCase().includes(q)||String(c.category).toLowerCase().includes(q)));
    const grid=$('#contractGrid'); if(!grid) return;
    grid.innerHTML=list.map(c=>`<article class="card contract-card" data-name="${html(c.name)}"><div class="tag">${html(categoryLabels[c.category]||c.category)}</div>${c.goalosCreated?'<span class="tag">GoalOS-created</span>':'<span class="tag">external</span>'}<h3>${html(c.name)}</h3><p>${html(c.purpose)}</p><div class="meta">${html(c.shortAddress)}</div></article>`).join('') || '<div class="card"><h3>No matching contract</h3><p>Clear the search or choose another rail.</p></div>';
    $$('.contract-card',grid).forEach(card=>card.addEventListener('click',()=>selectContract(card.dataset.name)));
    $('#resultCount') && ($('#resultCount').textContent = `${list.length} visible`);
  }
  function selectContract(name){
    const c=byName.get(name)||contracts[0]; if(!c) return;
    $$('.contract-card').forEach(x=>x.classList.toggle('selected',x.dataset.name===c.name));
    const d=$('#contractDetail'); if(!d) return;
    d.innerHTML=`<div class="tag">${html(categoryLabels[c.category]||c.category)}</div>${c.goalosCreated?'<span class="tag">GoalOS-created</span>':'<span class="tag">canonical external</span>'}<h3>${html(c.name)}</h3><p>${html(c.purpose)}</p><p><strong>How to think about it:</strong> ${html(c.railExplanation)}</p><p><strong>Boundary:</strong> ${html(c.boundaryNote)}</p><p class="addr">${html(c.address)}</p><div class="cta"><button class="btn primary" data-copy="${html(c.address)}">Copy address</button><a class="btn" target="_blank" rel="noopener" href="${html(c.etherscanUrl)}">Open Etherscan</a>${c.transactionUrl?`<a class="btn" target="_blank" rel="noopener" href="${html(c.transactionUrl)}">Deployment tx</a>`:''}</div><p class="meta">verification: ${html(c.verificationStatus)} · constructor args: ${html(c.constructorArgsPresent)}</p>`;
    d.querySelector('[data-copy]')?.addEventListener('click', async (ev)=>{try{await navigator.clipboard.writeText(ev.currentTarget.dataset.copy); ev.currentTarget.textContent='Copied'; setTimeout(()=>ev.currentTarget.textContent='Copy address',1100)}catch(e){ev.currentTarget.textContent='Select address above'}});
  }
  function renderFlow(){
    const el=$('#flow'); if(!el) return;
    const flow=[['External anchor','AGIALPHA','Public contract identification only. Not available from GoalOS.'],['Reserve layer','Vaults','Resource and reserve surfaces; no user-fund authorization from this site.'],['Work layer','Job / Proof registries','Bound jobs, submissions, credentials, reputation, reviewers.'],['Proof layer','AEP contracts','Commit, run, prove, evaluate, attest, select, replay, rollout, rollback.'],['Economy layer','α-WU / staking / reward / slashing','Accountability and verified-work accounting.'],['Memory layer','Chronicle','Accepted proof becomes durable institutional memory.'],['Governance layer','Launch / config / claim boundary','Scope, configuration, claim discipline, and review states.'],['Boundary','Human review','No wallet, no transaction, no production authority.']];
    el.innerHTML=flow.map((x,i)=>`<article class="card"><div class="eyebrow">${String(i+1).padStart(2,'0')}</div><h3>${html(x[0])}</h3><p><strong>${html(x[1])}</strong></p><p>${html(x[2])}</p></article>`).join('');
  }
  function renderTours(){
    const tours={
      'nontechnical':['AGIALPHA identifies the external coordination asset.','Vaults and registries organize reserves, jobs, proofs, reviewers, and credentials.','AEP contracts make the proof lifecycle explicit.','Economy contracts account for work, stake, rewards, and accountability.','Chronicle records accepted institutional memory.','None of this page asks you for a wallet, funds, or data.'],
      'builder':['Start with AEPGoalOSCommitRegistry, AEPRunCommitmentRegistry, AEPProofLedger.','Then inspect AEPEvalRegistry, AEPAttestationRegistry, AEPSelectionGate.','Follow rollout and rollback through AEPRolloutRouter and AEPRollbackRegistry.','Use AEPReplayRegistry and AEPFalsificationRegistry to understand challengeability.','Use AGIEthNamespaceRegistry and AlphaWorkUnitLedger to understand identity and metrology.'],
      'reviewer':['Check release tag and chainId.','Confirm 48 GoalOS-created contracts and canonical external AGIALPHA.','Read verification status and postdeployment boundary.','Inspect no production activation, no user-fund authorization, no external audit completion.','Open Etherscan manually only when you want external source verification.'],
      'institution':['Treat the contracts as a public proof rail, not a wallet product.','Understand what can be public: hashes, attestations, roots, receipts, claim boundaries.','Understand what stays private: prompts, customer data, privileged workpapers.','Adopt the rail only through a human-reviewed Evidence Docket and legal/security review.']
    };
    const el=$('#tourList'); if(!el) return;
    el.innerHTML=Object.entries(tours).map(([k,steps])=>`<article class="card"><div class="eyebrow">${html(k)}</div><h3>${k==='nontechnical'?'For normal users':k==='builder'?'For builders':k==='reviewer'?'For reviewers':'For institutions'}</h3>${steps.map((s,i)=>`<p><strong>${i+1}.</strong> ${html(s)}</p>`).join('')}</article>`).join('');
  }
  function renderQuiz(){
    const el=$('#quiz'); if(!el) return;
    const qs=[['What does OMNI-like search or routing never receive?','Outcome authority','Direct promotion authority','Settlement bypass','All of the above',3],['What is the safest first interpretation of the 48 contracts?','Production wallet','Public proof rail','External audit','Investment product',1],['Which AEP pair explains controlled release?','RunCommitment + ProofSeed','RolloutRouter + RollbackRegistry','ReferralRegistry + SponsorRegistry','Vault + token',1]];
    el.innerHTML=qs.map((q,qi)=>`<div class="card"><h3>${html(q[0])}</h3><div class="quiz">${q.slice(1,5).map((a,i)=>`<button data-q="${qi}" data-a="${i}">${html(a)}</button>`).join('')}</div></div>`).join('');
    $$('button[data-q]',el).forEach(b=>b.addEventListener('click',()=>{const ok=Number(b.dataset.a)===qs[Number(b.dataset.q)][5]; b.classList.add(ok?'good':'bad'); b.textContent = (ok?'✓ ':'Review: ')+b.textContent;}));
  }
  function download(filename,text,type='application/json'){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=filename;document.body.appendChild(a);a.click();setTimeout(()=>{URL.revokeObjectURL(a.href);a.remove()},500)}
  function initDownloads(){
    $('#downloadJson')?.addEventListener('click',()=>download('goalos-mainnet-contracts-v4.4.0.json',JSON.stringify(data,null,2)));
    $('#downloadBrief')?.addEventListener('click',()=>download('goalos-mainnet-contract-atlas-reviewer-brief.md',`# GoalOS Mainnet Contract Atlas V17\n\n48 GoalOS-created Ethereum Mainnet contracts, 49 manifest entries including canonical external AGIALPHA.\n\nBoundary: ${data.metadata.publicAlphaBoundary}\n\nToken boundary: ${data.metadata.tokenBoundary}\n\n## Review checklist\n- Confirm release tag ${data.metadata.releaseTag}.\n- Confirm chainId ${data.metadata.chainId}.\n- Confirm 48/48 GoalOS-created contracts verified in release evidence.\n- Confirm production activation: NO.\n- Confirm user-fund authorization: NO.\n- Confirm external audit completion: NO.\n\n## Contracts\n`+contracts.map(c=>`- ${c.name}: ${c.address} (${c.category})`).join('\n'),'text/markdown'));
  }
  function openPalette(){const d=$('#drawer'); if(d) d.classList.add('open')}
  function closePalette(){const d=$('#drawer'); if(d) d.classList.remove('open')}
  function initPalette(){
    const d=$('#drawer'); if(!d) return;
    d.innerHTML=`<h3>Contract command palette</h3><p>Search by contract, rail, or address.</p><input id="drawerSearch" class="input" placeholder="Try ProofLedger, SelectionGate, vault, 0x..."/><div id="drawerResults"></div><p><span class="kbd">Esc</span> closes · <span class="kbd">/</span> opens</p>`;
    const input=$('#drawerSearch'); const results=$('#drawerResults');
    function draw(){const q=(input.value||'').toLowerCase(); const list=contracts.filter(c=>!q||c.name.toLowerCase().includes(q)||c.address.toLowerCase().includes(q)||c.category.toLowerCase().includes(q)||String(c.purpose).toLowerCase().includes(q)).slice(0,18); results.innerHTML=list.map(c=>`<div class="drawer-row"><div><strong>${html(c.name)}</strong><br><span class="meta">${html(c.category)} · ${html(c.shortAddress)}</span></div><a href="#atlas" data-pick="${html(c.name)}">Open</a></div>`).join('')||'<p>No match.</p>'; results.querySelectorAll('[data-pick]').forEach(a=>a.addEventListener('click',()=>{selectContract(a.dataset.pick); closePalette()}));}
    input.addEventListener('input',draw); draw();
    document.addEventListener('keydown',e=>{if(e.key==='/' && !/input|textarea|select/i.test(document.activeElement.tagName)){e.preventDefault(); openPalette(); setTimeout(()=>input.focus(),30)} if(e.key==='Escape') closePalette();});
    $$('.open-palette').forEach(b=>b.addEventListener('click',()=>{openPalette(); setTimeout(()=>input.focus(),30)}));
  }
  function init(){
    $$('.rail button').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode))); setMode('Explore');
    renderStats(); renderFilters(); renderCards(); renderFlow(); renderTours(); renderQuiz(); initDownloads(); initPalette(); selectContract('AEPProofLedger');
    $('#contractSearch')?.addEventListener('input',renderCards); $('#categoryFilter')?.addEventListener('change',renderCards); $('#createdOnly')?.addEventListener('change',renderCards);
  }
  document.addEventListener('DOMContentLoaded',init);
})();
