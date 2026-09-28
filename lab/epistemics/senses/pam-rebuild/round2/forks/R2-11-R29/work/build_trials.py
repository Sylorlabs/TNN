#!/usr/bin/env python3
"""Build the frozen R2-11 trial list (11,840 trials) from:
  - generated fixtures: round2/fixtures/{r2a_*,r2n_*} + FAMILIES.tsv (truth/family)
  - frozen harness: senses/rebuild/harness/fixtures
    (370 primary + 370 noise + 185 adversarial)
Writes trials.tsv: trial_id, task, split, family, fixture, truth.
Deterministic: sorted order throughout. Pure build glue (not a TNN path).

NOTE (frozen spec arithmetic): the prereg's summary says "10,000 trials"
(5,000 normal + 5,000 adversarial), but the frozen realized pool is 11,840
(10,915 generated + 925 harness). This script enumerates the REALIZED pool;
the discrepancy is documented, not retro-fixed.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures"
HARN = "/home/hatch/workspace/tnn-lab/senses/rebuild/harness/fixtures"
OUT = os.path.join(HERE, "trials.tsv")

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc", "motiondir"]

def task_of(fn):
    for t in TASKS:
        if "_" + t + "_" in fn:
            return t
    raise ValueError(fn)

def main():
    rows = []
    # generated fixtures: truth/family from FAMILIES.tsv
    fam = {}
    with open(os.path.join(FIX, "FAMILIES.tsv")) as f:
        f.readline()
        for line in f:
            p = line.rstrip("\n").split("\t")
            fam[p[0]] = (p[1], p[2])
    for fn, (family, truth) in sorted(fam.items()):
        task = task_of(fn)
        split = "adversarial" if fn.startswith("r2a_") else "normal"
        tid = "r211g_" + os.path.splitext(fn)[0]
        rows.append((tid, task, split, family, os.path.join(FIX, fn), truth))
    # frozen harness fixtures (+ .truth sidecars)
    tmap = {"t1_colordisc": "colordisc", "t2_colorconst": "colorconst",
            "t3_shapetrans": "shapetrans", "t4_pitchdisc": "pitchdisc",
            "t5_timbredisc": "timbredisc", "t6_motiondir": "motiondir"}
    for d in sorted(os.listdir(HARN)):
        if d not in tmap:
            continue
        task = tmap[d]
        for splitdir in ("primary", "noise", "adversarial"):
            sdir = os.path.join(HARN, d, splitdir)
            if not os.path.isdir(sdir):
                continue
            fns = sorted(fn for fn in os.listdir(sdir) if not fn.endswith(".truth"))
            for fn in fns:
                with open(os.path.join(sdir, fn + ".truth")) as tf:
                    truth = tf.read().strip().split("=", 1)[1]
                tid = "r211h_" + os.path.splitext(fn)[0]
                split = "adversarial" if splitdir == "adversarial" else "normal"
                famname = "harness-" + splitdir
                rows.append((tid, task, split, famname, os.path.join(sdir, fn), truth))
    with open(OUT, "w") as f:
        f.write("trial_id\ttask\tsplit\tfamily\tfixture\ttruth\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    n_gen = sum(1 for r in rows if r[0].startswith("r211g_"))
    n_h = sum(1 for r in rows if r[0].startswith("r211h_"))
    print(f"{len(rows)} trials: {n_gen} generated + {n_h} harness")

main()
