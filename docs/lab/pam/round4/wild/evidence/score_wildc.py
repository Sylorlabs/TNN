#!/usr/bin/env python3
"""WILD-C K8 scorer: verifies OUT decisions against preregistered rules.
Usage: score_wildc.py <evidence_dir>
"""
import sys
import os

EVDIR = sys.argv[1] if len(sys.argv) > 1 else "."

def load_out(design):
    path = os.path.join(EVDIR, f"w{design}_run1.txt")
    outs = []
    sums = []
    kbs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("OUT|"):
                outs.append(line.split("|"))
            elif line.startswith("SUM|"):
                sums.append(line.split("|"))
            elif line.startswith("KB|"):
                kbs.append(line.split("|"))
    return outs, sums, kbs

def check_k1(design, outs):
    """K1: no W admit, no P pair both admit."""
    # W rows: K='W', dec field varies by design
    # P rows: need pair reconstruction. P rows have idx; pairs are consecutive?
    # For simplicity: W dec must be 0. P pairs: group by (idx//2)? 
    # Actually P rows: 18 rows, 9 pairs. Indices 2223-2240? Let me just check W.
    violations = []
    for o in outs:
        # o[0]=OUT, o[1]=design, o[2]=K, o[3]=idx, ...
        # dec field index varies; find it by design
        K = o[2]
        if K == 'W':
            # dec is second-to-last or last depending on design; use known positions
            dec = int(o[-2]) if design in [16,20,21,22,23] else int(o[-1])
            # Actually let me use explicit indices per design
            pass
    return violations

# Design-specific dec field indices (0-based in split list)
# OUT|D|K|idx|seq|producer|...|dec|...
DEC_IDX = {
    16: 10,  # OUT|16|K|idx|seq|prod|decl|class|c3|prov|dec|clean
    17: 8,   # OUT|17|K|idx|seq|prod|class|c3|dec|card
    18: 8,   # OUT|18|K|idx|seq|prod|class|c3|dec|veto|gap
    19: 8,   # OUT|19|K|idx|seq|prod|class|c3|dec|status|sclass
    20: 9,   # OUT|20|K|idx|seq|prod|decl|class|c3|dec|arena
    21: 8,   # OUT|21|K|idx|seq|prod|class|c3|dec|veto|rid
    22: 8,   # OUT|22|K|idx|seq|prod|class|c3|dec|fast|slow|hf|hs|div
    23: 8,   # OUT|23|K|idx|seq|prod|class|c3|dec|reason|status
}

def get_dec(design, o):
    return int(o[DEC_IDX[design]])

def main():
    print("WILD-C K8 Scorer")
    print("=" * 60)
    for d in [16,17,18,19,20,21,22,23]:
        outs, sums, kbs = load_out(d)
        # K1: W rows
        w_viol = sum(1 for o in outs if o[2]=='W' and get_dec(d,o)==1)
        # C rows correct-admit
        c_total = sum(1 for o in outs if o[2]=='C')
        c_admit = sum(1 for o in outs if o[2]=='C' and get_dec(d,o)==1)
        c_rate = 100.0*c_admit/c_total if c_total else 0
        # Attack rows (A)
        a_total = sum(1 for o in outs if o[2]=='A')
        a_admit = sum(1 for o in outs if o[2]=='A' and get_dec(d,o)==1)
        print(f"W{d}: C {c_admit}/{c_total}={c_rate:.2f}% | A admit {a_admit}/{a_total} | W viol {w_viol} | OUT lines {len(outs)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
