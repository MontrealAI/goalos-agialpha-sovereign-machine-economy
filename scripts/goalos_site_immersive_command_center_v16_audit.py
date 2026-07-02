#!/usr/bin/env python3
from pathlib import Path
import json, re, datetime
root=Path.cwd(); public=root/"public"
required=["index.html","start-here.html","pathfinder.html","site-map.html","demo-ecosystem-registry.html","search.html","site-health.html","trust-boundary.html","token-boundary.html","from-loop-to-rsi-state-capacity.html"]
missing=[p for p in required if not (public/p).exists()]
forbidden=["fetch(","XMLHttpRequest","sendBeacon","localStorage","sessionStorage","window.ethereum"]
hits=[]
for p in [public/"assets/goalos-site-immersive-command-center-v16.js", public/"assets/goalos-site-index-data-v16.js"]:
    if p.exists():
        text=p.read_text(errors="ignore")
        for f in forbidden:
            if f in text: hits.append({"file":str(p),"token":f})
pages={p.name for p in public.glob("*.html")}
broken=[]
for p in public.glob("*.html"):
    text=p.read_text(errors="ignore")
    for href in re.findall(r"href=[\"\']([^\"\']+)[\"\']", text):
        if href.startswith(("#","http","mailto:","tel:","javascript:")): continue
        target=href.split("#")[0].split("?")[0]
        if target.endswith(".html") and Path(target).name not in pages:
            broken.append({"page":p.name,"href":href})
index_text=(public/"index.html").read_text(errors="ignore") if (public/"index.html").exists() else ""
boundary_ok = "No user data" in index_text and "No user funds" in index_text and "No wallet" in index_text
status="passed" if not missing and not hits and not broken and boundary_ok else "failed"
report={"status":status,"generated_at":datetime.datetime.utcnow().isoformat()+"Z","missing":missing,"forbidden_browser_api_hits":hits,"broken_internal_html_links":broken,"boundary_ok":boundary_ok,"public_pages":len(pages)}
(root/"reports").mkdir(exist_ok=True)
(root/"reports/site-immersive-command-center-v16-audit.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
raise SystemExit(0 if status=="passed" else 1)
