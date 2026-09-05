"""Synthetic independent-arithmetic checks; not experimental observations."""
from pathlib import Path
import random
import runpy
import tempfile
import unittest

V = runpy.run_path(str(Path(__file__).with_name("derive.py")))


class RetentionTests(unittest.TestCase):
    def test_loss_regain_and_never_lost(self):
        result = V["retention_masks"](0b011, [0b110, 0b101])
        self.assertEqual([result[k] for k in ("anchor_successes", "ever_lost", "regained_at_final", "missing_at_final", "never_lost")], [2,2,1,1,0])

    def test_final_recovery_does_not_erase_loss(self):
        result = V["retention_masks"](1, [0,1])
        self.assertEqual(result["ever_lost"],1)
        self.assertEqual(result["never_lost"],0)
        self.assertEqual(result["missing_at_final"],0)

    def test_empty_anchor_not_full_retention(self):
        self.assertIsNone(V["retention_masks"](0,[1])["final_retained_fraction"])

    def test_missing_horizon_rejected(self):
        with self.assertRaises(ValueError):
            V["retention_masks"](1,[])

    def test_new_gains_not_retention(self):
        result = V["retention_masks"](1,[7])
        self.assertEqual(result["never_lost"],1)
        self.assertEqual(result["anchor_successes"],1)

    def test_paired_strata(self):
        result = V["paired_masks"](0b1010,0b0101,0b0011)
        self.assertEqual(result,{"paired_lost":2,"paired_rescued":2,"paired_net":0,
                                 "known_lost":1,"known_rescued":1,"no_unique_lost":1,"no_unique_rescued":1})

    def test_initial_unknown_and_anchor_accounting(self):
        masks = dict(zip(V["MASK_FIELDS"],(0b101,0b111,0b011,0b011,0b001,0b010,0b100,0b011)))
        result = V["metrics_from_masks"](masks,32)
        self.assertEqual([result[k] for k in V["FIELDS"]],[2,1,1,3,1,0,2,1,1,1,1,1,1,1])
        baseline = V["metrics_from_masks"](masks,-1)
        self.assertEqual((baseline["anchor_lost"],baseline["anchor_gained"]),(0,0))

    def test_duplicate_json_rejected(self):
        with self.assertRaises(ValueError):
            V["unique_json"]([("a",1),("a",2)])

    def test_malformed_native_episode_rejected(self):
        with self.assertRaisesRegex(ValueError,"width"):
            V["parse_masks"](b"e51aj_episode,0,0,0\n")

    def test_duplicate_native_episode_rejected(self):
        row = b"e51aj_episode,0,0,0,0,0,1,1,1,1,1,0,0,1\n"
        with self.assertRaisesRegex(ValueError,"duplicate native episode"):
            V["parse_masks"](row+row)

    def test_random_matrices_against_direct_row_arithmetic(self):
        rng = random.Random(71903)
        for _ in range(100):
            anchor = [rng.randrange(2) for _ in range(20)]
            rows = [[rng.randrange(2) for _ in anchor] for _ in range(8)]
            def bits(values):
                return sum(value << i for i,value in enumerate(values))
            result = V["retention_masks"](bits(anchor),[bits(row) for row in rows])
            selected = [i for i,value in enumerate(anchor) if value]
            ever = [i for i in selected if any(row[i] == 0 for row in rows)]
            self.assertEqual(result["ever_lost"],len(ever))
            self.assertEqual(result["never_lost"],sum(all(row[i] == 1 for row in rows) for i in selected))
            self.assertEqual(result["regained_at_final"],sum(rows[-1][i] for i in ever))
            self.assertEqual(result["missing_at_final"],sum(rows[-1][i] == 0 for i in selected))
            self.assertEqual(result["worst_simultaneous_loss"],max(sum(row[i] == 0 for i in selected) for row in rows))

    def test_full_shape_raw_mask_parser(self):
        repo = Path(__file__).resolve().parents[2]
        fixture = runpy.run_path(str(repo/".github/scripts/e51aj_verify_test.py"))["full_fixture"]
        with tempfile.TemporaryDirectory(prefix="e51aj-INDEPENDENT-SYNTHETIC-") as directory:
            root = Path(directory)
            fixture(root)
            groups = V["parse_masks"]((root/"RAW.log").read_bytes())
            self.assertEqual(len(groups),510)
            for (rep,cp,arm), masks in groups.items():
                result = V["metrics_from_masks"](masks,cp)
                self.assertEqual(result["reachable"],2160)
                self.assertEqual(result["known"],1680)
                self.assertEqual(result["no_unique"],480)
                self.assertEqual(result["anchor_lost"],0)


if __name__ == "__main__":
    unittest.main()
