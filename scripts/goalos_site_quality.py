#!/usr/bin/env python3
"""Deterministic local-only site route and boundary QA for GoalOS.

The checker is intentionally strict for public-alpha boundaries: a page that lacks
No Data / No Funds / Human Review language (or a link to the trust/no-data
boundary page) is a blocking failure, not a warning.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
REPORTS = ROOT / "reports"

BLOCKING_BROWSER_PATTERNS = {
    "fetch": re.compile(r"\bfetch\s*\("),
    "XMLHttpRequest": re.compile(r"\bXMLHttpRequest\b"),
    "sendBeacon": re.compile(r"\bsendBeacon\s*\("),
    "window.ethereum": re.compile(r"\bwindow\.ethereum\b"),
}
REVIEW_BROWSER_PATTERNS = {
    "localStorage": re.compile(r"\blocalStorage\b"),
    "sessionStorage": re.compile(r"\bsessionStorage\b"),
}

issues: list[dict[str, str]] = []


def add(kind: str, path: str | Path, message: str) -> None:
    issues.append({"kind": kind, "path": str(path), "message": message})


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.scripts: list[str] = []
        self.title = ""
        self.in_title = False
        self.viewport = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"] or "")
        if tag == "script" and data.get("src"):
            self.scripts.append(data["src"] or "")
        if tag == "meta" and (data.get("name") or "").lower() == "viewport":
            self.viewport = True
        if tag == "title":
            self.in_title = True

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def local_target(base: Path, raw: str) -> Path | None:
    target = raw.split("#", 1)[0].split("?", 1)[0]
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "#", "javascript:", "data:")):
        return None
    if target.startswith("/"):
        return (PUBLIC / target.lstrip("/")).resolve()
    return (base.parent / target).resolve()


def scan_browser_apis(path: Path, text: str) -> None:
    rel = path.relative_to(ROOT)
    for name, pattern in BLOCKING_BROWSER_PATTERNS.items():
        if pattern.search(text):
            add("forbidden_browser_api", rel, f"Forbidden public-demo browser API detected: {name}")
    for name, pattern in REVIEW_BROWSER_PATTERNS.items():
        if pattern.search(text):
            add("browser_api_review", rel, f"Browser storage API requires explicit public-alpha review: {name}")


html_pages = sorted(PUBLIC.glob("*.html"))
key_pages = [
    "index.html",
    "pathfinder.html",
    "demo-ecosystem-registry.html",
    "site-health.html",
    "proof-ledger.html",
    "public-proof-ledger.html",
    "proof-run-001-docket.html",
    "external-reviewer-replay-room.html",
    "proof-mission-forge.html",
    "proof-mission-control.html",
    "no-data-no-funds.html",
    "agialpha-token-boundary.html",
    "404.html",
]

for page in key_pages:
    if not (PUBLIC / page).exists():
        add("missing_key_page", Path("public") / page, "Key public page is missing")

referenced_scripts: set[Path] = set()
for page in html_pages:
    text = read(page)
    parser = PageParser()
    parser.feed(text)
    rel = page.relative_to(ROOT)

    if not parser.title.strip():
        add("empty_title", rel, "Missing or empty title tag")
    if not parser.viewport:
        add("missing_viewport", rel, "Missing viewport meta tag")

    lower = text.lower()
    has_direct_boundary = "no user data" in lower and "no user funds" in lower and "human review required" in lower
    has_boundary_link = "no-data-no-funds.html" in lower or "trust-boundary" in lower
    if not (has_direct_boundary or has_boundary_link):
        add("boundary_link_gap", rel, "Page lacks direct or linked no-data/no-funds/human-review boundary language")

    for href in parser.links:
        candidate = local_target(page, href)
        if candidate and candidate.suffix == ".html" and not candidate.exists():
            add("broken_html_link", rel, f"Broken local HTML link: {href}")

    scan_browser_apis(page, text)

    for src in parser.scripts:
        candidate = local_target(page, src)
        if candidate and candidate.suffix == ".js":
            if candidate.exists():
                referenced_scripts.add(candidate)
            else:
                add("missing_script_asset", rel, f"Referenced local script is missing: {src}")

for script in sorted(set(PUBLIC.glob("assets/**/*.js")) | referenced_scripts):
    scan_browser_apis(script, read(script))

if (PUBLIC / "search-index.json").exists():
    try:
        json.loads(read(PUBLIC / "search-index.json"))
    except json.JSONDecodeError as exc:
        add("invalid_search_index", "public/search-index.json", f"search-index.json is invalid JSON: {exc}")

if (PUBLIC / "sitemap.xml").exists():
    sitemap = read(PUBLIC / "sitemap.xml")
    for page in ["index.html", "pathfinder.html", "demo-ecosystem-registry.html", "agialpha-token-boundary.html"]:
        if page not in sitemap:
            add("sitemap_gap", "public/sitemap.xml", f"{page} missing from sitemap")

blocking_kinds = {
    "missing_key_page",
    "empty_title",
    "missing_viewport",
    "boundary_link_gap",
    "broken_html_link",
    "forbidden_browser_api",
    "missing_script_asset",
    "invalid_search_index",
    "sitemap_gap",
}
blocking_issues = [issue for issue in issues if issue["kind"] in blocking_kinds]

route_report = {
    "status": "passed" if not blocking_issues else "failed",
    "html_pages_found": len(html_pages),
    "key_pages": key_pages,
    "blocking_issue_count": len(blocking_issues),
    "issues": issues,
    "system_pages": ["public/404.html"],
}
quality_report = {
    **route_report,
    "boundary_gaps": [issue for issue in issues if issue["kind"] == "boundary_link_gap"],
    "browser_api_issues": [issue for issue in issues if "browser_api" in issue["kind"]],
    "broken_links": [issue for issue in issues if issue["kind"] == "broken_html_link"],
    "recommendations": [
        "Fail on missing boundary language before publishing public pages.",
        "Keep 404 classified as a system page, not a demo.",
        "Keep browser demos local-only unless explicitly reviewed and claim-bounded.",
    ],
}

REPORTS.mkdir(exist_ok=True)
(REPORTS / "site-route-health.json").write_text(json.dumps(route_report, indent=2) + "\n", encoding="utf-8")
(REPORTS / "site-quality.json").write_text(json.dumps(quality_report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(quality_report, indent=2))
sys.exit(0 if route_report["status"] == "passed" else 1)
