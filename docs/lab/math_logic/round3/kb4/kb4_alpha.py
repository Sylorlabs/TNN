#!/usr/bin/env python3
"""Krippendorff's alpha (ordinal) for MATH R3 KB4 grading.

Usage: kb4_alpha.py KB4_GRADES_A_V2.json KB4_GRADES_B_V2.json KB4_GRADES_C_V2.json
Prints per-dimension alpha and the pooled alpha. Prereg bar: alpha > 0.8 or VOID.
"""
import json, sys
from itertools import combinations

def load(fn):
    d = json.load(open(fn))
    return {s['tid']: s for s in d['scores']}

def ordinal_alpha(ratings):
    """ratings: list of items, each a list of grader scores (1-5, None if missing).
    Krippendorff's alpha with ordinal difference metric."""
    # coincidence matrix over value pairs
    vals = []
    for item in ratings:
        r = [x for x in item if x is not None]
        vals.extend(r)
    if not vals:
        return float('nan')
    # metric: squared difference normalized
    def delta(a, b):
        return (a - b) ** 2
    # observed disagreement
    Do_num, Do_den = 0.0, 0
    # all pairable values for expected disagreement
    n = 0
    De_num = 0.0
    for item in ratings:
        r = [x for x in item if x is not None]
        for a, b in combinations(r, 2):
            Do_num += delta(a, b)
            Do_den += 1
        n += len(r)
    if Do_den == 0 or n < 2:
        return float('nan')
    Do = Do_num / Do_den
    for a, b in combinations(vals, 2):
        De_num += delta(a, b)
    De = De_num / (len(vals) * (len(vals) - 1) / 2)
    if De == 0:
        return 1.0 if Do == 0 else float('nan')
    return 1.0 - Do / De

def main():
    graders = [load(f) for f in sys.argv[1:]]
    tids = sorted(set.intersection(*[set(g.keys()) for g in graders]))
    print(f"common tids: {len(tids)}, graders: {len(graders)}")
    dims = ['circularity', 'unwarranted', 'magic', 'honesty']
    alphas = {}
    for dim in dims:
        ratings = [[g[t][dim] for g in graders] for t in tids]
        a = ordinal_alpha(ratings)
        alphas[dim] = a
        print(f"alpha[{dim}] = {a:.4f}")
    # pooled: concatenate all dimensions' ratings
    pooled = []
    for dim in dims:
        pooled.extend([[g[t][dim] for g in graders] for t in tids])
    ap = ordinal_alpha(pooled)
    print(f"alpha[pooled] = {ap:.4f}")
    print("KB4 COHERENCE:", "PASS" if ap > 0.8 else "VOID (alpha <= 0.8)")

if __name__ == '__main__':
    main()
