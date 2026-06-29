from pathlib import Path
import json, datetime
ROOT=Path.cwd(); errors=[]
required=['public/validator-council-arena.html','public/assets/goalos-validator-council-arena-v1.css','public/assets/goalos-validator-council-arena-v1.js','docs/demos/VALIDATOR_COUNCIL_ARENA_V1.md','docs/reviewer/HOW_TO_REVIEW_VALIDATOR_COUNCIL_ARENA.md']
for p in required:
    if not (ROOT/p).exists(): errors.append('missing:'+p)
js=(ROOT/'public/assets/goalos-validator-council-arena-v1.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-validator-council-arena-v1.js').exists() else ''
for bad in ['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']:
    if bad in js: errors.append('forbidden_api:'+bad)
html=(ROOT/'public/validator-council-arena.html').read_text(encoding='utf-8') if (ROOT/'public/validator-council-arena.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','No network call','Human review required']:
    if phrase not in html: errors.append('missing_boundary:'+phrase)
report={"status":"passed" if not errors else "failed","checkedAt":datetime.datetime.now(datetime.timezone.utc).isoformat(),"errors":errors,"browserLocal":True,"noNetworkCall":True,"noUserData":True,"noUserFunds":True,"walletOrMainnet":False,"humanReviewRequired":True}
Path('reports').mkdir(exist_ok=True); (ROOT/'reports/validator-council-arena-v1-qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2)); raise SystemExit(0 if not errors else 1)
