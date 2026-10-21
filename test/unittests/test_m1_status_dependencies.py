"""Verify the M1 fixes required by position-aware M3 analysis."""
import unittest
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from claudio.module01.src.algorithm.check_data import double_check_data
from claudio.module03.src.algorithm.signal_analysis import analyse_homo_signals
from claudio.utils.utils import build_xl_dataset


class TestM1StatusDependencies(unittest.TestCase):
    def test_unsupported_peptide_is_invalid_and_not_scored_by_m3(self):
        data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "MKAAGT", "seq_b": "MKAAGT",
            "pep_a": "AKT", "pep_b": "MKA",
            "pos_a": 2, "pos_b": 2,
            "res_pos_a": np.nan, "res_pos_b": 2,
        }])
        with TemporaryDirectory() as folder:
            checked = double_check_data(
                data, "unsupported", build_xl_dataset("K"),
                folder + "/", 0,
            )

        self.assertEqual(len(checked), 1)
        self.assertEqual(checked.iloc[0]["position_status_a"], "invalid")
        analysed = analyse_homo_signals(checked, 0)
        for column in ("homo_adjacency", "homo_int_overl", "homo_pep_overl"):
            with self.subTest(column=column):
                self.assertTrue(pd.isna(analysed.iloc[0][column]))

    def test_expanded_candidates_are_rechecked_without_changing_the_original(self):
        data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "MKAKTAKT", "seq_b": "MKAKTAKT",
            "pep_a": "AKT", "pep_b": "MKA",
            "pos_a": 1, "pos_b": 2,
            "res_pos_a": np.nan, "res_pos_b": 2,
        }])
        with TemporaryDirectory() as folder:
            checked = double_check_data(
                data, "expanded", build_xl_dataset("K"),
                folder + "/", 0,
            )

        original = checked[checked["pos_a"] == 1]
        candidates = checked[checked["pos_a"].isin([4, 7])]

        self.assertEqual(len(original), 1)
        self.assertEqual(original.iloc[0]["position_status_a"], "ambiguous")
        self.assertEqual(set(candidates["pos_a"]), {4, 7})
        self.assertEqual(len(candidates), 2)
        self.assertTrue(candidates["position_status_a"].eq("valid").all())
        self.assertTrue(candidates["position_status_b"].eq("valid").all())


if __name__ == "__main__":
    unittest.main()
