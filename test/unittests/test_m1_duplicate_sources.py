"""Tests for tracing removed duplicates to retained input records."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.utils.utils import build_xl_dataset


class TestM1DuplicateSources(unittest.TestCase):
    def test_writes_source_link_for_removed_duplicate(self):
        first = {
            "unip_id_a": "P00001",
            "unip_id_b": "P00002",
            "seq_a": "MAKDGK",
            "seq_b": "MVKEAK",
            "pep_a": "AKD",
            "pep_b": "EAK",
            "pos_a": 3,
            "pos_b": 6,
            "res_pos_a": 2,
            "res_pos_b": 3,
            "source_record_id": "record_000001",
        }
        duplicate = first.copy()
        duplicate["source_record_id"] = "record_000002"

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                pd.DataFrame([first, duplicate]),
                "input",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )

            self.assertEqual(len(result), 1)
            self.assertEqual(
                result.iloc[0]["source_record_id"],
                "record_000001",
            )

            report_path = Path(output_dir) / "input_duplicate_sources.csv"
            self.assertTrue(
                report_path.is_file(),
                "M1 must write a duplicate-source report",
            )

            report = pd.read_csv(report_path)
            self.assertEqual(
                report.to_dict(orient="records"),
                [{
                    "retained_source_record_id": "record_000001",
                    "duplicate_source_record_id": "record_000002",
                }],
            )
    def test_links_all_duplicates_to_first_record(self):
        first = {
            "unip_id_a": "P00001",
            "unip_id_b": "P00002",
            "seq_a": "MAKDGK",
            "seq_b": "MVKEAK",
            "pep_a": "AKD",
            "pep_b": "EAK",
            "pos_a": 3,
            "pos_b": 6,
            "res_pos_a": 2,
            "res_pos_b": 3,
            "source_record_id": "record_000001",
        }

        second = first.copy()
        second["source_record_id"] = "record_000002"

        third = {"source_record_id": "record_000003"}
        for field in ("unip_id", "seq", "pep", "pos", "res_pos"):
            third[f"{field}_a"] = first[f"{field}_b"]
            third[f"{field}_b"] = first[f"{field}_a"]

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                pd.DataFrame([first, second, third]),
                "input",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )
            report = pd.read_csv(
                Path(output_dir) / "input_duplicate_sources.csv"
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result.iloc[0]["source_record_id"],
            "record_000001",
        )
        self.assertEqual(len(report), 2)
        self.assertEqual(
            set(zip(
                report["retained_source_record_id"],
                report["duplicate_source_record_id"],
            )),
            {
                ("record_000001", "record_000002"),
                ("record_000001", "record_000003"),
            },
        )
    def test_overwrites_old_report_when_no_duplicates_exist(self):
        record = {
            "unip_id_a": "P00001",
            "unip_id_b": "P00002",
            "seq_a": "MAKDGK",
            "seq_b": "MVKEAK",
            "pep_a": "AKD",
            "pep_b": "EAK",
            "pos_a": 3,
            "pos_b": 6,
            "res_pos_a": 2,
            "res_pos_b": 3,
            "source_record_id": "record_000001",
        }

        with TemporaryDirectory() as output_dir:
            report_path = Path(output_dir) / "input_duplicate_sources.csv"

            # Simulate a report left by an earlier run.
            report_path.write_text(
                "retained_source_record_id,duplicate_source_record_id\n"
                "old_record_1,old_record_2\n",
                encoding="utf-8",
            )

            result = double_check_data(
                pd.DataFrame([record]),
                "input",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )
            report = pd.read_csv(report_path)

        self.assertEqual(len(result), 1)
        self.assertTrue(report.empty)
        self.assertEqual(
            report.columns.tolist(),
            [
                "retained_source_record_id",
                "duplicate_source_record_id",
            ],
        )
    def test_removed_duplicate_does_not_generate_candidates(self):
        first = {
            "unip_id_a": "P00001",
            "unip_id_b": "P00002",
            "seq_a": "MAKTAKT",
            "seq_b": "MGKT",
            "pep_a": "AKT",
            "pep_b": "GKT",
            "pos_a": 3,
            "pos_b": 3,
            "res_pos_a": 2,
            "res_pos_b": 2,
            "source_record_id": "record_000001",
        }
        duplicate = first.copy()
        duplicate["source_record_id"] = "record_000002"

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                pd.DataFrame([first, duplicate]),
                "input",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )
            report = pd.read_csv(
                Path(output_dir) / "input_duplicate_sources.csv"
            )

        self.assertEqual(
            set(result["source_record_id"]),
            {"record_000001"},
            "Removed duplicate sources must not reappear as candidates",
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(
            set(zip(result["pos_a"], result["pos_b"])),
            {(3, 3), (6, 3)},
        )
        self.assertEqual(
            report.to_dict(orient="records"),
            [{
                "retained_source_record_id": "record_000001",
                "duplicate_source_record_id": "record_000002",
            }],
        )
if __name__ == "__main__":
    unittest.main()
