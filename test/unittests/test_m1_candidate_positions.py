"""Tests for valid position combinations during candidate expansion."""

import unittest
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.utils.utils import build_xl_dataset
from claudio.module01.src.algorithm.check_data import create_duplicates

class TestM1CandidatePositions(unittest.TestCase):
    def test_expands_both_endpoints_without_spurious_positions(self):
        sequence = "MAKTAKTGKTGKT"
        data = pd.DataFrame([{
            "unip_id_a": "TEST_PROTEIN",
            "unip_id_b": "TEST_PROTEIN",
            "seq_a": sequence,
            "seq_b": sequence,
            "pep_a": "AKT",
            "pep_b": "GKT",
            "pos_a": 3,
            "pos_b": 9,
            "res_pos_a": 2,
            "res_pos_b": 2,
            "original_pos_a": 3,
            "original_pos_b": 9,
            "source_record_id": "record_000001",
        }])

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                data,
                "candidate_positions",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )

        self.assertEqual(
            set(zip(result["pos_a"], result["pos_b"])),
            {(3, 9), (3, 12), (6, 9), (6, 12)},
        )
        self.assertEqual(len(result), 4)
        self.assertEqual(
            set(result["source_record_id"]),
            {"record_000001"},
        )
    def test_rechecks_status_for_new_candidate_position(self):
        row = pd.Series({
            "unip_id_a": "TEST_PROTEIN",
            "unip_id_b": "TEST_PROTEIN",
            "seq_a": "MAKTAKTGKT",
            "seq_b": "MAKTAKTGKT",
            "pep_a": "AKT",
            "pep_b": "GKT",
            "pos_a": 3,
            "pos_b": 9,
            "res_pos_a": 2,
            "res_pos_b": 2,
            "original_pos_a": 3,
            "original_pos_b": 9,
            "source_record_id": "record_000001",
            "position_status_a": "invalid",
            "position_status_b": "valid",
        })

        candidates, _ = create_duplicates(
            row, build_xl_dataset("K"), ""
        )

        self.assertEqual(len(candidates), 1)
        candidate = candidates.iloc[0]
        self.assertEqual(candidate["pos_a"], 6)
        self.assertEqual(candidate["pos_b"], 9)
        self.assertEqual(candidate["position_status_a"], "valid")
        self.assertEqual(candidate["position_status_b"], "valid")
        self.assertEqual(candidate["original_pos_a"], 3)
        self.assertEqual(
            candidate["source_record_id"], "record_000001"
        )

    def test_rejects_candidate_outside_the_matched_peptide(self):
        row = pd.Series({
            "unip_id_a": "TEST_PROTEIN",
            "unip_id_b": "TEST_PROTEIN",
            "seq_a": "MKAKTAKT",
            "seq_b": "MKAKTAKT",
            "pep_a": "AKT",
            "pep_b": "MKA",
            "pos_a": 2,
            "pos_b": 2,
            "res_pos_a": 2,
            "res_pos_b": 2,
            "original_pos_a": 2,
            "original_pos_b": 2,
            "source_record_id": "record_000001",
            "position_status_a": "invalid",
            "position_status_b": "valid",
        })

        candidates, log_text = create_duplicates(
            row, build_xl_dataset("K"), ""
        )

        self.assertEqual(
            set(zip(candidates["pos_a"], candidates["pos_b"])),
            {(4, 2), (7, 2)},
        )
        self.assertEqual(len(candidates), 2)
        self.assertTrue(
            candidates["position_status_a"].eq("valid").all()
        )
    def test_rejects_candidates_with_invalid_unchanged_endpoint(self):
        row = pd.Series({
            "unip_id_a": "TEST_PROTEIN",
            "unip_id_b": "TEST_PROTEIN",
            "seq_a": "MAKTAKTGKT",
            "seq_b": "MAKTAKTGKT",
            "pep_a": "AKT",
            "pep_b": "GKT",
            "pos_a": 3,
            "pos_b": 3,
            "res_pos_a": 2,
            "res_pos_b": 2,
            "original_pos_a": 3,
            "original_pos_b": 3,
            "source_record_id": "record_000001",
        })

        candidates, log_text = create_duplicates(
            row, build_xl_dataset("K"), ""
        )

        self.assertTrue(candidates.empty)
        self.assertIn("REJECT candidate", log_text)
if __name__ == "__main__":
    unittest.main()
