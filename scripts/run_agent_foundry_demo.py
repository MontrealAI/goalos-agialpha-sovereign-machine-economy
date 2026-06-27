from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.agent_foundry import MetaAgenticFoundry

result = MetaAgenticFoundry().select("Design a proof-governed institution for autonomous AI work")
Path("reports").mkdir(exist_ok=True)
Path("reports/meta-agentic-foundry-demo.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result["selected"], indent=2))
