#!/usr/bin/env python3
"""Chance-baseline computation log for PREREG_AUDIO_PRINCIPLES.md (frozen 2026-09-25).
Exact one-sided binomial tail probabilities, alpha=0.01. No RNG used."""
from math import comb

def tail(n, k, p):
    return sum(comb(n, i) * (p ** i) * ((1 - p) ** (n - i)) for i in range(k, n + 1))

print("PITCH-REL / RHY  2AFC n=100 p=0.5")
for k in (62, 63):
    print(f"  P(X>={k}) = {tail(100, k, 0.5):.6f}  -> bar >=63 (0.006016 < 0.01)")
print("ENV              3AFC n=60  p=1/3")
for k in (29, 30):
    print(f"  P(X>={k}) = {tail(60, k, 1/3):.6f}  -> bar >=30 (0.005553 < 0.01)")
print("PITCH-ABS       24AFC n=60  p=1/24")
for k in (7, 8):
    print(f"  P(X>={k}) = {tail(60, k, 1/24):.6f}  -> bar >=8 (0.003356 < 0.01)")
print("L non-degeneracy sign rule n=20 p=0.5")
for k in (15, 16):
    print(f"  P(X>={k}) = {tail(20, k, 0.5):.6f}  -> bar >=16/20 improved (0.005909 < 0.01)")
print("Analytic blind-pitch-hit bound: uniform guess over [80,1200] Hz, +-2% window:")
print("  P(hit) ~= 0.04 * E[t]/1120 ~= 0.04 * 640/1120 ~= 0.0229 (record only; C0 arm is binding)")
