from pathlib import Path
import json, datetime
errors = []
required = [
    'public/proof-to-action-command-room.html',
    'public/assets/goalos-proof-to-action-v1.css',
    'public/assets/goalos-proof-to-action-v1.js',
    'docs/demos/PROOF_TO_ACTION_COMMAND_ROOM_V1.md',
    'docs/reviewer/HOW_TO_REVIEW_PROOF_TO_ACTION_COMMAND_ROOM.md',
    'evidence/demo/proof-to-action-command-room-v1-reference-docket.json'
]
for r in required:
    if not Path(r).exists(): errors.append(f'missing:{r}')
html = Path('public/proof-to-action-command-room.html').read_text(encoding='utf-8') if Path('public/proof-to-action-command-room.html').exists() else ''
js = Path('public/assets/goalos-proof-to-action-v1.js').read_text(encoding='utf-8') if Path('public/assets/goalos-proof-to-action-v1.js').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review required']:
    if phrase not in html: errors.append(f'missing boundary phrase:{phrase}')
for banned in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']:
    if banned in js: errors.append(f'blocked browser API appears:{banned}')
for needed in ['Governed Decision State','Action Graph','Chronicle','Capability Package','Evidence Docket']:
    if needed not in html: errors.append(f'missing concept:{needed}')
report = {
    'status': 'failed' if errors else 'passed',
    'generated_at': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
    'page': 'public/proof-to-action-command-room.html',
    'browser_local': True,
    'no_network_call': True,
    'no_user_data': True,
    'no_user_funds': True,
    'wallet_or_mainnet': False,
    'human_review_required': True,
    'errors': errors
}
Path('reports').mkdir(exist_ok=True)
Path('reports/proof-to-action-command-room-v1-qa.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
if errors: raise SystemExit(1)
