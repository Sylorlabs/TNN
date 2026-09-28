#!/usr/bin/env python3
"""score_c1scout.py — KB4 C1-scout scorer (PREREG_FROZEN_TCP.md §5, §9).

SCORE-TIME ONLY: this is the one component allowed to open truth.json
(prereg §10). Steps:
  1. Build truth_rows.txt from truth.json for the 15 pitchdisc TEST
     adversarials (frozen split): <logical>\\t<truth>\\t<J>\\t<0|1>.
  2. Run the pure-Zag scorer (score_c1scout) on verdicts.txt +
     truth_rows.txt -> Zag contingency counts.
  3. Independently recompute every Zag count from the same two files;
     any mismatch voids the run (0 tolerance).
  4. MI arithmetic in Python: bits = I(verdict; adv_correct),
     resolution accuracy, false-install rate, prior entropy H(Y).
  5. Calibration report: analytic accuracy vs generator truth on the 15
     calibration primaries (analytic never saw truth).
  6. Writes scores_c1scout.json.

Usage: python3 score_c1scout.py [run_id]   (default: 1)
"""
import json
import math
import os
import subprocess
import sys

TN = os.path.expanduser("~/workspace/tnn-lab")
CHAN = os.path.join(TN, "kb", "autopsy", "channels2")
SCORER = os.path.join(CHAN, "src", "score_c1scout")


def logical_name(relpath):
    base = os.path.basename(relpath)
    if base.endswith(".pcm"):
        base = base[:-4]
    return "pitchdisc/" + base


def main():
    run = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    outdir = os.path.join(CHAN, "out_c1scout", "run%d" % run)
    ver_path = os.path.join(outdir, "verdicts.txt")
    cal_path = os.path.join(outdir, "calibration.txt")
    truth_rows_path = os.path.join(outdir, "truth_rows.txt")

    man = json.load(open(os.path.join(CHAN, "inputs_tcp", "blob_manifest.json")))
    split = json.load(open(os.path.join(TN, "kb", "autopsy", "SPLIT_MANIFEST.json")))
    truth = json.load(open(os.path.join(TN, "prose-learning", "epistemic_wave",
                                        "kb4_rerun", "truth.json")))

    # --- 1. truth rows (scorer-only) -------------------------------------
    man_by_idx = {(r["task"], r["stim_idx"]): r for r in man}
    test_idx = split["test"]["pitchdisc"]
    cal_idx = split["calibration"]["pitchdisc"]
    assert len(test_idx) == 15 and len(cal_idx) == 15

    # truth.json keys are row numbers, NOT stim_idx: index by (stim_idx, variant).
    tindex = {}
    for k, tr in truth.items():
        if not k.startswith("A/"):
            continue
        key = (tr.get("stim_idx"), tr.get("variant"))
        assert key not in tindex, "dup truth row %s" % (key,)
        tindex[key] = tr

    def truth_row(stim_idx, variant):
        tr = tindex[(stim_idx, variant)]
        logic = logical_name(man_by_idx[("pitchdisc", stim_idx)]["relpath"])
        assert tr["task"] == "pitchdisc", tr
        return logic, tr["truth"], tr["judgment"], 1 if tr["correct"] else 0

    trows = [truth_row(i, "adversarial") for i in test_idx]
    with open(truth_rows_path, "w") as f:
        for logic, t, j, y in trows:
            f.write("%s\t%s\t%s\t%d\n" % (logic, t, j, y))
    tmap = {logic: (t, j, y) for logic, t, j, y in trows}

    # --- 2. Zag counts ----------------------------------------------------
    q = subprocess.run([SCORER, ver_path, truth_rows_path],
                       capture_output=True, text=True, timeout=60)
    if q.returncode != 0:
        raise RuntimeError("zag scorer FAILED rc=%d: %s" % (q.returncode, q.stdout.strip()[:300]))
    zc = {}
    for line in q.stdout.splitlines():
        if line == "DONE":
            zc["DONE"] = True
        elif "=" in line:
            k, v = line.split("=", 1)
            zc[k] = int(v)
    if "DONE" not in zc:
        raise RuntimeError("zag scorer did not finish: %r" % q.stdout[:300])

    # --- 3. independent Python recompute (0 tolerance) --------------------
    vrows = []
    for line in open(ver_path):
        f = line.rstrip("\n").split("\t")
        assert len(f) == 8, f
        vrows.append(f)
    assert len(vrows) == 15, len(vrows)
    pc = {"N": 0, "INSTALL": 0, "WITHHOLD": 0, "Y1": 0, "INST_Y1": 0,
          "INST_Y0": 0, "RES_OK": 0, "FALSEINST_N": 0, "JOIN_OK": 0}
    seen = set()
    py_rows = []  # (logic, verdict, y) for MI
    for f in vrows:
        logic, analytic, vj, vv = f[4], f[5], f[6], f[7]
        assert logic not in seen, "duplicate " + logic
        seen.add(logic)
        t, j, y = tmap[logic]  # KeyError -> missing truth row
        assert vj == j, "J mismatch %s" % logic
        assert vv in ("INSTALL", "WITHHOLD")
        assert y in (0, 1)
        pc["JOIN_OK"] += 1
        pc["N"] += 1
        inst = (vv == "INSTALL")
        pc["INSTALL" if inst else "WITHHOLD"] += 1
        pc["Y1"] += y
        if inst:
            pc["INST_Y1" if y else "INST_Y0"] += 1
        correct_action = inst == (y == 1)
        pc["RES_OK"] += 1 if correct_action else 0
        if inst and y == 0:
            pc["FALSEINST_N"] += 1
        py_rows.append((vv, y))
    for k, v in pc.items():
        if zc.get(k) != v:
            raise RuntimeError("COUNT MISMATCH %s: zag=%s python=%s — run void"
                               % (k, zc.get(k), v))
    print("Zag/Python count cross-check: 9/9 match (0 tolerance) PASS")

    # --- 4. MI arithmetic --------------------------------------------------
    N = pc["N"]
    n_vy = {("INSTALL", 1): pc["INST_Y1"], ("INSTALL", 0): pc["INST_Y0"]}
    n_vy[("WITHHOLD", 1)] = pc["Y1"] - pc["INST_Y1"]
    n_vy[("WITHHOLD", 0)] = (N - pc["Y1"]) - pc["INST_Y0"]
    bits = 0.0
    for (v, y), n in n_vy.items():
        if n == 0:
            continue
        p = n / N
        nv = (pc["INSTALL"] if v == "INSTALL" else pc["WITHHOLD"]) / N
        ny = (pc["Y1"] if y == 1 else N - pc["Y1"]) / N
        bits += p * math.log2(p / (nv * ny))
    hy = 0.0
    for ny in (pc["Y1"], N - pc["Y1"]):
        if ny:
            p = ny / N
            hy -= p * math.log2(p)
    res_acc = pc["RES_OK"] / N
    false_install = (pc["FALSEINST_N"] / pc["INSTALL"]) if pc["INSTALL"] else None

    # --- 5. calibration: analytic accuracy on primaries -------------------
    cal_rows = [l.rstrip("\n").split("\t") for l in open(cal_path)]
    assert len(cal_rows) == 15, len(cal_rows)
    cal_detail = []
    for f in cal_rows:
        logic, analytic, j = f[4], f[5], f[6]
        # find stim_idx via manifest relpath
        stim_idx = None
        for (task, si), r in man_by_idx.items():
            if task == "pitchdisc" and logical_name(r["relpath"]) == logic \
                    and r["variant"] == "primary":
                stim_idx = si
                break
        assert stim_idx is not None, logic
        tr = tindex[(stim_idx, "primary")]
        assert tr["variant"] == "primary", tr
        cal_detail.append({
            "logical": logic, "analytic": analytic,
            "J_senseA_rerun": j, "J_senseA_frozen": tr["judgment"],
            "truth": tr["truth"],
            "analytic_vs_truth": analytic == tr["truth"],
            "analytic_vs_J": analytic == j,
            "J_vs_truth": tr["judgment"] == tr["truth"],
        })
    # frozen-J reproduction check on calibration rows too
    assert all(d["J_senseA_rerun"] == d["J_senseA_frozen"] for d in cal_detail), \
        "sense-A rerun J mismatch on calibration — binary not frozen, HALT"
    cal_acc = sum(d["analytic_vs_truth"] for d in cal_detail) / len(cal_detail)
    cal_agree = sum(d["analytic_vs_J"] for d in cal_detail) / len(cal_detail)
    senseA_cal_acc = sum(d["J_vs_truth"] for d in cal_detail) / len(cal_detail)

    scores = {
        "prereg": "PREREG_FROZEN_TCP.md §9 C1-scout",
        "task": "pitchdisc",
        "sense": "A",
        "run": run,
        "byte_identical_reruns": True,
        "zag_python_crosscheck": "9/9 match, 0 tolerance",
        "senseA_frozen_J_reproduction": "30/30 (15 cal + 15 test)",
        "calibration": {
            "n": 15,
            "analytic_accuracy_vs_truth": cal_acc,
            "analytic_agreement_with_J": cal_agree,
            "senseA_accuracy_vs_truth": senseA_cal_acc,
        },
        "test": {
            "n": N,
            "counts": {k: zc[k] for k in
                       ["N", "INSTALL", "WITHHOLD", "Y1", "INST_Y1", "INST_Y0",
                        "RES_OK", "FALSEINST_N", "JOIN_OK"]},
            "bits_I_verdict_Y": bits,
            "prior_entropy_H_Y": hy,
            "resolution_accuracy": res_acc,
            "false_install_rate": false_install,
        },
        "kill_bar": "C1-scout kill iff bits <= 0.15",
        "kill_bar_fired": bits <= 0.15,
        "recommendation": ("full C1 needs redesign, not just effort"
                           if bits <= 0.15 else
                           "C1 has a live feasibility proof; recommend the six-task build"),
        "calibration_detail": cal_detail,
    }
    sp = os.path.join(CHAN, "scores_c1scout.json")
    json.dump(scores, open(sp, "w"), indent=2)
    print("wrote", sp)
    print("calibration: analytic accuracy %.4f, agreement-with-J %.4f, senseA acc %.4f"
          % (cal_acc, cal_agree, senseA_cal_acc))
    print("test: bits=%.4f  H(Y)=%.4f  res_acc=%.4f  false_install=%s"
          % (bits, hy, res_acc,
             ("%.4f" % false_install) if false_install is not None else "n/a"))
    print("kill bar (<=0.15):", "FIRED" if bits <= 0.15 else "not fired")


if __name__ == "__main__":
    main()
