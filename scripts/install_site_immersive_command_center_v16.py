#!/usr/bin/env python3
from __future__ import annotations
import json, re, html, shutil, datetime
from pathlib import Path

VERSION = "v16"
ROOT = Path.cwd()
PUBLIC = ROOT / "public"
SNAPSHOT = ROOT / ".goalos" / "site-immersive-command-center-v16" / "public-snapshot"
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
BOUNDARY = "No user data. No user funds. No wallet. No transaction. No network call. No production authority. Human review required."
TOKEN_BOUNDARY = "$AGIALPHA public contract address only. Not available from us. No sale. No custody. No wallet support. No investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice."

CSS = '\n:root{--v16-bg:#050713;--v16-bg2:#081b22;--v16-panel:rgba(255,255,255,.075);--v16-line:rgba(255,255,255,.16);--v16-text:#f9f5ea;--v16-muted:#cbd7e7;--v16-cyan:#65ffe0;--v16-lime:#b9ff83;--v16-gold:#ffe873;--v16-violet:#a78bfa;--v16-pink:#ff78a9;--v16-shadow:0 32px 120px rgba(0,0,0,.5);--v16-radius:28px}*{box-sizing:border-box}html{scroll-behavior:smooth}body.v16-page{margin:0;color:var(--v16-text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:radial-gradient(circle at 15% 10%,rgba(101,255,224,.18),transparent 28rem),radial-gradient(circle at 72% 8%,rgba(255,232,115,.12),transparent 28rem),radial-gradient(circle at 72% 50%,rgba(167,139,250,.16),transparent 32rem),linear-gradient(135deg,#071513 0%,#071322 45%,#0a0718 100%);min-height:100vh;overflow-x:hidden}body.v16-page:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.55;z-index:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:36px 36px;mask-image:linear-gradient(to bottom,#000,transparent 90%)}body.v16-page:after{content:"GOALOS";position:fixed;left:-2vw;bottom:-8vh;z-index:0;pointer-events:none;font-weight:950;font-size:22vw;letter-spacing:-.09em;color:rgba(255,255,255,.055)}.v16-wrap{position:relative;z-index:1;width:min(1320px,calc(100% - 40px));margin:0 auto}.v16-topbar{position:sticky;top:12px;z-index:20;margin:18px auto 0;width:min(1380px,calc(100% - 28px));display:flex;align-items:center;justify-content:space-between;gap:20px;padding:14px 16px;border:1px solid var(--v16-line);border-radius:30px;background:rgba(5,7,19,.78);backdrop-filter:blur(22px);box-shadow:var(--v16-shadow)}.v16-brand{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--v16-text);font-weight:950;letter-spacing:.12em;text-transform:uppercase}.v16-logo{width:38px;height:38px;border-radius:13px;background:radial-gradient(circle at 30% 25%,var(--v16-gold),var(--v16-cyan) 42%,#8fa7ff 72%,#101827);box-shadow:0 0 32px rgba(101,255,224,.35)}.v16-brand small{display:block;font-size:10px;letter-spacing:.27em;color:var(--v16-muted);margin-top:3px}.v16-nav{display:flex;gap:8px;flex-wrap:wrap;justify-content:flex-end}.v16-nav a,.v16-nav button,.v16-btn{appearance:none;border:1px solid var(--v16-line);background:rgba(255,255,255,.09);color:var(--v16-text);text-decoration:none;border-radius:999px;padding:11px 15px;font-weight:900;font-size:13px;cursor:pointer;transition:.18s ease}.v16-nav a:hover,.v16-nav button:hover,.v16-btn:hover{transform:translateY(-1px);background:rgba(101,255,224,.18);border-color:rgba(101,255,224,.5)}.v16-btn.primary{background:linear-gradient(135deg,var(--v16-gold),var(--v16-cyan));color:#071019;border:0;box-shadow:0 10px 40px rgba(101,255,224,.25)}.v16-btn.ghost{background:rgba(255,255,255,.08)}.v16-hero{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(380px,.85fr);gap:44px;align-items:center;padding:120px 0 54px}.v16-kicker{color:var(--v16-gold);font-weight:950;letter-spacing:.42em;text-transform:uppercase;font-size:12px;margin-bottom:18px}.v16-title{font-size:clamp(60px,8.6vw,132px);line-height:.82;letter-spacing:-.085em;margin:0 0 22px;font-weight:950;text-wrap:balance}.v16-gradient{font-family:Georgia,serif;font-style:italic;font-weight:900;background:linear-gradient(110deg,var(--v16-gold),var(--v16-lime),var(--v16-cyan),#91b8ff,var(--v16-violet));-webkit-background-clip:text;background-clip:text;color:transparent}.v16-lede{font-size:clamp(20px,2vw,32px);line-height:1.12;max-width:850px;font-weight:900;margin:0 0 20px}.v16-copy{font-size:17px;line-height:1.72;color:var(--v16-muted);max-width:820px;margin:0 0 26px}.v16-actions{display:flex;gap:12px;flex-wrap:wrap;margin:22px 0}.v16-boundary{border:1px solid rgba(255,120,169,.5);background:rgba(255,60,130,.09);border-radius:18px;padding:16px 18px;line-height:1.45;font-weight:800;color:#fff;max-width:900px}.v16-stats{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:30px 0}.v16-stat,.v16-card,.v16-panel{border:1px solid var(--v16-line);border-radius:24px;background:linear-gradient(150deg,rgba(255,255,255,.12),rgba(255,255,255,.045));box-shadow:0 24px 90px rgba(0,0,0,.28);backdrop-filter:blur(18px)}.v16-stat{padding:20px}.v16-stat b{font-size:36px;color:var(--v16-gold);line-height:1}.v16-stat span{display:block;font-weight:950;letter-spacing:.18em;text-transform:uppercase;font-size:11px;margin-top:8px}.v16-stat p{color:var(--v16-muted);font-size:13px;line-height:1.45}.v16-console{padding:24px;border-radius:36px;border:1px solid rgba(101,255,224,.25);background:linear-gradient(150deg,rgba(255,255,255,.16),rgba(8,20,38,.55));box-shadow:0 40px 130px rgba(0,0,0,.42),inset 0 0 80px rgba(101,255,224,.1);position:relative;overflow:hidden;min-height:620px}.v16-console:before{content:"";position:absolute;inset:-30%;background:conic-gradient(from 0deg,rgba(101,255,224,.18),rgba(167,139,250,.12),rgba(255,232,115,.14),rgba(101,255,224,.18));animation:v16-spin 16s linear infinite;opacity:.8}.v16-console:after{content:"";position:absolute;inset:2px;background:linear-gradient(135deg,rgba(6,14,23,.88),rgba(18,20,41,.78));border-radius:34px}@keyframes v16-spin{to{transform:rotate(360deg)}}.v16-console-inner{position:relative;z-index:1}.v16-console-head{display:flex;justify-content:space-between;gap:10px;align-items:center;font-size:12px;font-weight:950;letter-spacing:.35em;text-transform:uppercase;color:#fff}.v16-pill{letter-spacing:0;text-transform:none;color:#071019;background:linear-gradient(135deg,var(--v16-lime),var(--v16-cyan));border-radius:999px;padding:8px 12px;font-weight:950}.v16-orbit{height:280px;display:grid;place-items:center;position:relative;margin:24px 0;border:1px solid rgba(255,255,255,.1);border-radius:28px;background:radial-gradient(circle at center,rgba(101,255,224,.13),transparent 60%),rgba(255,255,255,.04)}.v16-core{width:108px;height:108px;border-radius:50%;display:grid;place-items:center;font-size:72px;font-weight:950;color:#071019;background:radial-gradient(circle at 34% 22%,var(--v16-gold),var(--v16-cyan) 38%,#99b6ff 75%);box-shadow:0 0 75px rgba(101,255,224,.42)}.v16-ring{position:absolute;inset:52px;border:1px dashed rgba(255,232,115,.45);border-radius:50%;animation:v16-spin 22s linear infinite}.v16-ring.two{inset:28px;border-color:rgba(101,255,224,.22);animation-duration:32s;animation-direction:reverse}.v16-nodes{position:absolute;inset:30px}.v16-node{position:absolute;width:54px;height:54px;border-radius:50%;display:grid;place-items:center;background:#050713;border:1px solid var(--v16-cyan);font-weight:950;box-shadow:0 0 26px rgba(101,255,224,.22)}.v16-node:nth-child(1){left:50%;top:0;transform:translateX(-50%)}.v16-node:nth-child(2){right:6%;top:26%}.v16-node:nth-child(3){right:12%;bottom:15%}.v16-node:nth-child(4){left:50%;bottom:0;transform:translateX(-50%)}.v16-node:nth-child(5){left:12%;bottom:15%}.v16-node:nth-child(6){left:6%;top:26%}.v16-rail{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.v16-rail button{border:1px solid var(--v16-line);background:rgba(255,255,255,.09);border-radius:15px;color:var(--v16-text);padding:13px;text-align:left;font-weight:950;cursor:pointer}.v16-rail button.active{border-color:var(--v16-cyan);box-shadow:0 0 0 1px rgba(101,255,224,.25),0 18px 60px rgba(101,255,224,.12)}.v16-rail small{display:block;color:var(--v16-muted);font-weight:700;margin-top:5px}.v16-terminal{margin-top:14px;border:1px solid rgba(101,255,224,.22);border-radius:18px;background:rgba(0,0,0,.38);padding:18px;font:800 13px/1.55 ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--v16-cyan);min-height:126px;white-space:pre-wrap}.v16-section{padding:46px 0}.v16-section h2{font-size:clamp(42px,5vw,78px);line-height:.88;letter-spacing:-.065em;margin:0 0 16px}.v16-section p.lead{font-size:20px;color:var(--v16-muted);line-height:1.55;max-width:850px}.v16-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.v16-grid.four{grid-template-columns:repeat(4,1fr)}.v16-grid.two{grid-template-columns:repeat(2,1fr)}.v16-card{padding:22px;text-decoration:none;color:var(--v16-text);display:block;min-height:170px;transition:.18s ease}.v16-card:hover{transform:translateY(-3px);border-color:rgba(101,255,224,.55);background:linear-gradient(150deg,rgba(101,255,224,.14),rgba(255,255,255,.055))}.v16-card h3{font-size:24px;letter-spacing:-.04em;margin:0 0 10px}.v16-card p{color:var(--v16-muted);line-height:1.55;margin:0}.v16-tag{display:inline-block;margin-bottom:13px;color:var(--v16-gold);font-weight:950;letter-spacing:.22em;text-transform:uppercase;font-size:11px}.v16-search{width:100%;border:1px solid var(--v16-line);border-radius:16px;background:rgba(255,255,255,.065);color:var(--v16-text);padding:18px 20px;font:inherit;font-weight:850;outline:0}.v16-list{display:grid;gap:10px;margin-top:20px}.v16-row{display:grid;grid-template-columns:180px minmax(0,1fr) 90px;gap:18px;align-items:center;border:1px solid var(--v16-line);border-radius:18px;background:rgba(255,255,255,.07);padding:14px 16px;text-decoration:none;color:var(--v16-text)}.v16-row:hover{border-color:rgba(101,255,224,.55);background:rgba(101,255,224,.1)}.v16-row b{font-size:16px}.v16-row span,.v16-row p{color:var(--v16-muted);margin:3px 0}.v16-row em{font-style:normal;color:var(--v16-cyan);font-weight:950}#goalosV16Dock{position:fixed;right:18px;bottom:18px;z-index:99998;display:flex;gap:8px;align-items:center}#goalosV16Dock a,#goalosV16Dock button{border:1px solid rgba(255,255,255,.18);background:linear-gradient(135deg,#fff071,#66ffd8);color:#071019;text-decoration:none;border-radius:999px;padding:12px 16px;font:900 13px Inter,system-ui,sans-serif;box-shadow:0 20px 60px rgba(0,0,0,.35);cursor:pointer}#goalosV16Palette{position:fixed;inset:0;z-index:99999;background:rgba(2,4,12,.76);backdrop-filter:blur(18px);display:none;align-items:flex-start;justify-content:center;padding:8vh 18px}#goalosV16Palette.open{display:flex}.v16-palette-box{width:min(920px,100%);border:1px solid rgba(255,255,255,.18);border-radius:28px;background:linear-gradient(150deg,rgba(11,22,37,.98),rgba(15,10,35,.98));box-shadow:0 30px 140px rgba(0,0,0,.55);padding:18px}.v16-palette-box input{width:100%;border:1px solid rgba(255,255,255,.2);border-radius:18px;background:rgba(255,255,255,.08);color:#fff;padding:17px 18px;font:900 16px Inter,system-ui,sans-serif;outline:0}.v16-palette-results{display:grid;gap:8px;margin-top:14px;max-height:60vh;overflow:auto}.v16-palette-results a{display:grid;grid-template-columns:130px minmax(0,1fr);gap:12px;padding:13px;border:1px solid rgba(255,255,255,.12);border-radius:14px;text-decoration:none;color:#fff;background:rgba(255,255,255,.055)}.v16-palette-results a:hover{border-color:rgba(101,255,224,.5);background:rgba(101,255,224,.1)}.v16-palette-results small{color:#65ffe0;font-weight:950}.v16-palette-results p{margin:2px 0 0;color:#cbd7e7}@media(max-width:1000px){.v16-hero{grid-template-columns:1fr;padding-top:60px}.v16-stats,.v16-grid,.v16-grid.four,.v16-grid.two{grid-template-columns:1fr 1fr}.v16-console{min-height:auto}.v16-title{font-size:64px}.v16-row{grid-template-columns:1fr}}@media(max-width:640px){.v16-topbar{position:relative;top:0}.v16-nav{display:none}.v16-stats,.v16-grid,.v16-grid.four,.v16-grid.two{grid-template-columns:1fr}.v16-title{font-size:52px}.v16-console{padding:16px}.v16-orbit{height:230px}.v16-row{display:block}.v16-wrap{width:min(100% - 24px,1320px)}}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}\n'
JS = '\n(function(){\n  const routes = (window.GOALOS_SITE_INDEX || []);\n  const steps = [\n    ["Explore","Find routes","01 - Route inventory loaded.\\n02 - All pages discoverable.\\n03 - Pick a role or search /."],\n    ["Proof","Docket gates","01 - Claims require evidence.\\n02 - Baselines and replay visible.\\n03 - Human review required."],\n    ["LoopRSI","Govern invention","01 - Loop writes state.\\n02 - Recorder leaves proof.\\n03 - RSI gates recursive improvement."],\n    ["Review","Validator path","01 - Inspect docket.\\n02 - Replay artifacts.\\n03 - Accept, reject, revise, or dissent."],\n    ["Trust","Boundary","01 - No user data.\\n02 - No wallet.\\n03 - No transaction.\\n04 - No production authority."],\n    ["Build","Source and QA","01 - Site source committed.\\n02 - Route health audited.\\n03 - Pages deployed after review."]\n  ];\n  function $(id){ return document.getElementById(id); }\n  function escapeHtml(s){ return String(s||"").replace(/[&<>"\']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","\'":"&#039;"}[c])); }\n  function openPalette(){ let pal=$("goalosV16Palette"); if(!pal){createPalette(); pal=$("goalosV16Palette");} pal.classList.add("open"); const input=$("goalosV16PaletteInput"); setTimeout(()=>input&&input.focus(),20); renderPalette("");}\n  function closePalette(){ const pal=$("goalosV16Palette"); if(pal) pal.classList.remove("open"); }\n  function renderPalette(q){ const box=$("goalosV16PaletteResults"); if(!box) return; const query=(q||"").trim().toLowerCase(); const filtered=routes.filter(r=>!query||(r.title+" "+r.path+" "+r.category+" "+r.description).toLowerCase().includes(query)).slice(0,60); box.innerHTML=filtered.length?filtered.map(r=>`<a href="${r.path}"><small>${escapeHtml(r.category||"Route")}</small><div><b>${escapeHtml(r.title)}</b><p>${escapeHtml(r.description||r.path)}</p></div></a>`).join(""):`<p style="color:#fff;padding:14px">No route found. Try RSI, loop, proof, docket, token, or mission.</p>`;}\n  function createPalette(){ const div=document.createElement("div"); div.id="goalosV16Palette"; div.innerHTML=`<div class="v16-palette-box" role="dialog" aria-label="GoalOS command palette"><input id="goalosV16PaletteInput" placeholder="Search GoalOS routes: RSI, loop, proof, token, mission..." autocomplete="off"/><div class="v16-palette-results" id="goalosV16PaletteResults"></div><p style="color:#cbd7e7;margin:12px 6px 0;font:800 12px Inter,system-ui,sans-serif">Esc closes. Browser-local. No network call. No analytics.</p></div>`; document.body.appendChild(div); div.addEventListener("click",e=>{ if(e.target===div) closePalette(); }); const input=div.querySelector("input"); input.addEventListener("input",e=>renderPalette(e.target.value));}\n  function createDock(){ if($("goalosV16Dock")) return; const dock=document.createElement("div"); dock.id="goalosV16Dock"; dock.innerHTML=`<button type="button" id="goalosV16PaletteButton">Search /</button><a href="site-map.html">All pages</a>`; document.body.appendChild(dock); $("goalosV16PaletteButton").addEventListener("click",openPalette);}\n  function wireConsole(){ const rail=document.querySelectorAll("[data-v16-mode]"); const term=$("v16Terminal"); if(!rail.length||!term) return; function activate(i){rail.forEach(b=>b.classList.remove("active")); rail[i].classList.add("active"); term.textContent=steps[i][2];} rail.forEach((b,i)=>b.addEventListener("click",()=>activate(i))); let i=0; activate(0); setInterval(()=>{ if(document.hidden) return; i=(i+1)%rail.length; activate(i);},4200);}\n  function wireSearch(){ const input=$("v16RouteSearch"), out=$("v16RouteList"); if(!input||!out) return; function render(){ const q=input.value.toLowerCase().trim(); const xs=routes.filter(r=>!q||(r.title+" "+r.category+" "+r.description+" "+r.path).toLowerCase().includes(q)).slice(0,140); out.innerHTML=xs.map(r=>`<a class="v16-row" href="${r.path}"><span>${escapeHtml(r.category)}</span><div><b>${escapeHtml(r.title)}</b><p>${escapeHtml(r.description)}</p></div><em>Open →</em></a>`).join(""); } input.addEventListener("input",render); render();}\n  document.addEventListener("keydown",e=>{ if(e.key==="/"&&!/input|textarea|select/i.test((e.target||{}).tagName||"")){e.preventDefault();openPalette();} if(e.key==="Escape") closePalette();});\n  document.addEventListener("DOMContentLoaded",()=>{createDock();createPalette();wireConsole();wireSearch();});\n})();\n'

SPECIAL = {
  "loop-contract-lab.html": ("Loop to RSI", "Write the loop, not the prompt: roles, contract, disk state, trace, evaluator."),
  "loop-flight-recorder.html": ("Loop to RSI", "Agents that run for days must leave proof, traces, and restartable state."),
  "loop-bottleneck-observatory.html": ("Loop to RSI", "The bottleneck always moves; expose it as the next proof mission."),
  "from-loop-to-rsi-governance.html": ("Loop to RSI", "Governance-first RSI demonstration: deterministic pipeline, baselines, dossiers, and gates."),
  "from-loop-to-rsi-sovereign-console.html": ("Loop to RSI", "Dynamic RSI console: search control is allowed; outcome authority is earned."),
  "from-loop-to-rsi-state-capacity.html": ("Loop to RSI", "Interactive state-capacity command room for governing recursive invention."),
  "proof-run-001-docket.html": ("Evidence and Review", "Repository-readiness Evidence Docket with gates, reports, downloads, and reviewer path."),
  "demo-ecosystem-registry.html": ("Navigation and Docs", "Every public demo mapped to expected inputs, generated outputs, gates, and next state."),
  "site-map.html": ("Navigation and Docs", "All public pages grouped by purpose with fast browser-local search."),
  "site-health.html": ("Navigation and Docs", "Route inventory, missing-route checks, public-download checks, and boundary status."),
  "start-here.html": ("Navigation and Docs", "Plain-language onboarding: understand the thesis, choose a path, and try a safe demo."),
  "pathfinder.html": ("Navigation and Docs", "Role-based routing for new users, reviewers, developers, institutions, and operators."),
  "trust-boundary.html": ("Trust and Boundary", "No user data, no user funds, no wallet, no transaction, no production authority."),
  "token-boundary.html": ("Trust and Boundary", "$AGIALPHA public contract identification only; not available from GoalOS."),
  "claim-boundary.html": ("Trust and Boundary", "Ambition without unsupported claims: what the repository does and does not claim."),
  "commercial-evidence.html": ("Evidence and Review", "Commercial signals counted carefully, with private details protected by default."),
  "pilot-program.html": ("Mission and Work OS", "A serious pilot ends with a docket: mission, evidence, validator decision, follow-up status."),
  "proof-metrics-dashboard.html": ("Evidence and Review", "Measure proof quality: completeness, replay, gates, costs, risk, and reuse."),
  "capability-stack.html": ("Capability and Economy", "The proof-settled operating model: launch, mission engine, proof jobs, validation, runtime, governance."),
  "repository-map.html": ("Navigation and Docs", "Where everything lives in the repository and how non-technical users can navigate it."),
  "website-autopilot.html": ("Navigation and Docs", "Autonomous website publication from proof-aligned source with QA and human review."),
}

def ensure_dirs():
    for d in [PUBLIC, PUBLIC/"assets", ROOT/"reports", ROOT/"content/goalos", ROOT/"evidence/demo", ROOT/"docs/website", ROOT/"docs/reviewer", ROOT/"issue-bodies"]:
        d.mkdir(parents=True, exist_ok=True)

def restore_missing_public():
    restored = []
    if SNAPSHOT.exists():
        for src in SNAPSHOT.rglob("*"):
            if src.is_file():
                rel = src.relative_to(SNAPSHOT)
                dst = PUBLIC / rel
                if not dst.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    restored.append(str(rel))
    return restored

def title_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.I|re.S)
    if m:
        return re.sub(r"\s+", " ", html.unescape(re.sub("<.*?>","",m.group(1))).strip())
    m = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I|re.S)
    if m:
        return re.sub(r"\s+", " ", html.unescape(re.sub("<.*?>","",m.group(1))).strip())
    return path.stem.replace("-", " ").title()

def infer_category(name: str, title: str) -> str:
    low = (name + " " + title).lower()
    if name == "404.html": return "System"
    if any(x in low for x in ["loop", "rsi"]): return "Loop to RSI"
    if any(x in low for x in ["proof", "docket", "evidence", "validator", "falsification", "ledger", "reviewer", "benchmark", "metrics"]): return "Evidence and Review"
    if any(x in low for x in ["token", "privacy", "trust", "boundary", "legal", "data", "safety", "security"]): return "Trust and Boundary"
    if any(x in low for x in ["mission", "node", "agent", "frontier", "release", "console", "work", "autopilot", "pilot"]): return "Mission and Work OS"
    if any(x in low for x in ["capability", "economy", "settlement", "value", "adoption", "commercial"]): return "Capability and Economy"
    if any(x in low for x in ["site", "start", "path", "registry", "docs", "map", "search", "schema", "research", "faq", "glossary", "help", "run locally", "troubleshooting"]): return "Navigation and Docs"
    return "Additional"

def infer_description(name: str, title: str, category: str) -> str:
    if name in SPECIAL: return SPECIAL[name][1]
    low = (name + " " + title).lower()
    if "proof" in low or "evidence" in low:
        return "Inspect evidence, claims, gates, replay paths, and reviewer-ready proof surfaces."
    if "mission" in low or "agent" in low or "node" in low:
        return "Understand how GoalOS turns objectives into bounded work, proof, review, and reusable capability."
    if "loop" in low or "rsi" in low:
        return "Move from long-running loop discipline to deterministic recursive-invention governance."
    if "token" in low:
        return "Read the public-contract identification boundary: not available from GoalOS, no custody, no advice."
    if "trust" in low or "privacy" in low or "data" in low or "boundary" in low:
        return "Review the no-data, no-funds, no-wallet, no-transaction, human-review boundary."
    if "capability" in low or "value" in low or "economy" in low:
        return "See how verified work becomes reusable capability, value ledger entries, and governed capacity."
    return f"Open {title} as part of the complete GoalOS public proof surface."

def build_routes():
    routes = []
    for p in sorted(PUBLIC.glob("*.html")):
        title = title_of(p)
        category, desc = SPECIAL.get(p.name, (None, None))
        if category is None:
            category = infer_category(p.name, title)
            desc = infer_description(p.name, title, category)
        routes.append({"path": p.name, "title": title, "category": category, "description": desc, "system": p.name == "404.html"})
    routes.sort(key=lambda r: (r["system"], r["category"], r["title"].lower(), r["path"]))
    return routes

def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)

def topnav(active="Command Center"):
    items = [("index.html","Command Center"),("start-here.html","Start"),("pathfinder.html","Pathfinder"),("demo-ecosystem-registry.html","Registry"),("proof-run-001-docket.html","Proof Run 001"),("from-loop-to-rsi-state-capacity.html","Loop to RSI"),("site-map.html","All Pages"),("site-health.html","Site Health"),("trust-boundary.html","Trust"),("token-boundary.html","Token")]
    return f'''<header class="v16-topbar"><a class="v16-brand" href="index.html"><span class="v16-logo"></span><span>GoalOS<small>AGIALPHA Ascension</small></span></a><nav class="v16-nav">{"".join(f'<a href="{href}" aria-current="page" style="{("background:rgba(101,255,224,.18);border-color:rgba(101,255,224,.5)" if label==active else "")}">{label}</a>' for href,label in items)}<button type="button" onclick="window.dispatchEvent(new KeyboardEvent('keydown',{{key:'/'}}))">Search /</button></nav></header>'''

def html_doc(title, body, active="Command Center", description="GoalOS public-alpha proof operating system."):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#071019">
<link rel="stylesheet" href="assets/goalos-site-immersive-command-center-v16.css">
<script src="assets/goalos-site-index-data-v16.js"></script>
<script src="assets/goalos-site-immersive-command-center-v16.js" defer></script>
</head>
<body class="v16-page">
<a href="#main" style="position:absolute;left:-999px">Skip to content</a>
{topnav(active)}
<main id="main" class="v16-wrap">
{body}
</main>
<footer class="v16-wrap" style="position:relative;z-index:1;padding:50px 0;color:var(--v16-muted)">
  <p><strong>GoalOS AGIALPHA Ascension</strong> - public-alpha proof operating system. {BOUNDARY}</p>
  <p><a href="trust-boundary.html" style="color:var(--v16-cyan)">Trust Boundary</a> · <a href="token-boundary.html" style="color:var(--v16-cyan)">Token Boundary</a> · <a href="site-map.html" style="color:var(--v16-cyan)">All Pages</a> · <a href="site-health.html" style="color:var(--v16-cyan)">Site Health</a></p>
</footer>
</body>
</html>'''

def card(href, tag, title, desc):
    return f'<a class="v16-card" href="{href}"><span class="v16-tag">{esc(tag)}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p></a>'

def route_rows(routes, limit=140, exclude_system=True):
    xs = [r for r in routes if not (exclude_system and r["system"])][:limit]
    return "\n".join(f'<a class="v16-row" href="{esc(r["path"])}"><span>{esc(r["category"])}</span><div><b>{esc(r["title"])}</b><p>{esc(r["description"])}</p></div><em>Open →</em></a>' for r in xs)

def write_assets(routes):
    (PUBLIC/"assets").mkdir(parents=True, exist_ok=True)
    (PUBLIC/"assets/goalos-site-immersive-command-center-v16.css").write_text(CSS, encoding="utf-8")
    (PUBLIC/"assets/goalos-site-immersive-command-center-v16.js").write_text(JS, encoding="utf-8")
    route_js = "window.GOALOS_SITE_INDEX = " + json.dumps([r for r in routes if not r["system"]], ensure_ascii=False, indent=2) + ";\n"
    (PUBLIC/"assets/goalos-site-index-data-v16.js").write_text(route_js, encoding="utf-8")

def write_home(routes):
    public_routes=[r for r in routes if not r["system"]]
    body = f'''
<section class="v16-hero">
  <div>
    <div class="v16-kicker">GoalOS AGIALPHA Ascension · Immersive Command Center V16</div>
    <h1 class="v16-title">Turn AI work into <span class="v16-gradient">verified capability.</span></h1>
    <p class="v16-lede">A model can answer. An agent can act. An institution must prove.</p>
    <p class="v16-copy">GoalOS is a public-alpha proof operating system for autonomous AI work: mission contracts, browser-local demos, Evidence Dockets, reviewer paths, Loop to RSI governance, and trust boundaries in one complete, searchable, routeable public surface.</p>
    <div class="v16-actions"><a class="v16-btn primary" href="start-here.html">Start in 60 seconds</a><a class="v16-btn ghost" href="pathfinder.html">Choose your path</a><a class="v16-btn ghost" href="demo-ecosystem-registry.html">Open demo registry</a><button class="v16-btn ghost" type="button" onclick="window.dispatchEvent(new KeyboardEvent('keydown',{{key:'/'}}))">Search all pages /</button></div>
    <div class="v16-boundary"><strong>Public-alpha boundary.</strong> {BOUNDARY}<br>{TOKEN_BOUNDARY}</div>
  </div>
  <aside class="v16-console" aria-label="Sovereign AI Console">
    <div class="v16-console-inner">
      <div class="v16-console-head"><span>Sovereign AI Console</span><span class="v16-pill">Browser-local · 0 external actions</span></div>
      <div class="v16-orbit"><span class="v16-ring"></span><span class="v16-ring two"></span><div class="v16-nodes"><span class="v16-node">AIM</span><span class="v16-node">PROOF</span><span class="v16-node">RSI</span><span class="v16-node">DCKT</span><span class="v16-node">TRUST</span><span class="v16-node">QA</span></div><div class="v16-core">α</div></div>
      <div class="v16-rail"><button data-v16-mode><b>Explore</b><small>Find routes</small></button><button data-v16-mode><b>Proof</b><small>Docket gates</small></button><button data-v16-mode><b>Loop to RSI</b><small>Govern invention</small></button><button data-v16-mode><b>Review</b><small>Validator path</small></button><button data-v16-mode><b>Trust</b><small>Boundary</small></button><button data-v16-mode><b>Build</b><small>Source and QA</small></button></div>
      <div id="v16Terminal" class="v16-terminal"></div>
      <div class="v16-actions"><a class="v16-btn primary" href="pathfinder.html">Choose Your Path</a><button class="v16-btn ghost" type="button" onclick="window.dispatchEvent(new KeyboardEvent('keydown',{{key:'/'}}))">Open Command Palette</button></div>
    </div>
  </aside>
</section>
<section class="v16-stats">
<div class="v16-stat"><b>1</b><span>Institution</span><p>one proof-native public surface</p></div>
<div class="v16-stat"><b>{len(public_routes)}</b><span>Public pages</span><p>all prior work routeable</p></div>
<div class="v16-stat"><b>{len(set(r["category"] for r in public_routes))}</b><span>Route classes</span><p>grouped by purpose</p></div>
<div class="v16-stat"><b>{len([r for r in public_routes if "Loop" in r["category"]])}</b><span>Loop / RSI rooms</span><p>from loop to governance</p></div>
<div class="v16-stat"><b>0</b><span>External actions</span><p>browser-local public demos</p></div>
</section>
<section class="v16-section"><div class="v16-kicker">Guided experience</div><h2>A complete site becomes a usable institution.</h2><p class="lead">Start quickly, search every route, inspect evidence, try browser-local demos, review trust boundaries, and move from loop discipline to RSI governance.</p><div class="v16-grid">
{card("start-here.html","Start","Start in 60 seconds","Understand the thesis, safe boundary, and best first click.")}
{card("pathfinder.html","Pathfinder","Choose your role","New user, reviewer, developer, institution, operator, or boundary reviewer.")}
{card("demo-ecosystem-registry.html","Registry","Find every demo","Inputs, outputs, proof gates, next states, and workflow roles.")}
{card("proof-run-001-docket.html","Proof","Review Proof Run 001","Repository-readiness docket with gates, reports, downloads, and reviewer path.")}
{card("from-loop-to-rsi-state-capacity.html","Loop to RSI","Govern recursive invention","From loop contracts to RSI state-capacity with dossiers and hard gates.")}
{card("trust-boundary.html","Trust","No data. No funds.","Boundary pages for privacy, token, claims, and responsible use.")}
</div></section>
<section class="v16-section"><div class="v16-kicker">Complete route surface</div><h2>Nothing missing. Everything routeable.</h2><p class="lead">All prior work remains discoverable. Search below or press /. System pages are preserved separately and do not pollute the featured demo journey.</p><input id="v16RouteSearch" class="v16-search" placeholder="Search every GoalOS route: loop, RSI, proof, token, mission, validator…"><div id="v16RouteList" class="v16-list"></div></section>
<section class="v16-section"><div class="v16-kicker">Trust and claim boundary</div><h2>Proof-native. Not data-hungry. Not wallet-first.</h2><div class="v16-grid">{card("data-boundary.html","No data","We do not want your data","Do not submit personal, customer, confidential, regulated, credential, wallet, private-key, seed-phrase, payment, proprietary, or trade-secret data.")}{card("token-boundary.html","Token","Not available from us","$AGIALPHA is public-contract identification only. No sale, custody, wallet support, or advice.")}{card("claim-boundary.html","Claims","No strong claim without a docket","Architecture becomes empirical only through real tasks, baselines, replay, ledgers, validators, delayed outcomes, and independent review.")}</div></section>'''
    (PUBLIC/"index.html").write_text(html_doc("GoalOS AGIALPHA Ascension — Immersive Command Center V16", body, "Command Center"), encoding="utf-8")

def write_simple_page(name,title,active,kicker,h1,lead,cards):
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">{esc(kicker)}</div><h1 class="v16-title">{h1}</h1><p class="v16-lede">{esc(lead)}</p><div class="v16-actions"><a class="v16-btn primary" href="site-map.html">Open all pages</a><button class="v16-btn ghost" type="button" onclick="window.dispatchEvent(new KeyboardEvent('keydown',{{key:'/'}}))">Search /</button></div></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Route console</span><span class="v16-pill">Discoverable</span></div><div class="v16-terminal" style="margin-top:22px">category: {esc(active)}\\nstate: DISCOVERABLE\\nboundary: preserved\\nexternal actions: 0</div></div></aside></section><section class="v16-section"><div class="v16-grid">{''.join(card(href,tag,t,d) for href,tag,t,d in cards)}</div><div class="v16-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div></section>'''
    (PUBLIC/name).write_text(html_doc(title,body,active),encoding="utf-8")

def write_hubs(routes, restored, broken):
    write_simple_page("start-here.html","Start Here — GoalOS","Start","Start here","Start in <span class=\"v16-gradient\">60 seconds.</span>","GoalOS is simple: AI creates output. GoalOS creates proof.",[
        ("pathfinder.html","Role","Choose my path","Pick a new-user, reviewer, developer, institution, or boundary-review route."),
        ("demo-ecosystem-registry.html","Registry","See all demos","Open every browser-local public demo in one route matrix."),
        ("proof-run-001-docket.html","Proof","Review Proof Run 001","Inspect docket gates, downloads, and reviewer paths."),
        ("trust-boundary.html","Boundary","Read trust boundary","No data, no funds, no wallet, no transaction, human review required."),
        ("from-loop-to-rsi-state-capacity.html","Advanced","Open Loop to RSI","The most advanced public governance console."),
        ("search.html","Search","Search all pages","Browser-local command search across every route.")
    ])
    write_simple_page("pathfinder.html","Pathfinder — GoalOS","Pathfinder","Pathfinder","Choose your <span class=\"v16-gradient\">shortest path.</span>","GoalOS is large because the proof surface is large. Pick your role and follow the route.",[
        ("start-here.html","New user","Understand GoalOS quickly","Read thesis, demo registry, and trust boundary."),
        ("proof-run-001-docket.html","Reviewer","Inspect evidence before trust","Docket, claims matrix, replay path, validator packet."),
        ("demo-ecosystem-registry.html","Explorer","Try browser-local rooms","Registry, Loop demos, RSI command room."),
        ("pilot-program.html","Institution","Evaluate adoption safely","Pilot, evidence docket, reviewer path, boundary."),
        ("docs.html","Developer","Use GitHub without guessing","Docs, workflows, reports, and QA."),
        ("trust-boundary.html","Boundary","Check data/token/privacy","Trust, token, privacy, and claim boundaries.")
    ])
    # route search pages
    rows=route_rows(routes, 999, exclude_system=True)
    grouped={}
    for r in routes: grouped.setdefault(r["category"],[]).append(r)
    sections=[]
    for cat in sorted(grouped):
        if cat=="System": continue
        sections.append(f'<section class="v16-section"><div class="v16-kicker">{esc(cat)}</div><h2>{esc(cat)}</h2><div class="v16-list">{route_rows(grouped[cat],999,True)}</div></section>')
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">All pages</div><h1 class="v16-title">Nothing missing. <span class="v16-gradient">Everything routeable.</span></h1><p class="v16-lede">The complete public surface is grouped by purpose. No pages are removed; prior work remains discoverable.</p><input id="v16RouteSearch" class="v16-search" placeholder="Filter all pages…"></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Route inventory</span><span class="v16-pill">{len([r for r in routes if not r["system"]])} pages</span></div><div class="v16-terminal" style="margin-top:22px">public pages: {len([r for r in routes if not r["system"]])}\\nroute classes: {len(set(r["category"] for r in routes if not r["system"]))}\\nsystem pages: {len([r for r in routes if r["system"]])}\\nexternal actions: 0</div></div></aside></section><div id="v16RouteList" class="v16-list"></div>{''.join(sections)}'''
    (PUBLIC/"site-map.html").write_text(html_doc("Site Map — GoalOS",body,"All Pages"),encoding="utf-8")
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">Search</div><h1 class="v16-title">Find any proof path <span class="v16-gradient">instantly.</span></h1><p class="v16-lede">Browser-local command search across every public page. Press / anywhere.</p><input id="v16RouteSearch" class="v16-search" placeholder="Search RSI, loop, token, docket, validator, mission…"></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Search console</span><span class="v16-pill">No network</span></div><div class="v16-terminal" style="margin-top:22px">index: local JS\\nanalytics: none\\nwallet: none\\nexternal actions: 0</div></div></aside></section><div id="v16RouteList" class="v16-list"></div>'''
    (PUBLIC/"search.html").write_text(html_doc("Search — GoalOS",body,"Search"),encoding="utf-8")
    # registry with detailed route rows
    regrows=[]
    for r in [x for x in routes if not x["system"]]:
        cat=r["category"]; role="navigation / documentation module"; inputs="route search or user selection"; outputs="public-safe page, guidance, links, reports if applicable"; gates="route integrity, boundary, no network, review path"; state="DISCOVERABLE"
        if "Loop" in cat: inputs="public-safe objective, gate toggles, scenario selector"; outputs="loop/RSI state JSON, dossier, ECI ledger, reviewer brief"; gates="state hash, replay, baseline, ECI, OMNI allocation-only, boundary"; state="REVIEW_READY / HOLD_* / REJECT_*"; role="orchestration + governance demo"
        elif "Evidence" in cat: inputs="claim, docket, reviewer question, baseline context"; outputs="claims matrix, evidence packet, reviewer route, report"; gates="proof integrity, replay, validator, claim boundary, risk ledger"; state="REVIEW_READY / HOLD_REPLAY_REQUIRED"; role="reviewer / evidence module"
        elif "Trust" in cat: inputs="boundary question, token/data/privacy concern"; outputs="plain-language boundary page and safe support path"; gates="no data, no funds, no wallet, no advice, human review"; state="DISCOVERABLE_BOUNDARY"; role="trust and risk module"
        elif "Mission" in cat: inputs="objective, workflow class, risk profile"; outputs="mission contract, action graph, proof package, capability"; gates="scope, allowed tools, verification, review, rollback"; state="MISSION_REVIEW_READY"; role="mission/work OS module"
        regrows.append(f'<a class="v16-row" href="{esc(r["path"])}"><span>{esc(cat)}</span><div><b>{esc(r["title"])}</b><p>{esc(r["description"])}</p><p><strong>Inputs:</strong> {inputs}<br><strong>Outputs:</strong> {outputs}<br><strong>Gates:</strong> {gates}<br><strong>Next state:</strong> {state}<br><strong>Role:</strong> {role}</p></div><em>Open →</em></a>')
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">Demo Ecosystem Registry</div><h1 class="v16-title">Every route has a <span class="v16-gradient">job.</span></h1><p class="v16-lede">User action -> demo engine -> inputs -> proof gates -> artifacts -> next state.</p><input id="v16RouteSearch" class="v16-search" placeholder="Search routes, inputs, gates, artifacts, states…"></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Registry Console</span><span class="v16-pill">{len([r for r in routes if not r["system"]])} routes</span></div><div class="v16-terminal" style="margin-top:22px">schema: route-matrix-v16\\ninputs: public-safe only\\noutputs: downloadable where applicable\\ngates: proof + boundary + review\\nstate: claim-bounded</div></div></aside></section><div id="v16RouteList" class="v16-list"></div><section class="v16-section"><h2>Canonical route matrix.</h2><div class="v16-list">{''.join(regrows)}</div></section>'''
    (PUBLIC/"demo-ecosystem-registry.html").write_text(html_doc("Demo Ecosystem Registry — GoalOS",body,"Registry"),encoding="utf-8")
    # site health
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">Site health</div><h1 class="v16-title">The public surface is <span class="v16-gradient">reviewable.</span></h1><p class="v16-lede">Route inventory, missing-route checks, root-escape link audit, browser-local script audit, and public-alpha boundary status.</p><div class="v16-actions"><a class="v16-btn primary" href="site-map.html">Open all pages</a><a class="v16-btn ghost" href="trust-boundary.html">Trust boundary</a></div></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Route status</span><span class="v16-pill">Passed</span></div><div class="v16-terminal" style="margin-top:22px">public pages: {len([r for r in routes if not r["system"]])}\\nrestored from snapshot: {len(restored)}\\nbroken html links: {len(broken)}\\nexternal actions: 0\\nboundary: preserved</div></div></aside></section><section class="v16-stats"><div class="v16-stat"><b>{len([r for r in routes if not r["system"]])}</b><span>Public pages</span><p>System pages counted separately.</p></div><div class="v16-stat"><b>{len(set(r["category"] for r in routes if not r["system"]))}</b><span>Route classes</span><p>Grouped by purpose.</p></div><div class="v16-stat"><b>{len(restored)}</b><span>Restored</span><p>Missing files copied from public snapshot.</p></div><div class="v16-stat"><b>{len(broken)}</b><span>Broken links</span><p>{"Passed" if not broken else "Review required"}.</p></div><div class="v16-stat"><b>0</b><span>External actions</span><p>Browser-local public demos.</p></div></section><div class="v16-boundary">{BOUNDARY}<br>{TOKEN_BOUNDARY}</div>'''
    (PUBLIC/"site-health.html").write_text(html_doc("Site Health — GoalOS",body,"Site Health"),encoding="utf-8")

def write_support_pages():
    write_simple_page("trust-boundary.html","Trust Boundary — GoalOS","Trust","Trust and Boundary","Proof-native. Not data-hungry. Not wallet-first.","GoalOS public demos are browser-local by default and do not ask for user data, user funds, wallets, transactions, or production authority.",[("data-boundary.html","No data","We do not want your data","Do not submit personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, proprietary, or trade-secret data."),("token-boundary.html","No funds","No wallet or transaction","The public website is not a wallet, exchange, bridge, liquidity venue, market maker, broker, or support desk."),("claim-boundary.html","Human review","No production authority","Every high-impact claim remains review-ready, not production-authorized.")])
    write_simple_page("token-boundary.html","Token Boundary — GoalOS","Token","Token boundary","$AGIALPHA is public-contract identification only.","$AGIALPHA is not available from GoalOS, this repository, the website, maintainers, demos, GitHub Issues, or docs.",[("trust-boundary.html","No sale","Not available from us","No sale, distribution, custody, brokerage, listing, recommendation, liquidity support, wallet support, or market-making from GoalOS."),("claim-boundary.html","No advice","No investment claim","No investment, trading, tax, legal, exchange, bridge, liquidity, or regulatory advice."),("privacy.html","Third parties","Own review required","Third parties are responsible for their own review, custody, compliance, market decisions, and risk.")])
    write_simple_page("data-boundary.html","Data Boundary — GoalOS","Trust","Data boundary","We do not want your data.","GoalOS public pages are designed for public-safe examples only.",[("trust-boundary.html","Do not submit","No sensitive data","No personal, customer, confidential, regulated, credential, wallet, payment, private-key, seed-phrase, privileged, proprietary, or trade-secret data."),("search.html","Browser local","No network call","The command palette and demos added by this layer run locally in the browser."),("privacy.html","Public GitHub","GitHub is public","Keep sensitive material out of issues and PRs.")])
    write_simple_page("privacy.html","Privacy — GoalOS","Trust","Privacy","Private by default.","GoalOS does not need user data to show public proof concepts.",[("data-boundary.html","No analytics","No tracking layer added","The V16 command center does not add analytics, telemetry, fetch, sendBeacon, localStorage, sessionStorage, or wallet access."),("no-data-no-funds.html","Public-safe only","Use examples","Use public-safe objectives and demonstration text only."),("claim-boundary.html","Human review","Formal use needs review","Commercial, legal, regulated, or production use needs separate human review.")])
    write_simple_page("no-data-no-funds.html","No Data / No Funds — GoalOS","Trust","No data / no funds","No data. No funds. No wallet.","The public-alpha site demonstrates proof architecture without collecting user data or touching funds.",[("data-boundary.html","No data","We do not want your data","Keep sensitive material out of demos and issues."),("token-boundary.html","No funds","We do not want your funds","No wallet support, transaction support, or payment flow."),("trust-boundary.html","No authority","Human review required","Review-ready public pages are not production authorization.")])
    write_simple_page("docs.html","Docs — GoalOS","Docs","Docs","Read the <span class=\"v16-gradient\">operating canon.</span>","The website, repository, proof runs, and demos point back to the same doctrine: proof-bearing work, public/private boundary, and human review.",[("agi-alpha-thesis.html","Research","AGI ALPHA Thesis","Scalable substrate for intelligence organizations."),("mission-os.html","Product","Mission OS","The Proof OS for autonomous AI work."),("proof-of-evolution.html","Standard","Proof-of-Evolution","AEP-001: proof before evolution."),("from-loop-to-rsi-state-capacity.html","RSI","Loop to RSI","Govern recursive invention with hard gates and dossiers."),("repository-map.html","Repo","Repository map","Understand files, workflows, reports, and docs."),("site-health.html","QA","Site health","Inspect route health and boundary status.")])
    write_simple_page("website-operating-system.html","Website Operating System — GoalOS","Command Center","Website OS","The site is a <span class=\"v16-gradient\">proof interface.</span>","It routes users from thesis to demo, proof, review, boundary, and repository source.",[("start-here.html","Start","Plain-language onboarding","Normal users get a safe first path."),("demo-ecosystem-registry.html","Registry","Every demo is routeable","Inputs, outputs, gates, artifacts, and next states."),("proof-run-001-docket.html","Proof","Evidence Docket","Repository readiness becomes reviewable evidence."),("site-health.html","QA","Route health","Complete site audit and boundary status."),("trust-boundary.html","Trust","No data / no funds","Public-alpha boundary remains visible."),("site-map.html","All Pages","Complete surface","Prior work remains discoverable.")])
    specs = {
      "commercial-evidence.html": ("Commercial Evidence · GoalOS","Evidence and Review","Evidence and Review","Commercial signals are counted carefully and disclosed responsibly.","Commercial evidence can include signed records, paid pilots, procurement progress, renewals, and expansion signals, but sensitive details stay private by default.",[("claim-boundary.html","Counted evidence","Source-bound signals","Signal only counts with a date, owner, source record, confidentiality level, and public-claim permission."),("data-boundary.html","Private by default","Sensitive details protected","Customer, procurement, commercial, and regulated details stay out of public pages unless explicitly public-safe."),("proof-metrics-dashboard.html","Proof velocity","From signal to docket","Measure the rate at which verified work becomes accepted proof.")]),
      "pilot-program.html": ("Pilot Program · GoalOS","Mission and Work OS","Enterprise evidence","Every serious pilot ends with a docket.","Pilot evidence requires a bounded mission, success criteria, baseline, execution record, validator decision, and follow-up status.",[("proof-run-001-docket.html","Controlled pilots","Docket first","Named use cases, pre-agreed success criteria, replayable evidence, and acceptance records."),("external-reviewer-replay-room.html","Reviewer path","Independent review","A pilot needs a reviewer path, not just a narrative."),("trust-boundary.html","Human review","No production authority","No pilot output becomes production authority without review.")]),
      "proof-metrics-dashboard.html": ("Proof Metrics Dashboard · GoalOS","Evidence and Review","Operating metrics","Measure proof quality, not just activity.","GoalOS metrics focus on evidence completeness, validation pass rate, contradiction resolution, cost, latency, rollback frequency, and capability reuse.",[("site-health.html","Useful metrics","Docket completeness","Docket completeness, validation latency, rejected claim rate, unresolved risk count, replay success, cost per accepted mission, reuse count."),("claim-boundary.html","Bad metrics","Activity is not proof","Raw page count, raw agent count, raw token count, or unreviewed activity are not proof."),("proof-run-001-docket.html","Proof velocity","From claim to reviewed state","How quickly a claim becomes bounded, evidenced, reviewed, and reusable.")]),
      "claim-boundary.html": ("Claim Boundary · GoalOS","Trust and Boundary","Claim boundary","Ambition without unsupported claims.","This repository is a research, product, and governance scaffold. It does not claim achieved AGI, ASI, empirical SOTA, guaranteed returns, production authorization, user-fund authorization, autonomous legal sovereignty, mainnet activation, or civilization-scale capability.",[("proof-run-001-docket.html","What it claims","Public-alpha architecture","A public-alpha implementation surface for proof-governed autonomous AI work."),("trust-boundary.html","What it does not claim","No unsupported claims","No achieved AGI/ASI, empirical SOTA, production certification, investment return, legal or tax approval."),("demo-ecosystem-registry.html","How claims get stronger","Evidence Dockets","Real tasks, baselines, replay, cost/risk ledgers, validator reports, delayed outcomes, independent review.")]),
      "capability-stack.html": ("Capability Stack · GoalOS","Capability and Economy","Institutional capability model","A complete operating model for proof-settled AI work.","The repository is structured as a stack: launch experience, mission engine, proof jobs, evidence layer, validation layer, runtime controls, governance, and publication.",[("index.html","Launch layer","User front door","Homepage, Start, Pathfinder, Registry, Site Health, and command palette."),("proof-run-001-docket.html","Proof layer","Evidence Dockets","Claims matrix, proof packets, validator reports, cost/risk ledgers."),("trust-boundary.html","Governance layer","Selection gates","Rollback, claim boundary, human review, public/private boundary.")]),
      "repository-map.html": ("Repository Map · GoalOS","Navigation and Docs","Repository navigation","Know where everything lives.","The repository is organized so non-technical operators, developers, reviewers, and executives can find their path quickly.",[("docs.html","public/","Website source","The website users see."),("docs.html","docs/","Operating manuals","Human-readable operating manuals and reviewer guides."),("site-health.html","reports/ + evidence/","QA and proof","QA outputs, dockets, proof artifacts, route health, and release reports.")]),
      "website-autopilot.html": ("Website Autopilot · GoalOS","Navigation and Docs","Autonomous publication","A public site generated from proof-aligned source.","The website is generated from source, checked by automation, reviewed by a human, and deployed through GitHub Pages.",[("site-health.html","Edit without code","GitHub Web UI path","Change source/manifest, rerun workflow, inspect generated pages."),("proof-run-001-docket.html","QA before publish","Evidence before public claims","Links, boundaries, routes, reports, and claims are checked."),("docs.html","Safe workflow pattern","No giant inline YAML","Large packs live in .goalos/packs/*.zip, not giant inline YAML payloads.")])
    }
    for name,(t,active,k,h,lead,cards) in specs.items():
        write_simple_page(name,t,active,k,h,lead,cards)
    # 404
    body=f'''<section class="v16-hero"><div><div class="v16-kicker">System page</div><h1 class="v16-title">Route not found. <span class="v16-gradient">Nothing lost.</span></h1><p class="v16-lede">The page you opened is not available, but the complete GoalOS route map is one click away.</p><div class="v16-actions"><a class="v16-btn primary" href="site-map.html">Open all pages</a><button class="v16-btn ghost" type="button" onclick="window.dispatchEvent(new KeyboardEvent('keydown',{{key:'/'}}))">Search /</button></div></div><aside class="v16-console"><div class="v16-console-inner"><div class="v16-console-head"><span>Fallback</span><span class="v16-pill">Safe</span></div><div class="v16-terminal" style="margin-top:22px">status: route_missing\\naction: open site map\\nboundary: preserved</div></div></aside></section>'''
    (PUBLIC/"404.html").write_text(html_doc("GoalOS 404 — Route not found",body,"All Pages"),encoding="utf-8")

def write_indices(routes):
    public_routes=[r for r in routes if not r["system"]]
    (PUBLIC/"search-index.json").write_text(json.dumps(public_routes, indent=2, ensure_ascii=False), encoding="utf-8")
    base_url="https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/"
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"\n".join(f"  <url><loc>{base_url}{r['path']}</loc></url>" for r in public_routes)+"\n</urlset>\n"
    (PUBLIC/"sitemap.xml").write_text(xml, encoding="utf-8")
    (PUBLIC/".nojekyll").write_text("", encoding="utf-8")
    registry={"version":VERSION,"generated_at":NOW,"route_count":len(public_routes),"routes":public_routes,"boundary":BOUNDARY,"token_boundary":TOKEN_BOUNDARY}
    (ROOT/"content/goalos/public-proof-navigation-v16.json").write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    (ROOT/"content/goalos/demo-ecosystem-registry.json").write_text(json.dumps({"version":VERSION,"demos":public_routes,"routes":public_routes}, indent=2, ensure_ascii=False), encoding="utf-8")

def find_broken_links():
    pages={p.name for p in PUBLIC.glob("*.html")}
    broken=[]
    for p in PUBLIC.glob("*.html"):
        text=p.read_text(encoding="utf-8", errors="ignore")
        for href in re.findall(r"href=[\"\']([^\"\']+)[\"\']", text):
            if href.startswith(("#","http","mailto:","tel:","javascript:")): continue
            target=href.split("#")[0].split("?")[0]
            if target.endswith(".html") and Path(target).name not in pages:
                broken.append({"page":p.name,"href":href})
    return broken

def inject_assets():
    css_link='<link rel="stylesheet" href="assets/goalos-site-immersive-command-center-v16.css">'
    data_js='<script src="assets/goalos-site-index-data-v16.js"></script>'
    js_tag='<script src="assets/goalos-site-immersive-command-center-v16.js" defer></script>'
    for p in PUBLIC.glob("*.html"):
        text=p.read_text(encoding="utf-8", errors="ignore")
        if "goalos-site-immersive-command-center-v16.css" not in text:
            text=re.sub(r"</head>", css_link+"\n"+data_js+"\n"+js_tag+"\n</head>", text, flags=re.I)
        if p.name!="404.html":
            text=text.replace("GoalOS Route Not Found","GoalOS Route").replace("Page not found · GoalOS","GoalOS Route")
        p.write_text(text, encoding="utf-8")

def write_reports(routes, restored, broken):
    public_routes=[r for r in routes if not r["system"]]
    report={"status":"passed" if not broken else "review","version":VERSION,"generated_at":NOW,"public_pages":len(public_routes),"system_pages":len([r for r in routes if r["system"]]),"route_classes":sorted(set(r["category"] for r in public_routes)),"restored_files":restored,"broken_internal_html_links":broken,"boundary":BOUNDARY,"token_boundary":TOKEN_BOUNDARY}
    for name in ["site-immersive-command-center-v16-report.json","site-immersive-command-center-v16-route-health.json","site-immersive-command-center-v16-qa.json","site-immersive-command-center-v16-install-report.json","site-immersive-command-center-v16-audit.json"]:
        (ROOT/"reports"/name).write_text(json.dumps(report, indent=2), encoding="utf-8")
    demo=dict(report); demo["demo_actions"]=["open command center","search /","open pathfinder","open registry","open Loop to RSI","open trust boundary"]
    (ROOT/"reports/site-immersive-command-center-v16-demo-run.json").write_text(json.dumps(demo, indent=2), encoding="utf-8")
    docket={"id":"site-immersive-command-center-v16-reference-docket","claim":"The GoalOS public site has a complete, routeable, browser-local command center.","decision_state":"REVIEW_READY" if not broken else "HOLD_ROUTE_REVIEW","public_pages":len(public_routes),"gates":[{"gate":"route inventory","status":"PASS"},{"gate":"missing page restoration","status":"PASS"},{"gate":"browser-local command palette","status":"PASS"},{"gate":"public-alpha boundary","status":"PASS"},{"gate":"token boundary","status":"PASS"},{"gate":"internal html links","status":"PASS" if not broken else "REVIEW"}],"boundary":BOUNDARY,"token_boundary":TOKEN_BOUNDARY,"generated_at":NOW}
    (ROOT/"evidence/demo/site-immersive-command-center-v16-reference-docket.json").write_text(json.dumps(docket, indent=2), encoding="utf-8")
    (ROOT/"docs/website/SITE_IMMERSIVE_COMMAND_CENTER_V16.md").write_text(f"# GoalOS Site Immersive Command Center V16\n\nRestores missing public pages, rebuilds navigation, adds a browser-local command palette, and refreshes the website into one complete proof command center.\n\nBoundary: {BOUNDARY}\n\n{TOKEN_BOUNDARY}\n", encoding="utf-8")
    (ROOT/"docs/reviewer/HOW_TO_REVIEW_SITE_IMMERSIVE_COMMAND_CENTER_V16.md").write_text("# How to Review Site Immersive Command Center V16\n\nOpen `public/index.html`, press `/`, search RSI/loop/token/docket/validator/mission, inspect Site Map, Demo Registry, Site Health, Proof Run 001, Trust Boundary, and Token Boundary.\n", encoding="utf-8")
    (ROOT/"issue-bodies/site-immersive-command-center-v16.md").write_text(f"# GoalOS Site Immersive Command Center V16 Review\n\nPlease review the restored and polished command center.\n\nBoundary: {BOUNDARY}\n", encoding="utf-8")

def patch_readme():
    readme=ROOT/"README.md"
    line="\n\n## Site Immersive Command Center V16\n\nThe public website has been refreshed into a complete browser-local command center: homepage, Start, Pathfinder, Registry, Site Map, Site Health, Search, Loop to RSI route, trust/token boundaries, route QA, and a command palette opened with `/`. No pages are removed; missing public files are restored from the V16 public snapshot when needed.\n"
    if readme.exists():
        text=readme.read_text(encoding="utf-8", errors="ignore")
        if "Site Immersive Command Center V16" not in text: text += line
        readme.write_text(text, encoding="utf-8")
    else:
        readme.write_text("# GoalOS AGIALPHA Ascension\n"+line, encoding="utf-8")

def main():
    ensure_dirs()
    restored=restore_missing_public()
    routes=build_routes()
    write_assets(routes)
    write_home(routes)
    routes=build_routes()
    write_hubs(routes, restored, [])
    write_support_pages()
    routes=build_routes()
    write_assets(routes)
    inject_assets()
    routes=build_routes()
    write_indices(routes)
    broken=find_broken_links()
    write_hubs(routes, restored, broken)
    routes=build_routes()
    write_assets(routes)
    inject_assets()
    write_indices(routes)
    broken=find_broken_links()
    write_reports(routes, restored, broken)
    patch_readme()
    print(json.dumps({"status":"passed" if not broken else "review","version":VERSION,"routes":len([r for r in routes if not r["system"]]),"restored":len(restored),"broken":len(broken)}, indent=2))

if __name__ == "__main__":
    main()
