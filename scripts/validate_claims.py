#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path.cwd(); SCAN=["README.md","docs","public","content","evidence"]
PATS=["achieved AGI","achieved ASI","empirical SOTA","guaranteed return","guaranteed ROI","investment opportunity","buy token","send funds","connect wallet","available from us","production certified","safety certified","mainnet authorized","autonomous production remediation"]
BOUND=["does not claim","not achieved","not empirical","no investment","no wallet","no transaction","no sale","no custody","not available from","available from us: **no**","available from us: no","claim boundary","boundary","avoid unsupported","unsupported claims","legal advice, financial advice","tax advice, investment advice","or guaranteed roi","guaranteed security","guaranteed returns","legal approval, token settlement","user-fund movement","not legal advice","not financial advice","not tax advice"]
EXT={".md",".html",".json",".txt",".yml",".yaml"}
def iter_files():
 for item in SCAN:
  q=ROOT/item
  if q.is_file(): yield q
  elif q.is_dir():
   for f in q.rglob('*'):
    if f.is_file() and f.suffix.lower() in EXT and 'public/downloads' not in f.as_posix(): yield f
def allowed(txt,start,end):
 ctx=txt[max(0,start-180):min(len(txt),end+180)].lower(); before=txt[max(0,start-80):start].lower(); after=txt[end:min(len(txt),end+80)].lower()
 if any(x in before for x in ['not','no','does not','do not','without','never']): return True
 if any(x in ctx for x in BOUND): return True
 if re.match(r"\s*[:=-]?\s*(\*\*)?no(\*\*)?\b",after): return True
 return False
def main():
 blockers=[]; allowed_count=0; checked=0
 for f in iter_files():
  txt=f.read_text(encoding='utf-8',errors='ignore'); low=txt.lower(); checked+=1
  for pat in PATS:
   for m in re.finditer(re.escape(pat.lower()),low):
    item={"file":f.relative_to(ROOT).as_posix(),"phrase":pat,"context":txt[max(0,m.start()-80):min(len(txt),m.end()+80)].replace('\n',' ')}
    if allowed(txt,m.start(),m.end()): allowed_count+=1
    else: blockers.append(item)
 out={"status":"passed" if not blockers else "failed","checked_files":checked,"blockers":blockers,"blocker_count":len(blockers),"allowed_boundary_contexts":allowed_count}
 (ROOT/'reports').mkdir(exist_ok=True); (ROOT/'reports/claim-scan.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2)); raise SystemExit(0 if not blockers else 1)
if __name__=='__main__': main()
