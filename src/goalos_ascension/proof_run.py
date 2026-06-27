from __future__ import annotations

from pathlib import Path
from typing import Any
import json

from .aep001 import build_reference_commit, build_reference_run
from .coordination import CoordinationEngine
from .frontier_release import FrontierReleaseRoom
from .mission_os import MissionOS
from .models import canonical_hash, utc_now


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_proof_run_001(output_dir: Path | str = "evidence/proof-run-001") -> dict[str, Any]:
    output_dir = Path(output_dir)
    mission = MissionOS().run_until_done(
        "Verify that the GoalOS repository can produce a public-alpha Evidence Docket, governed decision state, simulated settlement receipt, Chronicle entry, and reusable capability package.",
        "proof-run-001",
    )
    frontier = FrontierReleaseRoom().review("public-source frontier release review", ["public_sources", "access_matrix", "rollback_protocol", "human_authority"])
    coordination = CoordinationEngine().route()
    aep = build_reference_run(build_reference_commit("Proof Run 001 public-alpha implementation parity"))
    docket = {
        "id": "proof-run-001-genesis-docket",
        "created_at": utc_now(),
        "mission_os": mission,
        "frontier_release_review": frontier.to_dict(),
        "coordination_result": coordination.to_dict(),
        "aep001_reference": aep,
        "capability_claim": "public-alpha reference implementation parity",
        "claim_boundary": [
            "not achieved AGI", "not achieved ASI", "not empirical SOTA", "not production authorization",
            "not legal approval", "not user-fund authorization", "not mainnet activation", "not guaranteed outcomes",
        ],
        "replay": {"command": "python scripts/run_proof_run_001.py", "network_required": False, "external_actions": 0},
    }
    report = {
        "status": "passed" if mission["done"] and coordination.evidence_bundle_hash and frontier.human_review_required else "needs_revision",
        "generated_at": utc_now(),
        "docket_hash": canonical_hash(docket),
        "human_review_required": True,
        "production_authority": False,
        "external_actions_authorized": False,
        "next_required_step": "independent reviewer replay and validator report",
    }
    write_json(output_dir / "proof-run-001-docket.json", docket)
    write_json(output_dir / "proof-run-001-report.json", report)
    write_json(Path("reports/proof-run-001-reference-report.json"), report)
    return {"docket": docket, "report": report}
