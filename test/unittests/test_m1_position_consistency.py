"""Tests for consistency between peptide and protein positions."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module01.src.algorithm.check_data import check_pep_pos, double_check_data
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


class TestM1BatchValidation(unittest.TestCase):
    def run_batch(self, **bad_values):
        good = {
            "unip_id_a": "P00001", "unip_id_b": "P00002",
            "seq_a": "MKAAKT", "seq_b": "MGKT",
            "pep_a": "AKT", "pep_b": "GKT",
            "pos_a": 5, "pos_b": 3, "res_pos_a": 2, "res_pos_b": 2,
        }
        records = [
            dict(good, label="before"),
            dict(good, label="bad", **bad_values),
            dict(good, unip_id_a="P00003", label="after"),
        ]
        with TemporaryDirectory() as temp_dir:
            result = double_check_data(
                pd.DataFrame(records, index=[10, 20, 30]), "input",
                build_xl_dataset("K"), temp_dir + "/", 0,
            )
            log_text = (Path(temp_dir) / "input_preprocessing.log").read_text()
        return result, log_text

    def test_invalid_peptide_positions_do_not_abort_the_batch(self):
        for site in ("a", "b"):
            for value in (0, -1, 1.5, 4, "bad"):
                with self.subTest(site=site, position=value):
                    result, log_text = self.run_batch(**{f"res_pos_{site}": value})
                    self.assertEqual(result["label"].tolist(), ["before", "after"])
                    self.assertIn(f"20_{site}", log_text)
                    self.assertEqual(log_text.count("\tREMOVE\n"), 1)

    def test_residue_rule_conflicts_do_not_abort_the_batch(self):
        for site in ("a", "b"):
            with self.subTest(site=site):
                result, log_text = self.run_batch(**{f"res_pos_{site}": 1})
                self.assertEqual(result["label"].tolist(), ["before", "after"])
                self.assertIn("cross-link residue rules", log_text)
                self.assertIn(f"20_{site}", log_text)
                self.assertEqual(log_text.count("\tREMOVE\n"), 1)

    def test_failed_alignment_is_logged_and_removed(self):
        result, log_text = self.run_batch(
            seq_a="MAAAA", pep_a="AKT", pos_a=1, res_pos_a=2,
        )
        self.assertEqual(result["label"].tolist(), ["before", "after"])
        self.assertIn("Could not correct protein position", log_text)
        self.assertIn("20_a", log_text)
        self.assertEqual(log_text.count("\tREMOVE\n"), 1)

    def test_removed_record_does_not_generate_repeated_peptide_candidates(self):
        result, log_text = self.run_batch(
            seq_a="MAKTAKT", pep_a="AKT", pos_a=3, res_pos_a=0,
        )
        self.assertEqual(result["label"].tolist(), ["before", "after"])
        self.assertEqual(result.index.tolist(), [10, 30])
        self.assertIn("20_a", log_text)
        self.assertEqual(log_text.count("\tREMOVE\n"), 1)


if __name__ == "__main__":
    unittest.main()
