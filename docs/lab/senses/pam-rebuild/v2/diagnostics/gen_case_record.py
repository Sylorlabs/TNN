#!/usr/bin/env python3
"""Generate the frozen case record for the R2-4 / RK-3 deep-dive self-application.

Reads (read-only) the frozen R2-4 evidence and emits two files the Zag
diagnostic harness consumes:
  case_r24_rk3.txt   - one line per trial: seq|tcode|prog|jcode|jcorrect|conf|pred|meas|progF|disp|detail
  expect_r24_rk3.txt - KEY=value expectations (the frozen verdict numbers)

Field sources (authoritative for the gate's actual input):
  records.txt            -> seq, tcode, prog (post-deliberation; verified == sweep final_prog), jcode
  sweep.jsonl            -> judgment, truth (=> jcorrect), conf, pred, measure, progF
  gate_dispositions.txt  -> disp, detail (recorded dispositions to replay against)

This script is glue, not the instrument: every number it emits is recomputed
independently by diagnose.zag, which also SHA256-freezes the raw bytes.
"""
import json
import os
import sys

EV = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-4/evidence/clean")
OUT = os.path.dirname(os.path.abspath(__file__))

PROG = {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}
DISP = {"PROVISIONAL_INSTALL": 0, "CORROBORATED": 1, "PERMANENT_INSTALL": 2,
        "WITHHELD": 3, "CONFLICT_WITHHELD": 4, "NEGATIVE_EVIDENCE": 5,
        "SUPPRESSED": 6}
DETAIL = {"new": 0, "corroborated": 1, "perm": 2, "perm-measure-diff": 3,
          "prov-measure-diff": 4, "reversed_old": 5, "perm_seq": 6,
          "unresolved": 7, "neg": 8, "pred0": 9, "stored": 10, "dup": 11}


def toint(v):
    return int(v) if not isinstance(v, int) else v


def main():
    sweep = {}
    for line in open(os.path.join(EV, "sweep.jsonl")):
        r = json.loads(line)
        sweep[r["seq"]] = r

    rec = {}  # seq -> (tcode, prog, jcode)
    for line in open(os.path.join(EV, "records.txt")):
        p = line.rstrip("\n").split("|")
        rec[int(p[0])] = (int(p[1]), int(p[3]), int(p[4]))

    disp = {}  # seq -> (disp_code, detail_code)
    for line in open(os.path.join(EV, "gate_dispositions.txt")):
        p = line.rstrip("\n").split("|")
        d = p[3]
        det = p[4].split("=")[0]
        disp[int(p[0])] = (DISP[d], DETAIL[det])

    assert len(sweep) == 11840 and len(rec) == 11840 and len(disp) == 11840
    assert set(sweep) == set(rec) == set(disp)

    lines = []
    for s in sorted(sweep):
        r = sweep[s]
        tcode, prog, jcode = rec[s]
        dcode, detcode = disp[s]
        jcorrect = 1 if r["judgment"] == r["truth"] else 0
        conf = toint(r["conf"])
        pred = toint(r["pred"])
        meas = toint(r["measure"])
        progF = PROG[r["progF"]]
        lines.append("%d|%d|%d|%d|%d|%d|%d|%d|%d|%d|%d" % (
            s, tcode, prog, jcode, jcorrect, conf, pred, meas, progF, dcode, detcode))

    case_path = os.path.join(OUT, "case_r24_rk3.txt")
    with open(case_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    # frozen verdict numbers (cross-checked here; diagnose.zag re-derives them)
    chc = [s for s in sweep if sweep[s]["judgment"] == sweep[s]["truth"]
           and toint(sweep[s]["conf"]) >= 700]
    inst = [s for s in chc if disp[s][0] in (0, 1, 2)]
    assert len(chc) == 1102, len(chc)
    assert len(inst) == 104, len(inst)

    expect_path = os.path.join(OUT, "expect_r24_rk3.txt")
    with open(expect_path, "w") as f:
        f.write("CASE=R2-4/RK-3\n")
        f.write("N_TRIALS=11840\n")
        f.write("RK3_NUM=104\n")
        f.write("RK3_DEN=1102\n")
        f.write("RK3_BAR_NUM=85\n")
        f.write("RK3_BAR_DEN=100\n")
        f.write("REPLAY_MISMATCH_MAX=0\n")
    print("wrote", case_path, len(lines), "trials")
    print("wrote", expect_path)


if __name__ == "__main__":
    main()
