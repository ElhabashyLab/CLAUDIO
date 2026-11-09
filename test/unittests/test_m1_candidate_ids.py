"""Identify shared residue-pair candidates without losing source rows."""
import unittest
from tempfile import TemporaryDirectory

import pandas as pd
from pathlib import Path

from claudio.module01.src.io.read_in import read_inputfile
from claudio.module01.src.io.write_out import write_outputs
from claudio.utils.utils import build_xl_dataset
from claudio.module01.src.algorithm.check_data import (
    assign_candidate_ids,
    double_check_data,
)

class TestM1CandidateIds(unittest.TestCase):
    def test_shared_candidates_keep_each_sources_positions_and_conditions(self):
        records = []
        for number, position in enumerate((3, 6), start=1):
            records.append({
                "source_record_id": f"record_{number:06d}",
                "unip_id_a": "P1", "unip_id_b": "P2",
                "seq_a": "MAKTAKT", "seq_b": "MGKT",
                "pep_a": "AKT", "pep_b": "GKT",
                "pos_a": position, "pos_b": 3,
                "res_pos_a": 2, "res_pos_b": 2,
                "original_pos_a": position, "original_pos_b": 3,
                "experiment": f"condition_{number}",
            })

        with TemporaryDirectory() as folder:
            result = double_check_data(
                pd.DataFrame(records), "shared_candidates",
                build_xl_dataset("K"), folder + "/", 0,
            )

        self.assertIn("candidate_id", result.columns)
        self.assertEqual(len(result), 4)
        self.assertFalse(result["candidate_id"].isna().any())
        self.assertEqual(result["candidate_id"].nunique(), 2)

        groups = list(result.groupby(["pos_a", "pos_b"]))
        self.assertEqual({pair for pair, _ in groups}, {(3, 3), (6, 3)})
        for pair, group in groups:
            with self.subTest(pair=pair):
                self.assertEqual(group["candidate_id"].nunique(), 1)
                self.assertEqual(len(group), 2)
                self.assertEqual(
                    set(group["source_record_id"]),
                    {"record_000001", "record_000002"},
                )

        for record in records:
            with self.subTest(source=record["source_record_id"]):
                source_rows = result[
                    result["source_record_id"] == record["source_record_id"]
                ]
                self.assertTrue(
                    source_rows["original_pos_a"].eq(record["original_pos_a"]).all()
                )
                self.assertTrue(
                    source_rows["experiment"].eq(record["experiment"]).all()
                )
                self.assertTrue(source_rows["position_status_a"].eq("valid").all())
                self.assertTrue(source_rows["position_status_b"].eq("valid").all())
    def test_identity_uses_complete_endpoints_and_ignores_their_order(self):
        first = {
            "unip_id_a": "P1", "unip_id_b": "P2",
            "seq_a": "MAKTAKT", "seq_b": "MGKT",
            "pos_a": 3, "pos_b": 3,
            "position_status_a": "valid", "position_status_b": "valid",
        }
        reversed_row = {}
        for field in ("unip_id", "seq", "pos", "position_status"):
            reversed_row[f"{field}_a"] = first[f"{field}_b"]
            reversed_row[f"{field}_b"] = first[f"{field}_a"]

        rows = [
            first,
            reversed_row,
            {**first, "unip_id_a": "P3"},
            {**first, "seq_a": "MAKSAKT"},
            {**first, "pos_a": 6},
            {**first, "position_status_a": "corrected"},
        ]
        for number, row in enumerate(rows, start=1):
            row["source_record_id"] = f"record_{number:06d}"

        data = pd.DataFrame(rows, index=[7, 12, 19, 23, 31, 40])
        original = data.copy(deep=True)
        result = assign_candidate_ids(data)
        ids = result["candidate_id"].tolist()

        self.assertEqual(ids[0], ids[1])
        self.assertEqual(ids[0], ids[5])
        self.assertEqual(len(set(ids)), 4)
        for index in (2, 3, 4):
            self.assertNotEqual(ids[0], ids[index])
        pd.testing.assert_frame_equal(result[original.columns], original)

    def test_unresolved_positions_have_no_candidate_id(self):
        rows = []
        for site in ("a", "b"):
            for status in ("ambiguous", "invalid", None, pd.NA):
                row = {
                    "unip_id_a": "P1", "unip_id_b": "P2",
                    "seq_a": "MAKTAKT", "seq_b": "MGKT",
                    "pos_a": 3, "pos_b": 3,
                    "position_status_a": "valid",
                    "position_status_b": "valid",
                }
                row[f"position_status_{site}"] = status
                rows.append(row)

        data = pd.DataFrame(rows)
        original = data.copy(deep=True)
        result = assign_candidate_ids(data)

        self.assertTrue(result["candidate_id"].isna().all())
        pd.testing.assert_frame_equal(result[original.columns], original)
    def test_preserves_candidate_ids_in_report_and_filters_sqcs(self):
        first = {
            "source_record_id": "record_000001",
            "unip_id_a": "P1", "unip_id_b": "P2",
            "seq_a": "MAKTAKT", "seq_b": "MGKT",
            "pos_a": 3, "pos_b": 3,
            "position_status_a": "valid", "position_status_b": "valid",
            "experiment": "condition_1",
        }
        second = {
            **first,
            "source_record_id": "record_000002",
            "position_status_a": "ambiguous",
            "experiment": "condition_2",
        }
        data = pd.DataFrame([first, second], index=[7, 12])
        original = data.copy(deep=True)
        expected = assign_candidate_ids(data)

        with TemporaryDirectory() as folder:
            write_outputs(
                expected, pd.DataFrame(), "candidate_ids", folder + "/", 0
            )
            saved = pd.read_csv(
                Path(folder) / "candidate_ids.sqcs", index_col=0
            )
            report = pd.read_csv(Path(folder) / "candidate_ids_record_tracking.csv", index_col=0)

        self.assertNotIn("candidate_id", saved.columns)
        self.assertEqual(saved.index.tolist(), [7])
        self.assertEqual(report.loc[7, "candidate_id"], expected.loc[7, "candidate_id"])
        self.assertTrue(pd.isna(report.loc[12, "candidate_id"]))
        self.assertFalse(report.loc[12, "included_in_sqcs"])
        self.assertEqual(saved["experiment"].tolist(), ["condition_1"])

    def test_rejects_candidate_id_from_input_or_column_projection(self):
        record = {
            "unip_id_a": "P1", "unip_id_b": "P2",
            "pep_a": "AKT", "pep_b": "GKT",
            "pos_a": 3, "pos_b": 3,
            "res_pos_a": 2, "res_pos_b": 2,
        }
        for column, projections in (
            ("candidate_id", {}),
            ("external_id", {"external_id": "candidate_id"}),
        ):
            with self.subTest(column=column):
                with TemporaryDirectory() as folder:
                    path = Path(folder) / "input.csv"
                    pd.DataFrame([{
                        **record, column: "existing_candidate",
                    }]).to_csv(path, index=False)

                    with self.assertRaisesRegex(ValueError, "candidate_id"):
                        read_inputfile(str(path), projections)
if __name__ == "__main__":
    unittest.main()
