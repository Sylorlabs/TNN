#!/usr/bin/env python3
"""Deterministic scale-input generator: sequential replication of necc_input.tsv.
IDs suffixed #s10rNN / #s100rNNN (sequential passes). Family/depth/f1/f5/
release/correct identical per pass. Row order: pass-major (all s1 rows of
pass 0, then pass 1, ...) -- matches the v1/v2 scale precedent.
Usage: gen_scale.py <necc_input.tsv> <10|100> <out.tsv>
"""
import sys
inp, scale, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rows = [l.rstrip("\n") for l in open(inp) if l.strip()]
w = 2 if scale == 10 else 3
tag = "s10" if scale == 10 else "s100"
with open(outp, "w") as f:
    for r in range(scale):
        suf = f"#{tag}r{r:0{w}d}"
        for line in rows:
            c = line.split("\t")
            f.write(f"{c[0]}{suf}\t{c[1]}\t{c[2]}\t{c[3]}\t{c[4]}\t{c[5]}\t{c[6]}\n")
print(f"wrote {len(rows)*scale} rows to {outp}")
