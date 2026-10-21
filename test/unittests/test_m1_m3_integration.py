"""Integration test for M1 statuses passing through the M3 CLI."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from click.testing import CliRunner

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.module03.src.main import main as m3_main
from claudio.module03.src.io.read_in import read_in
from claudio.utils.utils import build_xl_dataset, clean_dataset


class TestM1M3Integration(unittest.TestCase):
    def test_preserves_statuses_and_missing_results_through_cli(self):
        cases = [
            ("valid", "MKAAKT", "AKT", 5, 2),
            ("corrected", "MKAAKT", "AKT", 2, 2),
            ("ambiguous", "MKAAKAKT", "AKAKT", 2, float("nan")),
        ]

        records = []
        for name, sequence, peptide, position, peptide_position in cases:
            records.append({
                "unip_id_a": f"TEST_{name}",
                "unip_id_b": f"TEST_{name}",
                "seq_a": sequence,
                "seq_b": sequence,
                "pep_a": peptide,
                "pep_b": "MKA",
                "pos_a": position,
                "pos_b": 2,
                "res_pos_a": peptide_position,
                "res_pos_b": 2,
                "original_pos_a": position,
                "original_pos_b": 2,
                "source_record_id": name,
            })

        try:
            with TemporaryDirectory() as temp_dir:
                folder = Path(temp_dir)
                data = double_check_data(
                    pd.DataFrame(records),
                    "integration",
                    build_xl_dataset("K"),
                    temp_dir + "/",
                    0,
                )
                data = clean_dataset(data)
                input_path = folder / "integration.sqcs"
                data.to_csv(input_path)

                output_dir = folder / "m3"
                execution = CliRunner().invoke(
                    m3_main,
                    [
                        "-i", str(input_path),
                        "-o", str(output_dir),
                        "-v", "0",
                    ],
                )
                self.assertEqual(
                    execution.exit_code,
                    0,
                    f"{execution.output}\n{execution.exception!r}",
                )

                result = read_in(
                    str(output_dir / "integration.sqcs_ops.csv")
                ).set_index("source_record_id")

                self.assertEqual(
                    set(result.index),
                    {"valid", "corrected", "ambiguous"},
                )

                for record_id in ("valid", "corrected"):
                    self.assertEqual(
                        result.loc[record_id, "position_status_a"],
                        record_id,
                    )
                    self.assertEqual(
                        result.loc[record_id, "pos_a"], 5
                    )
                    self.assertEqual(
                        result.loc[record_id, "homo_adjacency"], 0.5
                    )
                    self.assertEqual(
                        result.loc[record_id, "homo_int_overl"], 0.0
                    )
                    flag = result.loc[record_id, "homo_pep_overl"]
                    self.assertNotIsInstance(flag, str)
                    self.assertEqual(flag, False)

                self.assertEqual(
                    result.loc["corrected", "original_pos_a"], 2
                )
                self.assertEqual(
                    result.loc["ambiguous", "position_status_a"],
                    "ambiguous",
                )
                self.assertEqual(
                    result.loc["ambiguous", "original_pos_a"], 2
                )
                self.assertEqual(
                    result.loc["ambiguous", "pos_a"], 2
                )
                for column in (
                    "homo_adjacency",
                    "homo_int_overl",
                    "homo_pep_overl",
                ):
                    self.assertTrue(
                        pd.isna(result.loc["ambiguous", column]),
                        f"{column} must remain missing after file reload",
                    )

                self.assertEqual(
                    len(list(output_dir.glob("*.png"))), 4
                )
        finally:
            plt.close("all")


if __name__ == "__main__":
    unittest.main()
