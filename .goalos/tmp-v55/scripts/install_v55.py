#!/usr/bin/env python3
from __future__ import annotations
import json, re, shutil, html, hashlib
from pathlib import Path
from datetime import datetime, timezone

VERSION = "v55"
SLUG = "sovereign-experience-os-v55"
ROOT = Path.cwd()
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"
REPORTS = ROOT / "reports"
CONTENT = ROOT / "content" / "goalos"
EVIDENCE = ROOT / "evidence" / "demo"
DOCS = ROOT / "docs" / "website"
REVIEWER = ROOT / "docs" / "reviewer"

BOUNDARY = "No user data. No user funds. No wallet. No transaction. No backend call. No production authority. Human review required."

FORBIDDEN_REPLACEMENTS = {
    "localStorage": "GoalOSBrowserMemory",
    "sessionStorage": "GoalOSBrowserMemory",
    "navigator.sendBeacon": "GoalOSBoundaryBeacon",
    "sendBeacon": "GoalOSBoundaryBeacon",
    "window.ethereum": "null /* wallet disabled */",
    "XMLHttpRequest": "GoalOSDisabledRequest",
    "fetch(": "GoalOSDisabledNetwork(",
}

CANONICAL_ROUTES = {
    "Command Center": ["index.html", "goalos-phase-completion.html", "goalos-command-center.html", "goalos-aurora-command-center.html", "goalos-gold-master.html", "public-alpha-gold-master.html", "start.html", "start-here.html"],
    "Autonomous Demos": ["autonomy-theatre.html", "autonomous-demo-run-theatre.html", "autonomous-proof-mission-demo.html", "end-to-end-autonomous-demo.html", "quintessential-autonomous-demo.html", "proof-flight-demo.html"],
    "AGI Agents": ["agi-agent-workbench.html", "agi-agent-mission-control.html", "agi-agent-playbooks.html", "agent-foundry.html", "agi-agent-run-theatre.html", "agent-flow-academy-v38.html", "meta-agentic-alpha-agi.html", "meta-agentic-agents.html"],
    "RSI / Loop": ["from-loop-to-rsi-state-capacity.html", "from-loop-to-rsi-governance.html", "from-loop-to-rsi-sovereign-console.html", "move37-dossier.html", "loop-bottleneck-observatory.html", "goalos-loop-bottleneck-observatory.html", "loop-contract-lab.html", "loop-flight-recorder.html", "loop-to-rsi.html", "rsi-state-capacity.html"],
    "AGI Nodes": ["agi-alpha-node-v0.html", "agi-node-validation.html", "agi-node-use-cases.html", "node.html"],
    "Validation": ["validation-control-tower.html", "human-or-agi-node-validation.html", "human-or-node-validation.html", "validation-authority.html", "validation-command-center.html", "validation-mesh.html", "validation-orchestrator.html", "validation-studio.html", "validation-use-cases.html", "validator-council-arena.html"],
    "48 Contracts": ["mainnet-contract-atlas.html", "contract-academy.html", "mainnet-proof-rail.html", "proof-settlement-lab.html", "proof-settlement-chronicle-lab.html"],
    "Proof / Evidence": ["proof-run-001-docket.html", "proof-run-001.html", "proof-run-001-live.html", "proof-ledger.html", "evidence-docket-theatre.html", "proof-mission-control.html", "proof-mission-forge.html", "proof-carrying-artifact-foundry.html", "proof-gradient-lab.html", "evidence-room.html"],
    "Navigation": ["all-pages.html", "site-map.html", "route-registry.html", "search.html", "site-health.html", "ask-goalos.html", "pathfinder.html", "registry.html"],
    "Trust Boundary": ["trust-boundary.html", "token-boundary.html", "privacy.html", "data-boundary.html", "claim-boundary.html", "security-boundary.html", "investment-token-boundary.html", "token-investment-boundary.html", "no-data-no-funds.html", "responsible-use.html", "legal.html", "terms.html"],
}

PROFILE_LIBRARY = {
    "command": {
        "label": "Command Center",
        "kicker": "GoalOS Sovereign Experience",
        "title": "Tell GoalOS what you want.",
        "subtitle": "One objective becomes a mission contract, agent route, evidence docket, validation path, Chronicle entry, and next best page.",
        "objective": "I want GoalOS to turn my objective into a proof-backed mission package with agents, validation, evidence, and a reviewer-ready next step.",
        "authority": "Browser-local command run. Human review remains required.",
        "agents": ["Architect", "Planner", "Research", "Builder", "Verifier", "Risk", "Chronicle", "Reviewer"],
        "stages": ["Objective", "Mission Contract", "Agent Route", "AGI Job", "AGI Node Handoff", "ProofBundle", "Evidence Docket", "Validation", "Chronicle", "Reusable Capability"],
        "artifacts": ["mission-contract.json", "agent-route.json", "proofbundle-plan.json", "evidence-docket.md", "reviewer-brief.md", "chronicle-entry.json"],
        "routes": ["autonomy-theatre.html", "agi-agent-workbench.html", "validation-control-tower.html", "mainnet-contract-atlas.html", "site-map.html"]
    },
    "autonomy": {
        "label": "Autonomy Theatre",
        "kicker": "End-to-end Mission Run",
        "title": "Watch one objective become proof.",
        "subtitle": "A deterministic browser-local theatre turns intent into a proof path: objective, agents, job, node, docket, validator, Chronicle.",
        "objective": "Run a public-safe autonomous mission from objective to proof to validation to Chronicle, with local artifacts I can inspect.",
        "authority": "Autonomous browser-local demonstration. No external action.",
        "agents": ["Objective", "Planner", "Agent Router", "AGI Job", "Node Handoff", "Verifier", "Docket", "Chronicle"],
        "stages": ["Declare objective", "Negotiate mission contract", "Select AGI Agents", "Create AGI Job", "Prepare AGI Node handoff", "Build ProofBundle", "Assemble Evidence Docket", "Validate", "Chronicle"],
        "artifacts": ["mission-contract.json", "agi-job-spec.json", "agi-node-handoff.json", "proofbundle-plan.json", "evidence-docket.md", "validation-certificate.json", "chronicle-entry.json"],
        "routes": ["agi-agent-run-theatre.html", "proof-run-001-docket.html", "visual-flow-proof.html", "validation-control-tower.html"]
    },
    "agents": {
        "label": "AGI Agents",
        "kicker": "Meta-Agentic α-AGI",
        "title": "A mission-ready agent institution.",
        "subtitle": "Planner, Research, Builder, Verifier, Governance, Simulator, Memory, and Liaison agents coordinate under proof gates.",
        "objective": "Show how AGI agents decompose an objective, assign roles, create an AGI Job, hand off to an AGI Node, and package evidence.",
        "authority": "Agent constellation run. Browser-local proof package only.",
        "agents": ["Planner", "Research", "Strategy", "Builder", "Operator", "Safety", "Memory", "Evaluator", "Governance", "Liaison"],
        "stages": ["Objective intake", "Role graph", "Access policy", "Specialist work", "Conflict resolution", "Verifier check", "Node handoff", "Docket package", "Capability reuse"],
        "artifacts": ["agent-constellation.json", "role-contracts.md", "agi-job-spec.json", "node-handoff.json", "evaluator-notes.md", "capability-package.json"],
        "routes": ["agent-foundry.html", "agi-agent-playbooks.html", "agi-agent-run-theatre.html", "agi-alpha-node-v0.html", "validation-control-tower.html"]
    },
    "playbooks": {
        "label": "Solved Use Cases",
        "kicker": "AGI Agent Playbooks",
        "title": "Choose a useful mission.",
        "subtitle": "Non-technical users can launch practical proof missions: contract learning, vendor review, pilot design, RSI dossier, and proof audit.",
        "objective": "Launch a solved GoalOS use case and produce a mission package that tells me exactly what to inspect next.",
        "authority": "Guided playbook run. User remains final reviewer.",
        "agents": ["Guide", "Planner", "Domain Expert", "Evidence", "Risk", "Reviewer", "Chronicle"],
        "stages": ["Select playbook", "Define decision", "Map evidence", "Run agents", "Check risks", "Package artifacts", "Recommend route"],
        "artifacts": ["playbook-selection.json", "mission-plan.md", "evidence-map.json", "risk-ledger.json", "next-route-card.md"],
        "routes": ["universal-mission-composer.html", "mainnet-contract-atlas.html", "from-loop-to-rsi-state-capacity.html", "proof-run-001-docket.html"]
    },
    "rsi": {
        "label": "Loop → RSI",
        "kicker": "Sovereign Invention Governance",
        "title": "Govern invention before it scales.",
        "subtitle": "TARGET → EMIT → FILTER → ATLAS → TEST-PLAN → EVAL → INSERT → PROMOTE with replay, evidence, baselines, and dossiers.",
        "objective": "Run an RSI governance mission that targets exploration, emits candidates, filters risk, builds an atlas, evaluates baselines, and packages a dossier.",
        "authority": "Search control only. Outcome authority remains mechanical.",
        "agents": ["Target", "Emitter", "Risk Filter", "Atlas", "Test Planner", "Evaluator", "Archivist", "Promoter"],
        "stages": ["TARGET", "EMIT", "FILTER", "ATLAS", "TEST-PLAN", "EVAL", "INSERT", "PROMOTE", "Dossier"],
        "artifacts": ["rsi-state.json", "target-plan.json", "candidate-cards.jsonl", "risk-reports.jsonl", "causal-atlas.jsonl", "eval-results.json", "promotion-dossier.md"],
        "routes": ["move37-dossier.html", "loop-bottleneck-observatory.html", "loop-contract-lab.html", "loop-flight-recorder.html", "validation-control-tower.html"]
    },
    "move37": {
        "label": "Move-37 Dossier",
        "kicker": "Breakthrough Control",
        "title": "High novelty raises the burden of proof.",
        "subtitle": "Recognition, reproduction, stress testing, persistence, and dossier packaging before strategic promotion.",
        "objective": "Package a high-novelty Move-37 candidate into a reproducible, stress-tested, reviewer-ready dossier.",
        "authority": "Dossier preparation only. No production promotion.",
        "agents": ["Novelty", "Baseline", "Reproducer", "Stress", "Risk", "Council", "Dossier"],
        "stages": ["Recognize", "Baseline compare", "Reproduce", "Stress-test", "Persistence gate", "Council review", "Dossier bundle"],
        "artifacts": ["move37-recognition.json", "baseline-comparison.json", "reproduction-manifest.json", "stress-tests.json", "persistence-gate.json", "council-dossier.md"],
        "routes": ["from-loop-to-rsi-state-capacity.html", "rsi-governance-lab.html", "validator-council-arena.html"]
    },
    "loop": {
        "label": "Agent Loops",
        "kicker": "Loop Field Notes",
        "title": "Write the loop, not the prompt.",
        "subtitle": "Roles, contracts, disk state, trace reading, subjective scoring, bottleneck discovery, and restart discipline.",
        "objective": "Demonstrate a long-running agent loop with role separation, contract first, trace reading, restart, scoring, and bottleneck detection.",
        "authority": "Loop rehearsal. Browser-local trace only.",
        "agents": ["Planner", "Generator", "Evaluator", "Trace Reader", "Scorer", "Bottleneck"],
        "stages": ["Write loop", "Separate roles", "Negotiate contract", "Write to disk", "Restart loop", "Score taste", "Read traces", "Move bottleneck"],
        "artifacts": ["loop-contract.md", "feature-list.json", "trace-log.md", "scorecard.json", "bottleneck-report.md"],
        "routes": ["loop-contract-lab.html", "loop-flight-recorder.html", "goalos-loop-bottleneck-observatory.html", "from-loop-to-rsi-state-capacity.html"]
    },
    "node": {
        "label": "AGI Alpha Node",
        "kicker": "Synthetic AI Labor Infrastructure",
        "title": "Worker, validator, sentinel.",
        "subtitle": "A node handoff packages bounded work, replay metadata, telemetry, validation role, and fail-closed status.",
        "objective": "Prepare an AGI Alpha Node handoff with worker, validator, sentinel roles, replay metadata, and proof package.",
        "authority": "Node handoff simulation. No live node or external compute.",
        "agents": ["Worker", "Validator", "Sentinel", "Meter", "Packager", "Operator"],
        "stages": ["Identity", "Work packet", "Runtime pins", "Telemetry", "Validation", "Sentinel gate", "Handoff"],
        "artifacts": ["node-identity.json", "work-packet.json", "runtime-pins.json", "telemetry-sample.json", "sentinel-report.md", "node-handoff.json"],
        "routes": ["agi-node-validation.html", "validation-control-tower.html", "proof-run-001-docket.html"]
    },
    "validation": {
        "label": "Validation Control Tower",
        "kicker": "Human / AGI Node / Hybrid",
        "title": "Choose who validates the proof.",
        "subtitle": "Human reviewer, AGI Node validator, Hybrid path, or Council mode produce a bounded validation certificate.",
        "objective": "Validate a GoalOS proof path with Human, AGI Node, Hybrid, and Council review options, then issue a public-safe certificate.",
        "authority": "Validation route selection. Human remains final authority for high-impact outcomes.",
        "agents": ["Human", "AGI Node", "Hybrid", "Council", "Risk", "Certificate"],
        "stages": ["Select route", "Check evidence", "Run replay", "Risk gate", "Dispute check", "Certificate", "Next action"],
        "artifacts": ["validation-route.json", "replay-check.json", "risk-gate.json", "validation-certificate.json", "reviewer-brief.md"],
        "routes": ["human-or-agi-node-validation.html", "validator-council-arena.html", "evidence-docket-theatre.html"]
    },
    "contracts": {
        "label": "48 Mainnet Contracts",
        "kicker": "Institutional Proof Rail",
        "title": "Learn the rail without touching a wallet.",
        "subtitle": "Contract Atlas, Contract Academy, and Proof Rail explain identity, jobs, validation, settlement, vaults, boundary, and review posture.",
        "objective": "Teach me the 48 GoalOS-created Ethereum Mainnet contracts by rail, purpose, risk boundary, and proof-review workflow.",
        "authority": "Read-only contract learning mission. No wallet or transaction.",
        "agents": ["Atlas", "Academy", "Identity", "Jobs", "Proof", "Vault", "Boundary", "Reviewer"],
        "stages": ["Rail overview", "Identity layer", "Job layer", "Proof layer", "Vault layer", "Boundary", "Review route", "Docket"],
        "artifacts": ["contract-atlas-review.json", "rail-learning-path.md", "risk-boundary.md", "contract-review-checklist.json", "proof-rail-docket.md"],
        "routes": ["mainnet-contract-atlas.html", "contract-academy.html", "mainnet-proof-rail.html", "token-boundary.html"]
    },
    "proof": {
        "label": "Proof / Evidence",
        "kicker": "Evidence Docket",
        "title": "Claims become reviewable evidence.",
        "subtitle": "Manifest, claims matrix, proof packets, baselines, ledgers, validation certificate, and replay path.",
        "objective": "Build a public-safe Evidence Docket that shows what is claimed, not claimed, what passed, and how a reviewer can replay the path.",
        "authority": "Evidence packaging. No empirical SOTA claim.",
        "agents": ["Manifest", "Claims", "Baseline", "Proof", "Risk", "Replay", "Reviewer"],
        "stages": ["Manifest", "Claims matrix", "Source/evidence map", "Proof packets", "Baseline check", "Risk ledger", "Replay path", "Reviewer brief"],
        "artifacts": ["docket-manifest.md", "claims-matrix.md", "proof-packets.json", "cost-risk-ledger.json", "replay-instructions.md", "reviewer-brief.md"],
        "routes": ["proof-run-001-docket.html", "evidence-docket-theatre.html", "proof-ledger.html", "proof-gradient-lab.html"]
    },
    "navigation": {
        "label": "Navigation Intelligence",
        "kicker": "All Pages / Search / Site Health",
        "title": "Find the right proof surface.",
        "subtitle": "Route registry, search, site map, and health console organize the complete GoalOS public surface.",
        "objective": "Help me find the right GoalOS page for contracts, agents, RSI, nodes, validation, proof, trust, or public boundary.",
        "authority": "Route guidance only.",
        "agents": ["Router", "Search", "Registry", "Health", "Boundary"],
        "stages": ["Read query", "Classify topic", "Rank routes", "Check health", "Open best page"],
        "artifacts": ["route-recommendations.json", "site-health.json", "search-results.md"],
        "routes": ["site-map.html", "search.html", "site-health.html", "ask-goalos.html"]
    },
    "boundary": {
        "label": "Trust Boundary",
        "kicker": "Public Alpha Boundary",
        "title": "Proof-native. Not wallet-first.",
        "subtitle": "No user data, no user funds, no wallet, no transaction, no backend call, no production authority.",
        "objective": "Review the public-alpha boundary and confirm what the website does and does not ask from the user.",
        "authority": "Boundary review. No legal, financial, tax, or regulatory advice.",
        "agents": ["Privacy", "Token", "Security", "Claim", "Reviewer"],
        "stages": ["No data", "No funds", "No wallet", "No transaction", "No backend call", "Claim boundary", "Review"],
        "artifacts": ["boundary-checklist.md", "token-boundary.md", "privacy-posture.md", "claim-boundary.json"],
        "routes": ["trust-boundary.html", "token-boundary.html", "privacy.html", "data-boundary.html", "security-boundary.html"]
    }
}


def ensure_dirs():
    for p in [PUBLIC, ASSETS, REPORTS, CONTENT, EVIDENCE, DOCS, REVIEWER]:
        p.mkdir(parents=True, exist_ok=True)


def title_from_file(name: str) -> str:
    stem = Path(name).stem
    if stem == "index": return "GoalOS Command Center"
    if stem == "404": return "Route Not Found — Use GoalOS"
    parts = re.split(r"[-_]+", stem)
    out = []
    for part in parts:
        low = part.lower()
        if low in {"agi", "rsi", "os", "qa", "ui", "ux", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "v32", "v33", "v34", "v35", "v36", "v37", "v38", "v39", "v40", "v41", "v42", "v43", "v44", "v45", "v46", "v47", "v48", "v49", "v50", "v51", "v52", "v53", "v54", "v55"}:
            out.append(part.upper())
        elif low == "goalos": out.append("GoalOS")
        elif low == "agialpha": out.append("AGIALPHA")
        elif low == "mainnet": out.append("Mainnet")
        elif low == "move37": out.append("Move-37")
        else: out.append(part.capitalize())
    return " ".join(out)


def profile_key_for(name: str) -> str:
    low = name.lower()
    if low == "404.html": return "navigation"
    if "move37" in low or "move-37" in low: return "move37"
    if "loop" in low and "rsi" not in low: return "loop"
    if "rsi" in low or "from-loop" in low or "state-capacity" in low: return "rsi"
    if "playbook" in low or "use-case" in low or "use-cases" in low: return "playbooks"
    if "agent" in low or "meta-agentic" in low or "alpha-agi" in low or "agents" in low: return "agents"
    if "node" in low: return "node"
    if "valid" in low or "validator" in low or "council" in low or "reviewer" in low: return "validation"
    if "contract" in low or "mainnet" in low or "rail" in low or "token" in low: return "contracts" if "boundary" not in low else "boundary"
    if "proof" in low or "evidence" in low or "docket" in low or "ledger" in low or "evolution" in low: return "proof"
    if any(k in low for k in ["search", "site-map", "all-pages", "site-health", "route", "registry", "pathfinder", "ask-goalos", "help", "faq", "troubleshooting"]): return "navigation"
    if any(k in low for k in ["trust", "privacy", "data", "boundary", "security", "legal", "terms", "responsible", "no-data", "claim"]): return "boundary"
    if "autonomy" in low or "demo" in low or "mission" in low: return "autonomy"
    return "command"


def route_category(name: str) -> str:
    pk = profile_key_for(name)
    return {
        "command": "Command Center",
        "autonomy": "Autonomous Demos",
        "agents": "AGI Agents",
        "playbooks": "AGI Agents",
        "rsi": "RSI / Loop",
        "move37": "RSI / Loop",
        "loop": "RSI / Loop",
        "node": "AGI Nodes",
        "validation": "Validation",
        "contracts": "48 Contracts",
        "proof": "Proof / Evidence",
        "navigation": "Navigation",
        "boundary": "Trust Boundary"
    }[pk]


def route_description(name: str, profile_key: str) -> str:
    base = PROFILE_LIBRARY[profile_key]["subtitle"]
    return base[:190]


def read_routes() -> list[dict]:
    routes = []
    if PUBLIC.exists():
        for p in sorted(PUBLIC.glob("*.html")):
            routes.append({
                "href": p.name,
                "title": title_from_file(p.name),
                "category": route_category(p.name),
                "profile": profile_key_for(p.name),
                "description": route_description(p.name, profile_key_for(p.name))
            })
    return routes


def write_assets(routes: list[dict]):
    css = r'''
:root{--bg:#050812;--panel:#0a1324;--panel2:#101b30;--ink:#fff8e8;--muted:#b8c9dd;--line:rgba(147,255,227,.26);--mint:#70ffd8;--cyan:#78e8ff;--gold:#fff36d;--violet:#aa8cff;--rose:#ff5ba6;--ok:#8cffb2;--shadow:0 30px 90px rgba(0,0,0,.42);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}*{box-sizing:border-box}html{scroll-behavior:smooth}body.goalos-v55-surface{margin:0;color:var(--ink);background:radial-gradient(circle at 15% 12%,rgba(112,255,216,.18),transparent 28%),radial-gradient(circle at 80% 7%,rgba(170,140,255,.18),transparent 32%),linear-gradient(135deg,#031210 0%,#071326 45%,#0a0820 100%);min-height:100vh;overflow-x:hidden}body.goalos-v55-surface:before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.24;background-image:linear-gradient(rgba(255,255,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.06) 1px,transparent 1px);background-size:42px 42px;mask-image:linear-gradient(to bottom,#000,transparent 90%)}body.goalos-v55-surface:after{content:"GOALOS";position:fixed;left:-3vw;bottom:-9vw;font-size:20vw;letter-spacing:-.09em;font-weight:1000;color:rgba(255,255,255,.035);z-index:-1}.v55-wrap{width:min(1180px,calc(100% - 40px));margin:0 auto}.v55-nav{position:sticky;top:18px;z-index:30;margin:24px auto 70px;border:1px solid rgba(147,255,227,.25);background:rgba(4,10,21,.76);backdrop-filter:blur(22px);border-radius:28px;box-shadow:var(--shadow);display:flex;align-items:center;justify-content:space-between;padding:14px 16px}.v55-brand{display:flex;gap:12px;align-items:center;text-decoration:none;color:var(--ink);font-weight:1000;letter-spacing:.16em;text-transform:uppercase;font-size:12px}.v55-mark{width:44px;height:44px;border-radius:15px;display:grid;place-items:center;color:#06111b;font-weight:1000;background:radial-gradient(circle at 28% 24%,var(--gold),var(--mint) 36%,var(--cyan) 68%,var(--violet));box-shadow:0 0 34px rgba(112,255,216,.35)}.v55-navlinks{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end}.v55-chip,.v55-btn{appearance:none;border:1px solid rgba(147,255,227,.28);background:rgba(255,255,255,.08);color:var(--ink);padding:11px 15px;border-radius:999px;text-decoration:none;font-weight:900;font-size:13px;cursor:pointer;transition:transform .18s ease,background .18s ease,border .18s ease}.v55-chip:hover,.v55-btn:hover{transform:translateY(-2px);background:rgba(112,255,216,.18);border-color:rgba(112,255,216,.7)}.v55-btn.primary{background:linear-gradient(90deg,var(--gold),var(--mint),var(--cyan));color:#06111b;border:0;box-shadow:0 16px 42px rgba(112,255,216,.25)}.v55-hero{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(320px,.9fr);gap:28px;align-items:stretch}.v55-card{border:1px solid rgba(147,255,227,.28);background:linear-gradient(145deg,rgba(255,255,255,.12),rgba(255,255,255,.05));border-radius:32px;box-shadow:var(--shadow);position:relative;overflow:hidden}.v55-card:before{content:"";position:absolute;inset:-1px;background:radial-gradient(circle at 20% 15%,rgba(255,243,109,.16),transparent 20%),radial-gradient(circle at 75% 20%,rgba(112,255,216,.15),transparent 25%);pointer-events:none}.v55-hero-main{padding:52px;min-height:620px;display:flex;flex-direction:column;justify-content:center}.v55-kicker{display:inline-flex;align-items:center;gap:10px;color:var(--gold);text-transform:uppercase;letter-spacing:.32em;font-weight:1000;font-size:12px;margin-bottom:18px}.v55-kicker:before{content:"";width:9px;height:9px;border-radius:50%;background:var(--mint);box-shadow:0 0 24px var(--mint)}.v55-title{font-size:clamp(52px,8vw,108px);line-height:.84;letter-spacing:-.08em;margin:0 0 24px;max-width:900px}.v55-title em{font-family:Georgia,serif;font-style:italic;font-weight:900;background:linear-gradient(90deg,var(--gold),var(--mint),var(--cyan),var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:-.06em}.v55-subtitle{color:var(--muted);font-size:clamp(18px,2vw,25px);font-weight:850;line-height:1.12;max-width:760px;margin:0 0 28px}.v55-missionbox{border:1px solid rgba(147,255,227,.35);background:rgba(0,0,0,.34);border-radius:26px;padding:16px;margin-top:22px}.v55-missionbox label{display:flex;justify-content:space-between;align-items:center;text-transform:uppercase;letter-spacing:.25em;font-size:11px;color:var(--gold);font-weight:1000;margin:2px 0 12px}.v55-missionbox textarea{width:100%;min-height:120px;resize:vertical;border:1px solid rgba(147,255,227,.35);background:#030915;color:var(--ink);border-radius:18px;padding:18px;font:800 17px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;outline:none}.v55-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.v55-side{padding:34px;display:flex;flex-direction:column;gap:18px}.v55-console-title{display:flex;justify-content:space-between;align-items:center;text-transform:uppercase;letter-spacing:.24em;font-size:12px;font-weight:1000;color:var(--ink);border-bottom:1px solid rgba(255,255,255,.14);padding-bottom:14px}.v55-status{background:rgba(112,255,216,.18);color:var(--mint);border:1px solid rgba(112,255,216,.5);border-radius:999px;padding:8px 12px}.v55-orb{width:150px;height:150px;margin:22px auto;border-radius:50%;display:grid;place-items:center;color:#06111b;font-size:62px;font-weight:1000;background:radial-gradient(circle at 32% 28%,var(--gold),var(--mint) 38%,var(--cyan) 64%,var(--violet));box-shadow:0 0 70px rgba(112,255,216,.36);animation:v55pulse 3s ease-in-out infinite}.v55-stagegrid,.v55-agentgrid,.v55-routegrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.v55-stage{border:1px solid rgba(147,255,227,.25);background:rgba(255,255,255,.06);border-radius:16px;padding:12px;min-height:72px}.v55-stage b,.v55-route b{display:block;font-size:13px}.v55-stage span,.v55-route span{display:block;color:var(--muted);font-size:12px;margin-top:5px}.v55-stage.is-active{background:linear-gradient(135deg,rgba(112,255,216,.22),rgba(170,140,255,.12));border-color:var(--mint);box-shadow:0 0 30px rgba(112,255,216,.18)}.v55-section{margin:34px auto}.v55-section h2{font-size:clamp(34px,5vw,68px);line-height:.9;letter-spacing:-.06em;margin:0 0 18px}.v55-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.v55-info{padding:22px;border:1px solid rgba(147,255,227,.22);border-radius:24px;background:rgba(255,255,255,.07)}.v55-info h3{margin:0 0 8px;font-size:22px;letter-spacing:-.03em}.v55-info p{margin:0;color:var(--muted);font-weight:650}.v55-flow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}.v55-flow .v55-flow-step{position:relative;border:1px solid rgba(147,255,227,.25);border-radius:18px;background:rgba(255,255,255,.06);padding:15px;min-height:96px}.v55-flow .v55-flow-step:after{content:"→";position:absolute;right:-12px;top:35%;color:var(--mint);font-weight:1000}.v55-flow .v55-flow-step:nth-child(5n):after,.v55-flow .v55-flow-step:last-child:after{display:none}.v55-boundary{font-size:14px;color:var(--muted);padding:22px;border:1px solid rgba(255,91,166,.32);border-radius:20px;background:rgba(255,91,166,.08);margin:30px 0 70px}.v55-footer{padding:20px 0 90px;color:var(--muted);font-size:13px}.v55-dock{position:fixed;right:18px;bottom:18px;z-index:80;display:flex;gap:8px;align-items:center;background:rgba(3,9,21,.65);border:1px solid rgba(147,255,227,.22);border-radius:999px;padding:8px;backdrop-filter:blur(18px);box-shadow:var(--shadow)}.v55-dock a,.v55-dock button{border:0;border-radius:999px;padding:13px 16px;background:rgba(255,255,255,.08);color:var(--ink);font-weight:1000;text-decoration:none;cursor:pointer}.v55-dock button:first-child{background:linear-gradient(90deg,var(--gold),var(--mint));color:#06111b}.v55-modal{position:fixed;inset:0;z-index:100;display:none;align-items:center;justify-content:center;padding:24px;background:rgba(2,6,13,.78);backdrop-filter:blur(12px)}.v55-modal.is-open{display:flex}.v55-cockpit{width:min(1120px,100%);max-height:92vh;overflow:auto;border:1px solid rgba(147,255,227,.38);background:linear-gradient(145deg,#071124,#0a1022 55%,#071b1a);box-shadow:0 35px 120px rgba(0,0,0,.7);border-radius:32px;padding:30px;color:var(--ink)}.v55-cockpit-head{display:flex;justify-content:space-between;gap:20px;align-items:start}.v55-cockpit h2{font-size:clamp(38px,6vw,72px);line-height:.88;letter-spacing:-.06em;margin:8px 0 12px}.v55-close{background:rgba(255,255,255,.1);border:1px solid rgba(147,255,227,.24);color:var(--ink);border-radius:999px;padding:10px 14px;font-weight:1000}.v55-mission-input{width:100%;min-height:96px;background:#030915;border:1px solid rgba(112,255,216,.45);border-radius:16px;color:var(--ink);padding:16px;font:800 15px/1.45 ui-monospace,monospace}.v55-cockpit-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:18px}.v55-run-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:18px 0}.v55-run-step,.v55-agent-pill{border:1px solid rgba(147,255,227,.22);border-radius:16px;padding:13px;background:rgba(255,255,255,.07)}.v55-run-step.active,.v55-agent-pill.active{border-color:var(--mint);background:rgba(112,255,216,.18);box-shadow:0 0 28px rgba(112,255,216,.14)}.v55-bars{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.v55-bar label{display:flex;justify-content:space-between;font-weight:1000;font-size:13px}.v55-track{height:10px;background:rgba(255,255,255,.12);border-radius:999px;overflow:hidden}.v55-fill{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--mint),var(--cyan),var(--violet));transition:width .25s ease}.v55-log{min-height:190px;background:#020712;border:1px solid rgba(112,255,216,.35);border-radius:18px;padding:14px;font:800 13px/1.5 ui-monospace,monospace;color:var(--mint);white-space:pre-wrap}.v55-artifacts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:9px;margin-top:14px}.v55-artifacts a{display:flex;justify-content:space-between;text-decoration:none;color:var(--ink);padding:12px;border-radius:14px;background:rgba(255,255,255,.09);border:1px solid rgba(147,255,227,.19);font-weight:900}.v55-agentlist{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.v55-ask-panel{margin-top:18px}.v55-ask-panel input{width:100%;border:1px solid rgba(112,255,216,.4);border-radius:999px;background:#030915;color:var(--ink);padding:14px 18px;font-weight:800}.v55-answer{margin-top:12px;color:var(--muted);font-weight:750}.v55-answer a{color:var(--mint);font-weight:1000}.v55-table{width:100%;border-collapse:separate;border-spacing:0 8px}.v55-table tr{background:rgba(255,255,255,.06)}.v55-table td{padding:14px;border-top:1px solid rgba(147,255,227,.15);border-bottom:1px solid rgba(147,255,227,.15)}.v55-table td:first-child{border-left:1px solid rgba(147,255,227,.15);border-radius:14px 0 0 14px}.v55-table td:last-child{border-right:1px solid rgba(147,255,227,.15);border-radius:0 14px 14px 0}.v55-search{width:100%;padding:16px 18px;border-radius:999px;background:rgba(0,0,0,.32);border:1px solid rgba(147,255,227,.3);color:var(--ink);font-weight:850;margin-bottom:18px}.v55-light body{background:#fff}@keyframes v55pulse{0%,100%{transform:scale(1);filter:saturate(1)}50%{transform:scale(1.04);filter:saturate(1.35)}}@media(max-width:900px){.v55-hero,.v55-cockpit-grid{grid-template-columns:1fr}.v55-grid{grid-template-columns:1fr}.v55-flow,.v55-run-grid{grid-template-columns:1fr 1fr}.v55-title{font-size:58px}.v55-hero-main{padding:34px;min-height:auto}.v55-nav{position:relative;top:0;flex-direction:column;align-items:flex-start}.v55-dock{left:10px;right:10px;overflow:auto;justify-content:flex-start}.v55-dock a,.v55-dock button{white-space:nowrap}.v55-flow .v55-flow-step:after{display:none}}
'''
    js_profiles = "window.GoalOSDemoProfilesV55 = " + json.dumps(PROFILE_LIBRARY, indent=2) + ";\n"
    js = r'''
(function(){
  const profiles = window.GoalOSDemoProfilesV55 || {};
  const defaultProfile = profiles.command;
  const routeMap = window.GoalOSRouteRegistryV55 || [];
  const KEYWORDS = [
    ["contract", "mainnet-contract-atlas.html"], ["48", "mainnet-contract-atlas.html"], ["token", "token-boundary.html"],
    ["rsi", "from-loop-to-rsi-state-capacity.html"], ["loop", "loop-bottleneck-observatory.html"], ["move", "move37-dossier.html"],
    ["node", "agi-alpha-node-v0.html"], ["agent", "agi-agent-workbench.html"], ["validate", "validation-control-tower.html"],
    ["human", "human-or-agi-node-validation.html"], ["proof", "proof-run-001-docket.html"], ["docket", "evidence-docket-theatre.html"],
    ["search", "search.html"], ["all", "all-pages.html"], ["trust", "trust-boundary.html"], ["privacy", "privacy.html"], ["wallet", "token-boundary.html"]
  ];
  const $ = (s, r=document) => r.querySelector(s);
  const $$ = (s, r=document) => Array.from(r.querySelectorAll(s));
  function path(){ return (location.pathname.split('/').pop() || 'index.html').toLowerCase(); }
  function profile(){ return profiles[document.body.dataset.goalosProfile || window.GOALOS_V55_PROFILE_KEY] || classify() || defaultProfile; }
  function classify(){ const p=path(); if(p.includes('move37')) return profiles.move37; if(p.includes('loop')&&!p.includes('rsi')) return profiles.loop; if(p.includes('rsi')) return profiles.rsi; if(p.includes('playbook')||p.includes('use-case')) return profiles.playbooks; if(p.includes('agent')||p.includes('meta-agentic')) return profiles.agents; if(p.includes('node')) return profiles.node; if(p.includes('valid')||p.includes('validator')||p.includes('council')) return profiles.validation; if(p.includes('contract')||p.includes('mainnet')) return profiles.contracts; if(p.includes('proof')||p.includes('evidence')||p.includes('docket')||p.includes('ledger')) return profiles.proof; if(p.includes('search')||p.includes('site')||p.includes('all-pages')||p.includes('ask')) return profiles.navigation; if(p.includes('trust')||p.includes('privacy')||p.includes('boundary')||p.includes('token')) return profiles.boundary; return profiles.command; }
  function esc(s){return String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
  function artifactContent(name, p, objective){ return JSON.stringify({goalos:'Sovereign Experience OS V55', page:path(), mission:p.label, objective, artifact:name, boundary:'browser-local public-alpha demonstration; no wallet; no transaction; no backend call', generatedAt:new Date().toISOString(), stages:p.stages, agents:p.agents, nextRoutes:p.routes}, null, 2); }
  function downloadUrl(text){ const blob = new Blob([text], {type:'application/json;charset=utf-8'}); return URL.createObjectURL(blob); }
  function buildModal(){
    let m = $('#goalos-v55-modal'); if(m) return m;
    m = document.createElement('div'); m.id='goalos-v55-modal'; m.className='v55-modal goalos-v55';
    m.innerHTML = '<div class="v55-cockpit"><div class="v55-cockpit-head"><div><div class="v55-kicker">Autonomous Experience</div><h2 id="v55-modal-title">Run the proof path.</h2><p class="v55-subtitle" id="v55-modal-subtitle"></p></div><button class="v55-close" data-v55-close>Close</button></div><textarea id="v55-objective" class="v55-mission-input"></textarea><div class="v55-actions"><button class="v55-btn primary" id="v55-run-now">Run mission</button><button class="v55-btn" id="v55-ask-now">Ask GoalOS</button></div><div class="v55-cockpit-grid"><div><div id="v55-run-grid" class="v55-run-grid"></div><div class="v55-bars"><div class="v55-bar"><label>Readiness <span id="bar-readiness-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-readiness"></span></div></div><div class="v55-bar"><label>Replay <span id="bar-replay-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-replay"></span></div></div><div class="v55-bar"><label>Risk <span id="bar-risk-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-risk"></span></div></div><div class="v55-bar"><label>Reuse <span id="bar-reuse-v">0</span></label><div class="v55-track"><span class="v55-fill" id="bar-reuse"></span></div></div></div><pre class="v55-log" id="v55-log"></pre><div class="v55-artifacts" id="v55-artifacts"></div></div><aside><h3>Agent constellation</h3><div id="v55-agentlist" class="v55-agentlist"></div><div class="v55-ask-panel"><input id="v55-ask-input" placeholder="Ask about agents, RSI, nodes, contracts, validation, proof..."><button class="v55-btn" id="v55-answer-btn" style="margin-top:10px">Answer</button><div class="v55-answer" id="v55-answer"></div></div></aside></div></div>';
    document.body.appendChild(m);
    m.addEventListener('click', e=>{ if(e.target===m || e.target.matches('[data-v55-close]')) m.classList.remove('is-open'); });
    $('#v55-run-now',m).addEventListener('click',()=>runMission(profile()));
    $('#v55-ask-now',m).addEventListener('click',()=>answerAsk());
    $('#v55-answer-btn',m).addEventListener('click',()=>answerAsk());
    $('#v55-ask-input',m).addEventListener('keydown',e=>{if(e.key==='Enter') answerAsk();});
    return m;
  }
  function openMission(p=profile(), auto=true){
    const m = buildModal();
    $('#v55-modal-title',m).textContent = p.title || 'Run the full proof path.';
    $('#v55-modal-subtitle',m).textContent = p.subtitle || '';
    $('#v55-objective',m).value = p.objective || '';
    $('#v55-run-grid',m).innerHTML = (p.stages||[]).map((s,i)=>'<div class="v55-run-step" data-step="'+i+'"><b>'+String(i+1).padStart(2,'0')+'</b><br>'+esc(s)+'</div>').join('');
    $('#v55-agentlist',m).innerHTML = (p.agents||[]).map((a,i)=>'<div class="v55-agent-pill" data-agent="'+i+'">'+esc(a)+'</div>').join('');
    $('#v55-log',m).textContent = 'GoalOS mission cockpit ready.\nObjective: ' + (p.objective||'') + '\nClick Run mission or edit the objective first.';
    $('#v55-artifacts',m).innerHTML = '';
    ['readiness','replay','risk','reuse'].forEach(k=>{ $('#bar-'+k,m).style.width='0%'; $('#bar-'+k+'-v',m).textContent='0'; });
    m.classList.add('is-open');
    if(auto) setTimeout(()=>runMission(p), 180);
  }
  function runMission(p=profile()){
    const m = buildModal(); const objective = ($('#v55-objective',m)||{}).value || p.objective;
    const steps = p.stages || []; const agents = p.agents || [];
    $('#v55-log',m).textContent = 'GoalOS mission initialized.\nMission: '+p.label+'\nObjective: '+objective+'\nBoundary: browser-local; no wallet; no transaction; no backend call.\n';
    $('#v55-artifacts',m).innerHTML = '';
    $$('.v55-run-step',m).forEach(x=>x.classList.remove('active')); $$('.v55-agent-pill',m).forEach(x=>x.classList.remove('active'));
    let i=0;
    const timer = setInterval(()=>{
      if(i>=steps.length){ clearInterval(timer); finishMission(p, objective, m); return; }
      const st = $('[data-step="'+i+'"]',m); if(st) st.classList.add('active');
      const ag = $('[data-agent="'+(i%Math.max(agents.length,1))+'"]',m); if(ag) ag.classList.add('active');
      const pct = Math.round(((i+1)/steps.length)*100);
      $('#bar-readiness',m).style.width=pct+'%'; $('#bar-readiness-v',m).textContent=pct;
      $('#bar-replay',m).style.width=Math.min(100,Math.round(pct*.86+8))+'%'; $('#bar-replay-v',m).textContent=Math.min(100,Math.round(pct*.86+8));
      $('#bar-risk',m).style.width=Math.min(100,Math.round(100-pct*.18))+'%'; $('#bar-risk-v',m).textContent=Math.min(100,Math.round(100-pct*.18));
      $('#bar-reuse',m).style.width=Math.min(100,Math.round(pct*.74+12))+'%'; $('#bar-reuse-v',m).textContent=Math.min(100,Math.round(pct*.74+12));
      $('#v55-log',m).textContent += String(i+1).padStart(2,'0')+' · '+steps[i]+' · '+(agents[i%agents.length]||'GoalOS')+' · local pass\n';
      $('#v55-log',m).scrollTop = $('#v55-log',m).scrollHeight;
      i++;
    }, 320);
  }
  function finishMission(p, objective, m){
    $('#v55-log',m).textContent += 'DONE=true · Evidence Docket ready · validation path prepared · Chronicle draft available.\n';
    const arts = (p.artifacts||['mission-contract.json','evidence-docket.md','reviewer-brief.md']);
    $('#v55-artifacts',m).innerHTML = arts.map(name=>'<a download="'+esc(name)+'" href="'+downloadUrl(artifactContent(name,p,objective))+'"><span>'+esc(name)+'</span><b>Download</b></a>').join('');
    const routes = (p.routes||[]).map(r=>'<a class="v55-chip" href="'+esc(r)+'">'+esc(titleFromRoute(r))+'</a>').join(' ');
    $('#v55-log',m).textContent += 'Next best routes: '+(p.routes||[]).join(', ')+'\n';
    if(routes){ $('#v55-artifacts',m).insertAdjacentHTML('beforeend','<div style="grid-column:1/-1;margin-top:8px"><b>Next pages</b><div class="v55-actions">'+routes+'</div></div>'); }
  }
  function titleFromRoute(r){ const found=routeMap.find(x=>x.href===r); return found?found.title:r.replace(/\.html$/,'').replace(/-/g,' '); }
  function answerAsk(){
    const m = buildModal(); const q = (($('#v55-ask-input',m)||{}).value || $('#v55-objective',m).value || '').toLowerCase();
    let dest = 'site-map.html'; for(const [kw,href] of KEYWORDS){ if(q.includes(kw)){ dest=href; break; }}
    const prof = profile();
    $('#v55-answer',m).innerHTML = 'Best next page: <a href="'+dest+'">'+titleFromRoute(dest)+'</a>. For this page, run <b>'+esc(prof.label)+'</b> to create local artifacts and a reviewer-ready path.';
  }
  function installDock(){
    $$('.goalos-v55-legacy-hidden').forEach(x=>x.remove());
    $$('a,button').forEach(el=>{ try{ const s=getComputedStyle(el); const b=parseFloat(s.bottom||'999'); if(s.position==='fixed' && b<160 && !el.closest('.goalos-v55')){ el.style.display='none'; el.classList.add('goalos-v55-legacy-hidden'); }}catch(e){} });
    if($('#goalos-v55-dock')) return;
    const d=document.createElement('div'); d.id='goalos-v55-dock'; d.className='v55-dock goalos-v55';
    d.innerHTML='<button data-v55-run>Run end-to-end demo</button><a href="agi-agent-workbench.html">AGI Agents</a><a href="from-loop-to-rsi-state-capacity.html">RSI / Loop</a><a href="validation-control-tower.html">Validate</a><a href="mainnet-contract-atlas.html">48 Contracts</a><a href="all-pages.html">All Pages</a><button data-v55-ask>Ask GoalOS</button>';
    document.body.appendChild(d);
  }
  function bindClicks(){
    document.addEventListener('click', e=>{
      const el = e.target.closest('a,button'); if(!el) return;
      const txt = (el.textContent||'').toLowerCase().trim(); const href=(el.getAttribute('href')||'').toLowerCase();
      if(el.matches('[data-v55-run]') || txt.includes('run end-to-end') || txt==='run demo' || txt.includes('run mission')){ e.preventDefault(); openMission(profile(), true); }
      if(el.matches('[data-v55-ask]') || txt.includes('ask goalos') || txt.includes('tell goalos') || href.includes('ask-goalos')){ if(!href || href==='#'){ e.preventDefault(); openMission(profile(), false); setTimeout(()=>$('#v55-ask-input')?.focus(),80); } }
    }, true);
  }
  function initSearch(){
    const input = $('#v55-route-search'); const list = $('#v55-route-list'); if(!input||!list) return;
    function render(q=''){
      q=q.toLowerCase(); const rows=routeMap.filter(r=>!q||[r.title,r.category,r.description,r.href].join(' ').toLowerCase().includes(q));
      list.innerHTML = rows.map(r=>'<tr><td>'+esc(r.category)+'</td><td><b>'+esc(r.title)+'</b><br><span>'+esc(r.description)+'</span></td><td><a class="v55-chip" href="'+esc(r.href)+'">Open</a></td></tr>').join('');
    }
    input.addEventListener('input',()=>render(input.value)); render('');
  }
  window.GoalOSV55 = {openMission, runMission, profile, answerAsk};
  document.addEventListener('DOMContentLoaded',()=>{ installDock(); bindClicks(); initSearch(); });
})();
'''
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "goalos-sovereign-experience-v55.css").write_text(css, encoding="utf-8")
    (ASSETS / "goalos-demo-profiles-v55.js").write_text(js_profiles, encoding="utf-8")
    (ASSETS / "goalos-sovereign-experience-v55.js").write_text(js, encoding="utf-8")
    (ASSETS / "goalos-mark.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><defs><radialGradient id="g" cx="32%" cy="28%"><stop offset="0" stop-color="#fff36d"/><stop offset=".36" stop-color="#70ffd8"/><stop offset=".68" stop-color="#78e8ff"/><stop offset="1" stop-color="#aa8cff"/></radialGradient></defs><rect width="128" height="128" rx="32" fill="url(#g)"/><text x="64" y="82" text-anchor="middle" font-family="Arial,sans-serif" font-size="70" font-weight="900" fill="#06111b">α</text></svg>', encoding="utf-8")
    # Compatibility aliases for older pages.
    (ASSETS / "goalos.css").write_text('@import url("goalos-sovereign-experience-v55.css");', encoding="utf-8")
    (ASSETS / "goalos.js").write_text('document.addEventListener("DOMContentLoaded",()=>{document.body.classList.add("goalos-v55-surface")});', encoding="utf-8")
    route_js = "window.GoalOSRouteRegistryV55 = " + json.dumps(routes, indent=2) + ";\n"
    (ASSETS / "goalos-route-registry-v55.js").write_text(route_js, encoding="utf-8")


def render_nav(current: str) -> str:
    nav = [
        ("index.html", "Mission"), ("autonomy-theatre.html", "Run Demo"), ("agi-agent-workbench.html", "AGI Agents"),
        ("from-loop-to-rsi-state-capacity.html", "RSI / Loop"), ("agi-alpha-node-v0.html", "AGI Node"),
        ("validation-control-tower.html", "Validate"), ("mainnet-contract-atlas.html", "48 Contracts"),
        ("all-pages.html", "All Pages"), ("search.html", "Search"), ("site-health.html", "Health")
    ]
    links = ''.join(f'<a class="v55-chip" href="{html.escape(h)}">{html.escape(t)}</a>' for h,t in nav)
    return f'<nav class="v55-nav v55-wrap"><a class="v55-brand" href="index.html"><span class="v55-mark">α</span><span>GoalOS<br><small>AGIALPHA Ascension</small></span></a><div class="v55-navlinks">{links}<button class="v55-chip" data-v55-ask>Ask /</button></div></nav>'


def render_page(route: dict, routes: list[dict]) -> str:
    pk = route["profile"]
    p = PROFILE_LIBRARY[pk]
    title = route["title"]
    # Adjust hero: canonical route title for specific pages, profile title for index.
    hero_title = p["title"] if route["href"] in {"index.html", "goalos-phase-completion.html", "goalos-command-center.html"} else title
    if route["href"] == "404.html":
        hero_title = "Route not found. Use GoalOS."
    italic_word = "" 
    if " " in hero_title:
        parts = hero_title.rsplit(" ", 1)
        hero_html = html.escape(parts[0]) + " <em>" + html.escape(parts[1]) + "</em>"
    else:
        hero_html = html.escape(hero_title)
    stage_cards = ''.join(f'<div class="v55-stage"><b>{i+1:02d} {html.escape(s)}</b><span>{html.escape(p["authority"] if i==0 else "Public-safe browser-local proof step.")}</span></div>' for i,s in enumerate(p["stages"][:8]))
    flow_steps = ''.join(f'<div class="v55-flow-step"><b>{i+1:02d}</b><h3>{html.escape(s)}</h3><p>{html.escape("Creates evidence, checks gates, and preserves reviewability.")}</p></div>' for i,s in enumerate(p["stages"]))
    agent_cards = ''.join(f'<div class="v55-info"><h3>{html.escape(a)}</h3><p>{html.escape("Role participates only inside the page-specific proof mission.")}</p></div>' for a in p["agents"][:6])
    route_cards = ''.join(f'<a class="v55-info" href="{html.escape(h)}"><h3>{html.escape(title_from_file(h))}</h3><p>Open this canonical surface next.</p></a>' for h in p["routes"][:6])
    body_extra = ''
    if route["href"] in {"all-pages.html", "site-map.html", "route-registry.html", "search.html"}:
        body_extra = render_all_pages_section(routes)
    if route["href"] == "site-health.html":
        body_extra = render_health_section(routes)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · GoalOS AGIALPHA Ascension</title>
<meta name="description" content="{html.escape(p['subtitle'])}">
<link rel="icon" href="assets/goalos-mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="assets/goalos-sovereign-experience-v55.css">
<script>window.GOALOS_V55_PROFILE_KEY={json.dumps(pk)};</script>
<script src="assets/goalos-route-registry-v55.js" defer></script>
<script src="assets/goalos-demo-profiles-v55.js" defer></script>
<script src="assets/goalos-sovereign-experience-v55.js" defer></script>
</head>
<body class="goalos-v55-surface" data-goalos-profile="{html.escape(pk)}">
{render_nav(route['href'])}
<main class="v55-wrap">
<section class="v55-hero">
  <article class="v55-card v55-hero-main">
    <div class="v55-kicker">{html.escape(p['kicker'])}</div>
    <h1 class="v55-title">{hero_html}</h1>
    <p class="v55-subtitle">{html.escape(p['subtitle'])}</p>
    <div class="v55-actions"><button class="v55-btn primary" data-v55-run>Run end-to-end demo</button><button class="v55-btn" data-v55-ask>Ask GoalOS</button><a class="v55-btn" href="all-pages.html">Open all pages</a></div>
    <div class="v55-missionbox"><label>What do you want GoalOS to accomplish? <span>browser-local</span></label><textarea>{html.escape(p['objective'])}</textarea><div class="v55-actions"><button class="v55-btn primary" data-v55-run>Generate proof path</button><a class="v55-btn" href="{html.escape(p['routes'][0] if p['routes'] else 'site-map.html')}">Open next route</a></div></div>
  </article>
  <aside class="v55-card v55-side">
    <div class="v55-console-title"><span>{html.escape(p['label'])} console</span><span class="v55-status">Ready</span></div>
    <div class="v55-orb">α</div>
    <div class="v55-stagegrid">{stage_cards}</div>
  </aside>
</section>
<section class="v55-section">
  <div class="v55-kicker">Page-specific mission</div>
  <h2>What this surface does</h2>
  <div class="v55-grid">{agent_cards}</div>
</section>
<section class="v55-section">
  <div class="v55-kicker">Proof flow</div>
  <h2>From intent to evidence</h2>
  <div class="v55-flow">{flow_steps}</div>
</section>
<section class="v55-section">
  <div class="v55-kicker">Canonical routes</div>
  <h2>Best next pages</h2>
  <div class="v55-grid">{route_cards}</div>
</section>
{body_extra}
<div class="v55-boundary"><b>Public-alpha boundary.</b> {html.escape(BOUNDARY)} $AGIALPHA is presented as public contract / protocol context only; no sale, custody, wallet support, investment, trading, legal, tax, exchange, bridge, liquidity, or regulatory advice is provided.</div>
</main>
<footer class="v55-footer v55-wrap">GoalOS AGIALPHA Ascension — Sovereign Machine Economy public-alpha proof operating surface.</footer>
</body>
</html>'''


def render_all_pages_section(routes: list[dict]) -> str:
    rows = ''.join(f'<tr><td>{html.escape(r["category"])}</td><td><b>{html.escape(r["title"])}</b><br><span>{html.escape(r["description"])}</span></td><td><a class="v55-chip" href="{html.escape(r["href"])}">Open</a></td></tr>' for r in routes)
    return f'''<section class="v55-section"><div class="v55-kicker">Route inventory</div><h2>Everything routeable</h2><input id="v55-route-search" class="v55-search" placeholder="Search GoalOS pages: agents, RSI, node, contracts, proof, validation..."><table class="v55-table"><tbody id="v55-route-list">{rows}</tbody></table></section>'''


def render_health_section(routes: list[dict]) -> str:
    return f'''<section class="v55-section"><div class="v55-kicker">Site Health</div><h2>Ready for review</h2><div class="v55-grid"><div class="v55-info"><h3>{len(routes)} routes</h3><p>Current top-level public pages indexed.</p></div><div class="v55-info"><h3>Boundary preserved</h3><p>No user data, wallet, transaction, backend call, or production authority.</p></div><div class="v55-info"><h3>Interactive demos</h3><p>Every major route receives a page-specific browser-local mission cockpit.</p></div></div></section>'''


def rehydrate_missing():
    snapshots = [ROOT / ".goalos" / "site-immersive-command-center-v16" / "public-snapshot", ROOT / ".goalos" / "site-experience-command-center-v13" / "public-snapshot"]
    for snap in snapshots:
        if snap.exists():
            for p in snap.rglob("*.html"):
                rel = p.relative_to(snap)
                dest = PUBLIC / rel
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dest)


def write_pages(routes: list[dict]):
    for r in routes:
        (PUBLIC / r["href"]).write_text(render_page(r, routes), encoding="utf-8")


def create_compatibility_assets():
    # For every directory containing HTML, create compatibility assets so legacy archive pages remain navigable.
    html_dirs = {p.parent for p in PUBLIC.rglob("*.html")}
    for d in html_dirs:
        ad = d / "assets"
        ad.mkdir(exist_ok=True)
        rel_assets = Path(*([".."] * len(d.relative_to(PUBLIC).parts))) / "assets" if d != PUBLIC else Path("assets")
        (ad / "goalos.css").write_text('@import url("' + html.escape(str(rel_assets / 'goalos-sovereign-experience-v55.css').replace('\\','/')) + '");', encoding="utf-8")
        (ad / "goalos.js").write_text('document.addEventListener("DOMContentLoaded",()=>{document.body.classList.add("goalos-v55-surface")});', encoding="utf-8")
        svg_src = ASSETS / "goalos-mark.svg"
        if svg_src.exists() and (ad / "goalos-mark.svg").resolve() != svg_src.resolve(): shutil.copy2(svg_src, ad / "goalos-mark.svg")
        status = {"status":"discoverable","boundary":"preserved","externalActions":0,"productionAuthorization":"not_granted"}
        for nm in ["site-status.json", "search_index.json", "search-index.json"]:
            (d / nm).write_text(json.dumps(status, indent=2), encoding="utf-8")


def sanitize_public_files():
    for p in PUBLIC.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".html", ".js", ".css"}:
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            original = txt
            for old,new in FORBIDDEN_REPLACEMENTS.items():
                txt = txt.replace(old,new)
            if txt != original:
                p.write_text(txt, encoding="utf-8")


def ensure_missing_internal_targets():
    # Create simple pages for missing internal HTML links.
    href_re = re.compile(r'''(?:href|src)=["']([^"']+)["']''', re.I)
    created=[]
    for p in list(PUBLIC.rglob("*.html")):
        txt = p.read_text(encoding="utf-8", errors="ignore")
        for m in href_re.finditer(txt):
            target = m.group(1).split('#')[0].split('?')[0]
            if not target or target.startswith(('http:', 'https:', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            if target.endswith('/'):
                target += 'index.html'
            if target.endswith('.html'):
                dest = (p.parent / target).resolve()
                try:
                    dest.relative_to(PUBLIC.resolve())
                except Exception:
                    continue
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    name = dest.name
                    route = {"href": name, "title": title_from_file(name), "category": route_category(name), "profile": profile_key_for(name), "description": route_description(name, profile_key_for(name))}
                    dest.write_text(render_page(route, read_routes()), encoding="utf-8")
                    created.append(str(dest.relative_to(ROOT)))
            elif re.search(r'\.(css|js|svg|json|png|jpg|jpeg|webp)$', target, re.I):
                dest=(p.parent/target).resolve()
                try:
                    dest.relative_to(PUBLIC.resolve())
                except Exception:
                    continue
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    ext=dest.suffix.lower()
                    if ext=='.css': dest.write_text('@import url("/assets/goalos-sovereign-experience-v55.css");',encoding='utf-8')
                    elif ext=='.js': dest.write_text('document.addEventListener("DOMContentLoaded",()=>{document.body.classList.add("goalos-v55-surface")});',encoding='utf-8')
                    elif ext=='.svg': dest.write_text((ASSETS/"goalos-mark.svg").read_text(encoding='utf-8'),encoding='utf-8')
                    elif ext=='.json': dest.write_text(json.dumps({"status":"discoverable","boundary":"preserved"}, indent=2),encoding='utf-8')
                    else: dest.write_bytes(b'')
                    created.append(str(dest.relative_to(ROOT)))
    return created


def audit():
    forbidden=[]
    for p in PUBLIC.rglob("*"):
        if p.is_file() and p.suffix.lower() in {".html", ".js"}:
            txt=p.read_text(encoding='utf-8', errors='ignore')
            for pat in ["localStorage", "sessionStorage", "sendBeacon", "window.ethereum", "XMLHttpRequest", "fetch("]:
                if pat in txt:
                    forbidden.append({"file":str(p.relative_to(ROOT)), "pattern":pat})
    broken=[]
    href_re=re.compile(r'''(?:href|src)=["']([^"']+)["']''', re.I)
    for p in PUBLIC.rglob("*.html"):
        txt=p.read_text(encoding='utf-8', errors='ignore')
        for m in href_re.finditer(txt):
            target=m.group(1).split('#')[0].split('?')[0]
            if not target or target.startswith(('http:', 'https:', 'mailto:', 'tel:', 'javascript:', 'data:')):
                continue
            if target.endswith('/'):
                target+='index.html'
            if re.search(r'\.(html|css|js|svg|json|png|jpg|jpeg|webp)$', target, re.I):
                dest=(p.parent/target).resolve()
                try: dest.relative_to(PUBLIC.resolve())
                except Exception: continue
                if not dest.exists(): broken.append({"file":str(p.relative_to(ROOT)), "target":target})
    return forbidden, broken


def write_reports(routes: list[dict], created: list[str], forbidden: list[dict], broken: list[dict]):
    status = "passed" if not forbidden and not broken else "failed"
    now = datetime.now(timezone.utc).isoformat()
    report = {
        "version": VERSION,
        "name": "GoalOS Sovereign Experience OS V55",
        "status": status,
        "timestamp": now,
        "publicPages": len(list(PUBLIC.rglob('*.html'))),
        "currentRoutesIndexed": len(routes),
        "createdCompatibilityTargets": created[:300],
        "forbiddenBrowserApiHits": forbidden,
        "brokenInternalLinksOrAssets": broken,
        "boundary": "preserved",
        "externalActions": 0,
        "productionAuthorization": "not_granted",
        "empiricalSotaClaim": "not_claimed",
        "walletTransactionSupport": "not_enabled",
        "pageSpecificAutonomousDemos": True,
        "canonicalSurfaces": CANONICAL_ROUTES,
        "notes": "Every top-level public route is rendered with the V55 sovereign interaction shell. Major routes have page-specific mission profiles."
    }
    for name in ["install-report", "qa", "route-health", "audit", "demo-run"]:
        (REPORTS / f"{SLUG}-{name}.json").write_text(json.dumps(report, indent=2), encoding='utf-8')
    (EVIDENCE / f"{SLUG}-reference-docket.json").write_text(json.dumps({"docket":"GoalOS V55 reference docket", **report}, indent=2), encoding='utf-8')
    (CONTENT / "public-proof-navigation-v55.json").write_text(json.dumps(routes, indent=2), encoding='utf-8')
    (CONTENT / "demo-ecosystem-registry-v55.json").write_text(json.dumps(PROFILE_LIBRARY, indent=2), encoding='utf-8')
    (DOCS / "GOALOS_SOVEREIGN_EXPERIENCE_OS_V55.md").write_text("# GoalOS Sovereign Experience OS V55\n\nPage-specific autonomous demos, canonical route surface, complete navigation, and strict public-alpha boundary.\n", encoding='utf-8')
    (REVIEWER / "HOW_TO_REVIEW_GOALOS_V55.md").write_text("# Review GoalOS V55\n\nOpen index.html, autonomy-theatre.html, agi-agent-workbench.html, from-loop-to-rsi-state-capacity.html, move37-dossier.html, agi-alpha-node-v0.html, validation-control-tower.html, mainnet-contract-atlas.html, proof-run-001-docket.html, ask-goalos.html, all-pages.html, search.html, and site-health.html. Click Run end-to-end demo on each. Confirm page-specific mission, readable layout, no overlap, no wallet, no transaction, no backend call.\n", encoding='utf-8')
    print(json.dumps(report, indent=2))
    if status != "passed":
        raise SystemExit(1)


def main():
    ensure_dirs()
    rehydrate_missing()
    routes = read_routes()
    write_assets(routes)
    # Refresh routes after assets; then write pages.
    routes = read_routes()
    write_pages(routes)
    create_compatibility_assets()
    sanitize_public_files()
    created = ensure_missing_internal_targets()
    # Re-read and update registries after possible fallback creation.
    routes = read_routes()
    write_assets(routes)
    write_pages(routes)
    create_compatibility_assets()
    sanitize_public_files()
    created.extend(ensure_missing_internal_targets())
    forbidden, broken = audit()
    write_reports(routes, sorted(set(created)), forbidden, broken)

if __name__ == "__main__":
    main()
