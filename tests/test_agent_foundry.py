from src.goalos_ascension.agent_foundry import MetaAgenticFoundry


def test_foundry_generates_24_candidates_and_preserves_boundary():
    result = MetaAgenticFoundry().select("Design a proof-governed institution")
    assert result["candidate_count"] == 24
    assert result["status"] == "ready_for_human_review"
    assert result["selected"]["gates"]["no_external_action"] is True
