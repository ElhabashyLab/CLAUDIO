"""Keep complete chain identities during M2 residue lookup."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import MMCIFIO
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import search_pdb_pos


class TestM2ChainIds(unittest.TestCase):

    def test_matches_complete_chain_ids_for_both_endpoints(self):
        model = Model(0)
        expected = {"AA": 11.0, "AB": 22.0, "A": 33.0}
        for serial, (chain_id, x) in enumerate(expected.items(), start=1):
            chain = Chain(chain_id)
            residue = Residue((" ", 1, " "), "LYS", " ")
            residue.add(
                Atom(
                    "CB", np.array([x, 0.0, 0.0]), 91.0, 1.0,
                    " ", " CB ", serial, element="C",
                )
            )
            chain.add(residue)
            model.add(chain)

        mapping = pd.DataFrame(columns=["PDB", "CHAIN", "SP_PRIMARY"])
        with patch.object(search_pdb_pos, "pdb_cache", {"memory.cif": [model]}):
            for site in ("a", "b"):
                for chain_id, expected_x in expected.items():
                    with self.subTest(site=site, chain=chain_id):
                        row = pd.Series({
                            "path": "memory.cif",
                            "pdb_id": "AFTEST",
                            f"chain_{site}": chain_id,
                            f"unip_id_{site}": "P1",
                            f"seq_{site}": "K",
                            f"pos_{site}": 1,
                        })
                        result = search_pdb_pos.compute_site_pos(
                            7, row, site, "inter", mapping, "", ["K"], 0,
                        )
                        self.assertTrue(
                            result[1], f"Chain {chain_id} must be found exactly"
                        )
                        self.assertEqual(result[0], 1)
                        np.testing.assert_allclose(
                            result[6], [expected_x, 0.0, 0.0]
                        )



    def test_reads_multicharacter_chains_from_mmcif(self):
        model = Model(0)
        for serial, (chain_id, x) in enumerate((("AA", 11.0), ("AB", 22.0)), start=1):
            chain = Chain(chain_id)
            residue = Residue((" ", 1, " "), "LYS", " ")
            residue.add(Atom(
                "CB", np.array([x, 0.0, 0.0]), 91.0, 1.0,
                " ", " CB ", serial, element="C",
            ))
            chain.add(residue)
            model.add(chain)

        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "chains.cif"
            writer = MMCIFIO()
            writer.set_structure(model)
            writer.save(str(source))
            data = pd.DataFrame([{
                "path": str(source), "pdb_id": "AFTEST",
                "chain_a": "AA", "chain_b": "AB",
                "unip_id_a": "P1", "unip_id_b": "P2",
                "seq_a": "K", "seq_b": "K", "pos_a": 1, "pos_b": 1,
            }], index=[7])
            mapping = pd.DataFrame(columns=["PDB", "CHAIN", "SP_PRIMARY"])
            with patch.object(search_pdb_pos, "pdb_cache", {}), patch.object(
                search_pdb_pos.pd, "read_csv", return_value=mapping
            ), patch.object(
                search_pdb_pos.r, "get",
                side_effect=AssertionError("Unexpected network request"),
            ):
                result = search_pdb_pos.search_site_pos_in_pdb(
                    data, pd.DataFrame([{"res": "K", "atom": "CB"}]), 0,
                )

            self.assertTrue(result.loc[7, "res_criteria_fulfilled"])
            self.assertTrue(result.loc[7, "is_interfaced"])
            self.assertEqual(result.loc[7, "chain_a"], "AA")
            self.assertEqual(result.loc[7, "chain_b"], "AB")
            self.assertEqual(result.loc[7, "pdb_pos_a"], 1)
            self.assertEqual(result.loc[7, "pdb_pos_b"], 1)


if __name__ == "__main__":
    unittest.main()
