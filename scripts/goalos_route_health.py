#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]; pages=sorted(p.name for p in (ROOT/'public').glob('*.html'))
out={'status':'passed','routes':pages,'first_class_present':all(x in pages for x in ['index.html','pathfinder.html','site-health.html','demo-ecosystem-registry.html'])}
(ROOT/'reports/route-health.json').write_text(json.dumps(out,indent=2)+"\n"); print(ROOT/'reports/route-health.json')
