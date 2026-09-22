#!/usr/bin/env python3
"""Byte-exactness safety analysis v2 for Task 2.

Learner fragment design (SYN-SIN):
  - argument computed BIT-IDENTICALLY to the oracle:
      phase = 6.283185307179586*freq*(n as f64)/sr   (left-to-right f64)
  - range reduction with 2pi split as HI(27 sig bits)+LO so qi*HI is exact:
      TWOPI_HI = 6.283185303211212, TWOPI_LO = 3.968374476925287e-09
  - fold to [-pi/2, pi/2], Taylor through x^21 (Horner).

This script simulates that fragment bit-exactly in Python (IEEE doubles)
and checks all 110,250 pre-floor values against the frozen oracle.
"""
import math
import sys
sys.path.insert(0, '/home/hatch/workspace/tnn-lab/coding/reflection/task2/oracle')
from oracle import v1_samples, v2_samples, v3_samples  # noqa
from analyze import oracle_val_v1, oracle_val_v2, oracle_val_v3, dist_to_int  # noqa

TWOPI = 6.283185307179586
TWOPI_HI = 6.283185303211212
TWOPI_LO = 3.968374318722162 / 1000000000.0  # as the fragment writes it
assert TWOPI_LO == 3.968374318722162e-09, hex(TWOPI_LO)
PI = 3.141592653589793
HPI = 1.5707963267948966


def zfloor(x):
    t = math.trunc(x)
    if x < 0.0 and float(t) != x:
        t -= 1
    return t


def zsin(x):
    q = x / TWOPI
    qi = zfloor(q)
    qf = float(qi)
    r1 = x - qf * TWOPI_HI
    r = r1 - qf * TWOPI_LO
    if r > PI:
        r = r - TWOPI
    if r < -PI:
        r = r + TWOPI
    s = 1.0
    if r > HPI:
        r = PI - r
    elif r < -HPI:
        r = PI + r
        s = -1.0
    x2 = r * r
    # Taylor via recurrence (avoids >2^32 literals znc rejects):
    # term_k = term_{k-1} * (-x^2)/((2k)(2k+1)), 12 terms -> through x^23
    term = r
    ssum = r
    k = 1
    while k < 12:
        d = float(2 * k) * float(2 * k + 1)
        term = -term * x2 / d
        ssum = ssum + term
        k += 1
    return s * ssum


def zphase(freq, n):
    return TWOPI * float(freq) * float(n) / 44100.0


def zenv(n):
    if n < 2205:
        return float(n) / 2205.0
    if n < 6615:
        return 1.0 - 0.3 * float(n - 2205) / 4410.0
    if n < 15435:
        return 0.7
    if n < 22050:
        return 0.7 * (1.0 - float(n - 15435) / 6615.0)
    return 0.0


def main():
    worst = 0.0
    margin = 1.0
    mism = []
    total = 0

    def check(ov, sv):
        nonlocal worst, margin, total
        d = abs(sv - ov)
        if d > worst:
            worst = d
        m = dist_to_int(ov)
        if m < margin:
            margin = m
        if zfloor(sv) != math.floor(ov):
            mism.append((total, ov, sv))
        total += 1

    for n in range(44100):
        check(oracle_val_v1(n), (32767.0 * 0.5) * zsin(zphase(440.0, n)))
    for n in range(22050):
        check(oracle_val_v2(n),
              ((32767.0 * 0.8) * zenv(n)) * zsin(zphase(880.0, n)))
    for n in range(22050):
        o1, o2 = oracle_val_v3(n)
        s1 = (32767.0 * 0.5) * zsin(zphase(440.0, n))
        s2 = (32767.0 * 0.3) * zsin(zphase(660.0, n))
        check(o1, s1)
        check(o2, s2)
    print('samples checked : %d' % total)
    print('floor mismatches: %d' % len(mism))
    for t, ov, sv in mism[:10]:
        print('  mismatch at %d: oracle=%.17g sim=%.17g' % (t, ov, sv))
    print('max |sim-oracle|: %.3e' % worst)
    # exact-integer oracle values are all 0.0 (n=0); both sides compute
    # sin(0)=0 exactly, so they are safe by construction, not by margin.
    print('min nonzero dist-to-int: %.3e' % margin)
    print('safety ratio    : %.1f' % (margin / worst if worst else float('inf')))
    print('VERDICT:', 'SAFE' if not mism and margin > 3 * worst else 'UNSAFE')


if __name__ == '__main__':
    main()
