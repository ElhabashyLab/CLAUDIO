"""Identical atoms are not distinct cross-link endpoints."""
import importlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import numpy as np
import pandas as pd
from Bio.PDB import Atom, Chain, MMCIFIO, Model, Residue, Structure

algorithm = importlib.import_module(
    "claudio.module02.src_distance_reevaluation.algorithm.af_complex_distances"
)


class TestAFComplexIdenticalEndpoints(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.model_id = "AF-0000000000000001"
        self.path = self.root / "model.cif"
        self.metadata_path = self.root / "metadata.json"
        self.write_model(chain_offset=10.0)
        self.row = {
            "inventory_record_id": "source:sheet:2",
            "source_record_id": "record_000001",
            "candidate_id": "candidate_000001",
            "source_crosslink_type": "Homodimer",
            "biological_replicate": "Replicate 1",
            "organelle_fraction": "Nucleus",
            "unip_id_a": "P12345", "unip_id_b": "P12345",
            "seq_a": "MAK", "seq_b": "MAK",
            "pep_a": "MAK", "pep_b": "MAK",
            "res_pos_a": 3, "res_pos_b": 3,
            "original_pos_a": 3, "original_pos_b": 3,
            "pos_a": 3, "pos_b": 3,
            "position_status_a": "valid", "position_status_b": "valid",
            "chain_a": "A", "chain_b": "A",
            "af_match_status": "matched",
            "af_model_id": self.model_id, "af_model_version": 1,
            "af_metadata_path": str(self.metadata_path), "path": str(self.path),
        }

    def write_model(self, chain_offset):
        structure = Structure.Structure("test")
        model = Model.Model(0)
        structure.add(model)
        for chain_id, offset in (("A", 0.0), ("B", chain_offset)):
            chain = Chain.Chain(chain_id)
            model.add(chain)
            for number, name in enumerate(("MET", "ALA", "LYS"), 1):
                residue = Residue.Residue((" ", number, " "), name, " ")
                atom = Atom.Atom(
                    "CA", np.array([float(number), offset, 0.0]),
                    90.0, 1.0, " ", " CA ", number, element="C",
                )
                residue.add(atom)
                chain.add(residue)
        writer = MMCIFIO()
        writer.set_structure(structure)
        writer.save(str(self.path))
        self.metadata_path.write_text(json.dumps([{
            "modelEntityId": self.model_id, "latestVersion": 1,
            "isComplex": True, "uniprotAccession": "P12345",
            "chainId": chain_id, "sequence": "MAK",
        } for chain_id in ("A", "B")]))

    @staticmethod
    def distance_backend(data, *args):
        result = data.copy()
        values = [float(np.linalg.norm(
            np.array(row.mapping_coord_a) - np.array(row.mapping_coord_b)
        )) for row in result.itertuples()]
        result["eucl_dist_tplk"] = values
        result["topo_dist_tplk"] = values
        return result

    def calculate(self, rows, **options):
        return algorithm.calculate_complex_site_dists(
            pd.DataFrame(rows), str(self.root / "work") + "/",
            "K:CA:0", 70, None, 0, **options,
        )

    def test_same_atom_is_retained_without_a_distance(self):
        with patch.object(
            algorithm, "calculate_site_dists", side_effect=self.distance_backend,
        ) as backend:
            result = self.calculate([self.row])
        row = result.iloc[0]
        self.assertEqual(row["distance_status"], "not_evaluable")
        self.assertEqual(row["distance_reason"], "identical_atom_endpoints")
        self.assertEqual(row["mapping_status_a"], "mapped")
        self.assertEqual(row["mapping_status_b"], "mapped")
        for column in ("eucl_dist_tplk", "topo_dist_tplk",
                       "eucl_dist_lower_bound", "topo_dist_lower_bound"):
            self.assertTrue(pd.isna(row[column]), column)
        for column in ("inventory_record_id", "source_record_id", "candidate_id",
                       "source_crosslink_type", "biological_replicate",
                       "organelle_fraction", "original_pos_a", "original_pos_b"):
            self.assertEqual(row[column], self.row[column])
        backend.assert_not_called()

    def test_cross_chain_options_survive_when_same_chain_options_are_rejected(self):
        rows = [{**self.row, "chain_a": a, "chain_b": b}
                for a, b in (("A", "A"), ("A", "B"), ("B", "A"), ("B", "B"))]
        with patch.object(
            algorithm, "calculate_site_dists", side_effect=self.distance_backend,
        ) as backend:
            result = self.calculate(rows)
        self.assertEqual(len(result), 4)
        self.assertEqual(result["distance_status"].tolist(),
                         ["not_evaluable", "computed", "computed", "not_evaluable"])
        self.assertEqual(result["source_record_id"].nunique(), 1)
        selected = backend.call_args.args[0]
        self.assertEqual(list(zip(selected.chain_a, selected.chain_b)),
                         [("A", "B"), ("B", "A")])
        self.assertEqual(result.loc[1, "eucl_dist_tplk"], 10.0)
        self.assertEqual(result.loc[2, "eucl_dist_tplk"], 10.0)

    def test_equal_coordinates_do_not_make_different_chain_atoms_identical(self):
        self.write_model(chain_offset=0.0)
        with patch.object(
            algorithm, "calculate_site_dists", side_effect=self.distance_backend,
        ) as backend:
            result = self.calculate([{**self.row, "chain_b": "B"}])
        backend.assert_called_once()
        self.assertEqual(result.iloc[0]["distance_status"], "computed")
        self.assertEqual(result.iloc[0]["eucl_dist_tplk"], 0.0)





if __name__ == "__main__":
    unittest.main()
