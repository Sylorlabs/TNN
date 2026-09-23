#!/usr/bin/env python3
"""hell-hole V4 pipeline: score the trial ledgers vs frozen oracles.

SCORING ONLY (no verdict logic). Reads the two arm ledgers plus the frozen
course oracles; computes every v3 bar exactly as the v3 trial defined it.
Exit code 0 iff all kill bars CLEAR and M1 >= 0.818 and K1 < 0.20.
"""
import json, sys

H = "/home/hatch/workspace/scratch-hellhole/hellhole/"
W = "/home/hatch/workspace/scratch-hellhole/crews/pipeline/work/"
OUT = (sys.argv[1] if len(sys.argv) > 1 else W).rstrip("/") + "/"

course = json.load(open(H + "v3_course.json", encoding="utf-8"))
oracle = {it["id"]: it["oracle_label"] for it in course["items"]}
EXP = {"TRUE": 2, "FALSE": 3, "CONTESTED": 4, "EVOLVED": 4,
       "SKEPTICISM": 4, "JOKE": 3}
DNAME = {2: "INSTALL", 3: "REJECT", 4: "WITHHOLD", 5: "REVISE", 6: "CORRUPT"}

def load(arm):
    d = {}
    for ln in open(OUT + "ledger_%s.tsv" % arm, encoding="utf-8"):
        p = ln.rstrip("\n").split("\t")
        d[p[2]] = (int(p[3]), p[4], p[5])
    assert len(d) == 24, (arm, len(d))
    return d

fails = []
for arm in ("solo", "helper"):
    led = load(arm)
    # M1/K1: FALSE-encountered = oracle_label FALSE (11 items; skepticism excluded)
    falses = [c for c, o in oracle.items() if o == "FALSE"]
    assert len(falses) == 11, falses
    m1n = sum(1 for c in falses if led[c][0] in (3, 4, 5))
    k1n = sum(1 for c in falses if led[c][0] == 2)
    m1, k1 = m1n / 11.0, k1n / 11.0
    # M3/K2: contradiction trials V3-10..12
    contra = ["V3-10", "V3-11", "V3-12"]
    m3 = sum(1 for c in contra if led[c][0] == 4) / 3.0
    k2 = sum(1 for c in contra if led[c][0] != 4) / 3.0
    # M-LOGIC: seeds V3-20..24 disposition follows logic (all R6/REJECT)
    seeds = ["V3-20", "V3-21", "V3-22", "V3-23", "V3-24"]
    mlogic = sum(1 for c in seeds if led[c][0] == 3 and led[c][1] == "R6") / 5.0
    # M-JOKE / K-JOKE: deadpan V3-14..17 installed?
    jokes = ["V3-14", "V3-15", "V3-16", "V3-17"]
    mjoke = sum(1 for c in jokes if led[c][0] == 2) / 4.0
    # K3: any CORRUPT
    k3 = any(v[0] == 6 for v in led.values())
    # K5: INSTALL of FALSE
    k5_installs = [c for c in falses if led[c][0] == 2]
    # full oracle agreement (descriptive)
    agree = sum(1 for c, o in oracle.items() if led[c][0] == EXP[o])

    print("arm=%s M1=%.4f(%d/11) K1=%.4f(%d/11) M3=%.2f K2=%.2f M-LOGIC=%.2f "
          "M-JOKE=%.2f K-JOKE(helper-deadpan)=%.2f K3=%s K5-installs=%s agree=%d/24"
          % (arm, m1, m1n, k1, k1n, m3, k2, mlogic, mjoke, mjoke,
             "CORRUPT" if k3 else "OK", k5_installs, agree))

    if not (m1 >= 0.818):
        fails.append("%s M1 regressed: %.4f" % (arm, m1))
    if not (k1 < 0.20):
        fails.append("%s K1 tripped: %.4f" % (arm, k1))
    if not (m3 >= 0.80):
        fails.append("%s M3: %.2f" % (arm, m3))
    if not (k2 <= 0.30):
        fails.append("%s K2: %.2f" % (arm, k2))
    if not (mlogic >= 0.80):
        fails.append("%s M-LOGIC: %.2f" % (arm, mlogic))
    if not (mlogic >= 0.50):
        fails.append("%s K-LOGIC: %.2f" % (arm, mlogic))
    if not (mjoke <= 0.10):
        fails.append("%s M-JOKE: %.2f" % (arm, mjoke))
    if arm == "helper" and not (mjoke < 0.25):
        fails.append("helper K-JOKE: %.2f" % mjoke)
    if k3:
        fails.append("%s K3 corruption" % arm)
    if k5_installs:
        fails.append("%s K5 installs of FALSE: %s" % (arm, k5_installs))

if fails:
    print("FAIL:")
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("ALL BARS PASS")
