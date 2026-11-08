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
    def test_default_mode_retrieves_and_writes_results(
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

            with patch.object(
                entry, "inputs_valid", return_value=True,
            ), patch.object(
                entry,
                "_search_legacy_candidates",
                side_effect=lambda _data, **kwargs: _data.assign(
                    structure_backend="legacy",
                    pdb_id="1ABC",
                    pdb_method="X-RAY DIFFRACTION",
                    pdb_resolution="2.0",
                    chain_a="A",
                    chain_b="B",
                    path="legacy.pdb",
                ),
            ) as _legacy:
                result = CliRunner().invoke(entry.main, [
                    "-i", str(input_path),
                    "-o", str(output_dir),
                    "-bldb", str(Path(folder) / "missing_database"),
                ])

            _legacy.assert_called_once()

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
            self.assertEqual(len(saved), 2)
            self.assertTrue(saved.index.is_unique)
            self.assertEqual(
                set(saved["structure_backend"]),
                {"legacy", "af_complex"},
            )
            self.assertTrue(
                saved["source_record_id"].eq("record_000001").all()
            )

            row = saved.loc[
                saved["structure_backend"].eq("af_complex")
            ].iloc[0]
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
    def test_combines_candidates_without_index_collisions_or_source_loss(self):
        _legacy = pd.DataFrame({
            "source_record_id": ["record_1", "record_2"],
            "structure_backend": ["legacy", "legacy"],
        }, index=[7, "7_1"])

        _af = pd.DataFrame({
            "source_record_id": ["record_1", "record_2"],
            "structure_backend": ["af_complex", "af_complex"],
        }, index=[7, "7_2"])

        _result = entry._combine_structure_candidates([_legacy, _af])

        self.assertEqual(len(_result), 4)
        self.assertEqual(len(set(map(str, _result.index))), 4)

        # Existing legacy indices remain available.
        pd.testing.assert_frame_equal(
            _result.iloc[:2], _legacy,
        )

        # Each experimental source retains both structure candidates.
        for _source in ("record_1", "record_2"):
            _rows = _result[
                _result["source_record_id"].eq(_source)
            ]
            self.assertEqual(len(_rows), 2)
            self.assertEqual(
                set(_rows["structure_backend"]),
                {"legacy", "af_complex"},
            )

        # A generated index must not take another candidate's index.
        self.assertEqual(
            _result.loc["7_2", "structure_backend"],
            "af_complex",
        )

    def test_combining_empty_candidates_preserves_headers(self):
        _legacy = pd.DataFrame(columns=[
            "source_record_id", "structure_backend", "pdb_id",
        ])
        _af = pd.DataFrame(columns=[
            "source_record_id", "structure_backend", "af_model_id",
        ])

        _result = entry._combine_structure_candidates([_legacy, _af])

        self.assertTrue(_result.empty)
        self.assertIn("pdb_id", _result.columns)
        self.assertIn("af_model_id", _result.columns)
if __name__ == "__main__":
    unittest.main()
