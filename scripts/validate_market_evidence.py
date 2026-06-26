from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from goalos_ascension.evidence import load_json_files, summarize_evidence

REPORT = ROOT / "reports" / "evidence-maturity-score.json"
PATTERNS = [
    "evidence/market/*.json", "evidence/pilots/*.json", "evidence/benchmarks/*.json",
    "evidence/commercial/*.json", "evidence/validation/*.json", "evidence/fair-value/*.json",
    "evidence/strategic-scale/*.json",
]
REQUIRED_KEYS = {"id", "artifact_type", "category", "evidence_status", "summary", "created_at", "public_claim_permission"}
ALLOWED_STATUS = {"example_placeholder", "operator_attested", "source_verifiable", "third_party_verified"}


def main() -> int:
    items = load_json_files(ROOT, PATTERNS)
    errors = []
    for item in items:
        missing = sorted(REQUIRED_KEYS - item.keys())
        if missing:
            errors.append({"path": item.get("_path"), "missing": missing})
        if item.get("evidence_status") not in ALLOWED_STATUS:
            errors.append({"path": item.get("_path"), "invalid_status": item.get("evidence_status")})
        if item.get("evidence_status") == "example_placeholder" and item.get("public_claim_permission") != "not_allowed":
            errors.append({"path": item.get("_path"), "error": "placeholder evidence cannot permit public claims"})
    summary = summarize_evidence(items)
    payload = {
        "status": "pass" if not errors else "fail",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_state": summary.state,
        "public_scale_claim_allowed": summary.public_scale_claim_allowed,
        "total_items": summary.total_items,
        "counted_items": summary.counted_items,
        "verified_items": summary.verified_items,
        "placeholder_items": summary.placeholder_items,
        "verified_categories_present": summary.categories_present,
        "required_categories_missing": summary.required_categories_missing,
        "errors": errors,
        "note": "Examples and templates are intentionally excluded from counted market evidence.",
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
