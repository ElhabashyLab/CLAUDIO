"""Tests for rejecting invalid AlphaFold download responses."""

import unittest
from unittest.mock import Mock, call, patch

from requests import Response

from claudio.data.constants import ALPHAFOLD_URL
from claudio.module02.src_structure_search.algorithm import pdb_download


class TestM2AFResponseValidation(unittest.TestCase):

    def test_returns_none_when_all_versions_return_xml_errors(self):
        error_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<Error>\n"
            "<Code>NoSuchKey</Code>\n"
            "<Message>The specified key does not exist.</Message>\n"
            "<Resource>missing-model.pdb</Resource>\n"
            "</Error>\n"
        )
        url = ALPHAFOLD_URL[0] + "P12345" + ALPHAFOLD_URL[1]

        with patch.object(
            pdb_download.r,
            "get",
            return_value=Mock(status_code=404, text=error_xml),
        ) as mock_get:
            result = pdb_download.download_pdb_from_db(url, 0, 5)

        self.assertIsNone(
            result,
            "An XML error response must not be returned as a structure",
        )
        self.assertEqual(
            mock_get.call_count,
            6,
            "Each supported model version should be tried once",
        )


    @staticmethod
    def _response(status, text):
        response = Response()
        response.status_code = status
        response._content = text.encode("utf-8")
        response.encoding = "utf-8"
        response.url = "https://alphafold.ebi.ac.uk/files/test.pdb"
        return response

    @staticmethod
    def _valid_pdb():
        return (
            "ATOM      1  CA  ALA A   1      11.000  12.000  13.000"
            "  1.00 90.00           C  \n"
            "END\n"
        )

    def test_rejects_invalid_structure_bodies(self):
        bodies = [
            "",
            "<html><body>Service unavailable</body></html>",
            "<?xml version=\"1.0\"?><Error><Code>NoSuchKey</Code></Error>",
            "HEADER    NO COORDINATES\nEND\n",
            self._valid_pdb().replace("11.000", "   nan"),
            self._valid_pdb().replace("11.000", "   inf"),
            "ATOM      1  CA  ALA A   1      broken coordinates\nEND\n",
        ]
        url = ALPHAFOLD_URL[0] + "P12345" + ALPHAFOLD_URL[1]
        for body in bodies:
            with self.subTest(body=body):
                with patch.object(
                    pdb_download.r, "get",
                    return_value=self._response(200, body),
                ):
                    result = pdb_download.download_pdb_from_db(url, 0, 5)
                self.assertIsNone(
                    result, "Only parseable structures with atoms may be returned"
                )

    def test_returns_valid_pdb_content_unchanged(self):
        text = self._valid_pdb()
        url = ALPHAFOLD_URL[0] + "P12345" + ALPHAFOLD_URL[1]
        with patch.object(
            pdb_download.r, "get",
            return_value=self._response(200, text),
        ) as mock_get:
            result = pdb_download.download_pdb_from_db(url, 0, 5)
        self.assertEqual(result, text)
        mock_get.assert_called_once_with(url, timeout=60)

    def test_falls_back_to_an_available_older_version(self):
        text = self._valid_pdb()
        url = ALPHAFOLD_URL[0] + "P12345" + ALPHAFOLD_URL[1]
        with patch.object(
            pdb_download.r, "get",
            side_effect=[
                self._response(404, "<Error>Missing</Error>"),
                self._response(200, text),
            ],
        ) as mock_get:
            result = pdb_download.download_pdb_from_db(url, 0, 5)
        self.assertEqual(result, text)
        self.assertEqual(
            mock_get.call_args_list,
            [call(url, timeout=60),
             call(url.replace("model_v6", "model_v5"), timeout=60)],
        )


if __name__ == "__main__":
    unittest.main()
