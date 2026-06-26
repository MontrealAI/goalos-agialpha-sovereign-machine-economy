from __future__ import annotations
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports' / 'artifact-digests.json'
INCLUDE = {'.md','.json','.py','.yml','.yaml','.html','.css','.js','.toml','.cff','.svg','.xml','.txt'}
SKIP_PARTS = {'.git','__pycache__'}

def digest(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return 'sha256:' + h.hexdigest()

def main() -> int:
    rows = []
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or p.suffix.lower() not in INCLUDE:
            continue
        if any(part in SKIP_PARTS for part in p.parts):
            continue
        if str(p.relative_to(ROOT)) == 'reports/artifact-digests.json':
            continue
        rows.append({'path':str(p.relative_to(ROOT)),'sha256':digest(p),'bytes':p.stat().st_size})
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps({'generated_at_utc':datetime.now(timezone.utc).isoformat(),'artifact_count':len(rows),'artifacts':rows}, indent=2), encoding='utf-8')
    print(f'Hashed {len(rows)} artifacts. Report: {REPORT.relative_to(ROOT)}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
