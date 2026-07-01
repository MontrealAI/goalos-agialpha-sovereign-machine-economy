from pathlib import Path
import json, datetime, re
ROOT=Path.cwd()
NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
page=ROOT/'public/from-loop-to-rsi-sovereign-console.html'
script=ROOT/'public/assets/goalos-from-loop-to-rsi-sovereign-console-v2.js'
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
errors=[]
if not page.exists(): errors.append('missing page')
if not script.exists(): errors.append('missing script')
text=page.read_text(encoding='utf-8') if page.exists() else ''
js=script.read_text(encoding='utf-8') if script.exists() else ''
for term in forbidden:
    if term in js: errors.append('forbidden browser API: '+term)
required=['No user data','No user funds','No wallet','No transaction','No network call','Human review required','Run RSI cycle','Move‑37','OMNI']
for term in required:
    if term not in text: errors.append('missing required text: '+term)
report={"status":"failed" if errors else "passed","generated_at":NOW,"errors":errors,"browser_local":True,"no_network_call":not any(t in js for t in forbidden),"no_user_data":"No user data" in text,"no_user_funds":"No user funds" in text,"human_review_required":"Human review required" in text}
p=ROOT/'reports/from-loop-to-rsi-sovereign-console-v2-qa.json'
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(1 if errors else 0)
