"""Keep inserted residue identities when preparing TopoLink calculations."""
import io
import shlex
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import PDBIO, PDBParser
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import (
    calc_site_distances,
)


class TestM2TopoLinkResidueIdentity(unittest.TestCase):

    def test_topolink_uses_the_inserted_residue_coordinates(self):
        model = Model(0)
        chain = Chain("A")
        model.add(chain)
        for serial, (number, icode, x) in enumerate(
            ((1, " ", 0.0), (1, "A", 20.0), (2, " ", 30.0)),
            start=1,
        ):
            residue = Residue((" ", number, icode), "LYS", " ")
            residue.add(
                Atom(
                    "CB", np.array([x, 0.0, 0.0]), 90.0, 1.0,
                    " ", " CB ", serial, element="C",
                )
            )
            chain.add(residue)

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "test_1ABC.pdb"
            writer = PDBIO()
            writer.set_structure(model)
            writer.save(str(path))

            data = pd.DataFrame(
                [
                    {
                        "source_record_id": "record_000001",
                        "path": str(path),
                        "unip_id_a": "P1",
                        "unip_id_b": "P1",
                        "seq_a": "KKK",
                        "seq_b": "KKK",
                        "pos_a": 2,
                        "pos_b": 3,
                        "chain_a": "A",
                        "chain_b": "A",
                        "pdb_pos_a": 1,
                        "pdb_pos_b": 2,
                        "pdb_hetflag_a": " ",
                        "pdb_hetflag_b": " ",
                        "pdb_icode_a": "A",
                        "pdb_icode_b": " ",
                        "method_a": "realigning",
                        "pLDDT_a": 90.0,
                        "pLDDT_b": 90.0,
                        "res_criteria_fulfilled": True,
                        "is_interfaced": True,
                    }
                ]
            )
            selected_coordinates = []
            errors = []

            def fake_topolink(command):
                try:
                    input_path = Path(shlex.split(command)[-1])
                    lines = input_path.read_text(encoding="utf-8").splitlines()
                    structure_line = next(
                        line for line in lines if line.startswith("structure ")
                    )
                    exported_path = structure_line.split(maxsplit=1)[1]
                    exported = PDBParser(QUIET=True).get_structure(
                        "exported", exported_path
                    )[0]
                    observed = next(
                        line.split() for line in lines
                        if line.strip().startswith("observed ")
                    )
                    a_name, a_chain, a_pos, b_name, b_chain, b_pos = observed[1:]
                    atom_a = exported[a_chain][int(a_pos)]["CB"]
                    atom_b = exported[b_chain][int(b_pos)]["CB"]
                    selected_coordinates.extend(
                        [atom_a.coord.copy(), atom_b.coord.copy()]
                    )
                    distance = float(atom_a - atom_b)
                    return io.StringIO(
                        f"  LINK: {a_name} {a_chain} {a_pos} CB "
                        f"{b_name} {b_chain} {b_pos} CB "
                        f"{distance:.3f} {distance + 2.0:.3f}\n"
                    )
                except Exception as error:
                    errors.append(repr(error))
                    return io.StringIO("")

            with patch.object(
                calc_site_distances.os, "popen", side_effect=fake_topolink
            ) as mocked_topolink:
                result = calc_site_distances.compute_dists_with_topolink(
                    data,
                    str(root / "work") + "/",
                    pd.DataFrame([{"res": "K", "atom": "CB"}]),
                    70.0,
                    None,
                    0,
                )

            mocked_topolink.assert_called_once()
            self.assertEqual(errors, [])
            np.testing.assert_allclose(result["eucl_dist_tplk"], [10.0])
            np.testing.assert_allclose(result["topo_dist_tplk"], [12.0])
            np.testing.assert_allclose(
                selected_coordinates,
                [[20.0, 0.0, 0.0], [30.0, 0.0, 0.0]],
            )
            mapping_files = list((root / "work").rglob("*_residue_map.csv"))
            self.assertEqual(len(mapping_files), 1)
            mapping = pd.read_csv(mapping_files[0], keep_default_na=False)
            inserted = mapping[
                (mapping["source_chain"] == "A")
                & (mapping["source_resseq"] == 1)
                & (mapping["source_icode"] == "A")
            ]
            self.assertEqual(len(inserted), 1)
            self.assertEqual(int(inserted.iloc[0]["topolink_resseq"]), 2)
            self.assertEqual(inserted.iloc[0]["source_path"], str(path))
            self.assertEqual(result.loc[0, "pdb_pos_a"], 1)
            self.assertEqual(result.loc[0, "pdb_icode_a"], "A")
            self.assertEqual(result.loc[0, "path"], str(path))
            self.assertEqual(result.loc[0, "source_record_id"], "record_000001")

    def test_legacy_numbers_require_a_unique_residue(self):
        residue_map = {
            ("A", " ", 1, " "): 1,
            ("A", " ", 1, "A"): 2,
            ("A", " ", 25, " "): 3,
        }
        for number, expected in ((1, None), (25, 3)):
            with self.subTest(number=number):
                row = pd.Series({"chain_a": "A", "pdb_pos_a": number})
                actual = calc_site_distances.resolve_topolink_position(
                    row, "a", residue_map
                )
                self.assertEqual(actual, expected)

    def test_unknown_insertion_code_is_not_replaced_by_another_residue(self):
        residue_map = {
            ("A", " ", 1, " "): 1,
            ("A", " ", 1, "A"): 2,
        }
        row = pd.Series(
            {
                "chain_a": "A",
                "pdb_pos_a": 1,
                "pdb_hetflag_a": " ",
                "pdb_icode_a": "B",
            }
        )
        self.assertIsNone(
            calc_site_distances.resolve_topolink_position(row, "a", residue_map)
        )


if __name__ == "__main__":
    unittest.main()
