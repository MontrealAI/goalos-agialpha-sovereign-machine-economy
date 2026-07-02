
import json, os, re, shutil, zipfile
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path.cwd()
PAYLOAD = Path(__file__).resolve().parents[1] / "payload"
PUBLIC = ROOT / "public"

GENERATED = PAYLOAD / "generated_public"
SNAPSHOT = PAYLOAD / "public_snapshot"
REPORTS = ROOT / "reports"
CONTENT = ROOT / "content" / "goalos"

KEY_PAGES = {
    "index.html","start-here.html","pathfinder.html","site-map.html","demo-ecosystem-registry.html",
    "search.html","site-health.html","website-operating-system.html","trust-boundary.html",
    "token-boundary.html","privacy.html","data-boundary.html","no-data-no-funds.html","docs.html",
    "proof-run-001-docket.html","404.html","commercial-evidence.html","pilot-program.html",
    "proof-metrics-dashboard.html","claim-boundary.html","capability-stack.html","repository-map.html",
    "website-autopilot.html"
}
FORBIDDEN = ["fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "window.ethereum"]

def copytree_missing(src, dst):
    if not src.exists():
        return 0
    copied = 0
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        target = dst / rel
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
            copied += 1
    return copied

def copytree_overwrite(src, dst):
    copied = 0
    for p in src.rglob("*"):
        if p.is_dir():
            continue
        rel = p.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        copied += 1
    return copied

def inject_nav(path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if "goalos-site-premium-experience-v15.css" not in text:
        link = '<link rel="stylesheet" href="assets/goalos-site-premium-experience-v15.css">\n'
        if "</head>" in text:
            text = text.replace("</head>", link + "</head>", 1)
    if "goalos-site-index-data-v15.js" not in text:
        scripts = '<script src="assets/goalos-site-index-data-v15.js" defer></script>\n<script src="assets/goalos-site-premium-experience-v15.js" defer></script>\n'
        if "</head>" in text:
            text = text.replace("</head>", scripts + "</head>", 1)
    if "Open all pages" not in text:
        floating = '<a class="btn primary float-map" href="site-map.html">Open all pages</a>\n'
        if "</body>" in text:
            text = text.replace("</body>", floating + "</body>", 1)
        else:
            text += floating
    path.write_text(text, encoding="utf-8")

def routes_from_public():
    routes = []
    for p in sorted(PUBLIC.glob("*.html")):
        s = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"<title>(.*?)</title>", s, re.I | re.S)
        title = re.sub(r"\s+", " ", m.group(1)).strip() if m else p.stem.replace("-", " ").title()
        routes.append({"path": p.name, "title": title, "system": p.name == "404.html"})
    return routes

def audit_links():
    broken = []
    htmls = list(PUBLIC.glob("*.html"))
    for p in htmls:
        s = p.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r'href=["\']([^"\']+)["\']', s):
            if not href or href.startswith(("#","http:","https:","mailto:","javascript:")):
                continue
            if href.startswith("../"):
                broken.append({"page": p.name, "href": href, "problem": "root_escape"})
                continue
            clean = href.split("#")[0].split("?")[0]
            if not clean or clean.endswith("/"):
                continue
            if clean.endswith(".html") and not (PUBLIC / clean).exists():
                broken.append({"page": p.name, "href": href, "problem": "missing_html"})
    return broken

def audit_forbidden():
    hits = []
    for p in [PUBLIC / "assets" / "goalos-site-premium-experience-v15.js", PUBLIC / "assets" / "goalos-site-index-data-v15.js"]:
        if not p.exists():
            continue
        s = p.read_text(encoding="utf-8", errors="ignore")
        for token in FORBIDDEN:
            if token in s:
                hits.append({"file": str(p.relative_to(ROOT)), "token": token})
    return hits

def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    CONTENT.mkdir(parents=True, exist_ok=True)

    restored = copytree_missing(SNAPSHOT, PUBLIC)
    generated = copytree_overwrite(GENERATED, PUBLIC)

    for src in ["content/goalos", "docs", "reports", "evidence", "issue-bodies", ".github"]:
        sp = PAYLOAD / src
        if sp.exists():
            copytree_overwrite(sp, ROOT / src)

    for p in PUBLIC.glob("*.html"):
        if p.name not in KEY_PAGES:
            inject_nav(p)

    routes = routes_from_public()
    broken = audit_links()
    forbidden = audit_forbidden()

    status = "passed" if not broken and not forbidden else "review"
    report = {
        "status": status,
        "version": "v0.37.0-site-premium-experience-v15",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "restored_missing_snapshot_files": restored,
        "generated_files_written": generated,
        "public_pages": len([r for r in routes if not r["system"]]),
        "system_pages": len([r for r in routes if r["system"]]),
        "broken_internal_html_links": broken,
        "forbidden_browser_api_hits": forbidden,
        "boundary": "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."
    }
    (REPORTS / "site-premium-experience-v15-install-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (REPORTS / "site-premium-experience-v15-qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if status != "passed":
        raise SystemExit(1)

if __name__ == "__main__":
    main()
