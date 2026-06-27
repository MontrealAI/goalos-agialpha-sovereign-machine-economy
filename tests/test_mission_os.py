import unittest
from src.goalos_ascension.mission_os import MissionOS


class MissionOSTests(unittest.TestCase):
    def test_until_done_loop_emits_required_artifacts(self):
        result = MissionOS().run_until_done("test public-safe mission", "unit-mission")
        self.assertTrue(result["mission_os_done_state"]["DONE"])
        self.assertTrue(result["evidence_docket"]["proof_bundles"])
        self.assertEqual(result["governed_decision_state"]["production_authority"], False)
        self.assertTrue(result["governed_decision_state"]["human_review_required"])


if __name__ == "__main__":
    unittest.main()
