"""Tests for preserving protein-position pairs during M1 deduplication."""

import unittest
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.utils.utils import build_xl_dataset


class TestM1Deduplication(unittest.TestCase):
    def test_keeps_distinct_protein_position_pairs(self):
        data = pd.DataFrame([
            {
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
            },
            {
                "unip_id_a": "P00001",
                "unip_id_b": "P00002",
                "seq_a": "MAKDGK",
                "seq_b": "MVKEAK",
                "pep_a": "DGK",
                "pep_b": "VKE",
                "pos_a": 6,
                "pos_b": 3,
                "res_pos_a": 3,
                "res_pos_b": 2,
                "source_record_id": "record_000002",
            },
        ])

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                data,
                "deduplication_test",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )

        self.assertEqual(
            len(result),
            2,
            "Different protein-position pairs must both be retained",
        )
        self.assertEqual(
            set(result["source_record_id"]),
            {"record_000001", "record_000002"},
        )
        self.assertEqual(
            set(zip(
                result["unip_id_a"],
                result["pos_a"],
                result["unip_id_b"],
                result["pos_b"],
            )),
            {
                ("P00001", 3, "P00002", 6),
                ("P00001", 6, "P00002", 3),
            },
        )
    def test_removes_duplicate_with_reversed_endpoints(self):
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

        reversed_record = {
            "source_record_id": "record_000002",
        }
        for field in ("unip_id", "seq", "pep", "pos", "res_pos"):
            reversed_record[f"{field}_a"] = first[f"{field}_b"]
            reversed_record[f"{field}_b"] = first[f"{field}_a"]

        data = pd.DataFrame([first, reversed_record])

        with TemporaryDirectory() as output_dir:
            result = double_check_data(
                data,
                "reversed_endpoints_test",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )

        self.assertEqual(len(result), 1)
        row = result.iloc[0]
        self.assertEqual(row["source_record_id"], "record_000001")
        self.assertEqual(
            (
                row["unip_id_a"], row["pos_a"],
                row["unip_id_b"], row["pos_b"],
            ),
            ("P00001", 3, "P00002", 6),
        )
    def test_removes_duplicate_with_identical_endpoints(self):
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
                "identical_endpoints_test",
                build_xl_dataset("K"),
                output_dir + "/",
                0,
            )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result.iloc[0]["source_record_id"],
            "record_000001",
        )
if __name__ == "__main__":
    unittest.main()
