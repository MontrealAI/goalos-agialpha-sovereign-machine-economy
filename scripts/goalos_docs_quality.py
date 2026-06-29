#!/usr/bin/env python3
"""Deterministic documentation quality checks for GoalOS public-alpha docs."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED_DOCS=[
'README.md','docs/README.md','docs/INDEX.md','docs/START_HERE.md','docs/NON_TECHNICAL_GUIDE.md','docs/REVIEWER_GUIDE.md','docs/DEVELOPER_GUIDE.md','docs/ARCHITECTURE.md','docs/REPOSITORY_MAP.md','docs/PROOF_RUN_001.md','docs/PROOF_LEDGER.md','docs/DEMO_ECOSYSTEM.md','docs/MISSION_FORGE.md','docs/EXTERNAL_REVIEW.md','docs/REPLAY.md','docs/CLAIM_BOUNDARY.md','docs/NO_DATA_NO_FUNDS.md','docs/TOKEN_BOUNDARY.md','docs/ROADMAP.md','docs/RELEASE_CHECKLIST.md','docs/PROOF_RUN_001_RELEASE_CHECKLIST.md','docs/GLOSSARY.md','docs/FAQ.md','docs/CHANGELOG_GUIDE.md','docs/REPOSITORY_SETTINGS.md']
BOUNDARY_PHRASES=['No user data','No user funds','No wallet','No transaction','Human review required','public-alpha','public contract identification only','not available from us']
FORBIDDEN=[r'\bsend funds\b',r'\bconnect wallet\b',r'\bsubmit private key\b',r'\bguaranteed return\b',r'\bachieved AGI\b',r'\bachieved ASI\b',r'\bempirical SOTA\b']
NEGATION_HINTS=('no ','not ','do not ','does not ','avoid ','without ','rather than ','not claim ','not claiming ')
LOCAL_LINK=re.compile(r'\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)')
PUBLIC_LINK=re.compile(r'https://montrealai\.github\.io/goalos-agialpha-sovereign-machine-economy/([^\s)"<>]+)')
issues=[]
def add(kind,path,msg): issues.append({'kind':kind,'path':str(path),'message':msg})
for rel in REQUIRED_DOCS:
 if not (ROOT/rel).exists(): add('missing_required_doc',rel,'Required documentation file is missing')
mds=[ROOT/'README.md']+sorted((ROOT/'docs').glob('*.md'))
combined='\n'.join(p.read_text(errors='ignore') for p in mds if p.exists())
for phrase in BOUNDARY_PHRASES:
 if phrase not in combined: add('missing_boundary_phrase','README.md/docs',f'Missing boundary phrase: {phrase}')
for p in mds:
 if not p.exists(): continue
 text=p.read_text(errors='ignore')
 for pat in FORBIDDEN:
  for m in re.finditer(pat,text,flags=re.I):
   before=text[max(0,m.start()-40):m.start()].lower()
   if any(h in before for h in NEGATION_HINTS):
    continue
   add('forbidden_phrase',p.relative_to(ROOT),f'Forbidden or unsafe phrase: {m.group(0)}')
 for m in LOCAL_LINK.finditer(text):
  target=m.group(1).split('#',1)[0]
  if not target or target.startswith(('tel:','javascript:')): continue
  if target.startswith('/'):
   candidate=ROOT/target.lstrip('/')
  else:
   candidate=(p.parent/target).resolve()
  if not candidate.exists(): add('broken_local_link',p.relative_to(ROOT),f'Broken local link: {m.group(1)}')
 for m in PUBLIC_LINK.finditer(text):
  page=m.group(1).split('#',1)[0]
  if page and not (ROOT/'public'/page).exists(): add('broken_public_page_reference',p.relative_to(ROOT),f'Referenced public page missing: {page}')
report={'status':'pass' if not issues else 'fail','checked_files':[str(p.relative_to(ROOT)) for p in mds if p.exists()],'required_docs':REQUIRED_DOCS,'issues':issues,'boundary_phrases':BOUNDARY_PHRASES,'forbidden_patterns':FORBIDDEN}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/docs-quality.json').write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
sys.exit(0 if not issues else 1)
