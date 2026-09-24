#!/usr/bin/env python3
"""RT-CASCADE comparator: fault mix vs clean mix (int32 LE .s32).
Counts differing samples before/at/after the fault cut. Usage:
  cascade.py clean.s32 fault.s32 cut_sample [label]
"""
import sys
import numpy as np

def load(p):
    return np.fromfile(p, dtype='<i4')

def main():
    clean_p, fault_p, cut = sys.argv[1], sys.argv[2], int(sys.argv[3])
    label = sys.argv[4] if len(sys.argv) > 4 else fault_p
    a, b = load(clean_p), load(fault_p)
    n = min(len(a), len(b))
    d = (a[:n] != b[:n])
    pre = int(np.sum(d[:cut]))
    # fault block: the 1024-sample block containing cut
    bs = (cut // 1024) * 1024
    inblk = int(np.sum(d[bs:bs + 1024]))
    post = int(np.sum(d[bs + 1024:]))
    maxd = float(np.max(np.abs(a[:n].astype(np.float64) - b[:n].astype(np.float64)))) if np.any(d) else 0.0
    print("%s: total_diffs=%d pre_cut=%d in_fault_block=%d POST_CUT=%d max_abs_diff=%.0f" %
          (label, int(np.sum(d)), pre, inblk, post, maxd))

if __name__ == "__main__":
    main()
