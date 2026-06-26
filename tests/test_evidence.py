import unittest
from src.goalos_ascension.evidence import summarize_evidence, proof_velocity


class EvidenceGateTests(unittest.TestCase):
    def test_placeholders_do_not_count_as_market_evidence(self):
        summary = summarize_evidence([{"evidence_status":"example_placeholder","category":"commercial"}])
        self.assertEqual(summary.counted_items, 0)
        self.assertFalse(summary.public_scale_claim_allowed)
        self.assertEqual(summary.state, "infrastructure_ready_market_evidence_pending")

    def test_verified_full_category_set_allows_candidate_state(self):
        cats = ["product","usage","customer_discovery","design_partner","pilot","benchmark","commercial","independent_validation","fair_value_support","governance"]
        summary = summarize_evidence([{"evidence_status":"third_party_verified","category":c} for c in cats])
        self.assertTrue(summary.public_scale_claim_allowed)
        self.assertEqual(summary.state, "strategic_scale_evidence_candidate")

    def test_proof_velocity_ignores_placeholders(self):
        metrics = proof_velocity([{"evidence_status":"example_placeholder","metrics":{"capability_reused":True}}])
        self.assertEqual(metrics["counted_events"], 0)
        self.assertEqual(metrics["capability_reuse_events"], 0)

if __name__ == "__main__":
    unittest.main()
