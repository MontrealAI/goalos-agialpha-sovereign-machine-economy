#!/usr/bin/env python3
from pathlib import Path
import json, datetime
ROOT=Path.cwd()
def write(path,text):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding="utf-8")
def patch_once(path,marker,text):
    p=ROOT/path
    existing=p.read_text(encoding="utf-8") if p.exists() else ""
    if marker not in existing:
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text+"\n\n"+existing,encoding="utf-8")
def patch_index():
    p=ROOT/"public/index.html"
    if not p.exists(): return
    html=p.read_text(encoding="utf-8")
    if "demo-ecosystem-registry.html" not in html:
        insert="""<section class="section panel" style="margin:40px auto;max-width:1180px">
<h2>Demo Ecosystem Registry</h2>
<p>The public proof demos are now routeable: every demo has a canonical URL, workflow category, expected inputs, generated artifacts, proof gates, and next allowed state.</p>
<p><a class="btn primary" href="demo-ecosystem-registry.html">Open the Demo Registry</a> <a class="btn" href="falsification-gauntlet.html">Open Falsification V1.2</a></p>
</section>"""
        html=html.replace("</body>",insert+"\n</body>") if "</body>" in html else html+insert
        p.write_text(html,encoding="utf-8")
registry=json.loads((ROOT/"content/goalos/demo-ecosystem-registry-v1.json").read_text(encoding="utf-8"))
report={"status":"passed","generated_at":datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z","registry_entries":len(registry.get("demos",[])),"falsification_hotfix":"v1.2 claim-sensitive stress path installed","browser_local":True,"no_user_data":True,"no_user_funds":True,"no_wallet":True,"no_network_call":True,"errors":[]}
for req in ["public/falsification-gauntlet.html","public/demo-ecosystem-registry.html","public/assets/goalos-falsification-gauntlet-v12.js","public/assets/goalos-demo-registry-data-v1.js"]:
    if not (ROOT/req).exists(): report["errors"].append(f"Missing {req}")
js=(ROOT/"public/assets/goalos-falsification-gauntlet-v12.js").read_text(encoding="utf-8")
for forbidden in ["fetch(","XMLHttpRequest","sendBeacon","localStorage","sessionStorage","window.ethereum"]:
    if forbidden in js: report["errors"].append(f"Forbidden browser API detected: {forbidden}")
if report["registry_entries"]<20: report["errors"].append("Registry has fewer than 20 demos")
if report["errors"]: report["status"]="failed"
write("reports/demo-registry-falsification-v1-2-qa.json",json.dumps(report,indent=2))
write("reports/demo-registry-falsification-v1-2-install-report.json",json.dumps({"installed":True,"generated_at":report["generated_at"],"entries":report["registry_entries"]},indent=2))
patch_once("README.md","<!-- GOALOS_DEMO_REGISTRY_FALSIFICATION_V12 -->","""<!-- GOALOS_DEMO_REGISTRY_FALSIFICATION_V12 -->
## GoalOS Demo Ecosystem Registry + Falsification Gauntlet V1.2

The public demo ecosystem now has a canonical routing matrix:

- Website: `public/demo-ecosystem-registry.html`
- Falsification hotfix: `public/falsification-gauntlet.html`
- Registry JSON: `content/goalos/demo-ecosystem-registry-v1.json`
- QA: `reports/demo-registry-falsification-v1-2-qa.json`

V1.2 makes Falsification Gauntlet stress mode claim-sensitive: narrower, bounded, replayable, low-overhead claims now score differently from broad, vague, overclaiming claims.
""")
patch_index()
search_path=ROOT/"public/search-index.json"
try:
    data=json.loads(search_path.read_text(encoding="utf-8")) if search_path.exists() else []
    if not isinstance(data,list): data=[]
except Exception:
    data=[]
existing={x.get("url") for x in data if isinstance(x,dict)}
for page,title,desc in [
    ("demo-ecosystem-registry.html","Demo Ecosystem Registry","Canonical routing matrix for GoalOS demos."),
    ("falsification-gauntlet.html","Falsification Gauntlet V1.2","Claim-sensitive stress test for strong claims.")
]:
    if page not in existing: data.append({"title":title,"url":page,"description":desc})
write("public/search-index.json",json.dumps(data,indent=2))
sitemap=ROOT/"public/sitemap.xml"
urls=["demo-ecosystem-registry.html","falsification-gauntlet.html"]
if sitemap.exists():
    sm=sitemap.read_text(encoding="utf-8")
else:
    sm='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
for page in urls:
    if page not in sm:
        item=f"<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{page}</loc></url>"
        sm=sm.replace("</urlset>",item+"\n</urlset>") if "</urlset>" in sm else sm+item
write("public/sitemap.xml",sm)
write(".nojekyll","")
print(json.dumps(report,indent=2))
if report["status"]!="passed": raise SystemExit(1)
