#!/usr/bin/env python3
"""T3 held-out calibration for the v3d head-to-head (v20 vs v26).
Same metric as job3 t13_v3c.py T3 section: mean|conf-true|, signed bias per
class + overall; frozen rule: overall mean|err| < 0.470 AND bias >= -0.05.
Usage: t3_h2h.py <workdir>   (expects v20_t3_A.tsv, v26_t3_A.tsv,
trap_t3_truth.tsv in workdir)
"""
import sys
W = sys.argv[1]
truth = {}
for line in open(f"{W}/trap_t3_truth.tsv"):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])

def load3(fn):
    rows = []
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        cls = c[0].split("-")[0].replace("T3C", "C")
        rows.append((cls, int(c[5]) / 1000))
    return rows

print("== T3 head-to-head (frozen rule: overall <0.470 AND bias>=-0.05) ==")
print("variant | " + " ".join(f"{c}:|err|/bias" for c in sorted(truth)) +
      " | OVERALL |err|/bias | rule | n")
for tag in ("v20", "v26"):
    rows = load3(f"{W}/{tag}_t3_A.tsv")
    ae, se, n = 0.0, 0.0, 0
    parts = []
    for c in sorted(truth):
        cr = [conf for cl, conf in rows if cl == c]
        t = truth[c]
        mae = sum(abs(x - t) for x in cr) / len(cr)
        bias = sum(x - t for x in cr) / len(cr)
        parts.append(f"{mae:.4f}/{bias:+.4f}")
        ae += sum(abs(x - t) for x in cr); se += sum(x - t for x in cr); n += len(cr)
    oae, ose = ae / n, se / n
    ok = oae < 0.470 and ose >= -0.05
    print(f"{tag:5s} | " + " ".join(parts) +
          f" | {oae:.4f}/{ose:+.4f} | {'PASS' if ok else 'FAIL'} | {n}")
