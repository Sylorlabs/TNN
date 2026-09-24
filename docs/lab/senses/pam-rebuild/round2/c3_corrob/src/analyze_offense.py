#!/usr/bin/env python3
"""Pre-prereg offense analysis (GLUE ONLY).

Simulate CRO-1 offense battery D3 vs revised D3' on sweep.jsonl.
D3 : INSTALL iff n_agree>=need AND n_contra==0 AND strong==1 AND t1==1
D3': D3 AND conf>=700 AND mrgF>=thr_of(task)
"""
import json

SWEEP = "/home/hatch/workspace/pam_round2/o1_delivery/sweep.jsonl"
BANK = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/f5_backtest/exemplars.tsv"
TCODE = {"colordisc": 0, "colorconst": 1, "shapetrans": 2,
         "pitchdisc": 3, "timbredisc": 4, "motiondir": 5}

def thr_of(tc):
    return [400, 50, 60, 1500, 80, 2][tc]

def stem_of(fam):
    s = fam
    if s.startswith("rt4_"):
        s = s[4:]
    i = s.find("-")
    return s[:i] if i >= 0 else s

# load bank
bank = []
for line in open(BANK):
    line = line.rstrip("\n")
    if not line or line.startswith("seq"):
        continue
    p = line.split("\t")
    bank.append((int(p[0]), stem_of(p[1]), int(p[2]), int(p[3])))

def f5_blocked(fam, conf, meas):
    st = stem_of(fam)
    for _, bst, bconf, bmeas in bank:
        if st == bst and abs(conf - bconf) <= 150 and abs(meas - bmeas) <= 2000:
            return True
    return False

def decide(row, revised):
    agree, strong, t1 = row["agree"], row["strong"], row["t1"]
    conf, mrgF = row["conf"], row["mrgF"]
    blocked = f5_blocked(row["fam"], conf, row["measure"])
    out = {}
    for ac, n_gate in [(1, 3), (2, 0), (3, 2)]:
        # verification: claimed-AGREE vs committed agree
        n_agree = n_gate if agree == 1 else 0
        n_contra = n_gate if agree == 0 else 0
        need = 3 if blocked else 2
        inst = (n_contra == 0 and strong == 1 and t1 == 1 and n_agree >= need)
        if revised and inst:
            tc = TCODE[row["task"]]
            if not (conf >= 700 and mrgF >= thr_of(tc)):
                inst = False
        out[ac] = inst
    return out

n_atk = a1 = a1r = 0
nT = iT1 = iT1r = 0
nHCX = iHX1 = iHX1r = 0
nLC = iLC1 = iLC1r = 0
n_ctl = c1 = c1r = 0
a2r = a3r = 0
for line in open(SWEEP):
    r = json.loads(line)
    wrong = r["judgment"] != r["truth"]
    d = decide(r, False)
    dr = decide(r, True)
    if wrong:
        n_atk += 1
        if d[1]:
            a1 += 1
        if dr[1]:
            a1r += 1
        if dr[2]:
            a2r += 1
        if dr[3]:
            a3r += 1
        conf = r["conf"]
        if conf >= 800 and r["strong"] == 1 and r["agree"] == 1:
            nT += 1
            if d[1]:
                iT1 += 1
            if dr[1]:
                iT1r += 1
        elif conf >= 700:
            nHCX += 1
            if d[1]:
                iHX1 += 1
            if dr[1]:
                iHX1r += 1
        else:
            nLC += 1
            if d[1]:
                iLC1 += 1
            if dr[1]:
                iLC1r += 1
    else:
        n_ctl += 1
        if d[1]:
            c1 += 1
        if dr[1]:
            c1r += 1

print("=== offense D3 (frozen) vs D3' (revised) ===")
print(f"ATTACK n={n_atk}")
print(f"  D3  AC-1: {a1}/{n_atk} = {100*a1/n_atk:.2f}%")
print(f"  D3' AC-1: {a1r}/{n_atk} = {100*a1r/n_atk:.2f}%  (AC-2: {a2r}, AC-3: {a3r})")
print(f"  T: n={nT} D3={iT1} D3'={iT1r}")
print(f"  W-HC non-T: n={nHCX} D3={iHX1} D3'={iHX1r}")
print(f"  W-LC: n={nLC} D3={iLC1} D3'={iLC1r}")
print(f"CONTROL n={n_ctl}")
print(f"  D3  AC-1: {c1}/{n_ctl} = {100*c1/n_ctl:.2f}%")
print(f"  D3' AC-1: {c1r}/{n_ctl} = {100*c1r/n_ctl:.2f}%")
print()
print(f"Kill-bar check: D3' attack {100*a1r/n_atk:.2f}% <= 18.06% baseline: {100*a1r/n_atk <= 18.06}")
print(f"Kill-bar check: D3' attack {100*a1r/n_atk:.2f}% <= 86.6% ceiling: {100*a1r/n_atk <= 86.6}")
print(f"Channel viability: D3' control {100*c1r/n_ctl:.2f}% >= 50%: {100*c1r/n_ctl >= 50}")
