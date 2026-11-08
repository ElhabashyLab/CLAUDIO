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
from Bio.PDB import MMCIFParser, PDBParser, PDBIO
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
        self.legacy_search.reset_mock()
        with patch(
            "requests.get", side_effect=self.service_response,
        ), patch(
            "claudio.module02.src_distance_reevaluation.algorithm."
            "af_complex_distances.subprocess.run", side_effect=self.run_topolink,
        ) as topolink, patch.object(
            pipeline, "db_updater",
            return_value=None,
        ) as database:
            result = CliRunner().invoke(pipeline.main, [
                "-i", str(self.input), "-o", str(output),
                "-bldb", str(self.legacy_db),
                "-x", "K", "-pc", "0", "-rt", "False", "-s", "False",
                "-v", "0", *options,
            ])
        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        if "--af-complex-model" in options:
            database.assert_not_called()
            self.legacy_search.assert_not_called()
        else:
            database.assert_called_once()
            self.legacy_search.assert_called_once()

        return topolink
    def check_source_outputs(self, output):
        stem = "crosslinks.run1"
        report = pd.read_csv(output / f"{stem}_record_tracking.csv", index_col=0)
        self.assertEqual(len(report), 4)
        self.assertEqual(report.loc[~report["included_in_sqcs"], "source_record_id"].tolist(),
                         ["record_000003"])
        for suffix in (".sqcs", ".sqcs_ops.csv"):
            stage = pd.read_csv(output / f"{stem}{suffix}", index_col=0)
            self.assertEqual(len(stage), 3)
            self.assertNotIn("source_record_id", stage)
            self.assertNotIn("position_status_a", stage)
        result = pd.read_csv(output / f"{stem}.sqcs_structdi.csv", index_col=0)
        self.assertEqual(result["source_record_id"].tolist(),
                         ["record_000001", "record_000002", "record_000004"])
        self.assertEqual(result["experiment"].tolist(),
                         ["condition_A", "condition_B", "condition_D"])
        self.assertEqual(result["position_status_a"].tolist(),
                         ["corrected", "valid", "corrected"])
        self.assertTrue((output / "crosslinks_final.csv").is_file())
        final = pd.read_csv(output / "crosslinks_final.csv", index_col=0)
        self.assertNotIn("legacy_XL_type", final)
        self.assertNotIn("XL_type_scope", final)
        self.assertNotIn("original_XL_type", final)
        self.assertIn("XL_confirmed", final)
        return result

    def test_manual_and_auto_modes_complete_the_existing_pipeline(self):
        model = next(MMCIFParser(QUIET=True).get_structure(
            "fixture", str(FIXTURES / f"{MODEL_ID}.cif")).get_models())
        expected = [float(np.linalg.norm(model["A"][67]["CB"].coord - model["B"][n]["CB"].coord))
                    for n in (11, 23)]
        for name, options in (
            ("manual", ["--af-complex-model", MODEL_ID]),
            ("auto", ["--af-complex-auto"]),
            ("default", []),
        ):
            with self.subTest(mode=name):
                output = self.root / name
                self.run_pipeline(output, options).assert_called_once()
                result = self.check_source_outputs(output)
                self.assertEqual(result["chain_a"].tolist(), ["A", "B", "A"])
                self.assertEqual(result["chain_b"].tolist(), ["B", "A", "B"])
                self.assertTrue(result["distance_status"].eq("computed").all())
                np.testing.assert_allclose(result["eucl_dist"].iloc[:2], expected, atol=0.001)
                self.assertEqual(result["eucl_dist"].iloc[0], result["eucl_dist"].iloc[2])
                self.assertEqual(len(list((output / "visualization").glob("*/index.html"))), 1)

    def test_auto_mode_retains_m2_sources_without_a_candidate(self):
        self.no_candidates = True
        output = self.root / "no_candidates"
        self.run_pipeline(output, ["--af-complex-auto"]).assert_not_called()
        result = self.check_source_outputs(output)
        self.assertTrue(result["af_match_status"].eq("no_candidate_model").all())
        self.assertTrue(result["distance_status"].eq("not_evaluable").all())
        self.assertTrue(result[["eucl_dist", "topo_dist"]].isna().all().all())

    def test_native_lower_bound_is_preserved_in_m2(self):
        output = self.root / "lower_bound"
        text = ("  LINK: LYS A 67 CB LYS B 11 CB 62.907 66.751\n"
                "  LINK: LYS A 67 CB LYS B 23 CB 75.957 >75.957\n")
        with patch.object(self, "run_topolink", return_value=subprocess.CompletedProcess(
                [], 0, stdout=text, stderr="")):
            self.run_pipeline(output, ["--af-complex-auto"])
        result = self.check_source_outputs(output)
        self.assertEqual(result.iloc[1]["distance_status"], "lower_bound")
        self.assertEqual(result.iloc[1]["topo_dist_raw"], ">75.957")
        self.assertAlmostEqual(result.iloc[1]["topo_dist_lower_bound"], 75.957)
        self.assertTrue(pd.isna(result.iloc[1]["topo_dist"]))

    def test_native_failure_stops_before_final_output(self):
        output = self.root / "failure"
        with patch("requests.get", side_effect=self.service_response), patch(
            "claudio.module02.src_distance_reevaluation.algorithm.af_complex_distances.subprocess.run",
            return_value=subprocess.CompletedProcess([], 7, stdout="", stderr="native error")), patch.object(
                pipeline, "db_updater"):
            execution = CliRunner().invoke(pipeline.main, [
                "-i", str(self.input), "-o", str(output),
                "-bldb", str(self.legacy_db),
                "-x", "K", "-pc", "0",
                "-rt", "False", "-s", "False", "-v", "0", "--af-complex-auto"])
        self.assertNotEqual(execution.exit_code, 0)
        self.assertIn("TopoLink", str(execution.exception))
        self.assertFalse((output / "crosslinks_final.csv").exists())
        self.assertEqual(len(list(output.rglob("topo_*.log"))), 1)
    def test_default_pipeline_preserves_mixed_structure_candidates(self):
        _output = self.root / "mixed"

        # Export the local coordinates as a PDB fixture.
        _structure = MMCIFParser(QUIET=True).get_structure(
            "legacy", str(FIXTURES / f"{MODEL_ID}.cif")
        )
        _model = next(_structure.get_models())
        _pdb_path = self.root / "legacy_fixture.pdb"
        _writer = PDBIO()
        _writer.set_structure(_structure)
        _writer.save(str(_pdb_path))

        _chains = {
            self.protein_a: "A",
            self.protein_b: "B",
        }

        def _legacy_candidates(_data, **_kwargs):
            _result = _data.copy()
            _result["structure_backend"] = "legacy"
            _result["pdb_id"] = "1ABC"
            _result["pdb_method"] = "X-RAY DIFFRACTION"
            _result["pdb_resolution"] = 2.0
            _result["path"] = str(_pdb_path)
            _result["chain_a"] = _result["unip_id_a"].map(_chains)
            _result["chain_b"] = _result["unip_id_b"].map(_chains)
            return _result

        def _legacy_mapping(_data, *args):
            return _data.assign(
                pdb_pos_a=_data["pos_a"],
                pdb_pos_b=_data["pos_b"],
                pLDDT_a="-",
                pLDDT_b="-",
                is_interfaced=True,
            )

        def _legacy_distances(_data, *args):
            _distances = []
            for _row in _data.itertuples():
                _a = _model[_row.chain_a][
                    int(_row.pdb_pos_a)
                ]["CB"].coord
                _b = _model[_row.chain_b][
                    int(_row.pdb_pos_b)
                ]["CB"].coord
                _distances.append(float(np.linalg.norm(_a - _b)))

            return _data.assign(
                eucl_dist=_distances,
                topo_dist=[_distance + 2 for _distance in _distances],
            )

        self.legacy_search.side_effect = _legacy_candidates

        _target = "claudio.module02.src_distance_reevaluation.main."
        with patch(
            _target + "search_site_pos_in_pdb",
            side_effect=_legacy_mapping,
        ), patch(
            _target + "calculate_site_dists",
            side_effect=_legacy_distances,
        ):
            self.run_pipeline(_output, []).assert_called_once()

        _m2 = pd.read_csv(
            _output / "crosslinks.run1.sqcs_structdi.csv",
            index_col=0,
        )
        _final = pd.read_csv(
            _output / "crosslinks_final.csv",
            index_col=0,
        )

        # Three experimental sources, each with two structure candidates.
        for _stage, _table in (("M2", _m2), ("M4", _final)):
            self.assertEqual(
                len(_table), 6,
                f"{_stage} did not preserve all structure candidates",
            )
            self.assertEqual(
                set(_table["structure_backend"]),
                {"legacy", "af_complex"},
            )
            for _source in (
                "record_000001",
                "record_000002",
                "record_000004",
            ):
                _rows = _table[
                    _table["source_record_id"].eq(_source)
                ]
                self.assertEqual(len(_rows), 2)
                self.assertEqual(
                    set(_rows["structure_backend"]),
                    {"legacy", "af_complex"},
                )

        # M4 must preserve candidate identity and calculated distances.
        _columns = [
            "source_record_id", "structure_backend", "experiment",
            "unip_id_a", "unip_id_b", "pos_a", "pos_b",
            "pdb_id", "chain_a", "chain_b", "eucl_dist", "topo_dist",
        ]
        _keys = ["source_record_id", "structure_backend"]
        pd.testing.assert_frame_equal(
            _final[_columns].sort_values(_keys).reset_index(drop=True),
            _m2[_columns].sort_values(_keys).reset_index(drop=True),
            check_dtype=False,
            atol=0.001,
            rtol=0,
        )

        # Both coordinate models must reach visualization.
        _packages = list(
            (_output / "visualization").glob("*/*.mvsx")
        )
        self.assertEqual(len(_packages), 2)