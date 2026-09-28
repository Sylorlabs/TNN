#!/usr/bin/env python3
"""CREW GAMMA — R3 gamma-disease retention: f3gammaproof prefix diffs.

Field B = song field A + one appended loud frame (frame index fr=40).
Shared-identical region: samples [0, 39*2756) — frame 39 interpolates toward
B's loud frame, so it is excluded (same window the repair crew used:
[0,107484)). NEW binaries must show 0 diffs (no output-derived rescaling).
"""
import os, struct
import numpy as np

BASE = os.path.expanduser("~/workspace/tnn-lab/bytegen/par_tournament/crew_gamma")
N = 39 * 2756  # shared samples

def read_pcm(path):
    with open(path, "rb") as f:
        raw = f.read()
    nsamp = struct.unpack("<i", raw[40:44])[0] // 2
    return np.frombuffer(raw[44:44 + nsamp * 2], dtype="<i2")

for v in ["ctl", "h1", "h2a", "h2b", "h2c", "h2d", "revert"]:
    d = os.path.join(BASE, "out", v, "proof")
    out = []
    for tag, fa, fb, n in [("wav", "f3proofA.wav", "f3proofB.wav", 20000),
                           ("hifi", "f3proofAh.wav", "f3proofBh.wav", N)]:
        a = read_pcm(os.path.join(d, fa))[:n]
        b = read_pcm(os.path.join(d, fb))[:n]
        ndiff = int((a != b).sum())
        # also: max abs delta on shared region (should be 0 for NEW)
        m = int(np.abs(a.astype(np.int64) - b.astype(np.int64)).max())
        out.append("%s: diffs=%d maxdelta=%d" % (tag, ndiff, m))
    print("%-6s %s" % (v, " | ".join(out)))
