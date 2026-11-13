
import unittest

import numpy as np
from scipy.stats import norm

from validator import DataValidator
from analyzer import ABAnalyzer


class TestDataValidator(unittest.TestCase):

    def setUp(self) -> None:
        self.validator = DataValidator("test_in_50.csv")
        self.validator.validate()

    def test_valid_records(self) -> None:
        data = self.validator.get_valid_data()
        self.assertEqual(len(data), 41)

    def test_validation_errors(self) -> None:
        errors = self.validator.get_errors()
        self.assertEqual(len(errors), 9)

    def test_no_duplicate_users(self) -> None:
        data = self.validator.get_valid_data()
        user_ids = [row["user_id"] for row in data]

        self.assertEqual(len(user_ids), len(set(user_ids)))
        self.assertNotIn("U010", user_ids)
        self.assertNotIn("U020", user_ids)

    def test_valid_values(self) -> None:
        data = self.validator.get_valid_data()

        for row in data:
            self.assertIn(row["group"], ("A", "B"))
            self.assertIn(row["converted"], (0, 1))


class TestABAnalyzer(unittest.TestCase):

    def setUp(self) -> None:
        validator = DataValidator("test_in_50.csv")
        validator.validate()
        self.analyzer = ABAnalyzer(validator.get_valid_data())

    def test_conversion_rates(self) -> None:
        p_A, p_B = self.analyzer.conversion_rates()

        self.assertAlmostEqual(
            p_A, sum(self.analyzer.A) / len(self.analyzer.A)
        )
        self.assertAlmostEqual(
            p_B, sum(self.analyzer.B) / len(self.analyzer.B)
        )

    def test_pooled_proportion(self) -> None:
        expected = (
            sum(self.analyzer.A) + sum(self.analyzer.B)
        ) / (len(self.analyzer.A) + len(self.analyzer.B))

        self.assertAlmostEqual(self.analyzer.pool_prop(), expected)

    def test_standard_error(self) -> None:
        p = self.analyzer.pool_prop()
        expected = np.sqrt(
            p * (1 - p) *
            (1 / len(self.analyzer.A) + 1 / len(self.analyzer.B))
        )

        self.assertAlmostEqual(self.analyzer.standard_error(), expected)

    def test_z_test(self) -> None:
        z, p_value = self.analyzer.z_test()

        expected_z = (
            sum(self.analyzer.B) / len(self.analyzer.B)
            - sum(self.analyzer.A) / len(self.analyzer.A)
        ) / self.analyzer.standard_error()

        self.assertAlmostEqual(z, expected_z)
        self.assertAlmostEqual(
            p_value, 2 * norm.sf(abs(z))
        )
        self.assertGreaterEqual(p_value, 0)
        self.assertLessEqual(p_value, 1)

    def test_interpret(self) -> None:
        _, p_value = self.analyzer.z_test()
        conclusion = self.analyzer.interpret(alpha=0.05)

        if p_value < 0.05:
            self.assertIn("Reject H0", conclusion)
        else:
            self.assertIn("Fail to reject H0", conclusion)


if __name__ == "__main__":
    unittest.main()
