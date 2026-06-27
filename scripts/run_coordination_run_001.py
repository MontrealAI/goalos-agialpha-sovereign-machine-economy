from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.coordination import CoordinationEngine

result = CoordinationEngine().route().to_dict()
Path("reports").mkdir(exist_ok=True)
Path("reports/coordination-run-001.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps(result, indent=2))
