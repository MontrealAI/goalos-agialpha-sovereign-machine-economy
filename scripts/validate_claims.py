from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "claim-scan.json"
SCAN_SUFFIXES = {".md", ".json", ".html", ".py", ".yml", ".yaml"}

BLOCKERS = [
    r"achieved\s+agi\b",
    r"achieved\s+asi\b",
    r"empirical\s+sota\b",
    r"guaranteed\s+(?:return|returns|roi|profit|profits|yield)\b",
    r"\bbuy\s+\$?agialpha\b",
    r"\bsend\s+funds\b",
    r"\bconnect\s+(?:your\s+)?wallet\b",
    r"\bprivate\s+key\b",
    r"\bseed\s+phrase\b",
    r"production\s+authorized\s*:\s*yes",
    r"mainnet\s+authorized\s*:\s*yes",
    r"user[-\s]?fund\s+authorization\s*:\s*yes",
    r"legal\s+approval\s*:\s*yes",
    r"tax\s+approval\s*:\s*yes",
]

REVIEW_SIGNALS = [
    r"decacorn",
    r"hectocorn",
    r"megacorn",
    r"investment\s+opportunity",
    r"safety\s+certified",
    r"production\s+certified",
    r"audited\s+final",
]

NEGATION_HINTS = (
    "does not claim", "do not claim", "do not submit", "doesn't claim", "not claim", "not achieved", "not empirical", "no achieved",
    "not production", "not available", "not a sale", "no sale", "no custody", "no wallet", "no transaction",
    "no investment", "no trading", "no legal", "no tax", "no guaranteed", "claim boundary", "public-alpha", "unsupported",
    "prohibited", "forbidden", "must not", "should not", "without claiming", "does not imply", "not imply", "what not to say", "not_claimed", "blocked_phrases", "blocked phrases", "avoids claims", "avoid claims",
)

ALLOW_PATH_PARTS = {"reports", ".git", "__pycache__"}


def boundary_negated(text: str, start: int) -> bool:
    window = text[max(0, start - 520): min(len(text), start + 240)].lower()
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", start)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].lower()
    line_hints = (
        "does not", "do not", "not ", " no ", "without", "claim boundary", "boundary",
        "human review", "human authority", "not available", "not a sale", "not a claim", "avoid claims", "avoids claims", "avoid claim", "what not to say", "do not say", "not to say", "not_claimed", "blocked_phrases", "blocked phrases"
    )
    return any(h in window for h in NEGATION_HINTS) or any(h in line for h in line_hints)


def should_skip(path: Path) -> bool:
    rel_parts = set(path.relative_to(ROOT).parts)
    return bool(rel_parts & ALLOW_PATH_PARTS)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on review signals as well as blockers.")
    args = parser.parse_args()
    blockers = []
    reviews = []
    allowed_negations = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES or should_skip(path):
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        lower = text.lower()
        for pattern in BLOCKERS:
            for m in re.finditer(pattern, lower):
                if boundary_negated(lower, m.start()):
                    allowed_negations.append({"path": rel, "pattern": pattern, "context": lower[max(0, m.start()-60):m.end()+60]})
                else:
                    blockers.append({"path": rel, "pattern": pattern, "context": lower[max(0, m.start()-80):m.end()+80]})
        for pattern in REVIEW_SIGNALS:
            for m in re.finditer(pattern, lower):
                if boundary_negated(lower, m.start()):
                    allowed_negations.append({"path": rel, "pattern": pattern, "context": lower[max(0, m.start()-60):m.end()+60]})
                else:
                    reviews.append({"path": rel, "pattern": pattern, "context": lower[max(0, m.start()-80):m.end()+80]})
    status = "passed" if not blockers and (not reviews or not args.strict) else "failed"
    payload = {
        "status": status,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "mode": "strict" if args.strict else "review-signal-nonblocking",
        "blockers": blockers,
        "review_signals": reviews,
        "allowed_boundary_negations": allowed_negations[:200],
        "note": "Context-aware claim scan. This is a public-alpha guardrail, not legal review, tax advice, investment advice, security certification, or production authorization.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    if blockers or (args.strict and reviews):
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
