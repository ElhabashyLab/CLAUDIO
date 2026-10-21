import unittest

import pandas as pd

from claudio.module01.src.algorithm.check_data import create_duplicates
from claudio.utils.utils import build_xl_dataset


class TestM1CandidateBounds(unittest.TestCase):
    def test_out_of_bounds_original_b_does_not_crash_expansion(self):
        row = pd.Series({
            "unip_id_a": "P1", "unip_id_b": "P2",
            "seq_a": "MGKTGKT", "seq_b": "MAKTAKT",
            "pep_a": "GKT", "pep_b": "AKT",
            "pos_a": 3, "pos_b": 100,
            "res_pos_a": 2, "res_pos_b": 2,
            "original_pos_a": 3, "original_pos_b": 100,
            "source_record_id": "record_000001",
            "position_status_a": "valid",
            "position_status_b": "invalid",
        })

        result, _ = create_duplicates(
            row, build_xl_dataset("K"), ""
        )

        self.assertEqual(len(result), 4)
        self.assertEqual(
            set(zip(result["pos_a"], result["pos_b"])),
            {(3, 3), (3, 6), (6, 3), (6, 6)},
        )
        self.assertTrue(result["position_status_a"].eq("valid").all())
        self.assertTrue(result["position_status_b"].eq("valid").all())