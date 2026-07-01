from pathlib import Path
import json, re, datetime

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

PAGE = {
    "title": "From Loop to RSI Governance Lab",
    "path": "from-loop-to-rsi-governance.html",
    "description": "Write the loop. Govern recursive improvement. Search control is not outcome authority.",
    "category": "Loop / RSI",
    "inputs": ["objective", "novelty", "advantage", "ECI", "drift risk", "gate toggles"],
    "outputs": ["RSI state", "Move-37 dossier", "ECI ledger", "baseline report", "reviewer brief"],
    "gates": ["schema", "replay", "state hash", "risk", "evidence", "baseline", "persistence", "dossier", "OMNI no authority", "boundary", "rollback", "human review"],
    "state": "RSI_REVIEW_READY"
}

def read(path):
    p = ROOT / path
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    text = read(path)
    if not text:
        return
    if marker in text:
        return
    write(path, text.rstrip() + "\n\n" + block.strip() + "\n")

def insert_before_body(path, marker, block):
    text = read(path)
    if not text or marker in text:
        return
    if "</body>" in text:
        text = text.replace("</body>", block.strip() + "\n</body>")
    elif "</main>" in text:
        text = text.replace("</main>", block.strip() + "\n</main>")
    else:
        text += "\n" + block
    write(path, text)

def patch_readme():
    block = """
## GoalOS From Loop to RSI Governance Lab V1

**Page:** [`public/from-loop-to-rsi-governance.html`](public/from-loop-to-rsi-governance.html)

A browser-local public demo showing how a restartable loop becomes deterministic RSI governance: `TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE`.

It demonstrates the rule: **search control is not outcome authority**. OMNI-style interestingness may allocate exploration, but promotion still requires risk, evidence, baseline, replay, persistence, dossier, rollback, and human-review gates.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
"""
    append_once("README.md", "GoalOS From Loop to RSI Governance Lab V1", block)

def patch_html_routes():
    card = """
<section class="goalos-added-route" style="max-width:1100px;margin:48px auto;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:24px;background:rgba(255,255,255,.06);">
  <p style="letter-spacing:.22em;color:#ffe777;font-weight:900;text-transform:uppercase;">New Loop → RSI Demo</p>
  <h2 style="font-size:clamp(2rem,4vw,4rem);line-height:.9;margin:.2em 0;">Build the governance institution first.</h2>
  <p>Open the From Loop to RSI Governance Lab: TARGET → EMIT → FILTER → ATLAS → TEST‑PLAN → EVAL → INSERT → PROMOTE. Search control is not outcome authority.</p>
  <p><a href="from-loop-to-rsi-governance.html" style="color:#67ffd1;font-weight:900;">Open From Loop to RSI Governance Lab →</a></p>
</section>
"""
    for page in ["public/index.html", "public/site-map.html", "public/website-operating-system.html", "public/demo-ecosystem-registry.html"]:
        insert_before_body(page, "from-loop-to-rsi-governance.html", card)

def patch_sitemap():
    path = ROOT / "public/sitemap.xml"
    if not path.exists():
        write("public/sitemap.xml", """<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n""")
    text = read("public/sitemap.xml")
    if "from-loop-to-rsi-governance.html" not in text:
        entry = "  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/from-loop-to-rsi-governance.html</loc></url>\n"
        text = text.replace("</urlset>", entry + "</urlset>") if "</urlset>" in text else text + "\n" + entry
        write("public/sitemap.xml", text)

def patch_search_index():
    path = ROOT / "public/search-index.json"
    item = {
        "title": PAGE["title"],
        "url": PAGE["path"],
        "path": PAGE["path"],
        "description": PAGE["description"],
        "category": PAGE["category"],
        "tags": ["loop", "RSI", "sovereign invention governance", "Move-37", "ECI", "OMNI"]
    }
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = []
    else:
        data = []
    if isinstance(data, dict):
        key = "items" if isinstance(data.get("items"), list) else "routes" if isinstance(data.get("routes"), list) else None
        if key:
            arr = data[key]
            if not any((x.get("url") == item["url"] or x.get("path") == item["path"]) for x in arr if isinstance(x, dict)):
                arr.append(item)
        else:
            data.setdefault("items", [item])
    elif isinstance(data, list):
        if not any((x.get("url") == item["url"] or x.get("path") == item["path"]) for x in data if isinstance(x, dict)):
            data.append(item)
    else:
        data = [item]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def patch_registry_json():
    path = ROOT / "content/goalos/demo-ecosystem-registry.json"
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    else:
        data = {}
    route = {
        "name": PAGE["title"],
        "path": PAGE["path"],
        "canonical_path": PAGE["path"],
        "description": PAGE["description"],
        "workflow_category": PAGE["category"],
        "expected_inputs": PAGE["inputs"],
        "generated_outputs": PAGE["outputs"],
        "proof_gates": PAGE["gates"],
        "state_transitions": ["RSI_REVIEW_READY", "MOVE37_DOSSIER_REVIEW_READY", "REJECT_OMNI_OUTCOME_AUTHORITY", "BLOCK_PRIVACY_BOUNDARY"],
        "role": "UI demo / governance module / evidence-docket generator"
    }
    for key in ["routes", "demos", "items"]:
        if isinstance(data.get(key), list):
            arr = data[key]
            if not any(x.get("path") == PAGE["path"] or x.get("canonical_path") == PAGE["path"] for x in arr if isinstance(x, dict)):
                arr.append(route)
            break
    else:
        data["routes"] = [route]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def main():
    (ROOT / "public/.nojekyll").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "public/.nojekyll").write_text("", encoding="utf-8")
    patch_readme()
    patch_html_routes()
    patch_sitemap()
    patch_search_index()
    patch_registry_json()
    report = {
        "status": "passed",
        "installed": PAGE,
        "generated_at": NOW,
        "boundary": "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."
    }
    write("reports/from-loop-to-rsi-governance-v1-install-report.json", json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
