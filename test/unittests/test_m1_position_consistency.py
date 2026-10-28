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
    def test_repairs_invalid_peptide_positions(self):
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

                corrected, log_text = check_pep_pos(
                    0, row, "a", build_xl_dataset("K"), "", 0,
                )

                self.assertIsNotNone(corrected)
                self.assertEqual(corrected["pos_a"], 5)
                self.assertEqual(corrected["res_pos_a"], 2)
                self.assertEqual(corrected["original_pos_a"], 5)
                self.assertIn("Invalid peptide position", log_text)

    def test_reports_ambiguous_correction_without_peptide_position(self):
        row = pd.Series({
            "seq_a": "MKAAKAKT",
            "pep_a": "AKAKT",
            "pos_a": 2,
            "res_pos_a": float("nan"),
            "original_pos_a": 2,
            "source_record_id": "record_000001",
        })
        before = row.copy(deep=True)

        checked, log_text = check_pep_pos(
            0, row, "a", build_xl_dataset("K"), "", 0,
        )

        self.assertIsNone(checked)
        pd.testing.assert_series_equal(row, before)
        self.assertIn("AMBIGUOUS", log_text)
        self.assertNotIn("REPLACE:", log_text)

    def test_repairs_peptide_position_with_disallowed_residue(self):
        row = pd.Series({
            "seq_a": "MKAAKT",
            "pep_a": "AKT",
            "pos_a": 5,
            "res_pos_a": 1,
            "original_pos_a": 5,
            "source_record_id": "record_000001",
        })

        corrected, log_text = check_pep_pos(
            0, row, "a", build_xl_dataset("K"), "", 0,
        )

        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 5)
        self.assertEqual(corrected["res_pos_a"], 2)
        self.assertIn("cross-link residue rules", log_text)


class TestM1PositionRecovery(unittest.TestCase):
    def make_record(self, label="valid", **changes):
        row = {
            "unip_id_a": "P00001", "unip_id_b": "P00002",
            "seq_a": "MKAAKT", "seq_b": "MGKT",
            "pep_a": "AKT", "pep_b": "GKT",
            "pos_a": 5, "pos_b": 3,
            "res_pos_a": 2, "res_pos_b": 2,
            "label": label,
        }
        row.update(changes)
        return row

    def check_batch(self, records):
        with TemporaryDirectory() as temp_dir:
            result = double_check_data(
                pd.DataFrame(records), "input", build_xl_dataset("K"),
                temp_dir + "/", 0,
            )
            log_text = (Path(temp_dir) / "input_preprocessing.log").read_text()
        return result, log_text

    def test_repairs_invalid_position_for_either_endpoint(self):
        for site in ("a", "b"):
            for value in (0, -1, 1.5, 4, float("inf"), "bad", True):
                with self.subTest(site=site, position=value):
                    row = pd.Series(self.make_record())
                    row[f"res_pos_{site}"] = value
                    corrected, _ = check_pep_pos(
                        0, row, site, build_xl_dataset("K"), "", 0,
                    )
                    self.assertIsNotNone(corrected)
                    self.assertEqual(corrected[f"pos_{site}"], 5 if site == "a" else 3)
                    self.assertEqual(corrected[f"res_pos_{site}"], 2)

    def test_repairs_wrong_protein_and_invalid_peptide_positions(self):
        row = pd.Series(self.make_record(pos_a=2, res_pos_a=0))
        corrected, _ = check_pep_pos(0, row, "a", build_xl_dataset("K"), "", 0)
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 5)
        self.assertEqual(corrected["res_pos_a"], 2)

    def test_uses_supported_protein_position_when_peptide_has_multiple_sites(self):
        row = pd.Series(self.make_record(
            seq_a="MAKAKT", pep_a="AKAKT", pos_a=5, res_pos_a=0,
        ))
        corrected, _ = check_pep_pos(0, row, "a", build_xl_dataset("K"), "", 0)
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 5)
        self.assertEqual(corrected["res_pos_a"], 4)

    def test_recovers_invalid_position_using_sequence_alignment(self):
        row = pd.Series(self.make_record(
            seq_a="MAAKSTG", pep_a="AAKTTG", pos_a=1, res_pos_a=0,
        ))
        corrected, log_text = check_pep_pos(
            0, row, "a", build_xl_dataset("K"), "", 0,
        )
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 4)
        self.assertEqual(corrected["res_pos_a"], 3)
        self.assertIn("align", log_text.lower())

    def test_does_not_choose_first_of_repeated_alignment_candidates(self):
        row = pd.Series(self.make_record(
            seq_a="MAAKSTGAAKSTG", pep_a="AAKTTG", pos_a=1, res_pos_a=0,
        ))
        corrected, log_text = check_pep_pos(
            0, row, "a", build_xl_dataset("K"), "", 0,
        )
        self.assertIsNone(corrected)
        self.assertIn("AMBIGUOUS", log_text)
        self.assertNotIn("REPLACE:", log_text)

    def test_does_not_map_an_absent_crosslinked_residue(self):
        row = pd.Series(self.make_record(
            seq_a="MAAATG", pep_a="AAKATG", pos_a=1, res_pos_a=0,
        ))
        corrected, _ = check_pep_pos(0, row, "a", build_xl_dataset("K"), "", 0)
        self.assertIsNone(corrected)

    def test_recovery_respects_protein_terminal_residue_rules(self):
        row = pd.Series(self.make_record(
            seq_a="QAMKT", pep_a="AMK", pos_a=1, res_pos_a=0,
        ))
        corrected, _ = check_pep_pos(
            0, row, "a", build_xl_dataset("K,M:CA:1"), "", 0,
        )
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 4)
        self.assertEqual(corrected["res_pos_a"], 3)

    def test_keeps_valid_records_after_an_unrecoverable_a_endpoint(self):
        bad = self.make_record("bad", seq_a="MAAAA", pep_a="AAA", pos_a=1, res_pos_a=1)
        good = self.make_record("good")
        result, log_text = self.check_batch([bad, good])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertIn("0_a", log_text)
        self.assertIn("REMOVE", log_text)

    def test_keeps_valid_records_after_an_unrecoverable_b_endpoint(self):
        bad = self.make_record("bad", seq_b="MAAAA", pep_b="AAA", pos_b=1, res_pos_b=1)
        good = self.make_record("good")
        result, log_text = self.check_batch([bad, good])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertIn("0_b", log_text)
        self.assertIn("REMOVE", log_text)

    def test_removed_repeated_record_cannot_generate_candidates(self):
        bad = self.make_record("bad", seq_a="MAKTAKT", pep_a="AKT", pos_a=1, res_pos_a=0)
        result, log_text = self.check_batch([bad, self.make_record("good")])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertEqual(len(result), 1)
        self.assertIn("AMBIGUOUS", log_text)
        self.assertIn("REMOVE", log_text)

    def test_drops_failed_realignments_with_a_valid_peptide_position(self):
        bad = self.make_record("bad", seq_a="MAAAA", pep_a="AKT", pos_a=1, res_pos_a=2)
        result, log_text = self.check_batch([bad, self.make_record("good")])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertIn("align", log_text.lower())
        self.assertIn("REMOVE", log_text)

    def test_all_failed_records_leave_an_empty_result_and_removal_log(self):
        records = [
            self.make_record("bad_a", seq_a="MAAAA", pep_a="AAA", pos_a=1, res_pos_a=1),
            self.make_record("bad_b", seq_b="MAAAA", pep_b="AAA", pos_b=1, res_pos_b=1),
        ]
        result, log_text = self.check_batch(records)
        self.assertTrue(result.empty)
        self.assertEqual(log_text.count("\tREMOVE\n"), 2)

    def test_recovers_missing_peptide_position_using_alignment(self):
        row = pd.Series(self.make_record(
            seq_a="MAAKSTG", pep_a="AAKTTG", pos_a=1, res_pos_a=float("nan"),
        ))
        corrected, _ = check_pep_pos(0, row, "a", build_xl_dataset("K"), "", 0)
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 4)
        self.assertEqual(corrected["res_pos_a"], 3)

    def test_alignment_can_map_the_last_protein_residue(self):
        row = pd.Series(self.make_record(
            seq_a="MAAKSTK", pep_a="AAKTTK", pos_a=7, res_pos_a=0,
        ))
        corrected, _ = check_pep_pos(0, row, "a", build_xl_dataset("K"), "", 0)
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected["pos_a"], 7)
        self.assertEqual(corrected["res_pos_a"], 6)


    def test_empty_sequence_does_not_stop_the_batch(self):
        bad = self.make_record("bad", seq_a="", res_pos_a=0)
        result, log_text = self.check_batch([bad, self.make_record("good")])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertIn("REMOVE", log_text)

    def test_empty_peptide_does_not_stop_the_batch(self):
        bad = self.make_record("bad", pep_a="", res_pos_a=0)
        result, log_text = self.check_batch([bad, self.make_record("good")])
        self.assertEqual(result["label"].tolist(), ["good"])
        self.assertIn("REMOVE", log_text)

    def test_excessive_alignment_ties_do_not_select_a_truncated_candidate_set(self):
        row = pd.Series(self.make_record(
            seq_a="MAAKSTG" * 1001, pep_a="AAKTTG", pos_a=4, res_pos_a=0,
        ))
        corrected, log_text = check_pep_pos(
            0, row, "a", build_xl_dataset("K"), "", 0,
        )
        self.assertIsNone(corrected)
        self.assertIn("too many optimal alignments", log_text)

    def test_bad_record_does_not_prevent_written_output_from_reaching_m3(self):
        from claudio.module01.src.io.read_in import read_inputfile
        from claudio.module01.src.io.write_out import write_outputs
        from claudio.module03.src.io.read_in import read_in
        from claudio.module03.src.algorithm.signal_analysis import analyse_homo_signals
        from claudio.utils.utils import clean_dataset

        records = [
            self.make_record("bad", seq_a="MAAAA", pos_a=1, res_pos_a=2),
            self.make_record("good"),
        ]
        projections = {name: name for name in (
            "pep_a", "pep_b", "pos_a", "pos_b",
            "res_pos_a", "res_pos_b", "unip_id_a", "unip_id_b",
        )}
        with TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "input.csv"
            pd.DataFrame(records).to_csv(input_path, index=False)
            data = read_inputfile(str(input_path), projections)
            checked = double_check_data(
                data, "input", build_xl_dataset("K"), temp_dir + "/", 0,
            )
            write_outputs(
                clean_dataset(checked), pd.DataFrame({"protein_id": []}),
                "input", temp_dir + "/", 0,
            )
            ops = analyse_homo_signals(
                read_in(str(Path(temp_dir) / "input.sqcs")), 0,
            )

        self.assertEqual(ops["label"].tolist(), ["good"])
        self.assertEqual(ops.iloc[0]["pos_a"], 5)
        self.assertEqual(ops.iloc[0]["pos_b"], 3)
        self.assertIn("homo_adjacency", ops)
        self.assertIn("homo_pep_overl", ops)


if __name__ == "__main__":
    unittest.main()
