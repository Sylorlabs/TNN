#!/usr/bin/env python3
"""Decompose F33 V2 theater: which keys/families, and delta-rise vs pi-drop."""
import csv, glob, os, re, sys
from collections import defaultdict

resdir = sys.argv[1]
txt = open(sys.argv[2]).read()
delta = {}
for m in re.finditer(r"if\(key==(\d+)\)\{((?:if\(di==\d+\)\{return -?\d+;\})+)\}", txt):
    for d, v in re.findall(r"if\(di==(\d+)\)\{return (-?\d+);\}", m.group(2)):
        delta[(int(m.group(1)), int(d))] = int(v)
state = {}
for row in csv.reader(open(os.path.join(resdir, ".f33state_A.tsv")), delimiter='\t'):
    state[row[0]] = (int(row[1]), int(row[2]))

def dslot(d): return {1:0,2:1,4:2,8:3,16:4,32:5,64:6}[d]

seq = defaultdict(dict); famof = {}
for fn in glob.glob(os.path.join(resdir, "*_m33_d*_A.tsv")):
    base = os.path.basename(fn)
    fam = base.split("_m33")[0]
    d = int(base.split("_d")[1].split("_")[0])
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        if len(c) < 9: continue
        seq[(fam, c[0])][d] = (c[7], int(c[8]))

v2key = defaultdict(int); v2fam = defaultdict(int)
v2_delta_pos = defaultdict(int); v2_delta_nonpos = defaultdict(int)
for (fam, iid), dd in seq.items():
    if iid not in state: continue
    m, s = state[iid]; key = m*4+s
    ds = sorted(dd)
    for a, b in zip(ds, ds[1:]):
        ca, fa = dd[a]; cb, fb = dd[b]
        if ca == "0" and cb == "0" and fb > fa:
            v2key[key] += 1; v2fam[fam] += 1
            cum = sum(delta.get((key, j), 0) for j in range(1, dslot(b)+1))
            cump = sum(delta.get((key, j), 0) for j in range(1, dslot(a)+1))
            if cum - cump > 0: v2_delta_pos[key] += 1
            else: v2_delta_nonpos[key] += 1
print("V2 by key:", dict(sorted(v2key.items())))
print("V2 by family:", dict(sorted(v2fam.items())))
print("total V2:", sum(v2key.values()))
print("V2 with rising cum(delta):", dict(sorted(v2_delta_pos.items())))
print("V2 with non-rising cum(delta) (pi-drop driven):", dict(sorted(v2_delta_nonpos.items())))
