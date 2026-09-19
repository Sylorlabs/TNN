"""Synthetic external format/oracle tests; these never execute the native codec."""
import copy
import unittest

from r33_validate import ContractError, load_json, parse_b000_output
from r33_c01 import CONFIG, check_inventory, expanded_config


class ComponentContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_json(CONFIG)
        cls.expanded = expanded_config(cls.config)
        rows = [f"M,{key},{value}" for key, value in cls.expanded["expected_metrics"].items()]
        rows.extend(f"V,{key},{i},{value}" for key, values in cls.expanded["expected_vectors"].items()
                    for i, value in enumerate(values))
        cls.synthetic_csv = "\n".join(rows) + "\n"

    def test_inventory(self):
        self.assertEqual(check_inventory(), {"metrics": 77, "vectors": 40, "vector_elements": 77986})

    def test_all_signed_code_reference(self):
        values = self.expanded["expected_vectors"]["pcm.all_i16_codes"]
        self.assertEqual([values[i] for i in (0, 32767, 32768, 65535)], [0, 32767, -32768, -1])
        self.assertEqual(len(set(values)), 65536)

    def test_pixel_reference(self):
        values = self.expanded["expected_vectors"]["vision.maximum_pixels"]
        self.assertEqual(len(values), 64 * 64 * 3)
        self.assertEqual(values[:3], [11, 40, 69])
        self.assertTrue(all(0 <= x <= 255 for x in values))

    def test_oracle_no_mutation(self):
        before = copy.deepcopy(self.config)
        expanded_config(self.config)
        self.assertEqual(before, self.config)

    def test_unknown_oracle_rejected(self):
        bad = copy.deepcopy(self.config)
        bad["generated_expected_vectors"]["pcm.all_i16_codes"]["rule"] = "HIDE_NEGATIVES"
        with self.assertRaises(ContractError): expanded_config(bad)

    def test_synthetic_output_format(self):
        result = parse_b000_output(self.synthetic_csv, self.expanded)
        self.assertFalse(result["mismatched_keys"])

    def test_duplicate_value_rejected(self):
        bad = self.synthetic_csv + "V,pcm.all_i16_codes,0,0\n"
        with self.assertRaises(ContractError): parse_b000_output(bad, self.expanded)

    def test_one_signed_error_visible(self):
        bad = self.synthetic_csv.replace("V,pcm.all_i16_codes,32768,-32768\n", "V,pcm.all_i16_codes,32768,32768\n")
        result = parse_b000_output(bad, self.expanded)
        self.assertEqual(result["mismatched_keys"], ["pcm.all_i16_codes"])

    def test_one_pixel_error_visible(self):
        bad = self.synthetic_csv.replace("V,vision.maximum_pixels,0,11\n", "V,vision.maximum_pixels,0,12\n")
        result = parse_b000_output(bad, self.expanded)
        self.assertEqual(result["mismatched_keys"], ["vision.maximum_pixels"])

    def test_missing_record_rejected(self):
        bad = self.synthetic_csv.replace("V,pcm.all_i16_codes,65535,-1\n", "")
        with self.assertRaises(ContractError): parse_b000_output(bad, self.expanded)

    def test_incomplete_run_rejected(self):
        bad = self.synthetic_csv.replace("M,audit.completed,1\n", "")
        with self.assertRaises(ContractError): parse_b000_output(bad, self.expanded)

    def test_outside_i32_rejected(self):
        bad = self.synthetic_csv.replace("V,pcm.all_i16_codes,0,0\n", "V,pcm.all_i16_codes,0,2147483648\n")
        with self.assertRaises(ContractError): parse_b000_output(bad, self.expanded)


if __name__ == "__main__":
    unittest.main(verbosity=2)
