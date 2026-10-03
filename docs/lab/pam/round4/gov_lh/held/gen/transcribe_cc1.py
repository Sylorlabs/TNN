#!/usr/bin/env python3
"""transcribe_cc1.py — CC1 wrong-pair family -> v4.zag trial streams.

Reads the frozen single source of truth (gen_guard.py CELLS, from the CC1
guard experiment) and emits one 13-field case file per scored CC1 cell:
  seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|correct|truth
correct = 1 iff jcode == truth (scoring only). progF=prog, agree=1, strong=1
(unused by the gate). Spans are NOT carried: v4 mode 1 derives them via the
frozen rule (seq, seq+2000) per PREREG_CREW6_HELD.md A.2.

Zero RNG. Deterministic.
"""
import re, sys, os

GEN = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/cc1_guard/gen_guard.py")
OUT = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held/gen/cc1_cells")

WANT = ["CC1", "CC1-V1", "CC1-V2", "CC1-V3", "CC1-V4",
        "CC1-V5", "CC1-V6", "CC1-V7", "CC1-V8"]

src = open(GEN).read()
cells = {}
for m in re.finditer(r'\("((?:CC1|CC1-V\d))", \[(.*?)\], (\d+), None, 0, (True|False)\)', src, re.S):
    name, body, finalj, scored = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    trials = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,\s]+)\)', body)]
    cells[name] = (trials, finalj, scored == "True")

os.makedirs(OUT, exist_ok=True)
for name in WANT:
    trials, finalj, scored = cells[name]
    assert scored, name
    lines = []
    for (tcode, prog, jcode, conf, pred, meas, mrgF, truth, jG, confG, seq, sa, sb) in trials:
        correct = 1 if jcode == truth else 0
        lines.append("|".join(map(str, [seq, tcode, prog, prog, 1, 1, conf, mrgF,
                                        jcode, pred, meas, correct, truth])))
    p = os.path.join(OUT, "cc1_%s.txt" % name.replace("-", "_").lower())
    open(p, "w").write("\n".join(lines) + "\n")
    print(name, len(lines), "trials ->", p, "finalj", finalj)
