#!/usr/bin/env python3
"""Freeze the 20-case held-out intent list for Crew L (prereg 2.3, 5.5).
Selection rule (deterministic, documented): integer-Hz targets in [90, 1175]
whose semitone-grid quantization error is in [1.0%, 2.9%] (guarantees a real,
correctable open-loop residual); 20 spread across the range; env cycles
flat/rise/decay. Disjoint from dev targets {440, 220, 880}.
No RNG."""
import json, os

R = 2 ** (1 / 12)
GRID = [440.0 * R ** k for k in range(-29, 18)]

def qerr(f):
    g = min(GRID, key=lambda x: abs(x - f))
    return abs(g - f) / f, g

cands = []
for f in range(90, 1176):
    if f in (440, 220, 880):
        continue
    e, g = qerr(f)
    if 0.010 <= e <= 0.029:
        cands.append((f, e, g))

# spread: sort by freq, take every kth
cands.sort()
step = len(cands) / 20
picked = [cands[int(i * step)] for i in range(20)]

ENVS = ["flat", "rise", "decay"]
cases = []
for i, (f, e, g) in enumerate(picked):
    cases.append({
        "case_id": "L%02d" % (i + 1),
        "target_hz": f,
        "target_env": ENVS[i % 3],
        "target_env_int": i % 3,
        "quant_err": round(e, 5),
        "plan_mhz_audit": int(round(g * 1000)),
    })

mp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "manifests", "intent_manifest.json")
os.makedirs(os.path.dirname(mp), exist_ok=True)
json.dump(cases, open(mp, "w"), indent=2)
for c in cases:
    print(c["case_id"], c["target_hz"], c["target_env"], "qerr=%.3f" % c["quant_err"],
          "plan=%d" % c["plan_mhz_audit"])
print("wrote", mp, "-", len(cases), "cases")
