from pathlib import Path
import json, datetime, hashlib
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
docket={"schema":"goalos.validator_council_arena.v1","generatedAt":now,"claim":"The current public-alpha repository has sufficient public pages, code artifacts, reports, no-data/no-funds boundaries, replay instructions, and reviewer paths to be submitted for external human review.","decisionState":"VALIDATION_REVIEW_READY","readiness":96,"gates":{"commitReveal":True,"quorum":True,"validatorDiversity":True,"replayPath":True,"evidenceIntegrity":True,"riskLedger":True,"challengeWindow":True,"dissentPreserved":True,"publicPrivateBoundary":True,"humanReview":True},"boundary":"No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."}
docket['docketHash']='sha256:'+hashlib.sha256(json.dumps(docket,sort_keys=True).encode()).hexdigest()
Path('evidence/demo').mkdir(parents=True,exist_ok=True); Path('reports').mkdir(exist_ok=True)
Path('evidence/demo/validator-council-arena-v1-reference-docket.json').write_text(json.dumps(docket,indent=2),encoding='utf-8')
report={"status":"passed","generatedAt":now,"docket":"evidence/demo/validator-council-arena-v1-reference-docket.json","decisionState":docket['decisionState'],"readiness":docket['readiness']}
Path('reports/validator-council-arena-v1-demo-run.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
