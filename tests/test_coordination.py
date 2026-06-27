import unittest
from src.goalos_ascension.coordination import CoordinationEngine


class CoordinationEngineTests(unittest.TestCase):
    def test_routing_selects_validator_and_returns_evidence_hash(self):
        result = CoordinationEngine().route()
        self.assertIn("validator.v0", result.selected_agents)
        self.assertTrue(result.evidence_bundle_hash.startswith("sha256:"))
        self.assertEqual(result.route_family, "R0_hamiltonian_baseline")


if __name__ == "__main__":
    unittest.main()
