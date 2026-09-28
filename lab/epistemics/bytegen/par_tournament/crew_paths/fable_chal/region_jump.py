#!/usr/bin/env python3
"""REGION-1 jump metric: phase JUMP at boundaries, immune to linear drift.
jump(tb) = |wrap( (phi(tb+e) - phi(tb-e)) - 2*pi*f_plan(tb)*2e )|, e=5 ms.
phi(t) = quadrature phase vs local plan freq. A constant freq offset
contributes 2*pi*df*2e ~ 0.0003 rad (negligible); a true jump survives.
Plans: region1 (12x5s events 440..451) and region1b (1x60s event glide)."""
import cmath, math, os, struct

A = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "artifacts", "WITHHELD-NOT-FOR-REVIEW", "fable_chal", "region1")
SR = 44100
E = int(0.005 * SR)   # 5 ms half-gap
WQ = 1024             # quadrature window

def load(tag):
    p = os.path.join(A, "region1_%s.mix" % tag)
    d = open(p, "rb").read()
    if tag in ("b", "b1b"):
        s = struct.unpack("<%dq" % (len(d) // 8), d)
    else:
        s = struct.unpack("<%dh" % (len(d) // 2), d)
    pk = max(abs(v) for v in s) or 1
    return [v / pk for v in s]

def make_freq(plan):
    if plan == "region1":
        return lambda t: 440.0 + min(int(t // 5), 11)
    return lambda t: 440.0 + 11.0 * t / 60.0

def jump(s, tb, freq):
    nb = int(tb * SR)
    def phi_at(nc):
        f = freq(nc / SR)
        acc = 0j
        for n in range(nc - WQ, nc + WQ):
            acc += s[n] * cmath.exp(-2j * math.pi * f * (n - nc) / SR)
        return cmath.phase(acc)
    p1 = phi_at(nb - E)
    p2 = phi_at(nb + E)
    expected = 2 * math.pi * freq(tb) * (2 * E) / SR
    d = (p2 - p1) - expected
    while d > math.pi:
        d -= 2 * math.pi
    while d <= -math.pi:
        d += 2 * math.pi
    return abs(d)

log = []
for plan, tags in [("region1", ["b", "gated", "stock", "off"]),
                   ("region1b", ["b1b", "gated1b"])]:
    freq = make_freq(plan)
    bounds5 = [5.0 * k for k in range(1, 12)]
    bounds3 = [3.0 * k for k in range(1, 20)]
    for tag in tags:
        s = load(tag)
        d5 = [jump(s, tb, freq) for tb in bounds5]
        d3 = [jump(s, tb, freq) for tb in bounds3]
        line = ("%s/%s: 5s marks jump mean=%.4f max=%.4f | 3s marks jump mean=%.4f max=%.4f" %
                (plan, tag, sum(d5) / len(d5), max(d5), sum(d3) / len(d3), max(d3)))
        print(line, flush=True)
        log.append(line)
    # fable bar on the 12-event plan, 11 boundaries
    if plan == "region1":
        for tag in ["b", "gated"]:
            s = load(tag)
            d5 = [jump(s, tb, freq) for tb in bounds5]
            m = sum(d5) / len(d5)
            line = "BAR (mean<0.1 rad, 11 event boundaries): %s mean=%.4f -> %s" % (
                tag, m, "PASS" if m < 0.1 else "FAIL")
            print(line, flush=True)
            log.append(line)

ev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")
open(os.path.join(ev, "region1_jump.log"), "w").write("\n".join(log) + "\n")
print("wrote evidence/region1_jump.log")
