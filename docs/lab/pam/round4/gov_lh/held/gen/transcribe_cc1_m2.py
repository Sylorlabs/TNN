#!/usr/bin/env python3
"""transcribe_cc1_m2.py — CC1 wrong-pair family -> v4.zag MODE-2 trial streams.

Single source of truth: gen_guard.py CELLS (the frozen CC1 guard experiment).
Emits 15-field lines per cell:
  seq|tcode|prog|progF|agree|strong|conf|mrgF|jcode|pred|measure|correct|truth|span_a|span_b
progF=prog, agree=1, strong=1 (unused by the gate). correct = 1 iff jcode==truth.
Spans are the EXPLICIT fixture spans (sa, sb) from gen_guard.py — v4 mode 2.

Covers the 9 scored cells (CC1, CC1-V1..V8) + CC1-V9 (unscored ceiling probe).
Zero RNG. Deterministic.
"""
import re, os

GEN = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild/round2/cc1_guard/gen_guard.py")
OUT = os.path.expanduser("~/workspace/pam_gov_lh/crew6_held/gen/cc1_cells/mode2")

WANT = ["CC1", "CC1-V1", "CC1-V2", "CC1-V3", "CC1-V4",
        "CC1-V5", "CC1-V6", "CC1-V7", "CC1-V8", "CC1-V9"]

src = open(GEN).read()
cells = {}
for m in re.finditer(r'\("((?:CC1|CC1-V\d))", \[(.*?)\], (\d+), None, 0, (True|False)\)', src, re.S):
    name, body, finalj, scored = m.group(1), m.group(2), int(m.group(3)), m.group(4)
    trials = [tuple(map(int, t.split(','))) for t in re.findall(r'\(([\d,\s]+)\)', body)]
    cells[name] = (trials, finalj, scored == "True")

os.makedirs(OUT, exist_ok=True)
for name in WANT:
    trials, finalj, scored = cells[name]
    lines = []
    for (tcode, prog, jcode, conf, pred, meas, mrgF, truth, jG, confG, seq, sa, sb) in trials:
        correct = 1 if jcode == truth else 0
        lines.append("|".join(map(str, [seq, tcode, prog, prog, 1, 1, conf, mrgF,
                                        jcode, pred, meas, correct, truth, sa, sb])))
    p = os.path.join(OUT, "cc1_%s_m2.txt" % name.replace("-", "_").lower())
    open(p, "w").write("\n".join(lines) + "\n")
    # sanity: 15 fields on every line, spans sane
    for ln in lines:
        f = ln.split("|")
        assert len(f) == 15, ln
        assert int(f[13]) < int(f[14]), ln
    print(name, len(lines), "trials", "scored" if scored else "UNSCORED",
          "->", p, "finalj", finalj)
