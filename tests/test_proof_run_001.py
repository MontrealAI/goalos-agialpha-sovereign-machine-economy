import tempfile
import unittest
from pathlib import Path
from src.goalos_ascension.proof_run import run_proof_run_001


class ProofRun001Tests(unittest.TestCase):
    def test_proof_run_writes_docket_and_report(self):
        with tempfile.TemporaryDirectory() as td:
            result = run_proof_run_001(Path(td))
            self.assertEqual(result["report"]["status"], "passed")
            self.assertTrue((Path(td) / "proof-run-001-docket.json").exists())
            self.assertFalse(result["report"]["production_authority"])


if __name__ == "__main__":
    unittest.main()
