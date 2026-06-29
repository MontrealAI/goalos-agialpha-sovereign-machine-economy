#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

out = {
  "schema":"goalos.proof_carrying_artifact_foundry.reference_run.v1",
  "generatedAt":datetime.now(timezone.utc).isoformat(),
  "artifactId":"pca-reference-repository-readiness-review",
  "artifactClass":"capability",
  "title":"Repository Launch Readiness Review capability package",
  "publicAlpha":True,
  "browserLocal":True,
  "noUserData":True,
  "noUserFunds":True,
  "noWallet":True,
  "noTransaction":True,
  "noNetworkCall":True,
  "humanReviewRequired":True,
  "gates":{
    "proofValid":True,
    "evalPass":True,
    "baselineCompared":True,
    "rollbackReady":True,
    "scopeAuthorized":True,
    "challengeCleared":True,
    "privacyBoundary":True,
    "replayPath":True
  },
  "decisionState":"ACTIVE_REVIEW_READY",
  "readiness":100,
  "selectionCertificate":{
    "decision":"review_ready_not_production_authorized",
    "scope":"public-alpha-review",
    "promotionAuthorized":False
  },
  "rollbackReceipt":{
    "rollbackReady":True,
    "rollbackTarget":"previous-safe-artifact-version",
    "productionRollback":False
  }
}
Path("evidence/demo").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(exist_ok=True)
Path("evidence/demo/proof-carrying-artifact-foundry-v1-reference-docket.json").write_text(json.dumps(out, indent=2)+"\n", encoding="utf-8")
Path("reports/proof-carrying-artifact-foundry-v1-demo-run.json").write_text(json.dumps({"status":"passed", "artifactId":out["artifactId"], "decisionState":out["decisionState"], "generatedAt":out["generatedAt"]}, indent=2)+"\n", encoding="utf-8")
print("proof-carrying artifact foundry demo generated")
