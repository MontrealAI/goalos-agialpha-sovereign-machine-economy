#!/usr/bin/env python3
import json
from pathlib import Path
report=json.loads(Path('reports/site-full-surface-restore-v12-report.json').read_text())
Path('reports/site-full-surface-restore-v12-demo-run.json').write_text(json.dumps({'status':'passed' if report.get('public_page_count',0)>=100 else 'review','checked':'site full surface restore demo run','public_page_count':report.get('public_page_count'),'restored_file_count':report.get('restored_file_count'),'boundary_preserved':'No user data' in report.get('boundary','')},indent=2))
print('site full surface restore demo run written')
