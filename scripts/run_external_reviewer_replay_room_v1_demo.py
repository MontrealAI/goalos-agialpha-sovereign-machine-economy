#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT=Path.cwd(); NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'evidence/reviewer-replay').mkdir(parents=True, exist_ok=True)
docket={
  'schema':'goalos.external_reviewer_replay.demo_run.v1','generated_at':NOW,'review_object':'Proof Run 001 rehearsal docket','browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True,
  'gates':{'evidence_docket':True,'replay_path':True,'baselines':True,'cost_risk_ledger':True,'claim_boundary':True,'validator_notes':True,'dissent_channel':True},
  'decision_state':'REVIEW_READY'
}
(ROOT/'evidence/reviewer-replay/external-reviewer-replay-room-v1-reference-docket.json').write_text(json.dumps(docket,indent=2))
(ROOT/'reports/external-reviewer-replay-room-v1-demo-run.json').write_text(json.dumps({'status':'passed','docket':'evidence/reviewer-replay/external-reviewer-replay-room-v1-reference-docket.json','generated_at':NOW},indent=2))
print('external reviewer replay demo generated')
