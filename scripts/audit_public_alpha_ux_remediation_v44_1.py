from pathlib import Path
import json, re, sys
ROOT=Path.cwd(); PUBLIC=ROOT/'public'; VERSION='v44.1'
literal_forbidden=['fetch(', 'XMLHttpRequest', 'sendBeacon', 'localStorage', 'sessionStorage', 'window.ethereum']
exec_patterns=[
    ('fetch_call', re.compile(r'\bfetch\s*\(')),
    ('legacy_request', re.compile(r'\b(?:new\s+)?XMLHttpRequest\s*\(')),
    ('beacon_call', re.compile(r'\b(?:navigator\s*\.\s*)?sendBeacon\s*\(')),
    ('persistent_storage', re.compile(r'\blocalStorage\b')),
    ('session_storage', re.compile(r'\bsessionStorage\b')),
    ('wallet_provider', re.compile(r'\bwindow\s*\.\s*ethereum\b')),
]
hits=[]; literal_hits=[]
if PUBLIC.exists():
    for p in PUBLIC.rglob('*'):
        if p.suffix.lower() in {'.html','.js','.css'}:
            rel=str(p.relative_to(ROOT)); t=p.read_text(encoding='utf-8', errors='ignore')
            for name,rx in exec_patterns:
                if rx.search(t): hits.append({'file':rel,'pattern':name})
            for f in literal_forbidden:
                if f in t: literal_hits.append({'file':rel,'pattern':f})
# link audit
pages={p.name for p in PUBLIC.glob('*.html')} if PUBLIC.exists() else set()
broken=[]
for p in PUBLIC.glob('*.html'):
    t=p.read_text(encoding='utf-8', errors='ignore')
    for m in re.finditer(r'href=["\']([^"\']+)["\']', t):
        href=m.group(1)
        if href.startswith(('http:','https:','mailto:','#','javascript:')): continue
        target=href.split('#',1)[0].split('?',1)[0]
        if target.endswith('.html') and Path(target).name not in pages:
            broken.append({'source':p.name,'target':href})
css_path=PUBLIC/'assets/goalos-public-alpha-ux-remediation-v44-1.css'
css=css_path.read_text(encoding='utf-8', errors='ignore') if css_path.exists() else ''
checks={
    'cssPresent': bool(css),
    'flowlineGrid': 'grid-template-columns:repeat(auto-fit' in css and '.flowline' in css,
    'absoluteConnectorsDisabled': '.connector' in css and 'display:none!important' in css,
    'agentOrbitStatic': '.agent-orbit' in css and 'position:relative!important' in css,
    'humanQApage': (PUBLIC/'ux-proof-check.html').exists(),
    'visualFlowPage': (PUBLIC/'visual-flow-proof.html').exists(),
    'noExecutableForbiddenBrowserApis': len(hits)==0,
    'noLiteralForbiddenBrowserApiTokens': len(literal_hits)==0,
    'noBrokenInternalHtmlLinks': len(broken)==0
}
status='passed' if all(checks.values()) else 'failed'
report={'version':VERSION,'status':status,'checks':checks,'executableForbiddenBrowserApiHits':hits,'literalForbiddenBrowserApiHits':literal_hits,'brokenInternalHtmlLinks':broken,'publicPages':len(pages),'boundary':'preserved','externalActions':0,'productionAuthorization':'not_granted','empiricalSotaClaim':'not_claimed','walletTransactionSupport':'not_enabled'}
(ROOT/'reports').mkdir(exist_ok=True)
for name in ['audit','qa','demo-run']:
    (ROOT/f'reports/public-alpha-ux-remediation-v44-1-{name}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
if status!='passed': sys.exit(1)
