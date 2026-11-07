"""Tests for mapping a table of AF complex candidates."""

import json
import unittest
from pathlib import Path

import pandas as pd

from claudio.module02.src_distance_reevaluation.algorithm.af_complex_mapping import (
    map_complex_dataset,
)


FIXTURE_DIR = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "af_complex"
)


class TestAFComplexBatchMapping(unittest.TestCase):
    def test_maps_mixed_records_and_preserves_candidate_indices(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = {
            record["chainId"]: record for record in records
        }

        first = {
            "source_record_id": "record_000001",
            "af_match_status": "matched",
            "af_model_id": "AF-0000000208747029",
            "af_model_version": 1,
            "af_metadata_path": str(FIXTURE_DIR / "metadata.json"),
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": metadata["A"]["sequence"],
            "seq_b": metadata["B"]["sequence"],
            "chain_a": "A",
            "chain_b": "B",
            "original_pos_a": 67,
            "original_pos_b": 11,
            "pos_a": 67,
            "pos_b": 11,
            "position_status_a": "valid",
            "position_status_b": "valid",
        }
        second = {**first, "pos_a": 76}
        unmatched = {
            **first,
            "source_record_id": "record_000002",
            "af_match_status": "no_candidate_model",
            "af_model_id": None,
            "af_model_version": None,
            "af_metadata_path": "-",
            "path": "-",
            "chain_a": "-",
            "chain_b": "-",
        }

        data = pd.DataFrame(
            [first, second, unmatched],
            index=pd.Index([7, "7_1", 12], name="candidate_index"),
        )
        original = data.copy(deep=True)

        result = map_complex_dataset(
            data=data,
            atom_a="CB",
            atom_b="CB",
        )

        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(
            result.loc[:, original.columns], original
        )
        pd.testing.assert_index_equal(result.index, original.index)
        self.assertEqual(len(result), 3)
        self.assertEqual(result["source_record_id"].nunique(), 2)

        for index, position in ((7, 67), ("7_1", 76)):
            self.assertEqual(result.loc[index, "mapping_status_a"], "mapped")
            self.assertEqual(result.loc[index, "mapping_status_b"], "mapped")
            self.assertEqual(
                result.loc[index, "mapped_residue_id_a"],
                (" ", position, " "),
            )
            self.assertEqual(
                result.loc[index, "mapped_residue_id_b"],
                (" ", 11, " "),
            )

        for site in ("a", "b"):
            self.assertEqual(
                result.loc[12, f"mapping_status_{site}"], "not_evaluable"
            )
            self.assertEqual(
                result.loc[12, f"mapping_reason_{site}"],
                "no_candidate_model",
            )
            self.assertIsNone(result.loc[12, f"mapped_residue_id_{site}"])
            self.assertIsNone(result.loc[12, f"mapping_coord_{site}"])
    def test_empty_input_preserves_columns_and_adds_mapping_fields(self):
        data = pd.DataFrame(
            columns=[
                "source_record_id",
                "af_match_status",
                "af_metadata_path",
                "path",
            ],
            index=pd.Index([], name="candidate_index"),
        )
        original = data.copy(deep=True)

        result = map_complex_dataset(
            data=data,
            atom_a="CB",
            atom_b="CB",
        )

        self.assertTrue(result.empty)
        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(
            result.loc[:, original.columns], original
        )
        pd.testing.assert_index_equal(result.index, original.index)

        for site in ("a", "b"):
            for field in (
                "mapping_status",
                "mapping_reason",
                "mapped_residue_id",
                "mapping_coord",
            ):
                self.assertIn(f"{field}_{site}", result.columns)

    def test_preserves_all_unmatched_records_without_reading_metadata(self):
        data = pd.DataFrame({
            "source_record_id": ["record_000001", "record_000002"],
            "af_match_status": [
                "no_candidate_model",
                "no_matching_chain_pair",
            ],
            "af_metadata_path": ["-", "-"],
            "path": ["-", "-"],
        }, index=pd.Index(
            ["none_1", "none_2"], name="candidate_index"
        ))
        original = data.copy(deep=True)

        result = map_complex_dataset(
            data=data,
            atom_a="CB",
            atom_b="CB",
        )

        self.assertEqual(len(result), 2)
        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(
            result.loc[:, original.columns], original
        )
        pd.testing.assert_index_equal(result.index, original.index)

        for site in ("a", "b"):
            self.assertEqual(
                result[f"mapping_status_{site}"].tolist(),
                ["not_evaluable", "not_evaluable"],
            )
            self.assertEqual(
                result[f"mapping_reason_{site}"].tolist(),
                original["af_match_status"].tolist(),
            )
            self.assertTrue(
                result[f"mapped_residue_id_{site}"].isna().all()
            )
            self.assertTrue(
                result[f"mapping_coord_{site}"].isna().all()
            )

if __name__ == "__main__":
    unittest.main()
