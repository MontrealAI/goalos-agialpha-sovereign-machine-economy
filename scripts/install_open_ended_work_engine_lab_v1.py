from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
PAGE = "open-ended-work-engine.html"

def ensure_parent(path):
    path.parent.mkdir(parents=True, exist_ok=True)

def patch_readme():
    p = ROOT / "README.md"
    marker = "<!-- GOALOS_OPEN_ENDED_WORK_ENGINE_V1 -->"
    block = f"""
{marker}
## GoalOS Open-Ended Work Engine Lab V1

**Generate tasks. Gate descendants. Keep open-endedness tethered to proof.**

The Open-Ended Work Engine Lab is a browser-local public demo showing how GoalOS can generate mission candidates, validator challenges, workflows, proof templates, curricula, and capability candidates while admitting only descendants that pass replay, validation, risk, and boundary gates.

- Website: [`public/{PAGE}`](public/{PAGE})
- Demo docs: [`docs/demos/OPEN_ENDED_WORK_ENGINE_LAB_V1.md`](docs/demos/OPEN_ENDED_WORK_ENGINE_LAB_V1.md)
- Reviewer guide: [`docs/reviewer/HOW_TO_REVIEW_OPEN_ENDED_WORK_ENGINE_LAB.md`](docs/reviewer/HOW_TO_REVIEW_OPEN_ENDED_WORK_ENGINE_LAB.md)

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
"""
    old = p.read_text(encoding="utf-8") if p.exists() else "# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n"
    if marker not in old:
        old += "\n" + block
    else:
        old = re.sub(rf"{re.escape(marker)}.*?(?=\n<!-- GOALOS_|\Z)", block.strip()+"\n", old, flags=re.S)
    p.write_text(old, encoding="utf-8")

def patch_index():
    p = ROOT / "public" / "index.html"
    ensure_parent(p)
    if not p.exists():
        p.write_text("<!doctype html><html><head><title>GoalOS</title></head><body><h1>GoalOS</h1></body></html>", encoding="utf-8")
    text = p.read_text(encoding="utf-8")
    href = 'open-ended-work-engine.html'
    if href not in text:
        card = """
<section class="goalos-open-ended-work-engine-card" style="margin:40px auto;max-width:1180px;padding:28px;border:1px solid rgba(255,255,255,.18);border-radius:24px;background:rgba(255,255,255,.06)">
  <p style="letter-spacing:.3em;text-transform:uppercase;color:#ffe875;font-weight:900">New public demo</p>
  <h2 style="font-size:clamp(32px,5vw,72px);line-height:.92;margin:0 0 14px;color:#fffaf0">Generate tasks. Gate descendants.</h2>
  <p style="color:#dce6fa;font-size:20px">Explore the GoalOS Open-Ended Work Engine Lab: a browser-local demonstration of proof-gated task, validator, workflow, and capability generation.</p>
  <a href="open-ended-work-engine.html" style="display:inline-block;margin-top:14px;padding:12px 18px;border-radius:999px;background:#ffe875;color:#07101d;font-weight:900;text-decoration:none">Open the Work Engine Lab</a>
</section>
"""
        text = text.replace("</body>", card + "\n</body>") if "</body>" in text else text + card
    p.write_text(text, encoding="utf-8")

def patch_search():
    p = ROOT / "public" / "search-index.json"
    ensure_parent(p)
    try:
        data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
        if isinstance(data, dict): data = data.get("pages", [])
        if not isinstance(data, list): data = []
    except Exception:
        data = []
    item = {"title":"Open-Ended Work Engine Lab","url":"open-ended-work-engine.html","description":"Generate tasks. Gate descendants. Keep open-endedness tethered to proof."}
    data = [x for x in data if x.get("url") != item["url"]] + [item]
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")

def patch_sitemap():
    p = ROOT / "public" / "sitemap.xml"
    ensure_parent(p)
    url = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/open-ended-work-engine.html"
    if p.exists():
        text = p.read_text(encoding="utf-8")
    else:
        text = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>'
    if url not in text:
        entry = f"<url><loc>{url}</loc><lastmod>{NOW[:10]}</lastmod></url>"
        text = text.replace("</urlset>", entry + "</urlset>") if "</urlset>" in text else text + entry
    p.write_text(text, encoding="utf-8")

def write_report():
    p = ROOT / "reports" / "open-ended-work-engine-lab-v1-install-report.json"
    ensure_parent(p)
    report = {
        "status":"passed",
        "installed_at":NOW,
        "page":"public/open-ended-work-engine.html",
        "assets":[
            "public/assets/goalos-open-ended-work-engine-v1.css",
            "public/assets/goalos-open-ended-work-engine-v1.js"
        ],
        "boundary":{"no_user_data":True,"no_user_funds":True,"no_wallet":True,"no_transaction":True,"no_network_call":True,"human_review_required":True}
    }
    p.write_text(json.dumps(report, indent=2), encoding="utf-8")

def main():
    (ROOT / "public").mkdir(exist_ok=True)
    (ROOT / "public" / ".nojekyll").write_text("", encoding="utf-8")
    patch_readme()
    patch_index()
    patch_search()
    patch_sitemap()
    write_report()
    print("GoalOS Open-Ended Work Engine Lab V1 installed.")

if __name__ == "__main__":
    main()
