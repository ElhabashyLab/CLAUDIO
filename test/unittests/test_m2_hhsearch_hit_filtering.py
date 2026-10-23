"""Tests for filtering HHsearch hits by the requested cutoffs."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from claudio.module02.src_structure_search.algorithm import structure_search


class TestM2HHsearchHitFiltering(unittest.TestCase):

    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "structure_search.retrieve_identical_chain_ids",
        return_value=None,
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "structure_search.os.system"
    )
    def test_rejects_hits_that_fail_each_requested_cutoff(
        self, mock_system, mock_identical_chains
    ):
        cases = [
            (
                "identity",
                "P1\t1AAA_A\t0.100\t100\t90\t0\t1\t100\t1\t100\t1e-10\t20\n",
            ),
            (
                "coverage",
                "P1\t1AAA_A\t1.000\t5\t0\t0\t1\t5\t1\t5\t1e-10\t20\n",
            ),
            (
                "e_value",
                "P1\t1AAA_A\t1.000\t100\t0\t0\t1\t100\t1\t100\t0.1\t20\n",
            ),
        ]

        for case, hit_line in cases:
            with self.subTest(case=case), TemporaryDirectory() as folder:
                root = Path(folder)
                mock_identical_chains.reset_mock()

                def fake_hhsearch(command):
                    (root / "tmpP1.hhr").write_text(
                        hit_line, encoding="utf-8"
                    )
                    return 0

                mock_system.side_effect = fake_hhsearch
                result = structure_search.perform_search(
                    unip_id="P1",
                    sequence="M" * 100,
                    search_tool="hhsearch",
                    e_value=1e-5,
                    query_id=90.0,
                    coverage=50.0,
                    tmp_filepath=str(root / "search_cache.csv"),
                    blast_bin=None,
                    blast_db="unused/",
                    hhsearch_bin=None,
                    hhsearch_db="unused/",
                )

                self.assertEqual(result, ([], None, None, "P1"))
                mock_identical_chains.assert_not_called()

    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "structure_search.retrieve_identical_chain_ids",
        return_value=None,
    )
    @patch(
        "claudio.module02.src_structure_search.algorithm."
        "structure_search.os.system"
    )
    def test_keeps_valid_local_hits_and_exact_cutoff_values(
        self, mock_system, mock_identical_chains
    ):
        cases = [
            (
                "perfect_local_match",
                "P1\t2BBB_C\t0.050\t1000\t0\t0\t1\t50\t101\t150\t1e-10\t50\n",
            ),
            (
                "exact_cutoffs",
                "P1\t2BBB_C\t0.045\t1000\t5\t0\t1\t50\t101\t150\t1e-5\t50\n",
            ),
        ]

        for case, hit_line in cases:
            with self.subTest(case=case), TemporaryDirectory() as folder:
                root = Path(folder)
                mock_identical_chains.reset_mock()

                def fake_hhsearch(command):
                    (root / "tmpP1.hhr").write_text(
                        hit_line, encoding="utf-8"
                    )
                    return 0

                mock_system.side_effect = fake_hhsearch
                result = structure_search.perform_search(
                    unip_id="P1", sequence="M" * 100,
                    search_tool="hhsearch",
                    e_value=1e-5, query_id=90.0, coverage=50.0,
                    tmp_filepath=str(root / "search_cache.csv"),
                    blast_bin=None, blast_db="unused/",
                    hhsearch_bin=None, hhsearch_db="unused/",
                )

                self.assertEqual(
                    result, (["2BBB_C"], "2BBB", "C", "P1")
                )
                mock_identical_chains.assert_called_once_with(
                    "2BBB", "C", 5
                )

    def test_filters_before_limiting_to_twenty_hits(self):
        bad_line = (
            "P1\t1AAA_A\t0.100\t100\t90\t0\t1\t100\t1\t100\t1e-10\t20\n"
        )
        other_query = (
            "OTHER\t2BBB_C\t1.000\t100\t0\t0\t1\t100\t1\t100\t1e-10\t50\n"
        )
        good_lines = [
            f"P1\t{1000 + i}_A\t0.045\t1000\t5\t0\t1\t50\t101\t150\t1e-5\t50\n"
            for i in range(22)
        ]

        with TemporaryDirectory() as folder:
            path = Path(folder) / "hits.hhr"
            path.write_text(
                bad_line * 21 + other_query + "".join(good_lines),
                encoding="utf-8",
            )
            result = structure_search._read_hhsearch_hits(
                str(path), "P1", 100, 1e-5, 90.0, 50.0
            )

        self.assertEqual(
            result, [f"{1000 + i}_A" for i in range(20)]
        )

    def test_handles_rounded_match_ratios_conservatively(self):
        cases = [
            (
                "uncertain_at_cutoff", 1000, [],
                "P1\t2BBB_C\t0.045\t10000\t50\t0\t1\t500\t101\t600\t1e-5\t50\n",
            ),
            (
                "clearly_above_cutoff", 1000, ["2BBB_C"],
                "P1\t2BBB_C\t0.046\t10000\t40\t0\t1\t500\t101\t600\t1e-5\t50\n",
            ),
            (
                "one_match_not_zero", 1, ["2BBB_C"],
                "P1\t2BBB_C\t0.333\t3\t0\t0\t1\t1\t1\t1\t1e-5\t50\n",
            ),
        ]

        with TemporaryDirectory() as folder:
            path = Path(folder) / "hits.hhr"
            for case, query_length, expected, line in cases:
                with self.subTest(case=case):
                    path.write_text(line, encoding="utf-8")
                    result = structure_search._read_hhsearch_hits(
                        str(path), "P1", query_length, 1e-5, 90.0, 50.0
                    )
                    self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
