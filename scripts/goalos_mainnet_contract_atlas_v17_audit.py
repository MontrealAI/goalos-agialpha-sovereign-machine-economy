import json, pathlib, re, sys
root=pathlib.Path.cwd()
required=['public/mainnet-contract-atlas.html','public/mainnet-proof-rail.html','public/contract-academy.html','content/goalos/mainnet-contracts-v4.4.0.json','reports/mainnet-contract-atlas-v17-qa.json']
missing=[p for p in required if not (root/p).exists()]
forbidden=['fetch(','XMLHttpRequest','sendBeacon','localStorage','sessionStorage','window.ethereum']
hits=[]
for p in [root/'public/assets/goalos-mainnet-contract-atlas-v17.js', root/'public/assets/goalos-mainnet-contract-data-v17.js']:
    t=p.read_text(errors='ignore')
    for f in forbidden:
        if f in t: hits.append({'file':str(p),'pattern':f})
status='passed' if not missing and not hits else 'failed'
report={'status':status,'missing':missing,'forbiddenBrowserApiHits':hits}
(root/'reports/mainnet-contract-atlas-v17-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if status!='passed': sys.exit(1)
