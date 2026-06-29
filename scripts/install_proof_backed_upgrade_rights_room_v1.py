#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
MARKER = "<!-- GOALOS_PROOF_BACKED_UPGRADE_RIGHTS_ROOM_V1 -->"

def write_text(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def append_once(path, marker, block):
    p = ROOT / path
    current = p.read_text(encoding="utf-8") if p.exists() else ""
    if marker not in current:
        if current and not current.endswith("\n"):
            current += "\n"
        p.write_text(current + "\n" + marker + "\n" + block + "\n", encoding="utf-8")

def patch_index():
    p = ROOT / "public/index.html"
    if not p.exists():
        return
    html = p.read_text(encoding="utf-8")
    if "proof-backed-upgrade-rights-room.html" in html:
        return
    card = """
<section class="shell" id="proof-backed-upgrade-rights-room">
  <div style="margin:36px auto;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.04));">
    <p style="letter-spacing:.24em;text-transform:uppercase;color:#ffeb7a;font-weight:900;">New public demo</p>
    <h2 style="font-size:clamp(34px,5vw,64px);line-height:.95;margin:8px 0;">The artifact earns authority.</h2>
    <p style="max-width:760px;color:#cbd6ea;font-size:18px;line-height:1.5;">Proof-backed upgrade rights show how useful work becomes limited, governed, rollbackable capability only after mandatory proof gates pass.</p>
    <p><a href="proof-backed-upgrade-rights-room.html" style="display:inline-block;margin-top:12px;padding:14px 20px;border-radius:999px;background:linear-gradient(90deg,#ffeb7a,#63f4c7);color:#07100d;text-decoration:none;font-weight:900;">Open Upgrade Rights Room</a></p>
  </div>
</section>
"""
    html = html.replace("</main>", card + "\n</main>") if "</main>" in html else html + card
    p.write_text(html, encoding="utf-8")

def patch_search_and_sitemap():
    search_path = ROOT / "public/search-index.json"
    item = {"title":"Proof-Backed Upgrade Rights Room","url":"proof-backed-upgrade-rights-room.html","description":"A browser-local demo showing how artifacts earn limited, rollbackable authority after proof gates pass."}
    if search_path.exists():
        try:
            data = json.loads(search_path.read_text(encoding="utf-8"))
            if isinstance(data, list) and not any(x.get("url")==item["url"] for x in data if isinstance(x, dict)):
                data.append(item)
                search_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass
    sitemap = ROOT / "public/sitemap.xml"
    if sitemap.exists():
        xml = sitemap.read_text(encoding="utf-8")
        if "proof-backed-upgrade-rights-room.html" not in xml:
            insert = "  <url><loc>https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-backed-upgrade-rights-room.html</loc></url>\n"
            xml = xml.replace("</urlset>", insert + "</urlset>") if "</urlset>" in xml else xml + "\n" + insert
            sitemap.write_text(xml, encoding="utf-8")

def main():
    append_once("README.md", MARKER, """## Proof-Backed Upgrade Rights Room

New public demo: [Proof-Backed Upgrade Rights Room](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-backed-upgrade-rights-room.html)

**Thesis:** the artifact earns authority. A useful output becomes reusable institutional capability only after proof, evaluation, baseline, scope, canary, rollback, challenge, privacy, and human-review gates pass.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
""")
    patch_index()
    patch_search_and_sitemap()
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    report = {
        "status": "installed",
        "installed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "page": "public/proof-backed-upgrade-rights-room.html",
        "boundary": {
            "no_user_data": True,
            "no_user_funds": True,
            "no_wallet": True,
            "no_transaction": True,
            "no_network_call": True,
            "human_review_required": True
        }
    }
    write_text("reports/proof-backed-upgrade-rights-room-v1-install-report.json", json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
