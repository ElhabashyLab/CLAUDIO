import io
import json
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import pandas as pd
from Bio.PDB import Atom, Chain, MMCIFIO, Model, PDBIO, PDBParser, Residue, Structure

from claudio.module04.src.io.create_molstar_view import export_molstar_visualization


def walk_nodes(node):
    yield node
    for child in node.get("children", []):
        yield from walk_nodes(child)


@unittest.skipIf(sys.version_info < (3, 10), "Mol* export requires Python 3.10 or newer")
class TestM4MolstarExport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.structure_path = self.root / "small_model.pdb"

        structure = Structure.Structure("small_model")
        model = Model.Model(0)
        structure.add(model)
        serial = 1
        for chain_id, positions in [
            ("A", [(10, (0.0, 0.0, 0.0)), (11, (0.0, 4.0, 0.0))]),
            ("B", [(20, (3.0, 0.0, 0.0))]),
        ]:
            chain = Chain.Chain(chain_id)
            model.add(chain)
            for number, coordinates in positions:
                residue = Residue.Residue((" ", number, " "), "LYS", " ")
                chain.add(residue)
                for atom_name, offset in [("CA", 1.0), ("CB", 0.0)]:
                    xyz = np.array(coordinates) + np.array([0.0, 0.0, offset])
                    residue.add(Atom.Atom(
                        atom_name, xyz, 80.0, 1.0, " ",
                        f" {atom_name:<3}", serial, element="C",
                    ))
                    serial += 1

        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(self.structure_path))

        self.data = pd.DataFrame([
            {
                "source_record_id": "source_1", "pdb_id": "DEMO",
                "path": str(self.structure_path),
                "chain_a": "A", "chain_b": "B",
                "pos_a": 100, "pos_b": 200,
                "pdb_pos_a": 10, "pdb_pos_b": 20,
                "eucl_dist": 3.0, "topo_dist": 7.25,
                "original_XL_type": "inter", "XL_type": "inter",
                "XL_confirmed": True, "evidence": "",
            },
            {
                "source_record_id": "source_2", "pdb_id": "DEMO",
                "path": str(self.structure_path),
                "chain_a": "A", "chain_b": "A",
                "pos_a": 100, "pos_b": 101,
                "pdb_pos_a": 10, "pdb_pos_b": 11,
                "eucl_dist": 4.0, "topo_dist": 43.761,
                "original_XL_type": "intra", "XL_type": "inter",
                "XL_confirmed": False, "evidence": "distance above range",
            },
        ])

    def read_scene(self, output_dir):
        packages = list(output_dir.glob("*.mvsx"))
        self.assertEqual(len(packages), 1)
        with zipfile.ZipFile(packages[0]) as archive:
            scene = json.loads(archive.read("index.mvsj"))
            nodes = list(walk_nodes(scene["root"]))
            downloads = [node for node in nodes if node["kind"] == "download"]
            self.assertEqual(len(downloads), 1)
            structure_name = downloads[0]["params"]["url"]
            self.assertIn(structure_name, archive.namelist())
            self.assertEqual(
                archive.read(structure_name), self.structure_path.read_bytes()
            )
        measurements = [
            node["params"] for node in nodes
            if node.get("params", {}).get("kind") == "distance_measurement"
        ]
        return packages[0], scene, measurements

    def test_exports_two_links_and_browser_instructions(self):
        original = self.data.copy(deep=True)
        output_dir = self.root / "visualization"
        console = io.StringIO()
        with redirect_stdout(console):
            export_molstar_visualization(self.data, output_dir, atom_name="CB")

        package, scene, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 2)
        endpoints = {
            (tuple(item["start"]), tuple(item["end"]))
            for item in measurements
        }
        self.assertEqual(endpoints, {
            ((0.0, 0.0, 0.0), (3.0, 0.0, 0.0)),
            ((0.0, 0.0, 0.0), (0.0, 4.0, 0.0)),
        })
        scene_text = json.dumps(scene)
        for text in ["source_1", "source_2", "original_XL_type", "XL_type",
                     "distance above range", "7.25", "43.761"]:
            self.assertIn(text, scene_text)

        html = (output_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn(package.name, html)
        self.assertNotIn(str(self.structure_path), html)
        self.assertIn("https://molstar.org/viewer/", console.getvalue())
        self.assertIn("Open Files", console.getvalue())
        self.assertIn(".mvsx", console.getvalue())
        self.assertNotIn("python -m http.server", console.getvalue())
        self.assertIn('href="https://molstar.org/viewer/"', html)
        self.assertIn("Open Files", html)
        self.assertIn("MVSX", html)
        pd.testing.assert_frame_equal(self.data, original)

    def test_duplicate_endpoint_pairs_share_a_label_without_losing_sources(self):
        for reverse in (False, True):
            with self.subTest(reverse=reverse):
                first = self.data.iloc[:1].copy()
                duplicate = first.copy()
                duplicate["source_record_id"] = "duplicate_source"
                if reverse:
                    for column in ("chain", "pdb_pos", "pos"):
                        duplicate[f"{column}_a"], duplicate[f"{column}_b"] = (
                            first[f"{column}_b"], first[f"{column}_a"]
                        )
                data = pd.concat([first, duplicate], ignore_index=True)
                original = data.copy(deep=True)
                output_dir = self.root / f"duplicate_pair_{reverse}"
                with redirect_stdout(io.StringIO()):
                    export_molstar_visualization(data, output_dir)

                _, scene, measurements = self.read_scene(output_dir)
                self.assertEqual(len(measurements), 1)
                tubes = [
                    node["params"] for node in walk_nodes(scene["root"])
                    if node.get("params", {}).get("kind") == "tube"
                ]
                self.assertEqual(len(tubes), 1)
                expected_start = [3.0, 0.0, 0.0] if reverse else [0.0, 0.0, 0.0]
                self.assertEqual(tubes[0]["start"], expected_start)
                html = (output_dir / "index.html").read_text(encoding="utf-8")
                for source in ("source_1", "duplicate_source"):
                    self.assertIn(source, html)
                    self.assertIn(source, json.dumps(scene))
                pd.testing.assert_frame_equal(data, original)

    def test_distinct_residues_at_identical_coordinates_keep_separate_labels(self):
        structure = PDBParser(QUIET=True).get_structure("model", str(self.structure_path))
        residue = structure[0]["A"][10].copy()
        residue.id = (" ", 12, " ")
        structure[0]["A"].add(residue)
        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(self.structure_path))
        first = self.data.iloc[:1].copy()
        other = first.copy()
        other["source_record_id"] = "other_residue_source"
        other["pdb_pos_a"] = 12
        data = pd.concat([first, other], ignore_index=True)
        output_dir = self.root / "distinct_residues"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(data, output_dir)
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 2)

    def test_no_structure_keeps_the_table_without_suggesting_a_missing_package(self):
        data = self.data.copy()
        data["path"] = "-"
        output_dir = self.root / "no_structure"
        console = io.StringIO()
        with redirect_stdout(console):
            export_molstar_visualization(data, output_dir)
        self.assertEqual(list(output_dir.glob("*.mvsx")), [])
        self.assertIn("No usable structure", console.getvalue())
        self.assertNotIn("Open Files", console.getvalue())
        html = (output_dir / "index.html").read_text(encoding="utf-8")
        for source in ("source_1", "source_2"):
            self.assertIn(source, html)

    def test_uses_the_requested_atom_instead_of_always_using_cb(self):
        output_dir = self.root / "ca_visualization"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(
                self.data.iloc[:1].copy(), output_dir, atom_name="CA"
            )
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["start"], [0.0, 0.0, 1.0])
        self.assertEqual(measurements[0]["end"], [3.0, 0.0, 1.0])

    def test_selects_the_insertion_code_without_using_the_plain_residue(self):
        structure = PDBParser(QUIET=True).get_structure("model", str(self.structure_path))
        inserted = Residue.Residue((" ", 10, "A"), "LYS", " ")
        inserted.add(Atom.Atom(
            "CB", np.array([9.0, 0.0, 0.0]), 80.0, 1.0,
            " ", " CB ", 99, element="C",
        ))
        structure[0]["A"].add(inserted)
        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(self.structure_path))
        data = self.data.iloc[:1].copy()
        data["pdb_icode_a"] = "A"

        output_dir = self.root / "inserted_residue"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(data, output_dir)
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["start"], [9.0, 0.0, 0.0])

    def test_keeps_complete_author_chain_ids_from_mmcif(self):
        structure = PDBParser(QUIET=True).get_structure("model", str(self.structure_path))
        structure[0]["A"].id = "NA"
        structure[0]["B"].id = "01"
        self.structure_path = self.root / "multi_character_chains.cif"
        writer = MMCIFIO()
        writer.set_structure(structure)
        writer.save(str(self.structure_path))
        data = self.data.iloc[:1].copy()
        data["path"] = str(self.structure_path)
        data["chain_a"] = "NA"
        data["chain_b"] = "01"

        output_dir = self.root / "mmcif_view"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(data, output_dir)
        _, scene, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["end"], [3.0, 0.0, 0.0])
        chain_ids = {
            node["params"]["selector"]["auth_asym_id"]
            for node in walk_nodes(scene["root"])
            if isinstance(node.get("params", {}).get("selector"), dict)
        }
        self.assertEqual(chain_ids, {"NA", "01"})

    def test_missing_atom_does_not_hide_the_other_link(self):
        structure = PDBParser(QUIET=True).get_structure("model", str(self.structure_path))
        structure[0]["B"][20].detach_child("CB")
        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(self.structure_path))

        output_dir = self.root / "missing_atom"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(self.data, output_dir)
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["end"], [0.0, 4.0, 0.0])
        html = (output_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("source_1", html)
        self.assertIn("atom CB not found", html)
        self.assertIn("source_2", html)

    def test_separates_structure_files_with_the_same_pdb_id(self):
        structure = PDBParser(QUIET=True).get_structure("model", str(self.structure_path))
        structure[0]["A"][11]["CB"].set_coord(np.array([0.0, 8.0, 0.0]))
        second_path = self.root / "another_version.pdb"
        writer = PDBIO()
        writer.set_structure(structure)
        writer.save(str(second_path))
        data = self.data.copy()
        data.loc[1, "path"] = str(second_path)

        output_dir = self.root / "two_models"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(data, output_dir)
        packages = list(output_dir.glob("*.mvsx"))
        self.assertEqual(len(packages), 2)
        ends = set()
        for package in packages:
            with zipfile.ZipFile(package) as archive:
                scene = json.loads(archive.read("index.mvsj"))
            measurements = [
                node["params"] for node in walk_nodes(scene["root"])
                if node.get("params", {}).get("kind") == "distance_measurement"
            ]
            self.assertEqual(len(measurements), 1)
            ends.add(tuple(measurements[0]["end"]))
        self.assertEqual(ends, {(3.0, 0.0, 0.0), (0.0, 8.0, 0.0)})

    def test_does_not_draw_an_endpoint_marked_not_evaluable(self):
        data = self.data.copy()
        data["mapping_status_a"] = "mapped"
        data["mapping_status_b"] = "mapped"
        data.loc[0, "mapping_status_a"] = "not_evaluable"

        output_dir = self.root / "unresolved_endpoint"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(data, output_dir)
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["end"], [0.0, 4.0, 0.0])
        html = (output_dir / "index.html").read_text(encoding="utf-8")
        self.assertIn("source_1", html)
        self.assertIn("mapping status is not_evaluable", html)

    def test_uses_atoms_from_the_existing_cross_link_configuration(self):
        output_dir = self.root / "configured_atoms"
        with redirect_stdout(io.StringIO()):
            export_molstar_visualization(
                self.data.iloc[:1].copy(), output_dir,
                xl_residues="K:CA:,M:N:1",
            )
        _, _, measurements = self.read_scene(output_dir)
        self.assertEqual(len(measurements), 1)
        self.assertEqual(measurements[0]["start"], [0.0, 0.0, 1.0])
        self.assertEqual(measurements[0]["end"], [3.0, 0.0, 1.0])
