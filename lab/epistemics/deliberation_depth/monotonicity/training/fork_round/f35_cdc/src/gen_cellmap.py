#!/usr/bin/env python3
"""Generate params/cellmap.tsv for F35 CDC.

Reads the frozen M4 result TSVs (results_100x/*_m4_d*_A.tsv) and emits them
in features.tsv row order (5,240 rows). The policy binary replaces only the
confidence column; all other columns (incl. release/correct) are M4-identical.

Verifies: 5,240 rows; every (family, depth, id) present; (id, depth) match.
"""
import sys, os

TRAIN = os.path.expanduser("~/workspace/tnn-lab/deliberation_depth/monotonicity/training")
FEAT = os.path.join(TRAIN, "features", "features.tsv")
R100 = os.path.join(TRAIN, "results_100x")
OUT = os.path.join(TRAIN, "fork_round", "f35_cdc", "params", "cellmap.tsv")

FAMS = ["admit", "revoke", "logic", "trap", "cost", "redteam", "D", "O", "P"]
DEPTHS = {"admit": [1,2,4,8,16], "revoke": [1,2,4,8,16], "logic": [1,2,4,8,16],
          "trap": [1,2,4,8,16], "cost": [1,2,4,8,16], "redteam": [1,2,4,8,16],
          "D": [1,2,4,8,16,32,64], "O": [1,2,4,8,16,32,64], "P": [1,2,4,8,16,32,64]}

def main():
    m4 = {}
    def index_file(p):
        with open(p) as f:
            for ln, line in enumerate(f):
                line = line.rstrip("\n")
                if not line:
                    continue
                cols = line.split("\t")
                assert len(cols) == 11, (p, ln, len(cols))
                key = (int(cols[1]), cols[0])  # (depth, id); family resolved at emit
                assert key not in m4, f"dup {key}"
                m4[key] = line
    for fam in ["admit", "revoke", "logic", "trap", "cost", "redteam"]:
        for d in DEPTHS[fam]:
            index_file(os.path.join(R100, f"{fam}_m4_d{d}_A.tsv"))
    for d in DEPTHS["D"]:
        index_file(os.path.join(R100, f"ceiling_m4_d{d}_A.tsv"))
    print(f"m4 rows indexed: {len(m4)}", file=sys.stderr)

    n_out = 0
    n_feat = 0
    with open(FEAT) as f, open(OUT, "w") as o:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            n_feat += 1
            c = line.split("\t")
            key = (int(c[3]), c[0])
            row = m4.get(key)
            if row is None:
                print(f"MISSING {key}", file=sys.stderr)
                sys.exit(1)
            rc = row.split("\t")
            assert rc[0] == c[0] and int(rc[1]) == int(c[3]), f"mismatch {key}"
            o.write(row + "\n")
            n_out += 1
    print(f"features rows: {n_feat}, cellmap rows: {n_out}", file=sys.stderr)
    assert n_feat == 5240 and n_out == 5240, "row count"
    print("cellmap OK", file=sys.stderr)

main()
