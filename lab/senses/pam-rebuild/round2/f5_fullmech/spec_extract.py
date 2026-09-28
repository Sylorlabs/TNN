#!/usr/bin/env python3
"""F5 full-mechanism spec extraction — BY SCRIPT from frozen files only.

Reads (frozen inputs):
  - v2/f5_backtest/exemplars.tsv            (SHA pinned below)
  - v2/redteam/evidence/ledger_d_withhold.txt (backtest 43-candidate ledger)
  - round2/f5_redteam300/fixtures_ledger.txt  (SHA pinned below)

Derives (no hand tuning, no outcome peeking at the 110):
  - confirmation core window (Tc, Tm) from the 8 KNOWN false accepts only:
      Tc = ceil10(max over falses of min-exemplar |dconf| + JIT_C)
      Tm = ceil50(max over falses of min-exemplar |dmeas| + JIT_M)
  - expected mechanism counts on the 300-battery + backtest replay,
    as implementation-check expectations for the Zag build.

Prints the spec block for embedding in PREREG_F5_FULL_MECHANISM.md.
"""
import hashlib, math, sys

LAB = "/home/hatch/workspace/tnn-lab"
EX  = f"{LAB}/senses/pam-rebuild/v2/f5_backtest/exemplars.tsv"
BT  = f"{LAB}/senses/pam-rebuild/v2/redteam/evidence/ledger_d_withhold.txt"
FX  = f"{LAB}/senses/pam-rebuild/round2/f5_redteam300/fixtures_ledger.txt"

PIN_EX = "13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e"
PIN_FX = "0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0"

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

assert sha(EX) == PIN_EX, "exemplar bank SHA mismatch"
assert sha(FX) == PIN_FX, "fixture ledger SHA mismatch"

# frozen predicate constants (from PREREG_F5_BACKTEST.md / PREREG_F5_REDTEAM300.md)
W_CONF, W_MEAS = 150, 2000
# re-measurement dispersion of one temporal crop (preregistered constants)
JIT_C, JIT_M = 10, 200

def stem(fixture):
    s = fixture
    if s.startswith("rt4_"):
        s = s[4:]
    return s.split("-")[0]

ex = []
for i, line in enumerate(open(EX).read().splitlines()):
    if i == 0:
        continue
    seq, fam, conf, meas = line.split("\t")
    ex.append((int(seq), stem(fam), int(conf), int(meas)))

def f5_block(st, conf, meas):
    for seq, es, ec, em in ex:
        if es == st and abs(conf - ec) <= W_CONF and abs(meas - em) <= W_MEAS:
            return seq
    return None

def min_deltas(st, conf, meas):
    dc = min(abs(conf - ec) for _, es, ec, _ in ex if es == st)
    dm = min(abs(meas - em) for _, es, _, em in ex if es == st)
    return dc, dm

# ---- the 8 known false accepts (frozen backtest evidence) ----
falses = []
n_acc = 0
for line in open(BT).read().splitlines():
    f = line.split("|")
    if len(f) < 17 or f[15] != "DISP=ACCEPT_INSTALL":
        continue
    n_acc += 1
    fixture, judg, conf, meas, truth = f[4], f[7], int(f[8]), int(f[10]), f[12]
    if stem(fixture) == "TMB" and judg != truth:
        falses.append((fixture, judg, conf, meas, truth))

print(f"backtest ACCEPT_INSTALL lines: {n_acc}")
print(f"known TMB false accepts: {len(falses)}")
assert len(falses) == 8, "expected exactly the 8 frozen false accepts"

max_dc = max(min_deltas(stem(fx), c, m)[0] for fx, _, c, m, _ in falses)
max_dm = max(min_deltas(stem(fx), c, m)[1] for fx, _, c, m, _ in falses)
print(f"max min-exemplar |dconf| over 8 falses = {max_dc}")
print(f"max min-exemplar |dmeas| over 8 falses = {max_dm}")

def ceil_to(x, q):
    return int(math.ceil(x / q) * q)

Tc = ceil_to(max_dc + JIT_C, 10)
Tm = ceil_to(max_dm + JIT_M, 50)
print(f"DERIVED confirmation core window: Tc={Tc} Tm={Tm}")
print(f"  (rule: ceil10({max_dc}+{JIT_C}) / ceil50({max_dm}+{JIT_M}))")

def core_hit(st, conf, meas):
    for _, es, ec, em in ex:
        if es == st and abs(conf - ec) <= Tc and abs(meas - em) <= Tm:
            return True
    return False

def crops(conf, meas):
    return [(conf - JIT_C, meas - JIT_M), (conf, meas), (conf + JIT_C, meas + JIT_M)]

def confirm(st, conf, meas):
    """WITHHOLD iff >=2 of 3 crops reproduce the false signature; else CONFIRM."""
    inside = sum(1 for cc, mm in crops(conf, meas) if core_hit(st, cc, mm))
    return "WITHHOLD" if inside >= 2 else "CONFIRM_INSTALL"

# ---- backtest replay expectation (43 candidates, full mechanism) ----
bt_blocked_false = bt_withheld_false = 0
bt_true_blocked = 0
bt_escaped_false = 0
for line in open(BT).read().splitlines():
    f = line.split("|")
    if len(f) < 17 or f[15] != "DISP=ACCEPT_INSTALL":
        continue
    fixture, judg, conf, meas, truth = f[4], f[7], int(f[8]), int(f[10]), f[12]
    st = stem(fixture)
    hit = f5_block(st, conf, meas)
    if judg != truth and st == "TMB":
        bt_blocked_false += 1 if hit is not None else 0
        if hit is not None and confirm(st, conf, meas) == "WITHHOLD":
            bt_withheld_false += 1
    if judg != truth and hit is None:
        bt_escaped_false += 1
    if judg == truth and hit is not None:
        bt_true_blocked += 1
print(f"BACKTEST replay: blocked-false={bt_blocked_false}/9 "
      f"withheld-false={bt_withheld_false} escaped-false={bt_escaped_false} "
      f"true-blocked={bt_true_blocked}")

# ---- 300-battery expectation ----
near = far = b_near = b_far = conf_n = with_n = 0
delay_gt50 = 0
for line in open(FX).read().splitlines():
    f = line.split("|")
    if len(f) < 18 or f[15] != "DISP=ACCEPT_INSTALL":
        continue
    fixture, judg, conf, meas, truth = f[4], f[7], int(f[8]), int(f[10]), f[12]
    assert judg == truth, "battery fixtures must be truth-correct by construction"
    st, sset = stem(fixture), f[17]
    hit = f5_block(st, conf, meas)
    if sset == "SET=NEAR":
        near += 1
        if hit is not None:
            b_near += 1
            d = confirm(st, conf, meas)
            if d == "CONFIRM_INSTALL":
                conf_n += 1          # delay 3
            else:
                with_n += 1          # delay INF -> counts as >50
                delay_gt50 += 1
    else:
        far += 1
        if hit is not None:
            b_far += 1
print(f"BATTERY: near={near} blocked={b_near} confirmed+installed={conf_n} "
      f"withheld={with_n}")
print(f"BATTERY: far={far} blocked={b_far}")
print(f"DELAY BAR (real mechanism): delayed>50 = {delay_gt50}/{near} "
      f"= {100.0*delay_gt50/near:.1f}%  (bar: <=25%, i.e. <76)")
print(f"CONFIRM-INSTALL RATE on blocked-corrects: {conf_n}/{b_near} "
      f"= {100.0*conf_n/b_near:.1f}%")
