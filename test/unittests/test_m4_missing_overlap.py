import unittest
import pandas as pd
from claudio.utils.utils import clean_dataset
from claudio.module04.src.algorithm.combine_reevals import (
    combine_inter_reevaluations,
)


class TestM4MissingOverlap(unittest.TestCase):
    def test_missing_overlap_does_not_create_inter_evidence(self):
        data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P1",
            "chain_a": "A", "chain_b": "A",
            "pos_a": 3, "pos_b": 9,
            "pLDDT_a": "-", "pLDDT_b": "-",
            "eucl_dist": 15.0, "topo_dist": 20.0,
            "homo_pep_overl": float("nan"),
            "homo_int_overl": float("nan"),
        }])

        result = combine_inter_reevaluations(
            data,
            plddt_cutoff=70,
            linker_minimum=5,
            linker_maximum=35,
            euclidean_strictness=None,
            distance_maximum=50,
            cutoff=0.5,
            compute_scoring=True,
        )
        row = result.iloc[0]

        self.assertEqual(row["inter_score"], 0.0)
        self.assertEqual(row["evidence"], "")
        self.assertEqual(row["XL_type"], "intra")
    def test_cleanup_preserves_missing_overlap(self):
        data = pd.DataFrame([{
            "unip_id_a": "P1", "unip_id_b": "P1",
            "seq_a": "MAKTAKTGKT", "seq_b": "MAKTAKTGKT",
            "pep_a": "AKT", "pep_b": "GKT",
            "pos_a": 3, "pos_b": 9,
            "res_pos_a": 2, "res_pos_b": 2,
            "homo_adjacency": float("nan"),
            "homo_int_overl": float("nan"),
            "homo_pep_overl": float("nan"),
        }])

        result = clean_dataset(data)

        self.assertTrue(pd.isna(result.iloc[0]["homo_pep_overl"]))