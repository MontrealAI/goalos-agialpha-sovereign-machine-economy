
(function(){
  const routes = (window.GOALOS_SITE_INDEX || []);
  const steps = [
    ["Explore","Find routes","01 - Route inventory loaded.\n02 - All pages discoverable.\n03 - Pick a role or search /."],
    ["Proof","Docket gates","01 - Claims require evidence.\n02 - Baselines and replay visible.\n03 - Human review required."],
    ["LoopRSI","Govern invention","01 - Loop writes state.\n02 - Recorder leaves proof.\n03 - RSI gates recursive improvement."],
    ["Review","Validator path","01 - Inspect docket.\n02 - Replay artifacts.\n03 - Accept, reject, revise, or dissent."],
    ["Trust","Boundary","01 - No user data.\n02 - No wallet.\n03 - No transaction.\n04 - No production authority."],
    ["Build","Source and QA","01 - Site source committed.\n02 - Route health audited.\n03 - Pages deployed after review."]
  ];
  function $(id){ return document.getElementById(id); }
  function escapeHtml(s){ return String(s||"").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;"}[c])); }
  function openPalette(){ let pal=$("goalosV16Palette"); if(!pal){createPalette(); pal=$("goalosV16Palette");} pal.classList.add("open"); const input=$("goalosV16PaletteInput"); setTimeout(()=>input&&input.focus(),20); renderPalette("");}
  function closePalette(){ const pal=$("goalosV16Palette"); if(pal) pal.classList.remove("open"); }
  function renderPalette(q){ const box=$("goalosV16PaletteResults"); if(!box) return; const query=(q||"").trim().toLowerCase(); const filtered=routes.filter(r=>!query||(r.title+" "+r.path+" "+r.category+" "+r.description).toLowerCase().includes(query)).slice(0,60); box.innerHTML=filtered.length?filtered.map(r=>`<a href="${r.path}"><small>${escapeHtml(r.category||"Route")}</small><div><b>${escapeHtml(r.title)}</b><p>${escapeHtml(r.description||r.path)}</p></div></a>`).join(""):`<p style="color:#fff;padding:14px">No route found. Try RSI, loop, proof, docket, token, or mission.</p>`;}
  function createPalette(){ const div=document.createElement("div"); div.id="goalosV16Palette"; div.innerHTML=`<div class="v16-palette-box" role="dialog" aria-label="GoalOS command palette"><input id="goalosV16PaletteInput" placeholder="Search GoalOS routes: RSI, loop, proof, token, mission..." autocomplete="off"/><div class="v16-palette-results" id="goalosV16PaletteResults"></div><p style="color:#cbd7e7;margin:12px 6px 0;font:800 12px Inter,system-ui,sans-serif">Esc closes. Browser-local. No network call. No analytics.</p></div>`; document.body.appendChild(div); div.addEventListener("click",e=>{ if(e.target===div) closePalette(); }); const input=div.querySelector("input"); input.addEventListener("input",e=>renderPalette(e.target.value));}
  function createDock(){ if($("goalosV16Dock")) return; const dock=document.createElement("div"); dock.id="goalosV16Dock"; dock.innerHTML=`<button type="button" id="goalosV16PaletteButton">Search /</button><a href="site-map.html">All pages</a>`; document.body.appendChild(dock); $("goalosV16PaletteButton").addEventListener("click",openPalette);}
  function wireConsole(){ const rail=document.querySelectorAll("[data-v16-mode]"); const term=$("v16Terminal"); if(!rail.length||!term) return; function activate(i){rail.forEach(b=>b.classList.remove("active")); rail[i].classList.add("active"); term.textContent=steps[i][2];} rail.forEach((b,i)=>b.addEventListener("click",()=>activate(i))); let i=0; activate(0); setInterval(()=>{ if(document.hidden) return; i=(i+1)%rail.length; activate(i);},4200);}
  function wireSearch(){ const input=$("v16RouteSearch"), out=$("v16RouteList"); if(!input||!out) return; function render(){ const q=input.value.toLowerCase().trim(); const xs=routes.filter(r=>!q||(r.title+" "+r.category+" "+r.description+" "+r.path).toLowerCase().includes(q)).slice(0,140); out.innerHTML=xs.map(r=>`<a class="v16-row" href="${r.path}"><span>${escapeHtml(r.category)}</span><div><b>${escapeHtml(r.title)}</b><p>${escapeHtml(r.description)}</p></div><em>Open →</em></a>`).join(""); } input.addEventListener("input",render); render();}
  document.addEventListener("keydown",e=>{ if(e.key==="/"&&!/input|textarea|select/i.test((e.target||{}).tagName||"")){e.preventDefault();openPalette();} if(e.key==="Escape") closePalette();});
  document.addEventListener("DOMContentLoaded",()=>{createDock();createPalette();wireConsole();wireSearch();});
})();
