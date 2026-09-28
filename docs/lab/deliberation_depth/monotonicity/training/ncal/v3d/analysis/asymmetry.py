#!/usr/bin/env python3
"""Asymmetry analysis for the v3d head-to-head.
Per battery, per (id,depth) row: err = conf/1e6 - correct(0/1).
CATCH: |err| <= 0.100. MISS: |err| > 0.100.
Reports per battery: n, v20 caught/missed/mean|err|, v26 caught/missed/mean|err|,
both-catch, both-miss, only-v20, only-v26 (+ the exact (id,depth) rows where
exactly one catches, capped at 12 shown, full counts kept).
Usage: asymmetry.py <workdir>  (expects <tag>_A.tsv pairs + battery inputs;
reads batteries.list: "<tag20> <tag26> <inputpath>")
"""
import sys
W = sys.argv[1]
CATCH = 0.100

def load_out(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        # output col5 = conf_thousandths (frozen source: "Output stays 6 cols
        # (id, fam, depth, release, correct, conf_thousandths)")
        d[(c[0], c[2])] = int(c[5]) / 1e3
    return d

def load_in(fn):
    d = {}
    for line in open(fn):
        c = line.rstrip("\n").split("\t")
        d[(c[0], c[2])] = int(c[6])
    return d

print("battery | n | v20 catch/miss/mean|err| | v26 catch/miss/mean|err| | "
      "bothC | bothM | only20 | only26")
for line in open(f"{W}/batteries.list"):
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    tag20, tag26, inp = line.split(None, 2)
    tin = load_in(inp)
    o20, o26 = load_out(f"{W}/{tag20}_A.tsv"), load_out(f"{W}/{tag26}_A.tsv")
    keys = [k for k in tin if k in o20 and k in o26]
    c20 = c26 = bC = bM = o20n = o26n = 0
    ae20 = ae26 = 0.0
    only20, only26 = [], []
    for k in keys:
        t = tin[k]
        e20 = abs(o20[k] - t); e26 = abs(o26[k] - t)
        ae20 += e20; ae26 += e26
        h20, h26 = e20 <= CATCH, e26 <= CATCH
        c20 += h20; c26 += h26
        if h20 and h26: bC += 1
        elif not h20 and not h26: bM += 1
        elif h20: o20n += 1; only20.append(k)
        else: o26n += 1; only26.append(k)
    n = len(keys)
    print(f"{tag20} | {n} | {c20}/{n-c20}/{ae20/n:.4f} | {c26}/{n-c26}/{ae26/n:.4f} | "
          f"{bC} | {bM} | {o20n} | {o26n}")
    if only20:
        print(f"  only-v20-catches ({o20n}): " +
              ", ".join(f"{i}@d{d}" for i, d in only20[:12]) +
              (" ..." if o20n > 12 else ""))
    if only26:
        print(f"  only-v26-catches ({o26n}): " +
              ", ".join(f"{i}@d{d}" for i, d in only26[:12]) +
              (" ..." if o26n > 12 else ""))
