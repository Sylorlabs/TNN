"""Synthetic arithmetic, scheduling and full-shape evidence tests, not research data."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import runpy
import tempfile
import unittest

V = runpy.run_path(str(Path(__file__).with_name("e51aj_verify.py")))


class ArithmeticTests(unittest.TestCase):
    def test_exact_multisets_every_cycle(self):
        for cycle in range(8):
            for arm in range(4):
                counts = Counter(V["sample"](arm,b,p) for b in range(cycle*4,cycle*4+4) for p in range(1080))
                expected = Counter({row: 8 if arm == 3 else 2 for row in range(540 if arm == 3 else 2160)})
                self.assertEqual(counts, expected)

    def test_replay_current_half(self):
        for block in range(32):
            self.assertEqual([V["sample"](1,block,p) for p in range(540)], list(range((block%4)*540,(block%4+1)*540)))

    def test_bad_schedule_indices(self):
        for args in ((4,0,0), (0,32,0), (0,0,1080), (-1,0,0)):
            with self.assertRaises(ValueError):
                V["sample"](*args)

    def test_pointwise_regain_not_never_lost(self):
        result = V["retention"]([1,1,0], [[0,1,1],[1,0,1]])
        self.assertEqual([result[k] for k in ("ever_lost","regained_at_final","missing_at_final","never_lost")], [2,1,1,0])

    def test_empty_anchor(self):
        self.assertIsNone(V["retention"]([0], [[1]])["final_retained_fraction"])

    def test_bad_retention_rows(self):
        for anchor, rows in (([1],[]), ([1],[[2]]), ([1,1],[[1]])):
            with self.assertRaises(ValueError):
                V["retention"](anchor,rows)

    def test_strict_loss(self):
        V["check_fit"]([1,10,9,1])
        V["check_fit"]([0,10,10,1])
        for bad in ([1,10,10,1], [0,10,9,1], [1,9,10,1], [261,1000,0,1], [1,10,0,0]):
            with self.assertRaises(ValueError):
                V["check_fit"](bad)

    def test_known_and_initial_decision_accounting(self):
        rows = [(1,1,1,int(i<420),1,0,0,1) for i in range(540)]
        self.assertEqual(V["summarize"](rows), [540,420,120,540,0,0,540,0,0,0,0,540,0,0])
        rows[0] = (1,1,1,1,1,1,0,1)
        with self.assertRaises(ValueError):
            V["summarize"](rows)

    def test_primary_retention_does_not_hide_behavioral_tradeoff(self):
        arms = {str(a):{"retention":{"anchor_successes":100,"missing_at_final":10-a,"ever_lost":12-a,"worst_simultaneous_loss":11-a},
                        "final":{key:50 for key in V["FIELDS"]}} for a in (0,1)}
        arms["1"]["final"]["known"] = 49
        result = V["primary"](arms)
        self.assertTrue(result["retention_direction"])
        self.assertFalse(result["no_final_behavioral_tradeoff"])

    def test_primary_worst_loss_cannot_be_hidden(self):
        arms = {str(a):{"retention":{"anchor_successes":100,"missing_at_final":10-a,"ever_lost":12-a,"worst_simultaneous_loss":11+a},
                        "final":{key:50 for key in V["FIELDS"]}} for a in (0,1)}
        self.assertFalse(V["primary"](arms)["retention_direction"])
        arms["1"]["retention"]["anchor_successes"] = 99
        with self.assertRaises(ValueError):
            V["primary"](arms)


def full_fixture(root):
    """A deliberately artificial, all-success, unchanged-weight ledger."""
    def save(name, text):
        p = root/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(text)
    source = "SYNTHETIC FIXTURE ONLY; THIS IS NOT ZAG OR EXPERIMENTAL EVIDENCE\n"
    source_sha = hashlib.sha256(source.encode()).hexdigest()
    save("SOURCE.zag",source)
    save("EXIT_CODE.txt","0\n")
    save("SOURCE_PIN_GATE.txt","1\n")
    save("BYTE_IDENTICAL.txt","1\n")
    save("NATIVE_BUILD_1","SYNTHETIC_NOT_EXECUTABLE")
    save("NATIVE_BUILD_2","SYNTHETIC_NOT_EXECUTABLE")
    save("COMPILER_SHA256SUMS.txt",V["COMPILER"]+"  SYNTHETIC_IDENTITY_ONLY\n")
    save("preflight/RESULT.log","E51AJ_SYNTHETIC_SELFTESTS_PASS=1\n")
    pin_path = "Research/R32_E51AJ_SOURCE_PIN.json"
    pin = json.dumps({"source_sha256":source_sha})
    save("inputs/"+pin_path,pin)
    save("SOURCE_MANIFEST.json",json.dumps({"parent_scientific_commit":V["PARENT"],"source_sha256":source_sha,
         "files":[{"path":pin_path,"sha256":hashlib.sha256(pin.encode()).hexdigest(),
                   "git_blob":hashlib.sha1(b"blob "+str(len(pin)).encode()+b"\0"+pin.encode()).hexdigest()}]}))
    save("RUN_EXECUTION.json",json.dumps({"exit_code":0,"timed_out":False,"wall_seconds":1,
                                         "max_address_space_bytes":2*1024**3,"max_output_file_bytes":1024**3}))
    model_hash = V["hash_values"]([0]*130)
    panel_hash = V["hash_values"]([0]*650)
    schedules = {(a,b):[V["sample"](a,b,p) for p in range(1080)] for a in range(4) for b in range(32)}
    with (root/"RAW.log").open("w",newline="") as stream:
        writer = csv.writer(stream,lineterminator="\n")
        def row(*values):
            writer.writerow(values)
        def model(rep,phase,cp,arm):
            row("e51aj_model",rep,phase,cp,arm,model_hash)
            for c in range(130):
                row("e51aj_weight",rep,phase,cp,arm,c,0)
        for gate in ("e50_seed_preflight_gate","e50_batch_statistics_gate","e50_batch_forward_reverse_identity_gate","e50_batch_convergence_gate","e50_aux_frozen_gate","e51y_parent_e50_integrity_gate","e51aj_world_gate","e51aj_schedule_gate","e51aj_direct_integrity_gate"):
            row(gate,1)
        row("e51y_terminal_reproduction",4200,4200,1200,1200,1)
        for stage in range(119,143):
            row("e51aj_stage",stage,stage*1000000,stage*1000000+539)
        for rep in range(3):
            for dataset in range(8):
                row("e51aj_dataset",rep,dataset,119+rep*8+dataset,540,0,540 if dataset<4 else 0,0)
                if dataset<4:
                    for ep in range(540):
                        row("e51aj_training_record",rep,dataset,ep,*([0]*67))
            row("e51aj_feature_isolation_gate",1)
            row("e51aj_dataset_integrity_gate",1)
            for phase in (0,1):
                for cp in range(1,5 if phase==0 else 33):
                    for arm in range(1 if phase==0 else 4):
                        sequence = schedules[(arm,cp-1)]
                        counts = [sum(x//540==j for x in sequence) for j in range(4)]
                        row("e51aj_exposure",rep,phase,cp,arm,*counts,V["hash_values"](sequence),1)
                        for candidate in range(2):
                            row("e51aj_fit",rep,phase,cp,arm,candidate,0,0,0,1)
                        row("e51aj_continuity",rep,phase,cp,arm,model_hash,model_hash)
                        if phase==0:
                            model(rep,phase,cp,arm)
            row("e51aj_fork",rep,model_hash)
            for cp in range(-1,33):
                for arm in range(5):
                    model(rep,1,cp,arm)
                    for cohort in range(4):
                        for ep in range(540):
                            row("e51aj_episode",rep,cp,arm,cohort,ep,1,1,1,int(ep<420),1,0,0,1 if cp>=0 else -1)
                        row("e51aj_metrics",rep,cp,arm,cohort,540,420,120,540,0,0,540,0,0,0,0,540,0,0)
                row("e51aj_panel",rep,cp,panel_hash,panel_hash,1)
            row("e51aj_replica_complete",rep,32,1)
        row("e51aj_terminal_hash_final",238967492)
        row("e51aj_direct_hash_final",1790306570)
        row("e51aj_replicas_completed",3)
        row("e51aj_validation_executed",0)
        row("e51aj_confirmation_executed",0)
        row("e51aj_integrity_gate",1)
        row("e51aj_outcome","REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE")
        row("TNN_R32_E51AJ_EXECUTION_COMPLETE=1")


class FullShapeTests(unittest.TestCase):
    def test_full_shape_and_duplicate_rejection(self):
        with tempfile.TemporaryDirectory(prefix="e51aj-SYNTHETIC-ONLY-") as directory:
            root = Path(directory)
            full_fixture(root)
            result = V["verify"](root)
            self.assertTrue(result["verified"])
            self.assertEqual(result["probe_episode_rows_verified"],1101600)
            self.assertEqual(result["retention_result"],"MIXED_OR_UNREPLICATED_RETENTION_DIRECTION")
            self.assertEqual(result["replicas"]["0"]["arms"]["0"]["parameter_changing_blocks"],0)
            with (root/"RAW.log").open("a") as stream:
                stream.write("e51aj_fork,0,0\n")
            with self.assertRaisesRegex(ValueError,"duplicate fork"):
                V["verify"](root)


if __name__ == "__main__":
    unittest.main()
