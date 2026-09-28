#!/usr/bin/env python3
"""Analyze class3-standardized run logs: verify N=5 byte-identity, compute
composites with the teach3 operationalization, and compare across sources.
"""
import glob
import hashlib
import os
import re
import sys

EV = "/home/hatch/workspace/tnn-lab/wave12/championship/class3-standardized/evidence"

def parse_result(path):
    d = {}
    digest = None
    for line in open(path):
        line = line.strip()
        if line.startswith("S37_TEACH3C_RESULT,"):
            for kv in line.split(",")[4:]:
                pass
            # manual parse: k,v pairs after label,rep,N
            parts = line.split(",")
            it = iter(parts[4:])
            for k in it:
                v = next(it)
                d[k] = int(v)
        elif line.startswith("S37_DIGESTC,"):
            digest = line.split(",")[-1]
    return d, digest

def composite(r):
    m = r["m1"] / 192
    rev = r["ws_revise"] / 32
    integ = (r["b7_hits"] / 96 + (1 if r["leak"] == 0 else 0) + (1 if r["tripwire"] == 0 else 0)) / 3
    ret = min(1.0, r["m2"] / r["m1"]) if r["m1"] else 0.0
    cost = 1 / (1 + 0.1 * r["ops"] / r["eps"])
    comp = 0.30 * m + 0.25 * rev + 0.25 * integ + 0.10 * ret + 0.10 * cost
    return m, rev, integ, ret, cost, comp

print(f"{'src':5} {'rep':3} {'m1':3} {'ws':2} {'b7':2} {'sk':2} {'m2':3} {'ops':3} {'eps':3} {'cost':6} {'composite':9} digest")
print("-" * 100)
results = {}
for src in ["grok", "sol", "step", "swe"]:
    logs = sorted(glob.glob(os.path.join(EV, f"{src}_rep*.log")))
    if not logs:
        print(f"{src:5} NO LOGS")
        continue
    # byte-identity across reps (strip the rep number from comparison)
    bodies = []
    for lg in logs:
        txt = open(lg).read()
        # normalize rep number for cross-rep comparison
        norm = re.sub(r",rep,\d+,", ",rep,N,", txt)
        norm = re.sub(r"rep \d+ exit", "rep N exit", norm)
        bodies.append(hashlib.sha256(norm.encode()).hexdigest())
    ident = "IDENTICAL" if len(set(bodies)) == 1 else "DIFFER"
    digests = set()
    for i, lg in enumerate(logs):
        r, dg = parse_result(lg)
        digests.add(dg)
        m, rev, integ, ret, cost, comp = composite(r)
        results[(src, i)] = comp
        print(f"{src:5} {i:3} {r['m1']:3} {r['ws_revise']:2} {r['b7_hits']:2} {r['skipped']:2} "
              f"{r['m2']:3} {r['ops']:3} {r['eps']:3} {cost:.4f} {comp:.4f}     {dg[:12]}")
    print(f"      N=5 cross-rep: {ident}; digests across reps: {len(digests)} unique")

# cross-source digest comparison
print()
print("Cross-source learner digests (rep 0):")
for src in ["grok", "sol", "step", "swe"]:
    r, dg = parse_result(os.path.join(EV, f"{src}_rep0.log")) if os.path.exists(os.path.join(EV, f"{src}_rep0.log")) else ({}, None)
    print(f"  {src:5} {dg}")
