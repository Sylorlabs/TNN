#!/usr/bin/env python3
"""Byte-exact Python sims of nec_v3c.zag variants 26/27/28 (NEC v3c JOB3).

Rule (from src/nec_v3c.zag, verified lines 240-370):
- idx<0 (first observation): 26/27 -> cl_mil = kc_lookup(f1,f5,depth,min_n) rate
  (millionths), stored as latch ceiling; 28 -> cl_mil = ka_schema(cls).
  personal ledger seeded ptp=1, pcp=(corr==1).
- idx>=0: p_raw = (cp*1_000_000)//tp (pre-update ledger);
  26/27: cl_mil = min(p_raw, latch); latch = cl_mil.
  28 (nolatch=1): cl_mil = p_raw (seed expires, no latch).
- emitted conf = cl_mil//1000 (thousandths).
- nopool=1: no class ledger. The 63-byte id cap is an IMPLEMENTATION defect in
  nec_cmp_id (not a design choice): this sim uses full ids, so it is byte-exact
  on batteries with all ids <= 63 bytes; RT-F (72-char ids) is binary-only.

K-C tables parsed from src/schema_kc.zag (L1/L2/L3 if-chains); K-A from
src/schema_ka.zag (ka_schema if-chain, cls = min(f1//150,6)*5 + min(f5//250,4)).

Validation: each mode must reproduce its Zag binary output byte-for-byte on
necc_input.tsv, trap_t1.tsv, trap_t3.tsv (s1 matrices, short ids).
Usage: sim_v3c.py <m26|m27|m28> <in.tsv>
Prints 6-col driver output (id,fam,depth,rel,corr,conf_thousandths).
"""
import sys, re, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "src")

def parse_kc():
    txt = open(os.path.join(SRC, "schema_kc.zag")).read()
    l1, l2, l3 = {}, {}, {}
    for m in re.finditer(r"if\(f1==(\d+) && f5==(\d+) && dep==(\d+)\)\{tot\.\*=(\d+);rate\.\*=(\d+);", txt):
        l1[(int(m.group(1)), int(m.group(2)), int(m.group(3)))] = (int(m.group(4)), int(m.group(5)))
    for m in re.finditer(r"if\(f1==(\d+) && f5==(\d+)\)\{tot\.\*=(\d+);rate\.\*=(\d+);", txt):
        l2[(int(m.group(1)), int(m.group(2)))] = (int(m.group(3)), int(m.group(4)))
    for m in re.finditer(r"if\(dep==(\d+)\)\{tot\.\*=(\d+);rate\.\*=(\d+);", txt):
        l3[int(m.group(1))] = (int(m.group(2)), int(m.group(3)))
    return l1, l2, l3, 896575  # L4 rate (frozen, header comment)

def parse_ka():
    txt = open(os.path.join(SRC, "schema_ka.zag")).read()
    s = {}
    for m in re.finditer(r"if\(cls==(\d+)\)\{return (\d+)\}", txt):
        s[int(m.group(1))] = int(m.group(2))
    return s

L1, L2, L3, L4RATE = parse_kc()
KA = parse_ka()
assert len(L1) == 312 and len(L2) == 246 and len(L3) == 7, (len(L1), len(L2), len(L3))
assert len(KA) == 35

def kc_lookup(f1, f5, dep, min_n):
    k = (f1, f5, dep)
    if k in L1 and L1[k][0] >= min_n:
        return L1[k][1], 1, L1[k][0]
    k2 = (f1, f5)
    if k2 in L2 and L2[k2][0] >= min_n:
        return L2[k2][1], 2, L2[k2][0]
    if dep in L3 and L3[dep][0] >= min_n:
        return L3[dep][1], 3, L3[dep][0]
    return L4RATE, 4, 4467

def ka_cls(f1, f5):
    return min(f1 // 150, 6) * 5 + min(f5 // 250, 4)

def run(in_tsv, mode):
    min_n = {"m26": 1, "m27": 8}[mode] if mode in ("m26", "m27") else None
    latch, pers = {}, {}   # id -> cl_mil ceiling ; id -> [cp,tp]
    out = []
    diag = []  # per released cell: (iid,depth,seed_rate_mil,cp,tp,p_raw_mil,conf_mil)
    for line in open(in_tsv):
        line = line.rstrip("\n")
        if not line: continue
        iid, fam, depth, f1, f5, rel, corr = line.split("\t")
        depth, f1, f5, rel, corr = int(depth), int(f1), int(f5), int(rel), int(corr)
        conf = 0
        if rel == 1:
            cp, tp = pers.get(iid, [0, 0])
            p_raw = (cp * 1000000) // tp if tp >= 1 else -1
            if mode in ("m26", "m27"):
                if iid not in latch:
                    seed, level, celln = kc_lookup(f1, f5, depth, min_n)
                    cm = seed
                    latch[iid] = cm
                else:
                    seed, _, _ = kc_lookup(f1, f5, depth, min_n)
                    cm = p_raw if p_raw < latch[iid] else latch[iid]
                    latch[iid] = cm
                conf = cm // 1000
                diag.append((iid, depth, seed, cp, tp, p_raw, cm))
            else:  # m28: K-A at tp=0, p_raw thereafter (no latch)
                if iid not in latch:
                    seed = KA[ka_cls(f1, f5)]
                    cm = seed
                    latch[iid] = cm  # stored but never consulted
                else:
                    seed = KA[ka_cls(f1, f5)]
                    cm = p_raw
                conf = cm // 1000
                diag.append((iid, depth, seed, cp, tp, p_raw, cm))
            tp += 1
            if corr == 1: cp += 1
            pers[iid] = [cp, tp]
        out.append(f"{iid}\t{fam}\t{depth}\t{rel}\t{corr}\t{conf}")
    return out, diag

if __name__ == "__main__":
    mode = sys.argv[1]
    out, _ = run(sys.argv[2], mode)
    sys.stdout.write("\n".join(out) + "\n")
