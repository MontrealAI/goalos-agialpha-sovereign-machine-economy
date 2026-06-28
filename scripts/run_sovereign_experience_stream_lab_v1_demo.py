from pathlib import Path
import json, datetime
Path('evidence/demo').mkdir(parents=True, exist_ok=True)
Path('reports').mkdir(exist_ok=True)
docket={"schema":"goalos.sovereign_experience_stream.v1","generated_at":datetime.datetime.now(datetime.UTC).isoformat(),"demo":"sovereign-experience-stream-lab-v1","experience_tuple":"e_t=(state,action,observation,reward,validator,cost,risk,memory)","events":[{"event_id":"EXP-001","state":"public_safe_task","action":"bounded_review","observation":"proof_packet","reward":"validator_signal","validator":"accepted_for_review","cost":{"network_calls":0},"risk":{"critical_violations":0},"memory":"chronicle_candidate"}],"boundary":["no_user_data","no_user_funds","no_wallet","no_transaction","no_network_call","human_review_required"]}
Path('evidence/demo/sovereign-experience-stream-lab-v1-reference-docket.json').write_text(json.dumps(docket,indent=2))
Path('reports/sovereign-experience-stream-lab-v1-demo-run.json').write_text(json.dumps({"status":"passed","artifact":"evidence/demo/sovereign-experience-stream-lab-v1-reference-docket.json"},indent=2))
print('sovereign experience demo generated')
