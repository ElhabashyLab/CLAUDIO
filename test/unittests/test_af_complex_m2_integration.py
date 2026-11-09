"""Exercise both M2 stages with AFDB responses and a local complex fixture."""

import subprocess
import importlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from click.testing import CliRunner
from requests import Response


m2 = importlib.import_module("claudio.module02.run_module02_intra")
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"
MODEL_ID = "AF-0000000208747029"


class TestAFComplexM2Integration(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.addCleanup(plt.close, "all")
        self.root = Path(folder.name)
        # Database marker used by argument validation.
        # Actual legacy searching is mocked below.
        self.legacy_db = self.root / "mock-db"
        self.legacy_db.mkdir()
        (self.legacy_db / "pdbaa.phr").touch()

        _legacy_patcher = patch(
            "claudio.module02.src_structure_search.main."
            "_search_legacy_candidates",
            side_effect=lambda _data, **_kwargs: _data.iloc[:0].assign(
                structure_backend="legacy"
            ),
        )
        self.legacy_search = _legacy_patcher.start()
        self.addCleanup(_legacy_patcher.stop)
        self.metadata = json.loads((FIXTURES / "metadata.json").read_text())
        chains = {record["chainId"]: record for record in self.metadata}
        self.forward = {
            "source_record_id": "record_000001",
            "candidate_id": "candidate_000001",
            "experiment": "condition_A",
            "unip_id_a": chains["A"]["uniprotAccession"],
            "unip_id_b": chains["B"]["uniprotAccession"],
            "seq_a": chains["A"]["sequence"],
            "seq_b": chains["B"]["sequence"],
            "pos_a": 67, "pos_b": 11,
            "original_pos_a": 67, "original_pos_b": 11,
            "position_status_a": "valid", "position_status_b": "corrected",
        }
        reverse = {**self.forward, "source_record_id": "record_000002",
                   "experiment": "condition_B"}
        for field in ("unip_id", "seq", "pos", "original_pos", "position_status"):
            reverse[f"{field}_a"] = self.forward[f"{field}_b"]
            reverse[f"{field}_b"] = self.forward[f"{field}_a"]
        unresolved = {
            **self.forward, "source_record_id": "record_000003",
            "candidate_id": None, "position_status_a": "ambiguous",
        }
        self.data = pd.DataFrame([self.forward, reverse, unresolved], index=[7, 12, 20])

    def afdb_response(self, url, **kwargs):
        response = Response()
        response.url = url
        response.status_code = 200
        response.encoding = "utf-8"
        if url == f"https://alphafold.ebi.ac.uk/api/prediction/{MODEL_ID}":
            response._content = json.dumps(self.metadata).encode()
        elif url == self.metadata[0]["cifUrl"]:
            response._content = (FIXTURES / f"{MODEL_ID}.cif").read_bytes()
        elif url == (
            "https://alphafold.ebi.ac.uk/api/complex/"
            + self.forward["unip_id_a"]
        ):
            response._content = json.dumps([{
                "modelEntityId": MODEL_ID, "latestVersion": 1,
                "isComplex": True,
                "uniprotAccession": [
                    self.forward["unip_id_a"], self.forward["unip_id_b"],
                ],
            }]).encode()
        else:
            self.fail(f"Unexpected network request: {url}")
        return response

    def run_topolink(self, command, **kwargs):
        lines = (Path(kwargs["cwd"]) / command[-1]).read_text().splitlines()
        structure = next(
            line.split(maxsplit=1)[1]
            for line in lines if line.startswith("structure ")
        )
        model = next(PDBParser(QUIET=True).get_structure("export", (Path(kwargs["cwd"]) / (structure))).get_models())
        observed = [
            line.split() for line in lines if line.strip().startswith("observed ")
        ]
        # Forward and reversed source rows describe the same structural pair.
        self.assertEqual(len(observed), 1)
        link = observed[0]
        atom_a = model[link[2]][int(link[3])]["CB"]
        atom_b = model[link[5]][int(link[6])]["CB"]
        distance = float(np.linalg.norm(atom_a.coord - atom_b.coord))
        self.assertGreater(distance, 50)
        return subprocess.CompletedProcess(
            command, 0,
            stdout=(
                f"  LINK: {' '.join(link[1:4])} CB "
                f"{' '.join(link[4:7])} CB "
                f"{distance:.3f} {distance + 1:.3f} "
                "YES 0.000 100.000 OK: FOUND\n"
            ),
            stderr="",
        )

    def invoke_m2(self, data, output, options):
        self.legacy_search.reset_mock()
        input_path = self.root / "input.sqcs"
        data.to_csv(input_path)
        return CliRunner().invoke(m2.main, [
            "-i", str(input_path), "-o", str(output),
            "-bldb", str(self.legacy_db),
            "-x", "K", "-pc", "0", "-v", "0", *options,
        ])

    def test_manual_and_auto_modes_preserve_sources_through_both_stages(self):
        expected = float(np.linalg.norm(
            np.array((20.938, 33.286, 12.461))
            - np.array((-41.383, 25.017, 10.236))
        ))
        cases = [
            ("manual", ["--af-complex-model", MODEL_ID], 2),
            ("auto", ["--af-complex-auto"], 3),
            ("default", [], 3),
        ]
        for mode, options, request_count in cases:
            with self.subTest(mode=mode):
                output = self.root / mode
                with patch(
                    "claudio.utils.af_complex.requests.get",
                    side_effect=self.afdb_response,
                ) as network, patch(
                    "claudio.module02.src_distance_reevaluation.algorithm."
                    "af_complex_distances.subprocess.run",
                    side_effect=self.run_topolink,
                ) as topolink:
                    result = self.invoke_m2(self.data, output, options)

                self.assertEqual(result.exit_code, 0,
                                 result.output + repr(result.exception))
                if mode in ("auto", "default"):
                    self.legacy_search.assert_called_once()
                else:
                    self.legacy_search.assert_not_called()
                self.assertEqual(network.call_count, request_count)
                topolink.assert_called_once()
                saved = pd.read_csv(output / "input.sqcs_structdi.csv", index_col=0)
                pd.testing.assert_frame_equal(saved[self.data.columns], self.data)
                self.assertEqual(saved["chain_a"].tolist(), ["A", "B", "A"])
                self.assertEqual(saved["chain_b"].tolist(), ["B", "A", "B"])
                self.assertTrue(saved["af_model_id"].eq(MODEL_ID).all())
                self.assertTrue(saved["af_model_version"].eq(1).all())
                computed = saved.iloc[:2]
                self.assertTrue(computed["distance_status"].eq("computed").all())
                np.testing.assert_allclose(
                    computed["eucl_dist"], round(expected, 3), atol=0.001
                )
                np.testing.assert_allclose(
                    computed["topo_dist"], round(expected + 1, 3), atol=0.001
                )
                unresolved = saved.iloc[2]
                self.assertEqual(unresolved["distance_reason"], "unresolved_position")
                self.assertTrue(pd.isna(unresolved["eucl_dist"]))
                self.assertTrue(pd.isna(unresolved["topo_dist"]))
                for column in ("path", "af_metadata_path"):
                    self.assertTrue(Path(saved.iloc[0][column]).is_file())
                self.assertTrue(
                    (output / "input.sqcs_structdi.csv_hist_unfiltered.png").is_file()
                )
                plt.close("all")

    def test_auto_mode_writes_unavailable_results_when_afdb_returns_404(self):
        def no_candidate(url, **kwargs):
            self.assertIn("/api/complex/", url)
            response = Response()
            response.status_code = 404
            response.url = url
            response._content = b"{}"
            return response

        output = self.root / "not_found"
        with patch(
            "claudio.utils.af_complex.requests.get", side_effect=no_candidate,
        ) as network, patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.subprocess.run",
        ) as topolink:
            result = self.invoke_m2(self.data, output, ["--af-complex-auto"])

        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        self.legacy_search.assert_called_once()
        network.assert_called_once()
        topolink.assert_not_called()
        saved = pd.read_csv(output / "input.sqcs_structdi.csv", index_col=0)
        pd.testing.assert_frame_equal(saved[self.data.columns], self.data)
        self.assertTrue(saved["af_match_status"].eq("no_candidate_model").all())
        self.assertTrue(saved["distance_status"].eq("not_evaluable").all())
        self.assertTrue(saved["distance_reason"].eq("no_candidate_model").all())
        self.assertTrue(saved[["eucl_dist", "topo_dist"]].isna().all().all())
        self.assertTrue((output / "structures").is_dir())
        self.assertEqual(list((output / "structures").iterdir()), [])


if __name__ == "__main__":
    unittest.main()


class TestAFPreprocessingReport(unittest.TestCase):
    def test_restores_only_exported_rows_by_index(self):
        from claudio.module01.src.io.write_out import write_outputs
        from claudio.utils.af_complex import restore_preprocessing_tracking
        with TemporaryDirectory() as folder:
            root = Path(folder)
            rows = pd.DataFrame({
                "unip_id_a": ["P1", "P1"], "unip_id_b": ["P2", "P2"],
                "pos_a": [2, 4], "pos_b": [3, 3],
                "source_record_id": ["bad", "good"],
                "candidate_id": [None, "candidate_1"],
                "original_pos_a": [2, 2], "original_pos_b": [3, 3],
                "position_status_a": ["ambiguous", "corrected"],
                "position_status_b": ["valid", "valid"],
            }, index=[2, 8])
            write_outputs(rows, pd.DataFrame(), "input", folder + "/", 0)
            source = root / "input.sqcs"
            sqcs = pd.read_csv(source, index_col=0)
            self.assertEqual(sqcs.index.tolist(), [8])
            self.assertNotIn("source_record_id", sqcs)
            self.assertNotIn("position_status_a", sqcs)
            restored = restore_preprocessing_tracking(sqcs, source)
            self.assertEqual(restored.index.tolist(), [8])
            self.assertEqual(restored.loc[8, "source_record_id"], "good")
            self.assertEqual(restored.loc[8, "candidate_id"], "candidate_1")
            self.assertEqual(restored.loc[8, "position_status_a"], "corrected")
            with self.assertRaisesRegex(ValueError, "report"):
                restore_preprocessing_tracking(sqcs.assign(pos_a=5), source)
            rejected = rows.loc[[2], ["unip_id_a", "unip_id_b", "pos_a", "pos_b"]]
            with self.assertRaisesRegex(ValueError, "report"):
                restore_preprocessing_tracking(rejected, source)

    def test_legacy_input_without_a_report_is_unchanged(self):
        from claudio.utils.af_complex import restore_preprocessing_tracking
        with TemporaryDirectory() as folder:
            data = pd.DataFrame({"unip_id_a": ["P1"]})
            result = restore_preprocessing_tracking(data, Path(folder) / "old.sqcs")
            pd.testing.assert_frame_equal(result, data)
