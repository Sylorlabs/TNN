#!/usr/bin/env python3
"""Byte-exact Python sims of nec_v2d.zag variant rules (m15/m20/m11/pool).
Modes:
  m15  : class ledger (c*1e6+2e6)/(t+2), personal min-cap (tp>=1), ceiling
  m20  : personal-only: p_raw if tp>=1 else d1prior (param), ceiling
  m11  : class ledger (c*1e6+1.9e6)/(t+2), personal min-cap, ceiling
  pool : m11's class-ledger pre-cap conf (no personal cap), ceiling
Usage: sim_v2d.py <mode> <in.tsv> [d1prior_mil]
Prints 6-col driver output (id,fam,depth,rel,corr,conf_thousandths).
Validated: each mode must reproduce its Zag binary output byte-for-byte
(pool: validated against nec_v2d-11 on all no-bind cells + code identity
 of the ledger path with m15/m11 modes).
"""
import sys

def run(in_tsv, mode, d1prior=950000):
    p0num = {"m15": 2000000, "m11": 1900000, "pool": 1900000, "m20": None}[mode]
    led = {}   # (mb,cb) -> [c,t]
    pers = {}  # id -> [cp,tp]
    prev = {}  # id -> conf_mil
    out = []
    diag = []  # per released cell: (iid,depth,class_rate_mil,cp,tp,p_raw_mil,conf_mil)
    for line in open(in_tsv):
        line = line.rstrip("\n")
        if not line: continue
        iid,fam,depth,f1,f5,rel,corr = line.split("\t")
        depth,f1,f5,rel,corr = int(depth),int(f1),int(f5),int(rel),int(corr)
        conf = 0
        if rel == 1:
            cls = (min(f1//150,6), min(f5//250,4))
            c,t = led.get(cls,[0,0])
            cp,tp = pers.get(iid,[0,0])
            p_raw = (cp*1000000)//tp if tp>=1 else None
            if mode == "m20":
                cm = p_raw if p_raw is not None else d1prior
            else:
                class_rate = (c*1000000 + p0num)//(t+2)
                cm = class_rate
                if mode in ("m15","m11") and p_raw is not None and cm > p_raw:
                    cm = p_raw
            pc = prev.get(iid)
            if pc is not None and cm > pc: cm = pc
            prev[iid] = cm
            conf = cm//1000
            class_rate = (c*1000000 + 1900000)//(t+2) if mode=="m20" else ((c*1000000 + p0num)//(t+2))
            diag.append((iid,depth,class_rate,cp,tp,p_raw if p_raw is not None else -1,cm))
            # updates AFTER conf
            if mode != "m20":
                t += 1
                if corr==1: c += 1
                led[cls] = [c,t]
            tp += 1
            if corr==1: cp += 1
            pers[iid] = [cp,tp]
        out.append(f"{iid}\t{fam}\t{depth}\t{rel}\t{corr}\t{conf}")
    return out, diag

if __name__ == "__main__":
    mode = sys.argv[1]
    d1p = int(sys.argv[3]) if len(sys.argv) > 3 else 950000
    out, _ = run(sys.argv[2], mode, d1p)
    sys.stdout.write("\n".join(out)+"\n")
