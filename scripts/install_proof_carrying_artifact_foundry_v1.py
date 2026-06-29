#!/usr/bin/env python3
import json, re, subprocess, sys, os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
PAGE = "proof-carrying-artifact-foundry.html"
SECTION_START = "<!-- GOALOS_PROOF_CARRYING_ARTIFACT_FOUNDRY_V1_START -->"
SECTION_END = "<!-- GOALOS_PROOF_CARRYING_ARTIFACT_FOUNDRY_V1_END -->"


def read(p):
    return p.read_text(encoding="utf-8") if p.exists() else ""

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")

def patch_between(path, block):
    p = ROOT / path
    txt = read(p)
    if not txt:
        txt = ""
    wrapped = f"\n{SECTION_START}\n{block.strip()}\n{SECTION_END}\n"
    if SECTION_START in txt and SECTION_END in txt:
        txt = re.sub(re.escape(SECTION_START)+r".*?"+re.escape(SECTION_END), wrapped.strip(), txt, flags=re.S)
    else:
        if "</body>" in txt.lower():
            txt = re.sub(r"</body>", wrapped + "\n</body>", txt, flags=re.I)
        else:
            txt += wrapped
    write(p, txt)

def patch_readme():
    block = """
## GoalOS Proof-Carrying Artifact Foundry V1

The Artifact Foundry is a browser-local public demonstration of the AEP-001 principle that the central reusable object is not the agent or the model, but the **Proof-Carrying Artifact**.

- Live page: `public/proof-carrying-artifact-foundry.html`
- Public URL: `https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-carrying-artifact-foundry.html`
- Doctrine: score is advisory; gates are mandatory.
- Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.

The page lets users transform a raw artifact candidate into a proof-carrying artifact with proof history, eval gate, baseline comparison, rollback target, scope authorization, challenge window, replay path, Selection Certificate, Rollback Receipt, and Evolution Ledger entry.
"""
    p = ROOT / "README.md"
    txt = read(p) or "# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n"
    wrapped = f"\n{SECTION_START}\n{block.strip()}\n{SECTION_END}\n"
    if SECTION_START in txt:
        txt = re.sub(re.escape(SECTION_START)+r".*?"+re.escape(SECTION_END), wrapped.strip(), txt, flags=re.S)
    else:
        txt += wrapped
    write(p, txt)

def patch_index():
    block = """
<section class="goalos-pca-foundry-card" style="margin:48px auto;max-width:1180px;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:28px;background:rgba(255,255,255,.055)">
  <p style="letter-spacing:.32em;text-transform:uppercase;color:#fff071;font-weight:900;font-size:12px">New public demo</p>
  <h2 style="font-size:clamp(34px,5vw,64px);line-height:.95;margin:0 0 12px;color:#f6f1e7">The artifact earns authority.</h2>
  <p style="font-size:18px;line-height:1.55;color:#dce4f8;max-width:780px">Run the Proof-Carrying Artifact Foundry: turn raw output into a scoped, evaluated, rollbackable, replayable artifact that can become reusable capability only after gates pass.</p>
  <a href="proof-carrying-artifact-foundry.html" style="display:inline-block;margin-top:18px;padding:13px 18px;border-radius:999px;background:linear-gradient(135deg,#fff071,#66ffd6);color:#061016;text-decoration:none;font-weight:900">Open Artifact Foundry</a>
</section>
"""
    patch_between("public/index.html", block)

def patch_search():
    p = ROOT / "public/search-index.json"
    item = {"title":"Proof-Carrying Artifact Foundry", "url":"proof-carrying-artifact-foundry.html", "description":"Browser-local demo showing how raw output becomes reusable capability only after proof, evaluation, rollback, scope, and replay gates pass."}
    try:
        data = json.loads(read(p) or "[]")
        if isinstance(data, list):
            data = [x for x in data if x.get("url") != item["url"]]
            data.append(item)
        elif isinstance(data, dict):
            arr = data.get("pages", [])
            arr = [x for x in arr if x.get("url") != item["url"]]
            arr.append(item)
            data["pages"] = arr
        else:
            data = [item]
    except Exception:
        data = [item]
    write(p, json.dumps(data, indent=2, ensure_ascii=False)+"\n")

def patch_sitemap():
    p = ROOT / "public/sitemap.xml"
    url = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-carrying-artifact-foundry.html"
    txt = read(p)
    if not txt.strip():
        txt = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n'
    if url not in txt:
        entry = f"  <url><loc>{url}</loc></url>\n"
        txt = txt.replace("</urlset>", entry + "</urlset>") if "</urlset>" in txt else txt + entry
    write(p, txt)

def run_demo():
    subprocess.check_call([sys.executable, "scripts/run_proof_carrying_artifact_foundry_v1_demo.py"])

def audit():
    subprocess.check_call([sys.executable, "scripts/goalos_proof_carrying_artifact_foundry_v1_audit.py"])

if __name__ == "__main__":
    patch_readme(); patch_index(); patch_search(); patch_sitemap()
    (ROOT/"reports").mkdir(exist_ok=True)
    (ROOT/".nojekyll").write_text("", encoding="utf-8")
    run_demo(); audit()
    report = {
      "schema":"goalos.install_report.v1",
      "name":"Proof-Carrying Artifact Foundry V1",
      "status":"passed",
      "installedAt":datetime.now(timezone.utc).isoformat(),
      "page":"public/proof-carrying-artifact-foundry.html",
      "boundary":"browser-local; no user data; no user funds; no wallet; no transaction; no network call; human review required"
    }
    write(ROOT/"reports/proof-carrying-artifact-foundry-v1-install-report.json", json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))
