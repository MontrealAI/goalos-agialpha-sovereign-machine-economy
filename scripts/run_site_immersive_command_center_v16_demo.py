#!/usr/bin/env python3
from pathlib import Path
import json, datetime
root = Path.cwd()
public = root / "public"
actions = [
  {"action":"open_homepage","path":"public/index.html","ok":(public/"index.html").exists()},
  {"action":"open_start","path":"public/start-here.html","ok":(public/"start-here.html").exists()},
  {"action":"open_pathfinder","path":"public/pathfinder.html","ok":(public/"pathfinder.html").exists()},
  {"action":"open_registry","path":"public/demo-ecosystem-registry.html","ok":(public/"demo-ecosystem-registry.html").exists()},
  {"action":"open_site_map","path":"public/site-map.html","ok":(public/"site-map.html").exists()},
  {"action":"open_loop_rsi","path":"public/from-loop-to-rsi-state-capacity.html","ok":(public/"from-loop-to-rsi-state-capacity.html").exists()},
  {"action":"open_trust","path":"public/trust-boundary.html","ok":(public/"trust-boundary.html").exists()},
  {"action":"open_token","path":"public/token-boundary.html","ok":(public/"token-boundary.html").exists()},
]
report = {"status":"passed" if all(a["ok"] for a in actions) else "failed","generated_at":datetime.datetime.utcnow().isoformat()+"Z","actions":actions}
(root/"reports").mkdir(exist_ok=True)
(root/"reports/site-immersive-command-center-v16-demo-run.json").write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
raise SystemExit(0 if report["status"]=="passed" else 1)
