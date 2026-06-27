import unittest
from src.goalos_ascension.aep001 import EvidenceDocket61, ProofGradient, build_reference_commit, build_reference_run


class AEP001ConformanceTests(unittest.TestCase):
    def test_reference_commit_run_and_selection_certificate(self):
        commit = build_reference_commit("test objective")
        run = build_reference_run(commit)
        self.assertIn("goalos_commit", run)
        self.assertIn("proof_packet", run)
        self.assertTrue(run["selection_certificate"]["hard_gates"]["RollbackReady"])

    def test_evidence_docket_61_requires_replay_and_cost(self):
        validator = EvidenceDocket61()
        result = validator.validate({"manifest": {}, "claims_matrix": []})
        self.assertEqual(result["status"], "needs_revision")
        self.assertIn("replay_path", result["missing"])

    def test_proof_gradient_hard_gates_are_mandatory(self):
        pg = ProofGradient()
        score = pg.score(quality_delta=1, transfer=1, verified_value=1, evidence_integrity=1, cost_delta=0, risk=0, coordination_overhead=0, rollback_debt=0)
        denied = pg.promote(score, {"ProofValid": True, "RollbackReady": False})
        self.assertFalse(denied.promoted)
        allowed = pg.promote(score, {"ProofValid": True, "RollbackReady": True, "EvalPass": True})
        self.assertTrue(allowed.promoted)


if __name__ == "__main__":
    unittest.main()
