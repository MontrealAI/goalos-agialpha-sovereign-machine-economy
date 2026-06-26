from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "reports" / "repo-validation.json"
FORBIDDEN = [
    "guaranteed returns", "guaranteed profit", "achieved AGI", "achieved ASI",
    "production activated: yes", "user-fund authorization: yes", "deca" + "corn", "mega" + "corn",
]
REQUIRED_FILES = [
    "README.md", "START_HERE.md", "LAUNCHPAD.md", "CLAIMS.md", "SECURITY.md", "LICENSE",
    "CREATE_REPOSITORY_WEB_UI_GUIDE.md", "GITHUB_REPOSITORY_SETTINGS.md",
    "content/site_manifest.json", "scripts/build_site.py", "scripts/verify_site.py",
    "scripts/validate_claims.py", "scripts/hash_artifacts.py", "scripts/run_demo_mission.py",
    "docs/EXECUTIVE_INSTITUTIONAL_BRIEF.md", "docs/NON_TECHNICAL_OPERATOR_MANUAL.md",
    "docs/WEBSITE_EDITOR_GUIDE.md", "docs/GITHUB_PAGES_TROUBLESHOOTING.md",
    "docs/INSTITUTIONAL_QUALITY_BAR.md", "docs/TRUST_AND_ASSURANCE_READINESS.md",
    "docs/PRACTICAL_CAPABILITY_MODEL.md", "docs/SOVEREIGN_MACHINE_ECONOMY_MODEL.md",
    "brand/IDENTITY.md", "brand/LAUNCH_COPY.md", "docs/assets/system-map.svg",
    "schemas/mission_contract.schema.json", "schemas/evidence_docket.schema.json", "schemas/validator_report.schema.json",
    "examples/mission-contract.example.json", "examples/evidence-docket.example.json", "examples/settlement-receipt.example.json",
]
JSON_GLOBS = ["schemas/*.json", "examples/*.json", "content/*.json"]
ALLOW_REVIEW_FILES = {
    "CLAIMS.md", "docs/CLAIM_BOUNDARY.md", "scripts/validate_repo.py", "scripts/validate_claims.py",
    "src/goalos_ascension/kernel.py", "tests/test_kernel.py",
}
NEGATION_HINTS = (
    "does not claim", "does **not** claim", "do not claim", "must not claim", "not a claim",
    "no claim of", "without claiming", "unsupported claims of", "do not introduce", "avoid unsupported claims", "forbidden", "prohibited", "restricted language",
    "blocked", "non_goals", "not include", "does not include", "does not imply",
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_context(low_text: str, start: int) -> bool:
    window = low_text[max(0, start - 240): start + 140]
    return any(h in window for h in NEGATION_HINTS)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required file: {rel}")
    json_files: list[Path] = []
    for pattern in JSON_GLOBS:
        json_files.extend(ROOT.glob(pattern))
    for path in json_files:
        try:
            load_json(path)
        except Exception as exc:
            errors.append(f"invalid json: {path.relative_to(ROOT)}: {exc}")
    manifest = load_json(ROOT / "content" / "site_manifest.json")
    pages = manifest.get("pages", [])
    if len(pages) < 30:
        errors.append("manifest should define at least 30 public pages")
    for page in pages:
        for key in ["slug", "nav", "title", "headline", "body", "sections"]:
            if key not in page:
                errors.append(f"manifest page missing {key}: {page}")
        if not page.get("sections"):
            errors.append(f"manifest page has no sections: {page.get('slug')}")
    if len(manifest.get("claim_boundary", "")) < 150:
        errors.append("manifest claim boundary is missing or too short")
    if any(p.name == ".pytest_cache" for p in ROOT.rglob(".pytest_cache")):
        errors.append(".pytest_cache should not be included in the repository kit")
    text_files = [p for p in ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json", ".yml", ".yaml", ".html", ".py"}]
    for path in text_files:
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("reports/") or "__pycache__" in rel or rel in ALLOW_REVIEW_FILES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        low = text.lower()
        for phrase in FORBIDDEN:
            start = low.find(phrase.lower())
            if start >= 0 and not safe_context(low, start):
                warnings.append(f"restricted phrase appears for review: {rel} :: {phrase}")
    REPORT.parent.mkdir(exist_ok=True)
    payload = {
        "status": "pass" if not errors else "fail",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "errors": errors,
        "warnings": warnings,
        "required_files_checked": len(REQUIRED_FILES),
        "json_files_checked": len(json_files),
        "page_count": len(pages),
    }
    REPORT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if errors:
        print(json.dumps(payload, indent=2))
        return 1
    print(f"Repository validation passed. Report: {REPORT.relative_to(ROOT)}")
    if warnings:
        print(f"Warnings: {len(warnings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
