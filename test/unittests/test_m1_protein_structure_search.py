"""M1 can prepare AF inputs without searching structures for its protein list."""

import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from click.testing import CliRunner

from claudio.module01.src.algorithm.create_unique_list import (
    create_list_of_unique_proteins,
)


m1 = importlib.import_module("claudio.module01.src.main")
unique_list = "claudio.module01.src.algorithm.create_unique_list"


class TestM1ProteinStructureSearch(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P2",
            "seq_a": "MAKT", "seq_b": "MAAKT",
        }])
        self.metadata = [
            ["Entry\tProtein names", "P1\tProtein one"],
            ["Entry\tProtein names", "P2\tProtein two"],
        ]
        self.input = self.root / "input.csv"
        pd.DataFrame([{
            "entry1": "P1", "entry2": "P2",
            "peptide1": "AKT", "peptide2": "AAKT",
            "position1": 1, "position2": 4,
            "k_pos1": 2, "k_pos2": 3, "experiment": "condition_A",
        }]).to_csv(self.input, index=False)

    def create_list(self, **options):
        return create_list_of_unique_proteins(
            self.data, str(self.root) + "/", "blastp", None,
            str(self.root / "missing-db"), None,
            str(self.root / "missing-hhdb"), 0, **options,
        )

    def test_unique_list_skips_structure_search_but_keeps_metadata(self):
        with patch(
            unique_list + ".search_uniprot_metadata", return_value=self.metadata,
        ) as metadata, patch(unique_list + ".search_pdb_entries") as search:
            result = self.create_list(search_structures=False)

        metadata.assert_called_once_with(["P1", "P2"], 0)
        search.assert_not_called()
        self.assertEqual(result["Entry"].tolist(), ["P1", "P2"])
        self.assertEqual(result["Sequence"].tolist(), ["MAKT", "MAAKT"])
        self.assertEqual(result["Count"].tolist(), [1, 1])
        self.assertTrue(result["PDB"].isna().all())

    def test_unique_list_searches_structures_by_default(self):
        with patch(
            unique_list + ".search_uniprot_metadata", return_value=self.metadata,
        ), patch(
            unique_list + ".search_pdb_entries", return_value=["1AAA_A", "2BBB_B"],
        ) as search:
            result = self.create_list()

        search.assert_called_once()
        self.assertEqual(result["PDB"].tolist(), ["1AAA_A", "2BBB_B"])

    def invoke_m1(self, extra=()):
        return CliRunner().invoke(m1.main, [
            "-i", str(self.input), "-o", str(self.root / "out"),
            "-bldb", str(self.root / "missing-db"),
            "-x", "K", "-v", "0", "--skip-protein-structure-search", *extra,
        ])

    def test_preprocessing_still_checks_positions_without_a_structure_database(self):
        def sequences(data, *args):
            return data.assign(seq_a="MAKT", seq_b="MAAKT")

        with patch.object(
            m1, "do_uniprot_search", side_effect=sequences,
        ) as sequence_search, patch(
            unique_list + ".search_uniprot_metadata", return_value=self.metadata,
        ), patch(unique_list + ".search_pdb_entries") as structure_search:
            result = self.invoke_m1()

        self.assertEqual(result.exit_code, 0,
                         result.output + repr(result.exception))
        sequence_search.assert_called_once()
        structure_search.assert_not_called()
        saved = pd.read_csv(self.root / "out" / "input.sqcs", index_col=0)
        self.assertEqual(saved.iloc[0]["experiment"], "condition_A")
        self.assertEqual(saved.iloc[0]["pos_a"], 3)
        self.assertNotIn("position_status_a", saved)
        self.assertNotIn("source_record_id", saved)
        report = pd.read_csv(self.root / "out" / "input_record_tracking.csv", index_col=0)
        row = report.iloc[0]
        self.assertEqual(row["source_record_id"], "record_000001")
        self.assertEqual(row["original_pos_a"], 1)
        self.assertEqual(row["pos_a"], 3)
        self.assertEqual(row["position_status_a"], "corrected")
        self.assertEqual(row["position_status_b"], "valid")
        self.assertFalse(pd.isna(row["candidate_id"]))
        proteins = pd.read_csv(
            self.root / "out" / "input_unique_proteins.csv", index_col=0,
        )
        self.assertEqual(proteins["Entry"].tolist(), ["P1", "P2"])
        self.assertTrue(proteins["PDB"].isna().all())

    def test_default_preprocessing_still_requires_structure_database(self):
        with patch.object(m1, "do_uniprot_search") as sequences:
            result = CliRunner().invoke(m1.main, [
                "-i", str(self.input), "-o", str(self.root / "out"),
                "-bldb", str(self.root / "missing-db"), "-v", "0",
            ])
        self.assertIsInstance(result.exception, FileNotFoundError)
        self.assertIn("pdbaa.phr", str(result.exception))
        sequences.assert_not_called()

    def test_skip_does_not_bypass_projection_or_sequence_cache_checks(self):
        cases = [
            (["-p", "bad_projection"], "projections"),
            (["-s", "False"], "temporary save file"),
        ]
        for options, message in cases:
            with self.subTest(options=options):
                with patch.object(m1, "do_uniprot_search") as sequences, patch(
                    unique_list + ".search_pdb_entries",
                ) as structures:
                    result = self.invoke_m1(options)
                self.assertNotEqual(result.exit_code, 0)
                self.assertIn(message, str(result.exception))
                sequences.assert_not_called()
                structures.assert_not_called()


if __name__ == "__main__":
    unittest.main()
