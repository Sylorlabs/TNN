#!/usr/bin/env python3
"""Crew C analysis: bars, C1 void rule, intent-vs-C0 z-tests, C-R1/C-R2.

Reads test_wavs/RESULTS_C.json + TEST_MANIFEST_C.json.
Writes test_wavs/STATS_C.json. Deterministic; no RNG.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "test_wavs")
results = json.load(open(os.path.join(W, "RESULTS_C.json")))


def Phi(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def ztest_one_sided(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    pp = (k1 + k2) / (n1 + n2)
    se = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0 if p1 <= p2 else 0.0
    z = (p1 - p2) / se
    return z, 1.0 - Phi(z)


def arm_hits(axis, arm):
    rs = [r for r in results if r["axis"] == axis and r["arm"] == arm]
    return sum(r["hit"] for r in rs), len(rs)


out = {"axes": {}, "cr1": {}, "cr2": {}}
void_flags = []
for axis, bar_n, bar_k in (("P", 40, 28), ("E", 20, 14), ("R", 20, 14)):
    ki, ni = arm_hits(axis, "intent")
    k0, n0 = arm_hits(axis, "C0")
    k1, n1 = arm_hits(axis, "C1")
    z, p = ztest_one_sided(ki, ni, k0, n0)
    c1_rate = k1 / n1
    if c1_rate > 0.25:
        void_flags.append(axis)
    out["axes"][axis] = {
        "intent": {"hits": ki, "n": ni, "rate": ki / ni,
                   "bar": f">={bar_k}/{bar_n}", "pass": ki >= bar_k},
        "C0": {"hits": k0, "n": n0, "rate": k0 / n0},
        "C1": {"hits": k1, "n": n1, "rate": c1_rate,
               "void_rule": "C1<=25%", "ok": c1_rate <= 0.25},
        "intent_vs_C0": {"z": z, "p_one_sided": p,
                         "significant_0.01": p < 0.01},
    }

kx, nx = arm_hits("X", "intent")
out["cr1"] = {"hits": kx, "n": nx, "rate": kx / nx,
              "note": "diagnostic; TABLE-SUSPECT if C-PASS but at chance"}
ks, ns = arm_hits("S", "intent")
out["cr2"] = {"hits": ks, "n": ns, "rate": ks / ns,
              "bar": ">=14/20 (diagnostic)"}

c_pass = (all(out["axes"][a]["intent"]["pass"] for a in "PER")
          and not void_flags
          and all(out["axes"][a]["intent_vs_C0"]["significant_0.01"]
                  for a in "PER"))
out["void_flags"] = void_flags
out["C_PASS"] = c_pass
if c_pass and kx / nx <= 0.2:
    out["table_suspect"] = True

with open(os.path.join(W, "STATS_C.json"), "w") as f:
    json.dump(out, f, indent=1)

for a in "PER":
    d = out["axes"][a]
    print(f"{a}: intent {d['intent']['hits']}/{d['intent']['n']} "
          f"pass={d['intent']['pass']} | C0 {d['C0']['hits']}/{d['C0']['n']} | "
          f"C1 {d['C1']['hits']}/{d['C1']['n']} ok={d['C1']['ok']} | "
          f"z={d['intent_vs_C0']['z']:.2f} p={d['intent_vs_C0']['p_one_sided']:.2e}")
print(f"C-R1: {kx}/{nx}  C-R2: {ks}/{ns}")
print("VOID_FLAGS:", void_flags, " C_PASS:", c_pass)
