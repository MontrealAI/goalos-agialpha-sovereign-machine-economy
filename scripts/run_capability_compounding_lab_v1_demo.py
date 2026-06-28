from pathlib import Path
import json, datetime
root=Path.cwd()
(root/'reports').mkdir(exist_ok=True)
(root/'evidence/demo').mkdir(parents=True,exist_ok=True)
report={
 'schema':'goalos.capability_compounding_lab.v1.demo_run',
 'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',
 'status':'passed',
 'demo':'capability-compounding-lab.html',
 'browser_local':True,
 'no_user_data':True,
 'no_user_funds':True,
 'gates':['mission_contract','claims_matrix','evidence_docket','replay_path','validator_report','cost_risk_ledger','claim_boundary','chronicle_entry','capability_package','rollback_plan','human_review'],
 'decision_state':'CAPABILITY_READY_FOR_HUMAN_REVIEW_REFERENCE'
}
(root/'reports/capability-compounding-lab-v1-demo-run.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(root/'evidence/demo/capability-compounding-lab-v1-reference-docket.json').write_text(json.dumps({
 'schema':'goalos.capability_compounding_lab.v1.reference_docket',
 'generated_at':report['generated_at'],
 'status':'reference_demo',
 'claim':'Verified work can become reusable capability only after proof gates pass.',
 'boundary':['no user data','no user funds','no wallet','no transaction','no network call','human review required']
},indent=2)+'\n',encoding='utf-8')
print('Capability Compounding Lab V1 reference demo generated')
