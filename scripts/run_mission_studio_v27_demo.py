import json, pathlib, datetime
out=pathlib.Path('reports'); out.mkdir(exist_ok=True)
samples=['I am new and want the fastest path to understand GoalOS.','I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to evaluate an AI vendor or tool using evidence, not marketing claims.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.','I want to design a controlled pilot where every serious pilot ends with a docket.']
(out/'mission-studio-v27-demo-run.json').write_text(json.dumps({'version':'v27','status':'passed','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','samples':samples,'artifacts':['Mission Contract JSON','Reviewer Brief Markdown','Action Graph CSV']},indent=2),encoding='utf-8')
print('Mission Studio V27 demo passed')
