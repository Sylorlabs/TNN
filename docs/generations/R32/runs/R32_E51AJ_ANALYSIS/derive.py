"""Independently derive E51AJ tables from verified native rows; no cognition.

Usage: python3 -B Research/R32_E51AJ_ANALYSIS/derive.py ARCHIVE_DIRECTORY
Uses integer bit sets to cross-check the frozen verifier's row/matrix arithmetic.
Post-run secondary pointwise decompositions are descriptive, not new primary tests.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path

SOURCE = "9ea141b050599854783258d82cfa3ee02efb1fad"
RUN = 33952427608
ARMS = ("sequential", "replay", "balanced_mixture", "continued_A", "frozen_fork")
FIELDS = ("reachable", "known", "no_unique", "union", "union_lost", "union_rescued",
          "hybrid", "hybrid_lost", "hybrid_rescued", "anchor_lost", "anchor_gained",
          "t0success", "t0unknown", "t0wrong")
MASK_FIELDS = ("hit", "union", "hybrid", "known", "t0success", "t0unknown", "t0wrong", "anchor")
CONTRASTS = ((1, 0), (2, 0), (1, 2), (3, 4))
FULL = (1 << 2160) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_json(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique_json)


def count(mask):
    require(mask >= 0, "negative count mask")
    return bin(mask).count("1")


def retention_masks(anchor, subsequent):
    require(anchor >= 0 and bool(subsequent) and all(m >= 0 for m in subsequent), "invalid retention inputs")
    continuous = anchor
    worst = 0
    for successes in subsequent:
        continuous &= successes
        worst = max(worst, count(anchor & ~successes))
    ever = anchor & ~continuous
    final = subsequent[-1]
    n = count(anchor)
    missing = count(anchor & ~final)
    return {"anchor_successes": n, "ever_lost": count(ever), "never_lost": count(continuous),
            "regained_at_final": count(ever & final), "missing_at_final": missing,
            "worst_simultaneous_loss": worst,
            "final_retained_fraction": (n-missing)/n if n else None}


def metrics_from_masks(masks, checkpoint, subset=FULL):
    hit, union, hybrid, known, t0s, t0u, t0w, anchor = [masks[k] & subset for k in MASK_FIELDS]
    values = (hit, hit & known, hit & ~known, union, union & ~hit, hit & ~union,
              hybrid, hybrid & ~hit, hit & ~hybrid,
              anchor & ~hit if checkpoint >= 0 else 0, hit & ~anchor if checkpoint >= 0 else 0,
              t0s, t0u, t0w)
    return {key: count(mask) for key, mask in zip(FIELDS, values)}


def paired_masks(treatment, control, known):
    lost, gained = control & ~treatment, treatment & ~control
    return {"paired_lost": count(lost), "paired_rescued": count(gained),
            "paired_net": count(gained)-count(lost),
            "known_lost": count(lost & known), "known_rescued": count(gained & known),
            "no_unique_lost": count(lost & ~known), "no_unique_rescued": count(gained & ~known)}


def csv_bytes(rows):
    require(bool(rows), "empty table")
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def parse_masks(raw):
    groups = {}
    seen = {}
    rows = 0
    with io.StringIO(raw.decode()) as stream:
        for row in csv.reader(stream):
            if not row or row[0] != "e51aj_episode":
                continue
            values = list(map(int, row[1:]))
            require(len(values) == 13, "wrong episode width")
            rep, cp, arm, cohort, ep = values[:5]
            require(0 <= rep < 3 and -1 <= cp <= 32 and 0 <= arm < 5 and 0 <= cohort < 4 and 0 <= ep < 540, "episode key outside range")
            outcomes = values[5:]
            require(all(v in (0, 1) for v in outcomes[:7]) and outcomes[7] in (-1, 0, 1), "outcome domain")
            require(sum(outcomes[4:7]) == 1, "initial-choice partition")
            require(outcomes[7] != -1 if cp >= 0 else outcomes[7] == -1, "anchor availability")
            key = (rep, cp, arm)
            bit = 1 << (cohort*540 + ep)
            require(not (seen.get(key, 0) & bit), "duplicate native episode")
            seen[key] = seen.get(key, 0) | bit
            masks = groups.setdefault(key, {name: 0 for name in MASK_FIELDS})
            for name, value in zip(MASK_FIELDS, outcomes):
                if value == 1:
                    masks[name] |= bit
            rows += 1
    require(rows == 1101600 and len(groups) == 510 and all(mask == FULL for mask in seen.values()), "incomplete independent probe matrix")
    return groups


def derive(archive):
    identity = read_json(archive/"IDENTITY_CHECK.json")
    native = read_json(archive/"LOCAL_EVIDENCE_CHECK.json")
    require(identity["verified"] is True and native["verified"] is True, "unverified experiment")
    require(identity["run"] == RUN and identity["source_commit"] == SOURCE, "wrong experiment source")
    raw = (archive/"extracted/RAW.log").read_bytes()
    raw_sha = hashlib.sha256(raw).hexdigest()
    require(raw_sha == identity["sha256"]["RAW.log"] == native["sha256"]["RAW.log"], "raw evidence changed")
    require(native["metric_columns"] == list(FIELDS), "metric schema changed")
    groups = parse_masks(raw)
    frozen_curve = {(r["replica"], r["checkpoint"], r["arm"]): r for r in native["curve"]}
    frozen_cohorts = {(r["replica"], r["checkpoint"], r["arm"], r["cohort"]): r for r in native["retention_matrix"]}
    require(len(frozen_curve) == 510 and len(frozen_cohorts) == 2040, "frozen curve incomplete")
    curve, cohorts, retained_rows, cohort_retained, secondary = [], [], [], [], []
    replicas = {}
    for rep in range(3):
        common = groups[(rep, 0, 0)]
        baseline = groups[(rep, -1, 0)]
        for cp in range(-1, 33):
            for arm in range(5):
                masks = groups[(rep, cp, arm)]
                require(all(masks[k] == baseline[k] for k in ("union", "hybrid", "known")), "control or population drift")
                require(cp < 0 or masks["anchor"] == common["hit"], "common anchor changed")
                require(cp != 0 or masks == common, "fork not identical")
                require(not (arm == 4 and cp >= 0) or masks == common, "frozen policy changed")
                metrics = metrics_from_masks(masks, cp)
                frozen = frozen_curve[(rep, cp, arm)]
                require(metrics == {k: frozen[k] for k in FIELDS}, "independent pooled arithmetic disagrees")
                presentations = 0 if cp == -1 else 4320 + (max(cp, 0)*1080 if arm < 4 else 0)
                curve.append({"replica": rep, "checkpoint": cp, "arm": arm, "name": ARMS[arm],
                              "lineage_record_presentations": presentations, **metrics})
                for cohort in range(4):
                    subset = ((1 << 540)-1) << (cohort*540)
                    calculated = metrics_from_masks(masks, cp, subset)
                    expected = frozen_cohorts[(rep, cp, arm, "ABCD"[cohort])]
                    require(calculated == {k: expected[k] for k in FIELDS}, "independent cohort arithmetic disagrees")
                    cohorts.append({"replica": rep, "checkpoint": cp, "arm": arm, "cohort": "ABCD"[cohort], **calculated})
        arm_summaries = {}
        for arm in range(5):
            panels = [groups[(rep, cp, arm)]["hit"] for cp in range(1, 33)]
            retention = retention_masks(common["hit"], panels)
            expected = native["replicas"][str(rep)]["arms"][str(arm)]
            require(retention == expected["retention"], "independent pooled retention disagrees")
            losses = [count(common["hit"] & ~mask) for mask in panels]
            first_loss = next((cp for cp, loss in enumerate(losses, 1) if loss), None)
            first_zero = next((cp for cp in range(first_loss+1, 33) if losses[cp-1] == 0), None) if first_loss else None
            retained_rows.append({"replica": rep, "arm": arm, "name": ARMS[arm], **retention,
                                  "first_loss_checkpoint": first_loss, "first_later_zero_loss_checkpoint": first_zero,
                                  "worst_loss_checkpoints": " ".join(str(cp) for cp, loss in enumerate(losses, 1) if loss == max(losses))})
            for cohort in range(4):
                subset = ((1 << 540)-1) << (cohort*540)
                values = retention_masks(common["hit"] & subset, [mask & subset for mask in panels])
                cohort_retained.append({"replica": rep, "arm": arm, "name": ARMS[arm], "cohort": "ABCD"[cohort], **values})
            final = metrics_from_masks(groups[(rep, 32, arm)], 32)
            arm_summaries[str(arm)] = {**expected, "retention": retention,
                                      "final_minus_anchor": {k: final[k]-metrics_from_masks(common, 0)[k] for k in FIELDS},
                                      "cycle_end_reachability": [count(groups[(rep, cp, arm)]["hit"]) for cp in range(0, 33, 4)],
                                      "cycle_end_anchor_loss": [count(common["hit"] & ~groups[(rep, cp, arm)]["hit"]) for cp in range(0, 33, 4)]}
        a, b = arm_summaries["0"], arm_summaries["1"]
        seq, replay = a["retention"], b["retention"]
        direction = (seq["anchor_successes"] > 0 and replay["missing_at_final"] < seq["missing_at_final"]
                     and replay["ever_lost"] <= seq["ever_lost"] and replay["worst_simultaneous_loss"] <= seq["worst_simultaneous_loss"])
        no_tradeoff = all(b["final"][k] >= a["final"][k] for k in ("reachable", "known", "no_unique", "t0success")) and b["final"]["t0wrong"] <= a["final"]["t0wrong"]
        primary = native["replicas"][str(rep)]["primary"]
        require(direction == primary["retention_direction"] and no_tradeoff == primary["no_final_behavioral_tradeoff"], "independent primary comparison disagrees")
        replicas[str(rep)] = {"arms": arm_summaries, "primary": primary,
                              "baseline_hybrid": metrics_from_masks(baseline, -1),
                              "common_fork": metrics_from_masks(common, 0)}
        for treatment, control in CONTRASTS:
            t, c = groups[(rep, 32, treatment)], groups[(rep, 32, control)]
            delta = {k: arm_summaries[str(treatment)]["final"][k]-arm_summaries[str(control)]["final"][k] for k in FIELDS}
            paired = paired_masks(t["hit"], c["hit"], common["known"])
            require(paired["paired_net"] == delta["reachable"], "paired final accounting")
            secondary.append({"replica": rep, "treatment_arm": treatment, "control_arm": control,
                              "contrast": ARMS[treatment]+"_minus_"+ARMS[control], **paired,
                              **{"delta_"+k: v for k, v in delta.items()},
                              "t0_successes_lost": count(c["t0success"] & ~t["t0success"]),
                              "t0_successes_rescued": count(t["t0success"] & ~c["t0success"]),
                              "t0_new_wrong_commitments": count(t["t0wrong"] & ~c["t0wrong"]),
                              "t0_wrong_commitments_removed": count(c["t0wrong"] & ~t["t0wrong"])})
    replicated = all(r["primary"]["retention_direction"] for r in replicas.values())
    require(native["retention_result"] == ("REPLICATED_RETENTION_DIRECTION" if replicated else "MIXED_OR_UNREPLICATED_RETENTION_DIRECTION"), "three-replica rule disagrees")
    require(native["no_final_behavioral_tradeoff"] == all(r["primary"]["no_final_behavioral_tradeoff"] for r in replicas.values()), "aggregate behavioral flag disagrees")
    physical_presentations = sum(sum(row[k] for k in "ABCD") for row in native["exposure"])
    require(physical_presentations == 427680 and len(native["exposure"]) == 396 and len(native["parameter_changes"]) == 396, "exposure matrix disagrees")
    summary = {"schema_version": 1, "experiment": "R32_E51AJ", "run": RUN, "source_commit": SOURCE,
               "artifact_id": identity["artifact_id"], "raw_log_sha256": raw_sha,
               "independent_bitset_verification": True, "retention_result": native["retention_result"],
               "no_final_behavioral_tradeoff": native["no_final_behavioral_tradeoff"],
               "replicas": replicas, "physical_record_presentations": physical_presentations,
               "retention_rows": retained_rows, "secondary_final_contrasts": secondary,
               "claim_boundaries": [
                   "This is a controlled E51AJ extension, not an exact E51AI replication.",
                   "Every replica is reported; pooled gains cannot erase a reversal.",
                   "Checkpoint 0 is a shared fixed-dose learned fork, not an acquired-competence threshold.",
                   "Later zero-loss or regained-at-final does not erase earlier losses or establish sustained recovery.",
                   "Exact full-cycle example-multiset matching is not matched intermediate support or actual compute.",
                   "No new trajectories arrive after preparation; these are same-generator populations, not separate tasks.",
                   "Feasible-state reachability, initial decisions and learned online stopping are different claims.",
                   "The aggregate behavioral-tradeoff flag cannot rule out pointwise swaps or cohort-specific harm.",
                   "Secondary pointwise decompositions are descriptive and do not replace the preregistered primary test.",
               ]}
    tables = {"CURVE.csv": curve, "RETENTION_MATRIX.csv": cohorts,
              "BASELINES.csv": [r for r in curve if (r["arm"] == 0 and r["checkpoint"] in (-1, 0)) or (r["arm"] == 4 and r["checkpoint"] == 32)],
              "CYCLE_ENDS.csv": [r for r in curve if r["checkpoint"] >= 0 and r["checkpoint"] % 4 == 0],
              "RETENTION.csv": retained_rows, "COHORT_RETENTION.csv": cohort_retained,
              "SECONDARY_CONTRASTS.csv": secondary, "EXPOSURE.csv": native["exposure"],
              "PARAMETER_CHANGES.csv": native["parameter_changes"]}
    files = {name: csv_bytes(rows) for name, rows in tables.items()}
    files["SUMMARY.json"] = (json.dumps(summary, indent=2)+"\n").encode()
    return summary, files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    summary, files = derive(args.archive.resolve())
    output = Path(__file__).resolve().parent
    for name, content in files.items():
        (output/name).write_bytes(content)
    print(json.dumps({"run": RUN, "retention_result": summary["retention_result"],
                      "no_final_behavioral_tradeoff": summary["no_final_behavioral_tradeoff"],
                      "files": {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}}, indent=2))
