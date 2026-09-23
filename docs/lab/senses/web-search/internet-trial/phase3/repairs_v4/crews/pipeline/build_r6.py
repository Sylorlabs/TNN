#!/usr/bin/env python3
"""hell-hole V4 pipeline: build the R6 proposition input from the C2 frozen battery.

Deterministic, mechanical seed->proposition mapping (documented in PIPELINE_REPORT.md):
  V3-20 -> ML-20, V3-21 -> ML-21, V3-22 -> ML-22, V3-23 -> ML-23, V3-24 -> ML-24
  V3-14 -> ML-21   (course pairs V3-14 with the V3-21 seed: discovery field
                    "Paired with the mechanistic seed V3-21"; the seed's own
                    composition step 5 states the joke phrasing's "non-toxic"
                    qualifier does not change the verdict)
Proposition bytes are the frozen mlogic.tsv rows verbatim (ids renamed);
no new propositions are authored and no verdict column is written --
verdicts come from logic_bin. The oracle field (col 4) is inert for the
engine (it parses fields 0-2 only) and is kept for scoring.
"""
import sys

C2B = "/home/hatch/workspace/scratch-hellhole/crews/c2/batteries/mlogic.tsv"
OUT = sys.argv[1] if len(sys.argv) > 1 else "r6_v4_input.tsv"

rows = {}
for ln in open(C2B, encoding="utf-8"):
    p = ln.rstrip("\n").split("\t")
    assert len(p) == 4, p
    rows[p[0]] = (p[1], p[2], p[3])

SEED = {"V3-20": "ML-20", "V3-21": "ML-21", "V3-22": "ML-22",
        "V3-23": "ML-23", "V3-24": "ML-24", "V3-14": "ML-21"}

with open(OUT, "w", encoding="utf-8") as f:
    for cid in ["V3-14", "V3-20", "V3-21", "V3-22", "V3-23", "V3-24"]:
        claim, ev, oracle = rows[SEED[cid]]
        assert oracle == "2", (cid, oracle)
        f.write("R6-%s\t%s\t%s\t%s\n" % (cid, claim, ev, oracle))
print("wrote", OUT, "6 rows")
