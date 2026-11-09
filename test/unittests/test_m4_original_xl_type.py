"""Preserve the XL type before M4 applies score and evidence reevaluation."""

import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from click.testing import CliRunner

from claudio.module04.src.algorithm.combine_reevals import combine_inter_reevaluations


class TestM4OriginalXLType(unittest.TestCase):
    def setUp(self):
        self.row = {
            "unip_id_a": "P1", "unip_id_b": "P1",
            "chain_a": "A", "chain_b": "A", "pos_a": 3, "pos_b": 9,
            "pep_a": "AKT", "pep_b": "GKT", "res_pos_a": 2, "res_pos_b": 2,
            "seq_a": "MAKTAKTGKT", "seq_b": "MAKTAKTGKT",
            "pep_a_repeated": False, "pep_b_repeated": False,
            "pep_a_repeat_count": 1, "pep_b_repeat_count": 1,
            "path": "-", "pdb_id": "1ABC", "pdb_method": "X-RAY DIFFRACTION",
            "pdb_resolution": 2., "pdb_pos_a": 3, "pdb_pos_b": 9,
            "pLDDT_a": "-", "pLDDT_b": "-", "is_interfaced": True,
            "eucl_dist": 15., "topo_dist": 20.,
            "homo_adjacency": 0., "homo_int_overl": 0., "homo_pep_overl": False,
        }

    def combine(self, rows, scoring=False):
        data = rows if isinstance(rows, pd.DataFrame) else pd.DataFrame(rows)
        return combine_inter_reevaluations(
            data, plddt_cutoff=70, linker_minimum=5, linker_maximum=35,
            euclidean_strictness=None, distance_maximum=50, cutoff=0.25,
            compute_scoring=scoring,
        )

    def test_uses_the_initial_protein_identity_rule_when_no_type_is_supplied(self):
        data = pd.DataFrame([
            self.row,
            {**self.row, "chain_b": "B"},
            {**self.row, "unip_id_b": "P2", "chain_b": "B"},
        ], index=["4", "4_1", "9"])
        result = self.combine(data)
        self.assertEqual(result["original_XL_type"].tolist(), ["intra", "intra", "inter"])
        self.assertEqual(result["XL_type"].tolist(), ["intra", "inter", "inter"])
        self.assertEqual(result.index.tolist(), ["4", "4_1", "9"])

    def test_overlap_can_change_intra_to_inter_without_losing_the_original(self):
        result = self.combine([{**self.row, "homo_pep_overl": True, "homo_int_overl": 1.}]).iloc[0]
        self.assertEqual(result["original_XL_type"], "intra")
        self.assertEqual(result["XL_type"], "inter")
        self.assertEqual(result["evidence"], "'peptides overlap'")
        self.assertTrue(result["XL_confirmed"])

    def test_distance_evidence_keeps_its_existing_classification_behavior(self):
        result = self.combine([{**self.row, "eucl_dist": 38., "topo_dist": 40.}]).iloc[0]
        self.assertEqual(result["original_XL_type"], "intra")
        self.assertEqual(result["XL_type"], "inter")
        self.assertEqual(result["evidence"], "'distance above range'")
        self.assertFalse(result["XL_confirmed"])

    def test_copies_a_supplied_type_before_it_is_overwritten(self):
        result = self.combine([{**self.row, "XL_type": "inter"}]).iloc[0]
        self.assertEqual(result["original_XL_type"], "inter")
        self.assertEqual(result["XL_type"], "intra")

    def test_rerunning_m4_keeps_the_first_original_type(self):
        first = self.combine([{**self.row, "XL_type": "inter"}])
        self.assertEqual(first.iloc[0]["XL_type"], "intra")
        second = self.combine(first.copy())
        self.assertEqual(second.iloc[0]["original_XL_type"], "inter")
        self.assertEqual(second.iloc[0]["XL_type"], "intra")

    def test_optional_scoring_does_not_replace_the_original_type(self):
        for scoring in (False, True):
            with self.subTest(scoring=scoring):
                result = self.combine([
                    self.row,
                    {**self.row, "homo_pep_overl": True, "homo_int_overl": 1.},
                ], scoring=scoring)
                self.assertEqual(result["original_XL_type"].tolist(), ["intra", "intra"])
                self.assertEqual(result["XL_type"].tolist(), ["intra", "inter"])
                if scoring:
                    self.assertEqual(result["inter_score"].tolist(), [0., 0.5])
                    self.assertEqual(result["score_XL_type"].tolist(), ["intra", "inter"])
                else:
                    self.assertNotIn("inter_score", result)

    def test_existing_original_values_including_missing_ones_are_not_overwritten(self):
        result = self.combine([
            {**self.row, "original_XL_type": "inter"},
            {**self.row, "original_XL_type": pd.NA},
        ])
        self.assertEqual(result.iloc[0]["original_XL_type"], "inter")
        self.assertTrue(pd.isna(result.iloc[1]["original_XL_type"]))

    def test_original_type_reaches_extended_final_and_protein_pair_csv_outputs(self):
        main = importlib.import_module("claudio.module04.src.main")
        rows = pd.DataFrame([
            self.row,
            {**self.row, "homo_pep_overl": True, "homo_int_overl": 1.},
            {**self.row, "unip_id_b": "P2", "chain_b": "B"},
        ])
        ops_columns = ["homo_adjacency", "homo_int_overl", "homo_pep_overl"]
        with TemporaryDirectory() as directory:
            root = Path(directory)
            structural = root / "example.sqcs_structdi.csv"
            ops = root / "example.sqcs_ops.csv"
            output = root / "output"
            rows.drop(columns=ops_columns).to_csv(structural)
            rows[ops_columns].to_csv(ops)

            with patch.object(main, "retrieve_oligomeric_states", side_effect=lambda frame, verbose: frame.assign(swiss_model_homology="")), patch.object(main, "setup_pml_scripts"), patch.object(main, "create_plots"):
                result = CliRunner().invoke(main.main, [
                    "-i", str(structural), "-i2", str(ops), "-o", str(output),
                    "-s", "False", "-v", "0",
                ])
            self.assertEqual(result.exit_code, 0, result.output + repr(result.exception))

            for name in ("example_extended.csv", "example_final.csv"):
                frame = pd.read_csv(output / name, index_col=0)
                self.assertIn("assigned_XL_type", frame.columns)
                self.assertNotIn("XL_type", frame.columns)
                self.assertEqual(frame["original_XL_type"].tolist(), ["intra", "intra", "inter"])
                self.assertEqual(frame["assigned_XL_type"].tolist(), ["intra", "inter", "inter"])
                self.assertEqual(frame.columns.tolist().count("original_XL_type"), 1)
                self.assertEqual(frame.columns.get_loc("assigned_XL_type"), frame.columns.get_loc("original_XL_type") + 1)

            homomer = pd.read_csv(output / "homomers/P1/P1_.csv")
            heteromer = pd.read_csv(output / "heteromers/P1_P2/P1_P2_.csv")
            self.assertEqual(homomer["original_XL_type"].tolist(), ["intra", "intra"])
            self.assertEqual(homomer["assigned_XL_type"].tolist(), ["intra", "inter"])
            self.assertEqual(heteromer["original_XL_type"].tolist(), ["inter"])

            self.assertEqual(
                heteromer["assigned_XL_type"].tolist(), ["inter"]
            )
            for _frame in (homomer, heteromer):
                self.assertIn("assigned_XL_type", _frame.columns)
                self.assertNotIn("XL_type", _frame.columns)
