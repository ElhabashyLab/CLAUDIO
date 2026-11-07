"""Tests for connecting AFDB discovery to complex retrieval."""

import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch
from requests import Response
import pandas as pd

from claudio.module02.src_structure_search.algorithm.af_complex_search import (
    retrieve_discovered_complexes,
)


class TestRetrieveDiscoveredComplexes(unittest.TestCase):
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_retrieves_discovered_model_for_input_record(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "source_record_id": "record_000001",
        }], index=[7])

        model_id = "AF-0000000208747029"
        mock_discover.return_value = [{
            "modelEntityId": model_id,
            "latestVersion": 1,
            "isComplex": True,
            "uniprotAccession": ["A0A0P0Y832", "P0C2Z6"],
        }]

        expected = data.assign(
            af_model_id=model_id,
            chain_a="A",
            chain_b="B",
            af_match_status="matched",
        )
        mock_retrieve.return_value = expected.copy()

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

            mock_discover.assert_called_once_with(
                "A0A0P0Y832", "P0C2Z6"
            )
            mock_retrieve.assert_called_once()

            args = mock_retrieve.call_args.args
            pd.testing.assert_frame_equal(args[0], data)
            self.assertEqual(args[1], model_id)
            self.assertEqual(args[2], output_dir)

        pd.testing.assert_frame_equal(result, expected)
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_preserves_record_when_no_candidate_exists(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([{
            "unip_id_a": "A0A0P0Y832",
            "unip_id_b": "P0C2Z6",
            "source_record_id": "record_000001",
            "pos_a": 10,
            "pos_b": 20,
            "chain_a": "X",
            "chain_b": "Y",
            "path": "old_structure.cif",
            "af_model_id": "old_model",
            "af_model_version": 1,
            "af_metadata_path": "old_metadata.json",
        }], index=[7])
        original = data.copy(deep=True)
        mock_discover.return_value = []

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

        mock_retrieve.assert_not_called()
        self.assertEqual(result.index.tolist(), [7])
        self.assertEqual(len(result), 1)

        row = result.iloc[0]
        self.assertEqual(row["source_record_id"], "record_000001")
        self.assertEqual(row["pos_a"], 10)
        self.assertEqual(row["pos_b"], 20)
        self.assertEqual(row["af_match_status"], "no_candidate_model")
        self.assertEqual(row["chain_a"], "-")
        self.assertEqual(row["chain_b"], "-")
        self.assertEqual(row["path"], "-")

        for column in (
            "af_model_id",
            "af_model_version",
            "af_metadata_path",
        ):
            self.assertTrue(pd.isna(row[column]), column)

        pd.testing.assert_frame_equal(data, original)
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_retrieves_all_candidate_models(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([{
            "unip_id_a": "P1",
            "unip_id_b": "P2",
            "source_record_id": "record_000001",
            "pos_a": 10,
            "pos_b": 20,
        }], index=[7])

        model_ids = ["AF-test-model-1", "AF-test-model-2"]
        mock_discover.return_value = [
            {
                "modelEntityId": model_id,
                "latestVersion": 1,
                "isComplex": True,
                "uniprotAccession": ["P1", "P2"],
            }
            for model_id in model_ids
        ]

        mock_retrieve.side_effect = [
            data.assign(
                af_model_id=model_id,
                chain_a="A",
                chain_b="B",
                af_match_status="matched",
            )
            for model_id in model_ids
        ]

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

            self.assertEqual(mock_retrieve.call_count, 2)
            self.assertEqual(
                [
                    call.args[1]
                    for call in mock_retrieve.call_args_list
                ],
                model_ids,
            )
            for call in mock_retrieve.call_args_list:
                pd.testing.assert_frame_equal(call.args[0], data)
                self.assertEqual(call.args[2], output_dir)

        self.assertEqual(len(result), 2)
        self.assertEqual(set(result["af_model_id"]), set(model_ids))
        self.assertEqual(
            result["source_record_id"].tolist(),
            ["record_000001", "record_000001"],
        )
        self.assertTrue(result["pos_a"].eq(10).all())
        self.assertTrue(result["pos_b"].eq(20).all())
        self.assertTrue(
            result.index.is_unique,
            "Candidates from different models need unique indices",
        )
        self.assertEqual(result.index[0], 7)
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_retrieves_models_for_different_protein_pairs(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([
            {
                "unip_id_a": "P1",
                "unip_id_b": "P2",
                "source_record_id": "record_000001",
            },
            {
                "unip_id_a": "P3",
                "unip_id_b": "P4",
                "source_record_id": "record_000002",
            },
        ], index=[7, 12])

        mock_discover.side_effect = [
            [{"modelEntityId": "AF-test-ab", "latestVersion": 1}],
            [{"modelEntityId": "AF-test-cd", "latestVersion": 1}],
        ]
        mock_retrieve.side_effect = [
            data.iloc[[0]].assign(af_model_id="AF-test-ab"),
            data.iloc[[1]].assign(af_model_id="AF-test-cd"),
        ]

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

            self.assertEqual(mock_discover.call_count, 2)
            self.assertEqual(
                [
                    call.args
                    for call in mock_discover.call_args_list
                ],
                [("P1", "P2"), ("P3", "P4")],
            )

            self.assertEqual(mock_retrieve.call_count, 2)
            first_call, second_call = mock_retrieve.call_args_list

            pd.testing.assert_frame_equal(
                first_call.args[0], data.iloc[[0]]
            )
            pd.testing.assert_frame_equal(
                second_call.args[0], data.iloc[[1]]
            )
            self.assertEqual(first_call.args[1], "AF-test-ab")
            self.assertEqual(second_call.args[1], "AF-test-cd")

        self.assertEqual(len(result), 2)
        self.assertEqual(result.index.tolist(), [7, 12])
        self.assertEqual(
            result.set_index("source_record_id")["af_model_id"].to_dict(),
            {
                "record_000001": "AF-test-ab",
                "record_000002": "AF-test-cd",
            },
        )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_reuses_shared_model_and_groups_reversed_pairs(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([
            {
                "unip_id_a": "P1",
                "unip_id_b": "P2",
                "source_record_id": "record_000001",
            },
            {
                "unip_id_a": "P2",
                "unip_id_b": "P1",
                "source_record_id": "record_000002",
            },
            {
                "unip_id_a": "P1",
                "unip_id_b": "P3",
                "source_record_id": "record_000003",
            },
        ], index=[7, 12, 20])

        model_id = "AF-test-abc"
        mock_discover.return_value = [{
            "modelEntityId": model_id,
            "latestVersion": 1,
        }]
        expected = data.assign(
            af_model_id=model_id,
            af_match_status="matched",
        )
        mock_retrieve.return_value = expected.copy()

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

            self.assertEqual(
                [
                    call.args
                    for call in mock_discover.call_args_list
                ],
                [("P1", "P2"), ("P1", "P3")],
            )

            mock_retrieve.assert_called_once()
            args = mock_retrieve.call_args.args
            pd.testing.assert_frame_equal(args[0], data)
            self.assertEqual(args[1], model_id)
            self.assertEqual(args[2], output_dir)

        pd.testing.assert_frame_equal(result, expected)
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.discover_complex_candidates"
    )
    def test_preserves_unmatched_records_in_mixed_input(
        self, mock_discover, mock_retrieve
    ):
        data = pd.DataFrame([
            {
                "unip_id_a": "P1",
                "unip_id_b": "P2",
                "source_record_id": "record_000001",
            },
            {
                "unip_id_a": "P3",
                "unip_id_b": "P4",
                "source_record_id": "record_000002",
            },
        ], index=[7, 12])
        data["chain_a"] = "X"
        data["chain_b"] = "Y"
        data["path"] = "old_structure.cif"

        mock_discover.side_effect = [
            [{"modelEntityId": "AF-test-ab", "latestVersion": 1}],
            [],
        ]
        mock_retrieve.return_value = data.iloc[[0]].assign(
            af_model_id="AF-test-ab",
            af_match_status="matched",
            chain_a="A",
            chain_b="B",
            path="new_structure.cif",
        )

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

        mock_retrieve.assert_called_once()
        pd.testing.assert_frame_equal(
            mock_retrieve.call_args.args[0],
            data.iloc[[0]],
        )

        self.assertEqual(len(result), 2)
        self.assertTrue(result.index.is_unique)

        by_source = result.set_index("source_record_id")
        matched = by_source.loc["record_000001"]
        unmatched = by_source.loc["record_000002"]

        self.assertEqual(matched["af_match_status"], "matched")
        self.assertEqual(matched["af_model_id"], "AF-test-ab")
        self.assertEqual(unmatched["af_match_status"], "no_candidate_model")
        self.assertEqual(unmatched["chain_a"], "-")
        self.assertEqual(unmatched["chain_b"], "-")
        self.assertEqual(unmatched["path"], "-")
        self.assertTrue(pd.isna(unmatched["af_model_id"]))
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.retrieve_af_complex"
    )
    @patch("claudio.utils.af_complex.requests.get")
    def test_continues_after_404_and_preserves_source_records(
        self, mock_get, mock_retrieve
    ):
        data = pd.DataFrame([
            {
                "unip_id_a": "P1", "unip_id_b": "P2",
                "source_record_id": "record_000001",
                "pos_a": 10, "pos_b": 20, "experiment": "condition_1",
            },
            {
                "unip_id_a": "P3", "unip_id_b": "P4",
                "source_record_id": "record_000002",
                "pos_a": 30, "pos_b": 40, "experiment": "condition_2",
            },
        ], index=[7, 12])
        original = data.copy(deep=True)

        missing = Response()
        missing.status_code = 404
        missing._content = b"{}"

        found = Response()
        found.status_code = 200
        found._content = (
            b'[{"modelEntityId":"AF-test-cd","latestVersion":1,'
            b'"isComplex":true,"uniprotAccession":["P3","P4"]}]'
        )
        mock_get.side_effect = [missing, found]
        mock_retrieve.return_value = data.iloc[[1]].assign(
            af_model_id="AF-test-cd",
            af_match_status="matched",
            chain_a="A", chain_b="B", path="new_structure.cif",
        )

        with TemporaryDirectory() as output_dir:
            result = retrieve_discovered_complexes(data, output_dir)

            mock_retrieve.assert_called_once()
            args = mock_retrieve.call_args.args
            pd.testing.assert_frame_equal(args[0], data.iloc[[1]])
            self.assertEqual(args[1:], ("AF-test-cd", output_dir))

        self.assertEqual(
            [call.args[0] for call in mock_get.call_args_list],
            [
                "https://alphafold.ebi.ac.uk/api/complex/P1",
                "https://alphafold.ebi.ac.uk/api/complex/P3",
            ],
        )
        self.assertEqual(len(result), 2)
        self.assertTrue(result.index.is_unique)
        pd.testing.assert_frame_equal(
            result.loc[data.index, data.columns], original
        )
        self.assertEqual(result.loc[7, "af_match_status"], "no_candidate_model")
        self.assertEqual(result.loc[7, "path"], "-")
        self.assertEqual(result.loc[7, "chain_a"], "-")
        self.assertEqual(result.loc[7, "chain_b"], "-")
        self.assertTrue(pd.isna(result.loc[7, "af_model_id"]))
        self.assertEqual(result.loc[12, "af_match_status"], "matched")
        self.assertEqual(result.loc[12, "af_model_id"], "AF-test-cd")
        pd.testing.assert_frame_equal(data, original)
if __name__ == "__main__":
    unittest.main()
