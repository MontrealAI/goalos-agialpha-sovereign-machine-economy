from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.node_runtime import SovereignNodeRuntime

result = SovereignNodeRuntime().review_mission("Produce a human-review-ready Evidence Docket").to_dict()
Path("reports").mkdir(exist_ok=True)
Path("reports/agi-alpha-node-theatre-demo.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
