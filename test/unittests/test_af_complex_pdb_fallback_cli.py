"""Tests for PDB-first automatic AF complex fallback."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from click.testing import CliRunner

from claudio.module02.src_structure_search import main as entry


class TestAFComplexPDBFallbackCLI(unittest.TestCase):
    def test_available_pdb_skips_complex_discovery(self):
        _data = pd.DataFrame([{
            "unip_id_a": "Q99623",
            "unip_id_b": "P35232",
            "source_record_id": "record_000001",
        }], index=[7])

        with TemporaryDirectory() as _folder:
            _root = Path(_folder)
            _input_path = _root / "demo.sqcs"
            _output_dir = _root / "output"
            _pdb_path = _root / "accepted.pdb"

            _data.to_csv(_input_path)
            _pdb_path.write_text("HEADER    TEST\nEND\n")

            def _legacy(_data, **_kwargs):
                return _data.assign(
                    structure_backend="legacy",
                    pdb_id="1ABC",
                    pdb_method="X-RAY DIFFRACTION",
                    pdb_resolution=2.0,
                    chain_a="A",
                    chain_b="B",
                    path=str(_pdb_path),
                )

            def _complex(_data, _folder):
                return _data.assign(
                    af_model_id="AF-0000000210845639",
                    af_model_version=1,
                    af_match_status="matched",
                    chain_a="A",
                    chain_b="B",
                    path=str(_root / "complex.cif"),
                )

            with patch.object(
                entry, "inputs_valid", return_value=True,
            ), patch.object(
                entry,
                "_search_legacy_candidates",
                side_effect=_legacy,
            ), patch.object(
                entry,
                "retrieve_discovered_complexes",
                side_effect=_complex,
            ) as _auto, patch.object(
                entry, "retrieve_af_complex",
            ) as _manual:
                _result = CliRunner().invoke(entry.main, [
                    "-i", str(_input_path),
                    "-o", str(_output_dir),
                    "-bldb", str(_root / "unused_database"),
                ])

            self.assertEqual(
                _result.exit_code,
                0,
                f"{_result.output}\n{_result.exception!r}",
            )
            _auto.assert_not_called()
            _manual.assert_not_called()

            _saved = pd.read_csv(
                _output_dir / "demo.sqcs_structdi.csv",
                index_col=0,
            )
            self.assertEqual(len(_saved), 1)
            self.assertEqual(_saved.iloc[0]["pdb_id"], "1ABC")
            self.assertEqual(
                _saved.iloc[0]["structure_backend"], "legacy"
            )
            self.assertEqual(
                _saved.iloc[0]["source_record_id"], "record_000001"
            )


    def _check_fallback(self, _kinds, _expected_ids):
        _size = len(_kinds)
        _data = pd.DataFrame({
            "unip_id_a": ["Q99623"] * _size,
            "unip_id_b": [
                "Q99623" if _kind == "monomer" else "P35232"
                for _kind in _kinds
            ],
            "source_record_id": [
                "record_000001", "record_000001", "record_000002"
            ][:_size],
            "candidate_id": [
                f"candidate_{_position + 1:06d}"
                for _position in range(_size)
            ],
        }, index=range(7, 7 + _size))

        _events = []

        with TemporaryDirectory() as _folder:
            _root = Path(_folder)
            _input_path = _root / "demo.sqcs"
            _output_dir = _root / "output"
            _data.to_csv(_input_path)

            # Both successful structure fixtures have existing files.
            for _filename in ("accepted.pdb", "monomer.pdb"):
                (_root / _filename).write_text("HEADER    TEST\nEND\n")

            _columns = [
                "pdb_id", "pdb_method", "pdb_resolution",
                "path", "chain_a", "chain_b",
            ]
            _models = {
                "missing": ("-", "-", "-", "-", "-", "-"),
                "pdb": (
                    "1ABC", "X-RAY DIFFRACTION", 2.0,
                    str(_root / "accepted.pdb"), "A", "B",
                ),
                "monomer": (
                    "afQ99623", "ALPHAFOLD", "ALPHAFOLD",
                    str(_root / "monomer.pdb"), "A", "A",
                ),
            }

            def _legacy(_data, **_kwargs):
                _events.append("legacy")
                _result = _data.copy()
                _result["structure_backend"] = "legacy"
                for _index, _kind in zip(_result.index, _kinds):
                    _result.loc[_index, _columns] = _models[_kind]
                return _result

            def _complex(_data, _folder):
                _events.append("complex")
                return _data.assign(
                    af_model_id="AF-0000000210845639",
                    af_model_version=1,
                    af_match_status="matched",
                    chain_a="A",
                    chain_b="B",
                    path=str(_root / "complex.cif"),
                )

            with patch.object(
                entry, "inputs_valid", return_value=True,
            ), patch.object(
                entry,
                "_search_legacy_candidates",
                side_effect=_legacy,
            ), patch.object(
                entry,
                "retrieve_discovered_complexes",
                side_effect=_complex,
            ) as _auto, patch.object(
                entry, "retrieve_af_complex",
            ) as _manual:
                _result = CliRunner().invoke(entry.main, [
                    "-i", str(_input_path),
                    "-o", str(_output_dir),
                    "-bldb", str(_root / "unused_database"),
                ])

            self.assertEqual(
                _result.exit_code,
                0,
                f"{_result.output}\n{_result.exception!r}",
            )
            self.assertEqual(_events, ["legacy", "complex"])
            _auto.assert_called_once()
            _manual.assert_not_called()

            _queried = _auto.call_args.args[0]
            self.assertEqual(
                _queried["candidate_id"].tolist(), _expected_ids
            )
            self.assertNotIn(
                "_claudio_structure_input_row", _queried.columns
            )

            _saved = pd.read_csv(
                _output_dir / "demo.sqcs_structdi.csv",
                index_col=0,
            )
            self.assertTrue(_saved.index.is_unique)
            self.assertNotIn(
                "_claudio_structure_input_row", _saved.columns
            )

            _af_rows = _saved.loc[
                _saved["structure_backend"].eq("af_complex")
            ]
            self.assertEqual(
                sorted(_af_rows["candidate_id"].tolist()),
                sorted(_expected_ids),
            )

            _source_by_candidate = _data.set_index(
                "candidate_id"
            )["source_record_id"]
            for _row in _af_rows.itertuples():
                self.assertEqual(
                    _row.source_record_id,
                    _source_by_candidate.loc[_row.candidate_id],
                )

            # Accepted PDB and existing monomer results remain available.
            for _kind, _candidate in zip(
                _kinds, _data["candidate_id"]
            ):
                if _kind == "missing":
                    continue
                _rows = _saved.loc[
                    _saved["structure_backend"].eq("legacy")
                    & _saved["candidate_id"].eq(_candidate)
                ]
                self.assertEqual(
                    _rows["pdb_id"].tolist(), [_models[_kind][0]]
                )

    def test_missing_pdb_uses_complex_fallback(self):
        self._check_fallback(
            ["missing"],
            ["candidate_000001"],
        )

    def test_existing_monomer_does_not_block_complex_fallback(self):
        self._check_fallback(
            ["monomer"],
            ["candidate_000001"],
        )

    def test_mixed_candidates_only_query_those_without_pdb(self):
        self._check_fallback(
            ["pdb", "missing", "monomer"],
            ["candidate_000002", "candidate_000003"],
        )


if __name__ == "__main__":
    unittest.main()
