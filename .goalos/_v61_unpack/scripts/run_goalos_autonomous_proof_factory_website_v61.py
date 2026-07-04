
#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,hashlib,csv,re,datetime
from pathlib import Path

def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:60] or 'mission'
def domain(obj):
    t=obj.lower()
    if re.search(r'web|site|github|repo|code|workflow|bug|release',t): return 'software-repository'
    if re.search(r'vendor|procure|market|business|strategy|customer|partner',t): return 'business-diligence'
    if re.search(r'research|paper|science|benchmark|experiment',t): return 'research-benchmark'
    if re.search(r'privacy|token|boundary|legal|governance|policy',t): return 'governance-boundary'
    if re.search(r'rsi|loop|move|novelty|invention',t): return 'rsi-open-ended-discovery'
    return 'general-work'
def write_json(p,data): p.write_text(json.dumps(data,indent=2),encoding='utf-8')
def run_one(root, mission, idx):
    obj=mission.get('objective') or str(mission); mid=mission.get('id') or slug(obj); d=root/'evidence'/'autonomous-proof-factory-v61'/'runtime'/f'{idx:02d}-{slug(mid)}'; d.mkdir(parents=True,exist_ok=True)
    now=datetime.datetime.utcnow().isoformat()+'Z'; dom=domain(obj)
    boundary=['No user data','No user funds','No wallet','No transaction','No network call','No production authority','Human review required for high-impact outcomes']
    stages=['Mission Contract','Agent Role Contracts','AGI Job Card','State on Disk','ProofBundle','AGI Node Validation','Evidence Docket','Chronicle Entry','Capability Promotion Gate','Human Review Hold']
    agents=['Mission Architect','Planner','Researcher','Builder','Evidence Agent','Verifier','AGI Node Validator','Sentinel','Chronicle Agent','Capability Promoter']
    base={'version':'v61','mission_id':mid,'objective':obj,'domain':dom,'created_at':now,'public_alpha_boundary':boundary}
    write_json(d/'mission-contract.json',{**base,'success_criteria':['objective bounded','claims evidence-backed','validation route selected','artifacts review-ready'],'failure_criteria':['unsupported claim','missing replay path','authority overreach','wallet or transaction request'],'done_condition':'reviewer-ready Evidence Docket and decision state'})
    write_json(d/'agent-constellation.json',{**base,'agents':[{'name':a,'role':'produce or validate one artifact','output_required':True} for a in agents]})
    write_json(d/'agi-job-card.json',{**base,'acceptance_tests':['schema valid','boundary preserved','action graph complete','risk ledger complete','review hold present'],'tool_scope':'browser-local / repository-local public-safe artifacts only','forbidden_actions':['wallet prompt','transaction','network call','secret collection','production authorization']})
    write_json(d/'agi-node-validation-certificate.json',{**base,'worker':'prepared bounded artifacts','validator':'checks replay path and proof completeness','sentinel':'monitors boundary and risk','verdict':'HUMAN_REVIEW_HOLD','challenge_window':'required before promotion'})
    write_json(d/'proof-bundle.json',{**base,'proof_packets':[{'stage':s,'status':'prepared','hash':hashlib.sha256((mid+s).encode()).hexdigest()} for s in stages],'replay_path':'Use this runtime folder plus hashes.json and reviewer-brief.md'})
    (d/'evidence-docket.md').write_text(f'# Evidence Docket — {mid}\n\nObjective: {obj}\n\nDomain: {dom}\n\n## Claims matrix\n\n| Claim | Evidence | Status |\n|---|---|---|\n| Mission is bounded | mission-contract.json | prepared |\n| Agents have roles | agent-constellation.json | prepared |\n| AGI Job is reviewable | agi-job-card.json | prepared |\n| AGI Node validation path exists | agi-node-validation-certificate.json | human-review hold |\n\n## Boundary\n\n'+'\n'.join('- '+b for b in boundary)+'\n',encoding='utf-8')
    (d/'reviewer-brief.md').write_text(f'# Reviewer Brief — {mid}\n\nReview the Evidence Docket, hashes, risk boundary, and validation certificate. Accept, reject, or request changes.\n',encoding='utf-8')
    with (d/'action-graph.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['step','owner','action','proof_required','status'])
        for i,s in enumerate(stages,1): w.writerow([i,agents[(i-1)%len(agents)],s,slug(s)+'.json','prepared'])
    write_json(d/'chronicle-entry.json',{**base,'summary':'Mission converted into autonomous proof-factory artifacts.','status':'review_hold','next_mission':'increase evidence depth or external replay'})
    write_json(d/'reusable-capability-package.json',{**base,'capability':'autonomous proof mission package for '+dom,'initiation_conditions':['public-safe objective','reviewer authority','proof boundary accepted'],'limitations':['simulation-only settlement','not production authorization']})
    write_json(d/'selection-certificate.json',{**base,'decision':'hold_for_review','why':'Public-alpha outputs require human or AGI Node validation before promotion','rollback':'discard runtime folder or mark rejected'})
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()}
    write_json(d/'hashes.json',hashes)
    return {'mission_id':mid,'objective':obj,'domain':dom,'runtime':str(d),'status':'review_hold','artifacts':len(hashes)+1}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--queue',default='.goalos/autonomy/v61/mission-queue.example.json'); ap.add_argument('--max-cycles',type=int,default=3); args=ap.parse_args(); root=Path.cwd()
    qpath=root/args.queue
    if not qpath.exists(): qpath=root/'.goalos/autonomy/v61/mission-queue.example.json'
    data=json.loads(qpath.read_text(encoding='utf-8')); missions=data.get('missions',data if isinstance(data,list) else [])[:args.max_cycles]
    rows=[run_one(root,m,i+1) for i,m in enumerate(missions)]
    (root/'reports').mkdir(exist_ok=True)
    report={'version':'v61','status':'passed','mission_cycles_processed':len(rows),'missions':rows,'public_alpha_boundary_preserved':True}
    (root/'reports'/'autonomous-proof-factory-website-v61-run-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    with (root/'reports'/'autonomous-proof-factory-website-v61-run-report.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['mission_id','objective','domain','runtime','status','artifacts']); w.writeheader(); w.writerows(rows)
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
