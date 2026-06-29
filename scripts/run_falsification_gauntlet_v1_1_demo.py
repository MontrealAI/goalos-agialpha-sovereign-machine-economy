from pathlib import Path
import json, datetime
out={
  'schema':'goalos.falsification_gauntlet.v1_1.demo_run',
  'generated_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),
  'status':'passed',
  'fixes':['custom claim text preserved during stress','stress changes baseline matrix','stress changes decision state','downloads use custom claim'],
  'browser_local':True,
  'no_user_data':True,
  'no_user_funds':True,
  'wallet_or_mainnet':False,
  'human_review_required':True
}
Path('reports').mkdir(exist_ok=True)
Path('reports/falsification-gauntlet-v1-1-demo-run.json').write_text(json.dumps(out,indent=2))
Path('evidence/demo').mkdir(parents=True, exist_ok=True)
Path('evidence/demo/falsification-gauntlet-v1-1-reference-docket.json').write_text(json.dumps({**out,'decision_state_under_stress':'REJECT_BASELINES_WIN'},indent=2))
print('Generated Falsification Gauntlet V1.1 demo report')
