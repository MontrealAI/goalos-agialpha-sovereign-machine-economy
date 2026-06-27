from src.goalos_ascension.node_runtime import SovereignNodeRuntime


def test_node_runtime_default_denies_external_authority():
    review = SovereignNodeRuntime().review_mission("Produce an Evidence Docket")
    assert review.authority == "NONE_GRANTED"
    assert review.external_actions == 0
    assert review.network_calls == 0
    assert review.node_state in {"HUMAN_REVIEW_REQUIRED", "HOLD_PENDING_EVIDENCE"}
