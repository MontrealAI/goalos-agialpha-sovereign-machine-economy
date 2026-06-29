#!/usr/bin/env python3
from pathlib import Path
import json, datetime

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
PAGE = "value-realization-control-room.html"
TITLE = "GoalOS Value Realization Control Room V1"
URL = f"https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/{PAGE}"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read(path)
    if marker not in text:
        write(path, text + "\n\n" + block.strip() + "\n")


def patch_readme() -> None:
    block = f"""
<!-- GOALOS_VALUE_REALIZATION_CONTROL_ROOM_V1 -->
## GoalOS Value Realization Control Room V1

**Verified work becomes allocable capacity.** This browser-local public demo shows how accepted evidence can become a Value Realization Ledger, Capacity Allocation Policy, Strategic Capability Asset Map, Sovereign Invention Reserve entry, and harder future mission path.

Live page: [{TITLE}]({URL})

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
<!-- /GOALOS_VALUE_REALIZATION_CONTROL_ROOM_V1 -->
"""
    append_once(ROOT / "README.md", "GOALOS_VALUE_REALIZATION_CONTROL_ROOM_V1", block)


def patch_index() -> None:
    path = ROOT / "public/index.html"
    if not path.exists():
        return
    text = read(path)
    card = """
<section class=\"goalos-vr-card\" style=\"max-width:1120px;margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.16);border-radius:24px;background:rgba(255,255,255,.06);color:#fff\">
  <p style=\"color:#ffe875;letter-spacing:.22em;text-transform:uppercase;font-weight:900\">New public demo</p>
  <h2 style=\"font-size:clamp(28px,4vw,54px);line-height:1;letter-spacing:-.05em;margin:.2em 0\">Verified work becomes allocable capacity.</h2>
  <p style=\"font-size:18px;max-width:780px\">Run the Value Realization Control Room: accepted proof → reusable capability → value ledger → capacity allocation → harder mission.</p>
  <a href=\"value-realization-control-room.html\" style=\"display:inline-block;margin-top:10px;background:#ffe875;color:#06111c;padding:13px 18px;border-radius:999px;font-weight:900;text-decoration:none\">Open Value Room</a>
</section>
"""
    if "goalos-vr-card" not in text:
        write(path, text.replace("</main>", card + "\n</main>") if "</main>" in text else text + card)


def patch_json_index() -> None:
    path = ROOT / "public/search-index.json"
    item = {
        "title": TITLE,
        "url": PAGE,
        "description": "Verified work becomes allocable capacity.",
        "tags": ["value", "capacity", "allocation", "proof", "capability"],
    }
    try:
        data = json.loads(read(path)) if path.exists() else []
    except Exception:
        data = []
    if isinstance(data, dict):
        arr = data.get("pages") or data.get("items") or []
        if not any(isinstance(x, dict) and x.get("url") == PAGE for x in arr):
            arr.append(item)
        data["pages"] = arr
    elif isinstance(data, list):
        if not any(isinstance(x, dict) and x.get("url") == PAGE for x in data):
            data.append(item)
    else:
        data = [item]
    write(path, json.dumps(data, indent=2))


def patch_sitemap() -> None:
    path = ROOT / "public/sitemap.xml"
    url_entry = f"  <url><loc>{URL}</loc></url>\n"
    if not path.exists():
        write(path, f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n{url_entry}</urlset>\n")
        return
    text = read(path)
    if URL not in text:
        write(path, text.replace("</urlset>", url_entry + "</urlset>") if "</urlset>" in text else text + "\n" + url_entry)


def write_content() -> None:
    content = {
        "name": TITLE,
        "url": PAGE,
        "canonical_url": URL,
        "one_line": "Verified work becomes allocable capacity.",
        "category": "capacity allocation / value realization / adoption bridge",
        "inputs": ["scenario", "candidate capability", "verified work strength", "reusability", "governance", "risk", "allocation policy", "proof gates"],
        "outputs": ["Value Realization Ledger", "Capacity Allocation Plan", "Strategic Capability Asset Map", "Sovereign Invention Reserve Entry", "Reviewer Brief"],
        "gates": ["Evidence Docket", "Validator review", "Capability package", "Value ledger", "Capacity allocation policy", "Risk/legal boundary", "No-data/no-funds boundary", "Human review"],
        "boundary": {"no_user_data": True, "no_user_funds": True, "wallet_or_mainnet": False, "network_calls": False, "human_review_required": True},
        "generated_at": NOW,
    }
    write(ROOT / "content/goalos/value-realization-control-room-v1.json", json.dumps(content, indent=2))


def main() -> None:
    patch_readme()
    patch_index()
    patch_json_index()
    patch_sitemap()
    write_content()
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    report = {
        "status": "passed",
        "installed": TITLE,
        "page": PAGE,
        "generated_at": NOW,
        "browser_local": True,
        "no_user_data": True,
        "no_user_funds": True,
        "wallet_or_mainnet": False,
        "human_review_required": True,
    }
    write(ROOT / "reports/value-realization-control-room-v1-install-report.json", json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
