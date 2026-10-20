"""Check coordinate bookkeeping when a PDB residue falls back to AlphaFold."""
import unittest
from unittest.mock import patch
import tempfile
from pathlib import Path
from Bio.PDB import PDBIO
import numpy as np
import pandas as pd
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import (
    search_pdb_pos,
)


class TestM2AFFallback(unittest.TestCase):
    @staticmethod
    def make_chain(positions):
        chain = Chain("A")
        for number, x in positions:
            residue = Residue((" ", number, " "), "LYS", " ")
            residue.add(
                Atom(
                    "CB",
                    np.array([x, 0.0, 0.0], dtype=float),
                    90.0 + number,
                    1.0,
                    " ",
                    " CB ",
                    number,
                    element="C",
                )
            )
            chain.add(residue)
        return chain

    def test_fallback_resets_position_method_and_confidence(self):
        original_model = Model(0)
        original_model.add(self.make_chain([(2, 2.0)]))
        af_chain = self.make_chain([(1, 100.0), (2, 200.0), (3, 300.0)])
        replacement_path = "replacement_afP1.pdb"

        # SIFTS maps UniProt position 2 to PDB position 3.
        # Position 3 is absent in the original PDB.
        mapping = pd.DataFrame(
            [
                {
                    "PDB": "1ABC",
                    "CHAIN": "A",
                    "SP_PRIMARY": "P1",
                    "SP_BEG": 1,
                    "SP_END": 3,
                    "PDB_BEG": 2,
                    "PDB_END": 4,
                }
            ]
        )
        row = pd.Series(
            {
                "path": "original.pdb",
                "pdb_id": "1ABC",
                "chain_a": "A",
                "unip_id_a": "P1",
                "seq_a": "KKK",
                "pos_a": 2,
            }
        )

        with patch.dict(
            search_pdb_pos.pdb_cache,
            {"original.pdb": [original_model]},
            clear=True,
        ), patch.object(
            search_pdb_pos,
            "replacement_alphafold_download",
            return_value=(af_chain, replacement_path),
        ):
            result = search_pdb_pos.compute_site_pos(
                0, row, "a", "intra", mapping, "", ["K"], 0
            )

        position, criteria, method, error, plddt, new_path, coord = result
        self.assertEqual(position, 2, "AF fallback must discard the PDB shift")
        self.assertTrue(criteria)
        self.assertEqual(method, "alphafold")
        self.assertEqual(error, -1)
        self.assertEqual(plddt, 92.0)
        self.assertEqual(new_path, replacement_path)
        np.testing.assert_array_equal(coord, [200.0, 0.0, 0.0])
    def test_both_endpoints_use_the_same_replacement_model(self):
        with tempfile.TemporaryDirectory() as folder:
            original_path = str(Path(folder) / "blastp_1ABC.pdb")
            replacement_path = str(Path(folder) / "blastp_afP1.pdb")

            for path, chain in (
                (original_path, self.make_chain([(2, 200.0)])),
                (
                    replacement_path,
                    self.make_chain([(1, 0.0), (2, 20.0), (3, 30.0)]),
                ),
            ):
                model = Model(0)
                model.add(chain)
                writer = PDBIO()
                writer.set_structure(model)
                writer.save(path)

            mapping = pd.DataFrame(
                [
                    {
                        "PDB": "1ABC",
                        "CHAIN": "A",
                        "SP_PRIMARY": "P1",
                        "SP_BEG": 1,
                        "SP_END": 3,
                        "PDB_BEG": 2,
                        "PDB_END": 4,
                    }
                ]
            )

            for pos_a, pos_b in ((2, 1), (1, 2)):
                with self.subTest(pos_a=pos_a, pos_b=pos_b):
                    data = pd.DataFrame(
                        [
                            {
                                "source_record_id": "record_000001",
                                "path": original_path,
                                "pdb_id": "1ABC",
                                "pdb_method": "X-RAY DIFFRACTION",
                                "pdb_resolution": 2.0,
                                "chain_a": "A",
                                "chain_b": "A",
                                "unip_id_a": "P1",
                                "unip_id_b": "P1",
                                "seq_a": "KKK",
                                "seq_b": "KKK",
                                "pos_a": pos_a,
                                "pos_b": pos_b,
                            }
                        ],
                        index=[7],
                    )

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
                    self.assertEqual(checked["path"], replacement_path)
                    self.assertEqual(checked["pdb_method"], "ALPHAFOLD")
                    self.assertEqual(
                        checked["source_record_id"], "record_000001"
                    )
                    self.assertTrue(checked["res_criteria_fulfilled"])
                    self.assertTrue(
                        checked["is_interfaced"],
                        "Both coordinates must come from the AF model",
                    )
                    for site, position in (("a", pos_a), ("b", pos_b)):
                        self.assertEqual(checked[f"pos_{site}"], position)
                        self.assertEqual(checked[f"pdb_pos_{site}"], position)
                        self.assertEqual(checked[f"chain_{site}"], "A")
                        self.assertEqual(checked[f"method_{site}"], "alphafold")
                        self.assertEqual(
                            checked[f"pLDDT_{site}"], 90.0 + position
                        )

if __name__ == "__main__":
    unittest.main()
