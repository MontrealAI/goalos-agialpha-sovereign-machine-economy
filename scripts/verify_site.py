from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
REPORT = ROOT / "reports" / "site-qa.json"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[str] = []
        self.has_h1 = False
        self.has_title = False
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        if tag == "a" and attrs_d.get("href"):
            self.links.append(attrs_d["href"])
        if tag == "img" and attrs_d.get("src"):
            self.images.append(attrs_d["src"])
        if tag == "h1":
            self.has_h1 = True
        if tag == "title":
            self.has_title = True

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


def local_target_exists(page: Path, href: str) -> bool:
    if href.startswith(("http://", "https://", "mailto:", "tel:")) or href.startswith("#"):
        return True
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return True
    return (page.parent / clean).exists()


def main() -> int:
    manifest = json.loads((ROOT / "content" / "site_manifest.json").read_text(encoding="utf-8"))
    expected = {"index.html" if p["slug"] == "index" else f"{p['slug']}.html" for p in manifest.get("pages", [])}
    errors: list[str] = []
    warnings: list[str] = []
    pages = sorted(PUBLIC.glob("*.html"))
    found = {p.name for p in pages}
    missing = sorted(expected - found)
    extra = sorted(found - expected)
    for name in missing:
        errors.append(f"missing generated page: {name}")
    if extra:
        warnings.append(f"extra generated pages: {', '.join(extra)}")
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="ignore")
        parser = LinkParser(); parser.feed(text)
        visible = " ".join(parser.text_parts).strip()
        if len(visible) < 500:
            errors.append(f"page appears too short: {page.name}")
        if "Claim Boundary" not in text or "does not claim" not in text:
            errors.append(f"claim boundary missing: {page.name}")
        if not re.search(r"<h1[^>]*>", text, re.I):
            errors.append(f"missing h1: {page.name}")
        if not re.search(r"<title>.+?</title>", text, re.I | re.S):
            errors.append(f"missing title: {page.name}")
        for href in parser.links:
            if not local_target_exists(page, href):
                errors.append(f"broken local link in {page.name}: {href}")
        for src in parser.images:
            if not local_target_exists(page, src):
                errors.append(f"missing image asset in {page.name}: {src}")
    for required in ["assets/goalos.css", "assets/goalos.js", "assets/goalos-mark.svg", "site-status.json", "search-index.json", "sitemap.xml", "robots.txt", "manifest.webmanifest"]:
        if not (PUBLIC / required).exists():
            errors.append(f"missing public asset: {required}")
    REPORT.parent.mkdir(exist_ok=True)
    payload = {
        "status": "pass" if not errors else "fail",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pages_checked": len(pages),
        "expected_pages": len(expected),
        "errors": errors,
        "warnings": warnings,
    }
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if errors:
        print(json.dumps(payload, indent=2))
        return 1
    print(f"Site QA passed. Report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
