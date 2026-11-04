"""Preserve the distinction between TopoLink distances and lower bounds."""

import io
import shlex
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import PDBIO
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import calc_site_distances
from claudio.module02.src_distance_reevaluation.io.write_out import write_output
from claudio.module04.src.algorithm.combine_reevals import combine_inter_reevaluations
from claudio.module04.src.io.write_outs import write_outputs
from claudio.utils.utils import clean_dataset


class TestM2DistanceBounds(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        model = Model(0)
        chain = Chain("A")
        model.add(chain)
        for number, x in ((1, 0.0), (2, 10.0), (3, 30.0)):
            residue = Residue((" ", number, " "), "LYS", " ")
            residue.add(Atom(
                "CB", np.array([x, 0.0, 0.0]), 90.0, 1.0,
                " ", " CB ", number, element="C",
            ))
            chain.add(residue)
        structure_path = self.root / "model_1AAA.pdb"
        writer = PDBIO()
        writer.set_structure(model)
        writer.save(str(structure_path))
        base = {
            "path": str(structure_path), "pdb_id": "1AAA",
            "pdb_method": "X-RAY DIFFRACTION", "pdb_resolution": 2.0,
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "KKK", "seq_b": "KKK",
            "pep_a": "KKK", "pep_b": "KKK",
            "res_pos_a": 1, "res_pos_b": 2,
            "pep_a_repeated": False, "pep_b_repeated": False,
            "pep_a_repeat_count": 1, "pep_b_repeat_count": 1,
            "chain_a": "A", "chain_b": "A",
            "method_a": "realigning", "method_b": "realigning",
            "pLDDT_a": 90.0, "pLDDT_b": 90.0,
            "res_criteria_fulfilled": True, "is_interfaced": True,
        }
        self.data = pd.DataFrame([
            {
                **base, "source_record_id": "record_000001",
                "pos_a": 1, "pos_b": 2, "pdb_pos_a": 1, "pdb_pos_b": 2,
            },
            {
                **base, "source_record_id": "record_000002",
                "pos_a": 2, "pos_b": 3, "pdb_pos_a": 2, "pdb_pos_b": 3,
            },
        ], index=[7, 23])

    def compute(self, euclidean="10.000", topological="12.000", data=None,
                missing=False):
        def topolink(command):
            input_path = Path(shlex.split(command)[-1])
            observed = [
                line.strip() for line in input_path.read_text().splitlines()
                if line.strip().startswith("observed ")
            ]
            self.assertEqual(observed, [
                "observed LYS A 1 LYS A 2",
                "observed LYS A 2 LYS A 3",
            ])
            if missing:
                return io.StringIO("")
            return io.StringIO(
                f"  LINK: LYS A 1 CB LYS A 2 CB {euclidean} {topological}\n"
                "  LINK: LYS A 2 CB LYS A 3 CB 20.000 22.000\n"
            )

        with patch.object(calc_site_distances.os, "popen", side_effect=topolink) as run:
            result = calc_site_distances.compute_dists_with_topolink(
                (self.data if data is None else data).copy(),
                str(self.root / "work") + "/",
                pd.DataFrame([{"res": "K", "atom": "CB"}]), 70.0, None, 0,
            )
        run.assert_called_once()
        return result

    def test_keeps_lower_bounds_separate_from_exact_distances(self):
        cases = [
            ("10.000", ">12.3456", 10.0, None, None, 12.3456),
            (">10.000", "12.000", None, 12.0, 10.0, None),
            (">10.000", ">12.000", None, None, 10.0, 12.0),
            ("10.000", "12.000", 10.0, 12.0, None, None),
        ]
        for euclidean, topological, exact_e, exact_t, bound_e, bound_t in cases:
            with self.subTest(euclidean=euclidean, topological=topological):
                result = self.compute(euclidean, topological)
                self.assertEqual(result.index.tolist(), [7, 23])
                self.assertEqual(result.source_record_id.tolist(),
                                 self.data.source_record_id.tolist())
                for column, expected in (
                    ("eucl_dist_tplk", exact_e), ("topo_dist_tplk", exact_t),
                    ("eucl_dist_lower_bound", bound_e),
                    ("topo_dist_lower_bound", bound_t),
                ):
                    self.assertIn(column, result.columns)
                    if expected is None:
                        self.assertTrue(pd.isna(result.loc[7, column]), column)
                    else:
                        self.assertEqual(result.loc[7, column], expected, column)
                self.assertEqual(result.loc[7, "eucl_dist_raw"], euclidean)
                self.assertEqual(result.loc[7, "topo_dist_raw"], topological)
                self.assertEqual(result.loc[23, "eucl_dist_tplk"], 20.0)
                self.assertEqual(result.loc[23, "topo_dist_tplk"], 22.0)
                self.assertTrue(pd.isna(result.loc[23, "topo_dist_lower_bound"]))

    def previous_results(self):
        data = self.data.copy()
        for prefix in ("eucl", "topo"):
            data[f"{prefix}_dist_tplk"] = 99.0
            data[f"{prefix}_dist_lower_bound"] = 98.7654
            data[f"{prefix}_dist_raw"] = ">98.7654"
        return data

    def test_recalculation_clears_old_bounds_and_replaces_raw_values(self):
        result = self.compute(data=self.previous_results())
        for prefix in ("eucl", "topo"):
            self.assertTrue(result[f"{prefix}_dist_lower_bound"].isna().all())
        self.assertEqual(result.loc[7, "eucl_dist_tplk"], 10.0)
        self.assertEqual(result.loc[7, "topo_dist_tplk"], 12.0)
        self.assertEqual(result.loc[7, "eucl_dist_raw"], "10.000")
        self.assertEqual(result.loc[7, "topo_dist_raw"], "12.000")

    def test_missing_results_clear_all_previous_distance_fields(self):
        result = self.compute(data=self.previous_results(), missing=True)
        for prefix in ("eucl", "topo"):
            for suffix in ("tplk", "lower_bound", "raw"):
                column = f"{prefix}_dist_{suffix}"
                self.assertTrue(result[column].isna().all(), column)

    def test_invalid_tokens_are_retained_without_numeric_results(self):
        for token in ("NaN", "inf", "-1", "<12", "missing", ">NaN", ">-1"):
            with self.subTest(token=token):
                result = self.compute(topological=token)
                self.assertTrue(pd.isna(result.loc[7, "topo_dist_tplk"]))
                self.assertIn("topo_dist_lower_bound", result.columns)
                self.assertTrue(pd.isna(result.loc[7, "topo_dist_lower_bound"]))
                self.assertEqual(result.loc[7, "topo_dist_raw"], token)

    def test_bounds_survive_m2_csv_and_m4_final_output(self):
        data = clean_dataset(self.compute(topological=">12.3456"))
        m2_path = self.root / "sample.sqcs_structdi.csv"
        write_output(data, str(m2_path))
        data = pd.read_csv(m2_path, index_col=0)
        self.assertTrue(pd.isna(data.loc[7, "topo_dist"]))
        self.assertIn("topo_dist_lower_bound", data.columns)
        self.assertEqual(data.loc[7, "topo_dist_lower_bound"], 12.3456)
        self.assertEqual(data.loc[7, "topo_dist_raw"], ">12.3456")

        data["homo_adjacency"] = 0.0
        data["homo_int_overl"] = 0.0
        data["homo_pep_overl"] = False
        data["swiss_model_homology"] = ""
        data = combine_inter_reevaluations(
            data, 70.0, 5.0, 35.0, None, 50.0, 0.5, False,
        )
        self.assertFalse(data.loc[7, "XL_confirmed"])
        self.assertTrue(data.loc[23, "XL_confirmed"])
        write_outputs(data, "sample", False, str(self.root) + "/")
        saved = pd.read_csv(self.root / "sample_final.csv", index_col=0)
        self.assertTrue(pd.isna(saved.loc[7, "topo_dist"]))
        self.assertEqual(saved.loc[7, "topo_dist_lower_bound"], 12.3456)
        self.assertEqual(saved.loc[7, "topo_dist_raw"], ">12.3456")
        self.assertEqual(saved.source_record_id.tolist(),
                         self.data.source_record_id.tolist())


if __name__ == "__main__":
    unittest.main()
