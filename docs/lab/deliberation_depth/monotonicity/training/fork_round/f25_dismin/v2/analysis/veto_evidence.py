#!/usr/bin/env python3
"""F25 v2 veto-evidence analysis (independent Python re-computation).

Recomputes, from features.tsv + the FIT (pre-shift) params, the final-veto
statistics the Zag trainer reported: V1 theater count, V2 meanConfCorrect,
V3 slot violations per head. Integer semantics mirror the Zag trainer:
tdiv = truncation toward zero, clamp to [0,1000].
"""
import sys
from collections import defaultdict

TR = "/home/hatch/workspace/tnn-lab/deliberation_depth/monotonicity/training"
V2 = TR + "/fork_round/f25_dismin/v2"
FEATS = TR + "/features/features.tsv"

FAMS = ["admit","revoke","logic","cost","trap","redteam","P","D","O"]
DSLOTS = [1,2,4,8,16,32,64]

# fit params (pre-shift), from the trainer log / params file
PA = [472, 472, 453, 0, 239]      # a0..a4 (fit)
PB = [404, 336, 205, 472, 351]    # b0..b4 (fit)

def tdiv(a, b):
    q = abs(a) // b
    return -q if a < 0 else q

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def conf(p, f, base):
    acc = p[1]*f[base] + p[2]*f[base+1] + p[3]*f[base+2] + p[4]*f[base+3]
    return clamp(tdiv(acc, 1000) + p[0], 0, 1000)

cells = []  # (id, fam, depth, y, f[8])
with open(FEATS) as fh:
    for line in fh:
        line = line.rstrip("\n")
        if not line:
            continue
        c = line.split("\t")
        iid, fam, heldout, depth = c[0], c[1], int(c[2]), int(c[3])
        rel4, c4 = int(c[5]), c[6]
        if heldout == 0 and rel4 == 1:
            y = 1 if c4 == "1" else 0
            f = [int(x) for x in c[7:15]]
            cells.append((iid, fam, depth, y, f))
print(f"training released cells: {len(cells)}")

for tag, p, base in (("A", PA, 0), ("B", PB, 4)):
    C = [conf(p, f, base) for (_, _, _, _, f) in cells]
    # V2: meanConfCorrect
    sc = sum(c for c, (_, _, _, y, _) in zip(C, cells) if y == 1)
    nc = sum(1 for (_, _, _, y, _) in cells if y == 1)
    mcc = sc / (1000.0 * nc)
    # V3: per (family,depth) G
    slot = defaultdict(lambda: [0, 0, 0])  # (fam,depth) -> [sumC, n, sumY]
    for (iid, fam, depth, y, f), c in zip(cells, C):
        k = (fam, depth)
        slot[k][0] += c; slot[k][1] += 1; slot[k][2] += y
    v3 = []
    for k in sorted(slot):
        s, n, sy = slot[k]
        if n >= 8:
            g = (s - 1000 * sy) / n / 1000.0
            if g < -0.080:
                v3.append((k, n, g, sy / n))
    # V1: theater on prev-chains (nearest previous same-id cell)
    last = {}
    v1 = v2t = 0
    for idx, (iid, fam, depth, y, f) in enumerate(cells):
        if iid in last:
            pidx = last[iid]
            yp = cells[pidx][3]
            cp = C[pidx]
            ci = C[idx]
            if yp == 1 and y == 0 and ci >= cp:
                v1 += 1
            if yp == 0 and y == 0 and ci > cp:
                v2t += 1
        last[iid] = idx
    print(f"head {tag}: V1+V2={v1+v2t} (V1={v1},V2={v2t}) "
          f"meanConfCorrect={mcc:.4f} (n_correct={nc}) v2ok={mcc>=0.55}")
    print(f"  V3-violating slots (n_rel>=8, G<-0.080): {len(v3)}")
    for k, n, g, acc in v3:
        print(f"    {k}: n={n} G={g:+.4f} acc={acc:.3f}")
    # weight pattern summary
    print(f"  params(bias,w1..w4)={p}")
print("done")
