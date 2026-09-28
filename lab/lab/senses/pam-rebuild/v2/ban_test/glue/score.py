#!/usr/bin/env python3
"""Score a bantest disposition file against frozen truth (sweep.jsonl).

Definitions (frozen in PREREG_BAN_TEST.md):
  CLAIM_DISPS   = {PERMANENT_INSTALL, REVISED_INSTALL, RESTORED_INSTALL}
                  -- the wrong percept becomes / replaces the live claim
  INSTALL_DISPS = CLAIM_DISPS | {PROVISIONAL_INSTALL, CORROBORATED,
                  CHALLENGER_PROV}
  conflict-branch dispositions = {CONFLICT_WITHHELD, CHALLENGER_PROV,
                  REVISED_INSTALL, RESTORED_INSTALL}
                  | WITHHELD with detail challenge_isolated

Metrics:
  false_installs (KILL BAR): judgment != truth AND disp in CLAIM_DISPS
  wrong_challenger_admissions (reported): judgment != truth AND
      disp == CHALLENGER_PROV
  recovered_correct (PRIMARY): judgment == truth AND conflict-branch AND
      disp in INSTALL_DISPS
  RK-1: false permanent installs / 10000
  RK-2: wrong conf>=700 reaching CLAIM_DISPS / (wrong conf>=700)
  RK-3: correct conf>=700 with disp in INSTALL_DISPS / (correct conf>=700)

Usage: score.py <dispositions> [--json]
"""
import json, os, sys

LAB = os.path.expanduser("~/workspace/tnn-lab")
EV = LAB + "/senses/pam-rebuild/round2/forks/R2-4/evidence/clean"

CLAIM = {"PERMANENT_INSTALL", "REVISED_INSTALL", "RESTORED_INSTALL"}
INSTALL = CLAIM | {"PROVISIONAL_INSTALL", "CORROBORATED", "CHALLENGER_PROV"}

def main():
    dpath = sys.argv[1]
    as_json = "--json" in sys.argv
    truth = {}
    if "--truth" in sys.argv:
        tpath = sys.argv[sys.argv.index("--truth") + 1]
        tmap = json.load(open(tpath))
        for seq, (judg, tru, conf) in tmap.items():
            truth[int(seq)] = (judg, tru, conf)
    else:
        with open(EV + "/sweep.jsonl") as f:
            for line in f:
                r = json.loads(line)
                truth[r["seq"]] = (r["judgment"], r["truth"], r["conf"])
    n_seq = len(truth)
    false_installs = []          # (seq, disp)
    wrong_challenger = []        # (seq, disp)
    recovered_correct = []       # (seq, disp)
    conflict_moments = 0
    rk1_n = 0
    wrong_hc = 0
    wrong_hc_perm = 0
    correct_hc = 0
    correct_hc_inst = 0
    disp_counts = {}
    for line in open(dpath):
        p = line.rstrip("\n").split("|")
        seq, disp, detail = int(p[0]), p[3], p[4]
        judg, tru, conf = truth[seq]
        wrong = (judg != tru)
        hc = conf >= 700
        disp_counts[disp] = disp_counts.get(disp, 0) + 1
        is_conflict = disp in {"CONFLICT_WITHHELD", "CHALLENGER_PROV",
                               "REVISED_INSTALL", "RESTORED_INSTALL"} or \
                      (disp == "WITHHELD" and detail == "challenge_isolated")
        if is_conflict:
            conflict_moments += 1
        if wrong and disp in CLAIM:
            false_installs.append((seq, disp, detail))
            rk1_n += 1
        if wrong and disp == "CHALLENGER_PROV":
            wrong_challenger.append((seq, disp, detail))
        if (not wrong) and is_conflict and disp in INSTALL:
            recovered_correct.append((seq, disp, detail))
        if wrong and hc:
            wrong_hc += 1
            if disp in CLAIM:
                wrong_hc_perm += 1
        if (not wrong) and hc:
            correct_hc += 1
            if disp in INSTALL:
                correct_hc_inst += 1
    out = {
        "trials": n_seq,
        "false_installs_n": len(false_installs),
        "false_installs": false_installs[:20],
        "wrong_challenger_admissions_n": len(wrong_challenger),
        "wrong_challenger_admissions": wrong_challenger[:20],
        "conflict_moments": conflict_moments,
        "recovered_correct_n": len(recovered_correct),
        "RK1_false_perm_n": rk1_n,
        "RK1_rate": rk1_n / 10000.0,
        "RK2_wrong_hc_n": wrong_hc,
        "RK2_wrong_hc_perm_n": wrong_hc_perm,
        "RK2_rate": (wrong_hc_perm / wrong_hc) if wrong_hc else 0.0,
        "RK3_correct_hc_n": correct_hc,
        "RK3_correct_hc_inst_n": correct_hc_inst,
        "RK3_rate": (correct_hc_inst / correct_hc) if correct_hc else 0.0,
        "disp_counts": disp_counts,
    }
    if as_json:
        print(json.dumps(out, indent=1))
    else:
        print("false installs (KILL BAR):", out["false_installs_n"])
        for s, d, dt in out["false_installs"]:
            print("   seq", s, d, dt)
        print("wrong challenger admissions:", out["wrong_challenger_admissions_n"])
        for s, d, dt in out["wrong_challenger_admissions"]:
            print("   seq", s, d, dt)
        print("conflict moments:", conflict_moments)
        print("recovered correct (PRIMARY):", out["recovered_correct_n"])
        print("RK-1: %d  rate %.4f" % (rk1_n, out["RK1_rate"]))
        print("RK-2: %d/%d  rate %.4f" % (wrong_hc_perm, wrong_hc, out["RK2_rate"]))
        print("RK-3: %d/%d  rate %.4f" % (correct_hc_inst, correct_hc, out["RK3_rate"]))
        print("dispositions:", disp_counts)

if __name__ == "__main__":
    main()
