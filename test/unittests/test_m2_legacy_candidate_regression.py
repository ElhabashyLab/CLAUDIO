import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

import pandas as pd


_entry = importlib.import_module(
    "claudio.module02.src_structure_search.main"
)
_search_module = importlib.import_module(
    "claudio.module02.src_structure_search.algorithm.structure_search"
)
_download_module = importlib.import_module(
    "claudio.module02.src_structure_search.algorithm.pdb_download"
)

_PDB_TEXT = (
    "HEADER    REGRESSION TEST\n"
    "EXPDTA    X-RAY DIFFRACTION\n"
    "REMARK   2 RESOLUTION.    2.00 ANGSTROMS.\n"
    "ATOM      1  CA  LYS A   2       0.000   0.000   0.000"
    "  1.00 90.00           C  \n"
    "END\n"
)


class TestLegacyCandidateRegression(unittest.TestCase):
    def _run_case(self, _hits):
        with TemporaryDirectory() as _folder:
            _root = Path(_folder)
            _structures = _root / "structures"
            _structures.mkdir()

            # Legacy cleanup must preserve AF complex files.
            _complex_file = _structures / "AF-test.cif"
            _complex_file.write_text("data_test\n", encoding="utf-8")

            _input = _root / "input.sqcs"
            pd.DataFrame([{
                "source_record_id": "record_000001",
                "candidate_id": "candidate_000001",
                "unip_id_a": "P12345",
                "unip_id_b": "P12345",
                "seq_a": "MKK",
                "seq_b": "MKK",
                "pos_a": 2,
                "pos_b": 3,
            }], index=[7]).to_csv(_input)

            _data, _filename = _entry.read_in(str(_input))
            _empty_cache = pd.DataFrame(
                columns=["pdb_id", "method", "resolution"]
            )
            _search_result = (
                _hits,
                "1ABC" if _hits else None,
                "A_B" if _hits else None,
                "P12345",
            )

            with patch.object(
                _search_module,
                "perform_search",
                return_value=_search_result,
            ), patch.object(
                _download_module.pd,
                "read_csv",
                return_value=_empty_cache,
            ), patch.object(
                _download_module.r,
                "get",
                return_value=SimpleNamespace(text=_PDB_TEXT),
            ) as _http:
                _result = _entry._search_legacy_candidates(
                    _data=_data,
                    _tmp_filepath=str(_root / "search.csv"),
                    _structures_dir=str(_structures) + "/",
                    _do_structure_search=True,
                    _search_tool="blastp",
                    _e_value=1e-5,
                    _query_id=90.0,
                    _coverage=50.0,
                    _res_cutoff=4.0,
                    _blast_bin=None,
                    _blast_db="unused/",
                    _hhsearch_bin=None,
                    _hhsearch_db="unused/",
                    _verbose_level=0,
                )

            _http.assert_called_once()
            _url = _http.call_args.args[0]

            self.assertTrue(_complex_file.is_file())
            self.assertTrue(
                _result["structure_backend"].eq("legacy").all()
            )
            self.assertTrue(
                _result["source_record_id"].eq("record_000001").all()
            )
            for _path in _result["path"].unique():
                self.assertEqual(
                    Path(_path).read_text(encoding="utf-8"),
                    _PDB_TEXT,
                )

            return _result, _url

    def test_pdb_hit_preserves_chain_candidates(self):
        _result, _url = self._run_case(["1ABC_A_B"])

        self.assertTrue(
            _url.startswith("https://files.rcsb.org/")
        )
        self.assertTrue(_result["pdb_id"].eq("1ABC").all())
        self.assertTrue(
            _result["pdb_method"].eq("X-RAY DIFFRACTION").all()
        )
        self.assertEqual(len(_result), 4)
        self.assertEqual(
            set(zip(_result["chain_a"], _result["chain_b"])),
            {("A", "A"), ("A", "B"), ("B", "A"), ("B", "B")},
        )

    def test_no_pdb_hit_falls_back_to_af_single(self):
        _result, _url = self._run_case([])

        self.assertIn("/AF-P12345-F1-model_v", _url)
        self.assertEqual(len(_result), 1)
        self.assertEqual(_result.iloc[0]["pdb_id"], "afP12345")
        self.assertEqual(_result.iloc[0]["pdb_method"], "ALPHAFOLD")
        self.assertEqual(_result.iloc[0]["chain_a"], "A")
        self.assertEqual(_result.iloc[0]["chain_b"], "A")


if __name__ == "__main__":
    unittest.main()