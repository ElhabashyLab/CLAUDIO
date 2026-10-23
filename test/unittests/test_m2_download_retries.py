"""Download retries must stop after the configured limit."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from requests.exceptions import ConnectionError

from claudio.module02.src_structure_search.algorithm import pdb_download
from claudio.module02.src_distance_reevaluation.algorithm import search_pdb_pos


class TestM2DownloadRetries(unittest.TestCase):

    def test_structure_download_stops_after_connection_failures(self):
        urls = [
            "https://files.rcsb.org/download/1ABC.pdb",
            "https://alphafold.ebi.ac.uk/files/AF-P12345-F1-model_v6.pdb",
        ]
        for url in urls:
            for start in [0, 5, 6]:
                with self.subTest(url=url, start=start):
                    attempts = max(1, 6 - start)
                    failures = [
                        ConnectionError("offline") for _ in range(attempts)
                    ]
                    failures.append(AssertionError("Download retried past its limit"))
                    with patch.object(
                        pdb_download.r, "get", side_effect=failures
                    ) as get, redirect_stdout(StringIO()):
                        result = pdb_download.download_pdb_from_db(url, start, 5)
                    self.assertIsNone(result)
                    self.assertEqual(get.call_count, attempts)

    def test_af_replacement_stops_after_connection_failures(self):
        with TemporaryDirectory() as folder:
            path = str(Path(folder) / "blastp_1ABC.pdb")
            for start in [0, 5, 6]:
                with self.subTest(start=start):
                    attempts = max(1, 6 - start)
                    failures = [
                        ConnectionError("offline") for _ in range(attempts)
                    ]
                    failures.append(AssertionError("AF replacement retried past its limit"))
                    with patch.object(
                        search_pdb_pos.r, "get", side_effect=failures
                    ) as get, redirect_stdout(StringIO()):
                        result = search_pdb_pos.replacement_alphafold_download(
                            "P12345", path, 0, i_try=start
                        )
                    self.assertEqual(result, (None, ""))
                    self.assertEqual(get.call_count, attempts)
                    self.assertEqual(list(Path(folder).iterdir()), [])



if __name__ == "__main__":
    unittest.main()
