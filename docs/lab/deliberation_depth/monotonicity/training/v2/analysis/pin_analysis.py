#!/usr/bin/env python3
"""v2 pin + non-degeneracy analysis on eval legs.
Joins policy TSVs (id, depth, release, correct, conf) with features.tsv
(id, depth -> f1..f8) and reports:
 - non-degeneracy: mean conf on correct released cells, separation
 - pin: w7 check is in the verdict (params); here: conf on f7=1000 cells
Usage: pin_analysis.py <results_dir> <mech> <features.tsv>
"""
import sys, glob, os
from collections import defaultdict

results_dir, mech, feat_path = sys.argv[1], sys.argv[2], sys.argv[3]

feats = {}
for line in open(feat_path):
    c = line.rstrip('\n').split('\t')
    feats[(c[0], int(c[3]))] = (c[1], list(map(int, c[7:15])), c[6])

n_rel = n_cor = 0
sum_cor = sum_wro = 0
n_wro = 0
f7_cells = []  # (id, fam, depth, correct, conf)
missing = 0
for fn in sorted(glob.glob(os.path.join(results_dir, f"*_m{mech}_d*_A.tsv"))):
    for line in open(fn):
        c = line.rstrip('\n').split('\t')
        iid, depth, rel, cor, conf = c[0], int(c[1]), c[6], c[7], int(c[8])
        if cor not in ('1', '0'):
            continue
        n_rel += 1
        key = (iid, depth)
        f = feats.get(key)
        if f is None:
            missing += 1
            continue
        fam, fv, _ = f
        if cor == '1':
            n_cor += 1; sum_cor += conf
        else:
            n_wro += 1; sum_wro += conf
        if fv[6] == 1000:
            f7_cells.append((iid, fam, depth, cor, conf))

mcC = sum_cor / max(1, n_cor) / 1000
mcW = sum_wro / max(1, n_wro) / 1000
print(f"mech {mech}: released eval cells joined: {n_rel} (missing feats: {missing})")
print(f"NON-DEGENERACY: meanConfCorrect={mcC:.3f} (bar >=0.500: {'PASS' if mcC>=0.50 else 'FAIL'})")
print(f"                meanConfWrong={mcW:.3f} separation={mcC-mcW:.3f} (bar >=0.20: {'PASS' if mcC-mcW>=0.20 else 'FAIL'})")
f7c = [x for x in f7_cells if x[3] == '1']
f7w = [x for x in f7_cells if x[3] == '0']
print(f"PIN: released f7=1000 cells: {len(f7_cells)} ({len(f7c)} correct, {len(f7w)} wrong)")
if f7_cells:
    mcf7 = sum(x[4] for x in f7_cells) / len(f7_cells) / 1000
    accf7 = len(f7c) / len(f7_cells)
    print(f"     meanConf(f7)={mcf7:.3f} acc(f7)={accf7:.3f} inflation={mcf7-accf7:+.3f} (bar <=acc+0.10: {'PASS' if mcf7<=accf7+0.10 else 'FAIL'})")
    if f7c:
        print(f"     meanConf(correct f7)={sum(x[4] for x in f7c)/len(f7c)/1000:.3f}")
    if f7w:
        print(f"     meanConf(wrong f7)={sum(x[4] for x in f7w)/len(f7w)/1000:.3f}")
        print("     wrong f7 cells (id, fam, depth, conf):")
        for x in sorted(f7w, key=lambda z: -z[4])[:20]:
            print(f"       {x[0]} {x[1]} d={x[2]} conf={x[4]}")
print(f"     max conf on wrong f7 cells: {max([x[4] for x in f7w]) if f7w else 'n/a'}")
