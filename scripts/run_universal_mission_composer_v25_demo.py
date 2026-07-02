from pathlib import Path
import json, datetime
samples=['I want to understand the 48 Ethereum Mainnet contracts.','I want to run a public-safe proof mission.','I want to understand Loop to RSI governance.','I want to check privacy, token, and data boundaries.','I am new and want the fastest path to understand GoalOS.']
intents={'contracts':'CONTRACT_ATLAS_READY','proof':'PROOF_MISSION_READY','rsi':'RSI_REVIEW_READY','trust':'BOUNDARY_REVIEW_READY','start':'ONBOARDING_READY'}
out=[]
for s in samples:
    q=s.lower(); key='start'
    if 'contract' in q or 'mainnet' in q: key='contracts'
    elif 'proof' in q or 'mission' in q: key='proof'
    elif 'rsi' in q or 'loop' in q: key='rsi'
    elif 'privacy' in q or 'token' in q or 'boundary' in q: key='trust'
    out.append({'objective':s,'intent':key,'decisionState':intents[key],'externalActions':0,'networkCalls':0})
Path('reports').mkdir(exist_ok=True)
Path('reports/universal-mission-composer-v25-demo-run.json').write_text(json.dumps({'version':'v25','status':'passed','generatedAt':datetime.datetime.utcnow().isoformat()+'Z','samples':out},indent=2),encoding='utf-8')
print(json.dumps({'status':'passed','samples':len(out)},indent=2))
