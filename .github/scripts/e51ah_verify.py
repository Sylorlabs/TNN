"""Verify native E51AH evidence without implementing or changing cognition."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys


def verify(root: Path) -> dict:
    errors = []
    raw_path = root / "RAW.log"
    raw = raw_path.read_text()
    rows = list(csv.reader(raw.splitlines()))

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    def one(key: str) -> list:
        found = [row[1:] for row in rows if row and row[0] == key]
        if len(found) != 1:
            raise ValueError(f"expected one {key} row, found {len(found)}")
        return found[0]

    def number(key: str) -> int:
        values = one(key)
        if len(values) != 1:
            raise ValueError(f"expected scalar {key}")
        return int(values[0])

    def table(key: str) -> dict:
        found = {}
        for row in rows:
            if row and row[0] == key:
                values = list(map(int, row[1:]))
                if values[0] in found:
                    raise ValueError(f"duplicate {key} arm {values[0]}")
                found[values[0]] = values[1:]
        return found

    for name in ("SOURCE_PIN_GATE.txt", "BYTE_IDENTICAL.txt"):
        check((root / name).read_text().strip() == "1", f"{name} did not pass")
    check((root / "EXIT_CODE.txt").read_text().strip() == "0", "native exit was nonzero")
    check((root / "NATIVE_BUILD_1").read_bytes() == (root / "NATIVE_BUILD_2").read_bytes(),
          "native builds differ")
    check(raw.splitlines().count("TNN_R32_E51AH_EXECUTION_COMPLETE=1") == 1,
          "missing or duplicate native completion marker")

    required_gates = (
        "e50_seed_preflight_gate", "e50_batch_statistics_gate",
        "e50_batch_forward_reverse_identity_gate", "e50_batch_convergence_gate",
        "e50_aux_frozen_gate", "e51y_parent_e50_integrity_gate",
        "e51ah_world_partition_gate", "e51ah_domain_gate",
        "e51ah_direct_global_identity_gate", "e51ah_direct_local_identity_gate",
        "e51ah_direct_target_support_gate", "e51ah_direct_integrity_gate",
        "e51ah_support_gate", "e51ah_parent_global_identity_gate",
        "e51ah_count_matched_identity_gate", "e51ah_replay_target_support_gate",
        "e51ah_replay_kind_coverage_gate", "e51ah_replay_global_identity_gate",
        "e51ah_replay_local_identity_gate", "e51ah_replay_local_strict_gate",
        "e51ah_frozen_training_gate", "e51ah_pre_validation_integrity_gate",
        "e51ah_validation_integrity_gate", "e51ah_confirmation_integrity_gate",
        "e51ah_residual_frozen_gate", "e51ah_frozen_final_gate", "e51ah_integrity_gate",
    )
    for key in required_gates:
        check(number(key) == 1, f"failed gate: {key}")
    check(list(map(int, one("e51y_terminal_reproduction"))) == [4200, 4200, 1200, 1200, 1],
          "terminal reproduction mismatch")
    check(number("e51ah_world_assignment_failures") == 0, "world assignment failure")
    check(number("e51ah_development_episodes") == 12960, "wrong development count")
    replay = list(map(int, one("e51ah_replay_set")))
    check(len(replay) == 14 and replay[0] == 12960 and replay[3] == 1,
          "replay count or isolation mismatch")
    check(number("e51ah_terminal_hash_before") == number("e51ah_terminal_hash_after_training"),
          "mature terminal hash changed")
    check(number("e51ah_direct_hash_before") == number("e51ah_direct_hash_after_training"),
          "direct hash changed")

    development = table("e51ah_development_arm")
    check(set(development) == {1, 2, 3, 4}, "wrong development arms")
    union = number("e51ah_frozen_union_development")
    for arm, values in development.items():
        check(len(values) == 4, f"wrong development columns for arm {arm}")
        preserve, rescue, _, gate = values
        check(0 <= preserve <= union and 0 <= rescue <= 12960 - union,
              f"development counts out of bounds: arm {arm}")
        check(gate == int(preserve == union and rescue > 0), f"development gate mismatch: arm {arm}")
    eligible = [arm for arm in (3, 4) if development[arm][3] == 1]
    opened = number("e51ah_development_open_gate")
    check(opened == int(bool(eligible)), "opening gate disagrees with development")
    validation_count = number("e51ah_validation_executed")
    confirmation_count = number("e51ah_sealed_confirmation_executed")
    validation = table("e51ah_validation")
    confirmation = table("e51ah_confirmation")
    outcome = one("e51ah_outcome")[0]
    expected_outcome = "PRESERVATION_REPLAY_DEVELOPMENT_FAILURE"

    if not eligible:
        check(validation_count == 0 and not validation, "validation exposed after failed development")
        check(confirmation_count == 0 and not confirmation, "confirmation exposed after failed development")
    else:
        check(validation_count == 5400 and set(validation) == set(range(6)), "incomplete validation")
        paired = table("e51ah_validation_paired")
        for arm, values in validation.items():
            n, reach, known, kr, nu, nr, t0s, t0u, t0w = values
            check(n == 5400 and known == 4200 and nu == 1200, f"population mismatch: {arm}")
            check(reach == kr + nr and 0 <= kr <= known and 0 <= nr <= nu, f"reachability mismatch: {arm}")
            if arm in (1, 2, 3, 4):
                check(t0s + t0u + t0w == n, f"state-zero accounting mismatch: {arm}")
            if arm:
                gain, loss = paired[arm]
                check(reach - validation[0][1] == gain - loss, f"paired accounting mismatch: {arm}")
        selected = eligible[0]
        check(number("e51ah_selected_replay_arm") == selected, "winner was not selected on development")
        candidate, control = validation[selected], validation[0]
        exact = candidate[1:6] == [5400, 4200, 4200, 1200, 1200]
        pareto = (candidate[1] > control[1] and candidate[3] > control[3]
                  and candidate[5] >= control[5] and paired[selected][1] == 0)
        tradeoff = ((candidate[3] > control[3] and candidate[5] < control[5])
                    or (candidate[3] < control[3] and candidate[5] > control[5]))
        if exact:
            check(number("e51ah_exact_winner_arm") == selected, "wrong exact winner")
            check(confirmation_count == 10800 and set(confirmation) == {selected}, "incomplete confirmation")
            result = confirmation[selected]
            conf_exact = result[:6] == [10800, 10800, 8400, 8400, 2400, 2400]
            expected_outcome = ("PRESERVATION_REPLAY_EXACT_CONFIRMED" if conf_exact
                                else "PRESERVATION_REPLAY_EXACT_NOT_CONFIRMED")
        else:
            check(confirmation_count == 0 and not confirmation, "confirmation exposed without exact selected arm")
            expected_outcome = ("PRESERVATION_REPLAY_PARETO_IMPROVEMENT" if pareto else
                                "PRESERVATION_REPLAY_TRADEOFF" if tradeoff else
                                "PRESERVATION_REPLAY_NO_GAIN")
    check(outcome == expected_outcome, "native outcome disagrees with frozen decision rules")
    for entry in json.loads((root / "TRANSITIVE_SOURCE_MANIFEST.json").read_text())["files"]:
        data = (root / "transitive_source" / entry["path"]).read_bytes()
        check(hashlib.sha256(data).hexdigest() == entry["sha256"], f"parent source bytes differ: {entry['path']}")
    return {"schema_version": 1, "verified": not errors, "errors": errors,
            "outcome": outcome, "development_arms": development,
            "validation_executed": validation_count, "confirmation_executed": confirmation_count,
            "sha256": {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                       for name in ("RAW.log", "SUMMARY.log", "NATIVE_BUILD_1", "NATIVE_BUILD_2",
                                    "tnn_r32_e51ah_grounded_preservation_replay.zag")}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(".scratch/e51ah"))
    args = parser.parse_args()
    try:
        report = verify(args.root)
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        report = {"schema_version": 1, "verified": False, "errors": [str(exc)]}
    (args.root / "EVIDENCE_CHECK.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["verified"] else 1)
