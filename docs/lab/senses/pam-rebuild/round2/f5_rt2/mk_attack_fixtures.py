#!/usr/bin/env python3
"""RT-1 attack fixture generator (H-PAM-15/16/20 vs the F5 full mechanism).

Deterministic: every coordinate is fixed arithmetic, zero RNG. Each fixture
line is the 17-field backtest-style format (no SET= field -> the binary's
BACKTEST set, no CORRUPT abort). Field 4 carries the fixture name whose stem
parses to TMB; field 7 judgment; field 8 conf; field 10 measure; field 12
truth; field 15 DISP=ACCEPT_INSTALL.

Falses: judg=RICH, truth=DARK (the backtest's false-accept convention).
Trues/controls: judg=RICH, truth=RICH.

Also writes expected (blocked, rep, decision) per fixture, computed from the
frozen constants (predicate 150/2000, core 130/950, jitter 10/200, quorum
rep>=2) against the frozen exemplar bank — the scorer asserts the binary's
decision matches on every fixture.
"""
import json

EX = [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632), (713, 2627)]

def blocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EX)

def rep(c, m):
    n = 0
    for dc, dm in [(-10, -200), (0, 0), (10, 200)]:
        if any(abs(c + dc - ec) <= 130 and abs(m + dm - em) <= 950 for ec, em in EX):
            n += 1
    return n

def decision(c, m):
    if not blocked(c, m):
        return "ALLOWED"
    return "WITHHOLD" if rep(c, m) >= 2 else "CONFIRM_INSTALL"

def line(tag, seq, c, m, false):
    j = "RICH"
    t = "DARK" if false else "RICH"
    fx = "rt4_TMB-5_%s_%04d.r24" % (tag, seq)
    f = ["0" * 64, "0" * 64, "0", "3", fx, "2", "1", j, str(c), "0", str(m),
         "0" * 64, t, "1", str(c), "DISP=ACCEPT_INSTALL", "DETAIL=rt2_" + tag]
    return "|".join(f), {"fx": fx, "tag": tag, "conf": c, "meas": m,
                         "false": false, "blocked": blocked(c, m),
                         "rep": rep(c, m), "exp": decision(c, m)}

out_lines = []
expect = {}

def add(tag, seq, c, m, false):
    l, e = line(tag, seq, c, m, false)
    out_lines.append(l)
    expect[e["fx"]] = e

# ---- A15A: interior falses, exactly as H-PAM-15 specifies (30) ----
seq = 0
confs = list(range(702, 718))
for mi, m in enumerate([2620, 2645]):
    for ci, c in enumerate(confs):
        if seq >= 30:
            break
        add("A15A", seq, c, m, True)
        seq += 1

# ---- A15B: predicate-marginal annulus falses, crop-coherent (30) ----
seq = 0
for c in range(859, 869):
    add("A15B", seq, c, 2632, True); seq += 1          # conf-high annulus
for c in range(551, 561):
    add("A15B", seq, c, 2632, True); seq += 1          # conf-low annulus
for m in range(3798, 3803):
    add("A15B", seq, 710, m, True); seq += 1           # meas-high annulus
for m in range(1458, 1463):
    add("A15B", seq, 710, m, True); seq += 1           # meas-low annulus
assert seq == 30, seq

# ---- A16: rep=1 transient falses (60) ----
seq = 0
for m in [2620, 2645]:
    for c in range(849, 859):
        add("A16F", seq, c, m, True); seq += 1         # conf-high edge
for m in [2620, 2645]:
    for c in range(561, 571):
        add("A16F", seq, c, m, True); seq += 1         # conf-low edge
for m in range(3602, 3612):
    add("A16F", seq, 710, m, True); seq += 1           # meas-high edge
for m in range(1653, 1663):
    add("A16F", seq, 710, m, True); seq += 1           # meas-low edge
assert seq == 60, seq

# ---- A16T: true-transient controls (30) ----
seq = 0
for c in range(849, 859):
    add("A16T", seq, c, 2632, False); seq += 1
for c in range(561, 571):
    add("A16T", seq, c, 2632, False); seq += 1
for m in list(range(3602, 3607)) + list(range(1653, 1658)):
    add("A16T", seq, 710, m, False); seq += 1
assert seq == 30, seq

# ---- A20F: K=40 planted falses interleaved with the 7 trues ----
seq = 0
for i in range(40):
    c = 770 + (i * 37) % 61
    m = 2185 + (i * 53) % 31
    add("A20F", seq, c, m, True); seq += 1

# ---- A20T: the 7 frozen in-rectangle trues ----
seq = 0
for c in [770, 780, 790, 800, 810, 820, 830]:
    add("A20T", seq, c, 2200, False); seq += 1

# ---- write ledgers ----
def write(tag_prefixes, path):
    ls = [l for l in out_lines
          for fx in [l.split("|")[4]]
          if any("_%s_" % t in fx for t in tag_prefixes)]
    open(path, "w").write("\n".join(ls) + "\n")
    return len(ls)

import os
D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt2"
n15 = write(["A15A", "A15B"], D + "/ledger_a15.txt")
n16 = write(["A16F", "A16T"], D + "/ledger_a16.txt")
n20 = write(["A20F", "A20T"], D + "/ledger_a20.txt")
json.dump(expect, open(D + "/expect.json", "w"), indent=1, sort_keys=True)
print("ledgers: a15=%d a16=%d a20=%d" % (n15, n16, n20))

# sanity: every fixture's expectation per frozen geometry
from collections import Counter
print(Counter((e["tag"], e["exp"]) for e in expect.values()))
bad = [fx for fx, e in expect.items()
       if (e["tag"] == "A15A" and e["exp"] != "WITHHOLD")
       or (e["tag"] == "A15B" and e["exp"] != "CONFIRM_INSTALL")
       or (e["tag"] == "A16F" and e["exp"] != "CONFIRM_INSTALL")
       or (e["tag"] == "A16T" and e["exp"] != "CONFIRM_INSTALL")
       or (e["tag"] in ("A20F", "A20T") and e["exp"] != "WITHHOLD")]
print("fixtures violating attack geometry:", bad if bad else "NONE")
# indistinguishability premise for A20: falses overlap trues in (conf,meas)
tf = [(e["conf"], e["meas"]) for e in expect.values() if e["tag"] == "A20F"]
tt = [(e["conf"], e["meas"]) for e in expect.values() if e["tag"] == "A20T"]
fc = [c for c, m in tf]; fm = [m for c, m in tf]
tc = [c for c, m in tt]; tm = [m for c, m in tt]
print("A20F conf range %d..%d meas range %d..%d" % (min(fc), max(fc), min(fm), max(fm)))
print("A20T conf range %d..%d meas range %d..%d" % (min(tc), max(tc), min(tm), max(tm)))
dmax = max(min(abs(c - c2) + abs(m - m2) for c2, m2 in tt) for c, m in tf)
print("A20F max L1 distance to nearest true: %d" % dmax)
