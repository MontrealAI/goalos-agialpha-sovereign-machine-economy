#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path.cwd()
required=["public/falsification-gauntlet.html","public/demo-ecosystem-registry.html","public/assets/goalos-falsification-gauntlet-v12.js","public/assets/goalos-demo-registry-data-v1.js","content/goalos/demo-ecosystem-registry-v1.json","reports/demo-registry-falsification-v1-2-qa.json"]
errors=[p for p in required if not (ROOT/p).exists()]
data=json.loads((ROOT/"content/goalos/demo-ecosystem-registry-v1.json").read_text())
if len(data.get("demos",[]))<20: errors.append("registry too small")
js=(ROOT/"public/assets/goalos-falsification-gauntlet-v12.js").read_text()
for forbidden in ["fetch(","XMLHttpRequest","sendBeacon","localStorage","sessionStorage","window.ethereum"]:
    if forbidden in js: errors.append(f"Forbidden browser API: {forbidden}")
report={"status":"passed" if not errors else "failed","errors":errors,"entries":len(data.get("demos",[]))}
(ROOT/"reports").mkdir(exist_ok=True)
(ROOT/"reports/demo-registry-falsification-v1-2-audit.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
