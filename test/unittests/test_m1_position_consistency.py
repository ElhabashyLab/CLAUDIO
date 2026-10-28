"""Tests for consistency between peptide and protein positions."""

import unittest

import pandas as pd

from claudio.module01.src.algorithm.check_data import check_pep_pos
from claudio.utils.utils import build_xl_dataset


class TestM1PositionConsistency(unittest.TestCase):
    def test_corrects_wrong_position_even_when_it_is_lysine(self):
        row = pd.Series({
            "seq_a": "MKAAKT",
            "pep_a": "AKT",
            "pos_a": 2,
            "res_pos_a": 2,
            "original_pos_a": 2,
            "source_record_id": "record_000001",
        })

        corrected, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(
            corrected["pos_a"],
            5,
            "The position must match the cross-linked K in peptide AKT",
        )
        self.assertEqual(corrected["original_pos_a"], 2)
        self.assertEqual(
            corrected["source_record_id"],
            "record_000001",
        )
        self.assertEqual(
            corrected["position_status_a"],
            "corrected",
        )
    def test_uses_supplied_position_when_peptide_has_two_lysines(self):
        row = pd.Series({
            "seq_a": "MAKAKT",
            "pep_a": "AKAKT",
            "pos_a": 3,
            "res_pos_a": 4,
            "original_pos_a": 3,
            "source_record_id": "record_000001",
        })

        corrected, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(corrected["pos_a"], 5)
        self.assertEqual(corrected["original_pos_a"], 3)
    def test_keeps_valid_position_in_second_peptide_occurrence(self):
        row = pd.Series({
            "seq_a": "MAKTAKT",
            "pep_a": "AKT",
            "pos_a": 6,
            "res_pos_a": 2,
            "original_pos_a": 6,
            "source_record_id": "record_000001",
        })

        checked, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(checked["pos_a"], 6)
        self.assertEqual(checked["original_pos_a"], 6)
    def test_corrects_unique_site_without_peptide_position(self):
        row = pd.Series({
            "seq_a": "MKAAKT",
            "pep_a": "AKT",
            "pos_a": 2,
            "res_pos_a": float("nan"),
            "original_pos_a": 2,
            "source_record_id": "record_000001",
        })

        corrected, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(
            corrected["pos_a"],
            5,
            "A unique peptide and unique K identify protein position 5",
        )
        self.assertEqual(corrected["original_pos_a"], 2)
        self.assertEqual(
            corrected["source_record_id"],
            "record_000001",
        )
    def test_keeps_supported_site_without_peptide_position(self):
        row = pd.Series({
            "seq_a": "MAKAKT",
            "pep_a": "AKAKT",
            "pos_a": 5,
            "res_pos_a": float("nan"),
            "original_pos_a": 5,
            "source_record_id": "record_000001",
        })

        checked, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(checked["pos_a"], 5)
        self.assertEqual(checked["original_pos_a"], 5)
    def test_rejects_invalid_peptide_positions(self):
        for invalid_position in (0, -1, 1.5, 4):
            with self.subTest(position=invalid_position):
                row = pd.Series({
                    "seq_a": "MKAAKT",
                    "pep_a": "AKT",
                    "pos_a": 5,
                    "res_pos_a": invalid_position,
                    "original_pos_a": 5,
                    "source_record_id": "record_000001",
                })

                with self.assertRaisesRegex(
                    ValueError, "Invalid peptide position"
                ):
                    check_pep_pos(
                        0,
                        row,
                        "a",
                        build_xl_dataset("K"),
                        "",
                        0,
                    )
    def test_reports_ambiguous_correction_without_peptide_position(self):
        row = pd.Series({
            "seq_a": "MKAAKAKT",
            "pep_a": "AKAKT",
            "pos_a": 2,
            "res_pos_a": float("nan"),
            "original_pos_a": 2,
            "source_record_id": "record_000001",
        })

        checked, log_text = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(checked["pos_a"], 2)
        self.assertEqual(checked["original_pos_a"], 2)
        self.assertIn("AMBIGUOUS", log_text)
        self.assertNotIn("REPLACE:", log_text)
        self.assertEqual(
            checked["position_status_a"],
            "ambiguous",
        )
    def test_rejects_peptide_position_with_disallowed_residue(self):
        row = pd.Series({
            "seq_a": "MKAAKT",
            "pep_a": "AKT",
            "pos_a": 5,
            "res_pos_a": 1,
            "original_pos_a": 5,
            "source_record_id": "record_000001",
        })

        with self.assertRaisesRegex(
            ValueError,
            "Peptide position does not satisfy cross-link residue rules",
        ):
            check_pep_pos(
                0,
                row,
                "a",
                build_xl_dataset("K"),
                "",
                0,
            )
    def test_marks_consistent_position_as_valid_for_each_endpoint(self):
        for site in ("a", "b"):
            with self.subTest(site=site):
                row = pd.Series({
                    f"seq_{site}": "MAAKT",
                    f"pep_{site}": "AKT",
                    f"pos_{site}": 4,
                    f"res_pos_{site}": 2,
                    f"original_pos_{site}": 4,
                    "source_record_id": "record_000001",
                })

                checked, _ = check_pep_pos(
                    0,
                    row,
                    site,
                    build_xl_dataset("K"),
                    "",
                    0,
                )

                status_column = f"position_status_{site}"
                self.assertIn(status_column, checked.index)
                self.assertEqual(checked[status_column], "valid")
                self.assertEqual(checked[f"pos_{site}"], 4)
    def test_marks_unresolvable_position_as_invalid(self):
        row = pd.Series({
            "seq_a": "MAAAT",
            "pep_a": "AAA",
            "pos_a": 2,
            "res_pos_a": float("nan"),
            "original_pos_a": 2,
            "source_record_id": "record_000001",
        })

        checked, _ = check_pep_pos(
            0,
            row,
            "a",
            build_xl_dataset("K"),
            "",
            0,
        )

        self.assertEqual(checked["position_status_a"], "invalid")
        self.assertEqual(checked["pos_a"], 2)
        self.assertEqual(checked["original_pos_a"], 2)
if __name__ == "__main__":
    unittest.main()
