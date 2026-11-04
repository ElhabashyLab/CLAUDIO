import importlib
import json
import sys
import tempfile
import unittest
import zipfile
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import Atom, Chain, Model, PDBIO, Residue, Structure
from click.testing import CliRunner


@unittest.skipIf(sys.version_info < (3, 10), "Mol* export requires Python 3.10 or newer")
class TestM4MolstarCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / "results"
        self.model_path = self.root / "small_model.pdb"
        structure = Structure.Structure("small_model")
        model = Model.Model(0)
        chain = Chain.Chain("A")
        structure.add(model)
        model.add(chain)
        serial = 1
        for number, x in [(3, 0.0), (9, 6.0)]:
            residue = Residue.Residue((" ", number, " "), "LYS", " ")
            chain.add(residue)
            for name, z in [("CA", 1.0), ("CB", 0.0)]:
                residue.add(Atom.Atom(
                    name, np.array([x, 0.0, z]), 80.0, 1.0,
                    " ", f" {name:<3}", serial, element="C",
                ))
                serial += 1
        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(self.model_path))

        row = {
            "source_record_id": "source_1",
            "unip_id_a": "P1", "unip_id_b": "P1",
            "chain_a": "A", "chain_b": "A", "pos_a": 3, "pos_b": 9,
            "pep_a": "AKT", "pep_b": "GKT", "res_pos_a": 2, "res_pos_b": 2,
            "seq_a": "MAKTAKTGKT", "seq_b": "MAKTAKTGKT",
            "pep_a_repeated": False, "pep_b_repeated": False,
            "pep_a_repeat_count": 1, "pep_b_repeat_count": 1,
            "path": str(self.model_path), "pdb_id": "DEMO",
            "pdb_method": "X-RAY DIFFRACTION", "pdb_resolution": 2.0,
            "pdb_pos_a": 3, "pdb_pos_b": 9, "pLDDT_a": "-", "pLDDT_b": "-",
            "is_interfaced": True, "eucl_dist": 6.0, "topo_dist": 20.0,
        }
        rows = pd.DataFrame([
            row,
            {**row, "source_record_id": "source_2", "topo_dist": 43.761},
        ])
        self.structural = self.root / "example.sqcs_structdi.csv"
        self.ops = self.root / "example.sqcs_ops.csv"
        rows.to_csv(self.structural)
        pd.DataFrame({
            "homo_adjacency": [0.0, 0.0], "homo_int_overl": [0.0, 0.0],
            "homo_pep_overl": [False, False],
        }).to_csv(self.ops)

    def run_m4(self, extra_args=()):
        main = importlib.import_module("claudio.module04.src.main")
        with patch.object(
            main, "retrieve_oligomeric_states",
            side_effect=lambda frame, verbose: frame.assign(swiss_model_homology=""),
        ), patch.object(main, "create_plots"):
            result = CliRunner().invoke(main.main, [
                "-i", str(self.structural), "-i2", str(self.ops),
                "-o", str(self.output), "-s", "False", "-v", "0",
                *extra_args,
            ])
        self.assertEqual(result.exit_code, 0, result.output + repr(result.exception))
        return result

    def test_m4_writes_a_browser_view_and_keeps_the_csv_classifications(self):
        result = self.run_m4()
        pages = list((self.output / "visualization").glob("*/index.html"))
        self.assertEqual(len(pages), 1)
        self.assertEqual(len(list(pages[0].parent.glob("*.mvsx"))), 1)
        self.assertIn("python -m http.server", result.output)
        self.assertIn("http://localhost:8000", result.output)
        self.assertFalse(self.model_path.with_suffix(".pml").exists())
        final = pd.read_csv(self.output / "example_final.csv", index_col=0)
        self.assertEqual(final["original_XL_type"].tolist(), ["intra", "intra"])
        self.assertEqual(final["XL_type"].tolist(), ["intra", "inter"])
        html = pages[0].read_text(encoding="utf-8")
        for source in final["source_record_id"]:
            self.assertIn(source, html)
        self.assertIn("distance above range", html)

    def test_rerunning_m4_keeps_the_previous_visualization(self):
        self.run_m4()
        first_pages = list((self.output / "visualization").glob("*/index.html"))
        self.assertEqual(len(first_pages), 1)
        first_files = {path.name: path.read_bytes() for path in first_pages[0].parent.iterdir()}
        self.run_m4()
        self.assertEqual(len(list((self.output / "visualization").glob("*/index.html"))), 2)
        for name, content in first_files.items():
            self.assertEqual((first_pages[0].parent / name).read_bytes(), content)

    def test_m4_accepts_the_same_atom_configuration_as_m2(self):
        self.run_m4(["--xl-residues", "K:CA:"])
        packages = list((self.output / "visualization").glob("*/*.mvsx"))
        self.assertEqual(len(packages), 1)
        with zipfile.ZipFile(packages[0]) as archive:
            state = json.loads(archive.read("index.mvsj"))

        def walk(node):
            yield node
            for child in node.get("children", []):
                yield from walk(child)

        links = [node["params"] for node in walk(state["root"])
                 if node.get("params", {}).get("kind") == "distance_measurement"]
        self.assertEqual(len(links), 2)
        for link in links:
            self.assertEqual(link["start"], [0.0, 0.0, 1.0])
            self.assertEqual(link["end"], [6.0, 0.0, 1.0])

    def test_full_pipeline_forwards_its_atom_configuration_to_m4(self):
        pipeline = importlib.import_module("claudio.claudio_m")
        self.output.mkdir()
        source = self.root / "example.csv"
        source.write_text("input\n", encoding="utf-8")
        for suffix in [".sqcs", ".sqcs_ops.csv", ".sqcs_structdi.csv"]:
            (self.output / ("example" + suffix)).write_text("input\n", encoding="utf-8")

        with ExitStack() as stack:
            stack.enter_context(patch.object(pipeline, "_pkg_version", return_value="2.2.1"))
            for name in ["db_updater", "run_claudio_lists", "run_claudio_ops", "run_claudio_structdi"]:
                stack.enter_context(patch.object(pipeline, name))
            run_m4 = stack.enter_context(patch.object(pipeline, "run_claudio_xl"))
            result = CliRunner().invoke(pipeline.main, [
                "-i", str(source), "-o", str(self.output), "-x", "K:CA:", "-v", "0",
            ])
        self.assertEqual(result.exit_code, 0, result.output + repr(result.exception))
        run_m4.assert_called_once()
        arguments = run_m4.call_args.args[0]
        self.assertIn("-x", arguments)
        self.assertEqual(arguments[arguments.index("-x") + 1], "K:CA:")
