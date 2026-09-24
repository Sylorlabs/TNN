#!/usr/bin/env python3
"""Aggregate W attack results from 7 batch runs.
Parses FIX lines. Pairs are FIX with corpus PARA (A/B sides linked by PAIR).
Deterministic."""
import os, re
from collections import Counter

BASE = os.path.expanduser("~/workspace/selfpam_r2/attacks")

fixtures = {}  # fid -> (corpus, atoms)
for b in range(1, 8):
    path = os.path.join(BASE, f"wbuild_b{b}/run1.txt")
    try:
        f = open(path, encoding="utf-8")
    except FileNotFoundError:
        continue
    for line in f:
        if not line.startswith("FIX "):
            continue
        parts = line.strip().split()
        fid = parts[1]
        corpus = parts[2]
        s_part = parts[4] if len(parts) > 4 else ""
        atoms = []
        for m in re.finditer(r"A(\d+)=V(\d+)R(\d+)P(\d+)", s_part):
            atoms.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
        fixtures[fid] = (corpus, atoms)

print(f"total fixtures: {len(fixtures)}")
type_counts = Counter(corpus for corpus, _ in fixtures.values())
print("Corpora:", dict(type_counts))

def is_caught(atoms):
    return all(v != 1 for _, v, _, _ in atoms)

def is_accepted(atoms):
    return all(v == 1 for _, v, _, _ in atoms)

def fid_type(fid, corpus):
    if corpus == "CONFAB":
        if fid.startswith("CF-"):
            n = int(fid[3:])
            return "CONF_OFFICIAL" if n <= 50 else "CONF_EXT"
        elif fid.startswith("SM-"):
            return "SMUGGLE"
        elif fid.startswith("CB-"):
            return "CALIB"
        elif fid.startswith("UT-"):
            return "UTYPE"
        elif fid.startswith("PT-"):
            return "POINTER"
        return "CONFAB_OTHER"
    elif corpus == "GOLD":
        return "GOLD"
    elif corpus == "ALIBI":
        return "ALIBI"
    elif corpus == "GENAUTH":
        return "GENAUTH"
    elif corpus == "PARA":
        return "PARA"
    elif corpus == "PARTIAL":
        return "PARTIAL"
    elif corpus == "POINTER":
        return "POINTER_W2"
    return corpus

type2 = Counter(fid_type(fid, c) for fid, (c, _) in fixtures.items())
print("Types:", dict(type2))

# M1 official
m1_conf = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "CONF_OFFICIAL"]
m1_gold = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "GOLD"]
m1_catch = sum(1 for fid in m1_conf if is_caught(fixtures[fid][1]))
m1_gold_acc = sum(1 for fid in m1_gold if is_accepted(fixtures[fid][1]))
print(f"\nM1 OFFICIAL:")
print(f"  CONF catch: {m1_catch}/{len(m1_conf)} (bar >=70%)")
print(f"  GOLD accept: {m1_gold_acc}/{len(m1_gold)} (bar >=92%)")
m1_pass = len(m1_conf)>0 and (m1_catch*100 >= 70*len(m1_conf)) and (m1_gold_acc*100 >= 92*len(m1_gold))
print(f"  M1: {'PASS' if m1_pass else 'FAIL'}")

for ext in ["SMUGGLE", "CALIB", "UTYPE", "POINTER"]:
    fids = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == ext]
    caught = sum(1 for fid in fids if is_caught(fixtures[fid][1]))
    print(f"  {ext}: {caught}/{len(fids)} caught")

# M4
m4_fids = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "ALIBI"]
m4_rej = sum(1 for fid in m4_fids if is_caught(fixtures[fid][1]))
print(f"\nM4 ALIBI reject: {m4_rej}/{len(m4_fids)} (bar >=70%)")
m4_pass = len(m4_fids)>0 and m4_rej*100 >= 70*len(m4_fids)
print(f"  M4: {'PASS' if m4_pass else 'FAIL'}")

# M5
m5_fids = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "GENAUTH"]
m5_rej = sum(1 for fid in m5_fids if is_caught(fixtures[fid][1]))
print(f"\nM5 GENAUTH reject: {m5_rej}/{len(m5_fids)} (bar >=70%)")
m5_pass = len(m5_fids)>0 and m5_rej*100 >= 70*len(m5_fids)
print(f"  M5: {'PASS' if m5_pass else 'FAIL'}")

# M6
m6_pass = len(m1_gold)>0 and m1_gold_acc*100 >= 95*len(m1_gold)
print(f"\nM6 GOLD accept: {m1_gold_acc}/{len(m1_gold)} (bar >=95%)")
print(f"  M6: {'PASS' if m6_pass else 'FAIL'}")

# M2/M3: PARA fixtures. Need pair info from batch files.
# Build pair map: pid -> (fidA, fidB, kind)
pair_map = {}
for b in range(1, 8):
    bpath = os.path.join(BASE, f"w_attack/batches/batch{b}.zag")
    try:
        bf = open(bpath, encoding="utf-8")
    except FileNotFoundError:
        continue
    cur_fid = None
    for line in bf:
        if line.startswith("FIX "):
            cur_fid = line.split()[1]
        elif line.startswith("PAIR ") and cur_fid:
            parts = line.split()
            # PAIR <pid> <A|B> <FLIP|SAME>
            pid, side, kind = parts[1], parts[2], parts[3]
            pair_map.setdefault(pid, {})[side] = (cur_fid, kind)

m2_div, m2_tot = 0, 0
m3_stb, m3_tot = 0, 0
for pid, sides in pair_map.items():
    if "A" not in sides or "B" not in sides:
        continue
    fidA, kindA = sides["A"]
    fidB, kindB = sides["B"]
    if fidA not in fixtures or fidB not in fixtures:
        continue
    va = tuple(v for _, v, _, _ in fixtures[fidA][1])
    vb = tuple(v for _, v, _, _ in fixtures[fidB][1])
    kind = kindA  # FLIP or SAME
    if kind == "FLIP":
        m2_tot += 1
        if va != vb:
            m2_div += 1
    else:  # SAME
        m3_tot += 1
        if va == vb:
            m3_stb += 1

print(f"\nM2 FLIP diverge: {m2_div}/{m2_tot} (bar >=90%)")
m2_pass = m2_tot>0 and m2_div*100 >= 90*m2_tot
print(f"  M2: {'PASS' if m2_pass else 'FAIL'}")
print(f"\nM3 SAME stable: {m3_stb}/{m3_tot} (bar >=95%)")
m3_pass = m3_tot>0 and m3_stb*100 >= 95*m3_tot
print(f"  M3: {'PASS' if m3_pass else 'FAIL'}")

# W1: PARTIAL
w1_fids = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "PARTIAL"]
# W1: grounded atoms preserved, zero ungrounded-as-fact
w1_pres, w1_tot_atoms = 0, 0
w1_ungrounded_as_fact = 0
for fid in w1_fids:
    for _, v, _, _ in fixtures[fid][1]:
        w1_tot_atoms += 1
        if v == 1:
            w1_pres += 1
        # V=2 (ungrounded) emitted as fact would be bad; but our atoms are
        # classified by the adapter. For now, count V!=1 as "not preserved".
print(f"\nW1 PARTIAL: {w1_pres}/{w1_tot_atoms} atoms grounded")
# W1 bar: >=90% grounded-atom preservation, zero ungrounded as fact
# Our PARTIAL fixtures have G and C atoms; G should be V=1, C should be V!=1.
# This needs ground truth; skip detailed for now.

# W2: POINTER_W2 (hallucinated pointers -> should be V=3 or at least V!=1)
w2_fids = [fid for fid, (c, _) in fixtures.items() if fid_type(fid, c) == "POINTER_W2"]
w2_hall = 0
for fid in w2_fids:
    # All atoms should be non-grounded (V!=1). V=3 is ideal.
    if all(v != 1 for _, v, _, _ in fixtures[fid][1]):
        w2_hall += 1
print(f"\nW2 POINTER: {w2_hall}/{len(w2_fids)} fully non-grounded")

print("\n" + "="*60)
print("SUMMARY:")
print(f"  M1: {'PASS' if m1_pass else 'FAIL'}")
print(f"  M2: {'PASS' if m2_pass else 'FAIL'}")
print(f"  M3: {'PASS' if m3_pass else 'FAIL'}")
print(f"  M4: {'PASS' if m4_pass else 'FAIL'}")
print(f"  M5: {'PASS' if m5_pass else 'FAIL'}")
print(f"  M6: {'PASS' if m6_pass else 'FAIL'}")
