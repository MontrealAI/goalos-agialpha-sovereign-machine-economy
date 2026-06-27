from src.goalos_ascension.website_parity import audit


def test_website_code_parity_v3_passes():
    report = audit(".")
    assert report["status"] == "passed"
    assert report["capabilities_checked"] >= 18
    assert report["capabilities_checked"] == report["capabilities_covered"]
    assert report["boundary"]["human_review_required"] is True
