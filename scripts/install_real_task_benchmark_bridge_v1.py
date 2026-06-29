#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def read(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    p = ROOT / path
    existing = p.read_text(encoding="utf-8") if p.exists() else ""
    if marker not in existing:
        p.write_text((existing.rstrip() + "\n\n" + block.strip() + "\n"), encoding="utf-8")

readme_block = """
<!-- GOALOS_REAL_TASK_BENCHMARK_BRIDGE_V1_START -->
## GoalOS Real-Task Benchmark Bridge V1

**From demos to real-task evidence.**

The Real-Task Benchmark Bridge is a browser-local public demonstration that shows how a GoalOS claim moves from architecture and demos toward empirical evidence: task family, real-task manifest, equal-budget baselines, ProofBundle / Evidence Docket, replay path, cost/risk ledgers, validator report, delayed-outcome plan, and external review path.

- Website: `public/real-task-benchmark-bridge.html`
- Docs: `docs/demos/REAL_TASK_BENCHMARK_BRIDGE_V1.md`
- QA: `reports/real-task-benchmark-bridge-v1-qa.json`

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
<!-- GOALOS_REAL_TASK_BENCHMARK_BRIDGE_V1_END -->
"""
append_once("README.md", "GOALOS_REAL_TASK_BENCHMARK_BRIDGE_V1_START", readme_block)

index = read("public/index.html")
link_block = """
<section class="goalos-added-section" style="max-width:1120px;margin:60px auto;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:rgba(255,255,255,.06)">
  <p style="letter-spacing:.3em;color:#ffe777;font-weight:900">NEW PUBLIC DEMO</p>
  <h2 style="font-size:clamp(32px,5vw,64px);line-height:.95;margin:0 0 16px">From demos to real-task evidence.</h2>
  <p style="font-size:20px;max-width:780px">The Real-Task Benchmark Bridge shows why strong GoalOS claims require real tasks, equal-budget baselines, ProofBundles, replay, cost/risk ledgers, validator reports, delayed outcomes, and independent review.</p>
  <p><a href="real-task-benchmark-bridge.html" style="display:inline-block;padding:14px 18px;border-radius:999px;background:#ffe777;color:#071021;font-weight:900;text-decoration:none">Open Benchmark Bridge</a></p>
</section>
"""
if index and "real-task-benchmark-bridge.html" not in index:
    if "</main>" in index:
        index = index.replace("</main>", link_block + "\n</main>")
    else:
        index += link_block
    write("public/index.html", index)

# Search index and sitemap
search_path = ROOT / "public/search-index.json"
try:
    search = json.loads(search_path.read_text(encoding="utf-8")) if search_path.exists() else []
    if isinstance(search, dict):
        items = search.get("items", [])
    else:
        items = search
    entry = {
        "title": "Real-Task Benchmark Bridge",
        "url": "real-task-benchmark-bridge.html",
        "description": "Browser-local demo showing how GoalOS moves from demos to real-task evidence with baselines, replay, ledgers, validators, and review."
    }
    if not any((i.get("url") if isinstance(i, dict) else "") == entry["url"] for i in items):
        items.append(entry)
    write("public/search-index.json", json.dumps(items, indent=2))
except Exception:
    write("public/search-index.json", json.dumps([{
        "title": "Real-Task Benchmark Bridge",
        "url": "real-task-benchmark-bridge.html",
        "description": "Browser-local real-task benchmark bridge."
    }], indent=2))

sitemap = read("public/sitemap.xml")
url = "<url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/real-task-benchmark-bridge.html</loc></url>"
if sitemap:
    if "real-task-benchmark-bridge.html" not in sitemap:
        sitemap = sitemap.replace("</urlset>", f"{url}\n</urlset>") if "</urlset>" in sitemap else sitemap + "\n" + url
else:
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{url}</urlset>'
write("public/sitemap.xml", sitemap)
write(".nojekyll", "")

report = {
    "status": "installed",
    "id": "real-task-benchmark-bridge-v1",
    "generated_at": NOW,
    "page": "public/real-task-benchmark-bridge.html",
    "boundary": {
        "no_user_data": True,
        "no_user_funds": True,
        "no_wallet": True,
        "no_transaction": True,
        "no_network_call": True,
        "human_review_required": True
    }
}
write("reports/real-task-benchmark-bridge-v1-install-report.json", json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
