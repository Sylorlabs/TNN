#!/usr/bin/env python3
"""COL-5 Bayes-ceiling proof (evidence for VERDICT_FE1.md).

Machine-checked claim: NO deterministic function of the COL-5 fixture bytes
reaches the 80% (20/24) separator bar on the frozen 24 fixtures.

Argument:
1. Both COL-5 panels are flat fills (verified per-pixel); the informative
   bytes reduce to two RGB triples: S1 (left, exact) and obs (right).
2. The generator's f64 drift math is replicated bit-exactly (op order
   preserved); validated by recovering each fixture's ground-truth jitter
   j_true (via a Python replica of rt_draw/rt_mix) and showing the replica
   reproduces the observed bytes under the true hypothesis on 24/24 fixtures.
3. obs = F(S1, S2, j), S2 in {S1, S1+(18,-12,+9)}, j in [-5,5]. Any separator
   is a function g(S1, obs) -> {SAME, DIFFERENT}. The accuracy-maximizing g
   is the Bayes rule: predict the hypothesis with more (S1,obs)-consistent
   j preimages (ties -> 0.5 expected). Truth prior is 12/12 on the frozen set.
4. The Bayes rule scores 15.5/24 = 64.6% < 20/24. Since the Bayes rule uses
   full white-box knowledge (true delta, exact f64 model), no byte-function
   with less knowledge can exceed it.

Zero RNG. Deterministic. Emits col5_ceiling.csv + digest.
"""
import sys, os, csv, hashlib

DATA = sys.argv[1]
OUT = sys.argv[2]

MASK = 0x7FFFFFFFFFFFFFFF
def rt_mix(a, b, c):
    z = (a * 1000003 + b * 911 + c * 131 + 12345) & MASK
    z = (z * 6364136223846793005 + 1442695040888963407) & MASK
    z = (z * 6364136223846793005 + 1442695040888963407) & MASK
    z = (z ^ (z >> 33)) & MASK
    return z

def rt_draw(fam, idx, k, m):
    return rt_mix(fam * 7919 + 13, idx + 1, k + 7) % m

def u32(b, at):
    return int(b[at]) | (int(b[at+1]) << 8) | (int(b[at+2]) << 16) | (int(b[at+3]) << 24)

def drift_pred(S2c, j, S1c):
    # bit-exact replica of gen_col5's f64 drift math (op order preserved)
    t = S1c * 255.0 / S2c
    t2 = t + float(j)
    v = S2c * t2 / 255.0
    return int(v)  # truncation == Zag `as i64` for v > 0

def obs_model(S1, S2, j):
    return tuple(drift_pred(S2[c], j, S1[c]) for c in range(3))

DELTA = (18, -12, 9)
rows = ["idx,truth,j_true,bit_exact,n_same,n_diff,bayes_pred,bayes_pts"]
total = 0.0
n_exact = 0
for idx in range(24):
    name = f"rt3_COL-5_{idx:04d}.img"
    p = os.path.join(DATA, name)
    b = open(p, "rb").read()
    w, h = u32(b, 0), u32(b, 4)
    assert (w, h) == (128, 64)
    import numpy as np
    px = np.frombuffer(b, dtype=np.uint8, offset=8).reshape(64, 128, 3)
    L, R = px[:, 0:64, :], px[:, 64:128, :]
    assert (L == L[0, 0]).all() and (R == R[0, 0]).all(), "panel not flat"
    S1 = tuple(int(v) for v in L[0, 0])
    obs = tuple(int(v) for v in R[0, 0])
    truth = open(os.path.join(DATA, name + ".truth")).read().strip().split("=")[1]
    j_true = rt_draw(6, idx, 4, 11) - 5
    h_true = "SAME" if rt_draw(6, idx, 3, 2) == 1 else "DIFFERENT"
    assert h_true == truth, "rt_draw replica disagrees with truth sidecar"
    S2t = S1 if h_true == "SAME" else tuple(S1[c] + DELTA[c] for c in range(3))
    exact = obs_model(S1, S2t, j_true) == obs
    n_exact += 1 if exact else 0
    ns = sum(1 for j in range(-5, 6) if obs_model(S1, S1, j) == obs)
    nd = sum(1 for j in range(-5, 6)
             if obs_model(S1, tuple(S1[c] + DELTA[c] for c in range(3)), j) == obs)
    if ns > nd:
        bp, pts = "SAME", 1.0 if truth == "SAME" else 0.0
    elif nd > ns:
        bp, pts = "DIFFERENT", 1.0 if truth == "DIFFERENT" else 0.0
    else:
        bp, pts = "TIE", 0.5
    total += pts
    rows.append(f"{idx},{truth},{j_true},{int(exact)},{ns},{nd},{bp},{pts}")

with open(OUT, "w") as f:
    f.write("\n".join(rows) + "\n")
print(f"bit-exact f64 replication: {n_exact}/24")
print(f"Bayes-optimal ceiling: {total}/24 = {100.0*total/24:.1f}% (bar: 20/24 = 83.3% for >=80%)")
print("ceiling csv sha256:", hashlib.sha256(open(OUT, "rb").read()).hexdigest())
assert n_exact == 24, "f64 replication failed"
assert total < 20, "ceiling unexpectedly reaches the bar - re-audit!"
