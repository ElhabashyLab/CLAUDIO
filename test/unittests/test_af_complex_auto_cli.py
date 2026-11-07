"""Tests for automatic AF complex retrieval through the search CLI."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from click.testing import CliRunner

from claudio.module02.src_structure_search import main as entry


class TestAFComplexAutoCLI(unittest.TestCase):
    @patch(
        "claudio.module02.src_structure_search.main.download_pdbs"
    )
    @patch(
        "claudio.module02.src_structure_search.main.structure_search"
    )
    @patch(
        "claudio.module02.src_structure_search.main.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.main."
        "retrieve_discovered_complexes"
    )
    def test_auto_mode_retrieves_and_writes_results(
        self, mock_auto, mock_manual, mock_search, mock_download
    ):
        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "source_record_id": "record_000001",
        }], index=[7])

        model_id = "AF-0000000208747029"
        mock_auto.side_effect = lambda frame, folder: frame.assign(
            af_model_id=model_id,
            af_model_version=1,
            af_match_status="matched",
            chain_a="A",
            chain_b="B",
            path="test_model.cif",
        )

        with TemporaryDirectory() as folder:
            input_path = Path(folder) / "demo.sqcs"
            output_dir = Path(folder) / "output"
            data.to_csv(input_path)

            result = CliRunner().invoke(entry.main, [
                "-i", str(input_path),
                "-o", str(output_dir),
                "--af-complex-auto",
                "-bldb", str(Path(folder) / "missing_database"),
            ])

            self.assertEqual(
                result.exit_code,
                0,
                f"{result.output}\n{result.exception!r}",
            )

            mock_auto.assert_called_once()
            args = mock_auto.call_args.args
            pd.testing.assert_frame_equal(
                args[0][data.columns], data
            )
            self.assertEqual(
                Path(args[1]),
                output_dir / "structures",
            )

            mock_manual.assert_not_called()
            mock_search.assert_not_called()
            mock_download.assert_not_called()

            output_path = output_dir / "demo.sqcs_structdi.csv"
            self.assertTrue(output_path.is_file())

            saved = pd.read_csv(output_path, index_col=0)
            self.assertEqual(saved.index.tolist(), [7])

            row = saved.iloc[0]
            self.assertEqual(row["source_record_id"], "record_000001")
            self.assertEqual(row["af_match_status"], "matched")
            self.assertEqual(row["chain_a"], "A")
            self.assertEqual(row["chain_b"], "B")
            self.assertEqual(row["pdb_id"], model_id)
            self.assertEqual(row["pdb_method"], "ALPHAFOLD")
            self.assertEqual(row["pdb_resolution"], "ALPHAFOLD")
    @patch(
        "claudio.module02.src_structure_search.main.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.main."
        "retrieve_discovered_complexes"
    )
    def test_rejects_auto_and_manual_modes_together(
        self, mock_auto, mock_manual
    ):
        mock_auto.side_effect = AssertionError(
            "Retrieval must not start with conflicting options"
        )
        mock_manual.side_effect = AssertionError(
            "Retrieval must not start with conflicting options"
        )

        with TemporaryDirectory() as folder:
            input_path = Path(folder) / "demo.sqcs"
            pd.DataFrame([{
                "unip_id_a": "A0A0P0Y832",
                "unip_id_b": "P0C2Z6",
            }]).to_csv(input_path)

            result = CliRunner().invoke(entry.main, [
                "-i", str(input_path),
                "-o", str(Path(folder) / "output"),
                "--af-complex-auto",
                "--af-complex-model", "AF-0000000208747029",
            ])

        self.assertEqual(result.exit_code, 2, result.output)
        self.assertIn("mutually exclusive", result.output)
        mock_auto.assert_not_called()
        mock_manual.assert_not_called()

if __name__ == "__main__":
    unittest.main()
