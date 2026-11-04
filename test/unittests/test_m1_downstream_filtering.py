import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.module01.src.io.write_out import write_outputs
from claudio.module03.src.algorithm.signal_analysis import analyse_homo_signals
from claudio.utils.utils import build_xl_dataset


class TestM1DownstreamFiltering(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sqcs = self.root / "sample.sqcs"
        self.report = self.root / "sample_record_tracking.csv"

    def record(self, **changes):
        row = {
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "MKAAKT", "seq_b": "MKAAKT",
            "pep_a": "AKT", "pep_b": "MKA",
            "pos_a": 5, "pos_b": 2, "res_pos_a": 2, "res_pos_b": 2,
            "source_record_id": "source_1", "original_pos_a": 5, "original_pos_b": 2,
            "position_status_a": "valid", "position_status_b": "valid",
        }
        row.update(changes)
        return row

    def write(self, data):
        write_outputs(data, pd.DataFrame({"unip_id": ["P1"]}),
                      "sample", str(self.root) + "/", 0)
        return pd.read_csv(self.sqcs, index_col=0)

    def read_report(self):
        self.assertTrue(self.report.is_file(), "Rejected sources need a preprocessing record")
        return pd.read_csv(self.report, index_col=0)

    def test_valid_and_corrected_records_reach_sqcs_without_tracking_columns(self):
        data = pd.DataFrame([
            self.record(),
            self.record(source_record_id="source_2", position_status_a="corrected"),
        ], index=[3, 8])
        output = self.write(data)
        self.assertEqual(list(output.index), [3, 8])
        self.assertEqual(list(output["pos_a"]), [5, 5])
        tracking = {"source_record_id", "original_pos_a", "original_pos_b",
                    "position_status_a", "position_status_b", "included_in_sqcs", "exclusion_reason"}
        self.assertTrue(tracking.isdisjoint(output.columns))
        report = self.read_report()
        self.assertEqual(list(report.index), [3, 8])
        self.assertEqual(list(report["source_record_id"]), ["source_1", "source_2"])
        self.assertTrue(report["included_in_sqcs"].all())

    def test_an_invalid_endpoint_is_excluded_and_its_reason_stays_in_the_report(self):
        for site in ("a", "b"):
            with self.subTest(site=site):
                data = pd.DataFrame([
                    self.record(source_record_id="bad", **{f"position_status_{site}": "invalid"}),
                    self.record(source_record_id="good"),
                ], index=[2, 7])
                output = self.write(data)
                self.assertEqual(list(output.index), [7])
                report = self.read_report()
                self.assertEqual(list(report.index), [2, 7])
                self.assertFalse(report.loc[2, "included_in_sqcs"])
                self.assertIn(f"position_status_{site}=invalid", report.loc[2, "exclusion_reason"])
                self.assertEqual(report.loc[2, "source_record_id"], "bad")
                self.assertEqual(report.loc[2, "original_pos_a"], 5)
                self.assertTrue(report.loc[7, "included_in_sqcs"])

    def test_ambiguous_source_does_not_remove_its_independently_validated_candidates(self):
        common = {"source_record_id": "repeated", "seq_a": "MKAKTAKT",
                  "seq_b": "MKAKTAKT", "original_pos_a": 1}
        data = pd.DataFrame([
            self.record(**common, position_status_a="ambiguous", pos_a=1),
            self.record(**common, pos_a=4),
            self.record(**common, pos_a=7),
        ], index=[0, 1, 2])
        output = self.write(data)
        self.assertEqual(list(output["pos_a"]), [4, 7])
        report = self.read_report()
        self.assertEqual(list(report["source_record_id"]), ["repeated"] * 3)
        self.assertEqual(list(report["included_in_sqcs"]), [False, True, True])
        self.assertIn("position_status_a=ambiguous", report.loc[0, "exclusion_reason"])

    def test_all_rejected_records_produce_a_header_only_sqcs_and_a_complete_report(self):
        data = pd.DataFrame([
            self.record(source_record_id="invalid", position_status_a="invalid"),
            self.record(source_record_id="ambiguous", position_status_b="ambiguous"),
        ])
        output = self.write(data)
        self.assertTrue(output.empty)
        self.assertTrue({"unip_id_a", "unip_id_b", "pep_a", "pep_b", "pos_a", "pos_b"}
                        <= set(output.columns))
        report = self.read_report()
        self.assertEqual(len(report), 2)
        self.assertFalse(report["included_in_sqcs"].any())

    def test_missing_or_unrecognised_statuses_are_not_assumed_to_be_valid(self):
        for status in (None, "", "pending", "VALID"):
            with self.subTest(status=status):
                output = self.write(pd.DataFrame([self.record(position_status_b=status)]))
                self.assertTrue(output.empty)
                self.assertFalse(self.read_report().iloc[0]["included_in_sqcs"])
        incomplete = pd.DataFrame([self.record()]).drop(columns="position_status_b")
        self.assertTrue(self.write(incomplete).empty)

    def test_legacy_data_without_position_status_columns_keep_the_existing_output(self):
        data = pd.DataFrame([self.record()]).drop(columns=["position_status_a", "position_status_b"])
        output = self.write(data)
        self.assertEqual(len(output), 1)
        self.assertEqual(output.iloc[0]["pos_a"], 5)
        self.assertNotIn("source_record_id", output.columns)

    def test_writing_outputs_does_not_modify_the_in_memory_preprocessing_records(self):
        data = pd.DataFrame([
            self.record(), self.record(source_record_id="rejected", position_status_b="invalid"),
        ])
        before = data.copy(deep=True)
        self.write(data)
        pd.testing.assert_frame_equal(data, before)

    def test_m3_reads_only_the_records_exported_as_valid_by_m1(self):
        data = pd.DataFrame([
            self.record(source_record_id="invalid", position_status_a="invalid", pos_a=2),
            self.record(source_record_id="valid", position_status_b="corrected"),
        ], index=[4, 9])
        sqcs = self.write(data)
        self.assertEqual(list(sqcs.index), [9])
        self.assertFalse({"position_status_a", "position_status_b"} & set(sqcs.columns))
        result = analyse_homo_signals(sqcs, 0)
        self.assertEqual(list(result.index), [9])
        self.assertEqual(result.iloc[0]["homo_adjacency"], 0.5)
        self.assertEqual(result.iloc[0]["homo_int_overl"], 0.0)
        self.assertFalse(result.iloc[0]["homo_pep_overl"])

    def test_real_m1_expansion_exports_valid_candidates_and_audits_the_ambiguous_parent(self):
        data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "MKAKTAKT", "seq_b": "MKAKTAKT",
            "pep_a": "AKT", "pep_b": "MKA", "pos_a": 1, "pos_b": 2,
            "res_pos_a": float("nan"), "res_pos_b": 2,
            "source_record_id": "repeated", "original_pos_a": 1, "original_pos_b": 2,
        }])
        checked = double_check_data(data, "sample", build_xl_dataset("K"), str(self.root) + "/", 0)
        output = self.write(checked)
        self.assertEqual(set(output["pos_a"]), {4, 7})
        self.assertEqual(len(output), 2)
        report = self.read_report()
        parent = report[report["pos_a"] == 1]
        self.assertEqual(len(parent), 1)
        self.assertFalse(parent.iloc[0]["included_in_sqcs"])
        self.assertEqual(parent.iloc[0]["position_status_a"], "ambiguous")
        self.assertEqual(int(report["included_in_sqcs"].sum()), 2)


if __name__ == "__main__":
    unittest.main()
