#!/usr/bin/env python3
"""T4 (FIX-A audit): principled-prior comparison on the FIX-A diet.
Sims of m11 (p0=0.95), m_eb (self-estimated prior), m_ind (p0=0.5) on the
FIX-A-augmented s1 input; outputs converted + barred identically.
Usage: audit_t4.py <necc_s1_FIXA.tsv> <outdir>
Writes <outdir>/t4_<variant>_A.tsv (driver-format: id fam depth rel corr conf).
"""
import sys, os

def run(in_tsv, mode):
    assert mode in ("m11", "eb", "ind")
    led = {}; pers = {}; prev = {}
    eb_cg = 0; eb_tg = 0
    out = []
    for line in open(in_tsv):
        line = line.rstrip("\n")
        if not line:
            continue
        iid, fam, depth, f1, f5, rel, corr = line.split("\t")
        depth, f1, f5, rel, corr = int(depth), int(f1), int(f5), int(rel), int(corr)
        conf = 0
        if rel == 1:
            cls = (min(f1 // 150, 6), min(f5 // 250, 4))
            c, t = led.get(cls, [0, 0])
            if mode == "m11":
                class_rate = (c * 1000000 + 1900000) // (t + 2)
            elif mode == "ind":
                class_rate = (c * 1000000 + 1000000) // (t + 2)
            else:
                eb_p0 = 500000 if eb_tg < 1 else (eb_cg * 1000000) // eb_tg
                class_rate = (c * 1000000 + 2 * eb_p0) // (t + 2)
            cp, tp = pers.get(iid, [0, 0])
            cm = class_rate
            if tp >= 1:
                p_raw = (cp * 1000000) // tp
                if cm > p_raw:
                    cm = p_raw
            pc = prev.get(iid)
            if pc is not None and cm > pc:
                cm = pc
            prev[iid] = cm
            conf = cm // 1000
            t += 1
            if corr == 1:
                c += 1
            led[cls] = [c, t]
            tp += 1
            if corr == 1:
                cp += 1
            pers[iid] = [cp, tp]
            eb_tg += 1
            if corr == 1:
                eb_cg += 1
        out.append(f"{iid}\t{fam}\t{depth}\t{rel}\t{corr}\t{conf}")
    return out

in_tsv, outdir = sys.argv[1], sys.argv[2]
os.makedirs(outdir, exist_ok=True)
for mode in ("m11", "eb", "ind"):
    out = run(in_tsv, mode)
    fn = os.path.join(outdir, f"t4_{mode}_A.tsv")
    with open(fn, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"wrote {fn} ({len(out)} rows)")
