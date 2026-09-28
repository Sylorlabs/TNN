#!/usr/bin/env python3
"""Biased ZCR sanity check on a rendered response region (disclosed bias:
6-harmonic timbre reads ~+60..97 cents sharp; this is NOT the scheme's
pitch claim - the claim is construction-exact f0q). Prints measured Hz and
cents vs the construction pitch.
Usage: measure_zcr.py <wav> <t0_s> <t1_s> <construction_hz>
"""
import struct, sys, math
import numpy as np

def read_wav(path):
    with open(path, "rb") as f:
        data = f.read()
    raw = data[44:]
    n = len(raw) // 2
    return np.array(struct.unpack("<%dh" % n, raw[: n * 2]), dtype=np.float64)

SR = 44100
s = read_wav(sys.argv[1])
t0, t1, fcon = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
seg = s[int(t0 * SR) : int(t1 * SR)]
zc = int(((seg[:-1] < 0) & (seg[1:] >= 0)).sum())
dur = len(seg) / SR
fmeas = zc / dur
cents = 1200 * math.log2(fmeas / fcon) if fmeas > 0 else float("nan")
print(f"region {t0}-{t1}s: zcr_hz={fmeas:.1f} construction_hz={fcon:.2f} "
      f"bias={cents:+.0f}c (DISCLOSED sensor bias, not the pitch claim)")
