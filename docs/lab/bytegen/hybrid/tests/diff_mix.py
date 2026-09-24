#!/usr/bin/env python3
"""Compare two i32-LE .mix files (as written by render_hyb mix modes).
Prints: differing samples, first/last diff time, and per-region counts."""
import struct, sys

def rd(p):
    d = open(p, "rb").read()
    n = len(d) // 4
    return struct.unpack("<%di" % n, d[: n * 4])

SR = 44100
a = rd(sys.argv[1]); b = rd(sys.argv[2])
assert len(a) == len(b), (len(a), len(b))
idx = [i for i in range(len(a)) if a[i] != b[i]]
print("nsamp=%d diffs=%d" % (len(a), len(idx)))
if idx:
    print("first t=%.4fs last t=%.4fs" % (idx[0] / SR, idx[-1] / SR))
