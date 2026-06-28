from pathlib import Path
import json, re, datetime
ROOT = Path('.')
required = [
 'public/multi-agent-institution.html',
 'public/assets/goalos-institution-v6.css',
 'public/assets/goalos-institution-v6.js',
 'docs/institution/MULTI_AGENT_INSTITUTION_EXPERIENCE_V6.md',
 'docs/institution/NON_TECHNICAL_USER_GUIDE.md',
 'docs/institution/ADVANCED_COORDINATION_NOTES.md'
]
errors=[]
for p in required:
    if not (ROOT/p).exists(): errors.append(f'missing:{p}')
js = (ROOT/'public/assets/goalos-institution-v6.js').read_text(encoding='utf-8') if (ROOT/'public/assets/goalos-institution-v6.js').exists() else ''
blocked = ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']
for b in blocked:
    if b in js: errors.append(f'blocked_js_api:{b}')
html = (ROOT/'public/multi-agent-institution.html').read_text(encoding='utf-8') if (ROOT/'public/multi-agent-institution.html').exists() else ''
for phrase in ['No user data','No user funds','No wallet','No transaction','Human review']:
    if phrase not in html: errors.append(f'missing_boundary_phrase:{phrase}')
report = {
  'status':'passed' if not errors else 'failed',
  'generated_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),
  'page':'public/multi-agent-institution.html',
  'checks':{
    'browser_local':True,
    'no_network_api_in_demo_js':not any(b in js for b in blocked[:3]),
    'no_storage_or_wallet_api':not any(b in js for b in blocked[3:]),
    'no_user_data_boundary': 'No user data' in html,
    'no_user_funds_boundary':'No user funds' in html,
    'human_review_required':'Human review' in html,
    'docket_download':'download-docket' in html and 'buildDocket' in js,
    'advanced_mode':'Coordination calculus' in html and 'Proof-conditioned objective' in html,
    'nontechnical_mode':'Plain-English guide' in html,
  },
  'errors':errors
}
(ROOT/'reports').mkdir(exist_ok=True)
(ROOT/'reports/multi-agent-institution-v6-qa.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
if errors:
    raise SystemExit('Multi-Agent Institution V6 audit failed: '+', '.join(errors))
print(json.dumps(report, indent=2))
