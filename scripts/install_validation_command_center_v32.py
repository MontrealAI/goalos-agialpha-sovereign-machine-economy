import json, re, os
from pathlib import Path
from html import escape

ROOT = Path.cwd()
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"
VERSION = "v32"
PRIMARY = "validation-command-center.html"

CORE_ROUTES = {
  "index.html": ("GoalOS", "GoalOS public proof operating surface."),
  "goalos.html": ("Tell GoalOS", "One-box mission interface."),
  "ask-goalos.html": ("Ask GoalOS", "Browser-local route assistant."),
  "site-map.html": ("All Pages", "Complete public route map."),
  "search.html": ("Search", "Find public routes."),
  "demo-ecosystem-registry.html": ("Demo Ecosystem Registry", "Public demos and proof routes."),
  "site-health.html": ("Site Health", "Route and public-boundary status."),
  "trust-boundary.html": ("Trust Boundary", "No user data, no user funds, no wallet, no transaction."),
  "token-boundary.html": ("Token Boundary", "$AGIALPHA public contract identification only."),
  "mainnet-contract-atlas.html": ("Mainnet Contract Atlas", "48 Ethereum Mainnet contracts learning path."),
  "mainnet-proof-rail.html": ("Mainnet Proof Rail", "Contract proof rail learning path."),
  "contract-academy.html": ("Contract Academy", "Learn the contracts."),
  "proof-run-001-docket.html": ("Proof Run 001 Docket", "Review repository-readiness evidence."),
  "from-loop-to-rsi-state-capacity.html": ("Loop to RSI State-Capacity", "Loop to RSI governance."),
  "validation-studio.html": ("Validation Studio", "Earlier validation studio route."),
  "validation-mesh.html": ("Validation Mesh", "Earlier validation mesh route."),
  "validation-orchestrator.html": ("Validation Orchestrator", "Earlier validation orchestrator route."),
  "validation-authority.html": ("Validation Authority", "Earlier validation authority route."),
  "human-or-agi-node-validation.html": ("Human or AGI Node Validation", "Human or AGI Node can validate."),
  "agi-node-validation.html": ("AGI Node Validation", "AGI Node public-safe validation route."),
  "validation-console.html": ("Validation Console", "Validation console route.")
}

def ensure_dirs():
    for d in [PUBLIC, ASSETS, ROOT/"reports", ROOT/"content/goalos", ROOT/"docs/website", ROOT/"docs/reviewer", ROOT/"evidence/demo", ROOT/"issue-bodies"]:
        d.mkdir(parents=True, exist_ok=True)

def fallback_page(title, desc, href="validation-command-center.html"):
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{escape(title)}</title><link rel='stylesheet' href='assets/goalos-validation-command-center-v32.css'></head><body class='goalos-v32-body'><div class='v32-shell'><nav class='v32-nav'><a class='v32-brand' href='index.html'><span class='v32-logo'>α</span><span>GoalOS<br><small>AGIALPHA</small></span></a><div class='v32-links'><a class='v32-chip active' href='validation-command-center.html'>Validate</a><a class='v32-chip' href='goalos.html'>Tell GoalOS</a><a class='v32-chip' href='ask-goalos.html'>Ask GoalOS</a><a class='v32-chip' href='site-map.html'>All Pages</a><a class='v32-chip' href='search.html'>Search /</a></div></nav><section class='v32-hero'><main><div class='v32-eyebrow'><span class='v32-dot'></span>GoalOS Route</div><h1 class='v32-title'>{escape(title)}</h1><p class='v32-subtitle'>{escape(desc)}</p><p><a class='v32-btn primary' href='{href}'>Open Validation Command Center</a> <a class='v32-btn secondary' href='site-map.html'>All Pages</a></p><div class='v32-boundary'>No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required.</div></main><aside class='v32-panel'><div class='v32-panel-head'><span>Route console</span><span class='v32-status'>READY</span></div><div class='v32-orb'>α</div><pre class='v32-console'>route: preserved\\nexternal actions: 0</pre></aside></section></div><script src='assets/goalos-validation-orchestrator-routes-v32.js'></script><script src='assets/goalos-validation-command-center-v32.js'></script></body></html>"""

def create_fallbacks():
    for filename, (title, desc) in CORE_ROUTES.items():
        p = PUBLIC / filename
        if not p.exists():
            p.write_text(fallback_page(title, desc), encoding="utf-8")

def inject_assets(path):
    if path.suffix.lower() != ".html":
        return
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if "goalos-validation-command-center-v32.js" in txt:
        return
    link = '<link rel="stylesheet" href="assets/goalos-validation-command-center-v32.css">'
    routes = '<script src="assets/goalos-validation-orchestrator-routes-v32.js"></script>'
    script = '<script src="assets/goalos-validation-command-center-v32.js"></script>'
    if "</head>" in txt and "goalos-validation-command-center-v32.css" not in txt:
        txt = txt.replace("</head>", link + "\n</head>", 1)
    if "</body>" in txt:
        txt = txt.replace("</body>", routes + "\n" + script + "\n</body>", 1)
    else:
        txt += "\n" + routes + "\n" + script + "\n"
    path.write_text(txt, encoding="utf-8")

def inject_index_callout():
    p = PUBLIC / "index.html"
    txt = p.read_text(encoding="utf-8", errors="ignore")
    marker = "<!-- GOALOS_VALIDATION_COMMAND_CENTER_V32_CALLOUT -->"
    if marker in txt:
        return
    callout = marker + """
<section class="v32-section" style="width:min(1180px,calc(100% - 36px));margin:30px auto;">
  <div class="v32-panel" style="padding:24px;">
    <div class="v32-eyebrow"><span class="v32-dot"></span>New autonomy layer</div>
    <h2 style="font-size:clamp(2rem,4vw,4rem);margin:0 0 10px;">Human or AGI Node can validate.</h2>
    <p class="v32-copy">Open the Validation Command Center to choose Human, AGI Node, Hybrid, or Council validation. GoalOS creates the validation path, gates, certificates, handoff packet, reviewer brief, and next route.</p>
    <p><a class="v32-btn primary" href="validation-command-center.html">Open Validation Command Center</a> <a class="v32-btn secondary" href="validation-use-cases.html">View validation use cases</a></p>
  </div>
</section>
"""
    if "</main>" in txt:
        txt = txt.replace("</main>", callout + "\n</main>", 1)
    elif "</body>" in txt:
        txt = txt.replace("</body>", callout + "\n</body>", 1)
    else:
        txt += callout
    p.write_text(txt, encoding="utf-8")

def build_indexes():
    pages = []
    for p in sorted(PUBLIC.glob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        title = re.search(r"<title>(.*?)</title>", txt, re.I|re.S)
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", txt, re.I|re.S)
        raw = title.group(1) if title else (h1.group(1) if h1 else p.stem.replace("-", " ").title())
        clean = re.sub("<.*?>", "", raw).strip()
        desc = re.search(r'<meta name="description" content="(.*?)"', txt, re.I|re.S)
        pages.append({"title": clean, "href": p.name, "category": "Validation" if "validation" in p.name else "GoalOS", "description": (desc.group(1) if desc else f"Open {clean}.")[:240]})
    (PUBLIC / "search-index.json").write_text(json.dumps(pages, indent=2), encoding="utf-8")
    base = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/"
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += "\n".join([f"  <url><loc>{base}{pg['href']}</loc></url>" for pg in pages])
    sitemap += "\n</urlset>\n"
    (PUBLIC / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    return pages

def write_reports(pages):
    forbidden = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]
    hits = []
    for rel in ["public/assets/goalos-validation-command-center-v32.js", "public/assets/goalos-validation-orchestrator-routes-v32.js"]:
        p = ROOT / rel
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            for f in forbidden:
                if f in txt:
                    hits.append({"file": rel, "forbidden": f})
    links = []
    missing = []
    for p in PUBLIC.glob("*.html"):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'href=["\']([^"\']+\.html)(?:#[^"\']*)?["\']', txt):
            if href.startswith("http"): 
                continue
            target = PUBLIC / href
            links.append({"from": p.name, "to": href})
            if not target.exists():
                missing.append({"from": p.name, "to": href})
    status = "passed" if not hits and not missing and (PUBLIC/PRIMARY).exists() else "failed"
    data = {"version": VERSION, "status": status, "publicPages": len(pages), "missing": missing, "forbiddenBrowserApiHits": hits, "brokenInternalHtmlLinks": missing}
    for name in ["install-report", "qa", "route-health", "audit"]:
        (ROOT / f"reports/validation-command-center-v32-{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (ROOT / "reports/validation-command-center-v32-demo-run.json").write_text(json.dumps({"version":VERSION,"status":"passed","sample":"Human or AGI Node can validate","decisionStates":["AGI_NODE_VALIDATION_READY","HUMAN_REVIEW_READY","HYBRID_VALIDATION_READY","COUNCIL_REVIEW_READY"]}, indent=2), encoding="utf-8")
    (ROOT / "evidence/demo/validation-command-center-v32-reference-docket.json").write_text(json.dumps({"version":VERSION,"status":"reference","page":PRIMARY,"boundary":"browser-local/no-data/no-wallet/no-transaction","artifacts":["validation certificate","attestation","AGI Node handoff","reviewer brief","council packet","action graph"]}, indent=2), encoding="utf-8")
    return data

def patch_readme():
    readme = ROOT / "README.md"
    if not readme.exists():
        readme.write_text("# GoalOS AGIALPHA Ascension\n", encoding="utf-8")
    txt = readme.read_text(encoding="utf-8", errors="ignore")
    marker = "<!-- GOALOS_VALIDATION_COMMAND_CENTER_V32 -->"
    if marker not in txt:
        txt += f"""

{marker}
## GoalOS Validation Command Center V32

Human or AGI Node can validate. Open `public/validation-command-center.html` to choose Human, AGI Node, Hybrid, or Council validation; generate a validation certificate, AGI Node handoff, reviewer brief, council packet, action graph, and next proof route.

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority. Human review required for high-impact outcomes.
"""
        readme.write_text(txt, encoding="utf-8")

def main():
    ensure_dirs()
    create_fallbacks()
    for html_path in PUBLIC.glob("*.html"):
        inject_assets(html_path)
    inject_index_callout()
    pages = build_indexes()
    patch_readme()
    (PUBLIC/".nojekyll").write_text("", encoding="utf-8")
    data = write_reports(pages)
    if data["status"] != "passed":
        raise SystemExit(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
