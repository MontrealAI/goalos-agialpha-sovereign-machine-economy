from pathlib import Path
import json, datetime
ROOT=Path('.')

def main():
    (ROOT/'evidence/demo').mkdir(parents=True,exist_ok=True)
    (ROOT/'reports').mkdir(exist_ok=True)
    docket={
      'schema':'goalos.falsification_gauntlet.v1',
      'generated_at':datetime.datetime.now(datetime.UTC).isoformat().replace('+00:00','Z'),
      'claim':'A claim should be promoted only after baselines, replay, privacy, cost/risk, validators, claim boundary, delayed-outcome plan, and human review are present.',
      'baseline_scores':{'B0':31,'B1':38,'B2':46,'B3':58,'B4':65,'B5':71,'B6':76},
      'decision_state':'HOLD_DELAYED_OUTCOME_PLAN_REQUIRED',
      'boundary':{'no_user_data':True,'no_user_funds':True,'no_wallet':True,'no_transaction':True,'no_network_call':True,'human_review_required':True}
    }
    (ROOT/'evidence/demo/falsification-gauntlet-v1-reference-docket.json').write_text(json.dumps(docket,indent=2),encoding='utf-8')
    report={'status':'passed','demo':'falsification-gauntlet-v1','artifacts':['evidence/demo/falsification-gauntlet-v1-reference-docket.json']}
    (ROOT/'reports/falsification-gauntlet-v1-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__': main()
