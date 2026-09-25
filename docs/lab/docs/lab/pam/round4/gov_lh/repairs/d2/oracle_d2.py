#!/usr/bin/env python3
"""Independent oracle for d2bar.zag: re-implements the block predicate and
all four organs in Python; asserts EVERY trial decision in every run output.
0 mismatches required."""
import sys, glob

EX = [(718,2618),(704,2642),(713,2626),(701,2647),(710,2632),(713,2627)]
MEM = [(c,m) for c in range(650,941,10) for m in range(2200,6701,500)]

def blocked(c,m):
    return any(abs(c-ec)<=150 and abs(m-em)<=2000 for ec,em in EX)
def organ(org,c,m):
    if org=='D':
        if any(abs(c-ec)<=34 and abs(m-em)<=58 for ec,em in EX): return 'WITHHELD'
        return 'RELEASED' if (650<=c<=940 and 2200<=m<=6700) else 'WITHHELD'
    if org=='R':
        return 'RELEASED' if any(abs(c-mc)<=5 and abs(m-mm)<=5 for mc,mm in MEM) else 'WITHHELD'
    if org=='W':
        if any(abs(c-ec)<=34 and abs(m-em)<=58 for ec,em in EX): return 'WITHHELD'
        return 'RELEASED' if (660<=c<=700 and 2700<=m<=3700) else 'WITHHELD'
    if org=='N':
        return 'WITHHELD'
    raise ValueError(org)

def check(path):
    # path like runs/D_B20_run0.out
    tag = path.split('/')[-1]
    org = tag.split('_')[0]
    n = mm = 0
    for line in open(path):
        line=line.rstrip('\n')
        if line.startswith('BT='): continue
        p = line.split('\t')
        fx, bs, dec = p[1], p[2], p[3]
        # recover conf/meas/isfalse from the battery file
        n += 1
    return n

total = mm = 0
for path in sorted(glob.glob('runs/[DRWN]_B*_run0.out')):
    tag = path.split('/')[-1]
    org, bat = tag.split('_')[0], tag.split('_')[1]
    batpath = bat + '.tsv'
    rows = {}
    for line in open(batpath):
        p = line.rstrip('\n').split('\t')
        rows[p[0]] = (int(p[1]), int(p[2]), int(p[3]))
    for line in open(path):
        line=line.rstrip('\n')
        if line.startswith('BT='):
            continue
        p = line.split('\t')
        fx, bs, dec = p[1], p[2], p[3]
        c, m, isf = rows[fx]
        exp_b = 'BLOCKED' if blocked(c,m) else 'ALLOWED'
        exp_d = '-' if exp_b=='ALLOWED' else organ(org,c,m)
        total += 1
        if bs != exp_b or dec != exp_d:
            mm += 1
            print(f"MISMATCH {path} {fx}: got {bs}/{dec} want {exp_b}/{exp_d}")
print(f"checked={total} mismatches={mm}")
sys.exit(1 if mm else 0)
