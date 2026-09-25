#!/usr/bin/env python3
"""Byte-exact Python sims of nec_v2d.zag variant rules, extended for v3b JOB2.
Adds modes m24 (m20 + K-A oracle schema) and m25 (m20 + K-B learned schema):
  personal-only, p_raw if tp>=1 else schema[cls] (millionths), ceiling min-latch.
Schemas loaded from the frozen committed TSVs (src/schema_ka.tsv / schema_kb.tsv).
Original modes (m15/m20/m11/pool) verbatim from v2d/sim_v2d.py.
Validation: each new mode must reproduce its Zag binary output byte-for-byte
on necc_input.tsv, trap_t1.tsv, trap_t3.tsv.
Usage: sim_v2d_v3b.py <mode> <in.tsv> [schema_tsv]
Prints 6-col driver output (id,fam,depth,rel,corr,conf_thousandths).
"""
import sys

SCHEMA_FILES = {"m24": "schema_ka.tsv", "m25": "schema_kb.tsv"}

def load_schema(mode, path=None):
    fn = path or ("../src/" + SCHEMA_FILES[mode])
    s = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        s[int(c[0])] = int(c[1])
    return s

def run(in_tsv, mode, d1prior=950000, schema=None):
    p0num = {"m15": 2000000, "m11": 1900000, "pool": 1900000,
             "m20": None, "m24": None, "m25": None}[mode]
    if mode in ("m24", "m25") and schema is None:
        schema = load_schema(mode)
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
            mb, cb = min(f1//150,6), min(f5//250,4)
            cls = (mb, cb)
            c,t = led.get(cls,[0,0])
            cp,tp = pers.get(iid,[0,0])
            p_raw = (cp*1000000)//tp if tp>=1 else None
            if mode == "m20":
                cm = p_raw if p_raw is not None else d1prior
            elif mode in ("m24", "m25"):
                cm = p_raw if p_raw is not None else schema[mb*5+cb]
            else:
                class_rate = (c*1000000 + p0num)//(t+2)
                cm = class_rate
                if mode in ("m15","m11") and p_raw is not None and cm > p_raw:
                    cm = p_raw
            pc = prev.get(iid)
            if pc is not None and cm > pc: cm = pc
            prev[iid] = cm
            conf = cm//1000
            class_rate = (c*1000000 + 1900000)//(t+2) if mode in ("m20","m24","m25") \
                else ((c*1000000 + p0num)//(t+2))
            diag.append((iid,depth,class_rate,cp,tp,p_raw if p_raw is not None else -1,cm))
            # updates AFTER conf
            if mode not in ("m20","m24","m25"):
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
    sch = sys.argv[3] if len(sys.argv) > 3 and mode in ("m24","m25") else None
    schema = load_schema(mode, sch) if mode in ("m24","m25") else None
    out, _ = run(sys.argv[2], mode, schema=schema)
    sys.stdout.write("\n".join(out)+"\n")
