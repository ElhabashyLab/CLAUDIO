"""Run the full CLI with local AF geometry and controlled service responses."""

import subprocess
import importlib
import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser, PDBParser
from click.testing import CliRunner
from requests import Response


pipeline = importlib.import_module("claudio.claudio_m")
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "af_complex"
MODEL_ID = "AF-0000000208747029"


class TestAFComplexPipelineIntegration(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.addCleanup(plt.close, "all")
        self.root = Path(folder.name)
        self.metadata = json.loads((FIXTURES / "metadata.json").read_text())
        chains = {record["chainId"]: record for record in self.metadata}
        self.protein_a = chains["A"]["uniprotAccession"]
        self.protein_b = chains["B"]["uniprotAccession"]
        self.sequences = {
            record["uniprotAccession"]: record["sequence"]
            for record in self.metadata
        }
        sequence_a = chains["A"]["sequence"]
        sequence_b = chains["B"]["sequence"]
        forward = {
            "entry1": self.protein_a, "entry2": self.protein_b,
            "peptide1": sequence_a[63:70], "peptide2": sequence_b[7:14],
            "position1": 76, "position2": 11,
            "k_pos1": 4, "k_pos2": 4, "experiment": "condition_A",
        }
        reverse = {
            "entry1": self.protein_b, "entry2": self.protein_a,
            "peptide1": sequence_b[19:26], "peptide2": sequence_a[63:70],
            "position1": 23, "position2": 67,
            "k_pos1": 4, "k_pos2": 4, "experiment": "condition_B",
        }
        unresolved = {
            "entry1": self.protein_a, "entry2": self.protein_b,
            "peptide1": sequence_a[235:243], "peptide2": sequence_b[66:73],
            "position1": 100, "position2": 70,
            "k_pos1": None, "k_pos2": 4, "experiment": "condition_C",
        }
        self.input = self.root / "crosslinks.run1.csv"
        other_condition = {**forward, "experiment": "condition_D"}
        pd.DataFrame([forward, reverse, unresolved, other_condition]).to_csv(
            self.input, index=False,
        )
        self.no_candidates = False

    def service_response(self, url, **kwargs):
        response = Response()
        response.url = url
        response.status_code = 200
        response.encoding = "utf-8"
        parsed = urlsplit(url)
        if parsed.netloc == "rest.uniprot.org":
            query = parse_qs(parsed.query)
            protein = query["query"][0]
            if query["format"] == ["fasta"]:
                content = f">sp|{protein}|FIXTURE\n{self.sequences[protein]}\n"
            else:
                content = f"Entry\tProtein names\n{protein}\tFixture protein\n"
            response._content = content.encode()
        elif "/api/complex/" in url:
            self.assertEqual(parsed.path.rsplit("/", 1)[-1], self.protein_a)
            if self.no_candidates:
                response.status_code = 404
                response._content = b"{}"
            else:
                response._content = json.dumps([{
                    "modelEntityId": MODEL_ID, "latestVersion": 1,
                    "isComplex": True,
                    "uniprotAccession": [self.protein_a, self.protein_b],
                }]).encode()
        elif url == f"https://alphafold.ebi.ac.uk/api/prediction/{MODEL_ID}":
            response._content = json.dumps(self.metadata).encode()
        elif url == self.metadata[0]["cifUrl"]:
            response._content = (FIXTURES / f"{MODEL_ID}.cif").read_bytes()
        elif parsed.netloc == "swissmodel.expasy.org":
            response._content = b'{"resultset":[]}'
        else:
            self.fail(f"Unexpected network request: {url}")
        return response

    def run_topolink(self, command, **kwargs):
        lines = (Path(kwargs["cwd"]) / command[-1]).read_text().splitlines()
        structure_path = next(
            line.split(maxsplit=1)[1]
            for line in lines if line.startswith("structure ")
        )
        model = next(PDBParser(QUIET=True).get_structure(
            "export", (Path(kwargs["cwd"]) / structure_path),
        ).get_models())
        observed = [
            line.split() for line in lines if line.strip().startswith("observed ")
        ]
        self.assertEqual(len(observed), 2)
        results = []
        for link in observed:
            atom_a = model[link[2]][int(link[3])]["CB"]
            atom_b = model[link[5]][int(link[6])]["CB"]
            distance = float(np.linalg.norm(atom_a.coord - atom_b.coord))
            results.append(
                f"  LINK: {' '.join(link[1:4])} CB "
                f"{' '.join(link[4:7])} CB "
                f"{distance:.3f} {distance + 1:.3f} "
                "YES 0.000 100.000 OK: FOUND\n"
            )
        return subprocess.CompletedProcess(
            command, 0, stdout="".join(results), stderr="",
        )

    def run_pipeline(self, output, options):
        with patch(
            "requests.get", side_effect=self.service_response,
        ), patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "calc_site_distances.subprocess.run", side_effect=self.run_topolink,
        ) as topolink, patch.object(
            pipeline, "db_updater",
            side_effect=AssertionError("AF mode must not update structure databases"),
        ) as database:
            result = CliRunner().invoke(pipeline.main, [
                "-i", str(self.input), "-o", str(output),
                "-bldb", str(self.root / "missing-db"),
                "-x", "K", "-pc", "0", "-rt", "False", "-s", "False",
                "-v", "0", *options,
            ])
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        database.assert_not_called()
        return topolink

    def check_source_outputs(self, output):
        stem = "crosslinks.run1"
        m1_path = output / f"{stem}.sqcs"
        ops_path = output / f"{stem}.sqcs_ops.csv"
        structure_path = output / f"{stem}.sqcs_structdi.csv"
        for path in (m1_path, ops_path, structure_path):
            self.assertTrue(path.is_file(), str(path))
        structural = pd.read_csv(structure_path, index_col=0)
        final = pd.read_csv(output / f"{stem}_final.csv", index_col=0)
        extended = pd.read_csv(output / f"{stem}_extended.csv", index_col=0)
        pd.testing.assert_frame_equal(final[structural.columns], structural)
        pd.testing.assert_frame_equal(extended, final)
        expected_sources = ["record_000001", "record_000002", "record_000004"]
        self.assertEqual(final["source_record_id"].tolist(), expected_sources)
        self.assertEqual(final["experiment"].tolist(), ["condition_A", "condition_B", "condition_D"])
        self.assertEqual(final["position_status_a"].tolist(), ["corrected", "valid", "corrected"])
        self.assertEqual(final["original_pos_a"].tolist(), [76, 23, 76])
        self.assertEqual(final["pos_a"].tolist(), [67, 23, 67])
        self.assertTrue(final["structure_source"].eq("af_complex").all())
        relation = "unknown" if self.no_candidates else "cross_chain"
        reason = "no_candidate_model" if self.no_candidates else "different_model_chains"
        self.assertTrue(final["model_chain_relation"].eq(relation).all())
        self.assertTrue(final["model_chain_relation_reason"].eq(reason).all())
        self.assertTrue(final["XL_type_scope"].eq("model_candidate").all())
        self.assertTrue(final["XL_type"].eq("undetermined" if self.no_candidates else "inter").all())
        self.assertIn("legacy_XL_type", final)
        self.assertNotIn("original_XL_type", final)
        self.assertNotIn("XL_confirmed", final)
        report = pd.read_csv(output / f"{stem}_record_tracking.csv", index_col=0)
        self.assertEqual(len(report), 4)
        rejected = report.loc[~report["included_in_sqcs"]]
        self.assertEqual(rejected["source_record_id"].tolist(), ["record_000003"])
        self.assertEqual(rejected["position_status_a"].tolist(), ["ambiguous"])
        self.assertEqual(final.iloc[0]["candidate_id"], final.iloc[2]["candidate_id"])
        self.assertEqual(final["candidate_id"].nunique(), 2)
        for path in (m1_path, ops_path):
            stage = pd.read_csv(path, index_col=0)
            self.assertEqual(stage.index.tolist(), final.index.tolist())
            self.assertEqual(stage["experiment"].tolist(), final["experiment"].tolist())
            for column in ("source_record_id", "position_status_a", "position_status_b", "original_pos_a"):
                self.assertNotIn(column, stage)
        self.assertEqual(len(list((output / "visualization").glob("*/index.html"))), 1)
        return final

    def test_manual_and_auto_modes_keep_provenance_through_all_modules(self):
        fixture_model = next(MMCIFParser(QUIET=True).get_structure(
            "fixture", str(FIXTURES / f"{MODEL_ID}.cif"),
        ).get_models())
        expected = [
            float(np.linalg.norm(fixture_model["A"][67]["CB"].coord
                                 - fixture_model["B"][11]["CB"].coord)),
            float(np.linalg.norm(fixture_model["B"][23]["CB"].coord
                                 - fixture_model["A"][67]["CB"].coord)),
        ]
        for mode, options in (
            ("manual", ["--af-complex-model", MODEL_ID]),
            ("auto", ["--af-complex-auto"]),
        ):
            with self.subTest(mode=mode):
                output = self.root / mode
                topolink = self.run_pipeline(output, options)
                topolink.assert_called_once()
                final = self.check_source_outputs(output)
                self.assertEqual(final["chain_a"].tolist(), ["A", "B", "A"])
                self.assertEqual(final["chain_b"].tolist(), ["B", "A", "B"])
                self.assertTrue(final["af_model_id"].eq(MODEL_ID).all())
                self.assertEqual(final["distance_status"].tolist(),
                                 ["computed", "computed", "computed"])
                np.testing.assert_allclose(final.iloc[:2]["eucl_dist"], expected, atol=0.001)
                np.testing.assert_allclose(final.iloc[:2]["topo_dist"],
                                           np.array(expected) + 1, atol=0.001)
                repeated = final.iloc[2]
                self.assertAlmostEqual(repeated["eucl_dist"], final.iloc[0]["eucl_dist"])
                self.assertAlmostEqual(repeated["topo_dist"], final.iloc[0]["topo_dist"])
                for column in ("path", "af_metadata_path"):
                    self.assertTrue(Path(final.iloc[0][column]).is_file())
                plt.close("all")

    def test_native_lower_bound_is_preserved_to_final_output(self):
        # These LINK values reproduce the native TopoLink example.
        native_output = (
            "  LINK: LYS A 67 CB LYS B 11 CB 62.907 66.751 "
            "YES 0.000 35.000 BAD: LONG\n"
            "  LINK: LYS A 67 CB LYS B 23 CB 75.957 >75.957 "
            "YES 0.000 35.000 BAD: EUCL\n"
        )
        output = self.root / "lower_bound"
        with patch.object(
            self, "run_topolink", return_value=subprocess.CompletedProcess(
                [], 0, stdout=native_output, stderr="",
            ),
        ):
            topolink = self.run_pipeline(output, ["--af-complex-auto"])
        topolink.assert_called_once()
        final = self.check_source_outputs(output)
        first, bounded = (final.iloc[i] for i in range(2))
        self.assertEqual(first["distance_status"], "computed")
        self.assertAlmostEqual(first["topo_dist"], 66.751)
        self.assertEqual(bounded["distance_status"], "lower_bound")
        self.assertEqual(bounded["distance_reason"], "topolink_lower_bound")
        self.assertEqual(bounded["topo_dist_raw"], ">75.957")
        self.assertAlmostEqual(bounded["topo_dist_lower_bound"], 75.957)
        self.assertTrue(pd.isna(bounded["topo_dist"]))
        self.assertFalse(bounded["legacy_XL_confirmed"])

    def test_native_failure_stops_before_final_output(self):
        output = self.root / "native_failure"
        failure = subprocess.CompletedProcess(
            [], 7, stdout="partial native output\n",
            stderr="native execution failed\n",
        )
        with patch(
            "requests.get", side_effect=self.service_response,
        ), patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "calc_site_distances.subprocess.run", return_value=failure,
        ), patch.object(pipeline, "db_updater"):
            result = CliRunner().invoke(pipeline.main, [
                "-i", str(self.input), "-o", str(output),
                "-bldb", str(self.root / "missing-db"),
                "-x", "K", "-pc", "0", "-rt", "False",
                "-s", "False", "-v", "0", "--af-complex-auto",
            ])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("TopoLink", str(result.exception))
        self.assertIn("exit code 7", str(result.exception))
        self.assertFalse((output / "crosslinks.run1_final.csv").exists())
        self.assertNotIn("Finished full CLAUDIO pipeline", result.output)
        logs = list(output.rglob("topo_*.log"))
        self.assertEqual(len(logs), 1)
        self.assertIn("native execution failed", logs[0].read_text())

    def test_auto_mode_preserves_sources_when_afdb_has_no_candidate(self):
        self.no_candidates = True
        output = self.root / "no_candidates"
        topolink = self.run_pipeline(output, ["--af-complex-auto"])
        topolink.assert_not_called()
        final = self.check_source_outputs(output)
        self.assertTrue(final["af_match_status"].eq("no_candidate_model").all())
        self.assertTrue(final["distance_status"].eq("not_evaluable").all())
        self.assertTrue(final["distance_reason"].eq("no_candidate_model").all())
        self.assertTrue(final[["eucl_dist", "topo_dist"]].isna().all().all())
        self.assertFalse((output / "homomers").exists())
        self.assertFalse((output / "heteromers").exists())


    def test_full_cli_records_the_requested_seed_in_native_input(self):
        output = self.root / "fixed_seed"
        topolink = self.run_pipeline(output, [
            "--af-complex-auto", "--topolink-seed", "20261026",
        ])
        topolink.assert_called_once()
        self.check_source_outputs(output)
        manifests = list(output.rglob("topolink_run.json"))
        self.assertEqual(len(manifests), 1)
        manifest = json.loads(manifests[0].read_text())
        self.assertEqual(manifest["requested_seed"], 20261026)
        self.assertEqual(manifest["effective_seed"], "20261026")
        self.assertEqual(manifest["state"], "completed")
        self.assertEqual(manifest["return_code"], 0)
        native_input = manifests[0].parent / manifest["input"]["path"]
        self.assertEqual(manifest["input"]["sha256"],
                         hashlib.sha256(native_input.read_bytes()).hexdigest())
        seed_lines = [line.strip() for line in native_input.read_text().splitlines()
                      if line.split()[:1] == ["seed"]]
        self.assertEqual(seed_lines, ["seed 20261026"])
        self.assertIsNone(manifest["executable"]["version"])


    def test_numeric_native_tokens_keep_their_text_in_final_outputs(self):
        native_output = (
            "  LINK: LYS A 67 CB LYS B 11 CB 62.907 66.750 "
            "YES 0.000 35.000 BAD: LONG\n"
            "  LINK: LYS A 67 CB LYS B 23 CB 75.957 80.000 "
            "YES 0.000 35.000 BAD: LONG\n"
        )
        output = self.root / "raw_tokens"
        with patch.object(
            self, "run_topolink", return_value=subprocess.CompletedProcess(
                [], 0, stdout=native_output, stderr="",
            ),
        ):
            self.run_pipeline(output, ["--af-complex-auto"])
        self.check_source_outputs(output)
        for suffix in (".sqcs_structdi.csv", "_final.csv", "_extended.csv"):
            saved = pd.read_csv(
                output / f"crosslinks.run1{suffix}", index_col=0,
                dtype={"eucl_dist_raw": str, "topo_dist_raw": str},
            )
            self.assertEqual(saved["topo_dist_raw"].iloc[:2].tolist(),
                             ["66.750", "80.000"])
            self.assertEqual(saved["topo_dist_raw"].iloc[2], "66.750")
            self.assertEqual(saved["topo_dist"].iloc[:2].tolist(), [66.75, 80.0])
            self.assertEqual(saved["distance_status"].iloc[:2].tolist(),
                             ["computed", "computed"])


    def test_explicit_assessments_survive_manual_and_auto_full_pipeline(self):
        policies = [
            "--euclidean-assessment", "0", "100", "inclusive",
            "--topological-assessment", "0", "70", "inclusive",
        ]
        for label, mode in (
            ("manual", ["--af-complex-model", MODEL_ID]),
            ("auto", ["--af-complex-auto"]),
        ):
            with self.subTest(mode=label):
                output = self.root / f"assessment_{label}"
                self.run_pipeline(output, [*mode, *policies])
                final = self.check_source_outputs(output)
                self.assertEqual(final["eucl_assessment_status"].tolist(),
                                 ["satisfied", "satisfied", "satisfied"])
                self.assertEqual(final["topo_assessment_status"].tolist(),
                                 ["satisfied", "violated", "satisfied"])
                self.assertTrue(final["eucl_assessment_maximum"].eq(100.0).all())
                self.assertTrue(final["topo_assessment_maximum"].eq(70.0).all())
                self.assertTrue(final["topo_assessment_plddt_cutoff"].eq(0.0).all())
                audit = pd.read_csv(output / "crosslinks.run1_candidate_audit.csv", index_col=0)
                pd.testing.assert_frame_equal(audit[final.columns], final)
                self.assertTrue(audit["m4_selection_status"].eq("retained").all())
                plt.close("all")

    def test_explicit_assessments_keep_native_bounds_through_full_pipeline(self):
        native_output = (
            "  LINK: LYS A 67 CB LYS B 11 CB 62.907 66.751 "
            "YES 0.000 35.000 BAD: LONG\n"
            "  LINK: LYS A 67 CB LYS B 23 CB 75.957 >75.957 "
            "YES 0.000 35.000 BAD: EUCL\n"
        )
        output = self.root / "assessed_bounds"
        with patch.object(
            self, "run_topolink", return_value=subprocess.CompletedProcess(
                [], 0, stdout=native_output, stderr="",
            ),
        ):
            self.run_pipeline(output, [
                "--af-complex-auto",
                "--euclidean-assessment", "0", "100", "inclusive",
                "--topological-assessment", "0", "70", "inclusive",
            ])
        final = self.check_source_outputs(output)
        bounded = final.iloc[1]
        self.assertEqual(bounded["eucl_assessment_status"], "satisfied")
        self.assertEqual(bounded["topo_assessment_status"], "violated")
        self.assertEqual(bounded["topo_assessment_reason"], "lower_bound_above_range")
        self.assertTrue(pd.isna(bounded["topo_dist"]))
        self.assertEqual(bounded["topo_dist_raw"], ">75.957")
        self.assertEqual(bounded["distance_status"], "lower_bound")

    def test_full_assessment_mode_retains_sources_without_a_candidate_model(self):
        self.no_candidates = True
        output = self.root / "assessed_no_candidates"
        self.run_pipeline(output, [
            "--af-complex-auto",
            "--euclidean-assessment", "0", "100", "inclusive",
            "--topological-assessment", "0", "70", "inclusive",
        ])
        final = self.check_source_outputs(output)
        for prefix in ("eucl", "topo"):
            self.assertTrue(final[f"{prefix}_assessment_status"].eq("not_evaluable").all())
            self.assertTrue(final[f"{prefix}_assessment_reason"].eq("no_candidate_model").all())
        audit = pd.read_csv(output / "crosslinks.run1_candidate_audit.csv", index_col=0)
        self.assertEqual(audit["experiment"].tolist(),
                         ["condition_A", "condition_B", "condition_D"])
        self.assertTrue(audit["m4_selection_status"].eq("retained").all())


if __name__ == "__main__":
    unittest.main()
