"""Tests for discovering existing AFDB protein-complex models."""
from requests import HTTPError
import unittest
from unittest.mock import patch

from claudio.utils.af_complex import fetch_complex_candidates
from claudio.module02.src_structure_search.algorithm.af_complex_search import (
    filter_complex_candidates,
    discover_complex_candidates,
)

class TestFetchComplexCandidates(unittest.TestCase):
    @patch("claudio.utils.af_complex.requests.get")
    def test_fetches_complex_candidates_for_uniprot_accession(self, mock_get):
        candidates = [
            {
                "modelEntityId": "AF-0000000208747029",
                "latestVersion": 1,
                "isComplex": True,
                "uniprotAccession": ["A0A0P0Y832", "P0C2Z6"],
            },
            {
                "modelEntityId": "AF-0000000208747028",
                "latestVersion": 1,
                "isComplex": True,
                "uniprotAccession": ["A0A0P0Y832", "P0C522"],
            },
        ]
        response = mock_get.return_value
        response.json.return_value = candidates

        result = fetch_complex_candidates("A0A0P0Y832")

        mock_get.assert_called_once_with(
            "https://alphafold.ebi.ac.uk/api/complex/A0A0P0Y832",
            timeout=30,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, candidates)
    @patch("claudio.utils.af_complex.requests.get")
    def test_returns_empty_list_when_no_candidates_exist(self, mock_get):
        response = mock_get.return_value
        response.json.return_value = []

        result = fetch_complex_candidates("A0A0P0Y832")

        self.assertEqual(result, [])

    @patch("claudio.utils.af_complex.requests.get")
    def test_propagates_http_failure(self, mock_get):
        response = mock_get.return_value
        response.raise_for_status.side_effect = HTTPError(
            "503 Service Unavailable"
        )

        with self.assertRaises(HTTPError):
            fetch_complex_candidates("A0A0P0Y832")

        response.json.assert_not_called()
    @patch("claudio.utils.af_complex.requests.get")
    def test_returns_empty_list_when_complex_endpoint_returns_404(
        self, mock_get
    ):
        response = mock_get.return_value
        response.status_code = 404
        response.raise_for_status.side_effect = HTTPError(
            "404 Not Found", response=response
        )
        response.json.return_value = {}

        result = fetch_complex_candidates("Q8WZ42")

        self.assertEqual(result, [])
        mock_get.assert_called_once_with(
            "https://alphafold.ebi.ac.uk/api/complex/Q8WZ42",
            timeout=30,
        )
        response.json.assert_not_called()
class TestFilterComplexCandidates(unittest.TestCase):
    def test_keeps_only_models_containing_both_proteins(self):
        matching = {
            "modelEntityId": "AF-0000000208747029",
            "latestVersion": 1,
            "isComplex": True,
            "uniprotAccession": ["A0A0P0Y832", "P0C2Z6"],
        }
        other_partner = {
            "modelEntityId": "AF-0000000208747028",
            "latestVersion": 1,
            "isComplex": True,
            "uniprotAccession": ["A0A0P0Y832", "P0C522"],
        }

        result = filter_complex_candidates(
            [matching, other_partner],
            protein_a="A0A0P0Y832",
            protein_b="P0C2Z6",
        )

        self.assertEqual(result, [matching])
    def test_matches_reversed_protein_pair(self):
        candidate = {
            "modelEntityId": "AF-test-ab",
            "isComplex": True,
            "uniprotAccession": ["P1", "P2"],
        }

        result = filter_complex_candidates(
            [candidate], protein_a="P2", protein_b="P1"
        )

        self.assertEqual(result, [candidate])

    def test_keeps_all_matches_including_larger_complexes(self):
        dimer = {
            "modelEntityId": "AF-test-ab",
            "isComplex": True,
            "uniprotAccession": ["P1", "P2"],
        }
        larger_complex = {
            "modelEntityId": "AF-test-abc",
            "isComplex": True,
            "uniprotAccession": ["P1", "P2", "P3"],
        }

        result = filter_complex_candidates(
            [dimer, larger_complex],
            protein_a="P1",
            protein_b="P2",
        )

        self.assertEqual(result, [dimer, larger_complex])

    def test_returns_empty_list_when_no_model_contains_both(self):
        candidate = {
            "modelEntityId": "AF-test-ac",
            "isComplex": True,
            "uniprotAccession": ["P1", "P3"],
        }

        result = filter_complex_candidates(
            [candidate], protein_a="P1", protein_b="P2"
        )

        self.assertEqual(result, [])
class TestDiscoverComplexCandidates(unittest.TestCase):
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "af_complex_search.fetch_complex_candidates"
    )
    def test_discovers_candidates_for_input_protein_pair(self, mock_fetch):
        matching = {
            "modelEntityId": "AF-0000000208747029",
            "latestVersion": 1,
            "isComplex": True,
            "uniprotAccession": ["A0A0P0Y832", "P0C2Z6"],
        }
        other_partner = {
            "modelEntityId": "AF-0000000208747028",
            "latestVersion": 1,
            "isComplex": True,
            "uniprotAccession": ["A0A0P0Y832", "P0C522"],
        }
        mock_fetch.return_value = [matching, other_partner]

        result = discover_complex_candidates(
            protein_a="A0A0P0Y832",
            protein_b="P0C2Z6",
        )

        mock_fetch.assert_called_once_with("A0A0P0Y832")
        self.assertEqual(result, [matching])
if __name__ == "__main__":
    unittest.main()
