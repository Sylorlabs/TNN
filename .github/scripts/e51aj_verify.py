"""Verify native E51AJ evidence and derive all preregistered contrasts; never fit."""
from __future__ import annotations

from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys

PARENT = "c46fbbf67e1b7d5a19dee7ca1164fc4c5b0eec22"
COMPILER = "498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef"
FIELDS = ("reachable", "known", "no_unique", "union", "union_lost", "union_rescued",
          "hybrid", "hybrid_lost", "hybrid_rescued", "anchor_lost", "anchor_gained",
          "t0success", "t0unknown", "t0wrong")
NAMES = ("sequential", "replay", "balanced_mixture", "continued_A", "frozen_fork")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def hash_values(values):
    result = 9101
    for value in values:
        result = (result * 1000003 + value) % 2147483629
    return result


def sample(arm, block, position):
    require(0 <= arm < 4 and 0 <= block < 32 and 0 <= position < 1080, "invalid schedule index")
    active, cycle = block % 4, block // 4
    if arm == 0:
        return active * 540 + position % 540
    if arm == 3:
        return position % 540
    if arm == 1:
        if position < 540:
            return active * 540 + position
        local = position - 540
        cohort = [j for j in range(4) if j != active][local % 3]
        phase = [j for j in range(4) if j != cohort].index(active)
        return cohort * 540 + ((phase * 180 + local // 3) * 29 + cycle * 97) % 540
    return (position % 4) * 540 + (((block % 2) * 270 + position // 4) * 29 + cycle * 97) % 540


def check_fit(values):
    require(len(values) == 4, "fit width")
    updates, initial, final, identity = values
    require(0 <= updates <= 260 and 0 <= final <= initial and identity == 1, "fit integrity")
    require((updates == 0 and final == initial) or (updates > 0 and final < initial), "strict update loss")


def summarize(rows):
    require(len(rows) == 540 and all(row is not None for row in rows), "incomplete cohort")
    for row in rows:
        require(len(row) == 8 and all(v in (0, 1) for v in row[:7]) and row[7] in (-1, 0, 1), "episode domain")
        require(sum(row[4:7]) == 1, "initial decision accounting")
    require(sum(row[3] for row in rows) == 420, "known population")
    return [sum(r[0] for r in rows), sum(r[0]*r[3] for r in rows), sum(r[0]*(1-r[3]) for r in rows),
            sum(r[1] for r in rows), sum(r[1]*(1-r[0]) for r in rows), sum((1-r[1])*r[0] for r in rows),
            sum(r[2] for r in rows), sum(r[2]*(1-r[0]) for r in rows), sum((1-r[2])*r[0] for r in rows),
            sum(r[7] == 1 and r[0] == 0 for r in rows), sum(r[7] == 0 and r[0] == 1 for r in rows),
            sum(r[4] for r in rows), sum(r[5] for r in rows), sum(r[6] for r in rows)]


def retention(anchor, subsequent):
    require(bool(subsequent) and all(v in (0, 1) for v in anchor), "retention anchor or horizon")
    require(all(len(row) == len(anchor) and all(v in (0, 1) for v in row) for row in subsequent), "retention matrix")
    success = {i for i, v in enumerate(anchor) if v}
    missing_sets = [{i for i in success if row[i] == 0} for row in subsequent]
    ever = set().union(*missing_sets)
    final = missing_sets[-1]
    return {"anchor_successes": len(success), "ever_lost": len(ever), "never_lost": len(success-ever),
            "regained_at_final": len(ever-final), "missing_at_final": len(final),
            "worst_simultaneous_loss": max(map(len, missing_sets)),
            "final_retained_fraction": (len(success)-len(final))/len(success) if success else None}


def primary(arms):
    seq, replay = arms["0"], arms["1"]
    a, b = seq["retention"], replay["retention"]
    require(a["anchor_successes"] == b["anchor_successes"], "unmatched primary anchor")
    direction = (a["anchor_successes"] > 0 and b["missing_at_final"] < a["missing_at_final"]
                 and b["ever_lost"] <= a["ever_lost"] and b["worst_simultaneous_loss"] <= a["worst_simultaneous_loss"])
    no_tradeoff = all(replay["final"][key] >= seq["final"][key] for key in ("reachable", "known", "no_unique", "t0success"))
    no_tradeoff = no_tradeoff and replay["final"]["t0wrong"] <= seq["final"]["t0wrong"]
    return {"retention_direction": direction, "no_final_behavioral_tradeoff": no_tradeoff,
            "replay_minus_sequential_final": {key: replay["final"][key]-seq["final"][key] for key in FIELDS},
            "replay_minus_sequential_retention": {key: b[key]-a[key] for key in ("missing_at_final", "ever_lost", "worst_simultaneous_loss")}}


def verify(root: Path):
    require((root / "EXIT_CODE.txt").read_text().strip() == "0", "native exit nonzero")
    require((root / "SOURCE_PIN_GATE.txt").read_text().strip() == "1", "unfrozen source")
    require((root / "BYTE_IDENTICAL.txt").read_text().strip() == "1", "double build gate")
    require((root / "NATIVE_BUILD_1").read_bytes() == (root / "NATIVE_BUILD_2").read_bytes(), "binary inequality")
    require((root / "COMPILER_SHA256SUMS.txt").read_text().split()[0] == COMPILER, "compiler identity")
    require("E51AJ_SYNTHETIC_SELFTESTS_PASS=1" in (root / "preflight/RESULT.log").read_text().splitlines(), "synthetic preflight")
    manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
    require(manifest["parent_scientific_commit"] == PARENT, "parent lineage")
    require(hashlib.sha256((root / "SOURCE.zag").read_bytes()).hexdigest() == manifest["source_sha256"], "source digest")
    paths = set()
    for entry in manifest["files"]:
        p = Path(entry["path"])
        require(not p.is_absolute() and ".." not in p.parts and str(p) not in paths, "unsafe/duplicate source path")
        paths.add(str(p))
        content = (root / "inputs" / p).read_bytes()
        require(hashlib.sha256(content).hexdigest() == entry["sha256"], f"source input: {p}")
        require(hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest() == entry["git_blob"], f"source blob: {p}")
    pin = json.loads((root / "inputs/Research/R32_E51AJ_SOURCE_PIN.json").read_text())
    require(pin["source_sha256"] == manifest["source_sha256"], "source pin")
    runtime = json.loads((root / "RUN_EXECUTION.json").read_text())
    require(runtime["exit_code"] == 0 and runtime["timed_out"] is False and runtime["wall_seconds"] <= 5400, "execution budget")
    require(runtime["max_address_space_bytes"] == 2*1024**3 and runtime["max_output_file_bytes"] == 1024**3, "resource limits")
    tables = {key: {} for key in ("stage", "dataset", "training_record", "fit", "model", "weight", "continuity", "exposure", "replica_complete", "panel", "fork", "metrics")}
    widths = {"stage": 1, "dataset": 2, "training_record": 3, "fit": 5, "model": 4, "weight": 5,
              "continuity": 4, "exposure": 4, "replica_complete": 1, "panel": 2, "fork": 1, "metrics": 4}
    episodes = {}
    scalars = defaultdict(list)
    complete = 0
    episode_count = 0
    with (root / "RAW.log").open() as stream:
        for row in csv.reader(stream):
            if not row:
                continue
            key = row[0]
            if key == "TNN_R32_E51AJ_EXECUTION_COMPLETE=1":
                complete += 1
            if key == "e51aj_episode":
                values = list(map(int, row[1:]))
                require(len(values) == 13, "episode width")
                rep, cp, arm, cohort, ep = values[:5]
                require(0 <= rep < 3 and -1 <= cp <= 32 and 0 <= arm < 5 and 0 <= cohort < 4 and 0 <= ep < 540, "episode index")
                group = episodes.setdefault((rep, cp, arm, cohort), [None]*540)
                require(group[ep] is None, "duplicate episode")
                group[ep] = tuple(values[5:])
                episode_count += 1
            elif key.startswith("e51aj_") and key[6:] in tables:
                short = key[6:]
                values = list(map(int, row[1:]))
                n = widths[short]
                index = tuple(values[:n])
                require(index not in tables[short], f"duplicate {short}")
                tables[short][index] = values[n:]
            elif key.startswith(("e51aj_", "e50_")) or key in ("e51y_terminal_reproduction", "e51y_parent_e50_integrity_gate"):
                scalars[key].append(row[1:])
            elif key in ("R32_E51AI_NATIVE v1", "R32_E51AH_NATIVE v1"):
                raise ValueError("historical scientific experiment was executed")
    def scalar(key, expected, repeats=1):
        require(scalars[key] == [expected]*repeats, f"scalar gate: {key}")
    for key in ("e50_seed_preflight_gate", "e50_batch_statistics_gate", "e50_batch_forward_reverse_identity_gate", "e50_batch_convergence_gate", "e50_aux_frozen_gate", "e51y_parent_e50_integrity_gate", "e51aj_world_gate", "e51aj_schedule_gate", "e51aj_direct_integrity_gate", "e51aj_integrity_gate"):
        scalar(key, ["1"])
    scalar("e51y_terminal_reproduction", ["4200", "4200", "1200", "1200", "1"])
    scalar("e51aj_feature_isolation_gate", ["1"], 3)
    scalar("e51aj_dataset_integrity_gate", ["1"], 3)
    scalar("e51aj_terminal_hash_final", ["238967492"])
    scalar("e51aj_direct_hash_final", ["1790306570"])
    scalar("e51aj_replicas_completed", ["3"])
    scalar("e51aj_validation_executed", ["0"])
    scalar("e51aj_confirmation_executed", ["0"])
    scalar("e51aj_outcome", ["REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE"])
    require(complete == 1 and episode_count == 1101600 and len(episodes) == 2040, "incomplete experiment")
    expected_counts = {"stage":24, "dataset":24, "training_record":6480, "fit":792, "model":522,
                       "weight":67860, "continuity":396, "exposure":396, "replica_complete":3,
                       "panel":102, "fork":3, "metrics":2040}
    for key, count in expected_counts.items():
        require(len(tables[key]) == count, f"incomplete {key}")
    for stage in range(119, 143):
        require(tables["stage"][(stage,)] == [stage*1000000, stage*1000000+539], "world allocation")
    for rep in range(3):
        require(tables["replica_complete"][(rep,)] == [32, 1], "replica incomplete")
        for dataset in range(8):
            values = tables["dataset"][(rep, dataset)]
            require(len(values) == 5 and values[:4] == [119+rep*8+dataset, 540, 0, 540 if dataset < 4 else 0], "dataset identity")
            if dataset < 4:
                for ep in range(540):
                    record = tables["training_record"][(rep, dataset, ep)]
                    require(len(record) == 67 and 0 <= record[0] <= 16 and all(-4000 <= x <= 4000 for x in record[3:]), "training record")
                    require(record[0] != 0 or all(x == 0 for x in record[35:]), "t0 lag nonzero")
    coefficients = {}
    for index, model in tables["model"].items():
        coeff = [tables["weight"][(*index, c)][0] for c in range(130)]
        require(all(abs(v) <= (4000 if c in (0, 65) else 16000) for c, v in enumerate(coeff)), "coefficient bounds")
        require(model == [hash_values(coeff)], "coefficient hash")
        coefficients[index] = coeff
    exposures = []
    parameter_changes = []
    schedules = {(a, b): [sample(a, b, p) for p in range(1080)] for a in range(4) for b in range(32)}
    for index, values in tables["continuity"].items():
        rep, phase, cp, arm = index
        require(0 <= rep < 3 and phase in (0, 1) and 1 <= cp <= (4 if phase == 0 else 32) and 0 <= arm < (1 if phase == 0 else 4), "training index")
        previous = (rep, phase, cp-1, arm) if (phase == 1 or cp > 1) else (rep, 1, -1, 0)
        old, new = coefficients[previous], coefficients[index]
        require(values == [hash_values(old), hash_values(new)], "warm-start continuity")
        for candidate in range(2):
            check_fit(tables["fit"][(*index, candidate)])
        schedule = schedules[(arm, cp-1)]
        counts = [sum(row//540 == j for row in schedule) for j in range(4)]
        require(tables["exposure"][index] == counts + [hash_values(schedule), 1], "native schedule disagreement")
        exposures.append({"replica":rep, "phase":phase, "checkpoint":cp, "arm":arm, "A":counts[0], "B":counts[1], "C":counts[2], "D":counts[3]})
        parameter_changes.append({"replica":rep, "phase":phase, "checkpoint":cp, "arm":arm,
                                  "changed_coefficients":sum(x != y for x, y in zip(old, new)),
                                  "l1_delta":sum(abs(x-y) for x,y in zip(old,new)),
                                  "accepted_updates":sum(tables["fit"][(*index,c)][0] for c in range(2))})
    curve = []
    matrices = []
    pooled = {}
    for rep in range(3):
        common = coefficients[(rep, 0, 4, 0)]
        require(tables["fork"][(rep,)] == [hash_values(common)], "fork hash")
        for cp in range(-1, 33):
            combined = []
            for arm in range(5):
                coeff = coefficients[(rep, 1, cp, arm)]
                require(cp != -1 or not any(coeff), "initialization")
                require(not (cp == 0 or (arm == 4 and cp > 0)) or coeff == common, "shared fork or frozen arm changed")
                combined.extend(coeff)
                totals = [0]*14
                for cohort in range(4):
                    rows = episodes[(rep, cp, arm, cohort)]
                    calculated = summarize(rows)
                    require(calculated == tables["metrics"][(rep, cp, arm, cohort)], "metric arithmetic")
                    for ep, row in enumerate(rows):
                        baseline = episodes[(rep, -1, 0, cohort)][ep]
                        anchor = episodes[(rep, 0, 0, cohort)][ep]
                        require(row[1:4] == baseline[1:4], "control/population drift")
                        require(row[7] == (anchor[0] if cp >= 0 else -1), "anchor changed")
                        require(cp != -1 or row[0] == row[2], "zero residual not hybrid")
                        require(cp != 0 or row == anchor, "unequal shared anchor")
                        require(not (arm == 4 and cp >= 0) or row == anchor, "static policy drift")
                    totals = [a+b for a,b in zip(totals, calculated)]
                    matrices.append({"replica":rep, "checkpoint":cp, "arm":arm, "cohort":"ABCD"[cohort], **dict(zip(FIELDS, calculated))})
                pooled[(rep, cp, arm)] = totals
                curve.append({"replica":rep, "checkpoint":cp, "arm":arm, "name":NAMES[arm], **dict(zip(FIELDS,totals))})
            require(tables["panel"][(rep, cp)] == [hash_values(combined), hash_values(combined), 1], "evaluation modified weights")
    replicas = {}
    for rep in range(3):
        arms = {}
        anchor = [r[0] for j in range(4) for r in episodes[(rep,0,0,j)]]
        for arm in range(5):
            subsequent = [[r[0] for j in range(4) for r in episodes[(rep,cp,arm,j)]] for cp in range(1,33)]
            retained = retention(anchor, subsequent)
            require(retained["missing_at_final"] == pooled[(rep,32,arm)][9], "retention disagreement")
            changes = [row for row in parameter_changes if row["replica"] == rep and row["phase"] == 1 and row["arm"] == arm]
            arms[str(arm)] = {"name":NAMES[arm], "final":dict(zip(FIELDS,pooled[(rep,32,arm)])),
                              "anchor_metrics":dict(zip(FIELDS,pooled[(rep,0,arm)])),
                              "retention":retained, "parameter_changing_blocks":sum(row["changed_coefficients"] > 0 for row in changes),
                              "accepted_updates":sum(row["accepted_updates"] for row in changes)}
        replicas[str(rep)] = {"arms":arms, "primary":primary(arms)}
    replicated = all(rep["primary"]["retention_direction"] for rep in replicas.values())
    return {"schema_version":1, "verified":True, "errors":[], "experiment":"R32_E51AJ",
            "outcome":"REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE", "parent_source_commit":PARENT,
            "retention_result":"REPLICATED_RETENTION_DIRECTION" if replicated else "MIXED_OR_UNREPLICATED_RETENTION_DIRECTION",
            "no_final_behavioral_tradeoff":all(rep["primary"]["no_final_behavioral_tradeoff"] for rep in replicas.values()),
            "replicas":replicas, "metric_columns":list(FIELDS), "curve":curve, "retention_matrix":matrices,
            "exposure":sorted(exposures,key=lambda r:(r["replica"],r["phase"],r["checkpoint"],r["arm"])),
            "parameter_changes":sorted(parameter_changes,key=lambda r:(r["replica"],r["phase"],r["checkpoint"],r["arm"])),
            "probe_episode_rows_verified":episode_count, "coefficient_rows_verified":67860,
            "source_inputs_verified":len(paths), "native_runtime":runtime,
            "validation_executed":0, "confirmation_executed":0, "canonical_system":"R27", "promotion_allowed":False,
            "sha256":{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ("SOURCE.zag","RAW.log","NATIVE_BUILD_1","NATIVE_BUILD_2")}}


if __name__ == "__main__":
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".scratch/e51aj")
    try:
        result = verify(root)
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        result = {"verified":False, "errors":[f"{type(exc).__name__}: {exc}"]}
    (root/"EVIDENCE_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("curve","retention_matrix","exposure","parameter_changes")},indent=2))
    raise SystemExit(0 if result["verified"] else 1)
