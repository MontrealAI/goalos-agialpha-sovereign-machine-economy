from pathlib import Path
import json, datetime, hashlib
now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
docket = {
    'schema': 'goalos.proof_to_action_command_room.v1',
    'generated_at': now,
    'browser_local_reference': True,
    'mission': 'Repository launch readiness',
    'loop': ['Objective','Mission Contract','Claims Matrix','Autonomous Work','Verification','Evidence Docket','Governed Decision State','Action Graph','Chronicle','Capability Package'],
    'governed_decision_state': {'state': 'HUMAN_REVIEW_READY_ACTION_GRAPH_READY', 'claim_boundary': 'public-alpha reference demo only', 'authority': 'human review required', 'external_actions': 0},
    'boundary': {'no_user_data': True, 'no_user_funds': True, 'no_wallet': True, 'no_transaction': True, 'no_network_call': True, 'human_review_required': True},
    'artifacts': ['Evidence Docket JSON','Action Graph JSON','Chronicle Entry JSON','Capability Package JSON','Executive Brief Markdown']
}
text = json.dumps(docket, sort_keys=True)
docket['digest'] = 'sha256:' + hashlib.sha256(text.encode()).hexdigest()
Path('evidence/demo').mkdir(parents=True, exist_ok=True)
Path('reports').mkdir(exist_ok=True)
Path('evidence/demo/proof-to-action-command-room-v1-reference-docket.json').write_text(json.dumps(docket, indent=2) + '\n', encoding='utf-8')
Path('reports/proof-to-action-command-room-v1-demo-run.json').write_text(json.dumps({'status': 'passed', 'generated_at': now, 'docket': 'evidence/demo/proof-to-action-command-room-v1-reference-docket.json', 'digest': docket['digest']}, indent=2) + '\n', encoding='utf-8')
print('Generated proof-to-action reference docket')
