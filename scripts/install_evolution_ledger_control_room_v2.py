#!/usr/bin/env python3
from pathlib import Path
import json, datetime, re

ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

REQUIRED = [
    "public/evolution-ledger-control-room.html",
    "public/assets/goalos-evolution-ledger-control-room-v2.css",
    "public/assets/goalos-evolution-ledger-control-room-v2.js",
    "docs/demos/EVOLUTION_LEDGER_CONTROL_ROOM_V2.md",
    "docs/reviewer/HOW_TO_REVIEW_EVOLUTION_LEDGER_CONTROL_ROOM_V2.md",
]

def ensure_link(path: str, label: str, href: str):
    p = ROOT / path
    if not p.exists():
        return False
    text = p.read_text(encoding="utf-8", errors="ignore")
    if href in text:
        return True
    marker = "<!-- GOALOS_EVOLUTION_LEDGER_CONTROL_ROOM_V2_LINK -->"
    block = f"\n{marker}\n\n### {label}\n\n- [{label}]({href}) — browser-local demo: the ledger remembers proof, not secrets.\n"
    if path.endswith(".md"):
        text += block
    else:
        insert = f'\n<a href="{href}">{label}</a>\n'
        text = text.replace("</nav>", f'{insert}</nav>') if "</nav>" in text else text + insert
    p.write_text(text, encoding="utf-8")
    return True

def main():
    errors = [p for p in REQUIRED if not (ROOT / p).exists()]
    if errors:
        raise SystemExit("Missing required files: " + ", ".join(errors))

    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "content/goalos").mkdir(parents=True, exist_ok=True)
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

    ensure_link("README.md", "Evolution Ledger Control Room V2", "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evolution-ledger-control-room.html")
    ensure_link("public/index.html", "Evolution Ledger", "evolution-ledger-control-room.html")

    search = ROOT / "public/search-index.json"
    if search.exists():
        try:
            data = json.loads(search.read_text(encoding="utf-8"))
            if isinstance(data, list) and not any("evolution-ledger-control-room.html" in json.dumps(x) for x in data):
                data.append({
                    "title": "Evolution Ledger Control Room V2",
                    "url": "evolution-ledger-control-room.html",
                    "description": "The ledger remembers proof, not secrets. Browser-local GoalOS proof commitment demo."
                })
                search.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

    sitemap = ROOT / "public/sitemap.xml"
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8", errors="ignore")
        url = "https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/evolution-ledger-control-room.html"
        if url not in text and "</urlset>" in text:
            text = text.replace("</urlset>", f"  <url><loc>{url}</loc></url>\n</urlset>")
            sitemap.write_text(text, encoding="utf-8")

    manifest = {
        "name": "GoalOS Evolution Ledger Control Room V2",
        "status": "installed",
        "generated_at": NOW,
        "public_page": "public/evolution-ledger-control-room.html",
        "fixes": [
            "high-contrast gate labels",
            "static SVG fallback",
            "executive and technical modes",
            "public/private proof boundary visualization",
            "downloadable ledger artifacts",
            "browser-local safety boundary"
        ],
        "boundary": {
            "no_user_data": True,
            "no_user_funds": True,
            "no_wallet": True,
            "no_transaction": True,
            "no_network_call": True,
            "production_authority": False,
            "human_review_required": True
        }
    }
    (ROOT / "reports/evolution-ledger-control-room-v2-install-report.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (ROOT / "content/goalos/evolution-ledger-control-room-v2.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
