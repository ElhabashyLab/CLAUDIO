"""Full CLI routing and failures at module boundaries."""

import importlib
import unittest
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import click
from click.testing import CliRunner


pipeline = importlib.import_module("claudio.claudio_m")
STAGES = (
    "db_updater", "run_claudio_lists", "run_claudio_ops",
    "run_claudio_structdi", "run_claudio_xl",
)


class TestAFComplexPipelineCLI(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.input = self.root / "input.csv"
        self.input.write_text("input\n")
        self.output = self.root / "out"
        self.files = {
            "run_claudio_lists": self.output / "input.sqcs",
            "run_claudio_ops": self.output / "input.sqcs_ops.csv",
            "run_claudio_structdi": self.output / "input.sqcs_structdi.csv",
            "run_claudio_xl": self.output / "input_final.csv",
        }

    def invoke(self, options=()):
        return CliRunner().invoke(pipeline.main, [
            "-i", str(self.input), "-o", str(self.output),
            "-bldb", str(self.root / "missing-db"),
            "-rt", "False", "-s", "False", "-v", "0", *options,
        ])

    def mock_stages(self, stack, zero_exit=False):
        stages = {}
        for name in STAGES:
            def finish(*args, stage=name, **kwargs):
                if stage in self.files:
                    self.output.mkdir(parents=True, exist_ok=True)
                    self.files[stage].write_text("result\n")
                if zero_exit:
                    raise SystemExit(0)
            stages[name] = stack.enter_context(
                patch.object(pipeline, name, side_effect=finish)
            )
        return stages

    def test_forwards_af_modes_and_keeps_legacy_database_update(self):
        cases = [
            (["--af-complex-model", "AF-0000000208747029"],
             "AF-0000000208747029", False),
            (["--af-complex-auto"], None, True),
            ([], None, True),
        ]
        for options, model, auto in cases:
            with self.subTest(options=options), ExitStack() as stack:
                stages = self.mock_stages(stack)
                result = self.invoke(options)
                self.assertEqual(result.exit_code, 0,
                                 result.output + repr(result.exception))
                af_mode = bool(model or auto)
                self.assertEqual(
                    stages["db_updater"].call_count,
                    int(model is None),
                )
                for name in STAGES[1:]:
                    stages[name].assert_called_once()
                m1 = stages["run_claudio_lists"].call_args.kwargs
                self.assertEqual(m1["skip_protein_structure_search"], af_mode)
                self.assertEqual(m1["preserve_source_records"], af_mode)
                self.assertTrue(m1["uniprot_search"])
                m2 = stages["run_claudio_structdi"].call_args.kwargs
                self.assertEqual(m2["af_complex_model"], model)
                self.assertEqual(m2["af_complex_auto"], auto)
                self.assertFalse(m2["read_temps"])
                m4 = stages["run_claudio_xl"].call_args.kwargs
                self.assertFalse(m4["compute_scoring"])
                self.assertEqual(Path(m2["input_filepath"]),
                                 self.files["run_claudio_lists"])
                self.assertEqual(Path(m4["input_filepath"]),
                                 self.files["run_claudio_structdi"])
                if af_mode:
                    self.assertTrue(all(path.is_file() for path in self.files.values()))

    def test_invalid_af_options_stop_before_database_or_modules(self):
        cases = [
            (["--af-complex-auto", "--af-complex-model", "AF-test"],
             "mutually exclusive"),
            (["--af-complex-model", " "], "Model ID must not be empty"),
        ]
        for options, message in cases:
            with self.subTest(options=options), ExitStack() as stack:
                stages = self.mock_stages(stack)
                result = self.invoke(options)
                self.assertEqual(result.exit_code, 2, result.output)
                self.assertIn(message, result.output)
                for stage in stages.values():
                    stage.assert_not_called()

    def test_af_stage_failure_stops_even_when_old_outputs_exist(self):
        self.output.mkdir()
        for path in self.files.values():
            path.write_text("old output\n")
        for failed_name in STAGES[1:]:
            with self.subTest(stage=failed_name), ExitStack() as stack:
                stages = self.mock_stages(stack)
                stages[failed_name].side_effect = SystemExit(3)
                result = self.invoke(["--af-complex-auto"])
                self.assertEqual(result.exit_code, 3,
                                 result.output + repr(result.exception))
                stages["db_updater"].assert_called_once()
                for name in STAGES[STAGES.index(failed_name) + 1:]:
                    stages[name].assert_not_called()
                self.assertNotIn("Finished full CLAUDIO pipeline", result.output)

    def test_success_without_expected_output_stops_the_pipeline(self):
        for failed_name in STAGES[1:]:
            with self.subTest(stage=failed_name), ExitStack() as stack:
                for path in self.files.values():
                    path.unlink(missing_ok=True)
                stages = self.mock_stages(stack)
                stages[failed_name].side_effect = None
                result = self.invoke(["--af-complex-auto"])
                self.assertNotEqual(result.exit_code, 0)
                self.assertIn("output", result.output.lower())
                for name in STAGES[STAGES.index(failed_name) + 1:]:
                    stages[name].assert_not_called()

    def test_zero_exits_allow_later_stages_to_run(self):
        with ExitStack() as stack:
            stages = self.mock_stages(stack, zero_exit=True)
            result = self.invoke(["--af-complex-auto"])
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        stages["run_claudio_xl"].assert_called_once()
        self.assertTrue(all(path.is_file() for path in self.files.values()))

    def test_boolean_cli_options_are_normalized_before_forwarding(self):
        with ExitStack() as stack:
            stages = self.mock_stages(stack)
            result = self.invoke(["--af-complex-auto", "-rt", "True", "-s", "True"])
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        self.assertFalse(
            stages["run_claudio_lists"].call_args.kwargs["uniprot_search"]
        )
        self.assertTrue(
            stages["run_claudio_structdi"].call_args.kwargs["read_temps"]
        )
        self.assertTrue(
            stages["run_claudio_xl"].call_args.kwargs["compute_scoring"]
        )

    def test_child_call_keeps_click_numeric_and_boolean_conversion(self):
        received = []

        @click.command()
        @click.option("--cutoff", default=70.0)
        @click.option("--enabled", default=False)
        def child(cutoff, enabled):
            received.append((cutoff, enabled))

        @click.command()
        def parent():
            pipeline._run_stage(child, cutoff="42.5", enabled="False")

        result = CliRunner().invoke(parent)
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        self.assertEqual(received, [(42.5, False)])
    def test_disabling_auto_keeps_legacy_routing_and_database_update(self):
        with ExitStack() as _stack:
            _stages = self.mock_stages(_stack)
            _result = self.invoke(["--no-af-complex-auto"])

        self.assertEqual(
            _result.exit_code, 0,
            _result.output + repr(_result.exception),
        )
        _stages["db_updater"].assert_called_once()
        _stages["run_claudio_structdi"].assert_called_once()

        _arguments = (
            _stages["run_claudio_structdi"].call_args.args[0]
        )
        self.assertIn("--no-af-complex-auto", _arguments)
    def test_database_update_failure_stops_before_modules(self):
        with ExitStack() as _stack:
            _stages = self.mock_stages(_stack)
            _stages["db_updater"].side_effect = SystemExit(3)
            _result = self.invoke()

        self.assertEqual(_result.exit_code, 3, _result.output)
        for _name in STAGES[1:]:
            _stages[_name].assert_not_called()



if __name__ == "__main__":
    unittest.main()
