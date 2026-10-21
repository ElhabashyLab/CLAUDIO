"""Tests for respecting M1 position statuses during M3 analysis."""

import unittest

import pandas as pd

from claudio.module03.src.algorithm.signal_analysis import (
    analyse_homo_signals,
)


class TestM3PositionStatus(unittest.TestCase):
    def test_does_not_score_unresolved_positions(self):
        for site in ("a", "b"):
            for status in ("ambiguous", "invalid"):
                with self.subTest(site=site, status=status):
                    record = {
                        "unip_id_a": "TEST_PROTEIN",
                        "unip_id_b": "TEST_PROTEIN",
                        "seq_a": "MKAAKAKT",
                        "seq_b": "MKAAKAKT",
                        "pep_a": "AKAKT",
                        "pep_b": "MKA",
                        "pos_a": 2,
                        "pos_b": 2,
                        "position_status_a": "valid",
                        "position_status_b": "valid",
                        "source_record_id": "record_000001",
                    }
                    record[f"position_status_{site}"] = status

                    result = analyse_homo_signals(
                        pd.DataFrame([record]), 0
                    )
                    row = result.iloc[0]

                    self.assertEqual(len(result), 1)
                    self.assertEqual(
                        row["source_record_id"], "record_000001"
                    )
                    self.assertTrue(
                        pd.isna(row["homo_adjacency"]),
                        "Unresolved positions must not receive adjacency scores",
                    )
                    self.assertTrue(
                        pd.isna(row["homo_int_overl"]),
                        "Unresolved positions must not receive overlap scores",
                    )
                    self.assertTrue(
                        pd.isna(row["homo_pep_overl"]),
                        "Not evaluated must remain distinct from False",
                    )

    def test_scores_supported_and_legacy_records(self):
        cases = (
            ("valid", "valid"),
            ("corrected", "valid"),
            ("valid", "corrected"),
            ("corrected", "corrected"),
            None,
        )

        for statuses in cases:
            with self.subTest(statuses=statuses):
                record = {
                    "unip_id_a": "TEST_PROTEIN",
                    "unip_id_b": "TEST_PROTEIN",
                    "seq_a": "MKAAKT",
                    "seq_b": "MKAAKT",
                    "pep_a": "AKT",
                    "pep_b": "MKA",
                    "pos_a": 5,
                    "pos_b": 2,
                    "source_record_id": "record_000001",
                }
                if statuses is not None:
                    record["position_status_a"] = statuses[0]
                    record["position_status_b"] = statuses[1]

                result = analyse_homo_signals(
                    pd.DataFrame([record]), 0
                )
                row = result.iloc[0]

                self.assertEqual(row["homo_adjacency"], 0.5)
                self.assertEqual(row["homo_int_overl"], 0.0)
                self.assertFalse(row["homo_pep_overl"])
                self.assertEqual(
                    row["source_record_id"], "record_000001"
                )

if __name__ == "__main__":
    unittest.main()
