from pathlib import Path
import json, datetime, hashlib
ROOT=Path('.')
mission={'name':'browser-local multi-agent institution demo','objective':'Compare unstructured swarm activity against proof-governed institutional work','boundary':['no_user_data','no_user_funds','no_wallet','no_transaction','human_review_required']}
gates=['Mission','Roles','Tools','Evidence','Validation','Risk','Claim','Decision','Chronicle','Capability']
report={'schema':'goalos.multi_agent_institution.demo_run.v6','generated_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'mission':mission,'gates':[{'gate':g,'status':'reference_pass'} for g in gates],'metrics':{'verified_work':82,'proof_integrity':88,'reuse_potential':79,'residual_risk':18,'coordination_overhead':31},'decision_state':'READY_FOR_VALIDATOR_REVIEW','artifact_hash':'pending'}
raw=json.dumps(report, sort_keys=True).encode(); report['artifact_hash']='sha256:'+hashlib.sha256(raw).hexdigest()
(ROOT/'evidence/demo').mkdir(parents=True, exist_ok=True)
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'evidence/demo/multi-agent-institution-v6-reference-docket.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
(ROOT/'reports/multi-agent-institution-v6-demo-run.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print('Generated multi-agent institution V6 demo artifacts')
