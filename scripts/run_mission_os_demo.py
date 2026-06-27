from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from src.goalos_ascension.mission_os import MissionOS

result = MissionOS().run_until_done("Produce a public-safe governed decision state for the GoalOS implementation parity review.", "mission-os-demo")
Path("reports").mkdir(exist_ok=True)
Path("reports/mission-os-demo.json").write_text(json.dumps(result, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
print(json.dumps(result["mission_os_done_state"], indent=2))
