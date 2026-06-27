.PHONY: qa site demo scorecard hashes

qa:
	python scripts/validate_repo.py
	python scripts/validate_claims.py
	python scripts/build_site.py
	python scripts/verify_site.py
	python scripts/compute_institutional_scorecard.py
	python scripts/hash_artifacts.py

site:
	python scripts/build_site.py

demo:
	python scripts/run_demo_mission.py

scorecard:
	python scripts/compute_institutional_scorecard.py

hashes:
	python scripts/hash_artifacts.py

.PHONY: capability-parity proof-run-001 aep001 mission-os-demo

capability-parity:
	python scripts/run_capability_parity_audit.py

proof-run-001:
	python scripts/run_proof_run_001.py

aep001:
	python scripts/run_aep001_conformance.py

mission-os-demo:
	python scripts/run_mission_os_demo.py
