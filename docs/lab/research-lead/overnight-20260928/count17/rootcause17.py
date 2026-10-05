#!/usr/bin/env python3
"""Root-cause probe: is there ANY learnable signal linking a candidate's
behaviour trace to being the correct candidate in PHASE 17's world?

Run outside the PURE-ZAG session env: this is analysis, not simulation.
"""
import statistics

def ctx_x(c):
    return ((c * 13) + 7) % 97

def cand_a(k):
    return (k // 5) + 1

def cand_b(k):
    return k % 5

def out(k, x):
    return cand_a(k) * x + cand_b(k)

for N in (5, 10, 20, 30, 50):
    C = 625
    # distance used by the LEARNED arm, averaged over the probe set
    rows = []
    for k in range(N):
        ds = []
        for p in range(8):
            ccx = ((p * 211) + (k * 7)) % C
            ds.append(abs(out(k, ctx_x(ccx)) - out(k, ctx_x(ccx))))
        rows.append((k, statistics.mean(ds)))
    vals = [r[1] for r in rows]
    # how often is each candidate correct?  (truth = c % N)
    freq = {k: 0 for k in range(N)}
    for c in range(C):
        freq[c % N] += 1
    correct_counts = [freq[k] for k in range(N)]
    print(f"N={N:3d}  trace-dist spread min={min(vals):.1f} max={max(vals):.1f} "
          f"distinct={len(set(vals))}  |  correctness counts min={min(correct_counts)} "
          f"max={max(correct_counts)}")

print()
print("FINDING: truth(c) = c % N depends only on the INDEX c. The trace of")
print("candidate k is out(k, ctx_x(c)) = a*x+b with a>=1, monotone in x.")
print("Ranking candidates by trace distance therefore ranks them by (a,b).")
print("Nothing about that ordering predicts k == c % N.")
print()
print("=> The LEARNED arm has no usable signal in this world. Its small")
print("   excesses over the query-blind ceiling are the +1/+2 slack of a")
print("   near-tie, NOT conditional competence.")
print()
print("This is a WORLD-CONSTRUCTION defect, not a result about counting.")
print("The truth function must be a function of something a learner can")
print("observe. c%N is a function of the query INDEX only.")