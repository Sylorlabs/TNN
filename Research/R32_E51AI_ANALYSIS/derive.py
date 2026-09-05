"""Derive descriptive tables from verified E51AI evidence, without fitting a learner.

Usage: python3 -B Research/R32_E51AI_ANALYSIS/derive.py ARCHIVE_DIRECTORY OUTPUT_DIRECTORY
ARCHIVE_DIRECTORY contains IDENTITY_CHECK.json, LOCAL_EVIDENCE_CHECK.json, and
extracted/RAW.log. Outputs are deterministic analysis products, not new tests.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

SOURCE = "c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22"
RUN = 33949274757
ARMS = (
    "current_plus_squared",
    "real_history",
    "zero_history",
    "real_history_plus_replay",
)
FIELDS = (
    "reachable", "known", "no_unique", "union", "union_lost", "union_rescued",
    "hybrid", "hybrid_lost", "hybrid_rescued", "anchor_lost", "anchor_gained",
    "t0success", "t0unknown", "t0wrong",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def retention(anchor: list[int], subsequent: list[list[int]]) -> dict:
    """Pointwise descriptive retention; regained at the end is not sustained recovery."""
    require(bool(subsequent), "retention needs a subsequent checkpoint")
    require(all(v in (0, 1) for v in anchor), "nonbinary anchor")
    require(all(len(row) == len(anchor) and all(v in (0, 1) for v in row)
                for row in subsequent), "invalid retention matrix")
    selected = [i for i, hit in enumerate(anchor) if hit]
    ever = [i for i in selected if any(row[i] == 0 for row in subsequent)]
    missing = [i for i in selected if subsequent[-1][i] == 0]
    regained = [i for i in ever if subsequent[-1][i] == 1]
    losses = [sum(row[i] == 0 for i in selected) for row in subsequent]
    require(len(ever) == len(missing) + len(regained), "pointwise accounting failure")
    return {
        "anchor_successes": len(selected),
        "ever_lost": len(ever),
        "never_lost": len(selected) - len(ever),
        "regained_at_final": len(regained),
        "missing_at_final": len(missing),
        "worst_checkpoint_loss": max(losses),
        "final_retained_fraction": (len(selected) - len(missing)) / len(selected) if selected else None,
    }


def csv_bytes(rows: list[dict]) -> bytes:
    require(bool(rows), "empty output table")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def parameter_delta(previous: list[int], current: list[int]) -> dict:
    """Compare actual checkpoint coefficients, not only their compact hashes."""
    require(len(previous) == len(current) == 130, "wrong coefficient vector width")
    difference = [after - before for before, after in zip(previous, current)]
    return {"changed_coefficients": sum(value != 0 for value in difference),
            "coefficient_l1_change": sum(abs(value) for value in difference),
            "largest_coefficient_change": max(abs(value) for value in difference)}


def derive(archive: Path) -> tuple[dict, dict[str, bytes]]:
    identity = json.loads((archive / "IDENTITY_CHECK.json").read_text())
    checked = json.loads((archive / "LOCAL_EVIDENCE_CHECK.json").read_text())
    require(identity.get("verified") is True and checked.get("verified") is True,
            "archive and scientific verification are required")
    require(identity["source_commit"] == SOURCE and identity["run"] == RUN, "wrong source or run")
    raw = (archive / "extracted/RAW.log").read_bytes()
    raw_sha = hashlib.sha256(raw).hexdigest()
    require(raw_sha == identity["sha256"]["RAW.log"] == checked["sha256"]["RAW.log"], "raw ledger changed")
    require(checked["metric_columns"] == list(FIELDS), "unexpected metric schema")
    curve = {(r["checkpoint"], r["arm"]): r["metrics"] for r in checked["curve"]}
    require(len(curve) == 132, "incomplete aggregate curve")
    episodes: dict = {}
    metrics: dict = {}
    model: dict = {}
    fit: dict = {}
    weights: dict = {}
    exposure: dict = {}
    for row in csv.reader(io.StringIO(raw.decode())):
        if not row:
            continue
        key = row[0]
        if key not in ("e51ai_episode", "e51ai_metrics", "e51ai_model", "e51ai_fit",
                       "e51ai_weight", "e51ai_exposure"):
            continue
        values = list(map(int, row[1:]))
        table, width = {
            "e51ai_episode": (episodes, 5), "e51ai_metrics": (metrics, 4),
            "e51ai_model": (model, 2), "e51ai_fit": (fit, 3),
            "e51ai_weight": (weights, 3), "e51ai_exposure": (exposure, 2),
        }[key]
        index = tuple(values[:width])
        require(index not in table, f"duplicate row: {key} {index}")
        table[index] = values[width:]
    require(len(episodes) == 293760 and len(metrics) == 544 and len(model) == 132
            and len(fit) == 256 and len(weights) == 17160 and len(exposure) == 128,
            "incomplete native evidence tables")

    pooled = []
    cohort_rows = []
    retention_rows = []
    update_rows = []
    exposure_rows = []
    shared_anchor_rows = []
    arm_results = {}
    for cp in range(1, 33):
        for arm in range(4):
            previous = [weights[(cp - 1, arm, c)][0] for c in range(130)]
            current = [weights[(cp, arm, c)][0] for c in range(130)]
            change = parameter_delta(previous, current)
            update_rows.append({"checkpoint": cp, "arm": arm, "name": ARMS[arm],
                                "active_cohort": "ABCD"[(cp - 1) % 4], **change,
                                "accepted_coordinate_updates": sum(fit[(cp, arm, c)][0] for c in range(2)),
                                "summed_initial_head_loss": sum(fit[(cp, arm, c)][1] for c in range(2)),
                                "summed_final_head_loss": sum(fit[(cp, arm, c)][2] for c in range(2))})
            counts = exposure[(cp, arm)]
            require(len(counts) == 5 and sum(counts[:4]) == 1080 and counts[4] == 1,
                    "invalid exposure budget")
            exposure_rows.append({"checkpoint": cp, "arm": arm, "name": ARMS[arm],
                                  "active_cohort": "ABCD"[(cp - 1) % 4],
                                  **{f"cohort_{'ABCD'[j]}_presentations": counts[j] for j in range(4)},
                                  "record_presentations": sum(counts[:4]),
                                  "prior_cohort_presentations": sum(counts[:4]) - counts[(cp - 1) % 4]})
    for cp in range(33):
        for arm in range(4):
            total = [sum(metrics[(cp, 0, arm, j)][k] for j in range(4)) for k in range(14)]
            require(total == curve[(cp, arm)], "cohort metrics disagree with verified curve")
            pooled.append({"checkpoint": cp, "arm": arm, "name": ARMS[arm],
                           "training_record_presentations": cp * 1080,
                           "anchored_cohorts": min(cp, 4), **dict(zip(FIELDS, total))})
            for j in range(4):
                observed = metrics[(cp, 0, arm, j)]
                anchor_n = None if cp < j + 1 else sum(episodes[(j + 1, 0, arm, j, e)][0] for e in range(540))
                cohort_rows.append({"checkpoint": cp, "arm": arm, "cohort": "ABCD"[j],
                                    "probe_stage": 115 + j, "anchor_checkpoint": j + 1,
                                    "anchor_successes": anchor_n, **dict(zip(FIELDS, observed))})
    for arm in range(4):
        by_cohort = []
        for j in range(4):
            start = j + 1
            anchor = [episodes[(start, 0, arm, j, e)][0] for e in range(540)]
            subsequent = [[episodes[(cp, 0, arm, j, e)][0] for e in range(540)] for cp in range(start + 1, 33)]
            result = retention(anchor, subsequent)
            require(result["missing_at_final"] == metrics[(32, 0, arm, j)][9], "final anchor loss disagrees")
            first_loss = next((cp for cp in range(start + 1, 33) if metrics[(cp, 0, arm, j)][9] > 0), None)
            first_zero = next((cp for cp in range(first_loss + 1, 33)
                               if metrics[(cp, 0, arm, j)][9] == 0), None) if first_loss is not None else None
            result.update(cohort="ABCD"[j], anchor_checkpoint=start, first_loss_checkpoint=first_loss,
                          first_later_zero_loss_checkpoint=first_zero,
                          zero_loss_checkpoint_trained_same_cohort=None if first_zero is None else (first_zero - 1) % 4 == j)
            retention_rows.append({"arm": arm, "name": ARMS[arm], **result})
            by_cohort.append(result)
        combined = {key: sum(row[key] for row in by_cohort) for key in
                    ("anchor_successes", "ever_lost", "never_lost", "regained_at_final", "missing_at_final")}
        n = combined["anchor_successes"]
        combined["final_retained_fraction"] = (n - combined["missing_at_final"]) / n if n else None
        combined["worst_simultaneous_loss_after_cycle_one"] = max(curve[(cp, arm)][9] for cp in range(4, 33))
        require(combined["missing_at_final"] == curve[(32, arm)][9], "pooled final loss disagrees")
        arm_results[str(arm)] = {
            "name": ARMS[arm], "baseline": dict(zip(FIELDS, curve[(0, arm)])),
            "cycle_one": dict(zip(FIELDS, curve[(4, arm)])),
            "final": dict(zip(FIELDS, curve[(32, arm)])),
            "cycle_one_to_final_delta": {key: curve[(32, arm)][k] - curve[(4, arm)][k]
                                         for k, key in enumerate(FIELDS)},
            "accepted_coordinate_updates": sum(fit[(cp, arm, c)][0] for cp in range(1, 33) for c in range(2)),
            "parameter_changing_blocks": sum(row["changed_coefficients"] > 0
                                             for row in update_rows if row["arm"] == arm),
            "training_record_presentations": sum(row["record_presentations"] for row in exposure_rows if row["arm"] == arm),
            "prior_cohort_presentations": sum(row["prior_cohort_presentations"] for row in exposure_rows if row["arm"] == arm),
            "presentations_by_training_cohort": {"ABCD"[j]: sum(exposure[(cp, arm)][j] for cp in range(1, 33)) for j in range(4)},
            "first_encounter_retention": combined, "cohort_retention": by_cohort,
            "cycle_end_reachability": [curve[(cp, arm)][0] for cp in range(0, 33, 4)],
        }
    final = {str(a): curve[(32, a)] for a in range(4)}
    # Supplemental descriptive comparison on the SAME first-encounter successes.
    # This does not replace the preregistered arm-specific retention summaries.
    for j in range(4):
        start = j + 1
        common = [int(episodes[(start, 0, 1, j, e)][0] == 1 and
                      episodes[(start, 0, 3, j, e)][0] == 1) for e in range(540)]
        for arm in (1, 3):
            subsequent = [[episodes[(cp, 0, arm, j, e)][0] for e in range(540)]
                          for cp in range(start + 1, 33)]
            shared_anchor_rows.append({"arm": arm, "name": ARMS[arm], "cohort": "ABCD"[j],
                                       "anchor_checkpoint": start, **retention(common, subsequent)})
    real = final["1"]
    signal = all(real[0] > final[str(a)][0] and real[1] > final[str(a)][1]
                 and real[2] >= final[str(a)][2] for a in (0, 2)) and real[4] == 0
    require(signal == checked["history_preserving_signal"], "primary signal disagrees")
    summary = {
        "schema_version": 2, "experiment": "R32_E51AI", "run": RUN, "source_commit": SOURCE,
        "artifact_id": identity["artifact_id"], "raw_log_sha256": raw_sha,
        "analysis_status": "DESCRIPTIVE_ARITHMETIC_NOT_NEW_PRIMARY_TEST",
        "history_preserving_signal": signal, "arms": arm_results,
        "shared_first_encounter_replay_contrast": {
            str(arm): {key: sum(row[key] for row in shared_anchor_rows if row["arm"] == arm)
                       for key in ("anchor_successes", "ever_lost", "never_lost",
                                   "regained_at_final", "missing_at_final")}
            for arm in (1, 3)},
        "limitations": [
            "Different cohorts have different first-encounter anchors; the pooled anchor is not one policy checkpoint.",
            "Anchors record observed successes, not a preregistered acquired-competence threshold.",
            "A later zero-loss checkpoint need not follow same-cohort training and does not establish sustained reacquisition.",
            "Regained at final is not uninterrupted retention or sustained recovery.",
            "t0unknown counts unsuccessful UNKNOWN choices; correct UNKNOWN decisions are included in t0success.",
            "Repeated development probes are not independent replications, cross-task transfer, or safe online stopping.",
            "Record presentations, optimizer sweeps, accepted updates, and actual coefficient changes are different quantities.",
            "Fit losses concern the current block's training support; cross-block losses are not one fixed objective curve.",
        ],
    }
    files = {
        "CURVE.csv": csv_bytes(pooled),
        "RETENTION_MATRIX.csv": csv_bytes(cohort_rows),
        "POINTWISE_RETENTION.csv": csv_bytes(retention_rows),
        "CYCLE_ENDS.csv": csv_bytes([r for r in pooled if r["checkpoint"] % 4 == 0]),
        "PARAMETER_CHANGES.csv": csv_bytes(update_rows),
        "EXPOSURE.csv": csv_bytes(exposure_rows),
        "SHARED_ANCHOR_REPLAY.csv": csv_bytes(shared_anchor_rows),
        "SUMMARY.json": (json.dumps(summary, indent=2) + "\n").encode(),
    }
    return summary, files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    summary, files = derive(args.archive.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (args.output / name).write_bytes(data)
    print(json.dumps({"run": RUN, "history_preserving_signal": summary["history_preserving_signal"],
                      "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}, indent=2))
