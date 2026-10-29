"""Tests for restoring structure-search results from cache."""

import unittest
from unittest.mock import patch
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module02.src_structure_search.algorithm.structure_search import (
    structure_search,
)
from claudio.module02.src_structure_search.io.read_temp import read_temp_file


class TestM2SearchCacheAlignment(unittest.TestCase):
    def test_restores_results_for_non_contiguous_input_indices(self):
        data = pd.DataFrame({
            "source_record_id": ["record_000002", "record_000003"],
            "unip_id_a": ["P1", "P3"],
            "unip_id_b": ["P2", "P4"],
            "seq_a": ["MAK", "MGK"],
            "seq_b": ["MKT", "MKS"],
        }, index=[1, 2])

        cached = pd.DataFrame({
            "pdb_id": ["1AAA", "2BBB"],
            "chain_a": ["A", "C"],
            "chain_b": ["B", "D"],
            "all_results": ["1AAA_A|_B", "2BBB_C|_D"],
        })
        for column in ("unip_id_a", "unip_id_b", "seq_a", "seq_b"):
            cached[column] = data[column].to_numpy()
        with TemporaryDirectory() as folder:
            path = Path(folder) / "search_cache.csv"
            cached.to_csv(path, index=False)
            result = read_temp_file(data.copy(), str(path))

        self.assertEqual(result.index.tolist(), [1, 2])
        self.assertEqual(
            result["source_record_id"].tolist(),
            ["record_000002", "record_000003"],
        )
        for column in cached.columns:
            with self.subTest(column=column):
                self.assertEqual(
                    result[column].tolist(),
                    cached[column].tolist(),
                    "Cached results must stay with their input records",
                )

    def test_rejects_cache_for_changed_input_identity_or_order(self):
        data = pd.DataFrame({
            "unip_id_a": ["P1", "P3"],
            "unip_id_b": ["P2", "P4"],
            "seq_a": ["MAK", "MGK"],
            "seq_b": ["MKT", "MKS"],
        }, index=[1, 2])
        cached = data.reset_index(drop=True).assign(
            pdb_id=["1AAA", "2BBB"],
            chain_a=["A", "C"],
            chain_b=["B", "D"],
            all_results=["1AAA_A|_B", "2BBB_C|_D"],
        )

        with TemporaryDirectory() as folder:
            path = Path(folder) / "search_cache.csv"
            cached.to_csv(path, index=False)

            for case in ("row_order", "protein_id", "sequence"):
                with self.subTest(case=case):
                    changed = data.copy(deep=True)
                    if case == "row_order":
                        changed = changed.iloc[::-1].copy()
                    elif case == "protein_id":
                        changed.loc[1, "unip_id_b"] = "P9"
                    else:
                        changed.loc[1, "seq_b"] = "MKA"

                    before = changed.copy(deep=True)
                    with self.assertRaisesRegex(
                        ValueError, "identity|order"
                    ):
                        read_temp_file(changed, str(path))

                    pd.testing.assert_frame_equal(changed, before)

    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "structure_search.perform_search"
    )
    def test_round_trip_preserves_results_and_source_fields(self, mock_search):
        data = pd.DataFrame({
            "source_record_id": ["record_000002", "record_000003"],
            "unip_id_a": ["P1", "P3"],
            "unip_id_b": ["P2", "P4"],
            "seq_a": ["MAK", "MGK"],
            "seq_b": ["MKT", "MKS"],
        }, index=[1, 2]).assign(
            pdb_id="-", chain_a="-", chain_b="-", all_results=""
        )

        hits = {
            "P1": ("1AAA", "A"),
            "P2": ("1AAA", "B"),
            "P3": ("2BBB", "C"),
            "P4": ("2BBB", "D"),
        }

        def fake_search(unip_id, sequence, *args):
            pdb_id, chain = hits[unip_id]
            return [f"{pdb_id}_{chain}"], pdb_id, chain, unip_id

        mock_search.side_effect = fake_search
        with TemporaryDirectory() as folder:
            path = Path(folder) / "search_cache.csv"
            searched = structure_search(
                data.copy(deep=True),
                search_tool="blastp",
                e_value=1e-5, query_id=90.0, coverage=50.0,
                tmp_filepath=str(path),
                blast_bin=None, blast_db="unused/",
                hhsearch_bin=None, hhsearch_db="unused/",
                verbose_level=0,
            )
            cached = pd.read_csv(path)
            for column in ("unip_id_a", "unip_id_b", "seq_a", "seq_b"):
                self.assertIn(column, cached.columns)
                self.assertEqual(
                    cached[column].tolist(), data[column].tolist()
                )

            restored = read_temp_file(data.copy(deep=True), str(path))

        self.assertEqual(mock_search.call_count, 4)
        pd.testing.assert_frame_equal(restored, searched)
        self.assertEqual(restored["pdb_id"].tolist(), ["1AAA", "2BBB"])
        self.assertEqual(restored["chain_a"].tolist(), ["A", "C"])
        self.assertEqual(restored["chain_b"].tolist(), ["B", "D"])

    def test_rejects_legacy_or_wrong_length_cache_before_modifying_input(self):
        data = pd.DataFrame({
            "unip_id_a": ["P1", "P3"],
            "unip_id_b": ["P2", "P4"],
            "seq_a": ["MAK", "MGK"],
            "seq_b": ["MKT", "MKS"],
        }, index=[1, 2])
        cached = data.reset_index(drop=True).assign(
            pdb_id="1AAA", chain_a="A", chain_b="B",
            all_results="1AAA_A|_B",
        )
        cases = [
            (cached.drop(columns=["seq_a"]), "identity"),
            (cached.iloc[:1], "row count"),
        ]

        with TemporaryDirectory() as folder:
            path = Path(folder) / "search_cache.csv"
            for cache_data, message in cases:
                with self.subTest(message=message):
                    cache_data.to_csv(path, index=False)
                    current = data.copy(deep=True)
                    with self.assertRaisesRegex(ValueError, message):
                        read_temp_file(current, str(path))
                    pd.testing.assert_frame_equal(current, data)


if __name__ == "__main__":
    unittest.main()
