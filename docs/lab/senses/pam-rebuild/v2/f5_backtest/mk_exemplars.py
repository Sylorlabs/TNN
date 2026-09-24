#!/usr/bin/env python3
"""F5 backtest: extract the frozen 6-exemplar bank from the R2-4 clean sweep.

Frozen filter (from PREREG_F5_BACKTEST.md):
  10983 <= seq <= 11192 AND judgment=="RICH" AND truth=="BRIGHT"
  AND 701 <= conf <= 718 AND 353 <= mrgF <= 382
Writes v2/f5_backtest/exemplars.tsv: seq, fam, conf, measure (tab-separated, header).
Deterministic. Asserts exactly 6 rows.
"""
import json
import os
import sys

BASE = os.path.expanduser("~/workspace/tnn-lab/senses/pam-rebuild")
SRC = os.path.join(BASE, "round2/forks/R2-4/evidence/clean/sweep.jsonl")
OUT = os.path.join(BASE, "v2/f5_backtest/exemplars.tsv")

rows = []
with open(SRC) as f:
    for line in f:
        r = json.loads(line)
        if (10983 <= r["seq"] <= 11192 and r["judgment"] == "RICH"
                and r["truth"] == "BRIGHT" and 701 <= r["conf"] <= 718
                and 353 <= r["mrgF"] <= 382):
            rows.append(r)

if len(rows) != 6:
    sys.exit(f"FATAL: filter yielded {len(rows)} rows, expected 6")

rows.sort(key=lambda r: r["seq"])
with open(OUT, "w") as f:
    f.write("seq\tfam\tconf\tmeasure\n")
    for r in rows:
        f.write(f"{r['seq']}\t{r['fam']}\t{r['conf']}\t{r['measure']}\n")
print("wrote", OUT, "rows:", len(rows))
for r in rows:
    print(r["seq"], r["fam"], r["conf"], r["measure"])
