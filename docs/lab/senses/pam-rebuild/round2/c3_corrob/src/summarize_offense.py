#!/usr/bin/env python3
"""Glue: summarize CRO-1 offense battery per-trial output.
Glue is never the instrument; it only reads bytes.
Input: offense_N.out (tab-separated: CRO seq AC class phase decision)
Output: attack/control rates per AC."""
from collections import Counter
import sys

path = sys.argv[1]
atk = Counter()
ctl = Counter()
for line in open(path):
    p = line.rstrip("\n").split("\t")
    if len(p) < 7 or p[0] != "CRO":
        continue
    ac, cls, dec = p[2], p[3], p[6]
    if cls == "T":
        ctl[(ac, dec)] += 1
    else:
        atk[(ac, dec)] += 1
for ac in ["AC1", "AC2", "AC3"]:
    ai = atk[(ac, "INSTALL")]
    aw = atk[(ac, "WITHHOLD")]
    ci = ctl[(ac, "INSTALL")]
    cw = ctl[(ac, "WITHHOLD")]
    an, cn = ai + aw, ci + cw
    print(f"{ac} attack : {ai}/{an} = {100.0*ai/an:.2f}%")
    print(f"{ac} control: {ci}/{cn} = {100.0*ci/cn:.2f}%")
