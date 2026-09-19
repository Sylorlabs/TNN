"""Synthetic rendering checks; counts below are not experimental observations."""
from pathlib import Path
import runpy
import unittest

T = runpy.run_path(str(Path(__file__).with_name("tables.py")))


class TableTests(unittest.TestCase):
    def test_markdown_escapes_cells_and_formats_boolean(self):
        rendered = T["markdown_table"](["Value", "Flag"], [["a|b\nc", False]])
        self.assertIn("| a\\|b c | no |", rendered)
        self.assertEqual(len(rendered.splitlines()), 3)

    def test_primary_includes_every_replica_and_failed_direction(self):
        replicas = {}
        for rep in range(3):
            sequential = {"anchor_successes": 10, "missing_at_final": rep+2,
                          "ever_lost": 8, "worst_simultaneous_loss": 6}
            replay = {"missing_at_final": rep+1, "ever_lost": 7,
                      "worst_simultaneous_loss": 5}
            replicas[str(rep)] = {"arms": {"0": {"retention": sequential},
                                            "1": {"retention": replay}},
                                  "primary": {"retention_direction": rep != 2}}
        rendered = T["primary_table"]({"replicas": replicas})
        self.assertEqual(len(rendered.splitlines()), 5)
        self.assertIn("| 0 | 10 | 2 | 1 | 8 / 7 | 6 / 5 | yes |", rendered)
        self.assertIn("| 2 | 10 | 4 | 3 | 8 / 7 | 6 / 5 | no |", rendered)

    def test_missing_replica_is_not_silently_omitted(self):
        with self.assertRaises(KeyError):
            T["primary_table"]({"replicas": {}})


if __name__ == "__main__":
    unittest.main()
