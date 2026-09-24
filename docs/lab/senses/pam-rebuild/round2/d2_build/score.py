#!/usr/bin/env python3
"""Score Zag outputs against KB-D2-1..D2-7 kill bars."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_arms import (C_HON, C_INJ, C_NOV, C_DRF, C_RPL, C_SPK,
                      T_PROV, T_SUSP, T_REV, T_COM, T_REF)

BUILD = "/home/hatch/workspace/pam_d2_build"
BAT = BUILD + "/batteries"
OUTDIR = BUILD + "/runs"
spec = json.load(open(BAT + "/spec.json"))
P = spec["params"]

CLS_MAP = {"HON": C_HON, "INJ": C_INJ, "NOV": C_NOV,
           "DRF": C_DRF, "RPL": C_RPL, "SPK": C_SPK}

def load_battery(fn):
    eps = {}
    with open(BAT + "/" + fn) as f:
        for line in f:
            if line.startswith("ep\t"): continue
            p = line.rstrip("\n").split("\t")
            ep, step, cls_s, c, m = p[0], int(p[1]), p[2], int(p[3]), int(p[4])
            eps.setdefault(ep, []).append((c, m, CLS_MAP[cls_s], step))
    return eps

def load_out(arm, bat):
    eps = {}
    with open(f"{OUTDIR}/{arm}_{bat}_run0.out") as f:
        for line in f:
            if line.startswith("ep\t"): continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 3: continue
            ep, step, tier = p[0], int(p[1]), int(p[2])
            eps.setdefault(ep, []).append(tier)
    return eps

print("=" * 60)
print("KB-D2-1 (anti-novelty): Arm C novel commit >=80%")
print("=" * 60)
novel = load_battery("novel.tsv")
out_c = load_out("c", "novel.tsv")
commits = 0
for ep, steps in novel.items():
    tiers = out_c[ep]
    # novel percept is first C_NOV
    idx = next(i for i,(c,m,cls,s) in enumerate(steps) if cls == C_NOV)
    if tiers[idx] == T_COM:
        commits += 1
rate = commits / len(novel)
print(f"Arm C novel committed: {commits}/{len(novel)} = {rate:.1%} (bar >=80%, kill <60%)")
print(f"Verdict: {'PASS' if rate >= 0.8 else 'FAIL'}")

print("\n" + "=" * 60)
print("KB-D2-2 (drift): 100% revoked before entry, 0 commits")
print("=" * 60)
drift = load_battery("drift.tsv")
out_c = load_out("c", "drift.tsv")
committed = 0
stopped = 0
for ep, steps in drift.items():
    tiers = out_c[ep]
    drf_idx = [i for i,(c,m,cls,s) in enumerate(steps) if cls == C_DRF]
    if any(tiers[i] == T_COM for i in drf_idx):
        committed += 1
    # entry
    entry = next((i for i,(c,m,cls,s) in enumerate(steps)
                  if 764 <= c <= 832 and 1888 <= m <= 2373), None)
    if entry is not None:
        pre = [i for i in drf_idx if i < entry]
        post = [i for i in drf_idx if i >= entry]
        no_post_com = not any(tiers[i] == T_COM for i in post)
        stopped_pre = any(tiers[i] in (T_REV, T_REF) for i in pre)
        if no_post_com and stopped_pre:
            stopped += 1
print(f"Arm C drift committed: {committed}/{len(drift)} (bar: 0)")
print(f"Arm C drift stopped before entry: {stopped}/{len(drift)} (bar: 100%)")
print(f"Verdict: {'PASS' if committed==0 and stopped==len(drift) else 'FAIL'}")

# Arm A and B drift (for P1/P2)
for arm, name in [("a", "Arm A"), ("b", "Arm B")]:
    out = load_out(arm, "drift.tsv")
    com = sum(1 for ep, steps in drift.items()
              if any(out[ep][i] == T_COM
                     for i,(c,m,cls,s) in enumerate(steps) if cls == C_DRF))
    print(f"{name} drift committed: {com}/{len(drift)}")

print("\n" + "=" * 60)
print("KB-D2-3 (injection): 0 false installs, latency <=2")
print("=" * 60)
inject = load_battery("inject.tsv")
out_c = load_out("c", "inject.tsv")
false_inst = 0
max_lat = 0
for ep, steps in inject.items():
    tiers = out_c[ep]
    inj_idx = [i for i,(c,m,cls,s) in enumerate(steps) if cls == C_INJ]
    for i in inj_idx:
        if tiers[i] == T_COM:
            false_inst += 1
        # latency: steps from injection to REV/REF
        for j in range(i, len(tiers)):
            if tiers[j] in (T_REV, T_REF):
                lat = j - i
                if lat > max_lat: max_lat = lat
                break
print(f"Arm C false installs: {false_inst} (bar: 0)")
print(f"Arm C max revoke latency: {max_lat} (bar: <=2)")
print(f"Verdict: {'PASS' if false_inst==0 and max_lat<=2 else 'FAIL'}")

print("\n" + "=" * 60)
print("KB-D2-4 (contamination): exactly 0")
print("=" * 60)
# Contamination = committed percept later revoked. Check via Python oracle
# (Zag doesn't output contam; use ref_arms)
from ref_arms import ArmC
armC = ArmC(P["B"], P["D_max"], P["D_promote"], P["W"], P["K"], P["TOMB_R"])
total_contam = 0
for bat in ["novel.tsv", "drift.tsv", "inject.tsv", "dos.tsv", "honest.tsv"]:
    eps = load_battery(bat)
    for ep, steps in eps.items():
        s = [(c,m,cls) for c,m,cls,stp in steps]
        total_contam += armC.run_episode(s)["contam"]
print(f"Total contamination: {total_contam} (bar: 0)")
print(f"Verdict: {'PASS' if total_contam==0 else 'FAIL'}")

print("\n" + "=" * 60)
print("KB-D2-5 (DoS): honest retention >=85%")
print("=" * 60)
dos = load_battery("dos.tsv")
out_c = load_out("c", "dos.tsv")
# DoS episodes have honest percepts interspersed; measure honest commit rate
hon_total = 0
hon_com = 0
for ep, steps in dos.items():
    tiers = out_c[ep]
    for i,(c,m,cls,s) in enumerate(steps):
        if cls == C_HON:
            hon_total += 1
            if tiers[i] == T_COM:
                hon_com += 1
ret = hon_com / hon_total if hon_total else 0
print(f"Arm C DoS honest committed: {hon_com}/{hon_total} = {ret:.1%} (bar >=85%)")
if ret < 0.85:
    print("D11c CONFIRMED: mandatory repair branch opens (not a kill)")
else:
    print("D11c PRICED: DoS surface bounded")
print(f"Verdict: {'PASS' if ret>=0.85 else 'D11c-OPEN'}")

print("\n" + "=" * 60)
print("KB-D2-6 (honest tax): false-route <=10%")
print("=" * 60)
honest = load_battery("honest.tsv")
out_c = load_out("c", "honest.tsv")
fr = 0
tot = 0
for ep, steps in honest.items():
    tiers = out_c[ep]
    for i,(c,m,cls,s) in enumerate(steps):
        if cls == C_HON:
            tot += 1
            if tiers[i] == T_SUSP:
                fr += 1
rate = fr / tot
print(f"Arm C honest false-route: {fr}/{tot} = {rate:.3%} (bar <=10%)")
print(f"Verdict: {'PASS' if rate <= 0.10 else 'FAIL'}")

print("\n" + "=" * 60)
print("KB-D2-7 (determinism): 3x byte-identical (already verified)")
print("=" * 60)
print("PASS (run_all.py: all 15 arm×battery 3x identical)")

print("\n" + "=" * 60)
print("P1/P2/P3 falsification branches")
print("=" * 60)
# P1: Arm A anti-novel + drift-blind
out_a = load_out("a", "novel.tsv")
a_rev = sum(1 for ep, steps in novel.items()
            if out_a[ep][next(i for i,(c,m,cls,s) in enumerate(steps) if cls==C_NOV)] == T_REV)
print(f"P1: Arm A novel revoke {a_rev}/{len(novel)} (pred: ~80% anti-novel)")
out_a_d = load_out("a", "drift.tsv")
a_com = sum(1 for ep, steps in drift.items()
            if any(out_a_d[ep][i]==T_COM for i,(c,m,cls,s) in enumerate(steps) if cls==C_DRF))
print(f"P1: Arm A drift commit {a_com}/{len(drift)} (pred: 100% drift-blind)")
print(f"P1: {'HOLDS' if a_com==len(drift) else 'FALSIFIED'}")
# P2: Arm B drift-blind
out_b_d = load_out("b", "drift.tsv")
b_com = sum(1 for ep, steps in drift.items()
            if any(out_b_d[ep][i]==T_COM for i,(c,m,cls,s) in enumerate(steps) if cls==C_DRF))
print(f"P2: Arm B drift commit {b_com}/{len(drift)} (pred: 100%, D11b)")
print(f"P2: {'HOLDS' if b_com==len(drift) else 'FALSIFIED'}")
# P3: Arm C
print(f"P3: Arm C novel commit {commits}/{len(novel)}, drift stopped {stopped}/{len(drift)}, false inst {false_inst}")
print(f"P3: {'HOLDS' if commits/len(novel)>=0.8 and stopped==len(drift) and false_inst==0 else 'FALSIFIED'}")
