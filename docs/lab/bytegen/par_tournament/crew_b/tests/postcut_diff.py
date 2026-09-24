#!/usr/bin/env python3
"""Post-cut diff count for RT-CASCADE: differing samples strictly after the
fault window (t > cut_end_s) between clean and faulted .mix files.
Usage: postcut_diff.py <clean.mix> <fault.mix> <cut_end_s>
"""
import struct, sys

def rd(p):
    d = open(p, "rb").read()
    n = len(d) // 4
    return struct.unpack("<%di" % n, d[: n * 4])

SR = 44100
a = rd(sys.argv[1]); b = rd(sys.argv[2])
cut_end = float(sys.argv[3])
assert len(a) == len(b)
pre = wth = post = 0
for i in range(len(a)):
    if a[i] != b[i]:
        t = i / SR
        if t < 3.0:
            pre += 1
        elif t <= cut_end:
            wth += 1
        else:
            post += 1
print(f"nsamp={len(a)} pre_cut_diffs={pre} fault_window_diffs={wth} post_cut_diffs={post}")
