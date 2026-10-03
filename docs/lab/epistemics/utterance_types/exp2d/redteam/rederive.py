#!/usr/bin/env python3
"""Independent red-team re-derivation of exp2d scores from runs/*.txt.
Pure deterministic parsing; no randomness.
Reads 2C_CURVE and X2C_CURVE lines, builds per-leg tables, and compares
against PREDICTIONS_LOCKED.md and bartable.md claims.
"""
import os, re, sys, hashlib

RUNS = os.path.expanduser("~/workspace/exp2d_redteam/wt/docs/lab/epistemics/utterance_types/exp2d/runs")

def parse_2c(line):
    # 2C_CURVE|type|TR|a|PA|b|NO|c|DP|d|LK|e
    p = line.strip().split("|")
    d = {}
    it = iter(p[1:])
    d["type"] = int(next(it))
    for k in it:
        v = next(it)
        d[k] = int(v)
    return d

def parse_x2c(line):
    # X2C_CURVE|3|WI|score|N|10
    p = line.strip().split("|")
    return {"type": int(p[1]), "kind": p[2], "score": int(p[3]), "n": int(p[5])}

legs = {}
sha_ok = True
manifest = {}
for ln in open(os.path.join(RUNS, "SHA_MANIFEST.txt")):
    h, fn = ln.split()
    manifest[fn] = h

for fn in sorted(os.listdir(RUNS)):
    if fn == "SHA_MANIFEST.txt" or not fn.endswith(".txt"):
        continue
    path = os.path.join(RUNS, fn)
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if manifest.get(fn) != h:
        print(f"SHA MISMATCH: {fn} manifest={manifest.get(fn)} actual={h}")
        sha_ok = False
    m = re.match(r"(.+)_rep(\d)\.txt", fn)
    leg, rep = m.group(1), int(m.group(2))
    curves2c, curvesx = {}, {}
    for ln in open(path):
        if ln.startswith("2C_CURVE"):
            d = parse_2c(ln)
            curves2c[d["type"]] = (d["DP"], d["LK"])
        elif ln.startswith("X2C_CURVE"):
            d = parse_x2c(ln)
            curvesx[d["kind"]] = (d["score"], d["n"])
    legs.setdefault(leg, {})[rep] = (curves2c, curvesx)

print("SHA manifest check:", "ALL OK" if sha_ok else "FAILURES ABOVE")
print()

# determinism: all 3 reps identical per leg
print("=== determinism (rep1 vs rep2 vs rep3 per leg) ===")
for leg in sorted(legs):
    reps = legs[leg]
    same = reps[1] == reps[2] == reps[3]
    print(f"{leg:8s} reps_identical={same}")
print()

# per-leg score table from rep1
print("=== 2C DP/LK per leg (from runs) ===")
hdr = f"{'leg':8s} " + " ".join(f"T{i} DP/LK" for i in range(1, 6))
print(hdr)
pred_2c = {
    "base":   {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
    "ab2-a":  {1:(9,9),  2:(10,10), 3:(9,9),  4:(10,10), 5:(9,9)},
    "ab2-b":  {1:(9,9),  2:(10,10), 3:(9,9),  4:(10,10), 5:(9,9)},
    "abc2-b": {1:(9,9),  2:(10,10), 3:(9,10), 4:(10,10), 5:(9,9)},
    "abc2-a": {1:(4,9),  2:(5,0),   3:(5,0),  4:(5,0),   5:(5,0)},
    "v96-a":  {1:(10,9), 2:(10,10), 3:(8,10), 4:(9,10),  5:(8,9)},
    "v96-b":  {1:(10,9), 2:(10,10), 3:(8,10), 4:(9,10),  5:(8,9)},
    "de2-a":  {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
    "de2-b":  {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
}
bar_2c = {
    "base":   {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
    "ab2-a":  {1:(9,9),  2:(10,10), 3:(9,9),  4:(10,10), 5:(9,9)},
    "ab2-b":  {1:(9,9),  2:(10,10), 3:(9,9),  4:(10,10), 5:(9,9)},
    "abc2-b": {1:(9,9),  2:(10,10), 3:(9,10), 4:(10,10), 5:(9,9)},
    "abc2-a": {1:(4,9),  2:(5,0),   3:(5,0),  4:(5,0),   5:(5,0)},
    "v96-a":  {1:(10,9), 2:(10,10), 3:(8,10), 4:(9,10),  5:(8,9)},
    "v96-b":  {1:(10,9), 2:(10,10), 3:(8,10), 4:(9,10),  5:(8,9)},
    "de2-a":  {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
    "de2-b":  {1:(9,9),  2:(10,10), 3:(9,3),  4:(10,10), 5:(10,9)},
}
mism_pred, mism_bar = [], []
for leg in sorted(legs):
    if leg == "empty":
        continue
    c2c, _ = legs[leg][1]
    row = f"{leg:8s} " + " ".join(f"{c2c[i][0]}/{c2c[i][1]:>5}" if False else f"T{i}:{c2c[i][0]}/{c2c[i][1]}" for i in range(1,6))
    print(row)
    for i in range(1, 6):
        if c2c[i] != pred_2c[leg][i]:
            mism_pred.append((leg, f"T{i}", "2C", pred_2c[leg][i], c2c[i]))
        if c2c[i] != bar_2c[leg][i]:
            mism_bar.append((leg, f"T{i}", "2C", bar_2c[leg][i], c2c[i]))
print()
print("=== X2C WI/WD per leg (from runs) ===")
pred_x = {
    "base":   ("WI",0,"WD",0),  "ab2-a":  ("WI",0,"WD",10), "ab2-b": ("WI",0,"WD",10),
    "abc2-a": ("WI",0,"WD",10), "abc2-b": ("WI",0,"WD",10), "v96-a": ("WI",0,"WD",10),
    "v96-b":  ("WI",0,"WD",10), "de2-a":  ("WI",10,"WD",10),"de2-b": ("WI",10,"WD",10),
}
bar_x = {
    "base":   ("WI",0,"WD",0),  "ab2-a":  ("WI",0,"WD",10), "ab2-b": ("WI",0,"WD",10),
    "abc2-a": ("WI",0,"WD",0),  "abc2-b": ("WI",0,"WD",10), "v96-a": ("WI",0,"WD",10),
    "v96-b":  ("WI",0,"WD",10), "de2-a":  ("WI",10,"WD",10),"de2-b": ("WI",10,"WD",10),
}
for leg in sorted(legs):
    if leg == "empty":
        continue
    _, cx = legs[leg][1]
    wi = cx.get("WI", ("?","?")); wd = cx.get("WD", ("?","?"))
    print(f"{leg:8s} WI={wi[0]}/{wi[1]} WD={wd[0]}/{wd[1]}")
    for kind in ("WI","WD"):
        act = cx[kind][0]
        p = pred_x[leg][pred_x[leg].index(kind)+1]
        b = bar_x[leg][bar_x[leg].index(kind)+1]
        if act != p:
            mism_pred.append((leg, kind, "X2C", p, act))
        if act != b:
            mism_bar.append((leg, kind, "X2C", b, act))
print()
print("=== mismatches vs PREDICTIONS_LOCKED.md ===")
for m in mism_pred: print("  PRED-MISMATCH", m)
if not mism_pred: print("  none")
print("=== mismatches vs bartable.md ===")
for m in mism_bar: print("  BAR-MISMATCH", m)
if not mism_bar: print("  none")
