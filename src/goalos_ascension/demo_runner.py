
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

BOUNDARY = {
    "no_user_data": True,
    "no_user_funds": True,
    "no_wallet": True,
    "no_transaction": True,
    "no_network_call": True,
    "no_production_authority": True,
    "human_review_required": True,
}
GATES = ["Mission Contract", "Claims Matrix", "Allowed Sources", "Tool Boundary", "Evidence Docket", "Validator Report", "Risk Ledger", "Governed Decision", "Chronicle", "Capability Package"]
SCENARIOS = {
    "launch": ("Repository launch readiness", 91, "low"),
    "frontier": ("Frontier release governance review", 84, "high"),
    "pilot": ("Public-safe proof mission pilot", 88, "medium"),
    "coordination": ("Multi-agent coordination check", 86, "medium"),
}
@dataclass
class DemoDocket:
    schema: str
    generated_at: str
    scenario: str
    readiness_score: int
    risk_class: str
    proof_gates: list[dict]
    boundary: dict
    claim_boundary: list[str]
    chain_head: str

def make_demo_docket(kind: str = "launch") -> DemoDocket:
    title, score, risk = SCENARIOS.get(kind, SCENARIOS["launch"])
    stamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = f"{kind}:{title}:{score}:{stamp}"
    head = "DEMO-" + hashlib.sha256(payload.encode()).hexdigest()[:16]
    return DemoDocket(
        schema="goalos.autonomous_demo_docket.v4",
        generated_at=stamp,
        scenario=title,
        readiness_score=score,
        risk_class=risk,
        proof_gates=[{"gate": i + 1, "name": name, "status": "passed" if i < 8 else "review-ready"} for i, name in enumerate(GATES)],
        boundary=BOUNDARY,
        claim_boundary=["public-alpha reference demo", "not achieved AGI/ASI", "not empirical SOTA", "not production authorization"],
        chain_head=head,
    )

def build_demo_pack() -> dict:
    dockets = {k: asdict(make_demo_docket(k)) for k in SCENARIOS}
    return {"schema": "goalos.autonomous_demo_pack.v4", "dockets": dockets, "boundary": BOUNDARY, "external_actions": 0}

def write_demo_pack(out: str | Path = "evidence/demo/autonomous-demo-pack.json") -> dict:
    out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
    pack = build_demo_pack()
    out.write_text(json.dumps(pack, indent=2) + "\n")
    Path("reports").mkdir(exist_ok=True)
    Path("reports/autonomous-demo-run-report.json").write_text(json.dumps({"status": "passed", "dockets": len(pack["dockets"]), "boundary": BOUNDARY}, indent=2) + "\n")
    return pack
