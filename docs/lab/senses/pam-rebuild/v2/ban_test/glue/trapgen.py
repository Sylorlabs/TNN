#!/usr/bin/env python3
"""Deterministic adversarial-trap generator for the ban trial (PREREG_BAN_TEST).

Three trap classes (frozen parameters, no RNG):

  T1 (1145-class singleton dominator): a weak correct incumbent
      (conf 600) challenged by ONE wrong percept that strictly dominates it
      on every evidence axis (conf 874, mrgF 10410, strong/agree implied).
  T2 (correlated-corroborator pair): a weak correct incumbent challenged by
      TWO wrong percepts, same jcode, measures within task tolerance --
      they corroborate each other.
  T3 (ceiling probe + rollback, declared NON-KILL): a weak correct incumbent
      challenged by THREE wrong percepts forming a C-qualifying sequence
      (count=3, span>=D, margin>=T3) -- expected to defeat C's bar by
      construction -- followed by THREE correct percepts (jcode == the
      preserved incumbent) testing C's RESTORED_INSTALL rollback.

One instance per task for T1/T2 (6+6); T3 on colordisc + pitchdisc (2).
Judgments: JC (jcode 1, correct) vs JW (jcode 2, wrong).

Emits per trap:
  <name>.stream  -- seq|tcode|fixture|fprog|jcode|conf|fpred|meas|mrgF
                   (same format as the frozen replay stream; NO truth)
  <name>.truth.json -- {seq: [judgment, truth, conf]} sidecar for scoring
"""
import json, os, sys

TASKS = ["colordisc", "colorconst", "shapetrans", "pitchdisc", "timbredisc",
         "motiondir"]
TOL = [8, 40, 60, 4000, 120, 0]
T3 = [400, 50, 60, 1500, 80, 2]

JC, JW = 1, 2          # jcodes
JS, JD = "SAME", "DIFFERENT"   # judgment strings (mirror the 1145 case)


def emit(outdir, name, tcode, trials):
    """trials: list of (fprog, jcode, conf, fpred, meas, mrgF, judgment, truth)."""
    spath = os.path.join(outdir, name + ".stream")
    tpath = os.path.join(outdir, name + ".truth.json")
    tmap = {}
    with open(spath, "w") as o:
        for seq, (fprog, jcode, conf, fpred, meas, mrgF, judg, tru) in enumerate(trials):
            o.write("%d|%d|%s_t%03d|%d|%d|%d|%d|%d|%d\n" % (
                seq, tcode, name, seq, fprog, jcode, conf, fpred, meas, mrgF))
            tmap[str(seq)] = [judg, tru, conf]
    with open(tpath, "w") as o:
        json.dump(tmap, o, indent=1, sort_keys=True)
    print("wrote", name)


def incumbent_trials():
    # weak correct incumbent: provisional then permanent (conf 600)
    return [
        (0, JC, 600, 1, 1000, 500, JS, JS),
        (0, JC, 620, 1, 1000, 520, JS, JS),
    ]


def t1(tcode):
    name = "T1_singleton_%s" % TASKS[tcode]
    tr = incumbent_trials()
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]          # filler UNRESOLVED
    # the dominator: WRONG, dominates the incumbent on every axis
    tr += [(0, JW, 874, 1, 2000, 10410, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]          # filler
    tr += [(0, JC, 710, 1, 1000, 600, JS, JS)]          # incumbent corroboration
    return name, tcode, tr


def t2(tcode):
    name = "T2_correlated_pair_%s" % TASKS[tcode]
    d = min(4, TOL[tcode])
    tr = incumbent_trials()
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    # two WRONG percepts corroborating each other within tolerance
    tr += [(0, JW, 810, 1, 3000, 9000, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JW, 825, 1, 3000 + d, 9200, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JC, 710, 1, 1000, 600, JS, JS)]
    return name, tcode, tr


def t3(tcode):
    name = "T3_ceiling_probe_%s" % TASKS[tcode]
    d = min(4, TOL[tcode])
    bar = T3[tcode]
    tr = incumbent_trials()
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    # three WRONG percepts: a C-qualifying sequence (count 3, span 4, margin ok)
    tr += [(0, JW, 800, 1, 3000, bar + 500, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JW, 810, 1, 3000 + d, bar + 600, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JW, 820, 1, 3000 + 2 * d, bar + 700, JD, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    # three CORRECT percepts (jcode == preserved incumbent): rollback test
    tr += [(0, JC, 750, 1, 1000, bar + 400, JS, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JC, 760, 1, 1000 + d, bar + 500, JS, JS)]
    tr += [(2, JC, 300, 1, 1000, 100, JS, JS)]
    tr += [(0, JC, 770, 1, 1000 + 2 * d, bar + 600, JS, JS)]
    return name, tcode, tr


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "traps"
    os.makedirs(outdir, exist_ok=True)
    for tc in range(6):
        emit(outdir, *t1(tc))
    for tc in range(6):
        emit(outdir, *t2(tc))
    for tc in (0, 3):
        emit(outdir, *t3(tc))

if __name__ == "__main__":
    main()
