#!/usr/bin/env python3
"""Run Zag arms on all batteries (3x each), SHA-compare, cross-check vs Python."""
import hashlib
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_arms import *
import json

BUILD = "/home/hatch/workspace/pam_d2_build"
BAT = BUILD + "/batteries"
BIN = BUILD + "/arm_bin"
OUTDIR = BUILD + "/runs"
os.makedirs(OUTDIR, exist_ok=True)

spec = json.load(open(BAT + "/spec.json"))
P = spec["params"]

BATTERIES = ["novel.tsv", "drift.tsv", "inject.tsv", "dos.tsv", "honest.tsv"]
ARMS = ["a", "b", "c"]

def sha_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def load_zag_out(path):
    """Returns dict ep -> list of tiers in step order."""
    eps = {}
    with open(path) as f:
        for line in f:
            if line.startswith("ep\t"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            ep, step, tier = p[0], int(p[1]), int(p[2])
            eps.setdefault(ep, []).append(tier)
    return eps

CLS_MAP = {"HON": C_HON, "INJ": C_INJ, "NOV": C_NOV,
           "DRF": C_DRF, "RPL": C_RPL, "SPK": C_SPK}

def load_battery_tsv(fn):
    eps = {}
    with open(BAT + "/" + fn) as f:
        for line in f:
            if line.startswith("ep\t"):
                continue
            p = line.rstrip("\n").split("\t")
            ep, step, cls_s, c, m = p[0], int(p[1]), p[2], int(p[3]), int(p[4])
            eps.setdefault(ep, []).append((c, m, CLS_MAP[cls_s]))
    return eps

def python_tiers(arm, steps):
    if arm == "a":
        a = ArmA(P["B"], P["TOMB_R"])
    elif arm == "b":
        a = ArmB(P["N_armB"], P["TOMB_R"])
    else:
        a = ArmC(P["B"], P["D_max"], P["D_promote"], P["W"], P["K"], P["TOMB_R"])
    return a.run_episode(steps)["tier"]

results = {}
for arm in ARMS:
    for bat in BATTERIES:
        shas = []
        for run in range(3):
            out = f"{OUTDIR}/{arm}_{bat}_run{run}.out"
            inp = f"{BAT}/{bat}"
            # Use workspace scratch, not /tmp
            subprocess.run([BIN, inp, out, arm], check=True,
                           cwd=BUILD)
            shas.append(sha_file(out))
        identical = (shas[0] == shas[1] == shas[2])
        results[(arm, bat)] = {"shas": shas, "identical": identical}
        print(f"Arm {arm} {bat}: 3x identical={identical} sha={shas[0][:16]}...")

# cross-check Zag vs Python (use run0)
mismatches = 0
total = 0
for arm in ARMS:
    for bat in BATTERIES:
        zout = load_zag_out(f"{OUTDIR}/{arm}_{bat}_run0.out")
        py_eps = load_battery_tsv(bat)
        for ep, steps in py_eps.items():
            if ep not in zout:
                print(f"MISSING ep {ep} in Zag output for {arm}/{bat}")
                mismatches += 1
                continue
            py_tier = python_tiers(arm, steps)
            z_tier = zout[ep]
            if len(py_tier) != len(z_tier):
                print(f"LEN MISMATCH {arm}/{bat}/{ep}: py={len(py_tier)} z={len(z_tier)}")
                mismatches += 1
                continue
            for i, (pt, zt) in enumerate(zip(py_tier, z_tier)):
                total += 1
                if pt != zt:
                    if mismatches < 5:
                        print(f"MISMATCH {arm}/{bat}/{ep} step {i}: py={pt} z={zt}")
                    mismatches += 1

print(f"\nCross-check: {mismatches} mismatches / {total} decisions")
if mismatches == 0:
    print("PASS: zero decision mismatches")
else:
    print("FAIL: mismatches found")
    sys.exit(1)

# all identical?
all_ident = all(v["identical"] for v in results.values())
print(f"All 3x identical: {all_ident}")
if not all_ident:
    sys.exit(1)
