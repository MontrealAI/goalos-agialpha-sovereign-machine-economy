from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.agi_jobs import AGIJobsLedger

result = AGIJobsLedger().run_lifecycle("Proof-gated autonomous work demo").to_dict()
Path("reports").mkdir(exist_ok=True)
Path("reports/agi-jobs-ledger-demo.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
