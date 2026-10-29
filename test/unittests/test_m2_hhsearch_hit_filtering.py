"""Tests for filtering HHsearch hits by the requested cutoffs."""

from io import StringIO
from pathlib import Path
import shlex
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from claudio.module02.src_structure_search.algorithm import structure_search


def write_hits(root, hits, query_length):
    """Write matching HH-suite tabular and alignment-report fixtures."""
    rows = []
    blocks = [f"Query P1\nMatch_columns {query_length}\n"]
    for number, (target, query, template, evalue, template_length) in enumerate(hits, 1):
        paired = [(q, t) for q, t in zip(query.upper(), template.upper())
                  if q not in "-." and t not in "-."]
        matches = sum(q == t for q, t in paired)
        qend = sum(q not in "-." for q in query)
        tend = sum(t not in "-." for t in template)
        gapopen = sum(
            residue == "-" and (i == 0 or seq[i - 1] != "-")
            for seq in (query, template) for i, residue in enumerate(seq)
        )
        rows.append(
            f"P1\t{target}\t{matches / template_length:.3f}\t"
            f"{template_length}\t{len(paired) - matches}\t{gapopen}\t"
            f"1\t{qend}\t1\t{tend}\t{evalue}\t50\n"
        )
        identity = 100 * matches / len(paired) if paired else 0
        blocks.append(
            f"No {number}\n>{target}\n"
            f"Probab=99 E-value={evalue} Aligned_cols={len(paired)} "
            f"Identities={identity:.0f}%\n"
            f"Q P1 1 {query} {qend} ({query_length})\n"
            f"T {target[:14]} 1 {template} {tend} ({template_length})\n\n"
        )
    (root / "tmpP1.hhr").write_text("".join(rows), encoding="utf-8")
    (root / "tmpP1_alignments.hhr").write_text("".join(blocks), encoding="utf-8")


class TestM2HHsearchHitFiltering(unittest.TestCase):
    def search(self, hits, query_length=100, identity=90.0, coverage=50.0):
        with TemporaryDirectory() as folder:
            root = Path(folder)

            def run_hhsearch(command):
                args = shlex.split(command)
                self.assertEqual(args[args.index("-o") + 1], str(root / "tmpP1_alignments.hhr"))
                self.assertEqual(args[args.index("-blasttab") + 1], str(root / "tmpP1.hhr"))
                self.assertEqual(args[args.index("-seq") + 1], "1")
                self.assertEqual(args[args.index("-p") + 1], "0")
                self.assertEqual(args[args.index("-B") + 1], "2147483647")
                self.assertNotIn("-qid", args)
                self.assertNotIn("-cov", args)
                write_hits(root, hits, query_length)
                return 0

            with patch.object(structure_search.os, "system", side_effect=run_hhsearch), patch.object(
                structure_search, "retrieve_identical_chain_ids", return_value=None
            ) as identical_chains:
                result = structure_search.perform_search(
                    "P1", "M" * query_length, "hhsearch", 1e-5, identity,
                    coverage, str(root / "search_cache.csv"),
                    None, "unused/", None, "unused/",
                )
                if not result[0]:
                    identical_chains.assert_not_called()
                return result

    def read_hits(self, hits, query_length=100, identity=90.0):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            write_hits(root, hits, query_length)
            return structure_search._read_hhsearch_hits(
                str(root / "tmpP1.hhr"), "P1", query_length, 1e-5,
                identity, 50.0, str(root / "tmpP1_alignments.hhr"),
            )

    def test_rejects_hits_that_fail_each_requested_cutoff(self):
        cases = [
            ("identity", "M" * 100, "M" * 10 + "K" * 90, "1e-10", 100),
            ("coverage", "M" * 5, "M" * 5, "1e-10", 5),
            ("e_value", "M" * 100, "M" * 100, "0.1", 100),
        ]
        for case, query, template, evalue, length in cases:
            with self.subTest(case=case):
                self.assertEqual(
                    self.search([("1AAA_A", query, template, evalue, length)]),
                    ([], None, None, "P1"),
                )

    def test_keeps_valid_local_hits_and_exact_cutoff_values(self):
        for case, template in [
            ("perfect_local_match", "M" * 50),
            ("exact_cutoffs", "M" * 45 + "K" * 5),
        ]:
            with self.subTest(case=case):
                self.assertEqual(
                    self.search([("2BBB_C", "M" * 50, template, "1e-5", 1000)]),
                    (["2BBB_C"], "2BBB", "C", "P1"),
                )

    def test_filters_before_limiting_to_twenty_hits(self):
        hits = [("1AAA_A", "M" * 100, "M" * 10 + "K" * 90, "1e-10", 100)] * 21
        hits += [(f"{1000 + i}_A", "M" * 50, "M" * 45 + "K" * 5, "1e-5", 1000)
                 for i in range(22)]
        self.assertEqual(self.read_hits(hits), [f"{1000 + i}_A" for i in range(20)])

    def test_identity_includes_gaps_in_either_sequence(self):
        for query, template in [
            ("M" * 10 + "--", "M" * 8 + "KKMM"),
            ("M" * 12, "M" * 8 + "KK--"),
        ]:
            with self.subTest(query=query, template=template):
                hit = ("1AAA_A", query, template, "1e-10", 100)
                self.assertEqual(self.search([hit], 20, 80.0), ([], None, None, "P1"))
                self.assertEqual(self.search([hit], 20, 66.66)[0], ["1AAA_A"])

    def test_counts_gap_columns_instead_of_gap_openings(self):
        cases = [
            ("one_long_gap", "M" * 90 + "-" * 10, []),
            ("two_single_gaps", "M" * 49 + "-" + "M" * 49 + "-", ["1AAA_A"]),
        ]
        for case, template, expected in cases:
            with self.subTest(case=case):
                self.assertEqual(
                    self.read_hits([("1AAA_A", "M" * 100, template, "1e-10", 100)], identity=95),
                    expected,
                )

    def test_keeps_exact_identity_at_a_gapped_cutoff(self):
        hit = ("1AAA_A", "M" * 100, "M" * 80 + "-" * 20, "1e-10", 100)
        self.assertEqual(self.read_hits([hit], identity=80.0), ["1AAA_A"])
        self.assertEqual(self.read_hits([hit], identity=80.01), [])

    def test_uses_alignment_counts_instead_of_rounded_tabular_ratio(self):
        hit = ("2BBB_C", "M" * 500, "M" * 450 + "K" * 50, "1e-5", 10000)
        self.assertEqual(self.read_hits([hit], 1000, 90.0), ["2BBB_C"])
        self.assertEqual(self.read_hits([hit], 1000, 90.01), [])

    def test_reads_wrapped_sequences_without_counting_annotation_rows(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            hit = ("1AAA_A", "M" * 10 + "--", "M" * 8 + "KKMM", "1e-10", 100)
            write_hits(root, [hit], 20)
            (root / "tmpP1_alignments.hhr").write_text(
                "Query P1\nNo 1\n>1AAA_A description\n"
                "Probab=99 E-value=1e-10 Aligned_cols=10 Identities=80%\n"
                "Q ss_pred CCCCCCCC\n"
                "Q P1 1 MMMMMMMM 8 (20)\n"
                "Q Consensus 1 mmmmmmmm 8 (20)\n"
                "T Consensus 1 mmmmmmmm 8 (100)\n"
                "T 1AAA_A 1 mmmmmmmm 8 (100)\n"
                "T ss_dssp CCCCCCCC\n\n"
                "Q P1 9 MM-- 10 (20)\n"
                "T 1AAA_A 9 KKMM 12 (100)\n"
            )
            self.assertEqual(structure_search._read_hhsearch_hits(
                str(root / "tmpP1.hhr"), "P1", 20, 1e-5, 80.0, 50.0,
                str(root / "tmpP1_alignments.hhr"),
            ), [])

    def test_rejects_missing_or_inconsistent_alignment_reports(self):
        reports = [
            "Query P1\n",
            "Query P1\n>2BBB_C\nQ P1 1 MMM 3 (3)\nT 2BBB_C 1 MMM 3 (3)\n",
            "Query OTHER\n>1AAA_A\nQ OTHER 1 MMM 3 (3)\nT 1AAA_A 1 MMM 3 (3)\n",
            "Query P1\n>1AAA_A\nQ P1 1 MMM 3 (3)\n",
            "Query P1\n>1AAA_A\nQ P1 1 MM 2 (3)\nT 1AAA_A 1 MM 2 (3)\n",
        ]
        with TemporaryDirectory() as folder:
            root = Path(folder)
            write_hits(root, [("1AAA_A", "MMM", "MMM", "1e-10", 3)], 3)
            for report in reports:
                with self.subTest(report=report):
                    (root / "tmpP1_alignments.hhr").write_text(report)
                    with self.assertRaises(ValueError):
                        structure_search._read_hhsearch_hits(
                            str(root / "tmpP1.hhr"), "P1", 3, 1e-5, 90.0, 50.0,
                            str(root / "tmpP1_alignments.hhr"),
                        )

    def test_blast_and_hhsearch_apply_the_same_gapped_identity_cutoff(self):
        hit = ("1AAA_A", "M" * 10 + "--", "M" * 8 + "KKMM", "1e-10", 100)
        for cutoff, expected in [(60.0, ["1AAA_A"]), (80.0, [])]:
            with self.subTest(cutoff=cutoff), TemporaryDirectory() as folder:
                with patch.object(structure_search.os, "popen", return_value=StringIO(
                    "1AAA_A,66.667,50,1e-10\n"
                )), patch.object(structure_search, "retrieve_identical_chain_ids", return_value=None):
                    blast = structure_search.perform_search(
                        "P1", "M" * 20, "blastp", 1e-5, cutoff, 50.0,
                        str(Path(folder) / "search_cache.csv"),
                        None, "unused/", None, "unused/",
                    )
                hhsearch = self.search([hit], 20, cutoff)
                self.assertEqual(blast[0], expected)
                self.assertEqual(hhsearch[0], expected)


if __name__ == "__main__":
    unittest.main()
