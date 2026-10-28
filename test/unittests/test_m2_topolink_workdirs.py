"""Keep parallel structure calculations in separate TopoLink work directories."""
import io
import shlex
import tempfile
import threading
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
from Bio.PDB.Structure import Structure

from claudio.module02.src_distance_reevaluation.algorithm import (
    calc_site_distances,
)


class TestM2TopoLinkWorkdirs(unittest.TestCase):
    @staticmethod
    def write_model(path, distance):
        structure = Structure("complex")
        model = Model(0)
        chain = Chain("A")
        structure.add(model)
        model.add(chain)

        for number, x in ((1, 0.0), (2, distance)):
            residue = Residue((" ", number, " "), "LYS", " ")
            residue.add(
                Atom(
                    "CB",
                    np.array([x, 0.0, 0.0], dtype=float),
                    90.0,
                    1.0,
                    " ",
                    " CB ",
                    number,
                    element="C",
                )
            )
            chain.add(residue)

        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(path))

    def test_parallel_models_keep_their_own_distances(self):
        for same_basename in (False, True):
            with self.subTest(same_basename=same_basename):
                self.check_parallel_models(same_basename)

    def check_parallel_models(self, same_basename):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            rows = []
            for model_id, distance in (("A", 10.0), ("B", 30.0)):
                if same_basename:
                    path = root / model_id / "model_v1.pdb"
                    path.parent.mkdir()
                else:
                    path = root / f"model_{model_id}_v1.pdb"
                self.write_model(path, distance)
                rows.append(
                    {
                        "path": str(path),
                        "unip_id_a": "P1",
                        "unip_id_b": "P1",
                        "seq_a": "KK",
                        "seq_b": "KK",
                        "pos_a": 1,
                        "pos_b": 2,
                        "pdb_pos_a": 1,
                        "pdb_pos_b": 2,
                        "chain_a": "A",
                        "chain_b": "A",
                        "method_a": "realigning",
                        "pLDDT_a": 90.0,
                        "pLDDT_b": 90.0,
                        "res_criteria_fulfilled": True,
                        "is_interfaced": True,
                    }
                )

            ready = threading.Barrier(2)
            errors = []
            input_paths = []
            structure_paths = []
            workdirs = []
            lock = threading.Lock()

            def fake_topolink(command):
                try:
                    input_path = Path(shlex.split(command)[-1])

                    # Both workers finish writing before either reads.
                    ready.wait(timeout=10)

                    lines = input_path.read_text(encoding="utf-8").splitlines()
                    structure_line = next(
                        line for line in lines if line.startswith("structure ")
                    )
                    structure_path = Path(structure_line.split(maxsplit=1)[1])
                    workdir = next(
                        (Path(line.split(maxsplit=1)[1]) for line in lines
                         if line.startswith("linkdir ")),
                        input_path.parent.parent,
                    )

                    exported = PDBParser(QUIET=True).get_structure(
                        "exported", str(structure_path)
                    )
                    chain = exported[0]["A"]
                    distance = float(chain[1]["CB"] - chain[2]["CB"])

                    with lock:
                        input_paths.append(input_path)
                        structure_paths.append(structure_path)
                        workdirs.append(workdir)

                    # Controlled output at the external-program boundary.
                    return io.StringIO(
                        f"  LINK: LYS A 1 CB LYS A 2 CB "
                        f"{distance:.3f} {distance + 2.0:.3f}\n"
                    )
                except Exception as error:
                    with lock:
                        errors.append(repr(error))
                    return io.StringIO("")

            with patch.object(
                calc_site_distances.os, "popen", side_effect=fake_topolink
            ) as mocked_topolink:
                result = calc_site_distances.compute_dists_with_topolink(
                    pd.DataFrame(rows),
                    temp_dir=str(root / "work") + "/",
                    df_xl_res=pd.DataFrame([{"res": "K", "atom": "CB"}]),
                    plddt_cutoff=70.0,
                    topolink_bin=None,
                    verbose_level=0,
                )

            self.assertEqual(mocked_topolink.call_count, 2)
            self.assertEqual(errors, [], f"Test setup failed: {errors}")

            np.testing.assert_allclose(
                result["eucl_dist_tplk"].to_numpy(dtype=float),
                [10.0, 30.0],
                err_msg="Parallel models must retain their own distances",
            )
            np.testing.assert_allclose(
                result["topo_dist_tplk"].to_numpy(dtype=float),
                [12.0, 32.0],
            )
            self.assertEqual(len(set(input_paths)), 2)
            self.assertEqual(len(set(structure_paths)), 2)
            self.assertEqual(len(set(workdirs)), 2)
            self.assertEqual(result["path"].tolist(), [row["path"] for row in rows])
            for workdir in workdirs:
                with self.subTest(workdir=workdir):
                    self.assertEqual(len(list((workdir / "in").glob("*.tmp"))), 1)
                    self.assertEqual(len(list((workdir / "struct").glob("*.pdb"))), 1)
                    self.assertEqual(len(list(workdir.glob("topo_*.log"))), 1)


if __name__ == "__main__":
    unittest.main()
