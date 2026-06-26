from __future__ import annotations

import html
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = ROOT / "content" / "site_manifest.json"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_href(slug: str) -> str:
    return "index.html" if slug == "index" else f"{slug}.html"


def card(item: dict) -> str:
    link = item.get("link")
    cta = f'<a class="card-link" href="{esc(link)}">Open →</a>' if link else ""
    return f'''<article class="card">
      <h3>{esc(item.get('title',''))}</h3>
      <p>{esc(item.get('text',''))}</p>
      {cta}
    </article>'''


def checklist(items: list[str]) -> str:
    rows = "".join(f'<li><span>{idx}</span><p>{esc(item)}</p></li>' for idx, item in enumerate(items, 1))
    return f'<ol class="checklist">{rows}</ol>'


def section_html(section: dict) -> str:
    cards = section.get("cards") or []
    card_grid = f'<div class="grid cards">{"".join(card(c) for c in cards)}</div>' if cards else ""
    checks = checklist(section.get("checklist") or []) if section.get("checklist") else ""
    return f'''<section class="content-section">
      <div class="section-copy">
        <p class="kicker">GoalOS Surface</p>
        <h2>{esc(section.get('title',''))}</h2>
        <p>{esc(section.get('text',''))}</p>
      </div>
      {card_grid}
      {checks}
    </section>'''


def nav_html(manifest: dict) -> str:
    priority = ["index", "start", "mission-os", "evidence", "trust-center", "claim-boundary", "repository-map"]
    pages = manifest["pages"]
    ordered = [p for slug in priority for p in pages if p["slug"] == slug]
    return "".join(f'<a href="{page_href(p["slug"])}">{esc(p["nav"])}</a>' for p in ordered)


def all_pages_menu(manifest: dict) -> str:
    links = "".join(f'<a href="{page_href(p["slug"])}">{esc(p["title"])}</a>' for p in manifest["pages"])
    return f'<div class="all-pages" id="all-pages"><h2>Explore the repository website</h2><div>{links}</div></div>'


def metrics(manifest: dict) -> str:
    return "".join(f'''<article class="metric"><strong>{esc(k['value'])}</strong><span>{esc(k['label'])}</span><p>{esc(k['detail'])}</p></article>''' for k in manifest.get("kpis", []))


def proof_flow(manifest: dict) -> str:
    return "".join(f'<li><span>{idx}</span>{esc(step)}</li>' for idx, step in enumerate(manifest.get("proof_flow", []), 1))


def source_lineage(manifest: dict) -> str:
    return "".join(f'''<li><a href="{esc(r['url'])}">{esc(r['name'])}</a><small>{esc(r['role'])}</small></li>''' for r in manifest.get("generated_from", []))


def shell(manifest: dict, page: dict, body: str) -> str:
    nav = nav_html(manifest)
    badges = "".join(f'<span>{esc(b)}</span>' for b in manifest.get("hero_badges", []))
    law = "".join(f'<li>{esc(item)}</li>' for item in manifest.get("operating_law", []))
    title = f"{page['title']} · {manifest['short_title']}"
    description = page.get("body") or manifest["subtitle"]
    json_ld = {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": page.get("headline", page.get("title")),
        "description": description,
        "isPartOf": {"@type": "CreativeWork", "name": manifest["title"]},
    }
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="theme-color" content="#05050a">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(page.get('headline', manifest['title']))}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="assets/social-preview.svg">
  <link rel="icon" href="assets/goalos-mark.svg" type="image/svg+xml">
  <link rel="manifest" href="manifest.webmanifest">
  <link rel="stylesheet" href="assets/goalos.css">
  <script type="application/ld+json">{json.dumps(json_ld)}</script>
  <script defer src="assets/goalos.js"></script>
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="topbar">
    <a class="brand" href="index.html" aria-label="GoalOS Ascension Home"><img src="assets/goalos-mark.svg" alt=""/> <span>{esc(manifest['short_title'])}</span></a>
    <nav aria-label="Primary navigation">{nav}<a href="#all-pages">All pages</a></nav>
  </header>
  <main id="main">
    <section class="hero">
      <div class="orb orb-one"></div><div class="orb orb-two"></div>
      <p class="eyebrow">{esc(page.get('eyebrow',''))}</p>
      <h1>{esc(page.get('headline',''))}</h1>
      <p class="lede">{esc(page.get('body',''))}</p>
      <div class="badges">{badges}</div>
      <div class="hero-actions"><a class="button primary" href="{esc(page.get('cta_href','start.html'))}">{esc(page.get('cta','Start'))}</a><a class="button ghost" href="claim-boundary.html">Read claim boundary</a></div>
    </section>
    <section class="metrics" aria-label="Repository metrics">{metrics(manifest)}</section>
    {body}
    <section class="proof-flow">
      <p class="kicker">Proof-settled operating loop</p>
      <h2>From objective to reusable capability</h2>
      <ol>{proof_flow(manifest)}</ol>
    </section>
    <section class="law">
      <p class="kicker">Operating Law</p>
      <h2>The rules that protect the institution</h2>
      <ul>{law}</ul>
    </section>
    <section class="claim-boundary" id="claim-boundary">
      <p class="kicker">Evidence boundary</p>
      <h2>Claim Boundary</h2>
      <p>{esc(manifest.get('claim_boundary',''))}</p>
      <a class="card-link" href="claim-boundary.html">Read the full boundary →</a>
    </section>
    <section class="lineage">
      <p class="kicker">Source lineage</p>
      <h2>Built from public GoalOS and AGIALPHA lineage</h2>
      <ul>{source_lineage(manifest)}</ul>
    </section>
    {all_pages_menu(manifest)}
  </main>
  <footer>
    <p>Generated by GoalOS Institutional Autopilot · Public proof, private data · <a href="site-status.json">site status</a> · <a href="search-index.json">search index</a> · <a href="sitemap.xml">sitemap</a></p>
  </footer>
</body>
</html>'''


def write_assets(manifest: dict) -> None:
    assets = PUBLIC / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    (assets / "goalos.css").write_text(r'''
:root{--bg:#05050a;--ink:#fffaf0;--muted:#d9d0e8;--subtle:#a59bbd;--line:rgba(255,255,255,.14);--panel:rgba(255,255,255,.075);--panel2:rgba(255,255,255,.045);--gold:#f8d47a;--violet:#a78bfa;--blue:#7dd3fc;--green:#8ef5c5;--shadow:0 30px 100px rgba(0,0,0,.36)}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#05050a;color:var(--ink);font:16px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;overflow-x:hidden}body:before{content:"";position:fixed;inset:0;z-index:-3;background:radial-gradient(circle at 10% 8%,rgba(167,139,250,.35),transparent 30%),radial-gradient(circle at 86% 12%,rgba(248,212,122,.20),transparent 24%),radial-gradient(circle at 60% 85%,rgba(125,211,252,.18),transparent 32%),linear-gradient(135deg,#05050a 0%,#090914 44%,#030306 100%)}body:after{content:"";position:fixed;inset:0;z-index:-2;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:56px 56px;mask-image:linear-gradient(to bottom,rgba(0,0,0,.78),transparent 80%)}a{color:#f3e8ff;text-decoration:none}a:hover{text-decoration:underline}.skip{position:absolute;left:-999px;top:8px;background:#fff;color:#000;padding:8px 12px;border-radius:10px}.skip:focus{left:8px;z-index:99}.topbar{position:sticky;top:0;z-index:10;display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 24px;border-bottom:1px solid var(--line);background:rgba(5,5,10,.78);backdrop-filter:blur(18px)}.brand{display:flex;align-items:center;gap:10px;color:white;font-weight:950;letter-spacing:-.02em}.brand img{width:34px;height:34px}nav{display:flex;gap:14px;align-items:center;flex-wrap:wrap;justify-content:flex-end}nav a{font-size:13px;color:var(--muted);font-weight:750}main{max-width:1240px;margin:0 auto;padding:0 22px 64px}.hero{position:relative;padding:96px 0 48px;min-height:560px;display:flex;flex-direction:column;justify-content:center}.orb{position:absolute;border-radius:999px;filter:blur(1px);pointer-events:none}.orb-one{width:280px;height:280px;right:4%;top:76px;background:radial-gradient(circle,rgba(248,212,122,.24),transparent 65%)}.orb-two{width:420px;height:420px;left:-15%;bottom:-60px;background:radial-gradient(circle,rgba(167,139,250,.22),transparent 65%)}.eyebrow,.kicker{color:var(--gold);font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:950;margin:0 0 14px}h1{font-size:clamp(48px,8.4vw,112px);line-height:.88;margin:0 0 24px;max-width:1120px;letter-spacing:-.075em}h2{font-size:clamp(31px,4.4vw,58px);line-height:1;letter-spacing:-.055em;margin:0 0 18px}h3{font-size:22px;line-height:1.1;margin:0 0 10px}.lede{max-width:900px;color:var(--muted);font-size:clamp(19px,2vw,24px);margin:0}.badges{display:flex;flex-wrap:wrap;gap:10px;margin:30px 0}.badges span{border:1px solid var(--line);background:linear-gradient(180deg,rgba(255,255,255,.10),rgba(255,255,255,.04));padding:8px 12px;border-radius:999px;color:#fbf7ff;font-size:13px}.hero-actions{display:flex;gap:12px;flex-wrap:wrap}.button{display:inline-flex;align-items:center;justify-content:center;min-height:46px;border-radius:999px;padding:13px 19px;font-weight:950;border:1px solid var(--line);box-shadow:var(--shadow)}.button.primary{background:linear-gradient(135deg,rgba(248,212,122,.30),rgba(167,139,250,.26));border-color:rgba(248,212,122,.52);color:#fff}.button.ghost{background:rgba(255,255,255,.055);color:var(--muted)}.metrics{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin:0 0 52px}.metric{border:1px solid var(--line);background:linear-gradient(180deg,var(--panel),var(--panel2));border-radius:22px;padding:18px;min-height:132px;box-shadow:0 20px 70px rgba(0,0,0,.18)}.metric strong{display:block;font-size:32px;line-height:1;color:white;letter-spacing:-.04em}.metric span{display:block;color:var(--gold);font-weight:900;margin-top:8px}.metric p{color:var(--subtle);font-size:13px;margin:6px 0 0}.content-section,.proof-flow,.law,.claim-boundary,.lineage,.all-pages{margin:28px 0;border:1px solid var(--line);background:linear-gradient(180deg,var(--panel),var(--panel2));border-radius:32px;padding:30px;box-shadow:var(--shadow);position:relative;overflow:hidden}.content-section:before,.proof-flow:before,.claim-boundary:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 100% 0,rgba(248,212,122,.10),transparent 35%);pointer-events:none}.section-copy{max-width:880px;position:relative}.section-copy p:not(.kicker),.content-section>p,.law li,.claim-boundary p,.lineage small,.card p,.checklist p{color:var(--muted)}.grid.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin-top:24px}.card{position:relative;border:1px solid var(--line);background:rgba(255,255,255,.055);border-radius:24px;padding:22px;min-height:172px}.card:after{content:"";position:absolute;left:22px;right:22px;top:0;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.5}.card-link{display:inline-flex;margin-top:10px;color:white;font-weight:950}.checklist{counter-reset:item;display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px;padding:0;margin:24px 0 0;list-style:none}.checklist li{display:flex;gap:12px;align-items:flex-start;border:1px solid var(--line);border-radius:20px;background:rgba(255,255,255,.045);padding:16px}.checklist span,.proof-flow span{display:inline-grid;place-items:center;flex:0 0 auto;width:32px;height:32px;border-radius:999px;background:rgba(248,212,122,.15);color:var(--gold);font-weight:950}.checklist p{margin:2px 0 0}.proof-flow ol{display:grid;grid-template-columns:repeat(auto-fit,minmax(175px,1fr));gap:12px;list-style:none;padding:0;margin:22px 0 0}.proof-flow li{border:1px solid var(--line);background:rgba(255,255,255,.055);border-radius:18px;padding:14px;color:#fff;display:flex;align-items:center;gap:10px;font-weight:800}.law ul{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px;padding:0;list-style:none;margin:22px 0 0}.law li{border:1px solid var(--line);background:rgba(255,255,255,.045);border-radius:18px;padding:14px;font-weight:850}.claim-boundary{border-color:rgba(248,212,122,.35);background:linear-gradient(135deg,rgba(248,212,122,.13),rgba(167,139,250,.09),rgba(255,255,255,.035))}.lineage ul{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:12px;list-style:none;padding:0;margin:22px 0 0}.lineage li{border:1px solid var(--line);border-radius:18px;background:rgba(255,255,255,.045);padding:16px}.lineage small{display:block;margin-top:6px}.all-pages div{display:flex;gap:10px;flex-wrap:wrap}.all-pages a{border:1px solid var(--line);background:rgba(255,255,255,.05);border-radius:999px;padding:8px 12px;color:var(--muted);font-size:13px}code{background:rgba(255,255,255,.10);padding:.15em .42em;border-radius:7px}footer{border-top:1px solid var(--line);text-align:center;padding:34px 20px;color:var(--subtle)}footer a{color:var(--muted)}@media(max-width:980px){.metrics{grid-template-columns:repeat(2,1fr)}.topbar{align-items:flex-start;flex-direction:column}nav{justify-content:flex-start}.hero{padding:64px 0 40px;min-height:auto}}@media(max-width:620px){main{padding-left:16px;padding-right:16px}.metrics{grid-template-columns:1fr}.content-section,.proof-flow,.law,.claim-boundary,.lineage,.all-pages{padding:22px;border-radius:24px}h1{font-size:44px}.lede{font-size:18px}.badges span{font-size:12px}}
''', encoding="utf-8")
    (assets / "goalos.js").write_text(r'''
const init=()=>{document.body.dataset.goalos='ready';const links=[...document.querySelectorAll('a[href^="#"]')];for(const a of links){a.addEventListener('click',e=>{const id=a.getAttribute('href').slice(1);const el=document.getElementById(id);if(el){e.preventDefault();el.scrollIntoView({behavior:'smooth',block:'start'});}})}};document.readyState==='loading'?document.addEventListener('DOMContentLoaded',init):init();
''', encoding="utf-8")
    (assets / "goalos-mark.svg").write_text(r'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><defs><radialGradient id="a" cx="35%" cy="25%"><stop offset="0" stop-color="#f8d47a"/><stop offset=".55" stop-color="#a78bfa"/><stop offset="1" stop-color="#05050a"/></radialGradient></defs><rect width="512" height="512" rx="112" fill="#05050a"/><circle cx="256" cy="256" r="164" fill="url(#a)" opacity=".92"/><path d="M135 260c55-86 187-86 242 0-55 86-187 86-242 0Z" fill="none" stroke="#fffaf0" stroke-width="18"/><circle cx="256" cy="260" r="52" fill="#fffaf0"/><circle cx="256" cy="260" r="22" fill="#05050a"/></svg>''', encoding="utf-8")
    (assets / "social-preview.svg").write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630"><defs><radialGradient id="g" cx="20%" cy="0%"><stop offset="0" stop-color="#a78bfa"/><stop offset=".4" stop-color="#111126"/><stop offset="1" stop-color="#05050a"/></radialGradient></defs><rect width="1200" height="630" fill="url(#g)"/><circle cx="970" cy="150" r="170" fill="#f8d47a" opacity=".15"/><text x="70" y="120" fill="#f8d47a" font-family="Inter,Arial" font-size="28" font-weight="800" letter-spacing="4">GOALOS AGIALPHA ASCENSION</text><text x="70" y="255" fill="#fffaf0" font-family="Inter,Arial" font-size="78" font-weight="900">Sovereign Machine</text><text x="70" y="345" fill="#fffaf0" font-family="Inter,Arial" font-size="78" font-weight="900">Economy</text><text x="70" y="440" fill="#d9d0e8" font-family="Inter,Arial" font-size="34">AI creates output. GoalOS creates proof.</text><text x="70" y="520" fill="#fffaf0" font-family="Inter,Arial" font-size="28">No proof, no settlement · Public proof, private data</text></svg>''', encoding="utf-8")


def page_body(page: dict) -> str:
    return "\n".join(section_html(section) for section in page.get("sections", []))


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    PUBLIC.mkdir(parents=True, exist_ok=True)
    write_assets(manifest)
    search = []
    for page in manifest["pages"]:
        filename = page_href(page["slug"])
        document = shell(manifest, page, page_body(page))
        (PUBLIC / filename).write_text(document, encoding="utf-8")
        search.append({
            "title": page["title"],
            "url": filename,
            "headline": page.get("headline", ""),
            "text": page.get("body", "") + " " + " ".join(section.get("text", "") for section in page.get("sections", [])),
        })
    urls = "\n".join(f"  <url><loc>{page_href(page['slug'])}</loc></url>" for page in manifest["pages"])
    (PUBLIC / "sitemap.xml").write_text(f'''<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n''', encoding="utf-8")
    (PUBLIC / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: sitemap.xml\n", encoding="utf-8")
    (PUBLIC / "manifest.webmanifest").write_text(json.dumps({
        "name": manifest["title"], "short_name": manifest["short_title"], "start_url": "index.html", "display": "standalone", "background_color": "#05050a", "theme_color": "#05050a", "icons": [{"src":"assets/goalos-mark.svg","sizes":"512x512","type":"image/svg+xml"}]
    }, indent=2), encoding="utf-8")
    status = {
        "status": "generated",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "page_count": len(manifest["pages"]),
        "claim_boundary_present": bool(manifest.get("claim_boundary")),
        "tagline": manifest.get("tagline"),
        "source": "content/site_manifest.json",
    }
    (PUBLIC / "site-status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (PUBLIC / "search-index.json").write_text(json.dumps(search, indent=2), encoding="utf-8")
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "autopilot-summary.md").write_text(f'''# GoalOS Institutional Autopilot Summary\n\nGenerated at: {status['generated_at_utc']}\n\nPages generated: {status['page_count']}\n\nClaim boundary present: {status['claim_boundary_present']}\n\nPrimary website source: `content/site_manifest.json`\n\nPublic output: `public/`\n''', encoding="utf-8")
    print(f"Generated {len(manifest['pages'])} pages in public/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
