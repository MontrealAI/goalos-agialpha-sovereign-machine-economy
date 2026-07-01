from __future__ import annotations
from pathlib import Path
import json, re, html, os
ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'public'
REPORTS=ROOT/'reports'
CONFIRMATION='I confirm I am not submitting personal data, customer data, confidential data, regulated data, credentials, wallet information, private keys, seed phrases, payment information, trade secrets, proprietary data, or user funds.'
BOUNDARY=['no user data','no user funds','human review required']
FORBIDDEN_APIS=['localStorage','sessionStorage','fetch(','XMLHttpRequest','sendBeacon','window.ethereum']

def write_report(name,obj):
 REPORTS.mkdir(exist_ok=True); (REPORTS/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(REPORTS/name)

def html_links(path):
 txt=path.read_text(encoding='utf-8',errors='ignore')
 return [html.unescape(m.group(2)).strip() for m in re.finditer(r'''(?:href|src)\s*=\s*(["'])(.*?)\1''',txt,re.I)]

def is_external(u): return (not u) or u.startswith(('http://','https://','mailto:','tel:','#','javascript:','data:'))

def resolve_link(base,u):
 u=u.split('#',1)[0].split('?',1)[0]
 if is_external(u): return None
 if u.startswith('/'):
  marker='/goalos-agialpha-sovereign-machine-economy/'
  return PUBLIC/u.split(marker,1)[1] if marker in u else None
 t=(base.parent/u).resolve()
 return t/'index.html' if u.endswith('/') else t

def public_pages(): return sorted(PUBLIC.glob('*.html'))

def registry():
 p=ROOT/'content/goalos/demo-ecosystem-registry.json'
 try:
  d=json.loads(p.read_text())
  return d.get('routes') or d.get('demos') or []
 except Exception:
  return []
