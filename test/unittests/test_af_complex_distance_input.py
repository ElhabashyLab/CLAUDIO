import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from Bio.PDB import MMCIFParser, PDBParser

from claudio.module02.src_distance_reevaluation.algorithm.af_complex_distances import (
    _export_complex,
)


FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "af_complex"
    / "AF-0000000208747029.cif"
)


class TestAFComplexDistanceInput(unittest.TestCase):
    def test_exported_endpoints_keep_the_original_atom_coordinates(self):
        source = next(MMCIFParser(QUIET=True).get_structure(
            "source", str(FIXTURE)
        ).get_models())
        with TemporaryDirectory() as folder:
            target = Path(folder) / "structure.pdb"
            residues = _export_complex(str(FIXTURE), target, ["A", "B"])
            model = next(PDBParser(QUIET=True).get_structure(
                "exported", str(target)
            ).get_models())

            for chain_id, position in (("A", 67), ("B", 11)):
                with self.subTest(chain=chain_id, position=position):
                    chain, number, name = residues[
                        (chain_id, (" ", position, " "))
                    ]
                    self.assertEqual(name, "LYS")
                    atom = model[chain][number]["CB"]
                    original = source[chain_id][position]["CB"]
                    self.assertLess(float(abs(atom.coord - original.coord).max()), 0.001)

    def test_export_includes_both_selected_complex_chains(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / "structure.pdb"
            residues = _export_complex(str(FIXTURE), target, ["A", "B"])
            model = next(PDBParser(QUIET=True).get_structure(
                "exported", str(target)
            ).get_models())
            self.assertEqual({chain.id for chain in model}, {"A", "B"})
            self.assertEqual({chain for chain, _ in residues}, {"A", "B"})

    def test_export_excludes_chains_that_are_not_requested(self):
        with TemporaryDirectory() as folder:
            target = Path(folder) / "structure.pdb"
            residues = _export_complex(str(FIXTURE), target, ["A"])
            model = next(PDBParser(QUIET=True).get_structure(
                "exported", str(target)
            ).get_models())
            self.assertEqual({chain.id for chain in model}, {"A"})
            self.assertEqual({chain for chain, _ in residues}, {"A"})


if __name__ == "__main__":
    unittest.main()
