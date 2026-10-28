import tempfile
import unittest
from pathlib import Path

import pandas as pd

from claudio.module04.src.io.read_ins import read_inputs


class TestM4OverlapReading(unittest.TestCase):
    def test_preserves_missing_overlap_for_different_chains(self):
        structures = pd.DataFrame({
            "chain_a": ["A", "A"],
            "chain_b": ["B", "B"],
        })
        ops = pd.DataFrame({
            "homo_pep_overl": [float("nan"), True],
        })

        with tempfile.TemporaryDirectory() as directory:
            structure_path = Path(directory) / "structures.csv"
            ops_path = Path(directory) / "ops.csv"
            structures.to_csv(structure_path)
            ops.to_csv(ops_path)

            result = read_inputs(str(structure_path), str(ops_path))

        self.assertTrue(
            pd.isna(result.loc[0, "homo_pep_overl"]),
            "Missing overlap must remain missing for different chains",
        )
        self.assertEqual(
            result.loc[1, "homo_pep_overl"],
            False,
            "Known overlap must retain the existing different-chain behavior",
        )


if __name__ == "__main__":
    unittest.main()
