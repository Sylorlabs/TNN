#!/usr/bin/env python3
"""STEP 0 (build glue) — Channel-ban test battery extraction.

Reads ONLY frozen measured evidence (KB4 autopsy artifacts) and emits the
92-row battery as five 92-char 0/1 strings for embedding in src/cbtest.zag.

Evidence sources (frozen, read-only):
  TCP truth rows : kb/autopsy/channels2/out_tcp/truth_rows.txt   (sense,task,variant,logical,Y,kb4idx)
  C2 verdicts    : kb/autopsy/channels2/out_tcp/run1/verdicts.txt (TEST rows, V col)
  C3 verdicts    : kb/autopsy/channels2/out_c3/run1/verdicts.txt  (TEST rows, V col)
  C1 scout rows  : kb/autopsy/channels2/out_c1scout/run1/truth_rows.txt (logical,J,A,Y)

KB3 pre-assertions (must hold or extraction aborts):
  92 sense-A rows; sum(y)==52; C2 all 1; C3 87 agree; 15 pitchdisc rows;
  on pitchdisc: sum(y)==7 and aej==y on all 15; joins 92/92 and 15/15.

This script is glue (extraction only). The gate mechanism and all counting
live in pure Zag (src/cbtest.zag); src/score_cbtest.py independently
re-verifies the embedded strings against these same evidence files.
Zero RNG.
"""
import os
import sys

TN = os.path.expanduser("~/workspace/tnn-lab")
CHAN2 = os.path.join(TN, "kb", "autopsy", "channels2")
OUT = os.path.join(TN, "senses", "pam-rebuild", "v2", "channel_ban_test", "src")


def rows(path):
    with open(path) as f:
        return [l.rstrip("\n").split("\t") for l in f if l.strip()]


def main():
    truth = [r for r in rows(os.path.join(CHAN2, "out_tcp", "truth_rows.txt")) if r[0] == "A"]
    c2v = [r for r in rows(os.path.join(CHAN2, "out_tcp", "run1", "verdicts.txt"))
           if r[0] == "TEST" and r[1] == "A"]
    c3v = [r for r in rows(os.path.join(CHAN2, "out_c3", "run1", "verdicts.txt"))
           if r[0] == "TEST" and r[1] == "A"]
    c1 = rows(os.path.join(CHAN2, "out_c1scout", "run1", "truth_rows.txt"))

    assert len(truth) == 92, len(truth)
    ymap = {(r[1], r[2], r[3]): int(r[4]) for r in truth}
    c2map = {(r[2], r[3], r[4]): int(r[6]) for r in c2v}
    c3map = {(r[2], r[3], r[4]): int(r[6]) for r in c3v}
    assert len(c2map) == 92 and len(c3map) == 92, (len(c2map), len(c3map))
    # C1 scout: logical -> (J, A); aej = 1 iff J == A
    # (scout keys lack the .pcm extension used in the TCP battery)
    def base(s):
        return s[:-4] if s.endswith(".pcm") else s
    c1map = {base(r[0]): (r[1], r[2], int(r[3])) for r in c1}
    assert len(c1map) == 15, len(c1map)

    keys = sorted(ymap.keys())  # (task, variant, logical)
    Y, C2, C3, PA, AEJ = [], [], [], [], []
    for (task, variant, logical) in keys:
        y = ymap[(task, variant, logical)]
        c2 = c2map[(task, variant, logical)]
        c3 = c3map[(task, variant, logical)]
        pa = 1 if task == "pitchdisc" else 0
        aej = 0
        if pa:
            assert base(logical) in c1map, logical
            j, a, cy = c1map[base(logical)]
            assert cy == y, (logical, cy, y)  # scout Y matches TCP Y
            aej = 1 if j == a else 0
        Y.append(y)
        C2.append(c2)
        C3.append(c3)
        PA.append(pa)
        AEJ.append(aej)

    # KB3 pre-assertions on the assembled battery
    assert sum(Y) == 52 and len(Y) - sum(Y) == 40, sum(Y)
    assert all(v == 1 for v in C2), "DPI: C2 must be constant INSTALL"
    assert sum(C3) == 87, sum(C3)
    assert sum(PA) == 15, sum(PA)
    pd_idx = [i for i, p in enumerate(PA) if p == 1]
    assert sum(Y[i] for i in pd_idx) == 7, "pitchdisc Y=1 count"
    assert all(AEJ[i] == Y[i] for i in pd_idx), "aej==y on all 15 pitchdisc rows"
    # C3 true/false installs on the battery (for the record)
    c3_true = sum(1 for i in range(92) if C3[i] == 1 and Y[i] == 1)
    c3_false = sum(1 for i in range(92) if C3[i] == 1 and Y[i] == 0)
    assert (c3_true, c3_false) == (50, 37), (c3_true, c3_false)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "battery_strings.txt"), "w") as f:
        f.write("Y=" + "".join(map(str, Y)) + "\n")
        f.write("C2=" + "".join(map(str, C2)) + "\n")
        f.write("C3=" + "".join(map(str, C3)) + "\n")
        f.write("PA=" + "".join(map(str, PA)) + "\n")
        f.write("AEJ=" + "".join(map(str, AEJ)) + "\n")
    print("battery: 92 rows; Y1=%d Y0=%d; C2=%d; C3=%d (true %d / false %d); pitchdisc=%d" % (
        sum(Y), 92 - sum(Y), sum(C2), sum(C3), c3_true, c3_false, sum(PA)))
    print("wrote src/battery_strings.txt")


if __name__ == "__main__":
    main()
