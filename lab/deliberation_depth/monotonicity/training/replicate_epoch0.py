#!/usr/bin/env python3
"""Replicate train.zag epoch 0 (phase 0) with CORRECT f1..f8 indices.
If the fixed binary's logged epoch-0 loss matches, the parser reads f1..f8."""
import math, sys

def tdiv(a, b):
    # truncation toward zero, b>0
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b >= 0) else -q

def clamp(v, lo, hi): return max(lo, min(hi, v))

def phase_of(fam, split):
    if fam in ('P', 'D', 'O'): return 2 if split == 0 else -1
    return {'admit': 0, 'revoke': 0, 'logic': 0, 'cost': 0, 'trap': 2, 'redteam': 2}[fam]

DIV = 4000000
cells = []
for line in open(sys.argv[1]):
    f = line.rstrip('\n').split('\t')
    fam, split, depth, t, rel = f[1], int(f[2]), int(f[3]), int(f[4]), int(f[5])
    ph = phase_of(fam, split)
    if ph < 0: continue
    y = -1
    if rel == 1:
        y = 1 if f[6] == '1' else 0
    feats = [int(x) for x in f[7:15]]  # CORRECT indices
    cells.append(dict(ph=ph, rel=rel, y=y, feats=feats, depth=depth,
                      fam=fam, id=f[0]))

w = [1000] + [0]*7
b = 0
loss = 0
v2c = 0
prev = {}  # id -> (cprev, yprev)
for c in cells:
    if c['ph'] != 0 or c['rel'] != 1: continue
    y = c['y']; yy = 1000 if y == 1 else 0
    feats = c['feats']
    acc = sum(wi*fi for wi, fi in zip(w, feats))
    cc = clamp(tdiv(acc, 1000) + b, 0, 1000)
    err = cc - yy
    rise = 0
    if c['id'] in prev:
        pc, py = prev[c['id']]
        if y == 0 and py == 0 and cc > pc:
            rise = cc - pc; v2c += 1
    yw = 1 if y == 0 else 0
    loss += err*err + 2*yw*cc*cc + 4*rise*rise
    for k in range(8):
        fk = feats[k]
        num = 2*err*fk + 4*yw*cc*fk + 8*rise*fk
        w[k] = w[k] - tdiv(num, DIV)
    nb = 2*err*1000 + 4*yw*cc*1000 + 8*rise*1000
    b = b - tdiv(nb, DIV)
    prev[c['id']] = (cc, y)

print("replicated epoch0 phase0 loss =", loss, "v2 =", v2c, "b =", b, "w =", w)
print("binary log will show epoch0 loss/v2/b for comparison")
