"""Preserve original chain identities in TopoLink PDB exports."""
import tempfile
import unittest
from pathlib import Path
import io
import shlex
from unittest.mock import patch
import numpy as np
import pandas as pd
from Bio.PDB import MMCIFIO, MMCIFParser, PDBParser
from Bio.PDB.Atom import Atom
from Bio.PDB.Chain import Chain
from Bio.PDB.Model import Model
from Bio.PDB.Residue import Residue

from claudio.module02.src_distance_reevaluation.algorithm import calc_site_distances


class TestM2TopoLinkChainIds(unittest.TestCase):

    def test_exports_distinct_single_character_chains_with_provenance(self):
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

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "complex.cif"
            writer = MMCIFIO()
            writer.set_structure(model)
            writer.save(str(source))
            work = root / "work"
            (work / "struct").mkdir(parents=True)

            try:
                exported_path, residue_map = (
                    calc_site_distances.prepare_topolink_structure(
                        str(source), "complex", str(work) + "/",
                        list(expected),
                    )
                )
            except Exception as error:
                self.fail(f"Multi-character chains must export safely: {error}")

            exported = PDBParser(QUIET=True).get_structure(
                "exported", exported_path
            )[0]
            chain_ids = [chain.id for chain in exported]
            self.assertEqual(len(chain_ids), 3)
            self.assertEqual(len(set(chain_ids)), 3)
            self.assertTrue(all(len(name) == 1 for name in chain_ids))

            mapping = pd.read_csv(
                work / "struct" / "complex_residue_map.csv", keep_default_na=False
            )
            self.assertEqual(set(mapping["source_chain"]), set(expected))
            self.assertEqual(mapping["topolink_chain"].nunique(), 3)

            for row in mapping.itertuples(index=False):
                with self.subTest(source_chain=row.source_chain):
                    atom = exported[row.topolink_chain][
                        int(row.topolink_resseq)
                    ]["CB"]
                    np.testing.assert_allclose(
                        atom.coord, [expected[row.source_chain], 0.0, 0.0]
                    )
                    self.assertEqual(
                        residue_map[(row.source_chain, " ", 1, " ")], 1
                    )
                    self.assertEqual(row.source_path, str(source))
                    if row.source_chain == "A":
                        self.assertEqual(row.topolink_chain, "A")

            original = MMCIFParser(QUIET=True).get_structure(
                "original", str(source)
            )[0]
            self.assertEqual([chain.id for chain in original], list(expected))

    def test_uses_exported_chain_ids_and_backfills_original_records(self):
        model = Model(0)
        for serial, (chain_id, x) in enumerate(
            (("AA", 11.0), ("AB", 22.0), ("A", 33.0)), start=1
        ):
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

        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "complex.cif"
            writer = MMCIFIO()
            writer.set_structure(model)
            writer.save(str(source))
            pairs = [("AA", "AB"), ("AA", "A"), ("AB", "AA")]
            data = pd.DataFrame(
                [
                    {
                        "source_record_id": f"record_{number:06d}",
                        "path": str(source),
                        "unip_id_a": f"P_{a}", "unip_id_b": f"P_{b}",
                        "seq_a": "K", "seq_b": "K",
                        "pos_a": 1, "pos_b": 1,
                        "chain_a": a, "chain_b": b,
                        "pdb_pos_a": 1, "pdb_pos_b": 1,
                        "pdb_hetflag_a": " ", "pdb_hetflag_b": " ",
                        "pdb_icode_a": " ", "pdb_icode_b": " ",
                        "method_a": "alphafold",
                        "pLDDT_a": 91.0, "pLDDT_b": 91.0,
                        "res_criteria_fulfilled": True,
                        "is_interfaced": True,
                    }
                    for number, (a, b) in enumerate(pairs, start=1)
                ],
                index=[7, 12, 19],
            )
            original = data.copy(deep=True)
            errors = []
            observed_pairs = []

            def fake_topolink(command):
                try:
                    input_path = Path(shlex.split(command)[-1])
                    lines = input_path.read_text().splitlines()
                    structure_line = next(
                        line for line in lines if line.startswith("structure ")
                    )
                    exported = PDBParser(QUIET=True).get_structure(
                        "exported", structure_line.split(maxsplit=1)[1]
                    )[0]
                    output = []
                    for line in lines:
                        if not line.strip().startswith("observed "):
                            continue
                        a_name, a_chain, a_pos, b_name, b_chain, b_pos = (
                            line.split()[1:]
                        )
                        if len(a_chain) != 1 or len(b_chain) != 1:
                            raise AssertionError(
                                "observed must use exported single-character IDs"
                            )
                        atom_a = exported[a_chain][int(a_pos)]["CB"]
                        atom_b = exported[b_chain][int(b_pos)]["CB"]
                        observed_pairs.append((a_chain, b_chain))
                        distance = float(atom_a - atom_b)
                        output.append(
                            f"  LINK: {a_name} {a_chain} {a_pos} CB "
                            f"{b_name} {b_chain} {b_pos} CB "
                            f"{distance:.3f} {distance + 2.0:.3f}\n"
                        )
                    return io.StringIO("".join(output))
                except Exception as error:
                    errors.append(str(error))
                    return io.StringIO("")

            with patch.object(
                calc_site_distances.os, "popen", side_effect=fake_topolink
            ) as mocked:
                result = calc_site_distances.compute_dists_with_topolink(
                    data, str(root / "work") + "/",
                    pd.DataFrame([{"res": "K", "atom": "CB"}]),
                    70.0, None, 0,
                )

            mocked.assert_called_once()
            self.assertEqual(errors, [])
            self.assertEqual(len(observed_pairs), 2)
            np.testing.assert_allclose(
                result["eucl_dist_tplk"], [11.0, 22.0, 11.0]
            )
            np.testing.assert_allclose(
                result["topo_dist_tplk"], [13.0, 24.0, 13.0]
            )
            pd.testing.assert_frame_equal(result[original.columns], original)


if __name__ == "__main__":
    unittest.main()
