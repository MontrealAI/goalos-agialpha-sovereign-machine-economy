import json
import unittest
from pathlib import Path

from src.goalos_ascension import ProofKernel, hash_payload


class ProofKernelTests(unittest.TestCase):
    def test_hash_is_stable(self):
        self.assertEqual(hash_payload({"b": 2, "a": 1}), hash_payload({"a": 1, "b": 2}))

    def test_example_docket_reaches_settlement_gate(self):
        docket = json.loads(Path("examples/evidence-docket.example.json").read_text(encoding="utf-8"))
        decision = ProofKernel().evaluate_docket(docket)
        self.assertEqual(decision.state, "READY_FOR_SETTLEMENT")
        self.assertTrue(decision.evidence_hash.startswith("sha256:"))

    def test_blocked_claim_phrase(self):
        docket = json.loads(Path("examples/evidence-docket.example.json").read_text(encoding="utf-8"))
        docket["claim_boundary"] = "achieved AGI"
        decision = ProofKernel().evaluate_docket(docket)
        self.assertEqual(decision.state, "BLOCKED")


if __name__ == "__main__":
    unittest.main()
