"""Prepare strictly mapped AF endpoints for distance calculation."""

import json
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser

from claudio.module02.src_distance_reevaluation.algorithm.af_complex_mapping import (
    prepare_complex_distance_input,
)
from claudio.utils.utils import build_xl_dataset


FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"


class TestAFComplexMappingAdapter(unittest.TestCase):
    def setUp(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        chains = {record["chainId"]: record for record in records}
        self.data = pd.DataFrame([{
            "source_record_id": "record_000001",
            "candidate_id": "candidate_000001",
            "experiment": "condition_A",
            "af_match_status": "matched",
            "af_model_id": "AF-0000000208747029",
            "af_model_version": 1,
            "af_metadata_path": str(FIXTURE_DIR / "metadata.json"),
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "unip_id_a": chains["A"]["uniprotAccession"],
            "unip_id_b": chains["B"]["uniprotAccession"],
            "seq_a": chains["A"]["sequence"],
            "seq_b": chains["B"]["sequence"],
            "chain_a": "A",
            "chain_b": "B",
            "original_pos_a": 67,
            "original_pos_b": 10,
            "pos_a": 67,
            "pos_b": 11,
            "position_status_a": "valid",
            "position_status_b": "corrected",
        }], index=pd.Index(["7_1"], name="candidate_index"))

    def test_preserves_model_and_source_when_preparing_endpoints(self):
        data = self.data.copy()
        original = data.copy(deep=True)

        result = prepare_complex_distance_input(data, build_xl_dataset("K"))

        pd.testing.assert_frame_equal(data, original)
        pd.testing.assert_frame_equal(result[original.columns], original)
        pd.testing.assert_index_equal(result.index, original.index)
        row = result.iloc[0]
        self.assertTrue(row["res_criteria_fulfilled"])

        expected = {
            "a": (67, 81.17, (20.938, 33.286, 12.461)),
            "b": (11, 56.86, (-41.383, 25.017, 10.236)),
        }
        for site, (number, confidence, coordinates) in expected.items():
            with self.subTest(site=site):
                self.assertEqual(row[f"mapping_status_{site}"], "mapped")
                self.assertEqual(row[f"pdb_pos_{site}"], number)
                self.assertEqual(row[f"pdb_hetflag_{site}"], " ")
                self.assertEqual(row[f"pdb_icode_{site}"], " ")
                self.assertEqual(row[f"mapping_atom_{site}"], "CB")
                self.assertEqual(row[f"method_{site}"], "alphafold")
                self.assertAlmostEqual(row[f"pLDDT_{site}"], confidence, places=2)
                np.testing.assert_allclose(
                    row[f"mapping_coord_{site}"], coordinates, atol=0.001
                )


    def test_unresolved_endpoint_clears_old_distance_fields(self):
        for site in ("a", "b"):
            for status in ("ambiguous", "invalid"):
                with self.subTest(site=site, status=status):
                    data = self.data.copy()
                    data[f"position_status_{site}"] = status
                    data[f"pdb_pos_{site}"] = 999
                    data[f"pLDDT_{site}"] = 99.0
                    data[f"res_crit_{site}"] = True
                    data["res_criteria_fulfilled"] = True
                    original = data.copy(deep=True)

                    row = prepare_complex_distance_input(
                        data, build_xl_dataset("K")
                    ).iloc[0]

                    pd.testing.assert_frame_equal(data, original)
                    self.assertFalse(row["res_criteria_fulfilled"])
                    self.assertEqual(row[f"mapping_reason_{site}"], "unresolved_position")
                    self.assertTrue(pd.isna(row[f"pdb_pos_{site}"]))
                    self.assertTrue(pd.isna(row[f"pLDDT_{site}"]))
                    self.assertFalse(row[f"res_crit_{site}"])
                    other = "b" if site == "a" else "a"
                    self.assertEqual(row[f"mapping_status_{other}"], "mapped")
                    self.assertTrue(row[f"res_crit_{other}"])

    def test_reversed_records_keep_their_endpoint_assignments(self):
        forward = self.data.iloc[0].copy()
        reverse = forward.copy()
        for field in (
            "unip_id", "seq", "chain", "original_pos", "pos", "position_status"
        ):
            reverse[f"{field}_a"] = forward[f"{field}_b"]
            reverse[f"{field}_b"] = forward[f"{field}_a"]
        reverse["source_record_id"] = "record_000002"
        data = pd.DataFrame(
            [forward, reverse],
            index=pd.Index([7, "7_1"], name="candidate_index"),
        )
        result = prepare_complex_distance_input(data, build_xl_dataset("K"))

        pd.testing.assert_frame_equal(result[data.columns], data)
        self.assertTrue(result["res_criteria_fulfilled"].all())
        for site, other in (("a", "b"), ("b", "a")):
            self.assertEqual(
                result.iloc[0][f"mapped_residue_id_{site}"],
                result.iloc[1][f"mapped_residue_id_{other}"],
            )
            np.testing.assert_allclose(
                result.iloc[0][f"mapping_coord_{site}"],
                result.iloc[1][f"mapping_coord_{other}"],
            )
            self.assertEqual(
                result.iloc[0][f"pLDDT_{site}"],
                result.iloc[1][f"pLDDT_{other}"],
            )

    def test_uses_configured_ca_for_glycine(self):
        data = self.data.copy()
        model = next(MMCIFParser(QUIET=True).get_structure(
            "fixture", str(FIXTURE_DIR / "AF-0000000208747029.cif")
        ).get_models())
        expected = {}
        for site in ("a", "b"):
            row = data.iloc[0]
            position = row[f"seq_{site}"].index("G") + 1
            data[f"pos_{site}"] = position
            atom = model[row[f"chain_{site}"]][(" ", position, " ")]["CA"]
            expected[site] = atom

        result = prepare_complex_distance_input(
            data, build_xl_dataset("G:CA:")
        ).iloc[0]
        self.assertTrue(result["res_criteria_fulfilled"])
        for site, atom in expected.items():
            self.assertEqual(result[f"mapping_atom_{site}"], "CA")
            np.testing.assert_allclose(
                result[f"mapping_coord_{site}"], atom.get_coord()
            )
            self.assertAlmostEqual(
                result[f"pLDDT_{site}"], atom.get_bfactor(), places=2
            )

        missing_cb = prepare_complex_distance_input(
            data, build_xl_dataset("G")
        ).iloc[0]
        self.assertFalse(missing_cb["res_criteria_fulfilled"])
        self.assertEqual(missing_cb["mapping_reason_a"], "missing_atom")
        self.assertIsNone(missing_cb["mapping_coord_a"])

    def test_rejects_conflicting_atoms_and_inapplicable_residue_rules(self):
        for rules in ("K:CA:,K:CB:", "K:CA:1", "K:CA:-1", "G:CA:"):
            with self.subTest(rules=rules):
                row = prepare_complex_distance_input(
                    self.data, build_xl_dataset(rules)
                ).iloc[0]
                self.assertFalse(row["res_criteria_fulfilled"])
                for site in ("a", "b"):
                    self.assertEqual(
                        row[f"mapping_reason_{site}"], "no_unique_configured_atom"
                    )
                    self.assertIsNone(row[f"mapping_coord_{site}"])
                    self.assertTrue(pd.isna(row[f"pdb_pos_{site}"]))

    def test_preserves_unmatched_rows_without_reading_structure(self):
        for status in ("no_candidate_model", "no_matching_chain_pair"):
            with self.subTest(status=status):
                data = self.data.copy()
                data["af_match_status"] = status
                data["path"] = "-"
                data["af_metadata_path"] = "-"
                data["chain_a"] = "-"
                data["chain_b"] = "-"
                result = prepare_complex_distance_input(
                    data, build_xl_dataset("K")
                )
                pd.testing.assert_frame_equal(result[data.columns], data)
                row = result.iloc[0]
                self.assertFalse(row["res_criteria_fulfilled"])
                for site in ("a", "b"):
                    self.assertEqual(row[f"mapping_reason_{site}"], status)
                    self.assertTrue(pd.isna(row[f"pdb_pos_{site}"]))
                    self.assertTrue(pd.isna(row[f"pLDDT_{site}"]))

    def test_empty_input_has_distance_columns(self):
        data = self.data.iloc[:0].copy()
        result = prepare_complex_distance_input(data, build_xl_dataset("K"))
        pd.testing.assert_frame_equal(result[data.columns], data)
        self.assertTrue(result.empty)
        for column in (
            "mapping_status_a", "mapping_status_b",
            "pdb_pos_a", "pdb_pos_b", "pLDDT_a", "pLDDT_b",
            "res_criteria_fulfilled",
        ):
            self.assertIn(column, result.columns)

if __name__ == "__main__":
    unittest.main()
