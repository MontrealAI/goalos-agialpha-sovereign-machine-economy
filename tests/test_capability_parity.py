import unittest
from src.goalos_ascension.parity import audit


class CapabilityParityTests(unittest.TestCase):
    def test_public_capability_matrix_is_covered(self):
        report = audit(".")
        self.assertEqual(report["status"], "passed")
        self.assertEqual(report["capabilities_checked"], report["capabilities_covered"])
        self.assertFalse(report["boundary"]["production_authority"])


if __name__ == "__main__":
    unittest.main()
