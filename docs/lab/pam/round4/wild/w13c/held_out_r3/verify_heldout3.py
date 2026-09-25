#!/usr/bin/env python3
"""Round 3 held-out stream verifier.

Checks per stream: 8-field format, lease_id == line ordinal, kind in {G,F},
tag < 2^23, every G row passes admission bars, G content in the 671 genuine
pool, F content in the 1139 false pool, and reports the genuine
corroboration fraction (G rows sitting in >=1 same-tag/diff-channel
|Delta ordinal| <= 3 pair).
"""
import os
import sys

M1 = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
D = os.path.dirname(os.path.abspath(__file__))
BAR_CONF, BAR_MRGF = 705, 3588
TAG_MAX = 1 << 23

def load_pools():
    genuine_l, false_l = [], []
    for line in open(M1):
        line = line.strip()
        if not line:
            continue
        p = line.split("|")
        k = p[0]
        if k == "C":
            c, m, s, a = int(p[1]), int(p[2]), int(p[3]), int(p[4])
            if c >= BAR_CONF and m >= BAR_MRGF and s >= 1 and a >= 1:
                genuine_l.append((c, m, s, a))
        elif k == "B":
            false_l.append((int(p[1]), int(p[2]), int(p[3]), int(p[4])))
        elif k == "W":
            false_l.append((int(p[1]), int(p[2]), 1, 1))
        elif k == "P":
            false_l.append((int(p[2]), int(p[3]), 1, 1))
    assert len(genuine_l) == 671, len(genuine_l)   # list count (dupes preserved)
    assert len(false_l) == 1139, len(false_l)
    genuine, false = set(genuine_l), set(false_l)  # membership on content identity
    return genuine, false

def verify(path, genuine, false):
    rows = []
    nG = nF = 0
    with open(path) as f:
        for ln, line in enumerate(f, start=1):
            p = line.rstrip("\n").split("|")
            assert len(p) == 8, f"line {ln}: {len(p)} fields"
            lid, kind, ch, tag = int(p[0]), p[1], int(p[2]), int(p[3])
            c, m, s, a = int(p[4]), int(p[5]), int(p[6]), int(p[7])
            assert lid == ln, f"lease_id {lid} != ordinal {ln}"
            assert kind in ("G", "F"), kind
            assert ch >= 0 and tag >= 0 and c >= 0 and m >= 0 and s >= 0 and a >= 0
            assert tag < TAG_MAX, f"tag {tag} >= 2^23"
            if kind == "G":
                nG += 1
                assert c >= BAR_CONF and m >= BAR_MRGF and s >= 1 and a >= 1, \
                    f"G row {ln} fails bar: {p[4:]}"
                assert (c, m, s, a) in genuine, f"G row {ln} content not in genuine pool"
            else:
                nF += 1
                assert (c, m, s, a) in false, f"F row {ln} content not in false pool"
            rows.append((kind, ch, tag))
    # corroboration fraction: G rows with >=1 same-tag/diff-channel |Delta ordinal|<=3 partner
    by_tag = {}
    for idx, (kind, ch, tag) in enumerate(rows):
        by_tag.setdefault(tag, []).append((idx, kind, ch))
    paired = 0
    for idx, (kind, ch, tag) in enumerate(rows):
        if kind != "G":
            continue
        hit = False
        for jdx, jkind, jch in by_tag[tag]:
            if jch != ch and abs(jdx - idx) <= 3:
                hit = True
                break
        if hit:
            paired += 1
    frac = paired / nG if nG else 0.0
    return ln, nG, nF, paired, frac

def main():
    genuine, false = load_pools()
    names = sorted(f for f in os.listdir(D) if f.endswith(".txt"))
    assert len(names) == 5, names
    for n in names:
        total, nG, nF, paired, frac = verify(os.path.join(D, n), genuine, false)
        print(f"{n}: rows={total} G={nG} F={nF} "
              f"paired_G={paired} corroboration={frac*100:.2f}% "
              f"{'PASS' if frac >= 0.80 else 'FAIL-BAR'}")

if __name__ == "__main__":
    main()
