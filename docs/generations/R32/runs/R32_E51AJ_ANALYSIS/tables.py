"""Render all fixed E51AJ comparisons from independently checked summary data.

This module only formats descriptive tables. It never selects a checkpoint,
fits a learner, or changes the preregistered comparison rules.

Usage: python3 -B Research/R32_E51AJ_ANALYSIS/tables.py
"""

from pathlib import Path
import hashlib
import json
import runpy


def markdown_table(headers, rows):
    def cell(value):
        if isinstance(value, bool):
            return "yes" if value else "no"
        return str(value).replace("|", "\\|").replace("\n", " ")
    return "\n".join(
        ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
        + ["| " + " | ".join(cell(value) for value in row) + " |" for row in rows]
    )


def primary_table(summary):
    rows = []
    for rep in range(3):
        result = summary["replicas"][str(rep)]
        seq = result["arms"]["0"]["retention"]
        replay = result["arms"]["1"]["retention"]
        rows.append([rep, seq["anchor_successes"], seq["missing_at_final"], replay["missing_at_final"],
                     f'{seq["ever_lost"]} / {replay["ever_lost"]}',
                     f'{seq["worst_simultaneous_loss"]} / {replay["worst_simultaneous_loss"]}',
                     result["primary"]["retention_direction"]])
    return markdown_table(["Replica", "Shared successes", "Final loss: sequential", "Final loss: replay",
                           "Ever lost: seq / replay", "Worst loss: seq / replay", "Retention direction"], rows)


def tables(summary):
    baseline, final, retention, cycles, secondary = [], [], [], [], []
    for rep in range(3):
        result = summary["replicas"][str(rep)]
        for key, label in (("baseline_hybrid", "Hybrid before residual fitting"), ("common_fork", "Shared learned fork")):
            m = result[key]
            baseline.append([rep, label, m["reachable"], m["known"], m["no_unique"], m["t0success"], m["t0wrong"]])
        for arm in range(5):
            a = result["arms"][str(arm)]
            m, r = a["final"], a["retention"]
            final.append([rep, arm, a["name"], m["reachable"], m["known"], m["no_unique"],
                          m["hybrid_lost"], m["hybrid_rescued"], m["t0success"], m["t0wrong"]])
            retention.append([rep, arm, r["anchor_successes"], r["ever_lost"], r["regained_at_final"],
                              r["missing_at_final"], r["never_lost"], r["worst_simultaneous_loss"],
                              a["parameter_changing_blocks"], a["accepted_updates"]])
        for i, cp in enumerate(range(0, 33, 4)):
            cycles.append([rep, cp] + [result["arms"][str(a)]["cycle_end_reachability"][i] for a in range(5)])
    for r in summary["secondary_final_contrasts"]:
        secondary.append([r["replica"], f'{r["treatment_arm"]} minus {r["control_arm"]}',
                          r["paired_lost"], r["paired_rescued"], r["paired_net"], r["delta_known"],
                          r["delta_no_unique"], r["delta_t0success"], r["delta_t0wrong"]])
    sections = [
        "# E51AJ — Complete fixed-comparison tables",
        f'Source `{summary["source_commit"]}`; run `{summary["run"]}`; artifact `{summary["artifact_id"]}`.',
        "Replica identifiers 0–2 match the native log. Each panel contains 2,160 probes: 1,680 known and 480 no-unique. Counts are not independent replications across checkpoints.",
        "## Primary retention comparison", primary_table(summary),
        "The rule requires all three replicas. These are fixed checkpoint-0 anchors and checkpoint-32 final losses; no favorable checkpoint is substituted.",
        "## Hybrid and shared learned baselines",
        markdown_table(["Replica", "Baseline", "Reachable", "Known", "No-unique", "t=0 success", "t=0 wrong commitment"], baseline),
        "## Every arm at checkpoint 32",
        markdown_table(["Replica", "Arm", "Name", "Reachable", "Known", "No-unique", "Hybrid lost", "Hybrid rescued", "t=0 success", "t=0 wrong commitment"], final),
        "Hybrid losses and rescues concern the zero-residual deployable controller, not the learned shared-fork anchor or the evaluator-only union.",
        "## Pointwise retention and actual continued parameter changes",
        markdown_table(["Replica", "Arm", "Anchor successes", "Ever lost", "Regained at final", "Missing at final", "Never lost", "Worst simultaneous loss", "Changing blocks", "Accepted updates"], retention),
        "Ever lost equals regained at final plus missing at final. Regaining a case does not erase its earlier loss. Frozen arm 4 intentionally has zero continued fitting.",
        "## All eight cycle endpoints, with shared fork",
        markdown_table(["Replica", "Checkpoint", "Sequential", "Replay", "Balanced mixture", "Continued A", "Frozen fork"], cycles),
        "The full intervening checkpoints are retained in CURVE.csv; endpoints are not selected winners.",
        "## Fixed final pointwise contrasts",
        markdown_table(["Replica", "Treatment minus control", "Paired lost", "Paired rescued", "Net reachable", "Delta known", "Delta no-unique", "Delta t=0 success", "Delta t=0 wrong"], secondary),
        "The contrasts are replay vs sequential, mixture vs sequential, replay vs mixture, and A-only vs frozen. Pointwise decompositions are descriptive; the primary rule is unchanged.",
        "Correct UNKNOWN choices are included in t=0 success. The separate t0unknown field in CSVs counts unsuccessful UNKNOWN choices. Feasible-state reachability does not establish a learned online stopping policy.",
    ]
    return ("\n\n".join(sections) + "\n").encode()


if __name__ == "__main__":
    directory = Path(__file__).resolve().parent
    routines = runpy.run_path(str(directory/"derive.py"))
    summary = routines["read_json"](directory/"SUMMARY.json")
    routines["require"](summary["independent_bitset_verification"] is True
                        and summary["run"] == routines["RUN"]
                        and summary["source_commit"] == routines["SOURCE"],
                        "summary is not independently checked E51AJ evidence")
    content = tables(summary)
    output = directory/"TABLES.md"
    output.write_bytes(content)
    print(json.dumps({"file": str(output), "sha256": hashlib.sha256(content).hexdigest()}, indent=2))
