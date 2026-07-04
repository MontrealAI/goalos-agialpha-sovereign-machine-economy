#!/usr/bin/env python3
from pathlib import Path
import shutil,json,re,datetime
ROOT=Path.cwd(); SRC=Path(__file__).resolve().parents[1]
for d in ['public','content','schemas','docs','evidence','scripts','.goalos']:
    s=SRC/d
    if s.exists():
        for p in s.rglob('*'):
            if p.is_file():
                dest=ROOT/p.relative_to(SRC); dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dest)
(ROOT/'public').mkdir(exist_ok=True); (ROOT/'public/.nojekyll').write_text('',encoding='utf-8')
pages=sorted(p.name for p in (ROOT/'public').glob('*.html'))
(ROOT/'public/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(f'  <url><loc>{p}</loc></url>' for p in pages)+'\n</urlset>\n',encoding='utf-8')
idx=[]
for p in pages:
    txt=(ROOT/'public'/p).read_text(encoding='utf-8',errors='ignore'); title=re.search(r'<title>(.*?)</title>',txt,re.S); body=re.sub('<[^<]+?>',' ',txt)
    idx.append({'title':title.group(1) if title else p,'url':p,'content':re.sub(r'\s+',' ',body[:700]).strip()})
(ROOT/'public/search-index.json').write_text(json.dumps(idx,indent=2),encoding='utf-8')
reg=ROOT/'content/goalos-route-registry.json'; reg.parent.mkdir(exist_ok=True)
try: data=json.loads(reg.read_text(encoding='utf-8')) if reg.exists() else {'routes':[]}
except Exception: data={'routes':[]}
existing={r.get('url') for r in data.get('routes',[]) if isinstance(r,dict)}
new=['autonomous-proof-factory.html','autonomous-work-os.html','autonomous-proof-gated-work-machine.html','until-done-autonomy-loop.html','autonomous-mission-queue-v9.html','state-on-disk-harness.html','agent-role-contracts.html','agi-node-validator-mesh-v9.html','proof-debt-dashboard-v9.html','chronicle-compounding-engine-v9.html','capability-promotion-gate-v9.html','autonomy-boundary-v9.html','autonomous-work-playbooks-v9.html','autonomous-mission-foundry-status-v9.html','autonomous-proof-factory-share-kit.html']
for u in new:
    if u not in existing: data.setdefault('routes',[]).append({'title':'GoalOS '+u.replace('.html','').replace('-',' ').title(),'url':u,'version':'V9','group':'Autonomous Proof Factory'})
reg.write_text(json.dumps(data,indent=2),encoding='utf-8')
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/goalos-autonomous-proof-factory-v9-install-report.json').write_text(json.dumps({'installed_at':datetime.datetime.utcnow().isoformat()+'Z','pages':new},indent=2),encoding='utf-8')
print('GoalOS Autonomous Proof Factory V9 installed:',len(new),'new pages; total public pages:',len(pages))
