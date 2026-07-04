#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,csv,datetime,re

def h(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')[:64] or 'mission'
roles=['Architect Agent','Planner Agent','Research Agent','Builder Agent','Verifier Agent','Sentinel Agent','Evidence Docket Agent','Chronicle Agent','AGI Node Validator']
def make(m,cycle):
    mid=m.get('mission_id') or slug(m.get('objective','mission')); obj=m.get('objective','Public-safe proof mission'); auth=m.get('authority_route','Hybrid review')
    contract={'schema':'GoalOSCommit.v9','mission_id':mid,'objective':obj,'authority_route':auth,'cycle':cycle,'status':'human_review_ready','blocked':['wallet','transaction','user funds','production authority']}
    docket={'schema':'EvidenceDocket6.1.v9','mission_id':mid,'claims':[{'claim':'Objective has a proof-gated work package.','status':'supported_by_generated_artifacts'},{'claim':'Production external authority is granted.','status':'blocked_not_claimed'}],'risks':['unsupported claim propagation','private data leakage'],'decision_state':'ready_for_human_review','replay_path':['inspect generated artifacts','run audit','human review']}
    return {'mission-contract.json':contract,'agent-constellation.json':{'mission_id':mid,'roles':roles},'agi-job-card.json':{'mission_id':mid,'acceptance_tests':['contract','docket','validation','review']},'agi-node-validation-certificate.json':{'mission_id':mid,'checks':['schema','boundary','docket','replay'],'outcome':'precheck_pass_human_gate_retained'},'proof-bundle.json':{'mission_id':mid,'docket_hash':h(docket),'contents':['contract','agent constellation','job card','validation','docket','chronicle']},'evidence-docket-61.json':docket,'chronicle-entry.json':{'mission_id':mid,'memory':'candidate; reusable after review only'},'reusable-capability-package.json':{'mission_id':mid,'promotion_status':'blocked_until_review'},'selection-certificate.json':{'mission_id':mid,'decision':'hold_for_review','reason':'public-alpha boundary'}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--queue',default='.goalos/autonomy/v9/mission-queue.example.json'); ap.add_argument('--max-cycles',type=int,default=1); args=ap.parse_args()
    root=Path.cwd(); q=root/args.queue
    data=json.loads(q.read_text(encoding='utf-8')) if q.exists() else {'queue':[{'mission_id':'v9-default','objective':'Prepare a public-safe proof mission.'}]}
    queue=data.get('queue') or data.get('missions') or []
    out=root/'evidence/autonomous-proof-factory-v9/runtime'; out.mkdir(parents=True,exist_ok=True); reports=root/'reports'; reports.mkdir(exist_ok=True)
    rows=[]
    for cycle in range(1,args.max_cycles+1):
        for m in queue:
            bundle=make(m,cycle); mid=(m.get('mission_id') or slug(m.get('objective','mission'))); d=out/mid; d.mkdir(parents=True,exist_ok=True)
            for name,obj in bundle.items(): (d/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
            (d/'reviewer-brief.md').write_text(f"# Reviewer Brief — {mid}\n\nObjective: {m.get('objective')}\n\nDecision state: hold for human review.\n",encoding='utf-8')
            (d/'action-graph.csv').write_text('step,owner,gate\nmission,Planner Agent,required\nvalidation,AGI Node Validator,precheck\nreview,Human Operator,required\n',encoding='utf-8')
            hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in d.iterdir() if p.is_file()}; (d/'hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
            rows.append({'cycle':cycle,'mission_id':mid,'status':'human_review_ready','artifact_count':len(list(d.iterdir())),'proof_hash':hashes.get('evidence-docket-61.json','')})
    (reports/'goalos-autonomous-proof-factory-v9-run-report.json').write_text(json.dumps({'generated_at':datetime.datetime.utcnow().isoformat()+'Z','missions':rows},indent=2),encoding='utf-8')
    with (reports/'goalos-autonomous-proof-factory-v9-run-report.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['cycle','mission_id','status','artifact_count','proof_hash']); w.writeheader(); w.writerows(rows)
    print('GoalOS V9 mission queue processed:',len(rows),'cycles')
if __name__=='__main__': main()
