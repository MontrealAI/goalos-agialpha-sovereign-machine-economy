from pathlib import Path
import json, datetime, re
ROOT=Path.cwd(); NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
required=['public/action-reason-trace-contract.html','public/assets/goalos-action-reason-trace-v1.css','public/assets/goalos-action-reason-trace-v1.js','docs/demos/ACTION_REASON_TRACE_CONTRACT_V1.md','docs/reviewer/HOW_TO_REVIEW_ACTION_REASON_TRACE_CONTRACT.md','evidence/demo/action-reason-trace-contract-v1-reference-docket.json']
errors=[]
for r in required:
    if not (ROOT/r).exists(): errors.append(f'missing {r}')
js=(ROOT/'public/assets/goalos-action-reason-trace-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-action-reason-trace-v1.js').exists() else ''
for token in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if token in js: errors.append(f'forbidden browser API detected: {token}')
html=(ROOT/'public/action-reason-trace-contract.html').read_text(encoding='utf-8') if (ROOT/'public/action-reason-trace-contract.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase.lower() not in html.lower(): errors.append(f'missing boundary phrase: {phrase}')
report={"status":"failed" if errors else "passed","generatedAt":NOW,"errors":errors,"browserLocal":True,"noNetworkCall":not any(x in js for x in ['fetch(','XMLHttpRequest','sendBeacon']),"noUserData":True,"noUserFunds":True,"walletOrMainnet":False,"humanReviewRequired":True}
p=ROOT/'reports/action-reason-trace-contract-v1-qa.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(1 if errors else 0)
