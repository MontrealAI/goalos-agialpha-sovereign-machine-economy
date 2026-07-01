#!/usr/bin/env python3
from pathlib import Path
import json, shutil, datetime

ROOT = Path.cwd()
PAYLOAD = Path(__file__).resolve().parents[1] / "payload"
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
BOUNDARY = "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."
FILES = [
    "public/loop-contract-lab.html",
    "public/assets/goalos-loop-contract-lab-v1.css",
    "public/assets/goalos-loop-contract-lab-v1.js",
    "docs/demos/LOOP_CONTRACT_LAB_V1.md",
    "docs/reviewer/HOW_TO_REVIEW_LOOP_CONTRACT_LAB.md",
    "examples/loop-contract-lab/public-safe-loop-scenarios.md",
    "scripts/run_loop_contract_lab_v1_demo.py",
    "scripts/goalos_loop_contract_lab_v1_audit.py",
    "evidence/demo/loop-contract-lab-v1-reference-docket.json",
    "reports/loop-contract-lab-v1-install-report.json",
    "content/goalos/loop-contract-lab-v1.json",
    ".github/ISSUE_TEMPLATE/loop_contract_lab_feedback.yml",
    "issue-bodies/loop-contract-lab-v1.md",
]

def copy_payload():
    for src in PAYLOAD.rglob("*"):
        if src.is_file():
            rel = src.relative_to(PAYLOAD)
            dst = ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

def add_index_card():
    index = ROOT / "public" / "index.html"
    if not index.exists():
        return False
    text = index.read_text(encoding="utf-8")
    if "loop-contract-lab.html" in text:
        return False
    card = (
        "\n<section class=\"goalos-v7-card goalos-loop-card\" data-goalos-demo=\"loop-contract-lab\">\n"
        "  <p class=\"eyebrow\"><span></span> NEW PUBLIC DEMO / LOOP CONTRACT</p>\n"
        "  <h2>Write the loop. Not the prompt.</h2>\n"
        "  <p>Run the browser-local Loop Contract Lab: role contracts, disk state, trace reading, restart, Evidence Docket plan, and bottleneck report. No data. No funds. Human review required.</p>\n"
        "  <a class=\"button primary\" href=\"loop-contract-lab.html\">Open Loop Contract Lab</a>\n"
        "</section>\n"
    )
    lower = text.lower()
    idx = lower.rfind("</main>")
    if idx == -1:
        idx = lower.rfind("</body>")
    text = text + card if idx == -1 else text[:idx] + card + text[idx:]
    index.write_text(text, encoding="utf-8")
    return True

def update_search_index():
    p = ROOT / "public" / "search-index.json"
    item = {
        "title": "GoalOS Loop Contract Lab",
        "url": "loop-contract-lab.html",
        "description": "Write the loop, not the prompt. Role contracts, disk state, restart, traces, Evidence Docket plan, and bottleneck report.",
        "category": "core-demo",
        "tags": ["loop", "contract", "trace", "restart", "evidence", "docket", "agent"]
    }
    data = []
    if p.exists():
        try:
            raw = json.loads(p.read_text(encoding="utf-8"))
            data = raw if isinstance(raw, list) else raw.get("items") or raw.get("pages") or []
        except Exception:
            data = []
    if not any(isinstance(x, dict) and x.get("url") == item["url"] for x in data):
        data.append(item)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

def update_sitemap():
    p = ROOT / "public" / "sitemap.xml"
    url = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/loop-contract-lab.html"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        if "loop-contract-lab.html" not in text:
            text = text.replace("</urlset>", f"  <url><loc>{url}</loc></url>\n</urlset>") if "</urlset>" in text else text + f"\n<url><loc>{url}</loc></url>\n"
        p.write_text(text, encoding="utf-8")
    else:
        p.write_text(f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n  <url><loc>{url}</loc></url>\n</urlset>\n", encoding="utf-8")

def patch_registry_pages():
    snippet = '<p><a href="loop-contract-lab.html">GoalOS Loop Contract Lab</a> — Write the loop, not the prompt: role contracts, disk state, restart, traces, docket plan.</p>\n'
    for rel in ["public/demo-ecosystem-registry.html", "public/site-map.html", "public/website-operating-system.html"]:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        if "loop-contract-lab.html" in text:
            continue
        lower = text.lower()
        idx = lower.rfind("</main>")
        if idx == -1:
            idx = lower.rfind("</body>")
        text = text + snippet if idx == -1 else text[:idx] + snippet + text[idx:]
        p.write_text(text, encoding="utf-8")

def update_readme():
    p = ROOT / "README.md"
    block = (
        "\n## GoalOS Loop Contract Lab V1\n\n"
        "**Write the loop, not the prompt.**\n\n"
        "The Loop Contract Lab adds a browser-local public demo showing how long-running agent work becomes reviewable through role contracts, disk state, readable traces, restart semantics, evaluator independence, Evidence Docket planning, and bottleneck reporting.\n\n"
        "Open: `public/loop-contract-lab.html`\n\n"
        "Boundary: No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.\n"
    )
    if p.exists():
        text = p.read_text(encoding="utf-8")
        if "GoalOS Loop Contract Lab V1" not in text:
            text += block
        p.write_text(text, encoding="utf-8")
    else:
        p.write_text("# GoalOS AGIALPHA Ascension\n" + block, encoding="utf-8")

def write_report(changed):
    out = ROOT / "reports" / "loop-contract-lab-v1-install-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"status":"passed","generated_at":NOW,"installed":FILES,"index_card_added":changed,"boundary":BOUNDARY}, indent=2) + "\n", encoding="utf-8")

def main():
    copy_payload()
    changed = add_index_card()
    update_search_index()
    update_sitemap()
    patch_registry_pages()
    update_readme()
    (ROOT / "public" / ".nojekyll").write_text("", encoding="utf-8")
    write_report(changed)
    print("GoalOS Loop Contract Lab V1 installed.")

if __name__ == "__main__":
    main()
