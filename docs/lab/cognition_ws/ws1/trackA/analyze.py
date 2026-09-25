#!/usr/bin/env python3
# WS1C Track A trial analysis: determinism gates, K1-K7, family tables.
import json, os, hashlib, sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = HERE + "/runs/main"
BATS = ["rtd1", "poison2", "baitflip2", "refute2", "refusal", "ambig1",
        "admit", "revoke", "logic", "trap", "cost"]
ARMS = {1: "forced", 2: "skep", 3: "auto", 4: "router"}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def load(b, arm, r):
    return [json.loads(l) for l in open(f"{RUNS}/{b}_arm{arm}_r{r}.jsonl") if l.strip()]

def fam_rtd1(rid):
    if "POISON" in rid: return "poison"
    if "BAIT" in rid: return "bait"
    if "DOUBLE" in rid: return "double"
    if "STRONG" in rid: return "strong"
    return "clean"

def fam_of(b, rid):
    if b == "rtd1": return "rtd1-" + fam_rtd1(rid)
    if b in ("poison2", "baitflip2", "refute2"):
        return b if not rid.endswith("CLEAN-01") and not rid.endswith("CLEAN-02") else b + "-clean"
    return b

def main():
    print("=== G1: 3/3 byte-identical reruns per cell (results + metrics) ===")
    det_ok = True
    for b in BATS:
        for arm in ARMS:
            hs = [sha(f"{RUNS}/{b}_arm{arm}_r{r}.jsonl") for r in range(3)]
            ms = [sha(f"{RUNS}/{b}_arm{arm}_r{r}.met.jsonl") for r in range(3)]
            ok = len(set(hs)) == 1 and len(set(ms)) == 1
            det_ok = det_ok and ok
            if not ok:
                print(f"  NONDET {b} arm{arm}: {hs} / {ms}")
    print("  all 44 cells byte-identical x3:", "PASS" if det_ok else "FAIL")
    print()
    print("=== per-family accuracy (arm1=forced arm2=skep arm3=auto arm4=router) ===")
    fam = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    wrong1000 = []
    for b in BATS:
        for arm in ARMS:
            for r in load(b, arm, 0):
                f = fam_of(b, r["id"])
                fam[f][ARMS[arm]][1] += 1
                if r["correct"] == 1:
                    fam[f][ARMS[arm]][0] += 1
                if ARMS[arm] == "skep" and r["correct"] == 0 and r["confidence"] == 1000 \
                   and b in ("rtd1", "poison2", "baitflip2", "refute2", "ambig1", "refusal"):
                    wrong1000.append((f, r["id"]))
    for f in sorted(fam):
        row = "  %-14s" % f
        for a in ["forced", "skep", "auto", "router"]:
            ok, n = fam[f][a]
            row += " %s=%d/%d" % (a, ok, n)
        print(row)
    print()
    adv = ["rtd1-poison", "rtd1-bait", "rtd1-double", "rtd1-strong", "poison2", "baitflip2", "refute2"]
    print("=== K1: skep >= auto per adversarial family ===")
    k1 = True
    for f in adv:
        s_ok, s_n = fam[f]["skep"]; a_ok, a_n = fam[f]["auto"]
        sa, aa = s_ok / s_n, a_ok / a_n
        p = sa >= aa
        k1 = k1 and p
        print("  %-14s skep=%d/%d auto=%d/%d %s" % (f, s_ok, s_n, a_ok, a_n, "PASS" if p else "KILL"))
    print("  K1:", "PASS" if k1 else "FAIL")
    print()
    print("=== K2: skep wrong at conf=1000 (must be none) ===")
    print("  ", wrong1000 if wrong1000 else "none PASS")
    k2 = len(wrong1000) == 0
    print()
    print("=== K3 refusal / K4 ambig1+perception / K5 honest no-regression ===")
    r_ok, r_n = fam["refusal"]["skep"]
    k3 = (r_ok == 60 and r_n == 60)
    print("  refusal skep=%d/%d %s" % (r_ok, r_n, "PASS" if k3 else "KILL"))
    a_ok, a_n = fam["ambig1"]["skep"]; f_ok, f_n = fam["ambig1"]["forced"]
    k4a = a_ok / a_n >= f_ok / f_n
    print("  ambig1 skep=%d/%d forced=%d/%d %s" % (a_ok, a_n, f_ok, f_n, "PASS" if k4a else "KILL"))
    k5 = True
    for b in ["admit", "revoke", "logic", "trap", "cost"]:
        s_ok, s_n = fam[b]["skep"]; f_ok, f_n = fam[b]["forced"]
        p = s_ok / s_n >= f_ok / f_n
        k5 = k5 and p
        print("  %-7s skep=%d/%d forced=%d/%d %s" % (b, s_ok, s_n, f_ok, f_n, "PASS" if p else "KILL"))
    print()
    print("=== K7 router ===")
    # K7a: 0 flags on refusal for arm4
    flags = sum(1 for r in load("refusal", 4, 0) if r["gate"] == 1)
    k7a = flags == 0
    print("  refusal router gate flags: %d/60 %s" % (flags, "PASS" if k7a else "KILL"))
    k7b = True
    for f in adv:
        r_ok, r_n = fam[f]["router"]; a_ok, a_n = fam[f]["auto"]
        p = r_ok / r_n >= a_ok / a_n
        k7b = k7b and p
        if not p:
            print("  %-14s router=%d/%d auto=%d/%d KILL" % (f, r_ok, r_n, a_ok, a_n))
    print("  K7b router>=auto per family:", "PASS" if k7b else "FAIL")
    # router on ambig1 + honest (informational)
    a_ok, a_n = fam["ambig1"]["router"]
    print("  ambig1 router=%d/%d (informational)" % (a_ok, a_n))
    for b in ["admit", "revoke", "logic", "trap", "cost"]:
        s_ok, s_n = fam[b]["router"]
        print("  %-7s router=%d/%d (informational)" % (b, s_ok, s_n))
    print()
    print("=== gate fire rates (arm2) ===")
    for b in BATS:
        rows = load(b, 2, 0)
        fl = sum(1 for r in rows if r["gate"] == 1)
        print("  %-9s %d/%d" % (b, fl, len(rows)))
    print()
    allpass = det_ok and k1 and k2 and k3 and k4a and k5 and k7a and k7b
    print("OVERALL:", "ADOPT" if allpass else "FALSIFIED")

if __name__ == "__main__":
    main()
