"""Share TopoLink results with every record for the same residue pair."""
import io
import shlex
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

from claudio.module02.src_distance_reevaluation.algorithm import (
    calc_site_distances,
)


class TestM2DistanceBackfill(unittest.TestCase):

    def test_backfills_duplicate_and_reversed_pairs_without_mixing_pairs(self):
        model = Model(0)
        chain = Chain("A")
        model.add(chain)
        for number, x in ((1, 0.0), (2, 10.0), (3, 30.0)):
            residue = Residue((" ", number, " "), "LYS", " ")
            residue.add(
                Atom(
                    "CB", np.array([x, 0.0, 0.0]), 90.0, 1.0,
                    " ", " CB ", number, element="C",
                )
            )
            chain.add(residue)

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "test_1ABC.pdb"
            writer = PDBIO()
            writer.set_structure(model)
            writer.save(str(path))

            base = {
                "path": str(path),
                "unip_id_a": "P1",
                "unip_id_b": "P1",
                "seq_a": "KKK",
                "seq_b": "KKK",
                "chain_a": "A",
                "chain_b": "A",
                "pdb_hetflag_a": " ",
                "pdb_hetflag_b": " ",
                "pdb_icode_a": " ",
                "pdb_icode_b": " ",
                "method_a": "realigning",
                "pLDDT_a": 90.0,
                "pLDDT_b": 90.0,
                "res_criteria_fulfilled": True,
                "is_interfaced": True,
            }
            rows = []
            for number, (pos_a, pos_b) in enumerate(
                ((1, 2), (1, 2), (2, 1), (2, 3)), start=1
            ):
                rows.append(
                    {
                        **base,
                        "source_record_id": f"record_{number:06d}",
                        "pos_a": pos_a,
                        "pos_b": pos_b,
                        "pdb_pos_a": pos_a,
                        "pdb_pos_b": pos_b,
                    }
                )
            data = pd.DataFrame(rows, index=[7, 12, 19, 23])
            source_ids = data["source_record_id"].tolist()
            observations = []

            def fake_topolink(command):
                input_path = Path(shlex.split(command)[-1])
                lines = input_path.read_text(encoding="utf-8").splitlines()
                observations.extend(
                    line.strip() for line in lines
                    if line.strip().startswith("observed ")
                )
                return io.StringIO(
                    "  LINK: LYS A 1 CB LYS A 2 CB 10.000 12.000\n"
                    "  LINK: LYS A 2 CB LYS A 3 CB 20.000 22.000\n"
                )

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
            self.assertEqual(len(observations), 2)
            self.assertEqual(result.index.tolist(), [7, 12, 19, 23])
            self.assertEqual(result["source_record_id"].tolist(), source_ids)
            np.testing.assert_allclose(
                result["eucl_dist_tplk"], [10.0, 10.0, 10.0, 20.0]
            )
            np.testing.assert_allclose(
                result["topo_dist_tplk"], [12.0, 12.0, 12.0, 22.0]
            )



if __name__ == "__main__":
    unittest.main()
