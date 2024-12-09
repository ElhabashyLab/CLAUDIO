import unittest
import numpy as np
from claudio.utils.utils import evaluate_boolean_input, round_self

class Test_utils(unittest.TestCase):
    def test_evaluate_boolean_input(self):
        self.assertEqual(evaluate_boolean_input("y"), True)
        self.assertEqual(evaluate_boolean_input("yes"), True)
        self.assertEqual(evaluate_boolean_input("t"), True)
        self.assertEqual(evaluate_boolean_input("true"), True)
        self.assertEqual(evaluate_boolean_input("on"), True)
        self.assertEqual(evaluate_boolean_input("1"), True)
        self.assertEqual(evaluate_boolean_input("n"), False)
        self.assertEqual(evaluate_boolean_input("no"), False)
        self.assertEqual(evaluate_boolean_input("f"), False)
        self.assertEqual(evaluate_boolean_input("false"), False)
        self.assertEqual(evaluate_boolean_input("off"), False)
        self.assertEqual(evaluate_boolean_input("0"), False)
        with self.assertRaises(ValueError):
            evaluate_boolean_input("invalid")

    def test_round_self(self):
        self.assertEqual(round_self(1.23456789, 2), 1.23)
        self.assertEqual(round_self(1.23456789, 3), 1.235)
        self.assertTrue(np.isnan(round_self(np.nan, 2)))
        self.assertEqual(round_self(1.5, 0), 2)


if __name__ == '__main__':
    unittest.main()