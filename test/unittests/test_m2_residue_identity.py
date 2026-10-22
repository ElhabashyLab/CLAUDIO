"""Preserve complete structure residue identities after sequence mapping."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import PDBIO
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import search_pdb_pos


class TestM2ResidueIdentity(unittest.TestCase):

    def test_preserves_insertion_code_for_each_endpoint(self):
        model = Model(0)
        chain = Chain("A")
        model.add(chain)
        residues = [
            ((" ", 1, " "), 0.0),
            ((" ", 1, "A"), 20.0),
            ((" ", 2, " "), 30.0),
            ((" ", 3, " "), 40.0),
        ]
        for serial, (residue_id, x) in enumerate(residues, start=1):
            residue = Residue(residue_id, "LYS", " ")
            residue.add(
                Atom(
                    "CB",
                    np.array([x, 0.0, 0.0], dtype=float),
                    90.0,
                    1.0,
                    " ",
                    " CB ",
                    serial,
                    element="C",
                )
            )
            chain.add(residue)

        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "test_1ABC.pdb")
            writer = PDBIO()
            writer.set_structure(model)
            writer.save(path)

            data = pd.DataFrame(
                [
                    {
                        "source_record_id": "record_000001",
                        "path": path,
                        "pdb_id": "1ABC",
                        "pdb_method": "X-RAY DIFFRACTION",
                        "pdb_resolution": 2.0,
                        "chain_a": "A",
                        "chain_b": "A",
                        "unip_id_a": "P1",
                        "unip_id_b": "P1",
                        "seq_a": "KKKK",
                        "seq_b": "KKKK",
                        "pos_a": 2,
                        "pos_b": 3,
                    }
                ],
                index=[7],
            )
            mapping = pd.DataFrame(columns=["PDB", "CHAIN", "SP_PRIMARY"])
            with patch.object(
                search_pdb_pos, "pdb_cache", {}
            ), patch.object(
                search_pdb_pos.pd, "read_csv", return_value=mapping
            ), patch.object(
                search_pdb_pos.r,
                "get",
                side_effect=AssertionError("Unexpected network request"),
            ):
                result = search_pdb_pos.search_site_pos_in_pdb(
                    data,
                    pd.DataFrame([{"res": "K", "atom": "CB"}]),
                    0,
                )

        checked = result.loc[7]
        self.assertTrue(checked["res_criteria_fulfilled"])
        for site, expected in (("a", (" ", 1, "A")), ("b", (" ", 2, " "))):
            with self.subTest(site=site):
                for prefix in ("pdb_hetflag", "pdb_icode"):
                    self.assertIn(f"{prefix}_{site}", result.columns)
                actual = (
                    checked[f"pdb_hetflag_{site}"],
                    checked[f"pdb_pos_{site}"],
                    checked[f"pdb_icode_{site}"],
                )
                self.assertEqual(actual, expected)
        self.assertEqual(checked["source_record_id"], "record_000001")



if __name__ == "__main__":
    unittest.main()
