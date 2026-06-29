from pathlib import Path
import json, datetime

ROOT = Path.cwd()
NOW = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def ensure_parent(p):
    p.parent.mkdir(parents=True, exist_ok=True)

def main():
    docket = {
        "id":"open-ended-work-engine-lab-v1-reference-docket",
        "generated_at":NOW,
        "demo":"GoalOS Open-Ended Work Engine Lab V1",
        "claim":"GoalOS can demonstrate, in browser-local form, how open-ended generated work remains gated by proof, replay, validator binding, risk boundaries, and human review.",
        "not_claims":["No live model call","No production task generation","No wallet","No transaction","No user data","No production authority"],
        "generation_cycle":["Generate","Validate","Prove","Archive","Select","Harder mission"],
        "admissibility_gates":["SyntaxValid","SandboxSafe","ValidatorBound","Replayable","Interesting","Learnable","NonRedundant","RiskBounded","ImprovesWork","BoundaryPass","HumanReview"],
        "decision_state":"ENGINE_REVIEW_READY",
        "boundary":{"no_user_data":True,"no_user_funds":True,"no_wallet":True,"no_transaction":True,"no_network_call":True,"human_review_required":True}
    }
    ep = ROOT / "evidence" / "demo" / "open-ended-work-engine-lab-v1-reference-docket.json"
    ensure_parent(ep)
    ep.write_text(json.dumps(docket, indent=2), encoding="utf-8")
    rp = ROOT / "reports" / "open-ended-work-engine-lab-v1-demo-run.json"
    ensure_parent(rp)
    rp.write_text(json.dumps({"status":"passed","generated_at":NOW,"docket":str(ep)}, indent=2), encoding="utf-8")
    print("Open-Ended Work Engine Lab reference docket generated.")

if __name__ == "__main__":
    main()
