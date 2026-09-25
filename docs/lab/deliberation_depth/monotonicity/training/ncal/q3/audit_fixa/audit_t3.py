#!/usr/bin/env python3
"""T3 (FIX-A audit): held-out calibration on FIX-A-augmented trap_t3.
mean|conf-true| and signed bias per class + overall vs trap_t3_truth.tsv.
PASS ⟺ overall |err| <= 0.20 and bias >= -0.05 (preregistered rule).
Usage: audit_t3.py <trap_t3_FIXA driver out> <trap_t3_truth.tsv>
"""
import sys
out_tsv, truth_tsv = sys.argv[1], sys.argv[2]
truth = {}
for line in open(truth_tsv):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])
rows = []
for line in open(out_tsv):
    c = line.rstrip("\n").split("\t")
    if not c[0].startswith("T3C"):
        continue
    cls = c[0].split("-")[0].replace("T3C", "C")
    rows.append((cls, int(c[5]) / 1000))
ae, se, n = 0.0, 0.0, 0
parts = []
for cl in sorted(truth):
    cr = [conf for k, conf in rows if k == cl]
    t = truth[cl]
    mae = sum(abs(x - t) for x in cr) / len(cr)
    bias = sum(x - t for x in cr) / len(cr)
    parts.append(f"{cl}:|err|={mae:.3f},bias={bias:+.3f}")
    ae += sum(abs(x - t) for x in cr); se += sum(x - t for x in cr); n += len(cr)
oae, ose = ae / n, se / n
ok = oae <= 0.20 and ose >= -0.05
print(" | ".join(parts))
print(f"T3 FIX-A: overall |err|={oae:.3f} bias={ose:+.3f} -> {'PASS' if ok else 'FAIL'}")
