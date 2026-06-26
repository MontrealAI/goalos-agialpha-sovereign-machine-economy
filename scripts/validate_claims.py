from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "claim-scan.json"
BLOCKED_PATTERNS = [
    r"achieved\s+agi",
    r"achieved\s+asi",
    r"guaranteed\s+returns?",
    r"guaranteed\s+profits?",
    r"risk[- ]free",
    r"external\s+audit\s+completed",
    r"production\s+authorized",
    r"production\s+activated:\s+yes",
    r"user[- ]fund\s+authorization:\s+yes",
    r"legal\s+approval:\s+yes",
    r"tax\s+approval:\s+yes",
    r"autonomous\s+legal\s+sovereignty\s+achieved",
    r"deca" + r"corn",
    r"mega" + r"corn",
]
ALLOW_FILES = {
    "CLAIMS.md",
    "docs/CLAIM_BOUNDARY.md",
    "scripts/validate_repo.py",
    "scripts/validate_claims.py",
    "src/goalos_ascension/kernel.py",
    "tests/test_kernel.py",
}
NEGATION_HINTS = (
    "does not claim", "does **not** claim", "do not claim", "must not claim", "not a claim",
    "no claim of", "without claiming", "unsupported claims of", "forbidden", "prohibited",
    "restricted", "non_goals", "does not imply", "not imply", "should not be represented as",
)
SCAN_SUFFIXES = {".md", ".json", ".html", ".py", ".yml", ".yaml"}


def negated(text: str, start: int) -> bool:
    window = text[max(0, start - 240): start + 140]
    return any(hint in window for hint in NEGATION_HINTS)


def main() -> int:
    findings: list[dict[str, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if rel in ALLOW_FILES or rel.startswith("reports/") or "__pycache__" in rel or "/.git/" in rel:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for pattern in BLOCKED_PATTERNS:
            for match in re.finditer(pattern, text):
                if negated(text, match.start()):
                    continue
                findings.append({"path": rel, "pattern": pattern})
    REPORT.parent.mkdir(exist_ok=True)
    payload = {
        "status": "pass" if not findings else "review",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "findings": findings,
        "note": "This scan is a guardrail, not a legal review or security audit.",
    }
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if findings:
        print(json.dumps(payload, indent=2))
        return 1
    print(f"Claim scan passed. Report: {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
