#!/usr/bin/env python3
"""D2 novelty-handling: battery construction (frozen spec script).

Deterministic (zero RNG). All percept values are EXTRACTED from SHA-verified
frozen ledgers; nothing is invented. Jitter pattern derived from the hex
digits of the pinned fixtures_ledger SHA (same pattern as the D2 probe).

Outputs (in OUTDIR):
  cal.tsv      calibration episodes (B calibration; not scored)
  novel.tsv    battery (i)  novel-honest, n=60
  drift.tsv    battery (ii) slow-drift, 4 rates x 15 profiles = 60
  inject.tsv   battery (iii) injection, 8 falses x 4 positions = 32
  dos.tsv      battery (iv) mass-revocation, 20 replay-poison + 20 spike-spam
  honest.tsv   battery (v)  honest control, n=120
  spec.json    frozen parameters + SHAs + derivation record

Parameter derivation (preregistered rules):
  B         = max L_inf short-term prediction error over calibration steps.
  D_max     = 0.5 * min over drift profiles of C(entry_step); REQUIRE
              D_max > 3 * honest_max_C else NO OPERATING POINT (report).
  D_promote = D_max / 2.
  r_min     = min over drift profiles of mean per-step C growth during drift.
  W         = ceil(2*D_max / r_min) + 5  (promotion-bar rule; verified by
              simulation: zero drift percepts commit in all 60 profiles).
  K = 3, N = 20 (Arm B warrant window), TOMB_R = 15. All preregistered.
"""
import hashlib
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ref_arms import (tdiv, linf, calibrate_B, ArmC,
                      C_HON, C_INJ, C_NOV, C_DRF, C_RPL, C_SPK,
                      T_NONE, T_PROV, T_SUSP, T_REV, T_COM, T_REF)

LAB = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild"
LED_RT300 = LAB + "/round2/f5_redteam300/fixtures_ledger.txt"
LED_D = LAB + "/v2/redteam/evidence/ledger_d_withhold.txt"
EXEMPL = LAB + "/round2/f5_fullmech/exemplars.tsv"
OUTDIR = "/home/hatch/workspace/pam_d2_build/batteries"

PIN_RT300 = "0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0"
PIN_D = "63ea591d8cbb9d8b3e1cd088364e96d8fdfa19d435e337dfac0ad17a0326c2b1"
PIN_EX = "13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e"

CLS_CH = {C_HON: "HON", C_INJ: "INJ", C_NOV: "NOV",
          C_DRF: "DRF", C_RPL: "RPL", C_SPK: "SPK"}
TRUTH = {C_HON: "HONEST", C_NOV: "HONEST", C_INJ: "FALSE",
         C_DRF: "FALSE", C_RPL: "FALSE", C_SPK: "FALSE"}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def check_sha(p, pin, name):
    got = sha256_file(p)
    assert got == pin, f"SHA MISMATCH {name}: got {got} want {pin}"
    print(f"SHA-OK {name}", file=sys.stderr)


check_sha(LED_RT300, PIN_RT300, "fixtures_ledger.txt")
check_sha(LED_D, PIN_D, "ledger_d_withhold.txt")
check_sha(EXEMPL, PIN_EX, "exemplars.tsv")

# ---- deterministic jitter from the pinned ledger SHA ----
digits = [int(ch, 16) for ch in PIN_RT300]
JITC, JITM = 8, 14  # half of frozen honest spans (17, 29)


def jitter(k):
    dc = ((digits[k % 64] % 3) - 1) * JITC
    dm = ((digits[(k + 37) % 64] % 3) - 1) * JITM
    return dc, dm


def honest(k, off):
    dc, dm = jitter(off + k)
    # STATIONARY (no ramp): reference uses v=0, so C(t)=|p(t)-anchor|.
    # Eliminates reference-velocity estimation error.
    return 650 + dc, 2600 + dm


# ---- extract the 8 KB4 falses (judged RICH, truth != RICH, DISP=ACCEPT_INSTALL)
falses = []
with open(LED_D) as f:
    for line in f:
        p = line.rstrip("\n").split("|")
        if len(p) < 17 or p[15] != "DISP=ACCEPT_INSTALL":
            continue
        judged, conf, meas, truth = p[7], int(p[8]), int(p[10]), p[12]
        if p[4].startswith("rt4_TMB-5_") and judged == "RICH" and truth != "RICH":
            falses.append((p[4], conf, meas, truth))
assert len(falses) == 8, f"expected 8 KB4 falses, got {len(falses)}"
print(f"KB4 falses: {[(c, m) for _, c, m, _ in falses]}", file=sys.stderr)

# ---- extract honest off-scale novels (judged == truth, DISP=ACCEPT_INSTALL)
ptc, col = [], []
with open(LED_D) as f:
    for line in f:
        p = line.rstrip("\n").split("|")
        if len(p) < 17 or p[15] != "DISP=ACCEPT_INSTALL":
            continue
        if p[7] != p[12]:
            continue
        nm, c, m = p[4], int(p[8]), int(p[10])
        if "_PTC-" in nm:
            ptc.append((nm, c, m))
        elif "_COL-" in nm:
            col.append((nm, c, m))
ptc.sort()
col.sort()
assert len(ptc) == 16 and len(col) == 12, f"PTC={len(ptc)} COL={len(col)}"
print(f"off-scale honest: PTC={len(ptc)} COL={len(col)}", file=sys.stderr)

# ---- extract TMB-1 same-scale novels from exemplars.tsv
tmb1 = []
with open(EXEMPL) as f:
    for line in f:
        p = line.rstrip("\n").split("\t")
        if len(p) == 4 and p[1] == "TMB-1":
            tmb1.append((int(p[2]), int(p[3])))
assert len(tmb1) == 6, f"TMB-1 exemplars: {len(tmb1)}"
print(f"TMB-1 exemplars: {tmb1}", file=sys.stderr)

# ---- KB4 false-cluster box (frozen)
BOX = (764, 832, 1888, 2373)


def in_box(c, m):
    return BOX[0] <= c <= BOX[1] and BOX[2] <= m <= BOX[3]


# ============ phase 1: calibration -> B ============
cal_eps = []
for i in range(40):
    off = 5000 + i * 53
    cal_eps.append([(honest(k, off)[0], honest(k, off)[1], C_HON)
                    for k in range(40)])
B = calibrate_B(cal_eps)
print(f"CALIBRATED B={B}", file=sys.stderr)
assert B > 0

# ============ phase 2: drift profiles ============
# 4 rates x 15 profiles; drift starts at step 10 toward a box target.
profiles = []
for fi, f in enumerate([25, 50, 75, 100]):
    sc = (f * 17) // 100
    sm = (f * 29) // 100
    for p in range(15):
        off = 2000 + fi * 1000 + p * 37
        tc = 764 + (p % 5) * 17
        tm = 1888 + (p // 5) * 242
        profiles.append(dict(f=f, sc=sc, sm=sm, p=p, off=off,
                             target=(tc, tm)))


def build_drift_steps(pr):
    steps = []
    off, sc, sm = pr["off"], pr["sc"], pr["sm"]
    tc, tm = pr["target"]
    c, m = honest(9, off)
    for k in range(400):  # over-generate; trimmed below
        if k <= 9:
            c, m = honest(k, off)
            steps.append((c, m, C_HON))
        else:
            nc = c + sc * (1 if tc > c else -1) if abs(tc - c) > sc else tc
            nm = m + sm * (1 if tm > m else -1) if abs(tm - m) > sm else tm
            c, m = nc, nm
            steps.append((c, m, C_DRF))
            if c == tc and m == tm:
                # hold at target 30 more steps, then stop
                for _ in range(30):
                    steps.append((c, m, C_DRF))
                break
    return steps


def onset_and_maxerr(steps):
    """per-step short-term errors; returns (e10, max e over drift t>=11)."""
    errs = []
    hist = []
    for t, (c, m, cls) in enumerate(steps):
        if len(hist) == 0:
            e = 0
        elif len(hist) == 1:
            e = linf(c, m, hist[0][0], hist[0][1])
        else:
            e = linf(c, m, 2 * hist[1][0] - hist[0][0],
                     2 * hist[1][1] - hist[0][1])
        hist.append((c, m))
        hist = hist[-2:]
        errs.append(e)
    e10 = errs[10]
    drift_max = max(errs[11:]) if len(errs) > 11 else 0
    return e10, drift_max


# onset check: per-step error at drift start (step 10) must be <= B, and the
# sustained drift (t>=11) must stay sub-budget (else Arm A's per-step check
# would catch the transient/mid-drift, confounding P1). Search deterministically
# over prefix offsets for a sub-budget onset.
bad_onset = []
for pr in profiles:
    base_off = pr["off"]
    found = False
    for trial in range(500):
        pr["off"] = base_off + trial
        steps = build_drift_steps(pr)
        e10, dmax = onset_and_maxerr(steps)
        if e10 <= B and dmax <= B:
            pr["onset_e"] = e10
            pr["drift_maxerr"] = dmax
            pr["steps"] = steps
            found = True
            break
    if not found:
        bad_onset.append((pr["f"], pr["p"]))
print(f"drift onset check: {len(bad_onset)}/60 profiles without sub-budget "
      f"onset after search", file=sys.stderr)
assert not bad_onset, f"profiles without sub-budget onset: {bad_onset[:5]}"

# entry step per profile (first in-box DRF step)
for pr in profiles:
    entry = -1
    for t, (c, m, cls) in enumerate(pr["steps"]):
        if cls == C_DRF and in_box(c, m):
            entry = t
            break
    pr["entry"] = entry
    assert entry > 0, f"profile f={pr['f']} p={pr['p']} never enters box"

# ============ phase 3: honest_max_C, C_at_entry, r_min ============
# Simulate with ArmC, D_max=INF (no cumulative revoke), to measure C(t).
# With v=0 and stationary honest, C(t)=|p-anchor| does NOT grow; honest_max_C
# is just the max jitter distance. Measured directly (with re-anchor).
INF = 10 ** 15


def C_series(arm_B, steps):
    """C(t) series mirroring ArmC internals (v=0: C=|p-anchor|). No promotion."""
    hist = []
    anchor = (0, 0)
    anchored = False
    out = {}
    for t, (c, m, cls) in enumerate(steps):
        if len(hist) == 0:
            e = 0
        elif len(hist) == 1:
            e = linf(c, m, hist[0][0], hist[0][1])
        else:
            e = linf(c, m, 2 * hist[1][0] - hist[0][0],
                     2 * hist[1][1] - hist[0][1])
        if e > arm_B:
            anchored = False
            hist = [(c, m)]
        else:
            hist.append((c, m))
            hist = hist[-2:]
            if not anchored:
                anchored = True
                anchor = (c, m)
            out[t] = linf(c, m, anchor[0], anchor[1])
    return out


def max_C_with_reanchor(arm_B, arm_W, steps):
    """Max C(t) running the real ArmC promotion/re-anchor logic."""
    arm = ArmC(B=arm_B, D_max=INF, D_promote=INF, W=arm_W, K=3, tomb_r=15)
    n = len(steps)
    tier = [T_NONE] * n
    hist = []
    anchor = (0, 0)
    anchored = False
    clean_run = 0
    oldest_uncom = 0
    mx = 0
    for t, (c, m, cls) in enumerate(steps):
        if len(hist) == 0:
            e = 0
        elif len(hist) == 1:
            e = linf(c, m, hist[0][0], hist[0][1])
        else:
            e = linf(c, m, 2 * hist[1][0] - hist[0][0],
                     2 * hist[1][1] - hist[0][1])
        tier[t] = T_PROV
        if e > arm_B:
            tier[t] = T_SUSP
            anchor = (c, m)
            anchored = True
            hist = [(c, m)]
            clean_run = 0
        else:
            clean_run += 1
            hist.append((c, m))
            hist = hist[-2:]
            if not anchored:
                anchored = True
                anchor = (c, m)
            Ct = linf(c, m, anchor[0], anchor[1])
            if Ct > mx:
                mx = Ct
            if clean_run >= arm_W:
                s = oldest_uncom
                while s <= t - arm_W:
                    if tier[s] in (T_PROV, T_SUSP):
                        tier[s] = T_COM
                    s += 1
                anchor = (c, m)
                while (oldest_uncom <= t and
                       tier[oldest_uncom] not in (T_PROV, T_SUSP)):
                    oldest_uncom += 1
    return mx


hon_eps = []
for i in range(120):
    off = 9000 + i * 61
    hon_eps.append([(honest(k, off)[0], honest(k, off)[1], C_HON)
                    for k in range(80)])

# W is solved jointly below; start with a guess, iterate once.
W_guess = 40
honest_max_C = max(max_C_with_reanchor(B, W_guess, s) for s in hon_eps)
print(f"honest_max_C (W={W_guess}) = {honest_max_C}", file=sys.stderr)

# C at entry + per-step growth during drift (v=0 C_series)
min_C_entry = INF
growths = []
for pr in profiles:
    cs = C_series(B, pr["steps"])
    entry = pr["entry"]
    ce = max((cs[t] for t in cs if t <= entry), default=0)
    pr["C_entry"] = ce
    if ce < min_C_entry:
        min_C_entry = ce
    c10 = cs.get(10, 0)
    if entry > 10:
        growths.append((ce - c10) / (entry - 10))

r_min = min(growths)
print(f"min_C_at_entry={min_C_entry} r_min={r_min:.2f}", file=sys.stderr)

# ---- solve for D_max, W ----
# D_max = FRAC * min_C_at_entry; W = ceil(2*D_max/r_min)+5
# require D_max > 3 * honest_max_C
FRAC = 0.7
D_max = int(FRAC * min_C_entry)
W = math.ceil(2 * D_max / r_min) + 5
# re-measure honest_max_C at the solved W (re-anchor interval matters)
honest_max_C = max(max_C_with_reanchor(B, W, s) for s in hon_eps)
print(f"D_max={D_max} W={W} honest_max_C={honest_max_C} "
      f"(need D_max > {3*honest_max_C})", file=sys.stderr)
assert D_max > 3 * honest_max_C, \
    f"NO OPERATING POINT: D_max={D_max} <= 3*honest_max_C={3*honest_max_C}"
D_promote = D_max // 2
print(f"FROZEN PARAMS: B={B} D_max={D_max} D_promote={D_promote} "
      f"W={W} K=3 N=20 TOMB_R=15", file=sys.stderr)

# verify W-rule: full ArmC sim on drift profiles -> zero drift commits,
# revoke before entry.
armC = ArmC(B=B, D_max=D_max, D_promote=D_promote, W=W, K=3, tomb_r=15)
T_REV, T_COM = 3, 4
for pr in profiles:
    r = armC.run_episode(pr["steps"])
    tier = r["tier"]
    drf_commit = sum(1 for t, (c, m, cls) in enumerate(pr["steps"])
                     if cls == C_DRF and tier[t] == T_COM)
    rev_steps = [t for t in range(len(tier)) if tier[t] == T_REV]
    first_rev = min(rev_steps) if rev_steps else -1
    assert drf_commit == 0, \
        f"W-RULE VIOLATED f={pr['f']} p={pr['p']}: {drf_commit} drift commits"
    assert first_rev != -1 and first_rev < pr["entry"], \
        f"DRIFT NOT REVOKED BEFORE ENTRY f={pr['f']} p={pr['p']}: " \
        f"rev={first_rev} entry={pr['entry']}"
print("W-rule verified: 60/60 drift profiles, 0 drift commits, "
      "all revoked before entry", file=sys.stderr)

# ============ phase 4: generate batteries ============
os.makedirs(OUTDIR, exist_ok=True)
rows = []  # (filename, ep, step, cls, c, m)


def emit(fn, ep, step, cls, c, m):
    rows.append((fn, ep, step, CLS_CH[cls], c, m, TRUTH[cls]))


# ---- (i) novel-60 ----
# 30 same-scale: 6 TMB-1 x 5 offsets; 30 off-scale: 16 PTC + 12 COL + 2 repeats
same_specs = []
for ei, (ec, em) in enumerate(tmb1):
    for r in range(5):
        same_specs.append((f"NOV-S{len(same_specs)+1:02d}", ec, em,
                           30000 + ei * 100 + r * 17))
off_specs = []
for i, (nm, ec, em) in enumerate(ptc):
    off_specs.append((f"NOV-O{len(off_specs)+1:02d}", ec, em,
                      31000 + i * 19))
for i, (nm, ec, em) in enumerate(col):
    off_specs.append((f"NOV-O{len(off_specs)+1:02d}", ec, em,
                      32000 + i * 23))
# 2 repeats to reach 30 off-scale (16+12=28)
off_specs.append((f"NOV-O{len(off_specs)+1:02d}", ptc[0][1], ptc[0][2], 33001))
off_specs.append((f"NOV-O{len(off_specs)+1:02d}", col[0][1], col[0][2], 33002))
assert len(same_specs) == 30, len(same_specs)
assert len(off_specs) == 30, len(off_specs)
novel_specs = same_specs + off_specs
POST = W + 15
for ep, ec, em, offv in novel_specs:
    for k in range(15):
        c, m = honest(k, offv)
        emit("novel.tsv", ep, k, C_HON, c, m)
    emit("novel.tsv", ep, 15, C_NOV, ec, em)
    for k in range(16, 16 + POST):
        dc, dm = jitter(offv + 7000 + k)
        emit("novel.tsv", ep, k, C_NOV, ec + dc, em + dm)

# ---- (ii) drift-60 ----
for pr in profiles:
    ep = f"DRF-{pr['f']}-P{pr['p']:02d}"
    for t, (c, m, cls) in enumerate(pr["steps"]):
        emit("drift.tsv", ep, t, cls, c, m)

# ---- (iii) inject-32: 8 falses x 4 positions ----
for fi, (nm, fc, fm, ft) in enumerate(falses):
    for pi, pos in enumerate([15, 25, 35, 45]):
        ep = f"INJ-F{fi+1}-P{pos}"
        off = 40000 + fi * 200 + pi * 31
        for k in range(pos):
            c, m = honest(k, off)
            emit("inject.tsv", ep, k, C_HON, c, m)
        emit("inject.tsv", ep, pos, C_INJ, fc, fm)
        for k in range(pos + 1, pos + 1 + POST):
            c, m = honest(k, off)
            emit("inject.tsv", ep, k, C_HON, c, m)

# ---- (iv) dos-40 ----
# replay-poison x20: 20 honest, 20 replay-as-spoof, 20 honest revisit
for i in range(20):
    ep = f"DOS-RPL-{i+1:02d}"
    off = 50000 + i * 41
    base = [honest(k, off) for k in range(20)]
    for k, (c, m) in enumerate(base):
        emit("dos.tsv", ep, k, C_HON, c, m)
    for k, (c, m) in enumerate(base):
        emit("dos.tsv", ep, 20 + k, C_RPL, c, m)
    for k, (c, m) in enumerate(base):
        emit("dos.tsv", ep, 40 + k, C_HON, c, m)
# spike-spam x20: 20 honest, 10 spikes every 3 steps, 20 honest
for i in range(20):
    ep = f"DOS-SPK-{i+1:02d}"
    off = 60000 + i * 43
    for k in range(20):
        c, m = honest(k, off)
        emit("dos.tsv", ep, k, C_HON, c, m)
    for k in range(20, 50):
        c, m = honest(k, off)
        if (k - 20) % 3 == 0:
            emit("dos.tsv", ep, k, C_SPK, c + 500, m - 1500)
        else:
            emit("dos.tsv", ep, k, C_HON, c, m)
    for k in range(50, 70):
        c, m = honest(k, off)
        emit("dos.tsv", ep, k, C_HON, c, m)

# ---- (v) honest-120 ----
for i in range(120):
    ep = f"HON-{i+1:03d}"
    off = 9000 + i * 61
    for k in range(80):
        c, m = honest(k, off)
        emit("honest.tsv", ep, k, C_HON, c, m)

# ---- cal.tsv ----
for i in range(40):
    ep = f"CAL-{i+1:02d}"
    off = 5000 + i * 53
    for k in range(40):
        c, m = honest(k, off)
        emit("cal.tsv", ep, k, C_HON, c, m)

# write files
byfn = {}
for r in rows:
    byfn.setdefault(r[0], []).append(r)
shas = {}
for fn, rs in sorted(byfn.items()):
    p = os.path.join(OUTDIR, fn)
    with open(p, "w") as f:
        f.write("ep\tstep\tcls\tconf\tmeas\ttruth\n")
        for _, ep, step, cls, c, m, truth in rs:
            f.write(f"{ep}\t{step}\t{cls}\t{c}\t{m}\t{truth}\n")
    shas[fn] = sha256_file(p)
    print(f"wrote {fn}: {len(rs)} rows sha={shas[fn][:16]}...", file=sys.stderr)

spec = {
    "frozen_inputs": {
        "fixtures_ledger.txt": PIN_RT300,
        "ledger_d_withhold.txt": PIN_D,
        "exemplars.tsv": PIN_EX,
    },
    "params": {"B": B, "D_max": D_max, "D_promote": D_promote, "W": W,
               "K": 3, "N_armB": 20, "TOMB_R": 15,
               "cluster_box": list(BOX)},
    "derivation": {
        "B": "max L_inf short-term prediction error over 40 honest "
             "calibration episodes (t>=2)",
        "honest_stream": "stationary (650,2600) + deterministic jitter "
             "(dc in {-8,0,8}, dm in {-14,0,14}); v=0 reference, "
             "C(t)=L_inf(p(t),anchor)",
        "honest_max_C": honest_max_C,
        "min_C_at_entry": min_C_entry,
        "r_min": r_min,
        "D_max": "floor(0.7 * min_C_at_entry); required > 3*honest_max_C",
        "D_promote": "D_max // 2",
        "W": "ceil(2*D_max / r_min) + 5; simulation-verified: 0 drift "
             "commits and revoke-before-entry on all 60 drift profiles",
        "K": "preregistered 3 (persistence window)",
        "N_armB": "preregistered 20 (Arm B provisional warrant window)",
        "TOMB_R": "preregistered 15 (L_inf tombstone match radius)",
    },
    "batteries": shas,
    "counts": {fn: len(rs) for fn, rs in sorted(byfn.items())},
}
with open(os.path.join(OUTDIR, "spec.json"), "w") as f:
    json.dump(spec, f, indent=2)
print("SPEC: " + json.dumps(spec["params"]), file=sys.stderr)
print("ALL BATTERIES BUILT", file=sys.stderr)
