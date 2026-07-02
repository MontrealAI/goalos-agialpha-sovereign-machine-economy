
(function(){
  const routes = window.GOALOS_ROUTES_V15 || [];
  const modes = {
    Explore:"01 · Route inventory loaded.\n02 · Pick a role or press / to search every page.\n03 · Every preserved route points back to the command center.",
    Proof:"01 · Mission contract bounded.\n02 · Evidence Docket assembled.\n03 · Reviewer path ready; strong claims require replay.",
    "Loop→RSI":"01 · Loop state persisted.\n02 · Drift sentinel active.\n03 · OMNI allocates search; gates own outcome authority.",
    Review:"01 · Claims matrix open.\n02 · Baselines and validator notes visible.\n03 · Accept, reject, revise, or dissent.",
    Trust:"01 · No user data.\n02 · No user funds, wallet, or transaction.\n03 · Human review required.",
    Build:"01 · Website source aligned.\n02 · QA and route-health reports emitted.\n03 · Publish only after human review."
  };
  function $(s,root=document){return root.querySelector(s)}
  function $all(s,root=document){return Array.from(root.querySelectorAll(s))}
  function ensureCommand(){
    if($("#goalos-command-modal")) return;
    const modal=document.createElement("div");
    modal.id="goalos-command-modal"; modal.className="command-modal";
    modal.innerHTML='<div class="command-panel" role="dialog" aria-label="GoalOS command search"><input id="goalos-command-input" placeholder="Search GoalOS routes: RSI, loop, proof, token, validator…" autocomplete="off"><div id="goalos-command-results" class="command-results"></div></div>';
    document.body.appendChild(modal);
    modal.addEventListener("click",e=>{ if(e.target===modal) closeCommand(); });
    $("#goalos-command-input").addEventListener("input",renderCommand);
  }
  function openCommand(){ensureCommand();$("#goalos-command-modal").classList.add("open");$("#goalos-command-input").focus();renderCommand();}
  function closeCommand(){const m=$("#goalos-command-modal"); if(m)m.classList.remove("open");}
  function renderCommand(){
    const q=($("#goalos-command-input")?.value||"").toLowerCase().trim();
    const pool=routes.filter(r=>!r.system).filter(r=>!q || (r.title+" "+r.path+" "+r.category+" "+r.description).toLowerCase().includes(q)).slice(0,42);
    const out=$("#goalos-command-results"); if(!out)return;
    out.innerHTML=pool.map(r=>`<a class="command-item" href="${r.path}"><b>${escapeHtml(r.title)}</b><small>${escapeHtml(r.category)} · ${escapeHtml(r.description)}</small></a>`).join("") || '<div class="command-item"><b>No route found.</b><small>Try proof, RSI, loop, token, mission, validator, or docket.</small></div>';
  }
  function escapeHtml(s){return String(s).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m]));}
  document.addEventListener("keydown",e=>{
    if(e.key==="/" && !["INPUT","TEXTAREA"].includes(document.activeElement.tagName)){e.preventDefault();openCommand();}
    if(e.key==="Escape") closeCommand();
  });
  document.addEventListener("click",e=>{
    const btn=e.target.closest("[data-command]");
    if(btn){e.preventDefault();openCommand();}
    const mode=e.target.closest("[data-mode]");
    if(mode){const name=mode.dataset.mode;$all("[data-mode]").forEach(x=>x.classList.toggle("active",x===mode));const t=$("#console-log");if(t)t.textContent=modes[name]||modes.Explore;const label=$("#console-state");if(label)label.textContent=name;}
  });
  function initRouteFilters(){
    $all("[data-route-filter]").forEach(input=>{
      const target=$(input.getAttribute("data-route-filter"));
      input.addEventListener("input",()=>{
        const q=input.value.toLowerCase().trim();
        $all("[data-route]", target || document).forEach(el=>{
          el.style.display = !q || el.textContent.toLowerCase().includes(q) ? "" : "none";
        });
      });
    });
  }
  function cycle(){
    const buttons=$all("[data-mode]");
    if(!buttons.length)return;
    let i=0; setInterval(()=>{i=(i+1)%buttons.length;buttons[i].click();},4800);
  }
  document.addEventListener("DOMContentLoaded",()=>{ensureCommand();initRouteFilters();cycle(); const first=$("[data-mode]"); if(first)first.click();});
})();
