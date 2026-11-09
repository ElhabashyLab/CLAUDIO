"""Public M2 options and propagation of child-stage failures."""

import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from click.testing import CliRunner

m2 = importlib.import_module("claudio.module02.run_module02_intra")


class TestAFComplexM2CLI(unittest.TestCase):
    def setUp(self):
        self.folder = TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.input = self.root / "input.sqcs"
        self.input.write_text("source_record_id\nrecord_000001\n")
        self.output = self.root / "out"

    def invoke_m2(self, extra=()):
        return CliRunner().invoke(m2.main, [
            "-i", str(self.input), "-o", str(self.output),
            "-bldb", str(self.root / "missing-db"),
            "-x", "G:CA:", "-pc", "42", "-lmin", "2", "-lmax", "44",
            *extra,
        ])

    def write_search_output(self, **params):
        directory = Path(params["output_directory"])
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "input.sqcs_structdi.csv").write_text("source_record_id\n")

    def test_forwards_manual_auto_and_legacy_options(self):
        cases = [
            (["--af-complex-model", "AF-0000000208747029"],
             "AF-0000000208747029", False),
            (["--af-complex-auto"], None, True),
            ([], None, True),
            (["--no-af-complex-auto"], None, False),
        ]
        for options, model, auto in cases:
            with self.subTest(options=options):
                with patch.object(
                    m2, "run_structure_search", side_effect=self.write_search_output
                ) as search, patch.object(m2, "run_distance_analysis") as distance:
                    result = self.invoke_m2(options)

                self.assertEqual(result.exit_code, 0,
                                 result.output + repr(result.exception))
                search.assert_called_once()
                distance.assert_called_once()
                params = search.call_args.kwargs
                self.assertEqual(params["af_complex_model"], model)
                self.assertEqual(params["af_complex_auto"], auto)
                self.assertTrue(params["do_structure_search"])
                self.assertIsNone(params["input_temppath"])
                params = distance.call_args.kwargs
                self.assertEqual(params["xl_residues"], "G:CA:")
                self.assertEqual(params["plddt_cutoff"], 42.0)
                self.assertEqual(params["linker_minimum"], 2.0)
                self.assertEqual(params["linker_maximum"], 44.0)
                self.assertEqual(
                    Path(params["input_filepath"]),
                    self.output / "input.sqcs_structdi.csv",
                )
                self.assertTrue(Path(params["input_directory"]).is_dir())

    def test_rejects_auto_and_manual_before_starting_stages(self):
        with patch.object(m2, "run_structure_search") as search, patch.object(
            m2, "run_distance_analysis"
        ) as distance:
            result = self.invoke_m2([
                "--af-complex-auto", "--af-complex-model", "AF-0000000208747029"
            ])
        self.assertEqual(result.exit_code, 2, result.output)
        self.assertIn("mutually exclusive", result.output)
        search.assert_not_called()
        distance.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_rejects_blank_model_id(self):
        with patch.object(m2, "run_structure_search") as search:
            result = self.invoke_m2(["--af-complex-model", " "])
        self.assertEqual(result.exit_code, 2, result.output)
        self.assertIn("Model ID must not be empty", result.output)
        search.assert_not_called()

    def test_search_failure_stops_even_when_old_output_exists(self):
        self.output.mkdir()
        (self.output / "input.sqcs_structdi.csv").write_text("stale output\n")
        for code in (1, 2):
            with self.subTest(code=code):
                with patch.object(
                    m2, "run_structure_search", side_effect=SystemExit(code)
                ), patch.object(m2, "run_distance_analysis") as distance:
                    result = self.invoke_m2()
                self.assertEqual(result.exit_code, code, result.output)
                distance.assert_not_called()

    def test_distance_failure_is_not_reported_as_success(self):
        with patch.object(
            m2, "run_structure_search", side_effect=self.write_search_output
        ), patch.object(m2, "run_distance_analysis", side_effect=SystemExit(1)):
            result = self.invoke_m2()
        self.assertEqual(result.exit_code, 1, result.output)

    def test_requires_output_from_successful_search(self):
        with patch.object(
            m2, "run_structure_search", return_value=None
        ), patch.object(m2, "run_distance_analysis") as distance:
            result = self.invoke_m2()
        self.assertNotEqual(result.exit_code, 0)
        distance.assert_not_called()
        self.assertIn("search output", result.output.lower())

    def test_zero_exit_from_search_allows_distance_stage(self):
        def search_success(**params):
            self.write_search_output(**params)
            raise SystemExit(0)

        with patch.object(
            m2, "run_structure_search", side_effect=search_success
        ), patch.object(m2, "run_distance_analysis") as distance:
            result = self.invoke_m2()
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        distance.assert_called_once()





if __name__ == "__main__":
    unittest.main()
