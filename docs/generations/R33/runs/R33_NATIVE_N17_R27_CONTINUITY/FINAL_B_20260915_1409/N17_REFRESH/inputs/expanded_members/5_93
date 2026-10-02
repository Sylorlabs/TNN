"""Synthetic verifier fixtures only; not scientific experiment evidence."""
import ast
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("e51ah_verifier", HERE / "e51ah_verify.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
tree = ast.parse((HERE / "e51ah_verify.py").read_text())
GATES = next(ast.literal_eval(node.value) for node in ast.walk(tree)
             if isinstance(node, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == "required_gates" for t in node.targets))


def fixture(root: Path, opened: bool = False, exact: bool = False) -> None:
    scalars = {key: 1 for key in GATES}
    scalars.update({
        "e51ah_world_assignment_failures": 0, "e51ah_development_episodes": 12960,
        "e51ah_terminal_hash_before": 123, "e51ah_terminal_hash_after_training": 123,
        "e51ah_direct_hash_before": 456, "e51ah_direct_hash_after_training": 456,
        "e51ah_frozen_union_development": 12000, "e51ah_development_open_gate": int(opened),
        "e51ah_validation_executed": 5400 if opened else 0,
        "e51ah_sealed_confirmation_executed": 10800 if exact else 0,
        "e51ah_selected_replay_arm": 3 if opened else -1,
        "e51ah_exact_winner_arm": 3 if exact else -1,
    })
    lines = [f"{key},{value}" for key, value in scalars.items()]
    lines += ["e51y_terminal_reproduction,4200,4200,1200,1200,1",
              "e51ah_replay_set,12960,101,102,1,6480,6480,0,6480,6480,0,11900,100,959,1",
              "TNN_R32_E51AH_EXECUTION_COMPLETE=1"]
    for arm in (1, 2, 3, 4):
        eligible = int(opened and arm in (3, 4))
        lines.append(f"e51ah_development_arm,{arm},{12000 if eligible else 11999},1,0,{eligible}")
    if opened:
        for arm in range(6):
            # Arm 4 is descriptively exact even when selected arm 3 is not.
            known = 4200 if arm in (4, 5) or (arm == 3 and exact) else 3800
            lines.append(f"e51ah_validation,{arm},5400,{known+1200},4200,{known},1200,1200,1000,4000,400")
            if arm:
                lines.append(f"e51ah_validation_paired,{arm},{known-3800},0")
    if exact:
        lines.append("e51ah_confirmation,3,10800,10800,8400,8400,2400,2400,2000,8000,800")
    outcome = ("PRESERVATION_REPLAY_EXACT_CONFIRMED" if exact else
               "PRESERVATION_REPLAY_NO_GAIN" if opened else
               "PRESERVATION_REPLAY_DEVELOPMENT_FAILURE")
    lines.append(f"e51ah_outcome,{outcome}")
    (root / "RAW.log").write_text("\n".join(lines) + "\n")
    (root / "SUMMARY.log").write_text("Synthetic test fixture, not a native experimental result.\n")
    for name, value in {"SOURCE_PIN_GATE.txt": "1", "BYTE_IDENTICAL.txt": "1",
                        "EXIT_CODE.txt": "0", "NATIVE_BUILD_1": "fixture-only",
                        "NATIVE_BUILD_2": "fixture-only",
                        "tnn_r32_e51ah_grounded_preservation_replay.zag": "fixture-only",
                        "TRANSITIVE_SOURCE_MANIFEST.json": json.dumps({"files": []})}.items():
        (root / name).write_text(value)


class EvidenceVerifierTests(unittest.TestCase):
    def run_fixture(self, opened=False, exact=False, replacement=None):
        with tempfile.TemporaryDirectory(prefix="e51ah-synthetic-verifier-") as temp:
            root = Path(temp)
            fixture(root, opened, exact)
            if replacement:
                raw = (root / "RAW.log").read_text()
                self.assertIn(replacement[0], raw)
                (root / "RAW.log").write_text(raw.replace(*replacement))
            return module.verify(root)

    def test_development_failure_keeps_partitions_sealed(self):
        self.assertTrue(self.run_fixture()["verified"])

    def test_later_exact_arm_cannot_replace_selected_arm(self):
        self.assertTrue(self.run_fixture(opened=True)["verified"])

    def test_exact_selected_arm_confirmation(self):
        self.assertTrue(self.run_fixture(opened=True, exact=True)["verified"])

    def test_integrity_failure_rejected(self):
        self.assertFalse(self.run_fixture(replacement=("e51ah_integrity_gate,1", "e51ah_integrity_gate,0"))["verified"])

    def test_unauthorized_validation_exposure_rejected(self):
        self.assertFalse(self.run_fixture(replacement=("e51ah_validation_executed,0", "e51ah_validation_executed,5400"))["verified"])

    def test_wrong_selected_arm_rejected(self):
        self.assertFalse(self.run_fixture(opened=True, replacement=("e51ah_selected_replay_arm,3", "e51ah_selected_replay_arm,4"))["verified"])

    def test_wrong_outcome_rejected(self):
        self.assertFalse(self.run_fixture(replacement=("e51ah_outcome,PRESERVATION_REPLAY_DEVELOPMENT_FAILURE", "e51ah_outcome,PRESERVATION_REPLAY_NO_GAIN"))["verified"])


if __name__ == "__main__":
    unittest.main()
