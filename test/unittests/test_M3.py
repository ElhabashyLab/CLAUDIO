import unittest
import pandas as pd
import numpy as np
from claudio.module03.src.algorithm.signal_analysis import compute_interaction_adj,compute_interaction_ovl

class TestM3(unittest.TestCase):
    def test_compute_interaction_adj(self):
        self.assertEqual(compute_interaction_adj(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12345", "pep_copies_found": False, "pos_a":"2", "pos_b":"4", "seq_a":"LKTKPS"})), 0.667)
        self.assertEqual(compute_interaction_adj(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12345", "pep_copies_found": False, "pos_a":"4", "pos_b":"2", "seq_a":"LKTKPS"})), 0.667)
        self.assertTrue(np.isnan(compute_interaction_adj(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12345", "pep_copies_found": True, "pos_a":"2", "pos_b":"4", "seq_a":"LKTKPS"}))))
        self.assertTrue(np.isnan(compute_interaction_adj(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12344", "pep_copies_found": False, "pos_a":"2", "pos_b":"4", "seq_a":"LKTKPS"}))))

    def test_compute_interaction_overlap(self):
        self.assertEqual(compute_interaction_ovl(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12345", "pep_copies_found": False, "pos_a":"2", "pos_b":"2"})), 1.0)
        self.assertTrue(np.isnan(compute_interaction_ovl(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12344", "pep_copies_found": False, "pos_a":"2", "pos_b":"2"}))))
        self.assertTrue(np.isnan(compute_interaction_ovl(pd.Series(data={"unip_id_a": "X12345", "unip_id_b": "X12345", "pep_copies_found": True, "pos_a":"2", "pos_b":"2"}))))

if __name__ == '__main__':
    unittest.main()