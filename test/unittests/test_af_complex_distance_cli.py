"""Exercise AF and legacy routing through the distance CLI."""

import importlib
import json
from contextlib import redirect_stdout
from io import StringIO
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import pandas as pd
from click.testing import CliRunner

distance_main = importlib.import_module(
    "claudio.module02.src_distance_reevaluation.main"
)
FIXTURE_DIR = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"


class TestAFComplexDistanceCLI(unittest.TestCase):
    def setUp(self):
        records = json.loads(
            (FIXTURE_DIR / "metadata.json").read_text(encoding="utf-8")
        )
        chains = {record["chainId"]: record for record in records}
        self.row = {
            "source_record_id": "record_000001",
            "candidate_id": "candidate_000001", "experiment": "condition_A",
            "af_match_status": "matched",
            "af_model_id": "AF-0000000208747029", "af_model_version": 1,
            "af_metadata_path": str(FIXTURE_DIR / "metadata.json"),
            "path": str(FIXTURE_DIR / "AF-0000000208747029.cif"),
            "pdb_id": "AF-0000000208747029",
            "pdb_method": "ALPHAFOLD", "pdb_resolution": "ALPHAFOLD",
            "unip_id_a": chains["A"]["uniprotAccession"],
            "unip_id_b": chains["B"]["uniprotAccession"],
            "seq_a": chains["A"]["sequence"], "seq_b": chains["B"]["sequence"],
            "chain_a": "A", "chain_b": "B",
            "pos_a": 67, "pos_b": 11,
            "original_pos_a": 67, "original_pos_b": 11,
            "position_status_a": "valid", "position_status_b": "valid",
            "pep_a": "K", "pep_b": "K", "res_pos_a": 1, "res_pos_b": 1,
        }

    def invoke_distance_cli(self, data, extra=()):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            structures = root / "structures"
            structures.mkdir()
            (structures / "complex.cif").symlink_to(
                FIXTURE_DIR / "AF-0000000208747029.cif"
            )
            path = root / "complex.sqcs_structdi.csv"
            data.to_csv(path)
            original = pd.read_csv(path, index_col=0)
            with patch.object(distance_main, "create_histogram") as plot:
                result = CliRunner().invoke(distance_main.main, [
                    "-i", str(structures), "-i2", str(path),
                    "-it", str(root / "temp"), "-o", str(root),
                    "-x", "K", "-p", "0", "-v", "0", *extra,
                ])
            self.assertEqual(
                result.exit_code, 0, result.output + repr(result.exception)
            )
            if data.empty:
                plot.assert_not_called()
            return original, pd.read_csv(path, index_col=0)

    def test_routes_af_records_without_dropping_sources_or_conditions(self):
        data = pd.DataFrame([
            self.row,
            {**self.row, "source_record_id": "record_000002",
             "experiment": "condition_B"},
            {**self.row, "source_record_id": "record_000003",
             "position_status_a": "ambiguous"},
        ], index=[7, "7_1", 12])

        def distances(selected, *args):
            output = selected.copy()
            values = [
                float(np.linalg.norm(
                    np.array(row.mapping_coord_a) - np.array(row.mapping_coord_b)
                ))
                for row in selected.itertuples()
            ]
            output["eucl_dist_tplk"] = values
            output["topo_dist_tplk"] = [value + 1 for value in values]
            return output

        with patch.object(
            distance_main, "search_site_pos_in_pdb",
            side_effect=AssertionError("AF input reached the legacy mapper"),
        ), patch.object(
            distance_main, "clean_dataset",
            side_effect=AssertionError("AF sources reached generic deduplication"),
        ), patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists",
            side_effect=distances,
        ) as calculate:
            original, saved = self.invoke_distance_cli(data)

        pd.testing.assert_frame_equal(saved[original.columns], original)
        self.assertEqual(len(saved), 3)
        calculate.assert_called_once()
        self.assertEqual(saved["distance_status"].tolist(),
                         ["computed", "computed", "not_evaluable"])
        self.assertTrue(saved.iloc[:2]["eucl_dist"].gt(50).all())
        self.assertTrue(pd.isna(saved.iloc[2]["eucl_dist"]))
        self.assertEqual(saved.iloc[2]["distance_reason"], "unresolved_position")

    def test_no_candidate_does_not_call_legacy_mapping_or_distance_engine(self):
        data = pd.DataFrame([{
            **self.row, "af_match_status": "no_candidate_model",
            "af_model_id": None, "af_model_version": None,
            "path": "-", "af_metadata_path": None,
            "chain_a": "-", "chain_b": "-",
        }])
        with patch.object(
            distance_main, "search_site_pos_in_pdb",
            side_effect=AssertionError("Missing AF model reached legacy mapping"),
        ), patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists"
        ) as calculate:
            original, saved = self.invoke_distance_cli(data)
        calculate.assert_not_called()
        pd.testing.assert_frame_equal(saved[original.columns], original)
        self.assertEqual(saved.iloc[0]["distance_reason"], "no_candidate_model")
        self.assertTrue(pd.isna(saved.iloc[0]["eucl_dist"]))
        self.assertTrue(pd.isna(saved.iloc[0]["topo_dist"]))

    def test_legacy_input_keeps_the_existing_mapping_path(self):
        data = pd.DataFrame([{
            key: value for key, value in self.row.items()
            if not key.startswith("af_")
        }])
        with patch.object(
            distance_main, "search_site_pos_in_pdb",
            side_effect=lambda data, *args: data,
        ) as search, patch.object(
            distance_main, "calculate_site_dists",
            side_effect=lambda data, *args: data.assign(eucl_dist=12.0, topo_dist=14.0),
        ) as calculate, patch.object(
            distance_main, "clean_dataset", side_effect=lambda data: data,
        ), patch.object(
            distance_main, "calculate_complex_site_dists", create=True,
        ) as complex_calculate:
            _, saved = self.invoke_distance_cli(data)
        search.assert_called_once()
        calculate.assert_called_once()
        complex_calculate.assert_not_called()
        self.assertEqual(saved.iloc[0]["eucl_dist"], 12.0)


    def test_checks_arguments_when_directory_contains_only_cif(self):
        with TemporaryDirectory() as folder:
            (Path(folder) / "model.cif").write_text("data_test\n")
            params = dict(
                input_directory=folder,
                input_filename="sample.sqcs_structdi.csv",
                search_tool="blastp", xl_residues="K", plddt_cutoff=70.0,
                output_directory=folder, topolink_bin=None, verbose_level=0,
            )
            cases = [
                ("input_filename", "wrong.csv", RuntimeError),
                ("search_tool", "invalid", ValueError),
                ("plddt_cutoff", -1, ValueError),
                ("plddt_cutoff", 101, ValueError),
                ("plddt_cutoff", float("nan"), ValueError),
                ("plddt_cutoff", "invalid", TypeError),
                ("xl_residues", "K:NZ:", ValueError),
            ]
            for field, value, error in cases:
                with self.subTest(field=field, value=value):
                    with redirect_stdout(StringIO()), self.assertRaises(error):
                        distance_main.inputs_valid(**{**params, field: value})

    def test_accepts_valid_arguments_for_empty_and_cif_directories(self):
        with TemporaryDirectory() as folder:
            params = dict(
                input_directory=folder,
                input_filename="sample.sqcs_structdi.csv",
                search_tool="blastp", xl_residues="K", plddt_cutoff=70.0,
                output_directory=folder, topolink_bin=None, verbose_level=0,
            )
            with redirect_stdout(StringIO()):
                self.assertTrue(distance_main.inputs_valid(**params))
                (Path(folder) / "model.cif").write_text("data_test\n")
                self.assertTrue(distance_main.inputs_valid(**params))

    def test_rerun_overwrites_old_distances_without_duplicate_columns(self):
        data = pd.DataFrame([{
            **self.row, "eucl_dist": 999.0, "topo_dist": 999.0,
            "distance_status": "not_evaluable", "distance_reason": "old",
        }])
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists",
            side_effect=lambda selected, *args: selected.assign(
                eucl_dist_tplk=12.0, topo_dist_tplk=14.0
            ),
        ):
            _, saved = self.invoke_distance_cli(data)
        self.assertEqual(saved.columns.tolist().count("eucl_dist"), 1)
        self.assertNotIn("eucl_dist.1", saved.columns)
        self.assertNotIn("topo_dist.1", saved.columns)
        self.assertEqual(saved.iloc[0]["eucl_dist"], 12.0)
        self.assertEqual(saved.iloc[0]["topo_dist"], 14.0)
        self.assertEqual(saved.iloc[0]["distance_status"], "computed")
        self.assertTrue(pd.isna(saved.iloc[0]["distance_reason"]))

    def test_empty_af_input_writes_headers_without_plotting(self):
        data = pd.DataFrame([self.row]).iloc[:0]
        with patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.calculate_site_dists"
        ) as calculate:
            original, saved = self.invoke_distance_cli(data)
        calculate.assert_not_called()
        self.assertTrue(saved.empty)
        pd.testing.assert_frame_equal(saved[original.columns], original)
        self.assertIn("eucl_dist", saved.columns)
        self.assertIn("distance_status", saved.columns)




if __name__ == "__main__":
    unittest.main()
