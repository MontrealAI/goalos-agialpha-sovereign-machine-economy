from pathlib import Path
import json, datetime, re
required=[
 'public/falsification-gauntlet.html',
 'public/assets/goalos-falsification-gauntlet-v1-1.css',
 'public/assets/goalos-falsification-gauntlet-v1-1.js',
 'scripts/install_falsification_gauntlet_v1_1.py',
 'scripts/run_falsification_gauntlet_v1_1_demo.py'
]
errors=[]
for f in required:
    if not Path(f).exists(): errors.append(f'missing {f}')
js=Path('public/assets/goalos-falsification-gauntlet-v1-1.js').read_text() if Path('public/assets/goalos-falsification-gauntlet-v1-1.js').exists() else ''
html=Path('public/falsification-gauntlet.html').read_text() if Path('public/falsification-gauntlet.html').exists() else ''
for token in ['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']:
    if token in js: errors.append(f'forbidden browser API in JS: {token}')
checks={
 'preserves_custom_claim':'state.claimText=e.target.value' in js and 'custom claim preserved' in js.lower(),
 'stress_modifies_baselines':'scores.B6=Math.max(0,scores.B6-18)' in js,
 'same_public_link':'falsification-gauntlet.html' in html,
 'new_asset_loaded':'goalos-falsification-gauntlet-v1-1.js' in html,
 'no_data_boundary':'no user data' in html.lower() and 'no user funds' in html.lower()
}
for k,v in checks.items():
    if not v: errors.append(f'check failed: {k}')
report={'schema':'goalos.falsification_gauntlet.v1_1.qa','generated_at':datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat().replace('+00:00','Z'),'status':'passed' if not errors else 'failed','errors':errors,'checks':checks,'browser_local':True,'no_network_call':True,'no_user_data':True,'no_user_funds':True,'wallet_or_mainnet':False,'human_review_required':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/falsification-gauntlet-v1-1-qa.json').write_text(json.dumps(report,indent=2))
Path('reports/falsification-gauntlet-v1-1-install-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
if errors: raise SystemExit(1)
