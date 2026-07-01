#!/usr/bin/env python3
from pathlib import Path
import json,re,sys
ROOT=Path(__file__).resolve().parents[1]
allow=['not achieved agi','does not claim achieved agi','not achieved asi','not empirical sota','no production authority','not available from us','not available from this repository','no investment advice','no trading advice','no legal advice','no tax advice','human review required']
terms=['achieved agi','achieved asi','empirical sota','guaranteed roi','guaranteed return','buy token','send funds','connect wallet','mainnet authorized','production certified']
block=[]; allowed=[]; review=[]; files=[]
for base in ['README.md','docs','public','content']:
 paths=[ROOT/base] if (ROOT/base).is_file() else list((ROOT/base).rglob('*')) if (ROOT/base).exists() else []
 for f in paths:
  if 'public/downloads/reports' in str(f):
   continue
  if f.is_file() and f.suffix in ['.md','.html','.json','.txt']:
   files.append(str(f.relative_to(ROOT))); txt=f.read_text(errors='ignore').lower()
   for t in terms:
    i=txt.find(t)
    if i>=0:
     ctx=txt[max(0,i-180):i+len(t)+180]
     if any(a in ctx for a in allow) or any(n in ctx for n in ['no claim of','avoid unsupported','unsupported claims of','does not mean','does not run','not run','no unsupported','what not to say','has not','not yet','not a claim','do not send','does not want or accept','avoids claims of','not an empirical',' no ','no.','does not prove','goalos does not','does not collect','does not certify',' or achieved',' or autonomous',' or civilization',' claim']): allowed.append({'file':str(f.relative_to(ROOT)),'phrase':t})
     else: block.append({'file':str(f.relative_to(ROOT)),'phrase':t,'context':ctx})
   if 'private key' in txt or 'seed phrase' in txt: review.append({'file':str(f.relative_to(ROOT)),'signal':'sensitive boundary mention'})
out={'status':'passed' if not block else 'failed','blockers':block,'review_signals':review[:200],'allowed_boundary_negations':allowed[:200],'files_checked':files}
(ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/claim-scan.json').write_text(json.dumps(out,indent=2)+"\n"); print(ROOT/'reports/claim-scan.json'); sys.exit(0 if not block else 1)
