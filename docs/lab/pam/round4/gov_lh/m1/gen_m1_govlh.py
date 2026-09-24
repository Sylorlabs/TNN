#!/usr/bin/env python3
"""gen_m1_govlh.py — Gov-LH Crew 4 fixture generator (derives from PREREG_M1_GOVLH.md).

Deterministic (zero RNG). Reads the frozen Round-3 fixture F and emits
m1_govlh_cases.txt with the novel wrong families of prereg section 3:

  C|conf|mrgF|strong|agree            (1,102, copied verbatim from F)
  W|conf|mrgF|1|1                     (12, copied verbatim from F)
  P|pairid|conf|mrgF|1|1              (18, copied verbatim from F)
  B|conf|mrgF|strong|agree            (1,109, copied verbatim from F)
  N|fam|conf|mrgF|strong|agree|src    novel wrongs (fam 1,2,3,5; src 0=real,1=synth)
  Q|pairid|conf|mrgF|strong|agree      novel wrong pairs (fam 4, all strong=agree=1)

Frozen bars: OPT=(0,0,705,3588), SAFE=(1,1,705,3588).
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = "/home/hatch/workspace/tnn-lab/pam/round3/m1/m1_cases.txt"
F_SHA = "5d4160d1e1a06c8250376bc85367981722fe0002296ae168c581c8353322c611"

OPT = (0, 0, 705, 3588)  # ST, AT, CT, MT


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def passes(conf, mrg, s, a, bar):
    st, at, ct, mt = bar
    return conf >= ct and mrg >= mt and s >= st and a >= at


def main():
    got = sha(F)
    assert got == F_SHA, "frozen fixture sha mismatch: %s" % got
    rows = []          # (kind, fields...) in fixture order; kind in C,W,P,B,N,Q
    b_rows = []        # parsed B rows for family derivation
    for ln in open(F):
        f = ln.rstrip("\n").split("|")
        k = f[0]
        if k == "C":
            rows.append(("C", int(f[1]), int(f[2]), int(f[3]), int(f[4])))
        elif k == "W":
            rows.append(("W", int(f[1]), int(f[2]), 1, 1))
        elif k == "P":
            rows.append(("P", int(f[1]), int(f[2]), int(f[3]), 1, 1))
        elif k == "B":
            r = ("B", int(f[1]), int(f[2]), int(f[3]), int(f[4]))
            rows.append(r)
            b_rows.append(r)
        else:
            raise AssertionError("unknown kind %r" % k)
    nC = sum(1 for r in rows if r[0] == "C")
    nW = sum(1 for r in rows if r[0] == "W")
    nP = sum(1 for r in rows if r[0] == "P")
    nB = sum(1 for r in rows if r[0] == "B")
    assert (nC, nW, nP, nB) == (1102, 12, 18, 1109), (nC, nW, nP, nB)

    # --- N1: 1145-class (strong=agree=1, passes OPT) — REAL, src=0
    n1 = [r for r in b_rows
          if r[3] == 1 and r[4] == 1 and passes(r[1], r[2], r[3], r[4], OPT)]
    # --- N2: single-arm exploit (exactly one of strong/agree is 0) — REAL
    n2 = [r for r in b_rows
          if (r[3] == 0) != (r[4] == 0) and passes(r[1], r[2], r[3], r[4], OPT)]
    # --- N5-real: double-arm exploit — REAL
    n5r = [r for r in b_rows
           if r[3] == 0 and r[4] == 0 and passes(r[1], r[2], r[3], r[4], OPT)]
    # partition check (prereg section 3): N1+N2+N5r == B rows passing OPT
    b_opt = [r for r in b_rows if passes(r[1], r[2], r[3], r[4], OPT)]
    assert len(n1) + len(n2) + len(n5r) == len(b_opt), \
        (len(n1), len(n2), len(n5r), len(b_opt))
    assert len({id(r) for r in n1} & {id(r) for r in n2}) == 0
    assert len({id(r) for r in n1} & {id(r) for r in n5r}) == 0
    assert len({id(r) for r in n2} & {id(r) for r in n5r}) == 0

    for r in n1:
        rows.append(("N", 1, r[1], r[2], r[3], r[4], 0))
    for r in n2:
        rows.append(("N", 2, r[1], r[2], r[3], r[4], 0))
    for r in n5r:
        rows.append(("N", 5, r[1], r[2], r[3], r[4], 0))

    # --- N3: boundary grid — SYNTH, src=1
    confs = [704, 705, 706, 750, 874, 1000]
    mrgs = [3587, 3588, 3589, 5000, 6600, 10410]
    n3pts = []
    for c in confs:
        for m in mrgs:
            for s in (0, 1):
                for a in (0, 1):
                    n3pts.append((c, m, s, a))
                    rows.append(("N", 3, c, m, s, a, 1))
    assert len(n3pts) == 144

    # --- N4: corroborated wrong pairs from N3 (strong=agree=1, OPT-passing),
    #     sorted by (conf, mrgF), consecutive pairing; drop leftover if odd.
    cand = sorted([(c, m) for (c, m, s, a) in n3pts
                   if s == 1 and a == 1 and passes(c, m, s, a, OPT)])
    assert all(passes(c, m, 1, 1, OPT) for (c, m) in cand)
    if len(cand) % 2 == 1:
        dropped = cand.pop()
    else:
        dropped = None
    npairs4 = len(cand) // 2
    for pi in range(npairs4):
        for mi in range(2):
            c, m = cand[2 * pi + mi]
            rows.append(("Q", pi, c, m, 1, 1))

    # --- N5-synth: engineered double-arm exploits — SYNTH, src=1
    for c in (874, 1000):
        for m in (6600, 10410):
            assert passes(c, m, 0, 0, OPT) and not passes(c, m, 0, 0, (1, 1, 705, 3588))
            rows.append(("N", 5, c, m, 0, 0, 1))

    out = os.path.join(HERE, "m1_govlh_cases.txt")
    with open(out, "w") as fo:
        for r in rows:
            k = r[0]
            if k == "P":
                fo.write("P|%d|%d|%d|%d|%d\n" % r[1:])
            elif k == "N":
                fo.write("N|%d|%d|%d|%d|%d|%d\n" % r[1:])
            elif k == "Q":
                fo.write("Q|%d|%d|%d|%d|%d\n" % r[1:])
            else:
                fo.write("%s|%d|%d|%d|%d\n" % r)
    nn1 = len(n1)
    nn2 = len(n2)
    nn5r = len(n5r)
    print("wrote %s rows=%d (C=%d W=%d P=%d B=%d N1=%d N2=%d N3=144 N4pairs=%d N5real=%d N5synth=4)"
          % (out, len(rows), nC, nW, nP, nB, nn1, nn2, npairs4, nn5r))
    print("partition: N1+N2+N5real=%d == B passing OPT=%d"
          % (nn1 + nn2 + nn5r, len(b_opt)))
    print("N4 dropped leftover: %s" % (dropped,))
    print("sha=%s" % sha(out))


if __name__ == "__main__":
    main()
