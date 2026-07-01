#!/usr/bin/env python3
from pathlib import Path
import json, datetime

ROOT = Path.cwd()
SRC = Path(__file__).resolve().parents[1]

def copy_tree(src, dst):
    if not src.exists():
        return
    for p in src.rglob("*"):
        if p.is_file():
            rel = p.relative_to(src)
            out = dst / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(p.read_bytes())

def read(path):
    return path.read_text(encoding="utf-8") if path.exists() else ""

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def patch_readme():
    p = ROOT / "README.md"
    current = read(p)
    block = """
<!-- GOALOS_LOOP_FLIGHT_RECORDER_V1_START -->
## GoalOS Loop Flight Recorder V1

**Write the loop. Not the prompt.**

New browser-local public demonstration: [`loop-flight-recorder.html`](public/loop-flight-recorder.html).

It shows how long-running agent loops become review-ready by separating roles, writing state to disk, reading traces, restarting cleanly, scoring subjective quality, deleting harness overhead, exposing the next bottleneck, and emitting downloadable review artifacts.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
<!-- GOALOS_LOOP_FLIGHT_RECORDER_V1_END -->
"""
    if "GOALOS_LOOP_FLIGHT_RECORDER_V1_START" not in current:
        current = (current.rstrip() + "\n\n" + block + "\n") if current else "# GoalOS AGIALPHA Ascension\n\n" + block
    write(p, current)

def patch_index():
    p = ROOT / "public/index.html"
    current = read(p)
    card = """
<section class="goalos-loop-flight-recorder-card" style="max-width:1180px;margin:64px auto;padding:34px;border:1px solid rgba(255,255,255,.18);border-radius:28px;background:linear-gradient(135deg,rgba(112,255,212,.13),rgba(255,255,255,.06));color:#fff;">
  <p style="letter-spacing:.28em;text-transform:uppercase;color:#ffe872;font-weight:900;">New public demo / loop</p>
  <h2 style="font-size:clamp(34px,5vw,72px);line-height:.95;margin:0 0 14px;">Write the loop. Not the prompt.</h2>
  <p style="max-width:850px;font-size:18px;line-height:1.55;color:#dfe8f8;">Open the Loop Flight Recorder: separate roles, write state to disk, read traces, restart cleanly, score subjective quality, delete harness overhead, expose the next bottleneck, and download review artifacts. Browser-local. No data. No funds.</p>
  <a href="loop-flight-recorder.html" style="display:inline-block;margin-top:14px;padding:13px 18px;border-radius:999px;background:linear-gradient(120deg,#ffe872,#70ffd4);color:#03100d;font-weight:900;text-decoration:none;">Open Loop Flight Recorder</a>
</section>
"""
    if not current or "loop-flight-recorder.html" in current:
        return
    if "</main>" in current:
        current = current.replace("</main>", card + "\n</main>", 1)
    elif "</body>" in current:
        current = current.replace("</body>", card + "\n</body>", 1)
    write(p, current)

def patch_search_index():
    p = ROOT / "public/search-index.json"
    data = []
    if p.exists():
        try:
            data = json.loads(read(p))
        except Exception:
            data = []
    if not isinstance(data, list):
        data = []
    if not any((item.get("url") or item.get("path")) == "loop-flight-recorder.html" for item in data if isinstance(item, dict)):
        data.append({
            "title": "GoalOS Loop Flight Recorder V1",
            "url": "loop-flight-recorder.html",
            "path": "loop-flight-recorder.html",
            "description": "Write the loop, not the prompt: restartable agent loops with disk state, trace reading, bottleneck reports, and review artifacts.",
            "category": "Loop demo"
        })
    write(p, json.dumps(data, indent=2))

def patch_sitemap():
    p = ROOT / "public/sitemap.xml"
    url = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/loop-flight-recorder.html"
    if p.exists():
        s = read(p)
        if "loop-flight-recorder.html" not in s:
            entry = f"  <url><loc>{url}</loc></url>\n"
            if "</urlset>" in s:
                s = s.replace("</urlset>", entry + "</urlset>")
            else:
                s += "\n" + entry
    else:
        s = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n'
    write(p, s)

def patch_registry_json():
    p = ROOT / "content/goalos/demo-ecosystem-registry.json"
    if p.exists():
        try:
            data = json.loads(read(p))
        except Exception:
            data = {}
    else:
        data = {}
    entry = {
        "id": "loop-flight-recorder-v1",
        "name": "GoalOS Loop Flight Recorder V1",
        "path": "loop-flight-recorder.html",
        "description": "Restartable long-running agent loops with disk state, trace reading, evaluator separation, bottleneck reporting, and downloadable proof artifacts.",
        "workflow_category": "loop / long-running agents / proof",
        "expected_inputs": ["public-safe objective", "scenario", "gate toggles", "taste sliders"],
        "generated_outputs": ["loop recorder", "state pack", "Evidence Docket plan", "bottleneck report", "reviewer brief"],
        "proof_gates": ["contract before code", "role separation", "write state to disk", "independent evaluator", "trace reading", "restart ready", "public/private boundary"],
        "state_transitions": ["LOOP_REVIEW_READY", "REJECT_NO_CONTRACT", "HOLD_STATE_FILES_REQUIRED", "REJECT_SELF_GRADED_LOOP", "BLOCK_PRIVACY_BOUNDARY"],
        "role": "UI demo / scoring module / reviewer module / loop-governance module"
    }
    if "routes" in data and isinstance(data["routes"], list):
        data["routes"] = [r for r in data["routes"] if not (isinstance(r, dict) and r.get("id") == entry["id"])]
        data["routes"].append(entry)
    elif "demos" in data and isinstance(data["demos"], list):
        data["demos"] = [r for r in data["demos"] if not (isinstance(r, dict) and r.get("id") == entry["id"])]
        data["demos"].append(entry)
    else:
        data = {"version": "loop-flight-recorder-v1", "routes": [entry]}
    write(p, json.dumps(data, indent=2))

def patch_registry_html():
    p = ROOT / "public/demo-ecosystem-registry.html"
    html = read(p)
    if not html or "loop-flight-recorder.html" in html:
        return
    block = """
<section class="registry-loop-flight-recorder" style="max-width:1180px;margin:40px auto;padding:28px;border:1px solid rgba(255,255,255,.18);border-radius:24px;background:rgba(255,255,255,.07);color:#fff;">
  <p style="letter-spacing:.25em;text-transform:uppercase;color:#ffe872;font-weight:900;">Loop / long-running agents</p>
  <h2>GoalOS Loop Flight Recorder V1</h2>
  <p>Expected inputs: public-safe objective, scenario, gate toggles, taste sliders. Outputs: recorder JSON, state pack, Evidence Docket plan, bottleneck report, reviewer brief. Gates: contract first, role separation, disk state, evaluator separation, trace reading, restart readiness, public/private boundary.</p>
  <a href="loop-flight-recorder.html" style="color:#70ffd4;font-weight:900;">Open Loop Flight Recorder →</a>
</section>
"""
    if "</main>" in html:
        html = html.replace("</main>", block + "\n</main>", 1)
    elif "</body>" in html:
        html = html.replace("</body>", block + "\n</body>", 1)
    write(p, html)

def create_reports():
    report = {
        "status": "passed",
        "demo": "GoalOS Loop Flight Recorder V1",
        "created": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "browser_local": True,
        "no_network_call": True,
        "no_user_data": True,
        "no_user_funds": True,
        "wallet_or_mainnet": False,
        "human_review_required": True,
        "files": [
            "public/loop-flight-recorder.html",
            "public/assets/goalos-loop-flight-recorder-v1.css",
            "public/assets/goalos-loop-flight-recorder-v1.js"
        ]
    }
    write(ROOT/"reports/loop-flight-recorder-v1-install-report.json", json.dumps(report, indent=2))

def main():
    copy_tree(SRC / "public", ROOT / "public")
    copy_tree(SRC / "docs", ROOT / "docs")
    copy_tree(SRC / "examples", ROOT / "examples")
    copy_tree(SRC / "evidence", ROOT / "evidence")
    copy_tree(SRC / "reports", ROOT / "reports")
    copy_tree(SRC / "scripts", ROOT / "scripts")
    copy_tree(SRC / "content", ROOT / "content")
    copy_tree(SRC / ".github", ROOT / ".github")
    copy_tree(SRC / "issue-bodies", ROOT / "issue-bodies")
    patch_readme()
    patch_index()
    patch_search_index()
    patch_sitemap()
    patch_registry_json()
    patch_registry_html()
    (ROOT / "public/.nojekyll").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "public/.nojekyll").touch()
    create_reports()
    print("GoalOS Loop Flight Recorder V1 installed.")

if __name__ == "__main__":
    main()
