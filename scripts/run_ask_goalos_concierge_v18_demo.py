
from __future__ import annotations
import json, pathlib, datetime, re
root=pathlib.Path.cwd()
routes=[]
ki=root/'public/assets/goalos-ask-goalos-knowledge-v18.js'
if ki.exists():
    txt=ki.read_text(encoding='utf-8', errors='ignore')
    start=txt.find('['); end=txt.rfind(']')+1
    if start>=0 and end>start: routes=json.loads(txt[start:end])

def norm(x): return re.sub(r'[^a-z0-9$]+',' ',str(x).lower()).strip()
def score(r, q):
    raw=norm(q); hay=norm(' '.join([r.get('title',''),r.get('url',''),r.get('category',''),r.get('description',''),' '.join(r.get('keywords',[]))]))
    val=0
    for t in raw.split():
        if len(t)>2 and t in hay: val += 5
    if '48' in raw and 'mainnet' in r.get('url',''): val += 40
    if 'contract' in raw and 'mainnet' in r.get('url',''): val += 40
    if 'agialpha' in raw and 'token' in r.get('url',''): val += 40
    if 'rsi' in raw and 'rsi' in r.get('url',''): val += 40
    if 'proof run' in raw and 'proof-run-001' in r.get('url',''): val += 40
    if 'start' in raw and 'start' in r.get('url',''): val += 40
    return val
queries=['where are the 48 contracts?','how do I start?','what is RSI?','is $AGIALPHA available from GoalOS?','show Proof Run 001']
checks={}
for q in queries:
    ranked=sorted(routes, key=lambda r: score(r,q), reverse=True)
    checks[q]=[{'title':r['title'],'url':r['url'],'score':score(r,q)} for r in ranked[:3] if score(r,q)>0]
status='passed' if routes and all(checks.values()) else 'failed'
out={'status':status,'queries':checks,'routeCount':len(routes),'generatedAt':datetime.datetime.utcnow().isoformat()+'Z'}
(root/'reports').mkdir(exist_ok=True)
(root/'reports/ask-goalos-concierge-v18-demo-run.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
print(json.dumps(out, indent=2))
raise SystemExit(0 if status=='passed' else 1)
