import unittest
from src.goalos_ascension.frontier_release import FrontierReleaseRoom


class FrontierReleaseRoomTests(unittest.TestCase):
    def test_readiness_score_is_dynamic_and_boundary_preserved(self):
        room = FrontierReleaseRoom()
        low = room.review("public-source review", ["public_sources"])
        high = room.review("public-source review", ["public_sources", "safeguard_eval", "redteam_summary", "validator_memo", "rollback_protocol", "human_authority"])
        self.assertGreater(high.readiness_score, low.readiness_score)
        self.assertTrue(high.human_review_required)
        self.assertFalse(high.authority_granted)


if __name__ == "__main__":
    unittest.main()
