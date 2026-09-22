#!/usr/bin/env python3
"""Byte-exactness safety analysis for Task 2.

Simulates the planned Zag learner fragment BIT-EXACTLY in Python (every float
op is IEEE-754 double, correctly rounded — identical to x86-64 SSE2, which is
what znc's f64 lowers to; verified empirically by the f64 probe in
src/probe_f64.zag). Compares the simulated fragment's floor() outputs against
the frozen oracle's floors on all 88,200 samples, and measures the safety
margin: min over all samples of distance-to-nearest-integer of the oracle's
exact (pre-floor) value.

Byte-exactness is SAFE (not luck) iff
    max |sim_val - oracle_val|  <<  min distance-to-nearest-integer.
"""
import math
import sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/coding/reflection/task2/oracle')
from oracle import v1_samples, v2_samples, v3_samples  # noqa

TWOPI = 6.283185307179586
PI = 3.141592653589793
HPI = 1.5707963267948966


def zfloor(x):
    t = math.trunc(x)
    if x < 0.0 and float(t) != x:
        t -= 1
    return t


def zsin(x):
    # planned SYN-OSC fragment, op-for-op
    q = x / TWOPI
    qi = zfloor(q)
    r = x - float(qi) * TWOPI
    if r > PI:
        r = r - TWOPI
    s = 1.0
    if r > HPI:
        r = PI - r
    elif r < -HPI:
        r = PI + r
        s = -1.0
    x2 = r * r
    p = 1.0 / 51090942171709440000.0
    p = -1.0 / 121645100408832000.0 + x2 * p
    p = 1.0 / 355687428096000.0 + x2 * p
    p = -1.0 / 1307674368000.0 + x2 * p
    p = 1.0 / 6227020800.0 + x2 * p
    p = -1.0 / 39916800.0 + x2 * p
    p = 1.0 / 362880.0 + x2 * p
    p = -1.0 / 5040.0 + x2 * p
    p = 1.0 / 120.0 + x2 * p
    p = -1.0 / 6.0 + x2 * p
    p = 1.0 + x2 * p
    return s * r * p


def zphase(freq, n):
    # planned fragment: phase in cycles, then radians in [-pi, pi]
    cyc = float(freq) * float(n) / 44100.0
    fc = cyc - float(zfloor(cyc))
    ph = fc
    if ph >= 0.5:
        ph = ph - 1.0
    return TWOPI * ph


def zenv(n):
    if n < 2205:
        return float(n) / 2205.0
    if n < 6615:
        return 1.0 - (1.0 - 0.7) * float(n - 2205) / float(6615 - 2205)
    if n < 15435:
        return 0.7
    if n < 22050:
        return 0.7 * (1.0 - float(n - 15435) / float(22050 - 15435))
    return 0.0


def oracle_val_v1(n):
    return 32767 * 0.5 * math.sin(2 * math.pi * 440 * n / 44100)


def oracle_val_v2(n):
    if n < 2205:
        env = n / 2205
    elif n < 6615:
        env = 1 - 0.3 * (n - 2205) / 4410
    elif n < 15435:
        env = 0.7
    else:
        env = 0.7 * (1 - (n - 15435) / 6615)
    return 32767 * 0.8 * env * math.sin(2 * math.pi * 880 * n / 44100)


def oracle_val_v3(n):
    s1 = 32767 * 0.5 * math.sin(2 * math.pi * 440 * n / 44100)
    s2 = 32767 * 0.3 * math.sin(2 * math.pi * 660 * n / 44100)
    return s1, s2


def sim_v1(n):
    return (32767.0 * 0.5) * zsin(zphase(440, n))


def sim_v2(n):
    return ((32767.0 * 0.8) * zenv(n)) * zsin(zphase(880, n))


def sim_v3(n):
    s1 = (32767.0 * 0.5) * zsin(zphase(440, n))
    s2 = (32767.0 * 0.3) * zsin(zphase(660, n))
    return s1, s2


def dist_to_int(x):
    f = x - math.floor(x)
    return min(f, 1.0 - f)


def main():
    worst = 0.0
    margin = 1.0
    mism = 0
    total = 0
    # V1
    for n in range(44100):
        ov = oracle_val_v1(n)
        sv = sim_v1(n)
        d = abs(sv - ov)
        if d > worst:
            worst = d
        m = dist_to_int(ov)
        if m < margin:
            margin = m
        if zfloor(sv) != math.floor(ov):
            mism += 1
        total += 1
    # V2
    for n in range(22050):
        ov = oracle_val_v2(n)
        sv = sim_v2(n)
        d = abs(sv - ov)
        if d > worst:
            worst = d
        m = dist_to_int(ov)
        if m < margin:
            margin = m
        if zfloor(sv) != math.floor(ov):
            mism += 1
        total += 1
    # V3 (compare pre-clamp floors; clamp is exact integer math)
    for n in range(22050):
        o1, o2 = oracle_val_v3(n)
        s1, s2 = sim_v3(n)
        for ov, sv in ((o1, s1), (o2, s2)):
            d = abs(sv - ov)
            if d > worst:
                worst = d
            m = dist_to_int(ov)
            if m < margin:
                margin = m
            if zfloor(sv) != math.floor(ov):
                mism += 1
        total += 2
    print('samples checked : %d' % total)
    print('floor mismatches: %d' % mism)
    print('max |sim-oracle|: %.3e' % worst)
    print('min dist-to-int : %.3e' % margin)
    print('safety ratio    : %.1f' % (margin / worst if worst else float('inf')))
    print('VERDICT:', 'SAFE' if mism == 0 and margin > 10 * worst else 'UNSAFE')


if __name__ == '__main__':
    main()
