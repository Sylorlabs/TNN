#!/usr/bin/env python3
"""Build FIX-* curriculum inputs from a base input (s1/s10/s100).
All deterministic, zero RNG. m11 mechanism frozen; only the INPUT varies.

FIX-A: prior-anchoring. For each class with honest-correct cells and pooled
       rate < 0.95, add correct anchors until empirical rate = 0.95.
       Count = ceil((0.95*t - c)/0.05), derived from frozen p0=0.95.
FIX-B: scale-graded calibration. 1:1 replication of every honest correct
       released cell (release=1, correct=1), new IDs, uniform interleave.
FIX-C: underconfidence traps. For each released WRONG cell in the 7 polluted
       classes, add one CORRECT trap with identical (f1,f5) (adversarial
       honesty: matched 1:1, indistinguishable by allowed features).
FIX-D: deployment-mix thinning. Drop released wrong cells except every 20th
       in input order (5% kept, derived from p0=0.95); all else untouched.

Anchor/trap/calib cells: fam in {anchor,calib,trapu}, depth=1, release=1,
correct=1, unique deterministic IDs. convert.py skips fam anchor/calib/trapu
(they update the ledger but are not scored; bars measured on 37-leg matrix).

Usage: fixbuild.py <base.tsv> <FIX-A|FIX-B|FIX-C|FIX-D> <out.tsv>
"""
import sys
import math

POLLUTED = [5, 10, 12, 15, 16, 17, 18]

def cls_of(f1, f5):
    return min(f1 // 150, 6) * 5 + min(f5 // 250, 4)

def read_base(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            c = line.split("\t")
            rows.append({
                "id": c[0], "fam": c[1], "depth": int(c[2]),
                "f1": int(c[3]), "f5": int(c[4]),
                "rel": int(c[5]), "corr": int(c[6]),
                "raw": line,
            })
    return rows

def interleave(base_rows, extra_by_group):
    """Uniformly interleave each group's extras through base_rows (deterministic).
    extra_by_group: dict group -> list of row-dicts. Each group's items are
    spread uniformly and INDEPENDENTLY, so no group clusters in one region.
    Returns list of formatted TSV lines."""
    n = len(base_rows)
    # (base_position, group_order, seq, rowdict)
    placements = []
    for g, items in extra_by_group.items():
        a = len(items)
        if a == 0:
            continue
        for j, rd in enumerate(items):
            # uniform position for this group's j-th item
            pos = (j * n) // a
            placements.append((pos, g, j, rd))
    # sort by position; tie-break deterministically by (group, seq)
    placements.sort(key=lambda x: (x[0], x[1], x[2]))
    out_lines = []
    p = 0
    nplace = len(placements)
    for i, r in enumerate(base_rows):
        while p < nplace and placements[p][0] <= i:
            out_lines.append(fmt(placements[p][3]))
            p += 1
        out_lines.append(r["raw"] if isinstance(r, dict) else r)
    while p < nplace:
        out_lines.append(fmt(placements[p][3]))
        p += 1
    return out_lines

def fmt(cell):
    return "\t".join([cell["id"], cell["fam"], str(cell["depth"]),
                       str(cell["f1"]), str(cell["f5"]),
                       str(cell["rel"]), str(cell["corr"])])

def fix_a(rows):
    # per-class (c,t) over released cells; (f1,f5) of correct cells per class
    ct = {}
    f1f5 = {}
    for r in rows:
        if r["rel"] != 1:
            continue
        cls = cls_of(r["f1"], r["f5"])
        c, t = ct.get(cls, (0, 0))
        t += 1
        if r["corr"] == 1:
            c += 1
            f1f5.setdefault(cls, []).append((r["f1"], r["f5"]))
        ct[cls] = (c, t)
    by_cls = {}
    total = 0
    for cls in sorted(ct):
        c, t = ct[cls]
        if t == 0 or c / t >= 0.95:
            continue
        if cls not in f1f5:
            continue  # no honest (f1,f5) to copy; skip
        need = math.ceil((0.95 * t - c) / 0.05)
        pool = f1f5[cls]
        lst = []
        for j in range(need):
            f1, f5 = pool[j % len(pool)]
            lst.append({
                "id": f"A{cls:02d}{j:06d}", "fam": "a", "depth": 1,
                "f1": f1, "f5": f5, "rel": 1, "corr": 1,
            })
        by_cls[cls] = lst
        total += need
    print(f"FIX-A: {total} anchors in {len(by_cls)} classes")
    return interleave(rows, by_cls)

def fix_b(rows):
    calibs = []
    j = 0
    for r in rows:
        if r["rel"] == 1 and r["corr"] == 1:
            calibs.append({
                "id": f"C{j:06d}", "fam": "c", "depth": 1,
                "f1": r["f1"], "f5": r["f5"], "rel": 1, "corr": 1,
            })
            j += 1
    print(f"FIX-B: {len(calibs)} calibration replicas (1:1 honest)")
    return interleave(rows, {"calib": calibs})

def fix_c(rows):
    by_cls = {}
    j = 0
    for r in rows:
        cls = cls_of(r["f1"], r["f5"])
        if r["rel"] == 1 and r["corr"] == 0 and cls in POLLUTED:
            by_cls.setdefault(cls, []).append({
                "id": f"T{j:06d}", "fam": "t", "depth": 1,
                "f1": r["f1"], "f5": r["f5"], "rel": 1, "corr": 1,
            })
            j += 1
    print(f"FIX-C: {j} matched honest traps in {len(by_cls)} classes")
    return interleave(rows, by_cls)

def fix_d(rows):
    out = []
    kept = dropped = 0
    w = 0
    for r in rows:
        if r["rel"] == 1 and r["corr"] == 0:
            if w % 20 == 0:
                out.append(r["raw"])
                kept += 1
            else:
                dropped += 1
            w += 1
        else:
            out.append(r["raw"])
    print(f"FIX-D: kept {kept} released-wrong, dropped {dropped}")
    return out

def main():
    base, fix, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    rows = read_base(base)
    fn = {"FIX-A": fix_a, "FIX-B": fix_b, "FIX-C": fix_c, "FIX-D": fix_d}[fix]
    lines = fn(rows)
    with open(out_path, "w") as f:
        for ln in lines:
            f.write(ln + "\n")
    print(f"wrote {out_path}: {len(lines)} rows")

if __name__ == "__main__":
    main()
