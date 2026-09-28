#!/usr/bin/env python3
"""Convert nec_scale driver output to frozen-analyzer per-leg TSVs.
Driver output cols: id, fam, depth, release, correct, conf_thousandths
Analyzer format per leg file {battery}_m{mech}_d{depth}_{run}.tsv:
  id, depth, 0,0,0,0, RELEASE, correct|A, conf, 0, 0
release=0 -> correct='A' (abstained). Battery from fam col (ceiling stays ceiling).
Usage: convert.py <driver_out.tsv> <mech_id> <run_letter> <out_dir>
"""
import sys, os
from collections import defaultdict

def main():
    out_path, mech, run, outdir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    os.makedirs(outdir, exist_ok=True)
    legs = defaultdict(list)
    skipped = 0
    with open(out_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            cols = line.split("\t")
            iid, fam, depth = cols[0], cols[1], cols[2]
            if fam in ("a", "c", "t"):
                # fixture-only curriculum cells (compact fams a/c/t): update the ledger but are not
                # scored; bars measured on the 37-leg matrix
                skipped += 1
                continue
            rel, corr, conf = cols[3], cols[4], cols[5]
            battery = fam  # fam col holds battery name; ceiling items keep fam='ceiling'
            corr_out = corr if rel == "1" else "A"
            rel_out = "RELEASE" if rel == "1" else "ABSTAIN"
            legs[(battery, depth)].append(
                f"{iid}\t{depth}\t0\t0\t0\t0\t{rel_out}\t{corr_out}\t{conf}\t0\t0\n")
    for (battery, depth), rows in legs.items():
        fn = os.path.join(outdir, f"{battery}_m{mech}_d{depth}_{run}.tsv")
        with open(fn, "w") as f:
            f.writelines(rows)
    print(f"wrote {len(legs)} leg files to {outdir}; skipped {skipped} fixture cells")

if __name__ == "__main__":
    main()
