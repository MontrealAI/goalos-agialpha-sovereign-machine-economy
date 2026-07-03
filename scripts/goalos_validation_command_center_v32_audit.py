import json, re, sys
from pathlib import Path
ROOT=Path.cwd()
PUBLIC=ROOT/"public"
required=[
 "public/validation-command-center.html",
 "public/validation-use-cases.html",
 "public/agi-node-use-cases.html",
 "public/assets/goalos-validation-command-center-v32.css",
 "public/assets/goalos-validation-command-center-v32.js",
 "public/assets/goalos-validation-orchestrator-routes-v32.js"
]
missing=[r for r in required if not (ROOT/r).exists()]
forbidden=["fetch(","XMLHttpRequest","sendBeacon","localStorage","sessionStorage","window.ethereum"]
hits=[]
for rel in required:
    p=ROOT/rel
    if p.exists() and p.suffix in [".js",".html"]:
        txt=p.read_text(encoding="utf-8",errors="ignore")
        for f in forbidden:
            if f in txt:
                hits.append({"file":rel,"forbidden":f})
broken=[]
for p in PUBLIC.glob("*.html"):
    txt=p.read_text(encoding="utf-8",errors="ignore")
    for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', txt):
        if not href.startswith("http") and not (PUBLIC/href).exists():
            broken.append({"from":p.name,"to":href})
status="passed" if not missing and not hits and not broken else "failed"
out={"version":"v32","status":status,"missing":missing,"forbiddenBrowserApiHits":hits,"brokenInternalHtmlLinks":broken,"publicPages":len(list(PUBLIC.glob("*.html")))}
Path("reports").mkdir(exist_ok=True)
Path("reports/validation-command-center-v32-audit.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=2))
if status!="passed":
    sys.exit(1)
