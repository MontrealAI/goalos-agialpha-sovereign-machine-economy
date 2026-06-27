from __future__ import annotations

from pathlib import Path
from typing import Any

from .agent_foundry import MetaAgenticFoundry
from .agi_jobs import AGIJobsLedger
from .coordination import CoordinationEngine
from .frontier_release import FrontierReleaseRoom
from .mission_os import MissionOS
from .node_runtime import SovereignNodeRuntime
from .proof_run import run_proof_run_001
from .models import canonical_hash, utc_now


CAPABILITY_MAP: list[dict[str, str]] = [
    {"capability": "Homepage proof-governed operating regime", "website": "public/index.html", "code": "src/goalos_ascension/mission_os.py", "test": "tests/test_mission_os.py"},
    {"capability": "Interactive Proof Console", "website": "public/console.html", "code": "src/goalos_ascension/kernel.py", "test": "tests/test_mission_os.py"},
    {"capability": "Frontier Release Room", "website": "public/frontier-release-room.html", "code": "src/goalos_ascension/frontier_release.py", "test": "tests/test_frontier_release.py"},
    {"capability": "META-Agentic Institution Foundry", "website": "public/meta-agentic-alpha-agi.html", "code": "src/goalos_ascension/agent_foundry.py", "test": "tests/test_agent_foundry.py"},
    {"capability": "AGI Alpha Node v0 Theatre", "website": "public/agi-alpha-node-v0.html", "code": "src/goalos_ascension/node_runtime.py", "test": "tests/test_node_runtime.py"},
    {"capability": "AGI Jobs v0/v2 Work OS", "website": "public/agi-jobs-v0-v2.html", "code": "src/goalos_ascension/agi_jobs.py", "test": "tests/test_agi_jobs.py"},
    {"capability": "Research Spine", "website": "public/research-spine.html", "code": "src/goalos_ascension/aep001.py", "test": "tests/test_aep001_conformance.py"},
    {"capability": "Proof Run 001", "website": "public/proof-run-001.html", "code": "src/goalos_ascension/proof_run.py", "test": "tests/test_proof_run_001.py"},
    {"capability": "$AGIALPHA Proof Control Rail", "website": "public/agialpha-control-rail.html", "code": "src/goalos_ascension/agi_jobs.py", "test": "tests/test_agi_jobs.py"},
    {"capability": "Multi-Agent Institution", "website": "public/multi-agent-institution.html", "code": "src/goalos_ascension/coordination.py", "test": "tests/test_coordination.py"},
    {"capability": "Coordination Console", "website": "public/coordination-console.html", "code": "src/goalos_ascension/coordination.py", "test": "tests/test_coordination.py"},
    {"capability": "AEP-001 Evidence Docket 6.1", "website": "public/proof-of-evolution.html", "code": "src/goalos_ascension/aep001.py", "test": "tests/test_aep001_conformance.py"},
    {"capability": "Document Series", "website": "public/document-series.html", "code": "docs/series/00_SERIES_INDEX.md", "test": "reports/document-series-manifest.json"},
    {"capability": "Launch Narrative", "website": "public/launch-narrative.html", "code": "docs/communications/LAUNCH_NARRATIVE.md", "test": "reports/goalos-latest-website-qa.json"},
    {"capability": "Validator Seats", "website": "public/validator-seats.html", "code": "docs/validators/VALIDATOR_SEAT_INVITATION.md", "test": "issue-bodies/validator-seat-001.md"},
    {"capability": "Proof Mission Slots", "website": "public/proof-mission-slots.html", "code": "docs/proof-runs/PROOF_RUN_001_DOCKET_STRUCTURE.md", "test": "issue-bodies/proof-mission-slots.md"},
    {"capability": "Falsification Box", "website": "public/falsification-box.html", "code": "docs/metrics/PUBLIC_PROOF_METRICS.md", "test": "issue-bodies/proof-run-001-falsification-box.md"},
    {"capability": "Capability Parity Page", "website": "public/capability-parity.html", "code": "src/goalos_ascension/parity.py", "test": "reports/capability-parity-audit.json"},
]


def path_status(root: Path, relative: str) -> bool:
    return (root / relative).exists()


def probe_reference_implementations() -> dict[str, Any]:
    mission = MissionOS().run_until_done("Website-code parity probe", "website-code-parity-v3")
    frontier = FrontierReleaseRoom().review("frontier release room parity", ["public_sources", "access_matrix", "rollback_protocol", "human_authority"])
    foundry = MetaAgenticFoundry().select("Design a proof-governed institution for autonomous AI work")
    node = SovereignNodeRuntime().review_mission("Produce a human-review-ready Evidence Docket")
    jobs = AGIJobsLedger().run_lifecycle("Proof-gated autonomous work demo")
    coordination = CoordinationEngine().route()
    return {
        "mission_os_done": bool(mission.get("done")),
        "frontier_release_human_review_required": frontier.human_review_required,
        "foundry_candidates": foundry["candidate_count"],
        "node_external_actions": node.external_actions,
        "agi_jobs_settlement_simulated": jobs.settlement.get("mainnet") is False and jobs.settlement.get("user_funds") is False,
        "coordination_route_family": coordination.route_family,
        "production_authority": False,
        "external_actions_authorized": False,
        "human_review_required": True,
    }


def audit(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    rows = []
    for item in CAPABILITY_MAP:
        row = dict(item)
        row["website_exists"] = path_status(root, item["website"])
        row["implementation_exists"] = path_status(root, item["code"])
        row["test_or_report_exists"] = path_status(root, item["test"])
        row["covered"] = row["website_exists"] and row["implementation_exists"] and row["test_or_report_exists"]
        rows.append(row)
    probes = probe_reference_implementations()
    missing = [r for r in rows if not r["covered"]]
    boundary_ok = probes["production_authority"] is False and probes["external_actions_authorized"] is False and probes["human_review_required"] is True
    report = {
        "schema": "goalos.website_code_parity.v3",
        "generated_at": utc_now(),
        "status": "passed" if not missing and boundary_ok else "needs_revision",
        "capabilities_checked": len(rows),
        "capabilities_covered": sum(1 for r in rows if r["covered"]),
        "missing": missing,
        "capability_matrix": rows,
        "reference_probes": probes,
        "boundary": {"production_authority": False, "external_actions_authorized": False, "wallet_or_mainnet": False, "human_review_required": True},
        "report_hash": canonical_hash({"rows": rows, "probes": probes}),
    }
    return report
