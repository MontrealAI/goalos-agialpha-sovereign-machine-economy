#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
root=Path.cwd(); public=root/'public'
required=['autonomous-proof-factory.html','autonomous-work-os.html','autonomous-proof-gated-work-machine.html','until-done-autonomy-loop.html','autonomous-mission-queue-v9.html','state-on-disk-harness.html','agent-role-contracts.html','agi-node-validator-mesh-v9.html','proof-debt-dashboard-v9.html','chronicle-compounding-engine-v9.html','capability-promotion-gate-v9.html','autonomy-boundary-v9.html','autonomous-work-playbooks-v9.html','autonomous-mission-foundry-status-v9.html','autonomous-proof-factory-share-kit.html']
missing=[p for p in required if not (public/p).exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [public/x for x in required if (public/x).exists()]:
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for f in forbidden:
        if f in txt: hits.append({'file':str(p.relative_to(root)),'pattern':f})
links=[]
for p in [public/x for x in required if (public/x).exists()]:
    txt=p.read_text(encoding='utf-8',errors='ignore')
    for href in re.findall(r'href="([^"]+)"',txt):
        if href.startswith(('http','#','mailto:')): continue
        target=public/href.split('#')[0]
        if href and href.endswith('.html') and not target.exists(): links.append({'file':p.name,'href':href})
report={'required_missing':missing,'forbidden_public_hits':hits,'broken_internal_links':links,'public_html_count':len(list(public.glob('*.html'))),'passed':not missing and not hits and not links}
(root/'reports').mkdir(exist_ok=True); (root/'reports/goalos-autonomous-proof-factory-v9-audit.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if report['passed'] else 1)
