#!/usr/bin/env python3
"""Verify the fixed (killpg) runner reproduces the original run's tallies.
Runs B2R (12 normal) + B6X (panic + miss cases) with the fixed run_once,
compares solved/incorrect counts against results_formal_quot.json.
"""
import json, os, sys, hashlib
sys.path.insert(0, "/home/hatch/workspace/math_r2/eval")
from run_quot import run_once, QUOT, BASE, sealed, verdict_class

R = json.load(open("/home/hatch/workspace/math_r2/eval/results_formal_quot.json"))
SEAL_B2 = sealed(f"{BASE}/problems/sealed/SEALED_B2.sol")
SEAL_B2["B2_07"] = "WITHHELD"  # CORRECTED (F-SEAL-01, same as eval)
SEAL_B6X = sealed(f"{BASE}/round2/batteries/sealed/SEALED_B6X.sol")

def verdict_of(outp):
    for line in open(outp):
        if line.startswith("verdict:"):
            return line.split(":")[1].strip()
    return None

ok = True
# B2R
probs = [(f"{BASE}/problems/b2/B2_{i:02d}.form", f"B2_{i:02d}") for i in range(1, 13)]
solved = inc = 0
for prob, pid in probs:
    outs = []
    good = True
    for r in range(3):
        outp = f"/tmp/verify_quot/B2R_{pid}.r{r}"
        try:
            dt, rc = run_once(f"{QUOT} {prob} {outp}", timeout=600)
        except Exception:
            good = False; break
        if rc != 0 or not os.path.exists(outp):
            good = False; break
        outs.append(open(outp, "rb").read())
    if not good or not (outs[0] == outs[1] == outs[2]):
        print(f"B2R {pid}: RUNNER MISMATCH"); ok = False; continue
    v = verdict_of(f"/tmp/verify_quot/B2R_{pid}.r0")
    sv = SEAL_B2.get(pid)
    if verdict_class(v) == verdict_class(sv): solved += 1
    else: inc += 1; print(f"B2R {pid}: verdict {v} vs sealed {sv}")
exp = R["B2R"]["agg"]
print(f"B2R fixed-runner: solved {solved}/12 incorrect {inc} | original: {exp['solved']}/12 incorrect {exp['incorrect']} -> {'MATCH' if (solved, inc) == (exp['solved'], exp['incorrect']) else 'DIFFER'}")
ok = ok and (solved, inc) == (exp["solved"], exp["incorrect"])

# B6X (covers EXIT_1 panic path)
solved = inc = 0; statuses = {}
for i in range(1, 4):
    pid = f"B6X_{i:02d}"; prob = f"{BASE}/round2/batteries/b6x/{pid}.form"
    try:
        dt, rc = run_once(f"{QUOT} {prob} /tmp/verify_quot/{pid}.r0", timeout=600)
        statuses[pid] = f"rc={rc}"
        if rc != 0:
            continue
    except Exception:
        statuses[pid] = "TIMEOUT"; continue
    v = verdict_of(f"/tmp/verify_quot/{pid}.r0")
    sv = SEAL_B6X.get(pid)
    if verdict_class(v) == verdict_class(sv): solved += 1
    else: inc += 1
print(f"B6X fixed-runner statuses: {statuses} solved {solved} incorrect {inc}")
exp6 = R["B6X"]
exp_status = {pid: p["status"] for pid, p in exp6["problems"].items()}
print(f"B6X original statuses: {exp_status} solved {exp6['agg']['solved']} incorrect {exp6['agg']['incorrect']}")
match6 = (statuses.get("B6X_01") == "rc=1" and statuses.get("B6X_02", "").startswith("rc=0")
          and statuses.get("B6X_03", "").startswith("rc=0") and (solved, inc) == (exp6["agg"]["solved"], exp6["agg"]["incorrect"]))
print("B6X ->", "MATCH" if match6 else "DIFFER")
print("OVERALL:", "EQUIVALENT" if (ok and match6) else "MISMATCH")
