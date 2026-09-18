"""Check native E51AI logs and derive longitudinal metrics, without learner fitting."""
from __future__ import annotations
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys


def require(value, message):
    if not value:
        raise ValueError(message)


def checkpoint_hash(coefficients: list[int]) -> int:
    value = 9101
    for coefficient in coefficients:
        value = (value * 1000003 + coefficient) % 2147483629
    return value


def check_continuity(previous: int, current: int, native: list[int]) -> None:
    require(native == [previous, current], "model reset or continuity failure")


def check_fit(values: list[int]) -> None:
    require(len(values) == 4, "fit row width mismatch")
    updates, initial, final, identity = values
    require(updates >= 0 and 0 <= final <= initial and identity == 1, "fit failed strict loss/identity")


def summarize(rows: list[list[int]]) -> list[int]:
    # hit, union, hybrid, is_known, t0success, t0unknown, t0wrong, anchor
    require(len(rows) == 540, "incomplete probe cohort")
    for r in rows:
        require(len(r) == 8 and all(x in (0,1) for x in r[:7]) and r[7] in (-1,0,1), "bad outcome domain")
        require(sum(r[4:7]) == 1, "t0 accounting mismatch")
    require(sum(r[3] for r in rows) == 420, "known population mismatch")
    return [sum(r[0] for r in rows), sum(r[0]*r[3] for r in rows), sum(r[0]*(1-r[3]) for r in rows),
            sum(r[1] for r in rows), sum(r[1] and not r[0] for r in rows), sum(not r[1] and r[0] for r in rows),
            sum(r[2] for r in rows), sum(r[2] and not r[0] for r in rows), sum(not r[2] and r[0] for r in rows),
            sum(r[7] == 1 and not r[0] for r in rows), sum(r[7] == 0 and r[0] for r in rows),
            sum(r[4] for r in rows), sum(r[5] for r in rows), sum(r[6] for r in rows)]


def verify(root: Path) -> dict:
    require((root / "EXIT_CODE.txt").read_text().strip() == "0", "native exit nonzero")
    require((root / "SOURCE_PIN_GATE.txt").read_text().strip() == "1", "source gate failed")
    require((root / "BYTE_IDENTICAL.txt").read_text().strip() == "1", "build gate failed")
    require((root / "NATIVE_BUILD_1").read_bytes() == (root / "NATIVE_BUILD_2").read_bytes(), "binary inequality")
    require("E51AI_SYNTHETIC_SELFTESTS_PASS=1" in (root / "preflight/RESULT.log").read_text().splitlines(), "preflight failed")
    manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text())
    require(manifest["parent_scientific_commit"] == "c8f62bac285e72653bd6e9412498575ea8036b77", "parent identity mismatch")
    require(hashlib.sha256((root / "SOURCE.zag").read_bytes()).hexdigest() == manifest["source_sha256"], "source SHA mismatch")
    paths = set()
    for entry in manifest["files"]:
        path = Path(entry["path"])
        require(not path.is_absolute() and ".." not in path.parts and str(path) not in paths, "unsafe or duplicate source path")
        paths.add(str(path))
        data = (root / "inputs" / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == entry["sha256"], f"input mismatch: {path}")
    episodes = {}; metrics = {}; fits = {}; models = {}; weights = {}; continuity = {}; exposures = {}; datasets = {}; train = {}; scalars = defaultdict(list)
    complete = 0
    with (root / "RAW.log").open() as stream:
        for row in csv.reader(stream):
            if not row:
                continue
            key = row[0]
            if key == "TNN_R32_E51AI_EXECUTION_COMPLETE=1":
                complete += 1
            if key in ("e51ai_episode", "e51ai_metrics", "e51ai_fit", "e51ai_model", "e51ai_weight", "e51ai_continuity", "e51ai_exposure", "e51ai_dataset", "e51ai_training_record"):
                v = list(map(int, row[1:]))
                table, n = {
                    "e51ai_episode": (episodes,5), "e51ai_metrics": (metrics,4), "e51ai_fit": (fits,3),
                    "e51ai_model": (models,2), "e51ai_weight": (weights,3), "e51ai_continuity": (continuity,2),
                    "e51ai_exposure": (exposures,2), "e51ai_dataset": (datasets,1), "e51ai_training_record": (train,2)
                }[key]
                k = tuple(v[:n]); require(k not in table, f"duplicate {key}: {k}"); table[k] = v[n:]
            elif key.startswith("e51ai_") or key.startswith("e50_") or key == "e51y_parent_e50_integrity_gate" or key == "e51y_terminal_reproduction":
                scalars[key].append(row[1:])
    def one(key):
        require(len(scalars[key]) == 1, f"missing/duplicate {key}")
        return scalars[key][0]
    for name in ("e50_seed_preflight_gate", "e50_batch_statistics_gate", "e50_batch_forward_reverse_identity_gate", "e50_batch_convergence_gate", "e50_aux_frozen_gate", "e51y_parent_e50_integrity_gate",
                 "e51ai_direct_integrity_gate", "e51ai_feature_isolation_gate", "e51ai_dataset_integrity_gate", "e51ai_snapshot_identity_gate", "e51ai_data_frozen_gate", "e51ai_frozen_controllers_gate", "e51ai_integrity_gate"):
        require(one(name) == ["1"], f"failed gate: {name}")
    require(one("e51y_terminal_reproduction") == ["4200","4200","1200","1200","1"], "parent terminal mismatch")
    require(one("e51ai_blocks_completed") == ["32"] and complete == 1, "incomplete longitudinal run")
    require(one("e51ai_validation_executed") == ["0"] and one("e51ai_confirmation_executed") == ["0"], "unexpected qualification exposure")
    require(one("e51ai_terminal_hash_final") == ["238967492"] and one("e51ai_direct_hash_final") == ["1790306570"], "frozen model mismatch")
    require(one("e51ai_outcome") == ["LONGITUDINAL_CONTEXT_DIAGNOSTIC_COMPLETE"], "wrong outcome")
    require(len(datasets) == 8 and len(train) == 2160, "incomplete datasets")
    for d in range(8):
        stage, count, unknown, selected, _ = datasets[(d,)]
        require((stage,count,unknown,selected) == (111+d,540,0,540 if d<4 else 0), "wrong dataset identity")
    for (d,ep), record in train.items():
        require(0<=d<4 and 0<=ep<540 and len(record)==67 and 0<=record[0]<=16, "bad training record")
        require(all(-4000<=x<=4000 for x in record[3:]), "feature bound failed")
        if record[0] == 0:
            require(all(x==0 for x in record[35:]), "nonzero t0 lag")
    require(len(fits)==256 and len(models)==132 and len(weights)==17160 and len(continuity)==128 and len(exposures)==128, "missing fit/checkpoint evidence")
    for cp in range(33):
        for a in range(4):
            coeff = [weights[(cp,a,c)][0] for c in range(130)]
            require(checkpoint_hash(coeff) == models[(cp,a)][0], "native model hash disagrees with coefficients")
            require(all(abs(v) <= (4000 if c in (0,65) else 16000) for c,v in enumerate(coeff)), "coefficient bound failed")
            if cp==0:
                require(not any(coeff), "nonzero initialization")
                continue
            check_continuity(models[(cp-1,a)][0], models[(cp,a)][0], continuity[(cp,a)])
            count = exposures[(cp,a)]
            require(len(count)==5 and sum(count[:4])==1080 and count[4]==1, "wrong experience budget")
            active=(cp-1)%4
            if a!=3 or cp==1:
                require(count[:4] == [1080 if c==active else 0 for c in range(4)], "unexpected current-only support")
            else:
                require(count[active]==540 and all(n==0 for c,n in enumerate(count[:4]) if c>=cp and cp<=4), "future-cohort replay")
            for candidate in range(2):
                check_fit(fits[(cp,a,candidate)])
    require(len(episodes)==34*4*4*540 and len(metrics)==34*4*4, "incomplete longitudinal probe matrix")
    checkpoints = [(cp,0) for cp in range(33)] + [(32,1)]
    for cp,snapshot in checkpoints:
        for a in range(4):
            for cohort in range(4):
                outcomes = [episodes[(cp,snapshot,a,cohort,ep)] for ep in range(540)]
                require(summarize(outcomes)==metrics[(cp,snapshot,a,cohort)], "native aggregate disagrees with episodes")
                for ep,r in enumerate(outcomes):
                    initial=episodes[(0,0,a,cohort,ep)]
                    require(r[1:4]==initial[1:4], "control/population changed")
                    if cp==0:
                        require(r[0]==r[2], "zero residual differs from deployable control")
                    if cp>=cohort+1:
                        require(r[7]==episodes[(cohort+1,0,a,cohort,ep)][0], "retention anchor changed")
                    else:
                        require(r[7]==-1, "premature anchor")
                    if snapshot:
                        require(r[:7]==episodes[(4,0,a,cohort,ep)][:7], "frozen snapshot behavior drifted")
    totals={}
    for cp in range(33):
        for a in range(4):
            totals[(cp,a)] = [sum(metrics[(cp,0,a,j)][k] for j in range(4)) for k in range(14)]
    final={str(a): totals[(32,a)] for a in range(4)}
    real=final["1"]
    history_signal=all(real[0]>final[str(a)][0] and real[1]>final[str(a)][1] and real[2]>=final[str(a)][2] for a in (0,2)) and real[4]==0
    longevity={}
    for a in range(4):
        recovery={}
        for cohort in range(4):
            first_loss=next((cp for cp in range(cohort+2,33) if metrics[(cp,0,a,cohort)][9]>0),None)
            recovered=next((cp for cp in range(first_loss+1,33) if metrics[(cp,0,a,cohort)][9]==0),None) if first_loss else None
            recovery[str(cohort)]={"first_anchor_loss_checkpoint":first_loss,"first_zero_anchor_loss_return":recovered}
        longevity[str(a)]={"final_anchor_losses":totals[(32,a)][9], "worst_anchor_losses_after_cycle_one":max(totals[(cp,a)][9] for cp in range(4,33)),
                            "cycle_one_reachability":totals[(4,a)][0],"final_reachability":totals[(32,a)][0],"recovery":recovery}
    return {"schema_version":1,"verified":True,"errors":[],"outcome":one("e51ai_outcome")[0],
            "metric_columns":["reachable","known","no_unique","union","union_lost","union_rescued","hybrid","hybrid_lost","hybrid_rescued","anchor_lost","anchor_gained","t0success","t0unknown","t0wrong"],
            "final_metrics":final,"history_preserving_signal":history_signal,"longevity":longevity,
            "curve":[{"checkpoint":cp,"arm":a,"metrics":totals[(cp,a)]} for cp in range(33) for a in range(4)],
            "probe_episode_rows_verified":len(episodes),"checkpoint_parameters_verified":len(weights),
            "input_files_verified":len(paths),"validation_executed":0,"confirmation_executed":0,
            "sha256":{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ("SOURCE.zag","RAW.log","NATIVE_BUILD_1","NATIVE_BUILD_2")}}


if __name__ == "__main__":
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".scratch/e51ai")
    try:
        result=verify(root)
    except (OSError,ValueError,KeyError,IndexError,TypeError) as exc:
        result={"verified":False,"errors":[f"{type(exc).__name__}: {exc}"]}
    (root/"EVIDENCE_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="curve"},indent=2))
    raise SystemExit(0 if result["verified"] else 1)
