from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.parity import audit

report = audit(".")
print(json.dumps(report, indent=2))
