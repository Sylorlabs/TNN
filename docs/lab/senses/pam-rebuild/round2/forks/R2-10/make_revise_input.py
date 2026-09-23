#!/usr/bin/env python3
"""Build revise input TSVs for R2-10 gate discipline.

Columns: fixture, task, jcode, conf, margin, feat0, feat1, truth, human

human="PENDING" marks verdicts not yet received (excluded from revision).
For feasibility testing only, human can be set to truth (oracle stand-in);
real discipline uses the verbatim human verdicts from the human package.
"""
import os
import subprocess
import sys

R2 = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/forks/R2-10")
FIX = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/fixtures")
SENSE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(R2, "src", "sense")

JCODE = {
    "colordisc": {"SAME": 0, "DIFFERENT": 1},
    "colorconst": {"SAME_SURFACE": 0, "DIFFERENT": 1},
    "shapetrans": {"CIRCLE": 0, "SQUARE": 1, "TRIANGLE": 2},
    "pitchdisc": {"SAME": 0, "HIGHER": 1, "LOWER": 2},
    "timbredisc": {"PURE": 0, "DARK": 1, "RICH": 2, "BRIGHT": 3},
    "motiondir": {"E": 0, "NE": 1, "N": 2, "NW": 3, "W": 4, "SW": 5, "S": 6, "SE": 7, "STILL": 8},
}


def task_of(fixture):
    for t in JCODE:
        if "_%s_" % t in fixture:
            return t
    raise ValueError(fixture)


def main():
    split = sys.argv[2] if len(sys.argv) > 2 else "train"
    oracle = sys.argv[3] if len(sys.argv) > 3 else "PENDING"  # PENDING | TRUTH
    man = os.path.join(R2, "evidence", "sample_%s_manifest.tsv" % split)
    trials = []
    for line in open(man):
        p = line.rstrip("\n").split("\t")
        if p[0] == "order":
            continue
        trials.append((p[1], task_of(p[1])))
    # run sense (noemit is enough: judgment/conf/margin/feats don't need artifacts)
    percepts = {}
    for t in JCODE:
        sub = [fx for fx, tt in trials if tt == t]
        if not sub:
            continue
        sl = "/tmp/r210_rev_%s_%s.list" % (split, t)
        with open(sl, "w") as f:
            for fx in sub:
                f.write(os.path.join(FIX, fx) + "\n")
        rr = subprocess.run([SENSE, "batch", t, sl, "noemit", "-"],
                            capture_output=True, text=True)
        if rr.returncode != 0:
            raise RuntimeError("batch failed %s: %s" % (t, rr.stderr[:300]))
        for line in rr.stdout.splitlines():
            p = line.split("\t")
            if len(p) >= 11 and not p[0].startswith("BATCH_ERROR"):
                percepts[p[0]] = p
    out = os.path.join(R2, "evidence", "human", split,
                       "revise_input_%s.tsv" % oracle.lower())
    with open(out, "w") as f:
        f.write("fixture\ttask\tjcode\tconf\tmargin\tfeat0\tfeat1\ttruth\thuman\n")
        for fx, t in trials:
            p = percepts[fx]
            jud, conf, margin, feat0, feat1 = p[1], p[2], p[3], p[8], p[9]
            truth = open(os.path.join(FIX, fx + ".truth")).read().strip().split("=", 1)[1]
            human = truth if oracle == "TRUTH" else "PENDING"
            f.write("%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\n" %
                    (fx, t, JCODE[t][jud], conf, margin, feat0, feat1, truth, human))
    print("wrote %s (%d rows, oracle=%s)" % (out, len(trials), oracle))


if __name__ == "__main__":
    main()
