#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
required_docs=['docs/START_HERE.md','docs/NON_TECHNICAL_GUIDE.md','docs/REVIEWER_GUIDE.md','docs/DEVELOPER_GUIDE.md','docs/ARCHITECTURE.md','docs/DEMO_ECOSYSTEM.md','docs/RSI_GOVERNANCE.md','docs/FROM_LOOP_TO_RSI.md','docs/REPOSITORY_SETTINGS.md']
sections=['Start in under 60 seconds','What this is','What this is not','Current release state','Choose your path','Claim boundaries']
missing=[p for p in required_docs if not (ROOT/p).exists()]
readme=(ROOT/'README.md').read_text(errors='ignore')
missing_sections=[s for s in sections if f'## {s}' not in readme]
phrases=['No user data','No user funds','Human review required','not available from this repository']
boundary=[p for p in phrases if p.lower() not in readme.lower()]
reg_ok=True
try:
 data=json.loads((ROOT/'content/goalos/demo-ecosystem-registry.json').read_text()); reg_ok=bool(data.get('routes') or data.get('demos'))
except Exception: reg_ok=False
issue_templates=list((ROOT/'.github/ISSUE_TEMPLATE').glob('*.yml')) if (ROOT/'.github/ISSUE_TEMPLATE').exists() else []
confirmation='I confirm I am not submitting personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.'
template_missing=[str(p.relative_to(ROOT)) for p in issue_templates if confirmation not in p.read_text(errors='ignore')]
allowed=['not achieved agi','does not claim achieved agi','not achieved asi','not empirical sota','not available from us','not available from this repository','no investment advice','no wallet support','no legal advice','no tax advice','human review required']
blocked=[]
for f in [ROOT/'README.md']+list((ROOT/'docs').glob('*.md')):
 txt=f.read_text(errors='ignore').lower()
 for phrase in ['achieved agi','achieved asi','empirical sota','guaranteed return','guaranteed roi','investment opportunity','buy token','send funds','connect wallet','production certified','safety certified','audited final','mainnet authorized','autonomous production remediation']:
  if phrase in txt and not (any(a in txt[max(0,txt.find(phrase)-90):txt.find(phrase)+len(phrase)+90] for a in allowed) or any(n in txt[max(0,txt.find(phrase)-90):txt.find(phrase)+len(phrase)+90] for n in ['no claim of','avoid unsupported','does not mean','does not run','not run','no unsupported'])): blocked.append({'file':str(f.relative_to(ROOT)),'phrase':phrase})
issues=missing+missing_sections+boundary+([] if reg_ok else ['demo registry invalid'])+template_missing+blocked
out={'status':'passed' if not issues else 'failed','checked_files':len(list((ROOT/'docs').glob('*.md')))+1,'missing_files':missing,'missing_sections':missing_sections,'boundary_issues':boundary,'risky_phrases':blocked,'issue_templates_missing_confirmation':template_missing,'recommendations':[] if not issues else ['Resolve listed defects.']}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/docs-quality.json').write_text(json.dumps(out,indent=2)+"\n"); print(ROOT/'reports/docs-quality.json'); sys.exit(0 if not issues else 1)
