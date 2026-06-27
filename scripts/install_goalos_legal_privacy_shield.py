from pathlib import Path
import re, json, datetime
root = Path('.')
block = """
<!-- GOALOS_LEGAL_PRIVACY_SHIELD_START -->

## Legal & Privacy Shield — zero user data boundary

**GoalOS does not want user data. Do not submit personal data, customer data, confidential data, credentials, private keys, regulated records, payment data, health data, children’s data, trade secrets, or privileged information through the public website, GitHub issues, pull requests, demos, Evidence Dockets, or public proof runs.**

Public-alpha boundary:

- No intentional analytics.
- No public forms collecting user data.
- No wallet connection.
- No transaction execution.
- No production authorization.
- No legal, financial, investment, tax, medical, security, or regulatory advice.
- No token sale, investment offer, profit promise, or user-fund authorization.
- Human review required.

Key pages:

- [Privacy Notice](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/privacy.html)
- [Terms of Use](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/terms.html)
- [Zero User Data Boundary](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/data-boundary.html)
- [Token & Investment Boundary](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/investment-token-boundary.html)
- [Responsible Use](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/responsible-use.html)

Private, enterprise, regulated, customer-data, token-related, settlement, or production work requires a separate written agreement and independent legal/security review.

<!-- GOALOS_LEGAL_PRIVACY_SHIELD_END -->
"""
readme = root/'README.md'
if readme.exists():
    s = readme.read_text(encoding='utf-8')
    pat = re.compile(r'<!-- GOALOS_LEGAL_PRIVACY_SHIELD_START -->.*?<!-- GOALOS_LEGAL_PRIVACY_SHIELD_END -->', re.S)
    s = pat.sub(block.strip(), s) if pat.search(s) else block.strip()+"\n\n"+s
else:
    s = '# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n\n'+block.strip()+"\n"
readme.write_text(s, encoding='utf-8')
home_block = """
<!-- GOALOS_LEGAL_PRIVACY_HOME_START -->
<section class="legal-privacy-shield" style="max-width:1120px;margin:48px auto;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:28px;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.04));box-shadow:0 24px 70px rgba(0,0,0,.28)">
  <p style="color:#ffe17a;letter-spacing:.22em;text-transform:uppercase;font-size:12px;font-weight:900;margin:0 0 10px">Legal & Privacy Shield</p>
  <h2 style="font-size:clamp(30px,4vw,58px);line-height:.95;letter-spacing:-.05em;margin:0 0 12px;color:#fff">We do not want your data.</h2>
  <p style="color:#c4cee9;font-size:18px;max-width:900px">GoalOS is designed as a public-alpha, browser-local, no-wallet, no-transaction, no-intentional-analytics proof architecture. Do not submit personal, customer, confidential, regulated, credential, or trade-secret data through the website, GitHub issues, pull requests, demos, or public dockets.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:18px"><a href="privacy.html" style="padding:12px 15px;border-radius:14px;background:#ffe17a;color:#06101c;text-decoration:none;font-weight:900">Privacy Notice</a><a href="data-boundary.html" style="padding:12px 15px;border-radius:14px;background:rgba(255,255,255,.08);color:#fff;text-decoration:none;font-weight:800;border:1px solid rgba(255,255,255,.12)">Data Boundary</a><a href="terms.html" style="padding:12px 15px;border-radius:14px;background:rgba(255,255,255,.08);color:#fff;text-decoration:none;font-weight:800;border:1px solid rgba(255,255,255,.12)">Terms</a><a href="investment-token-boundary.html" style="padding:12px 15px;border-radius:14px;background:rgba(255,255,255,.08);color:#fff;text-decoration:none;font-weight:800;border:1px solid rgba(255,255,255,.12)">Token Boundary</a></div>
</section>
<!-- GOALOS_LEGAL_PRIVACY_HOME_END -->
"""
index = root/'public/index.html'
if index.exists():
    s = index.read_text(encoding='utf-8')
    pat = re.compile(r'<!-- GOALOS_LEGAL_PRIVACY_HOME_START -->.*?<!-- GOALOS_LEGAL_PRIVACY_HOME_END -->', re.S)
    if pat.search(s): s = pat.sub(home_block.strip(), s)
    elif '</main>' in s: s = s.replace('</main>', home_block.strip()+'\n</main>', 1)
    elif '</body>' in s: s = s.replace('</body>', home_block.strip()+'\n</body>', 1)
    else: s += '\n'+home_block
    index.write_text(s, encoding='utf-8')
search_path = root/'public/search-index.json'
entries = [
 {'title':'Legal Shield','url':'legal.html','summary':'GoalOS legal, privacy, data, investment, and responsibility boundary.'},
 {'title':'Privacy Notice','url':'privacy.html','summary':'GoalOS does not want user data; static, no-account, no-tracking public site posture.'},
 {'title':'Zero User Data Boundary','url':'data-boundary.html','summary':'Do not submit personal, customer, confidential, regulated, credential, or trade-secret data.'},
 {'title':'Terms of Use','url':'terms.html','summary':'Public-alpha no-reliance, no-advice, no-production-authority terms.'},
 {'title':'Token & Investment Boundary','url':'investment-token-boundary.html','summary':'No token sale, no investment offer, no profit promise, no user-fund authorization.'},
 {'title':'Responsible Use','url':'responsible-use.html','summary':'Lawful, bounded, public-safe, human-reviewed use only.'},
 {'title':'Security Boundary','url':'security-boundary.html','summary':'Default-deny, no public secrets, no unauthorized testing.'}
]
try:
    data = json.loads(search_path.read_text(encoding='utf-8')) if search_path.exists() else []
    if not isinstance(data, list): data=[]
except Exception: data=[]
urls={x.get('url') for x in data if isinstance(x,dict)}
for e in entries:
    if e['url'] not in urls: data.append(e)
search_path.parent.mkdir(exist_ok=True)
search_path.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
sitemap = root/'public/sitemap.xml'
page_names = ['legal.html','privacy.html','terms.html','data-boundary.html','responsible-use.html','investment-token-boundary.html','security-boundary.html']
base_url='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/'
if sitemap.exists():
    sm=sitemap.read_text(encoding='utf-8')
    for name in page_names:
        loc=f'<loc>{base_url}{name}</loc>'
        if loc not in sm and '</urlset>' in sm:
            sm=sm.replace('</urlset>', f'  <url><loc>{base_url}{name}</loc></url>\n</urlset>')
else:
    sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{base_url}{n}</loc></url>\n' for n in page_names)+'</urlset>\n'
sitemap.write_text(sm, encoding='utf-8')
(root/'public/.nojekyll').write_text('', encoding='utf-8')
(root/'.nojekyll').write_text('', encoding='utf-8')
manifest={'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','name':'GoalOS Legal & Privacy Shield','version':'v0.14.0-legal-privacy-shield','core_rule':'GoalOS does not want user data; do not submit personal, customer, confidential, regulated, credential, or trade-secret data.','claim_boundaries':['no legal advice','no investment advice','no token sale','no production authorization','no achieved AGI/ASI/SOTA','no user-fund authorization'],'counsel_review_recommended':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/legal-privacy-shield-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(json.dumps(manifest, indent=2))
