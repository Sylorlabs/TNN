#!/usr/bin/env python3
"""REGION-1 analysis: phase discontinuity at boundaries for B vs gated-C.
B mix = f64 LE; gated/stock/off mix = i16 LE. 60 s @44100 Hz.
Metric: |wrap(phi_after - phi_before)| at each boundary, phi estimated by
quadrature against the local plan freq, extrapolated to the boundary sample.
Bar (fable): mean < 0.1 rad over the 11 five-second event boundaries."""
import cmath, math, os, struct

A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "artifacts", "WITHHELD-NOT-FOR-REVIEW", "fable_chal", "region1")
SR = 44100
W = 2048  # analysis window each side

def load(tag):
    p = os.path.join(A, "region1_%s.mix" % tag)
    d = open(p, "rb").read()
    if tag == "b":
        n = len(d) // 8
        return struct.unpack("<%dq" % n, d)  # B mix = i64 LE samples
    n = len(d) // 2
    return struct.unpack("<%dh" % n, d)

def freq_at(t):
    k = min(int(t // 5), 11)
    return 440.0 + k

def phi_at(s, nb, f, side):
    # quadrature sum over window, phase extrapolated to nb
    acc = 0j
    if side < 0:
        rng = range(nb - W, nb)
    else:
        rng = range(nb, nb + W)
    for n in rng:
        v = s[n]
        acc += v * cmath.exp(-2j * math.pi * f * (n - nb) / SR)
    return cmath.phase(acc)

def wrap(x):
    while x > math.pi:
        x -= 2 * math.pi
    while x <= -math.pi:
        x += 2 * math.pi
    return x

def discontinuities(tag, bounds):
    s = load(tag)
    pk = max(abs(v) for v in s) or 1
    s = [v / pk for v in s]
    out = []
    for tb in bounds:
        nb = int(tb * SR)
        fb = freq_at(tb - 1e-6)
        fa = freq_at(tb + 1e-6)
        pb = phi_at(s, nb, fb, -1)
        pa = phi_at(s, nb, fa, +1)
        out.append(abs(wrap(pa - pb)))
    return out

event_bounds = [5.0 * k for k in range(1, 12)]   # 11 boundaries (fable's set)
b3_bounds = [3.0 * k for k in range(1, 20)]      # B's 19 internal 3 s boundaries

log = []
for tag in ["b", "gated", "stock", "off"]:
    de = discontinuities(tag, event_bounds)
    mean_e, max_e = sum(de) / len(de), max(de)
    line = ("%s: 11 event boundaries mean=%.4f rad max=%.4f rad "
            "[bar mean<0.1: %s]" % (tag, mean_e, max_e, "PASS" if mean_e < 0.1 else "FAIL"))
    print(line, flush=True)
    log.append(line)
    if tag == "b":
        d3 = discontinuities(tag, b3_bounds)
        line2 = ("b: 19 internal 3 s region boundaries mean=%.4f rad max=%.4f rad" %
                 (sum(d3) / len(d3), max(d3)))
        print(line2, flush=True)
        log.append(line2)
        log.append("b event-boundary values: " + " ".join("%.3f" % v for v in de))
        log.append("b 3s-boundary values: " + " ".join("%.3f" % v for v in d3))

ev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
open(os.path.join(ev, "region1.log"), "w").write("\n".join(log) + "\n")
print("wrote evidence/region1.log")
