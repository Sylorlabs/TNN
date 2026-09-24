#!/usr/bin/env python3
"""Derive the F5 tightened windows mechanically from the frozen exemplar bank.

Deterministic, zero RNG. Inputs (read-only, SHA-checked by caller):
  exemplars.tsv          frozen bank (6 rows), prereg §3a-anchored
  fixtures_ledger.txt    the frozen 300-percept battery fixtures (round2/f5_redteam300)
  ledger_d_withhold.txt  backtest evidence ledger (v2/redteam/evidence) for retention metric

DERIVATION RULE (frozen in PREREG_F5_TIGHTENED.md §3):
  On each axis, the per-exemplar window radius = ceil(cluster span / 2),
  where the cluster span = max - min over the 6 bank exemplars.
  Rationale: a candidate within one cluster-radius of an exemplar is "within
  the cluster's own scale"; the union of the six per-exemplar windows covers
  exactly the cluster bounding box plus one cluster-radius of margin.
"""
import math, hashlib, sys

EX = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_redteam300/exemplars.tsv"
FIX = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_redteam300/fixtures_ledger.txt"
BT = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2/redteam/evidence/ledger_d_withhold.txt"

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

print("exemplars.tsv SHA:", sha(EX))
print("fixtures_ledger.txt SHA:", sha(FIX))
print("ledger_d_withhold.txt SHA:", sha(BT))

ex = []
with open(EX) as f:
    lines = f.read().splitlines()
for ln in lines[1:]:
    if not ln.strip():
        continue
    parts = ln.split("\t")
    ex.append((int(parts[0]), parts[1], int(parts[2]), int(parts[3])))
confs = [e[2] for e in ex]
meass = [e[3] for e in ex]
cspan = max(confs) - min(confs)
mspan = max(meass) - min(meass)
wc = math.ceil(cspan / 2)
wm = math.ceil(mspan / 2)
print(f"bank: conf {min(confs)}..{max(confs)} span {cspan}; "
      f"measure {min(meass)}..{max(meass)} span {mspan}")
print(f"DERIVED WINDOWS: |dconf| <= {wc}, |dmeas| <= {wm}")

def stem(fixture):
    s = fixture
    if s.startswith("rt4_"):
        s = s[4:]
    return s.split("-")[0]

def blocked(stm, conf, meas):
    for (_, fam, ec, em) in ex:
        es = stem(fam)
        if es == stm and abs(conf - ec) <= wc and abs(meas - em) <= wm:
            return True
    return False

# --- 300 NEAR grid (§3a of the red-team prereg): conf=650+10i, meas=2200+500j
b_near = 0
for i in range(30):
    c = 650 + 10 * i
    for j in range(10):
        m = 2200 + 500 * j
        if blocked("TMB", c, m):
            b_near += 1
# delayed>50 under primary model: delay_k = 3k > 50 -> k>=17
d_gt50 = max(0, b_near - 16)
print(f"NEAR grid: blocked {b_near}/300; primary delayed>50 {d_gt50}/300 "
      f"({100.0*d_gt50/300:.1f}%)")

# --- 60 FAR controls (§3b)
b_far = 0
for k in range(20):
    if blocked("COL", 800 + 5 * k, 50000 + 500 * k):
        b_far += 1
    if blocked("TMB", 950 + 2 * k, 5500 + 50 * k):
        b_far += 1
    if blocked("PTC", 780 + 8 * k, 1000 + 2500 * k):
        b_far += 1
print(f"FAR controls: blocked {b_far}/60")

# --- backtest retention: 8 TMB-5 false accepts (RICH/DARK) + 1 COL-4
n_false = 0
b_false = 0
n_true = 0
b_true = 0
kept_false = []
with open(BT) as f:
    for ln in f.read().splitlines():
        if not ln.strip():
            continue
        p = ln.split("|")
        if len(p) < 16 or not p[15].startswith("DISP=ACCEPT_INSTALL"):
            continue
        fixture, judg, conf, meas, truth = p[4], p[7], int(p[8]), int(p[10]), p[12]
        if blocked(stem(fixture), conf, meas):
            if judg != truth:
                n_false += 1
                b_false += 1
                kept_false.append(fixture)
            else:
                n_true += 1
                b_true += 1
        else:
            if judg != truth:
                n_false += 1
            else:
                n_true += 1
print(f"BACKTEST retention: false blocked {b_false}/{n_false}; "
      f"true blocked {b_true}/{n_true}")
print("kept false accepts:", kept_false)
