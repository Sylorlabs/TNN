#!/usr/bin/env python3
"""Byte-exact Python sim of m11's STATED rule (ADDENDUM_V2_m11.md).
Used for T1-M2 exact-rule checks and T2 per-cell diagnostics.
Validated: must reproduce the Zag binary's output byte-for-byte."""
import sys

def run(in_tsv):
    led = {}   # (mb,cb) -> [c,t]
    pers = {}  # id -> [cp,tp]
    prev = {}  # id -> conf_mil
    out = []
    diag = []  # per released cell: (id,depth,class_rate_mil,cp,tp,p_raw_mil,conf_mil)
    for line in open(in_tsv):
        line = line.rstrip("\n")
        if not line: continue
        iid,fam,depth,f1,f5,rel,corr = line.split("\t")
        depth,f1,f5,rel,corr = int(depth),int(f1),int(f5),int(rel),int(corr)
        conf = 0
        if rel == 1:
            cls = (min(f1//150,6), min(f5//250,4))
            c,t = led.get(cls,[0,0])
            class_rate = (c*1000000 + 1900000)//(t+2)
            cp,tp = pers.get(iid,[0,0])
            p_raw = (cp*1000000)//tp if tp>=1 else None
            cm = class_rate
            if p_raw is not None and cm > p_raw: cm = p_raw
            pc = prev.get(iid)
            if pc is not None and cm > pc: cm = pc
            prev[iid] = cm
            conf = cm//1000
            diag.append((iid,depth,class_rate,cp,tp,p_raw if p_raw is not None else -1,cm))
            # updates AFTER conf
            t += 1
            if corr==1: c += 1
            led[cls] = [c,t]
            tp += 1
            if corr==1: cp += 1
            pers[iid] = [cp,tp]
        out.append(f"{iid}\t{fam}\t{depth}\t{rel}\t{corr}\t{conf}")
    return out, diag

if __name__ == "__main__":
    out, _ = run(sys.argv[1])
    sys.stdout.write("\n".join(out)+"\n")
