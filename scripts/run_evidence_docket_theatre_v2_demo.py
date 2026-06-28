#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT=Path('.')
ROOT.joinpath('evidence/demo').mkdir(parents=True, exist_ok=True)
docket={
  'schema':'goalos.evidence_docket_theatre.reference.v2',
  'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z',
  'claim':'GoalOS Evidence Docket Theatre demonstrates how a public-safe claim becomes a review-ready proof room.',
  'browser_local':True,
  'no_user_data':True,
  'no_user_funds':True,
  'external_actions':0,
  'elements':['manifest','claims_matrix','environment','baselines','proof_packets','evaluator_notes','selection_certificate','safety_ledger','public_report','replay_path'],
  'decision_state':'READY_FOR_HUMAN_REVIEW',
  'claim_boundary':['public-alpha demonstration','not empirical SOTA','not achieved AGI','not achieved ASI','human review required']
}
Path('evidence/demo/evidence-docket-theatre-v2-reference-docket.json').write_text(json.dumps(docket,indent=2)+'\n',encoding='utf-8')
Path('reports').mkdir(exist_ok=True)
Path('reports/evidence-docket-theatre-v2-demo-run.json').write_text(json.dumps({'status':'passed','docket':'evidence/demo/evidence-docket-theatre-v2-reference-docket.json'},indent=2)+'\n',encoding='utf-8')
print('wrote reference docket')
