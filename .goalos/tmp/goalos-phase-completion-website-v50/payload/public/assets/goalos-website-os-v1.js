
(function(){
  "use strict";
  var data = window.GOALOS_SITE_INDEX || {routes:[]};
  function ready(fn){ if(document.readyState !== "loading") fn(); else document.addEventListener("DOMContentLoaded", fn); }
  function el(tag, cls, text){ var n=document.createElement(tag); if(cls)n.className=cls; if(text)n.textContent=text; return n; }
  function makePalette(){
    if(document.getElementById("goalos-command-palette")) return;
    var skip=el("a","goalos-skip","Skip to content"); skip.href="#main"; document.body.prepend(skip);
    var wrap=el("div","goalos-floating","");
    var btn=el("button","goalos-float-btn","Open site map");
    btn.type="button"; btn.setAttribute("aria-haspopup","dialog"); btn.setAttribute("aria-controls","goalos-command-palette");
    wrap.appendChild(btn); document.body.appendChild(wrap);
    var pal=el("div","goalos-palette",""); pal.id="goalos-command-palette"; pal.setAttribute("role","dialog"); pal.setAttribute("aria-label","GoalOS site navigation");
    var box=el("div","goalos-palette-box","");
    var head=el("div","goalos-palette-head","");
    var input=document.createElement("input"); input.type="search"; input.placeholder="Search demos, proof rooms, review paths, legal boundary…"; input.setAttribute("aria-label","Search GoalOS pages");
    var close=el("button","","Close"); close.type="button";
    head.appendChild(input); head.appendChild(close);
    var results=el("div","goalos-results","");
    box.appendChild(head); box.appendChild(results); pal.appendChild(box); document.body.appendChild(pal);
    function escapeHtml(s){ return String(s||"").replace(/[&<>"']/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); }
    function render(){
      var q=(input.value||"").toLowerCase().trim();
      var routes=(data.routes||[]).filter(function(r){
        var hay=[r.name,r.category,r.description,r.audience,(r.tags||[]).join(" ")].join(" ").toLowerCase();
        return !q || hay.indexOf(q)>=0;
      }).slice(0,80);
      results.innerHTML="";
      routes.forEach(function(r){
        var a=el("a","goalos-result","");
        a.href=r.href; a.innerHTML="<small>"+escapeHtml(r.category||"")+(r.status==="planned"?" · planned":"")+"</small><b>"+escapeHtml(r.name)+"</b><span>"+escapeHtml(r.description||"")+"</span>";
        results.appendChild(a);
      });
      if(!routes.length){ results.appendChild(el("div","goalos-result","No matching route.")); }
    }
    function open(){ pal.classList.add("open"); render(); setTimeout(function(){input.focus();},30); }
    function shut(){ pal.classList.remove("open"); }
    btn.addEventListener("click", open);
    close.addEventListener("click", shut);
    input.addEventListener("input", render);
    pal.addEventListener("click", function(e){ if(e.target===pal) shut(); });
    document.addEventListener("keydown", function(e){
      if(e.key==="Escape") shut();
      if((e.key==="/" || e.key==="?") && !/INPUT|TEXTAREA|SELECT/.test((e.target||{}).tagName||"")){ e.preventDefault(); open(); }
    });
  }
  ready(function(){
    makePalette();
    if(!document.getElementById("main")){
      var main=document.querySelector("main");
      if(main) main.id="main";
    }
  });
})();
