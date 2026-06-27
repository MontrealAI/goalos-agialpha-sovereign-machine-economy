from src.goalos_ascension.agi_jobs import AGIJobsLedger


def test_agi_jobs_lifecycle_is_simulation_only_and_replayable():
    record = AGIJobsLedger().run_lifecycle("Proof-gated autonomous work")
    assert record.settlement["status"] == "settled_simulated"
    assert record.settlement["mainnet"] is False
    assert record.settlement["user_funds"] is False
    assert "replay_path" in record.proof
