#!/usr/bin/env python3
"""White-box MDUMP analysis from committed run outputs.
MDUMP|concept+1|field|status|support|bytes  (field 0=UTT 1=CTX 2=SPK; status 1=PROV 2=COMMIT 3=REVOKED)
Concepts (1-based as printed): 1=sarcasm 2=joke 3=hypothetical 4=quotation 5=metaphor.
"""
import os, sys

RUNS = os.path.expanduser("~/workspace/redteam_exp2c/evidence/runs")

def mdump(fn):
    d = {}
    with open(os.path.join(RUNS, fn)) as f:
        for line in f:
            if line.startswith("MDUMP|"):
                p = line.rstrip("\n").split("|")
                d[(int(p[1]), int(p[2]), p[5])] = (int(p[3]), int(p[4]))
    return d

def show(fn, concept=None, field=None, status=None, contains=None):
    d = mdump(fn)
    rows = []
    for (c, f, b), (st, sup) in sorted(d.items()):
        if concept and c != concept: continue
        if field is not None and f != field: continue
        if status and st != status: continue
        if contains and contains not in b: continue
        rows.append((c, f, st, sup, b))
    return rows

which = sys.argv[1] if len(sys.argv) > 1 else "diff"
if which == "diff":
    # abc-a vs abc-b: joke CTX markers
    for fn, label in [("abc_a_rep1.txt", "abc-a(alpha)"), ("abc_b_rep1.txt", "abc-b(beta)")]:
        print(f"=== {label}: concept=2(joke) CTX markers ===")
        for c, f, st, sup, b in show(fn, concept=2, field=1):
            stn = {1: "PROV", 2: "COMMIT", 3: "REVOKED"}.get(st, st)
            print(f"  {stn:8s} sup={sup:4d} [{b}]")
        print()
elif which == "calib":
    for fn in ["abc_a_rep1.txt", "abc_b_rep1.txt", "vol_a_rep1.txt", "vol_b_rep1.txt",
               "vol2_a_rep1.txt", "vol2_b_rep1.txt", "ab_a_rep1.txt", "ab_b_rep1.txt",
               "de_a_rep1.txt", "base_rep1.txt"]:
        with open(os.path.join(RUNS, fn)) as f:
            for line in f:
                if line.startswith("2CCALIB|"):
                    print(fn, line.strip())
elif which == "hyp3":
    # hypothetical UTT markers status in base vs ab-a vs abc-b
    for fn, label in [("base_rep1.txt", "base"), ("ab_a_rep1.txt", "ab-a"),
                      ("abc_b_rep1.txt", "abc-b"), ("vol2_b_rep1.txt", "vol2-b")]:
        print(f"=== {label}: concept=3(hyp) UTT markers with status != 3 (top 40 by support) ===")
        rows = [r for r in show(fn, concept=3, field=0) if r[2] != 3]
        rows.sort(key=lambda r: -r[3])
        for c, f, st, sup, b in rows[:40]:
            stn = {1: "PROV", 2: "COMMIT", 3: "REVOKED"}.get(st, st)
            print(f"  {stn:8s} sup={sup:4d} [{b}]")
        print()
