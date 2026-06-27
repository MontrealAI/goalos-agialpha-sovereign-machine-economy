from __future__ import annotations

from pathlib import Path
from typing import Any
import json

CAPABILITY_MATRIX = [
    {"capability": "Mission Contracts", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Proof Jobs", "code": "src/goalos_ascension/kernel.py", "test": "tests/test_mission_os.py"},
    {"capability": "Tool Traces", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Evidence Dockets", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Validator Reports", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Governed Decision States", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Settlement Receipts", "code": "src/goalos_ascension/kernel.py", "test": "tests/test_mission_os.py"},
    {"capability": "Chronicle Memory", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "Capability Packages", "code": "src/goalos_ascension/models.py", "test": "tests/test_mission_os.py"},
    {"capability": "AEP-001 Object Model", "code": "src/goalos_ascension/aep001.py", "test": "tests/test_aep001_conformance.py"},
    {"capability": "Proof Gradient", "code": "src/goalos_ascension/aep001.py", "test": "tests/test_aep001_conformance.py"},
    {"capability": "Evidence Docket 6.1", "code": "src/goalos_ascension/aep001.py", "test": "tests/test_aep001_conformance.py"},
    {"capability": "Mission OS until-DONE", "code": "src/goalos_ascension/mission_os.py", "test": "tests/test_mission_os.py"},
    {"capability": "Frontier Release Room", "code": "src/goalos_ascension/frontier_release.py", "test": "tests/test_frontier_release.py"},
    {"capability": "Multi-Agent Institution", "code": "src/goalos_ascension/coordination.py", "test": "tests/test_coordination.py"},
    {"capability": "Proof Run 001", "code": "src/goalos_ascension/proof_run.py", "test": "tests/test_proof_run_001.py"},
    {"capability": "Capability Parity Audit", "code": "src/goalos_ascension/parity.py", "test": "tests/test_capability_parity.py"},
    {"capability": "Public Parity Page", "code": "public/capability-parity.html", "test": "tests/test_capability_parity.py"},
]


def audit(root: Path | str = ".") -> dict[str, Any]:
    root = Path(root)
    items = []
    for row in CAPABILITY_MATRIX:
        code_exists = (root / row["code"]).exists()
        test_exists = (root / row["test"]).exists()
        items.append({**row, "code_exists": code_exists, "test_exists": test_exists, "covered": code_exists and test_exists})
    missing = [i for i in items if not i["covered"]]
    status = "passed" if not missing else "needs_revision"
    report = {
        "status": status,
        "capabilities_checked": len(items),
        "capabilities_covered": len(items) - len(missing),
        "missing": missing,
        "boundary": {
            "production_authority": False,
            "external_actions_authorized": False,
            "wallet_or_mainnet": False,
            "human_review_required": True,
        },
        "capability_matrix": items,
    }
    out = root / "reports/capability-parity-audit.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
