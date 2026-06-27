from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.proof_run import run_proof_run_001

result = run_proof_run_001(Path("evidence/proof-run-001"))
print(json.dumps(result["report"], indent=2))
