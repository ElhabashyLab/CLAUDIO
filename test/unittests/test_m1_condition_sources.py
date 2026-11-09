"""Keep experimental sources separate from shared residue-pair candidates."""
import importlib
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pandas as pd
from click.testing import CliRunner

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.utils.utils import build_xl_dataset

m1 = importlib.import_module("claudio.module01.src.main")


class TestM1ConditionSources(unittest.TestCase):
    def setUp(self):
        folder = TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.records = []
        conditions = [("Rep1", "Mitochondria"), ("Rep1", "Nucleus"),
                      ("Rep2", "Nucleus")]
        for number, (replicate, fraction) in enumerate(conditions, 1):
            self.records.append({
                "source_record_id": f"record_{number:06d}",
                "unip_id_a": "P1", "unip_id_b": "P2",
                "seq_a": "MAKT", "seq_b": "MGKT",
                "pep_a": "AKT", "pep_b": "GKT",
                "pos_a": 3, "pos_b": 3,
                "res_pos_a": 2, "res_pos_b": 2,
                "original_pos_a": 3, "original_pos_b": 3,
                "biological_replicate": replicate,
                "organelle_fraction": fraction,
                "supporting_csm_count": number,
            })

    def check(self, records, **options):
        result = double_check_data(
            pd.DataFrame(records), "conditions", build_xl_dataset("K"),
            str(self.root) + "/", 0, **options,
        )
        report = pd.read_csv(self.root / "conditions_duplicate_sources.csv")
        return result, report

    def test_five_sources_remain_separate_with_three_shared_candidates(self):
        records = self.records + [
            {**self.records[0], "source_record_id": "record_000004",
             "unip_id_a": "P3"},
            {**self.records[0], "source_record_id": "record_000005",
             "unip_id_a": "P4"},
        ]
        expected = pd.DataFrame(records).set_index("source_record_id")
        columns = ["original_pos_a", "original_pos_b", "biological_replicate",
                   "organelle_fraction", "supporting_csm_count"]
        for order in (records, records[::-1]):
            with self.subTest(reversed=order is not records):
                result, report = self.check(order, preserve_source_records=True)
                self.assertEqual(len(result), 5)
                self.assertEqual(result["candidate_id"].nunique(), 3)
                self.assertTrue(result["candidate_id"].notna().all())
                pd.testing.assert_frame_equal(
                    result.set_index("source_record_id")[columns].sort_index(),
                    expected[columns].sort_index(),
                )
                shared = result[result["unip_id_a"].eq("P1")]
                self.assertEqual(shared["candidate_id"].nunique(), 1)
                self.assertTrue(report.empty)

    def test_reversed_endpoints_and_identical_conditions_keep_their_sources(self):
        first = self.records[0]
        reverse = dict(first, source_record_id="record_000003")
        for field in ("unip_id", "seq", "pep", "pos", "res_pos", "original_pos"):
            reverse[f"{field}_a"] = first[f"{field}_b"]
            reverse[f"{field}_b"] = first[f"{field}_a"]
        result, report = self.check([
            first, {**first, "source_record_id": "record_000002"}, reverse,
        ], preserve_source_records=True)
        self.assertEqual(result["source_record_id"].tolist(),
                         ["record_000001", "record_000002", "record_000003"])
        self.assertEqual(result["candidate_id"].nunique(), 1)
        self.assertTrue(report.empty)

    def test_each_source_gets_all_repeated_peptide_candidates(self):
        records = [{**row, "seq_a": "MAKTAKT"} for row in self.records]
        result, report = self.check(records, preserve_source_records=True)
        self.assertEqual(len(result), 6)
        self.assertEqual(result["candidate_id"].nunique(), 2)
        for source, rows in result.groupby("source_record_id"):
            with self.subTest(source=source):
                self.assertEqual(set(rows["pos_a"]), {3, 6})
                self.assertTrue(rows["original_pos_a"].eq(3).all())
                self.assertTrue(rows["position_status_a"].eq("valid").all())
        self.assertTrue(report.empty)

    def test_unsupported_positions_stay_invalid_without_a_candidate_id(self):
        records = [{**row, "seq_a": "MGKT"} for row in self.records]
        result, report = self.check(records, preserve_source_records=True)
        self.assertEqual(len(result), 3)
        self.assertTrue(result["position_status_a"].eq("invalid").all())
        self.assertTrue(result["candidate_id"].isna().all())
        self.assertTrue(report.empty)

    def test_default_deduplication_still_reports_removed_sources(self):
        result, report = self.check(self.records)
        self.assertEqual(result["source_record_id"].tolist(), ["record_000001"])
        self.assertEqual(report.to_dict("records"), [
            {"retained_source_record_id": "record_000001",
             "duplicate_source_record_id": "record_000002"},
            {"retained_source_record_id": "record_000001",
             "duplicate_source_record_id": "record_000003"},
        ])

    def test_m1_cli_writes_each_condition_when_preservation_is_requested(self):
        data = pd.DataFrame(self.records).drop(columns=[
            "source_record_id", "seq_a", "seq_b", "original_pos_a", "original_pos_b",
        ])
        input_path = self.root / "input.csv"
        data.to_csv(input_path, index=False)
        projections = "pep_a,pep_b,pos_a,pos_b,res_pos_a,res_pos_b,unip_id_a,unip_id_b"
        for preserve in (False, True):
            with self.subTest(preserve=preserve):
                output = self.root / str(preserve)
                options = ["--preserve-source-records"] if preserve else []
                with patch.object(
                    m1, "do_uniprot_search",
                    side_effect=lambda data, *args: data.assign(seq_a="MAKT", seq_b="MGKT"),
                ), patch.object(
                    m1, "create_list_of_unique_proteins", return_value=pd.DataFrame(),
                ):
                    result = CliRunner().invoke(m1.main, [
                        "-i", str(input_path), "-o", str(output), "-p", projections,
                        "-x", "K", "-v", "0", "--skip-protein-structure-search", *options,
                    ])
                self.assertEqual(result.exit_code, 0,
                                 result.output + repr(result.exception))
                saved = pd.read_csv(output / "input.sqcs", index_col=0)
                self.assertEqual(len(saved), 3 if preserve else 1)
                if preserve:
                    self.assertEqual(saved["organelle_fraction"].tolist(),
                                     data["organelle_fraction"].tolist())
                    report = pd.read_csv(output / "input_record_tracking.csv", index_col=0)
                    self.assertEqual(report["candidate_id"].nunique(), 1)
                    self.assertNotIn("candidate_id", saved)
                    self.assertNotIn("position_status_a", saved)


if __name__ == "__main__":
    unittest.main()
