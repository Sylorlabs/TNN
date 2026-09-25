#!/usr/bin/env python3
"""kb_diet_v3c.tsv — NEC v3c B13-fix diet (deterministic).

From ~/workspace/nec_v3b/job2/work/necc_input.tsv (7 cols:
id, fam, depth, f1, f5, rel, corr): keep rows with rel=1.
Emit 6 cols: id \t f1 \t f5 \t depth \t correct \t prov
where prov = `kb-diet-v3c:matrix:<id>`.

PREREG_NCAL_V3C_B13FIX_FROZEN.md §3.1. Zero RNG, pure function of input.
"""
import csv, hashlib, sys

SRC = "/home/hatch/workspace/nec_v3b/job2/work/necc_input.tsv"
DST = "/home/hatch/workspace/nec_v3b/job3/kb_diet_v3c.tsv"

def main():
    rows = list(csv.reader(open(SRC, newline=""), delimiter="\t"))
    kept = []
    for r in rows:
        if len(r) != 7:
            raise SystemExit("bad col count: %r" % (r,))
        rid, fam, depth, f1, f5, rel, corr = r
        if rel != "1":
            continue
        # sanity: integer fields parse
        int(f1); int(f5); int(depth); int(corr)
        if corr not in ("0", "1"):
            raise SystemExit("bad corr: %r" % (r,))
        kept.append((rid, f1, f5, depth, corr, "kb-diet-v3c:matrix:" + rid))
    with open(DST, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        for row in kept:
            w.writerow(row)
    sha = hashlib.sha256(open(DST, "rb").read()).hexdigest()
    print("kept=%d sha256=%s" % (len(kept), sha))
    if len(kept) != 4467:
        raise SystemExit("expected 4467 rows, got %d" % len(kept))

if __name__ == "__main__":
    main()
