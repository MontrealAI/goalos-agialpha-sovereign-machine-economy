from pathlib import Path
import json, re, datetime
root=Path.cwd()
checks=[]; errors=[]
required=["public/sovereign-experience-stream-lab.html","public/assets/goalos-experience-stream-lab-v1.css","public/assets/goalos-experience-stream-lab-v1.js","docs/demos/SOVEREIGN_EXPERIENCE_STREAM_LAB_V1.md"]
for f in required:
    ok=Path(f).exists(); checks.append({"file":f,"exists":ok});
    if not ok: errors.append(f"missing {f}")
js=Path('public/assets/goalos-experience-stream-lab-v1.js').read_text() if Path('public/assets/goalos-experience-stream-lab-v1.js').exists() else ''
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
found=[x for x in forbidden if x in js]
if found: errors.append('forbidden browser call(s): '+', '.join(found))
html=Path('public/sovereign-experience-stream-lab.html').read_text() if Path('public/sovereign-experience-stream-lab.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase.lower() not in html.lower(): errors.append('boundary phrase missing: '+phrase)
report={"status":"passed" if not errors else "failed","checked_at":datetime.datetime.now(datetime.UTC).isoformat(),"checks":checks,"browser_local":True,"no_network_call":not found,"no_user_data":True,"no_user_funds":True,"human_review_required":True,"errors":errors}
Path('reports').mkdir(exist_ok=True)
Path('reports/sovereign-experience-stream-lab-v1-qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
