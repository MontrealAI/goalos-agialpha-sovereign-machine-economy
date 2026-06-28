
from pathlib import Path
import json, datetime, re
ROOT=Path.cwd()

def write_report():
    Path('reports').mkdir(exist_ok=True)
    report={"status":"installed","layer":"proof-gradient-lab-v1","generated_at":datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z","pages":["public/proof-gradient-lab.html"],"browser_local":True,"no_user_data":True,"no_user_funds":True,"human_review_required":True}
    Path('reports/proof-gradient-lab-v1-install-report.json').write_text(json.dumps(report,indent=2)+"\n")

def patch_readme():
    p=Path('README.md')
    text=p.read_text(encoding='utf-8') if p.exists() else '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'
    marker='<!-- GOALOS_PROOF_GRADIENT_LAB_V1 -->'
    block=f'''\n{marker}\n\n## Proof Gradient Lab — No proof, no evolution\n\nA new browser-local public demonstration is available:\n\n- [Proof Gradient Lab](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-gradient-lab.html)\n\nIt demonstrates the core GoalOS / AEP-001 idea: score is advisory, hard gates are mandatory, and no candidate capability earns evolution without proof, evaluation, rollback readiness, scope authorization, canary posture, and challenge clearance.\n\nBoundary: no user data, no user funds, no wallet, no transaction, no external action, human review required.\n'''
    if marker not in text:
        text=block+'\n'+text
    p.write_text(text,encoding='utf-8')

def patch_index():
    p=Path('public/index.html')
    if not p.exists(): return
    text=p.read_text(encoding='utf-8')
    marker='goalos-proof-gradient-lab-card'
    if marker in text: return
    block='''\n<section id="goalos-proof-gradient-lab-card" style="max-width:1180px;margin:32px auto;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:28px;background:linear-gradient(135deg,rgba(255,232,138,.12),rgba(102,255,210,.06));color:#f8f4e8">\n  <p style="letter-spacing:.22em;text-transform:uppercase;color:#ffe88a;font-weight:900;font-size:12px">New public demonstration</p>\n  <h2 style="font-size:clamp(32px,5vw,64px);line-height:.95;margin:0 0 12px">Proof Gradient Lab</h2>\n  <p style="font-size:18px;line-height:1.6;max-width:850px;color:#cbd6f2">No proof, no evolution. Run a browser-local selection gate, inspect why score alone is not authority, and download an Evidence Docket, Selection Certificate, Ledger Entry, and Proof Card.</p>\n  <p><a href="proof-gradient-lab.html" style="display:inline-block;padding:14px 18px;border-radius:16px;background:#ffe88a;color:#061020;font-weight:900;text-decoration:none">Open Proof Gradient Lab</a></p>\n</section>\n'''
    if '</main>' in text:
        text=text.replace('</main>',block+'</main>',1)
    elif '</body>' in text:
        text=text.replace('</body>',block+'</body>',1)
    else:
        text+=block
    p.write_text(text,encoding='utf-8')

def patch_search():
    p=Path('public/search-index.json')
    item={"title":"Proof Gradient Lab","url":"proof-gradient-lab.html","description":"Browser-local demonstration of Aim, Act, Prove, Evolve and the Selection Gate."}
    data=[]
    if p.exists():
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            data=[]
    if isinstance(data,dict):
        arr=data.setdefault('pages',[])
    elif isinstance(data,list):
        arr=data
    else:
        arr=[]; data=arr
    if not any((x.get('url') if isinstance(x,dict) else None)==item['url'] for x in arr): arr.append(item)
    p.write_text(json.dumps(data,indent=2)+"\n",encoding='utf-8')

def patch_sitemap():
    p=Path('public/sitemap.xml')
    url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-gradient-lab.html'
    if p.exists():
        text=p.read_text(encoding='utf-8')
        if url in text: return
        entry=f'  <url><loc>{url}</loc></url>\n'
        if '</urlset>' in text: text=text.replace('</urlset>',entry+'</urlset>')
        else: text+='\n'+entry
    else:
        text=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{url}</loc></url>\n</urlset>\n'
    p.write_text(text,encoding='utf-8')

def issue_template():
    d=Path('.github/ISSUE_TEMPLATE'); d.mkdir(parents=True,exist_ok=True)
    p=d/'proof_gradient_lab_feedback.yml'
    if not p.exists():
        p.write_text('''name: Proof Gradient Lab feedback\ndescription: Public-safe feedback on the browser-local Proof Gradient Lab.\ntitle: "Proof Gradient Lab feedback: "\nlabels: ["proof-gradient", "feedback", "public-safe"]\nbody:\n  - type: markdown\n    attributes:\n      value: |\n        Do not submit personal data, customer data, confidential data, credentials, wallet data, private keys, seed phrases, funds, or regulated records.\n  - type: textarea\n    id: feedback\n    attributes:\n      label: Feedback\n      description: What was clear, confusing, impressive, or missing?\n    validations:\n      required: true\n  - type: checkboxes\n    id: boundary\n    attributes:\n      label: Boundary confirmation\n      options:\n        - label: I am not submitting personal, confidential, regulated, wallet, credential, payment, or customer data.\n          required: true\n''')

Path('.nojekyll').write_text('')
write_report(); patch_readme(); patch_index(); patch_search(); patch_sitemap(); issue_template()
print('Proof Gradient Lab V1 installed')
