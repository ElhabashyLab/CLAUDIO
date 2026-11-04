"""Honor configured atoms during M2 coordinate lookup."""
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
from claudio.utils.utils import build_xl_dataset


class TestM2ConfiguredAtoms(unittest.TestCase):
    def test_uses_configured_ca_for_glycine_at_both_endpoints(self):
        model = Model(0)
        for serial, (chain_id, x, confidence) in enumerate(
            (("A", 0.0, 91.0), ("B", 10.0, 92.0)), start=1
        ):
            chain = Chain(chain_id)
            residue = Residue((" ", 1, " "), "GLY", " ")
            residue.add(
                Atom(
                    "CA", np.array([x, 0.0, 0.0]), confidence, 1.0,
                    " ", " CA ", serial, element="C",
                )
            )
            chain.add(residue)
            model.add(chain)

        with tempfile.TemporaryDirectory() as folder:
            path = str(Path(folder) / "test_AFTEST.pdb")
            writer = PDBIO()
            writer.set_structure(model)
            writer.save(path)

            data = pd.DataFrame(
                [
                    {
                        "source_record_id": "record_000001",
                        "path": path,
                        "pdb_id": "AFTEST",
                        "chain_a": "A",
                        "chain_b": "B",
                        "unip_id_a": "P1",
                        "unip_id_b": "P2",
                        "seq_a": "G",
                        "seq_b": "G",
                        "pos_a": 1,
                        "pos_b": 1,
                    }
                ],
                index=[7],
            )
            config = build_xl_dataset("G:CA:")
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
                result = search_pdb_pos.search_site_pos_in_pdb(data, config, 0)

        checked = result.loc[7]
        self.assertTrue(
            checked["res_criteria_fulfilled"],
            "G:CA: must accept glycine with a CA atom and no CB",
        )
        self.assertTrue(checked["res_crit_a"])
        self.assertTrue(checked["res_crit_b"])
        self.assertTrue(checked["is_interfaced"])
        self.assertEqual(checked["pLDDT_a"], 91.0)
        self.assertEqual(checked["pLDDT_b"], 92.0)
        self.assertEqual(checked["method_a"], "alphafold")
        self.assertEqual(checked["method_b"], "alphafold")
        self.assertEqual(checked["source_record_id"], "record_000001")
    def test_selects_ca_when_cb_is_also_present(self):
        model = Model(0)
        for chain_id, offset in (("A", 0.0), ("B", 10.0)):
            chain = Chain(chain_id)
            residue = Residue((" ", 1, " "), "LYS", " ")
            for serial, (name, x, confidence) in enumerate(
                (("CA", offset + 1.0, 91.0),
                 ("CB", offset + 100.0, 21.0)), start=1
            ):
                residue.add(
                    Atom(
                        name, np.array([x, 0.0, 0.0]), confidence, 1.0,
                        " ", f" {name} ", serial, element="C",
                    )
                )
            chain.add(residue)
            model.add(chain)

        row = pd.Series({
            "path": "memory.pdb",
            "pdb_id": "AFTEST",
            "chain_a": "A", "chain_b": "B",
            "unip_id_a": "P1", "unip_id_b": "P2",
            "seq_a": "K", "seq_b": "K",
            "pos_a": 1, "pos_b": 1,
        })
        mapping = pd.DataFrame(columns=["PDB", "CHAIN", "SP_PRIMARY"])

        with patch.object(search_pdb_pos, "pdb_cache", {"memory.pdb": [model]}):
            for site, offset in (("a", 0.0), ("b", 10.0)):
                for atom_map, expected_x, expected_confidence in (
                    ({"K": ("CA",)}, offset + 1.0, 91.0),
                    (None, offset + 100.0, 21.0),
                ):
                    with self.subTest(site=site, atom_map=atom_map):
                        result = search_pdb_pos.compute_site_pos(
                            7, row, site, "inter", mapping, "", ["K"], 0,
                            xl_atom_map=atom_map,
                        )
                        self.assertTrue(result[1])
                        self.assertEqual(result[3], -1)
                        self.assertEqual(result[4], expected_confidence)
                        np.testing.assert_allclose(
                            result[6], [expected_x, 0.0, 0.0]
                        )
    def test_handles_missing_configured_atom_without_using_cb(self):
        model = Model(0)
        original_chain = Chain("A")
        original_residue = Residue((" ", 1, " "), "LYS", " ")
        original_residue.add(
            Atom(
                "CB", np.array([100.0, 0.0, 0.0]), 21.0, 1.0,
                " ", " CB ", 1, element="C",
            )
        )
        original_chain.add(original_residue)
        model.add(original_chain)

        replacement_chain = Chain("A")
        replacement_residue = Residue((" ", 1, " "), "LYS", " ")
        replacement_residue.add(
            Atom(
                "CA", np.array([5.0, 0.0, 0.0]), 95.0, 1.0,
                " ", " CA ", 1, element="C",
            )
        )
        replacement_chain.add(replacement_residue)

        row = pd.Series({
            "path": "memory.pdb", "pdb_id": "AFTEST",
            "chain_a": "A", "unip_id_a": "P1",
            "seq_a": "K", "pos_a": 1,
        })
        mapping = pd.DataFrame(columns=["PDB", "CHAIN", "SP_PRIMARY"])

        with patch.object(
            search_pdb_pos, "pdb_cache", {"memory.pdb": [model]}
        ), patch.object(
            search_pdb_pos, "replacement_alphafold_download",
            return_value=(replacement_chain, "replacement.pdb"),
        ):
            for xl_type in ("inter", "intra"):
                with self.subTest(xl_type=xl_type):
                    result = search_pdb_pos.compute_site_pos(
                        7, row, "a", xl_type, mapping, "", ["K"], 0,
                        xl_atom_map={"K": ("CA",)},
                    )
                    if xl_type == "inter":
                        self.assertIsNone(result[0])
                        self.assertFalse(result[1])
                        self.assertIsNone(result[6])
                    else:
                        self.assertTrue(result[1])
                        self.assertEqual(result[2], "alphafold")
                        self.assertEqual(result[3], -1)
                        self.assertEqual(result[4], 95.0)
                        self.assertEqual(result[5], "replacement.pdb")
                        np.testing.assert_allclose(
                            result[6], [5.0, 0.0, 0.0]
                        )

if __name__ == "__main__":
    unittest.main()
