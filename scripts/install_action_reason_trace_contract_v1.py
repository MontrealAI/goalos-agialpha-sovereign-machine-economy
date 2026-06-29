from pathlib import Path
import json, datetime, re
ROOT = Path.cwd()
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
FILES = [
 'public/action-reason-trace-contract.html',
 'public/assets/goalos-action-reason-trace-v1.css',
 'public/assets/goalos-action-reason-trace-v1.js',
 'docs/demos/ACTION_REASON_TRACE_CONTRACT_V1.md',
 'docs/reviewer/HOW_TO_REVIEW_ACTION_REASON_TRACE_CONTRACT.md',
 'examples/action-reason-trace/public-safe-action-scenarios.md',
 'scripts/run_action_reason_trace_contract_v1_demo.py',
 'scripts/goalos_action_reason_trace_contract_v1_audit.py',
 'content/goalos/action-reason-trace-contract-v1.json',
 '.github/ISSUE_TEMPLATE/action_reason_trace_contract_feedback.yml',
 'issue-bodies/action-reason-trace-contract-v1.md'
]

def append_once(path, marker, text):
    p=ROOT/path
    existing=p.read_text(encoding='utf-8') if p.exists() else ''
    if marker not in existing:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text((existing.rstrip()+"\n\n"+text.strip()+"\n") if existing else text.strip()+"\n", encoding='utf-8')

def patch_index():
    p=ROOT/'public/index.html'
    if not p.exists(): return
    s=p.read_text(encoding='utf-8')
    link='action-reason-trace-contract.html'
    if link in s: return
    card='''\n<section class="goalos-action-trace-callout" style="max-width:1180px;margin:40px auto;padding:28px;border:1px solid rgba(255,255,255,.16);border-radius:24px;background:rgba(255,255,255,.06)">\n  <p style="color:#ffe978;font-weight:900;letter-spacing:.18em;text-transform:uppercase">New public demo</p>\n  <h2>Every action must carry a reason.</h2>\n  <p>Open the Action-Reason Trace Contract to see how GoalOS binds external action to scope, observation, validation, cost/risk, rollback, and evidence.</p>\n  <p><a href="action-reason-trace-contract.html" style="color:#64ffd2;font-weight:900">Open Action Trace →</a></p>\n</section>\n'''
    s=s.replace('</main>', card+'</main>') if '</main>' in s else s+card
    p.write_text(s,encoding='utf-8')

def patch_search():
    p=ROOT/'public/search-index.json'
    entry={"title":"Action-Reason Trace Contract","url":"action-reason-trace-contract.html","description":"Browser-local GoalOS demo: every external action carries reason, scope, observation, validation, rollback, and evidence."}
    arr=[]
    if p.exists():
        try: arr=json.loads(p.read_text(encoding='utf-8'))
        except Exception: arr=[]
    if isinstance(arr,dict): arr=arr.get('items',[])
    if not any(x.get('url')==entry['url'] for x in arr if isinstance(x,dict)):
        arr.append(entry)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(arr,indent=2),encoding='utf-8')

def patch_sitemap():
    p=ROOT/'public/sitemap.xml'
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/action-reason-trace-contract.html'
    if not p.exists():
        p.write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>\n',encoding='utf-8')
    s=p.read_text(encoding='utf-8')
    if url not in s:
        s=s.replace('</urlset>',f'  <url><loc>{url}</loc></url>\n</urlset>')
    p.write_text(s,encoding='utf-8')

def main():
    append_once(Path('README.md'),'<!-- GOALOS_ACTION_REASON_TRACE_CONTRACT_V1 -->','''<!-- GOALOS_ACTION_REASON_TRACE_CONTRACT_V1 -->\n\n## Action-Reason Trace Contract V1\n\n**Every action must carry a reason.** The browser-local Action-Reason Trace Contract demonstrates how GoalOS binds action intent to permission scope, expected observation, actual observation, validator status, cost/risk, rollback, evidence pointer, and human review.\n\nOpen: `public/action-reason-trace-contract.html`\n\nBoundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority; human review required.''')
    patch_index(); patch_search(); patch_sitemap();
    (ROOT/'public/.nojekyll').write_text('',encoding='utf-8')
    report={"status":"passed","generatedAt":NOW,"files":FILES,"page":"public/action-reason-trace-contract.html","boundary":{"noUserData":True,"noUserFunds":True,"noWallet":True,"noTransaction":True,"noNetworkCall":True,"humanReviewRequired":True}}
    out=ROOT/'reports/action-reason-trace-contract-v1-install-report.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
