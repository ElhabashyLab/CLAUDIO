import unittest

import pandas as pd

from claudio.module01.src.algorithm.check_data import check_pep_pos
from claudio.utils.utils import build_xl_dataset


class TestM1PositionSupport(unittest.TestCase):
    def test_missing_peptide_position_requires_sequence_support(self):
        cases = (
            ("MKAAGT", 2, "invalid"),
            ("MAKTAKTK", 8, "ambiguous"),
            ("MAKTAKTK", 6, "valid"),
        )

        for site in ("a", "b"):
            for sequence, position, expected in cases:
                with self.subTest(
                    site=site, sequence=sequence, position=position
                ):
                    row = pd.Series({
                        f"seq_{site}": sequence,
                        f"pep_{site}": "AKT",
                        f"pos_{site}": position,
                        f"res_pos_{site}": float("nan"),
                    })

                    result, _ = check_pep_pos(
                        0, row, site, build_xl_dataset("K"), "", 0
                    )

                    self.assertEqual(
                        result[f"position_status_{site}"],
                        expected,
                    )