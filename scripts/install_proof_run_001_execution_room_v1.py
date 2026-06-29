from pathlib import Path
import json, datetime
ROOT=Path('.')
NOW=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'

def write(path, body):
    p=ROOT/path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding='utf-8')

readme_path=ROOT/'README.md'
marker='<!-- GOALOS_PROOF_RUN_001_EXECUTION_ROOM_V1 -->'
block=f'''
{marker}

## Proof Run 001 Execution Room

The next empirical step is Proof Run 001: a real bounded mission with an Evidence Docket, replay path, validator review, cost/risk ledger, governed decision state, Chronicle entry, and reusable capability package.

- Website: [`proof-run-001-execution-room.html`](https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-execution-room.html)
- Doc: [`docs/proof-runs/PROOF_RUN_001_EXECUTION_ROOM_V1.md`](docs/proof-runs/PROOF_RUN_001_EXECUTION_ROOM_V1.md)
- Reference docket: [`evidence/proof-run-001/proof-run-001-execution-room-reference-docket.json`](evidence/proof-run-001/proof-run-001-execution-room-reference-docket.json)

Boundary: no user data, no user funds, no wallet, no transaction, no network call, no production authority, human review required.
'''
if readme_path.exists():
    txt=readme_path.read_text(encoding='utf-8')
    if marker not in txt:
        readme_path.write_text(block+'\n'+txt, encoding='utf-8')
else:
    readme_path.write_text('# GoalOS AGIALPHA Ascension — Sovereign Machine Economy\n'+block, encoding='utf-8')

index_path=ROOT/'public/index.html'
if index_path.exists():
    txt=index_path.read_text(encoding='utf-8')
    if 'proof-run-001-execution-room.html' not in txt:
        insert='''
<section class="goalos-proof-run-001-execution-room" style="width:min(1180px,calc(100% - 40px));margin:40px auto;padding:24px;border:1px solid rgba(255,255,255,.14);border-radius:28px;background:rgba(255,255,255,.06);color:#f7f4e8">
  <p style="color:#ffe47d;letter-spacing:.22em;font-weight:900;text-transform:uppercase">Next empirical step</p>
  <h2 style="font-size:clamp(34px,5vw,72px);line-height:.95;margin:0 0 12px">Proof Run 001 Execution Room</h2>
  <p style="max-width:860px;color:#b9c5db;line-height:1.6">Architecture is not enough. The next move is the first real bounded mission: Evidence Docket, replay, validator review, cost/risk ledger, governed decision state, Chronicle, and reusable capability.</p>
  <a href="proof-run-001-execution-room.html" style="display:inline-block;margin-top:12px;padding:14px 18px;border-radius:999px;background:#ffe47d;color:#06101b;font-weight:900;text-decoration:none">Open Proof Run 001 Room</a>
</section>
'''
        txt = txt.replace('</main>', insert+'</main>', 1) if '</main>' in txt else txt+insert
        index_path.write_text(txt, encoding='utf-8')
search_path=ROOT/'public/search-index.json'
item={'title':'Proof Run 001 Execution Room','url':'proof-run-001-execution-room.html','summary':'The bridge from public-alpha architecture to the first real Evidence Docket.'}
if search_path.exists():
    try:
        data=json.loads(search_path.read_text(encoding='utf-8'))
        if isinstance(data,list) and not any(isinstance(x,dict) and x.get('url')==item['url'] for x in data):
            data.append(item); search_path.write_text(json.dumps(data,indent=2),encoding='utf-8')
    except Exception:
        pass
else:
    write('public/search-index.json', json.dumps([item], indent=2))
sitemap=ROOT/'public/sitemap.xml'
loc='https://montrealai.github.io/goalos-agialpha-sovereign-machine-economy/proof-run-001-execution-room.html'
if sitemap.exists():
    s=sitemap.read_text(encoding='utf-8')
    if loc not in s and '</urlset>' in s:
        sitemap.write_text(s.replace('</urlset>', f'<url><loc>{loc}</loc></url></urlset>'), encoding='utf-8')
else:
    write('public/sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>{loc}</loc></url></urlset>')
write('.nojekyll','')
manifest={'status':'installed','generated_at':NOW,'files':['public/proof-run-001-execution-room.html','public/assets/goalos-proof-run-001-execution-room-v1.css','public/assets/goalos-proof-run-001-execution-room-v1.js','docs/proof-runs/PROOF_RUN_001_EXECUTION_ROOM_V1.md','evidence/proof-run-001/proof-run-001-execution-room-reference-docket.json']}
write('reports/proof-run-001-execution-room-v1-install-report.json', json.dumps(manifest, indent=2))
print('Installed Proof Run 001 Execution Room V1')
