
(function(){
  window.GoalOSBoundary = Object.freeze({state:'browser-local', externalActions:0, wallet:false, transaction:false});
  window.goalos_no_network_call = function(){ return null; };
  window.local_Storage_disabled = {getItem(){return null},setItem(){},removeItem(){},clear(){}};
  window.session_Storage_disabled = window.local_Storage_disabled;
})();
