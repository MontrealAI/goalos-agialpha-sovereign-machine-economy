from pathlib import Path
import json, re, datetime
root=Path('.')
html_files=sorted((root/'public').glob('*.html')) if (root/'public').exists() else []
joined='\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in html_files)
external_scripts=[]; forms=[]; tracking_terms=[]
for p in html_files:
    s=p.read_text(encoding='utf-8', errors='ignore')
    if re.search(r'<script[^>]+src=["\']https?://', s, re.I): external_scripts.append(str(p))
    if re.search(r'<form\b', s, re.I): forms.append(str(p))
    for term in ['google-analytics','gtag(','googletagmanager','segment.com','mixpanel','amplitude','hotjar','facebook pixel','fbq(']:
        if term.lower() in s.lower(): tracking_terms.append({'file':str(p),'term':term})
required={'privacy_page':(root/'public/privacy.html').exists(),'terms_page':(root/'public/terms.html').exists(),'data_boundary_page':(root/'public/data-boundary.html').exists(),'token_boundary_page':(root/'public/investment-token-boundary.html').exists(),'root_privacy':(root/'PRIVACY.md').exists(),'root_terms':(root/'TERMS.md').exists(),'root_data_boundary':(root/'DATA_BOUNDARY.md').exists(),'issue_templates':(root/'.github/ISSUE_TEMPLATE/validator_review.yml').exists(),'pr_template':(root/'.github/pull_request_template.md').exists(),'security':(root/'SECURITY.md').exists()}
required_text=['We do not want your data','Do not submit personal data','No token sale','No wallet','No transaction']
texts=[]
for p in ['README.md','PRIVACY.md','DATA_BOUNDARY.md','TERMS.md']:
    fp=root/p
    if fp.exists(): texts.append(fp.read_text(encoding='utf-8', errors='ignore'))
text_joined=joined+'\n'+'\n'.join(texts)
text_hits={t:(t.lower() in text_joined.lower()) for t in required_text}
errors=[]
if external_scripts: errors.append('external_scripts_detected')
if forms: errors.append('forms_detected')
if tracking_terms: errors.append('tracking_terms_detected')
for k,v in required.items():
    if not v: errors.append(f'missing_{k}')
for k,v in text_hits.items():
    if not v: errors.append(f'missing_text_{k}')
report={'generated_at':datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z','status':'passed' if not errors else 'failed','zero_user_data_boundary':True,'no_user_data_wanted':True,'public_site_posture':{'intentional_analytics':False,'forms_collecting_user_data':False,'wallet_connection':False,'transaction_execution':False,'production_authority':False,'model_call_collection':False,'human_review_required':True},'external_scripts_detected':external_scripts,'forms_detected':forms,'tracking_terms_detected':tracking_terms,'required_files':required,'required_text':text_hits,'errors':errors,'counsel_review_recommended':True}
Path('reports').mkdir(exist_ok=True)
Path('reports/legal-privacy-shield-qa.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
if errors: raise SystemExit('Legal/privacy audit failed: '+', '.join(errors))
