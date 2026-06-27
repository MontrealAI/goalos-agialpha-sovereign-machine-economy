from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.website_parity import audit

report = audit(".")
Path("reports").mkdir(exist_ok=True)
Path("reports/website-code-parity-v3.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
if report["status"] != "passed":
    raise SystemExit(1)
