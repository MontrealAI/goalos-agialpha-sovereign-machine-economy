#!/usr/bin/env python3
from goalos_common_quality import ROOT, write_report
import re, sys
issues=[]; checked=[]
for f in sorted((ROOT/'.github/workflows').glob('*')):
 if not f.is_file(): continue
 txt=f.read_text(errors='ignore'); checked.append(str(f.relative_to(ROOT)))
 if len(txt)>60000 or re.search(r'[A-Za-z0-9+/]{21000,}={0,2}',txt): issues.append({'file':checked[-1],'issue':'possible giant inline payload; use .goalos/packs/*.zip'})
 if re.search(r'permissions:\s*\n(?:\s+\w+:\s*write\s*\n){3,}',txt): issues.append({'file':checked[-1],'issue':'broad write permissions review recommended'})
 if any(x in txt.lower() for x in ['connect wallet','private key','seed phrase','send funds','airdrop','market-making']): issues.append({'file':checked[-1],'issue':'token/wallet/funds language not allowed in workflows'})
out={'status':'passed' if not issues else 'failed','checked_workflows':checked,'issue_count':len(issues),'issues':issues,'pack_files':[str(p.relative_to(ROOT)) for p in (ROOT/'.goalos/packs').glob('*.zip')] if (ROOT/'.goalos/packs').exists() else []}
write_report('workflow-quality.json',out); sys.exit(0 if not issues else 1)
