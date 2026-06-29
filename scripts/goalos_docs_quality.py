#!/usr/bin/env python3
"""Deterministic documentation quality checks for GoalOS public-alpha docs.

The checker is intentionally local-only: it validates repository files, local links,
required boundary language, required diagrams, public page references, and public-safe
GitHub templates without fetching the network or requiring secrets.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DOCS = [
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "PRIVACY.md",
    "DATA_BOUNDARY.md",
    "DISCLAIMER.md",
    "TOKEN_BOUNDARY.md",
    "docs/README.md",
    "docs/INDEX.md",
    "docs/START_HERE.md",
    "docs/NON_TECHNICAL_GUIDE.md",
    "docs/REVIEWER_GUIDE.md",
    "docs/DEVELOPER_GUIDE.md",
    "docs/ARCHITECTURE.md",
    "docs/REPOSITORY_MAP.md",
    "docs/PROOF_RUN_001.md",
    "docs/PROOF_LEDGER.md",
    "docs/DEMO_ECOSYSTEM.md",
    "docs/MISSION_FORGE.md",
    "docs/EXTERNAL_REVIEW.md",
    "docs/REPLAY.md",
    "docs/CLAIM_BOUNDARY.md",
    "docs/NO_DATA_NO_FUNDS.md",
    "docs/TOKEN_BOUNDARY.md",
    "docs/ROADMAP.md",
    "docs/RELEASE_CHECKLIST.md",
    "docs/PROOF_RUN_001_RELEASE_CHECKLIST.md",
    "docs/GLOSSARY.md",
    "docs/FAQ.md",
    "docs/CHANGELOG_GUIDE.md",
    "docs/REPOSITORY_SETTINGS.md",
]

REQUIRED_DIAGRAMS = [
    "docs/diagrams/goalos-core-loop.mmd",
    "docs/diagrams/aep-object-lifecycle.mmd",
    "docs/diagrams/evidence-docket-flow.mmd",
    "docs/diagrams/public-private-proof-boundary.mmd",
    "docs/diagrams/website-user-journey.mmd",
    "docs/diagrams/developer-local-run.mmd",
    "docs/diagrams/reviewer-path.mmd",
    "docs/diagrams/token-boundary.mmd",
]

REQUIRED_TEMPLATES = [
    ".github/ISSUE_TEMPLATE/new_user_question.yml",
    ".github/ISSUE_TEMPLATE/documentation_feedback.yml",
    ".github/ISSUE_TEMPLATE/demo_bug_report.yml",
    ".github/ISSUE_TEMPLATE/evidence_docket_review.yml",
    ".github/ISSUE_TEMPLATE/external_reviewer_report.yml",
    ".github/ISSUE_TEMPLATE/proof_mission_proposal.yml",
    ".github/ISSUE_TEMPLATE/security_boundary_report.yml",
    ".github/ISSUE_TEMPLATE/token_or_market_boundary.yml",
    ".github/pull_request_template.md",
    ".github/workflows/goalos-docs-quality.yml",
]

BOUNDARY_PHRASES = [
    "No user data",
    "No user funds",
    "No wallet",
    "No transaction",
    "Human review required",
    "public-alpha",
    "public contract identification only",
    "not available from us",
]


README_REQUIRED_PHRASES = [
    "Visit the Website",
    "30-second explanation",
    "3-minute explanation",
    "What this repository is / is not",
    "What users can do right now",
    "What reviewers can inspect",
    "What developers can run locally",
    "Repository map",
    "Public demo journey",
    "Evidence and reports",
    "How to propose a proof mission",
    "How to review or challenge a docket",
    "How to run locally",
    "How to contribute safely",
    "Claim boundary",
    "Legal / privacy / token boundary",
    "Citation / research canon",
    "Release / roadmap",
    "Maintainer checklist",
]

REQUIRED_PUBLIC_PAGES = [
    "index.html",
    "start-here.html",
    "website-operating-system.html",
    "demo-ecosystem-registry.html",
    "proof-experience-atlas.html",
    "proof-ledger.html",
    "proof-run-001-docket.html",
    "external-reviewer-replay-room.html",
    "proof-mission-forge.html",
    "proof-mission-control.html",
    "no-data-no-funds.html",
    "agialpha-token-boundary.html",
]

WORKFLOW_FORBIDDEN = [
    r"secrets\.",
    r"window\.ethereum",
    r"private[-_ ]?key",
    r"auto[-_ ]?merge",
    r"git push",
]

TEMPLATE_CONFIRMATION = (
    "I am not submitting personal data, customer data, confidential data, regulated data, "
    "credentials, wallet information, private keys, seed phrases, payment information, "
    "trade secrets, or user funds."
)

FORBIDDEN = [
    r"\bsend funds\b",
    r"\bconnect wallet\b",
    r"\bsubmit private key\b",
    r"\bguaranteed return\b",
    r"\bachieved AGI\b",
    r"\bachieved ASI\b",
    r"\bempirical SOTA\b",
    r"\bavailable from (this repository|the repository|us|maintainers)\b",
]

NEGATION_HINTS = (
    "no ",
    "not ",
    "do not ",
    "does not ",
    "avoid ",
    "without ",
    "rather than ",
    "not claim ",
    "not claiming ",
    "is not ",
)

LOCAL_LINK = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
PUBLIC_LINK = re.compile(
    r"https://montrealai\.github\.io/goalos-agialpha-sovereign-machine-economy/([^\s)\"<>]+)"
)

issues: list[dict[str, str]] = []


def add(kind: str, path: str | Path, message: str) -> None:
    issues.append({"kind": kind, "path": str(path), "message": message})


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


for rel in REQUIRED_DOCS + REQUIRED_DIAGRAMS + REQUIRED_TEMPLATES:
    if not (ROOT / rel).exists():
        add("missing_required_file", rel, "Required public-alpha repository file is missing")

markdown_files = [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md"))
# Keep the acceptance-scope check intentionally focused on README.md and docs/*.md,
# then add publication-critical root policy files so boundary regressions are caught.
markdown_files += [ROOT / name for name in ["CONTRIBUTING.md", "SECURITY.md", "PRIVACY.md", "DATA_BOUNDARY.md", "DISCLAIMER.md", "TOKEN_BOUNDARY.md"]]
markdown_files = [path for path in markdown_files if path.exists()]
combined = "\n".join(read(path) for path in markdown_files)

for phrase in BOUNDARY_PHRASES:
    if phrase not in combined:
        add("missing_boundary_phrase", "README.md/docs", f"Missing boundary phrase: {phrase}")

readme_text = read(ROOT / "README.md") if (ROOT / "README.md").exists() else ""
for phrase in README_REQUIRED_PHRASES:
    if phrase not in readme_text:
        add("missing_readme_front_door_section", "README.md", f"README front door is missing: {phrase}")

for page in REQUIRED_PUBLIC_PAGES:
    if not (ROOT / "public" / page).exists():
        add("missing_public_navigation_page", "public", f"Required public navigation page is missing: {page}")

for path in markdown_files:
    text = read(path)
    rel_path = path.relative_to(ROOT)
    for pattern in FORBIDDEN:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            before = text[max(0, match.start() - 80) : match.start()].lower()
            if any(hint in before for hint in NEGATION_HINTS):
                continue
            add("forbidden_phrase", rel_path, f"Forbidden or unsafe phrase: {match.group(0)}")

    for match in LOCAL_LINK.finditer(text):
        target = match.group(1).split("#", 1)[0]
        if not target or target.startswith(("tel:", "javascript:")):
            continue
        candidate = ROOT / target.lstrip("/") if target.startswith("/") else (path.parent / target).resolve()
        if not candidate.exists():
            add("broken_local_link", rel_path, f"Broken local link: {match.group(1)}")

    for match in PUBLIC_LINK.finditer(text):
        page = match.group(1).split("#", 1)[0].split("?", 1)[0]
        if page and not (ROOT / "public" / page).exists():
            add("broken_public_page_reference", rel_path, f"Referenced public page missing: {page}")

for rel in REQUIRED_TEMPLATES:
    path = ROOT / rel
    if path.exists() and rel.startswith(".github/ISSUE_TEMPLATE/"):
        text = read(path)
        if TEMPLATE_CONFIRMATION not in text:
            add("missing_issue_template_confirmation", rel, "Missing required public-safe data/funds confirmation")

workflow_path = ROOT / ".github/workflows/goalos-docs-quality.yml"
if workflow_path.exists():
    workflow_text = read(workflow_path)
    for required in ["workflow_dispatch", "pull_request", "actions/checkout@v4", "actions/setup-python@v5", "actions/upload-artifact@v4", "python scripts/goalos_docs_quality.py"]:
        if required not in workflow_text:
            add("unsafe_or_incomplete_docs_quality_workflow", workflow_path.relative_to(ROOT), f"Docs quality workflow missing expected safe element: {required}")
    for pattern in WORKFLOW_FORBIDDEN:
        if re.search(pattern, workflow_text, flags=re.IGNORECASE):
            add("unsafe_docs_quality_workflow", workflow_path.relative_to(ROOT), f"Docs quality workflow includes unsafe pattern: {pattern}")

public_html_pages = sorted((ROOT / "public").glob("*.html"))
registry = ROOT / "content/goalos/demo-ecosystem-registry.json"
registry_demo_count = 0
if registry.exists():
    try:
        data = json.loads(read(registry))
        if not isinstance(data.get("demos"), list) or not data["demos"]:
            add("invalid_demo_registry", registry.relative_to(ROOT), "Registry must include a non-empty demos list")
        else:
            registry_demo_count = len(data["demos"])
            registry_paths = {item.get("path") for item in data["demos"] if isinstance(item, dict)}
            missing_from_registry = [str(path.relative_to(ROOT)) for path in public_html_pages if str(path.relative_to(ROOT)) not in registry_paths]
            if missing_from_registry:
                add("incomplete_demo_registry", registry.relative_to(ROOT), "Public HTML pages missing from registry: " + ", ".join(missing_from_registry[:10]))
    except json.JSONDecodeError as exc:
        add("invalid_json", registry.relative_to(ROOT), f"Demo registry JSON is invalid: {exc}")
else:
    add("missing_required_file", registry.relative_to(ROOT), "Machine-readable demo registry is missing")

report = {
    "status": "pass" if not issues else "fail",
    "checked_markdown_files": [str(path.relative_to(ROOT)) for path in markdown_files],
    "public_html_pages_found": len(public_html_pages),
    "demo_registry_entries": registry_demo_count,
    "required_docs": REQUIRED_DOCS,
    "required_diagrams": REQUIRED_DIAGRAMS,
    "required_templates": REQUIRED_TEMPLATES,
    "required_readme_front_door_phrases": README_REQUIRED_PHRASES,
    "required_public_navigation_pages": REQUIRED_PUBLIC_PAGES,
    "boundary_phrases": BOUNDARY_PHRASES,
    "forbidden_patterns": FORBIDDEN,
    "issue_template_confirmation": TEMPLATE_CONFIRMATION,
    "issues": issues,
}

(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/docs-quality.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(0 if not issues else 1)
