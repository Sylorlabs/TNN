#!/usr/bin/env python3
"""Generate the frozen K-B training diet kb_diet_v1.tsv (deterministic, zero RNG).
Spec: ADDENDUM_V3B_JOB2_DIET_2026-09-25.md §2.1.
Usage: gen_kb_diet.py <out.tsv>
Oracle rates R (millionths) per bin — byte-identical to the addendum §1 table.
"""
import sys

# (cls -> R millionths), from ADDENDUM §1 (K-A oracle table)
ORACLE = {
    0:0, 1:0, 2:0, 3:1000000, 4:750000, 5:515152, 6:0, 7:0, 8:1000000,
    9:500000, 10:673469, 11:1000000, 12:62500, 13:250000, 14:0, 15:775578,
    16:652174, 17:659091, 18:666667, 19:1000000, 20:1000000, 21:1000000,
    22:1000000, 23:0, 24:1000000, 25:1000000, 26:1000000, 27:1000000,
    # 28: absent by design (no evidence anywhere -> learner must ABSTAIN)
    29:1000000, 30:1000000, 31:997290, 32:996226, 33:1000000, 34:996964,
}
N = 1000

def main():
    out = sys.argv[1]
    rows = []
    for cls in sorted(ORACLE):
        R = ORACLE[cls]
        mb, cb = cls // 5, cls % 5
        f1, f5 = mb * 150 + 75, cb * 250 + 125
        # binning rule round-trip check (same rule as nec_v2d.zag)
        assert min(f1 // 150, 6) == mb and min(f5 // 250, 4) == cb, (cls, f1, f5)
        assert min(f1 // 150, 6) * 5 + min(f5 // 250, 4) == cls
        K = (R * N + 500000) // 1000000  # round(R*N/1e6)
        ncorr = 0
        for i in range(N):
            corr = 1 if (i * K) % N < K else 0
            ncorr += corr
            iid = f"KBDIET-{cls:02d}-{i:04d}"
            prov = f"kb-diet-v1:bin{cls:02d}:i{i:04d}:rate{R}"
            rows.append(f"{iid}\t{f1}\t{f5}\t{corr}\t{prov}")
        assert ncorr == K, (cls, K, ncorr)
    with open(out, "w") as f:
        f.write("\n".join(rows) + "\n")
    print(f"wrote {out}: {len(rows)} rows, {len(ORACLE)} bins (28 absent)")

if __name__ == "__main__":
    main()
