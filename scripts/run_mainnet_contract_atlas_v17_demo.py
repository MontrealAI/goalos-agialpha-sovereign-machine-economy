import json, pathlib
root=pathlib.Path.cwd()
data=json.loads((root/'content/goalos/mainnet-contracts-v4.4.0.json').read_text())
assert data['metadata']['goalosCreatedContractCount']==48
assert len(data['contracts'])==49
assert any(c['name']=='AEPProofLedger' for c in data['contracts'])
(root/'reports').mkdir(exist_ok=True)
(root/'reports/mainnet-contract-atlas-v17-demo-run.json').write_text(json.dumps({'status':'passed','visibleContracts':49,'goalosCreated':48,'selected':'AEPProofLedger','externalActions':0}, indent=2))
print('mainnet contract atlas demo passed')
