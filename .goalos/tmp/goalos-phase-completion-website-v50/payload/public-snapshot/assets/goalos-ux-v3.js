(function(){
  function $(s,r){return (r||document).querySelector(s)}
  function $$(s,r){return Array.from((r||document).querySelectorAll(s))}
  document.addEventListener('click', async function(e){
    const b=e.target.closest('[data-copy]'); if(!b) return;
    const target=$(b.getAttribute('data-copy')); if(!target) return;
    try{await navigator.clipboard.writeText(target.innerText); b.textContent='Copied'; setTimeout(()=>b.textContent='Copy',1200)}catch{b.textContent='Select text'}
  });
  $$('.goalos-tour').forEach(function(tour){
    const steps=$$('.tour-step',tour), bar=$('.progress span',tour); let i=0;
    function show(){steps.forEach((s,k)=>s.classList.toggle('active',k===i)); if(bar)bar.style.width=((i+1)/steps.length*100)+'%'; const out=$('[data-tour-count]',tour); if(out)out.textContent=(i+1)+' / '+steps.length;}
    $('[data-tour-next]',tour)?.addEventListener('click',()=>{i=Math.min(steps.length-1,i+1);show()});
    $('[data-tour-prev]',tour)?.addEventListener('click',()=>{i=Math.max(0,i-1);show()}); show();
  });
})();
