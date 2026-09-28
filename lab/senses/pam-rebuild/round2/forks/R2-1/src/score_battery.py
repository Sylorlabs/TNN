#!/usr/bin/env python3
"""Score R2-1 battery: B1-B7 and kill criteria.

Inputs: evidence/battery_run1/full_results.csv, ablated_results.csv, trial_index.csv
"""
import csv, sys, os
from collections import Counter, defaultdict

FORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
EV = os.path.join(FORK, "evidence", "battery_run1")

def load(fn):
    return list(csv.DictReader(open(os.path.join(EV, fn))))

def main():
    full = {r["trial_idx"]: r for r in load("full_results.csv")}
    abl = {r["trial_idx"]: r for r in load("ablated_results.csv")}
    idx = {r["trial_idx"]: r for r in csv.DictReader(
        open(os.path.join(FORK, "evidence", "trial_index.csv")))}
    assert len(full) == 10000 and len(abl) == 10000, (len(full), len(abl))

    # --- Helper: correctness ---
    # A "correct percept" = front-end judgment matches truth on F.
    # For install metrics: INSTALL is correct iff judgment==truth (percept correct).
    # False install = INSTALL when judgment != truth.
    def is_correct_install(r):
        return r["decision"] == "INSTALL" and r["judgment"] == r["truth"]
    def is_false_install(r):
        return r["decision"] == "INSTALL" and r["judgment"] != r["truth"]

    # --- Kill criterion 1 & B5: false installs ---
    false_full = sum(1 for r in full.values() if is_false_install(r))
    false_abl = sum(1 for r in abl.values() if is_false_install(r))
    fi_rate_full = false_full / 10000
    fi_rate_abl = false_abl / 10000

    # Adversarial false installs (B5)
    adv_trials = [i for i, t in idx.items() if t["stratum"] in ("gen_adv", "frozen_adv")]
    false_adv_full = sum(1 for i in adv_trials if is_false_install(full[i]))
    fi_adv_rate = false_adv_full / len(adv_trials)

    # --- Kill criterion 2: true-install recall ---
    # Denominator: all correct percepts (judgment==truth in full mode)
    correct_percepts = [i for i in full if full[i]["judgment"] == full[i]["truth"]]
    true_installs = sum(1 for i in correct_percepts if full[i]["decision"] == "INSTALL")
    recall = true_installs / len(correct_percepts) if correct_percepts else 0

    # --- Kill criterion 3: ablation raises false installs by >=5x ---
    abl_ratio = (false_abl / false_full) if false_full > 0 else float('inf')

    # --- B1: primary accuracy on frozen 370 primary ---
    # Reconstruct primary indices: per task, primary first then noise.
    # Task order and counts: colordisc 60, colorconst 40, shapetrans 90,
    #   pitchdisc 60, timbredisc 60, motiondir 60.
    task_primary_counts = {"colordisc": 60, "colorconst": 40, "shapetrans": 90,
                           "pitchdisc": 60, "timbredisc": 60, "motiondir": 60}
    primary_ids = set()
    # r21f_<task>_<global_idx>; global idx ranges computed in convert order
    tidx = 0
    for task in ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]:
        n = task_primary_counts[task]
        for j in range(n):
            primary_ids.add("r21f_%s_%d" % (task, tidx + j))
        tidx += 2 * n
    b1_trials = [i for i, t in idx.items()
                 if t["stratum"] == "frozen_normal" and t["fixture_id"] in primary_ids]
    assert len(b1_trials) == 370, len(b1_trials)
    b1_acc = sum(1 for i in b1_trials if full[i]["judgment"] == full[i]["truth"]) / 370

    # --- B2: judgment-accuracy delta R2-1 - Approach A ---
    # Approach A = ablated (T1 only) decision accuracy; R2-1 = full decision accuracy.
    # Decision accuracy: INSTALL iff percept correct.
    def decision_correct(r):
        percept_ok = (r["judgment"] == r["truth"])
        if r["decision"] == "INSTALL":
            return percept_ok
        else:  # WITHHOLD
            return not percept_ok
    acc_full = sum(1 for r in full.values() if decision_correct(r)) / 10000
    acc_abl = sum(1 for r in abl.values() if decision_correct(r)) / 10000
    b2_delta = acc_full - acc_abl

    # --- B4: contract changes decisions on >=10% of adversarial, reduces false installs ---
    changed = sum(1 for i in adv_trials if full[i]["decision"] != abl[i]["decision"])
    b4_change_rate = changed / len(adv_trials)
    b4_reduces = false_adv_full < sum(1 for i in adv_trials if is_false_install(abl[i]))

    # --- Report ---
    print("=== R2-1 BATTERY RESULTS (run1) ===")
    print("Kill 1 (false installs <=2%%): %d/10000 = %.4f%% %s" %
          (false_full, fi_rate_full*100, "PASS" if fi_rate_full <= 0.02 else "FAIL"))
    print("Kill 2 (recall >=80%%): %d/%d = %.4f%% %s" %
          (true_installs, len(correct_percepts), recall*100,
           "PASS" if recall >= 0.80 else "FAIL"))
    print("Kill 3 (ablation >=5x): abl=%d full=%d ratio=%.2fx %s" %
          (false_abl, false_full, abl_ratio,
           "PASS" if abl_ratio >= 5 else "FAIL"))
    print("B1 (primary acc >=60%%): %.4f%% %s" %
          (b1_acc*100, "PASS" if b1_acc >= 0.60 else "FAIL"))
    print("B2 (delta R2-1 - ApproachA): %.4f%% (report only)" % (b2_delta*100))
    print("B4 (change >=10%% adv): %.4f%% %s; reduces false installs: %s %s" %
          (b4_change_rate*100, "PASS" if b4_change_rate >= 0.10 else "FAIL",
           b4_reduces, "PASS" if (b4_change_rate>=0.10 and b4_reduces) else "FAIL"))
    print("B5 (adv false-install <=2%%): %d/%d = %.4f%% %s" %
          (false_adv_full, len(adv_trials), fi_adv_rate*100,
           "PASS" if fi_adv_rate <= 0.02 else "FAIL"))
    print("  (ablated false installs: %d/10000 = %.4f%%)" % (false_abl, fi_rate_abl*100))

if __name__ == "__main__":
    main()
