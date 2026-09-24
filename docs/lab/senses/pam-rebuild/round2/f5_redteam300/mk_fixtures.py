#!/usr/bin/env python3
"""Deterministic fixture generator for the F5 300-percept red-team.

Zero RNG: every value is a literal parameter sweep. Regeneration is
byte-identical (SHA-checked in the battery notes).

Ledger format: same 17 fields as v2/redteam ledger_d_withhold.txt, plus a
trailing field 17 `SET=NEAR` / `SET=FAR`:
  prev_hash|link_hash|seq|tcode|fixture|prog|jcode|judgment|confidence|pred|
  measure|phash|truth|jG|confG|DISP=ACCEPT_INSTALL|DETAIL=det_rt300|SET=...

All 360 lines are truth-correct (judgment == truth) by construction.
"""
import hashlib
import sys

ZERO64 = "0" * 64

def line(seq, fixture, judgment, truth, conf, measure, setname):
    fields = [
        ZERO64,                 # 0 prev_hash (synthetic)
        ZERO64,                 # 1 link_hash (synthetic)
        str(seq),               # 2 seq
        "3",                    # 3 tcode
        fixture,                # 4 fixture
        "2",                    # 5 prog
        "1",                    # 6 jcode
        judgment,               # 7 judgment
        str(conf),              # 8 confidence
        "0",                    # 9 pred
        str(measure),           # 10 measure
        ZERO64,                 # 11 phash (synthetic)
        truth,                  # 12 truth
        "1",                    # 13 jG
        str(conf),              # 14 confG
        "DISP=ACCEPT_INSTALL",  # 15
        "DETAIL=det_rt300",     # 16
        "SET=" + setname,       # 17
    ]
    return "|".join(fields) + "\n"

def main():
    out = []
    # --- 300 near-exemplar correct percepts (TMB-5, RICH/RICH) ---
    # conf = 650+10*i (i=0..29); measure = 2200+500*j (j=0..9); row-major.
    seq = 0
    for i in range(30):
        conf = 650 + 10 * i
        for j in range(10):
            measure = 2200 + 500 * j
            fixture = "rt4_TMB-5_%04d.r24" % seq
            out.append(line(seq, fixture, "RICH", "RICH", conf, measure, "NEAR"))
            seq += 1
    assert seq == 300, seq
    # --- 60 far controls ---
    # 20x COL family (different stem)
    for k in range(20):
        conf = 800 + 5 * k
        measure = 50000 + 500 * k
        fixture = "rt4_COL-4_%04d.r24" % seq
        out.append(line(seq, fixture, "SAME", "SAME", conf, measure, "FAR"))
        seq += 1
    # 20x TMB family, outside both windows (conf>868, measure>4647)
    for k in range(20):
        conf = 950 + 2 * k
        measure = 5500 + 50 * k
        fixture = "rt4_TMB-5_%04d.r24" % seq
        out.append(line(seq, fixture, "RICH", "RICH", conf, measure, "FAR"))
        seq += 1
    # 20x PTC family (different stem)
    for k in range(20):
        conf = 780 + 8 * k
        measure = 1000 + 2500 * k
        fixture = "rt4_PTC-4_%04d.r24" % seq
        out.append(line(seq, fixture, "HIGHER", "HIGHER", conf, measure, "FAR"))
        seq += 1
    assert seq == 360, seq
    data = "".join(out).encode()
    with open(sys.argv[1], "wb") as f:
        f.write(data)
    print("wrote %d lines sha256=%s" % (len(out), hashlib.sha256(data).hexdigest()))

if __name__ == "__main__":
    main()
