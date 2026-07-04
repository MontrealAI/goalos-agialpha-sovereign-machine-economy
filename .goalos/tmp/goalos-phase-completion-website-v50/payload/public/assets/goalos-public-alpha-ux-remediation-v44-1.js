(function(){
  'use strict';
  const storage = Object.freeze({getItem(){return null;},setItem(){return undefined;},removeItem(){return undefined;},clear(){return undefined;},key(){return null;},get length(){return 0;}});
  function response(){return {ok:false,status:0,blocked:true,json:async()=>({blocked:true,boundary:'browser-local'}),text:async()=>''};}
  function blockedNetworkCall(){console.warn('[GoalOS boundary] Network calls are disabled in public-alpha browser-local demos.');return Promise.resolve(response());}
  function blockedBeacon(){console.warn('[GoalOS boundary] Beacon calls are disabled in public-alpha browser-local demos.');return false;}
  class BlockedLegacyRequest{constructor(){this.readyState=4;this.status=0;this.responseText='';}open(){}send(){if(typeof this.onerror==='function')this.onerror(new Error('Blocked by GoalOS boundary'));}setRequestHeader(){}addEventListener(){}getAllResponseHeaders(){return '';}getResponseHeader(){return null;}}
  window.GoalOSBoundary = Object.freeze({disabledStorage:storage,disabledWallet:null,blockedNetworkCall,blockedBeacon,BlockedLegacyRequest});
  function mark(){document.documentElement.setAttribute('data-goalos-ux-remediation','v44.1');}
  function inspect(){
    const flowSelectors=['.flowline','.visual-flow','.proof-flow','.mission-flow','.state-flow','.e2e-flow','.proof-path','.action-graph','.rail','.stage-rail'];
    const items=[]; flowSelectors.forEach(s=>document.querySelectorAll(s).forEach(el=>items.push(el)));
    document.documentElement.setAttribute('data-goalos-flow-surfaces', String(items.length));
    const boundaryText=(document.body.innerText||'').toLowerCase();
    const boundaryOk=boundaryText.includes('no user data') && boundaryText.includes('no wallet') && boundaryText.includes('no transaction');
    document.documentElement.setAttribute('data-goalos-boundary-visible', boundaryOk?'true':'review');
  }
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>{mark();inspect();});} else {mark();inspect();}
})();
