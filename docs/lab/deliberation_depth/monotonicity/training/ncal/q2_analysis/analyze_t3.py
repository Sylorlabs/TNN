#!/usr/bin/env python3
"""T3: held-out calibration. mean|conf-true| and signed bias per class + overall."""
truth = {}
for line in open("trap_t3_truth.tsv"):
    c = line.rstrip("\n").split("\t")
    truth[c[0]] = float(c[3])  # C0..C4 -> true rate
def load(fn):
    rows = []
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        cls = c[0].split("-")[0].replace("T3C","C")  # T3C0-000 -> C0
        rows.append((cls, int(c[5])/1000))
    return rows
print("variant | " + " ".join(f"{c}:|err|/bias" for c in sorted(truth)) + " | OVERALL |err|/bias | verdict")
for v in ["m11","floor","u1","u2","g","eb","ind"]:
    rows = load(f"results/{v}_trap_t3_A.tsv")
    ae, se, n = 0.0, 0.0, 0
    parts = []
    for c in sorted(truth):
        cr = [conf for cl,conf in rows if cl==c]
        t = truth[c]
        mae = sum(abs(x-t) for x in cr)/len(cr)
        bias = sum(x-t for x in cr)/len(cr)
        parts.append(f"{mae:.3f}/{bias:+.3f}")
        ae += sum(abs(x-t) for x in cr); se += sum(x-t for x in cr); n += len(cr)
    oae, ose = ae/n, se/n
    ok = oae <= 0.20 and ose >= -0.05
    print(f"{v:5s} | " + " ".join(f"{p:>13s}" for p in parts) + f" | {oae:.3f}/{ose:+.3f} | {'PASS' if ok else 'FAIL'}")
