"""Tests for B-side protein coordinates during candidate expansion."""

import unittest

import pandas as pd

from claudio.module01.src.algorithm.check_data import create_duplicates
from claudio.utils.utils import build_xl_dataset


class TestM1BSideCandidateStart(unittest.TestCase):
    def test_expands_b_side_without_spurious_positions(self):
        row = pd.Series({
            "unip_id_a": "P1",
            "unip_id_b": "P2",
            "seq_a": "MAKT",
            "seq_b": "MGKTGKT",
            "pep_a": "AKT",
            "pep_b": "GKT",
            "pos_a": 3,
            "pos_b": 3,
            "res_pos_a": 2,
            "res_pos_b": 2,
        })

        candidates, _ = create_duplicates(
            row, build_xl_dataset("K"), ""
        )

        self.assertEqual(
            set(zip(candidates["pos_a"], candidates["pos_b"])),
            {(3, 6)},
            "B-side expansion must not introduce protein position 2",
        )
        self.assertEqual(len(candidates), 1)


if __name__ == "__main__":
    unittest.main()
