#!/usr/bin/env python3
"""Generate B9X2 release-redesign inputs (deterministic, zero RNG).

Reads the frozen necc_input.tsv and m11 d1 confidences (from q1/results_q1
A-run legs), and writes:
  q1/inputs/b9x_strat.tsv  (mech 37: confidence-stratified nested release)
  q1/inputs/b9x_grad.tsv   (mech 38: gradual phase-out of below-mean drops)

Columns: id, fam, depth, f1, f5, release(1/0), correct(imputed per verified
1000/1000 label-constancy). Frozen f1/f5 kept verbatim; frozen row order kept.

B9X-STRAT (per battery):
  1. d1 cohort C = items released at d1 under M4 (= all items at d1).
  2. Rank C by (m11 d1 conf asc, item id asc); decile = rank*10 // |C|.
  3. Within each decile sort by id; interleave round-robin across deciles 0..9.
  4. At depth d release the first K_d ids of that order, K_d = M4's released
     count at (battery, d). Nested; d1 set == M4's d1 set.

B9X-GRAD (per battery):
  R_d = M4's released set at depth d (nested). G_1 = R_1.
  G_{d'} = R_{d'} UNION first-half-by-id of (R_d - R_{d'}), i.e. half of each
  item-batch M4 drops is retained for exactly one extra depth. Nested;
  superset of M4.

Usage: gen_b9x2.py <ncal_dir>
Writes into <ncal_dir>/q1/inputs/. Prints design statistics.
"""
import sys, os
from collections import defaultdict

BATTERY_DEPTHS = {
    "admit": [1,2,4,8,16], "revoke": [1,2,4,8,16], "logic": [1,2,4,8,16],
    "trap": [1,2,4,8,16], "cost": [1,2,4,8,16], "redteam": [1,2,4,8,16],
    "ceiling": [1,2,4,8,16,32,64],
}

def main():
    ncal = sys.argv[1]
    inp = os.path.join(ncal, "necc_input.tsv")
    resdir = os.path.join(ncal, "q1", "results_q1")
    outdir = os.path.join(ncal, "q1", "inputs")

    # ---- load frozen input ----
    rows = []  # (id, fam, depth, f1, f5, rel, corr)
    rel = defaultdict(set)   # (fam, depth) -> set(ids released under M4)
    label = {}               # id -> constant correct label (from released cells)
    cell = defaultdict(dict) # id -> depth -> (fam, f1, f5, rel, corr)
    with open(inp) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            iid, fam, depth, f1, f5, r, c = line.split("\t")
            depth = int(depth)
            rows.append((iid, fam, depth, f1, f5, r, c))
            cell[iid][depth] = (fam, f1, f5, r, c)
            if r == "1":
                rel[(fam, depth)].add(iid)
                if iid in label:
                    assert label[iid] == c, f"label not constant for {iid}"
                label[iid] = c
    n_items = len(cell)
    assert n_items == 1000, f"expected 1000 items, got {n_items}"
    assert len(label) == 1000, "every item must have >=1 released cell"

    # ---- m11 d1 conf per item (A-run legs) ----
    d1conf = {}  # id -> conf (thousandths)
    for battery in BATTERY_DEPTHS:
        fn = os.path.join(resdir, f"{battery}_m11_d1_A.tsv")
        with open(fn) as f:
            for line in f:
                cols = line.rstrip("\n").split("\t")
                iid, corr, conf = cols[0], cols[7], int(cols[8])
                assert corr in ("1", "0"), f"d1 cell not released: {iid}"
                d1conf[iid] = conf
    assert len(d1conf) == 1000

    # ---- per-battery depth lists present in the matrix ----
    depths_of = defaultdict(set)
    for (fam, d) in rel:
        depths_of[fam].add(d)

    strat_rel = defaultdict(set)  # (fam, depth) -> set(ids)
    grad_rel = defaultdict(set)

    for fam in sorted(depths_of):
        depths = sorted(depths_of[fam])
        # d1 cohort
        cohort = sorted(rel[(fam, 1)])
        # STRAT: deciles by (conf asc, id asc)
        ranked = sorted(cohort, key=lambda i: (d1conf[i], i))
        n = len(ranked)
        dec = defaultdict(list)
        for rank, iid in enumerate(ranked):
            dec[rank * 10 // n].append(iid)
        for k in dec:
            dec[k].sort()
        order = []
        while len(order) < n:
            for k in range(10):
                if dec[k]:
                    order.append(dec[k].pop(0))
        assert len(order) == n and set(order) == set(cohort)
        prev = None
        for d in depths:
            k = len(rel[(fam, d)])
            s = set(order[:k])
            strat_rel[(fam, d)] = s
            if prev is not None:
                assert s <= prev, f"STRAT not nested: {fam} d{d}"
            prev = s
        # GRAD: retain half of each M4 drop for one extra depth
        g = set(rel[(fam, depths[0])])
        grad_rel[(fam, depths[0])] = set(g)
        for di in range(1, len(depths)):
            d, dp = depths[di - 1], depths[di]
            m4drop = sorted(rel[(fam, d)] - rel[(fam, dp)])
            keep = set(m4drop[:len(m4drop) // 2])
            g = set(rel[(fam, dp)]) | keep
            grad_rel[(fam, dp)] = set(g)
        # nestedness check for GRAD
        prev = None
        for d in depths:
            s = grad_rel[(fam, d)]
            if prev is not None:
                assert s <= prev, f"GRAD not nested: {fam} d{d}"
            assert rel[(fam, d)] <= s, f"GRAD not a superset of M4: {fam} d{d}"
            prev = s

    def write(name, relmap):
        fn = os.path.join(outdir, name)
        with open(fn, "w") as f:
            for (iid, fam, depth, f1, f5, r, c) in rows:
                nr = "1" if iid in relmap[(fam, depth)] else "0"
                f.write("\t".join([iid, fam, str(depth), f1, f5, nr, label[iid]]) + "\n")
        return fn

    fs = write("b9x_strat.tsv", strat_rel)
    fg = write("b9x_grad.tsv", grad_rel)

    # ---- statistics ----
    for tag, relmap in (("STRAT", strat_rel), ("GRAD", grad_rel)):
        print(f"== {tag} ==")
        for fam in sorted(depths_of):
            ks = [(d, len(relmap[(fam, d)]), len(rel[(fam, d)])) for d in sorted(depths_of[fam])]
            print(f"  {fam}: " + " ".join(f"d{d}:{k}(M4:{m})" for d, k, m in ks))
    print("wrote", fs)
    print("wrote", fg)

if __name__ == "__main__":
    main()
