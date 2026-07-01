#!/usr/bin/env python3
from goalos_common_quality import ROOT, CONFIRMATION, registry, write_report
import sys
required=['docs/START_HERE.md','docs/NON_TECHNICAL_GUIDE.md','docs/REVIEWER_GUIDE.md','docs/VALIDATOR_GUIDE.md','docs/DEVELOPER_GUIDE.md','docs/ARCHITECTURE.md','docs/WEBSITE_MAP.md','docs/REPOSITORY_MAP.md','docs/DEMO_ECOSYSTEM.md','docs/LOOP_TO_RSI_JOURNEY.md','docs/RSI_GOVERNANCE.md','docs/PROOF_RUN_001.md','docs/PROOF_LEDGER.md','docs/MISSION_FORGE.md','docs/MISSION_CONTROL.md','docs/EXTERNAL_REVIEW.md','docs/REPLAY.md','docs/CLAIM_BOUNDARY.md','docs/NO_DATA_NO_FUNDS.md','docs/TOKEN_BOUNDARY.md','docs/ROADMAP.md','docs/RELEASE_CHECKLIST.md','docs/PROOF_RUN_001_RELEASE_CHECKLIST.md','docs/GLOSSARY.md','docs/FAQ.md','docs/REPOSITORY_SETTINGS.md','docs/CHANGELOG_GUIDE.md','docs/WEBSITE_QUALITY_STANDARD.md','docs/PUBLIC_DOWNLOADS.md']
sections=['## Start in 60 seconds','## What this is','## What this is not','## Core doctrine','## Choose your path','## Claim boundary']
missing=[p for p in required if not (ROOT/p).exists()]
readme=(ROOT/'README.md').read_text(errors='ignore')
missing_sections=[s for s in sections if s not in readme]
issue_missing=[str(p.relative_to(ROOT)) for p in (ROOT/'.github/ISSUE_TEMPLATE').glob('*.yml') if CONFIRMATION not in p.read_text(errors='ignore')]
mermaids=list((ROOT/'docs/diagrams').glob('*.mmd')) if (ROOT/'docs/diagrams').exists() else []
reg=registry()
issues=missing+missing_sections+issue_missing+([] if len(mermaids)>=16 else ['missing required Mermaid diagrams'])+([] if reg else ['registry missing routes/demos'])
out={'status':'passed' if not issues else 'failed','missing_files':missing,'missing_readme_sections':missing_sections,'issue_templates_missing_confirmation':issue_missing,'mermaid_count':len(mermaids),'registry_entries':len(reg),'issues':issues}
write_report('docs-quality.json',out); sys.exit(0 if not issues else 1)
