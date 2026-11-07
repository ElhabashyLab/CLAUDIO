"""Tests for mapping both endpoints of one XL-MS record."""

import json
import unittest
from pathlib import Path

import pandas as pd

from claudio.module02.src_distance_reevaluation.algorithm.af_complex_mapping import (
    map_complex_record,
)


FIXTURE_DIR = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "af_complex"
)


class TestAFComplexRecordMapping(unittest.TestCase):
    def test_maps_both_endpoints_and_preserves_source_fields(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = {
            record["chainId"]: record
            for record in records
        }

        row = pd.Series({
            "source_record_id": "record_000001",
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
            "original_pos_b": 10,
            "pos_a": 67,
            "pos_b": 11,
            "position_status_a": "valid",
            "position_status_b": "corrected",
        }, name="7_1")
        original = row.copy(deep=True)

        result = map_complex_record(
            row=row,
            records=records,
            atom_a="CB",
            atom_b="CB",
        )

        # Preserve the input, its provenance fields and candidate index.
        pd.testing.assert_series_equal(row, original)
        pd.testing.assert_series_equal(
            result.loc[original.index], original
        )
        self.assertEqual(result.name, "7_1")

        expected = {
            "a": ((" ", 67, " "), (20.938, 33.286, 12.461)),
            "b": ((" ", 11, " "), (-41.383, 25.017, 10.236)),
        }

        for site, (residue_id, coordinates) in expected.items():
            with self.subTest(site=site):
                self.assertEqual(result[f"mapping_status_{site}"], "mapped")
                self.assertIsNone(result[f"mapping_reason_{site}"])
                self.assertEqual(
                    result[f"mapped_residue_id_{site}"], residue_id
                )
                self.assertEqual(result[f"mapping_atom_{site}"], "CB")

                actual = result[f"mapping_coord_{site}"]
                self.assertEqual(len(actual), 3)
                for value, expected_value in zip(actual, coordinates):
                    self.assertAlmostEqual(
                        value, expected_value, places=3
                    )
    def test_preserves_valid_endpoint_when_other_is_unresolved(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = {
            record["chainId"]: record for record in records
        }

        template = pd.Series({
            "source_record_id": "record_000001",
            "af_model_id": "AF-0000000208747029",
            "af_model_version": 1,
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": metadata["A"]["sequence"],
            "seq_b": metadata["B"]["sequence"],
            "chain_a": "A",
            "chain_b": "B",
            "pos_a": 67,
            "pos_b": 11,
            "position_status_a": "valid",
            "position_status_b": "corrected",
        }, name="7_1")

        expected_ids = {
            "a": (" ", 67, " "),
            "b": (" ", 11, " "),
        }

        for site in ("a", "b"):
            for status in ("ambiguous", "invalid"):
                with self.subTest(site=site, status=status):
                    row = template.copy(deep=True)
                    row[f"position_status_{site}"] = status

                    # Simulate stale results from an earlier mapping.
                    row[f"mapping_status_{site}"] = "mapped"
                    row[f"mapped_residue_id_{site}"] = (" ", 999, " ")
                    row[f"mapping_coord_{site}"] = (999.0, 999.0, 999.0)
                    original = row.copy(deep=True)

                    result = map_complex_record(
                        row=row,
                        records=records,
                        atom_a="CB",
                        atom_b="CB",
                    )

                    pd.testing.assert_series_equal(row, original)
                    self.assertEqual(
                        result["source_record_id"], "record_000001"
                    )
                    self.assertEqual(result.name, "7_1")
                    self.assertEqual(
                        result[f"mapping_status_{site}"], "not_evaluable"
                    )
                    self.assertEqual(
                        result[f"mapping_reason_{site}"],
                        "unresolved_position",
                    )
                    self.assertIsNone(
                        result[f"mapped_residue_id_{site}"]
                    )
                    self.assertIsNone(result[f"mapping_coord_{site}"])

                    other = "b" if site == "a" else "a"
                    self.assertEqual(
                        result[f"mapping_status_{other}"], "mapped"
                    )
                    self.assertEqual(
                        result[f"mapped_residue_id_{other}"],
                        expected_ids[other],
                    )
                    self.assertIsNotNone(
                        result[f"mapping_coord_{other}"]
                    )
    def test_preserves_records_without_a_usable_structure(self):
        for status in ("no_candidate_model", "no_matching_chain_pair"):
            with self.subTest(af_match_status=status):
                has_model = status == "no_matching_chain_pair"

                source = pd.Series({
                    "source_record_id": "record_000002",
                    "af_match_status": status,
                    "af_model_id": (
                        "AF-0000000208747029" if has_model else None
                    ),
                    "af_model_version": 1 if has_model else None,
                    "path": "-",
                    "unip_id_a": "TEST_A",
                    "unip_id_b": "TEST_B",
                    "seq_a": "AK",
                    "seq_b": "MK",
                    "pos_a": 2,
                    "pos_b": 2,
                    "chain_a": "-",
                    "chain_b": "-",
                    "position_status_a": "valid",
                    "position_status_b": "valid",
                }, name="12")

                row = source.copy(deep=True)
                for site in ("a", "b"):
                    row[f"mapped_residue_id_{site}"] = (" ", 999, " ")
                    row[f"mapping_coord_{site}"] = (999.0, 999.0, 999.0)
                original = row.copy(deep=True)

                result = map_complex_record(
                    row=row,
                    records=[],
                    atom_a="CB",
                    atom_b="CB",
                )

                pd.testing.assert_series_equal(row, original)
                pd.testing.assert_series_equal(
                    result.loc[source.index], source
                )

                for site in ("a", "b"):
                    self.assertEqual(
                        result[f"mapping_status_{site}"],
                        "not_evaluable",
                    )
                    self.assertEqual(
                        result[f"mapping_reason_{site}"], status
                    )
                    self.assertIsNone(
                        result[f"mapped_residue_id_{site}"]
                    )
                    self.assertIsNone(
                        result[f"mapping_coord_{site}"]
                    )
    def test_rejects_model_identity_or_version_mismatch(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        metadata = {
            record["chainId"]: record for record in records
        }

        template = pd.Series({
            "source_record_id": "record_000001",
            "af_match_status": "matched",
            "af_model_id": "AF-0000000208747029",
            "af_model_version": 1,
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "seq_a": metadata["A"]["sequence"],
            "seq_b": metadata["B"]["sequence"],
            "chain_a": "A",
            "chain_b": "B",
            "pos_a": 67,
            "pos_b": 11,
            "position_status_a": "valid",
            "position_status_b": "valid",
        }, name="7_1")

        cases = (
            (
                "af_model_id",
                "AF-9999999999999999",
                "model_identity_mismatch",
            ),
            (
                "af_model_version",
                2,
                "model_version_mismatch",
            ),
        )

        for field, wrong_value, expected_reason in cases:
            with self.subTest(field=field):
                row = template.copy(deep=True)
                row[field] = wrong_value
                original = row.copy(deep=True)

                result = map_complex_record(
                    row=row,
                    records=records,
                    atom_a="CB",
                    atom_b="CB",
                )

                pd.testing.assert_series_equal(row, original)
                pd.testing.assert_series_equal(
                    result.loc[original.index], original
                )

                for site in ("a", "b"):
                    self.assertEqual(
                        result[f"mapping_status_{site}"],
                        "not_evaluable",
                    )
                    self.assertEqual(
                        result[f"mapping_reason_{site}"],
                        expected_reason,
                    )
                    self.assertIsNone(
                        result[f"mapped_residue_id_{site}"]
                    )
                    self.assertIsNone(
                        result[f"mapping_coord_{site}"]
                    )
if __name__ == "__main__":
    unittest.main()
