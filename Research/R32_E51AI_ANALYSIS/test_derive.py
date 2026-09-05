"""Synthetic retention arithmetic tests; these fixtures are not research evidence."""
import runpy
from pathlib import Path
import unittest

RETENTION = runpy.run_path(str(Path(__file__).with_name("derive.py")))["retention"]
DELTA = runpy.run_path(str(Path(__file__).with_name("derive.py")))["parameter_delta"]


class RetentionTests(unittest.TestCase):
    def test_loss_and_regain(self):
        result = RETENTION([1, 1, 0], [[0, 1, 1], [1, 0, 1]])
        self.assertEqual(result["ever_lost"], 2)
        self.assertEqual(result["regained_at_final"], 1)
        self.assertEqual(result["missing_at_final"], 1)
        self.assertEqual(result["never_lost"], 0)
        self.assertEqual(result["worst_checkpoint_loss"], 1)

    def test_new_gain_is_not_retention(self):
        result = RETENTION([1, 0, 0], [[1, 1, 1]])
        self.assertEqual(result["anchor_successes"], 1)
        self.assertEqual(result["never_lost"], 1)

    def test_final_regain_does_not_erase_earlier_loss(self):
        result = RETENTION([1], [[0], [1]])
        self.assertEqual(result["ever_lost"], 1)
        self.assertEqual(result["never_lost"], 0)
        self.assertEqual(result["missing_at_final"], 0)

    def test_empty_success_set_has_undefined_fraction(self):
        result = RETENTION([0, 0], [[1, 1]])
        self.assertIsNone(result["final_retained_fraction"])

    def test_bad_width_rejected(self):
        with self.assertRaises(ValueError):
            RETENTION([1, 1], [[1]])

    def test_nonbinary_rejected(self):
        with self.assertRaises(ValueError):
            RETENTION([1], [[2]])

    def test_missing_checkpoints_rejected(self):
        with self.assertRaises(ValueError):
            RETENTION([1], [])

    def test_exact_coefficient_changes(self):
        current = [0] * 130
        current[0], current[129] = 3, -4
        self.assertEqual(DELTA([0] * 130, current), {
            "changed_coefficients": 2, "coefficient_l1_change": 7,
            "largest_coefficient_change": 4})

    def test_unchanged_coefficients(self):
        self.assertEqual(DELTA([1] * 130, [1] * 130)["changed_coefficients"], 0)

    def test_incomplete_coefficients_rejected(self):
        with self.assertRaises(ValueError):
            DELTA([0] * 129, [0] * 130)


if __name__ == "__main__":
    unittest.main()
