#!/usr/bin/env python3
"""R0 fork-exhaustion sweep: test ALL paths and ALL forks for R-3/R-4/R-5.

Pure arithmetic on frozen measured numbers + synthetic suites. No RNG
(no random import; all data literal). Deterministic by construction.

Measured values (formal legs, commit 13bbaf07067e, byte-identical reruns):
  R-3: leg0 raw=950 chunk=550 dual=950 d=0 ratio_mp=1417
       leg1 raw=950 chunk=250 dual=950 d=0 ratio_mp=1195
  R-4: both legs 950 at all six doses 250/500/1000/2000/4000/8000
  R-5: clean 8/8 every (leg,exposure); contested 4/4 every (leg,exposure);
       onset leg0 e=3, leg1 e=4.
"""
import json, os

OUT = "/tmp/r0_fork"
os.makedirs(OUT, exist_ok=True)

# =====================================================================
# R-3  (B-T2: |dual-raw| <= eps AND ratio >= floor AND chunk<dual,raw)
# =====================================================================
LEG0 = dict(raw=950, chunk=550, dual=950, d=0, ratio_mp=1417)
LEG1 = dict(raw=950, chunk=250, dual=950, d=0, ratio_mp=1195)
LEGS = [LEG0, LEG1]

R3_EPS = [0, 5, 10, 15, 25, 50]            # /1000
R3_FLOOR = [1000, 1100, 1150, 1200, 1300]  # milli ratio

def r3_eval(d, ratio_mp, chunk, raw, eps, floor_mp, eps_le=True, ratio_ge=True,
            chunk_mode="binary", drop_chunk=False):
    """chunk_mode: 'binary' (chunk<dual and chunk<raw) or 'margin' (raw-chunk > eps).
    drop_chunk: structural fork removing the chunk conjunct entirely."""
    dual = raw - d if d >= 0 else raw + (-d)  # d = |dual-raw| signed handling below
    ok_eps = (d <= eps) if eps_le else (d < eps)
    ok_ratio = (ratio_mp >= floor_mp) if ratio_ge else (ratio_mp > floor_mp)
    if drop_chunk:
        ok_chunk = True
    elif chunk_mode == "binary":
        ok_chunk = (chunk < dual) and (chunk < raw)
    else:  # margin: chunk must lose by MORE than eps
        ok_chunk = (raw - chunk > eps) and (dual - chunk > eps)
    return ok_eps and ok_ratio and ok_chunk

def r3_cell(d, ratio_mp, chunk, raw, eps, floor_mp, **kw):
    return all(r3_eval(d, ratio_mp, chunk, raw, eps, floor_mp, **kw) for (d, ratio_mp, chunk, raw) in [(d, ratio_mp, chunk, raw)])

# --- normative + adversarial scenarios: (name, d, ratio_mp, chunk, raw, expected) ---
R3_SCEN = [
    ("N1_leg0_measured", 0, 1417, 550, 950, True),
    ("N1_leg1_measured", 0, 1195, 250, 950, True),
    ("A1_degenerate_dual_is_raw", 0, 1000, 550, 950, False),   # anti-degeneracy
    ("A2_trivial_compression_1.02", 0, 1020, 550, 950, False),
    ("A3_dual_30_worse", 30, 1417, 550, 950, False),            # 6-label miss
    ("A4_dual_at_eps_boundary", None, 1417, 550, 950, True),    # d := eps (boundary PASS under <=)
    ("A5_chunk_beats_dual", 0, 1417, 950, 950, False),          # chunk conjunct must fire
    ("A6_ratio_just_under_floor", None, None, 550, 950, False), # ratio_mp := floor-1
    ("A8_future_tighter_gate_1.10", 0, 1100, 250, 950, "varies"),  # headroom probe
    ("A9_five_label_miss", 25, 1417, 550, 950, "varies"),       # eps precedent probe
    ("A10_small_chunk_deficit", 0, 1417, 920, 950, "varies"),   # chunk-margin fork probe
    ("A11_future_regime_1.125", 0, 1125, 250, 950, "varies"),  # 1.1-vs-1.15 headroom probe
]

r3_results = {}  # (eps, floor, variant) -> {scen: outcome}
VARIANTS_R3 = {
    "base": {},
    "eps_strict": {"eps_le": False},
    "ratio_strict": {"ratio_ge": False},
    "chunk_margin": {"chunk_mode": "margin"},
    "no_chunk_conjunct": {"drop_chunk": True},
}
for eps in R3_EPS:
    for fl in R3_FLOOR:
        for vname, kw in VARIANTS_R3.items():
            outcomes = {}
            for name, d, ratio_mp, chunk, raw, exp in R3_SCEN:
                dd = eps if (d is None and name == "A4_dual_at_eps_boundary") else (d if d is not None else 0)
                rr = fl - 1 if ratio_mp is None else ratio_mp
                outcomes[name] = r3_eval(dd, rr, chunk, raw, eps, fl, **kw)
            r3_results[(eps, fl, vname)] = outcomes

# normative mismatch count per cell (skip 'varies' scenarios for mismatch, record separately)
def r3_mismatches(outcomes):
    n = 0
    for name, d, ratio_mp, chunk, raw, exp in R3_SCEN:
        if exp == "varies":
            continue
        if outcomes[name] != exp:
            n += 1
    return n

json.dump({f"{e}/{f}/{v}": o for (e, f, v), o in r3_results.items()},
          open(f"{OUT}/r3_raw.json", "w"), indent=1)

# =====================================================================
# R-4  (B-T3 dose curve)
# =====================================================================
DOSES = [250, 500, 1000, 2000, 4000, 8000]
R4_TOL = [0, 5, 10, 25, 50]

R4_CURVES = [  # (name, scores, normative)
    ("M0_measured", [950]*6, True),
    ("S1_one_span_loss", [950,950,950,950,950,910], False),
    ("S1b_sub_span_loss", [950,950,950,950,950,930], True),
    ("S2_transient_recovers", [950,950,950,945,950,950], True),
    ("S3_slow_bleed_25", [950,945,945,940,935,925], True),
    ("S3b_deep_bleed_50", [950,940,930,920,910,900], False),
    ("S4_cliff_50", [950,950,900,900,900,900], False),
    ("S5_sawtooth", [950,930,950,930,950,930], True),
    ("S6_early_dip_nondecr", [900,900,950,950,950,950], True),
    ("S7_boundary_25", [950,950,950,950,950,925], True),
    # --- new adversarial ---
    ("A1_double_dip", [950,900,950,900,950,950], False),
    ("A2_drop25_early_flat", [950,925,925,925,925,925], True),
    ("A3_mid_dip25_recovers", [950,950,925,950,950,950], True),
    ("A4_improve_then_bleed", [900,950,940,930,920,910], False),
    ("A5_mid_dip20_recovers", [950,950,930,950,950,950], True),
    ("A6_boundary_30", [950,950,950,950,950,920], False),
    ("A7_slow_bleed_30", [950,945,940,935,930,920], False),
    ("A8_vshape_deep", [950,900,900,900,900,950], False),
]

def stat_drawdown(s):
    peak = s[0]; dd = 0
    for x in s:
        peak = max(peak, x); dd = max(dd, peak - x)
    return dd

def stat_adjacent(s):
    return max([0] + [s[i-1]-s[i] for i in range(1, len(s))])

def stat_cumulative(s):
    return max(0, s[0] - min(s))

def stat_endpoint(s):
    return max(0, s[0] - s[-1])

def stat_totalvar(s):
    return sum(max(0, s[i-1]-s[i]) for i in range(1, len(s)))

def stat_recovery_allowed(s):
    """max drawdown never recovered to its running peak by a later dose."""
    worst = 0
    for i in range(len(s)):
        peak = max(s[:i+1])
        dd = peak - s[i]
        if dd <= 0:
            continue
        recovered = any(x >= peak for x in s[i+1:])
        if not recovered:
            worst = max(worst, dd)
    return worst

def stat_bleed_flag(s):
    """F1 drawdown, but monotone cumulative bleed of any size FAILs (flag hardened)."""
    dd = stat_drawdown(s)
    monotone_bleed = all(s[i] <= s[i-1] for i in range(1, len(s))) and s[-1] < s[0]
    return dd, monotone_bleed

R4_FORMS = {
    "F1_drawdown_runnmax": lambda s: stat_drawdown(s),
    "F2_adjacent_only": lambda s: stat_adjacent(s),
    "F3_cumulative_baseline": lambda s: stat_cumulative(s),
    "F4_strict_zero": lambda s: stat_drawdown(s),   # tol ignored: pass iff ==0
    "F5_endpoint_only": lambda s: stat_endpoint(s),
    "F6_total_variation": lambda s: stat_totalvar(s),
    "F7_recovery_allowed": lambda s: stat_recovery_allowed(s),
}

r4_results = {}  # (form, tol, boundary) -> {curve: outcome}
for fname, fn in R4_FORMS.items():
    for tol in R4_TOL:
        for bname, le in (("le", True), ("lt", False)):
            outcomes = {}
            for cname, s, exp in R4_CURVES:
                if fname == "F4_strict_zero":
                    outcomes[cname] = (fn(s) == 0)
                else:
                    v = fn(s)
                    outcomes[cname] = (v <= tol) if le else (v < tol)
            r4_results[(fname, tol, bname)] = outcomes
# F8: bleed-flag hardened (tol 25, le) as its own fork
for tol in R4_TOL:
    outcomes = {}
    for cname, s, exp in R4_CURVES:
        dd, flag = stat_bleed_flag(s)
        outcomes[cname] = (dd <= tol) and (not flag)
    r4_results[("F8_bleedflag_hard", tol, "le")] = outcomes

def r4_mismatches(outcomes):
    return sum(1 for _, _, exp in R4_CURVES for c in [outcomes[[n for n,_,_ in R4_CURVES][[n for n,_,_ in R4_CURVES].index(c)] if False else None]] if False)

def r4_mm(outcomes):
    n = 0
    for cname, s, exp in R4_CURVES:
        if outcomes[cname] != exp:
            n += 1
    return n

json.dump({f"{f}/{t}/{b}": o for (f, t, b), o in r4_results.items()},
          open(f"{OUT}/r4_raw.json", "w"), indent=1)

# =====================================================================
# R-5  (B-T4 support gap)
# =====================================================================
MINSUP = {0: 3, 1: 4}
EXPS = list(range(1, 17))

# build deterministic 384-row battery: (leg, exp, sub, rep) -> dict
rows = []
for leg in (0, 1):
    ms = MINSUP[leg]
    for exp in EXPS:
        for rep in range(8):
            should_abstain = exp < ms
            rows.append(dict(leg=leg, exp=exp, sub="clean", rep=rep,
                             should_abstain=should_abstain,
                             should_rid=-1 if should_abstain else 2,
                             should_reason=1 if should_abstain else 0,
                             correct=True, fail_kind="none"))
        for rep in range(4):
            should_abstain = True
            rows.append(dict(leg=leg, exp=exp, sub="contested", rep=rep,
                             should_abstain=True, should_rid=-1,
                             should_reason=1 if exp < ms else 2,
                             correct=True, fail_kind="none"))

def degrade(pred, kind):
    """pred(row)->bool selects rows; kind 'outcome' or 'reason_only' -> correct=False."""
    n = 0
    for r in rows:
        if pred(r):
            r["correct"] = False
            r["fail_kind"] = kind
            n += 1
    return n

def reset():
    for r in rows:
        r["correct"] = True
        r["fail_kind"] = "none"

def C(leg=None, exp=None, sub=None, rep=None):
    return dict(leg=leg, exp=exp, sub=sub, rep=rep)

def match(r, **kw):
    return all(v is None or r[k] == v for k, v in kw.items())

R5_SCEN = []  # (name, apply_fn, normative)

def scen(name, normative, pred=None, kind="outcome", setup=None):
    R5_SCEN.append((name, normative, pred, kind))

# measured clean battery = no degradation, normative PASS
scen("M0_measured", True, pred=None)
scen("D1_overeager_e1_leg0", False, pred=lambda r: match(r, leg=0, exp=1, sub="clean"), kind="outcome")
scen("D2_late_onset_leg0", False, pred=lambda r: match(r, leg=0, exp=3, sub="clean"), kind="outcome")
scen("D3_early_onset_leg1", False, pred=lambda r: match(r, leg=1, exp=3, sub="clean"), kind="outcome")
scen("D4_wrong_chunk", False, pred=lambda r: match(r, leg=0, exp=10, sub="clean"), kind="outcome")
scen("D5_contested_leak_1rep", False, pred=lambda r: match(r, leg=1, exp=16, sub="contested", rep=0), kind="outcome")
scen("D6_single_rep_flake", False, pred=lambda r: match(r, leg=0, exp=9, sub="clean", rep=0), kind="outcome")
scen("D7_wrong_reason_preonset", False, pred=lambda r: match(r, leg=0, exp=2, sub="clean"), kind="reason_only")
# --- new adversarial ---
scen("D8_contested_leak_2exp", False,
     pred=lambda r: match(r, sub="contested") and ((r["leg"]==0 and r["exp"]==5 and r["rep"]==0) or (r["leg"]==0 and r["exp"]==12 and r["rep"]==0)),
     kind="outcome")
scen("D9_one_collapsed_exposure", False, pred=lambda r: match(r, leg=1, exp=7, sub="clean"), kind="outcome")
scen("D10_wrong_reason_2exp", False, pred=lambda r: match(r, leg=0, sub="clean") and r["exp"] in (1,2), kind="reason_only")
scen("D11_e1_single_recruit", False, pred=lambda r: match(r, leg=0, exp=1, sub="clean", rep=0), kind="outcome")
scen("D12_contested_3of4", False, pred=lambda r: match(r, leg=1, exp=9, sub="contested", rep=0), kind="outcome")
scen("D13_onset_delayed_both", False,
     pred=lambda r: match(r, sub="clean") and ((r["leg"]==0 and r["exp"]==3) or (r["leg"]==1 and r["exp"]==4)),
     kind="outcome")
scen("D14_contested_full_leak", False, pred=lambda r: match(r, leg=0, exp=16, sub="contested"), kind="outcome")
scen("D15_leg1_e1_single_wrong", False, pred=lambda r: match(r, leg=1, exp=1, sub="clean", rep=0), kind="outcome")

def clean_cells():
    cells = {}
    for r in rows:
        if r["sub"] != "clean":
            continue
        k = (r["leg"], r["exp"])
        c, t = cells.get(k, (0, 0))
        cells[k] = (c + (1 if r["correct"] else 0), t + 1)
    return cells

def clean_outcome_failures():
    return sum(1 for r in rows if r["sub"]=="clean" and r["fail_kind"]=="outcome")

def contested_outcome_failures(leg=None):
    return sum(1 for r in rows if r["sub"]=="contested" and r["fail_kind"]=="outcome"
               and (leg is None or r["leg"]==leg))

def contested_cells():
    cells = {}
    for r in rows:
        if r["sub"] != "contested":
            continue
        k = (r["leg"], r["exp"])
        cells[k] = cells.get(k, 0) + (0 if r["fail_kind"]=="outcome" else 0)
        # count outcome failures per cell:
    out = {}
    for r in rows:
        if r["sub"] != "contested":
            continue
        k = (r["leg"], r["exp"])
        out[k] = out.get(k, 0) + (1 if r["fail_kind"]=="outcome" else 0)
    return out

def w_eval(w):
    cells = clean_cells()
    if w == "W1_strict8":
        ok = all(c == 8 for c, t in cells.values())
    elif w == "W2_ge7":
        ok = all(c >= 7 for c, t in cells.values())
    elif w == "W3a_avg75":
        ok = all(sum(cells[(leg, e)][0]/8 for e in EXPS)/16 >= 7.5/8 for leg in (0,1))
    elif w == "W3b_avg7":
        ok = all(sum(cells[(leg, e)][0]/8 for e in EXPS)/16 >= 7/8 for leg in (0,1))
    elif w == "W4a_pooled100":
        ok = all(sum(cells[(leg, e)][0] for e in EXPS) == 128 for leg in (0,1))
    elif w == "W4b_pooled63_64":
        ok = all(sum(cells[(leg, e)][0] for e in EXPS) >= 126 for leg in (0,1))
    elif w == "W4c_pooled7_8":
        ok = all(sum(cells[(leg, e)][0] for e in EXPS) >= 112 for leg in (0,1))
    elif w == "W5_onset_split":
        ok = (clean_outcome_failures() == 0)
    elif w == "W7_xleg_pooled100":
        ok = (sum(c for c, t in cells.values()) == 256)
    elif w == "W8_xleg_pooled255":
        ok = (sum(c for c, t in cells.values()) >= 255)
    else:
        raise ValueError(w)
    return ok

def c_eval(c):
    cc = contested_cells()
    if c == "C1_zero":
        ok = all(v == 0 for v in cc.values())
    elif c == "C2_le1_per_cell":
        ok = all(v <= 1 for v in cc.values())
    elif c == "C3_le1_per_leg":
        ok = all(contested_outcome_failures(leg) <= 1 for leg in (0,1))
    elif c == "C4_le1_total":
        ok = (contested_outcome_failures() <= 1)
    else:
        raise ValueError(c)
    return ok

R5_WORDS = ["W1_strict8","W2_ge7","W3a_avg75","W3b_avg7","W4a_pooled100",
            "W4b_pooled63_64","W4c_pooled7_8","W5_onset_split",
            "W7_xleg_pooled100","W8_xleg_pooled255"]
R5_CONT = ["C1_zero","C2_le1_per_cell","C3_le1_per_leg","C4_le1_total"]

r5_results = {}
for name, normative, pred, kind in R5_SCEN:
    reset()
    nflip = degrade(pred, kind) if pred else 0
    for w in R5_WORDS:
        for c in R5_CONT:
            r5_results[(name, w, c)] = (w_eval(w) and c_eval(c), nflip)

def r5_mm(cell_outcomes):
    n = 0
    for name, normative, pred, kind in R5_SCEN:
        if cell_outcomes[name] != normative:
            n += 1
    return n

json.dump({f"{n}|{w}|{c}": {"pass": p, "flipped": f} for (n, w, c), (p, f) in r5_results.items()},
          open(f"{OUT}/r5_raw.json", "w"), indent=1)

# ---- mismatch summary tables ----
print("=== R3: mismatches vs normative (base variant), eps x floor ===")
print("eps\\floor | " + " | ".join(str(f) for f in R3_FLOOR))
for eps in R3_EPS:
    row = []
    for fl in R3_FLOOR:
        row.append(str(r3_mismatches(r3_results[(eps, fl, "base")])))
    print(f"{eps:>7} | " + " | ".join(f"{x:>5}" for x in row))

print("\n=== R3: boundary-semantics forks (mismatches) ===")
for vname in VARIANTS_R3:
    mm = {(e, f): r3_mismatches(r3_results[(e, f, vname)]) for e in R3_EPS for f in R3_FLOOR}
    cells = sum(1 for v in mm.values() if v == 0)
    print(f"{vname:>18}: cells with 0 mismatches = {cells}/30")

print("\n=== R4: mismatches vs normative, formulation x tol (le boundary) ===")
print("form\\tol | " + " | ".join(str(t) for t in R4_TOL))
for fname in list(R4_FORMS) + ["F8_bleedflag_hard"]:
    row = []
    for tol in R4_TOL:
        key = (fname, tol, "le")
        row.append(str(r4_mm(r4_results[key])))
    print(f"{fname:>20} | " + " | ".join(f"{x:>5}" for x in row))

print("\n=== R4: lt-boundary mismatches at tol=25 ===")
for fname in list(R4_FORMS):
    print(f"{fname:>20}: {r4_mm(r4_results[(fname, 25, 'lt')])}")

print("\n=== R5: mismatches vs normative, wording x contested ===")
print("word\\cont | " + " | ".join(R5_CONT))
for w in R5_WORDS:
    row = []
    for c in R5_CONT:
        mo = {name: r5_results[(name, w, c)][0] for name, _, _, _ in R5_SCEN}
        n = sum(1 for name, normative, _, _ in R5_SCEN if mo[name] != normative)
        row.append(str(n))
    print(f"{w:>16} | " + " | ".join(f"{x:>14}" for x in row))

print("\nDONE")

# ================= DETAIL DUMPS (which scenarios mismatch, for the verdict) ===
print("\n### R3 detail: mismatching scenarios")
for (eps, fl, vname) in [(0,1000,"base"), (25,1000,"base"), (50,1150,"base"),
                         (25,1200,"base"), (25,1150,"ratio_strict"), (0,1000,"ratio_strict")]:
    o = r3_results[(eps, fl, vname)]
    bad = [name for name, d, rr, ch, ra, exp in R3_SCEN
           if exp != "varies" and o[name] != exp]
    print(f"eps={eps} floor={fl} {vname}: mismatches={bad}")

print("\n### R3 A8/A9/A11 probes (floor -> outcome), base variant, eps=25")
for name in ["A8_future_tighter_gate_1.10", "A9_five_label_miss", "A11_future_regime_1.125"]:
    row = {fl: r3_results[(25, fl, "base")][name] for fl in R3_FLOOR}
    print(f"{name}: {row}")
print("### R3 A9 probe across eps (floor=1150):",
      {e: r3_results[(e, 1150, "base")]["A9_five_label_miss"] for e in R3_EPS})
print("### R3 A3 (dual 30 worse) across eps (floor=1150):",
      {e: r3_results[(e, 1150, "base")]["A3_dual_30_worse"] for e in R3_EPS})

print("\n### R4 detail: mismatching curves at tol=25 (le)")
for fname in ["F1_drawdown_runnmax","F2_adjacent_only","F3_cumulative_baseline",
              "F5_endpoint_only","F6_total_variation","F7_recovery_allowed","F8_bleedflag_hard"]:
    o = r4_results[(fname, 25, "le")]
    bad = [cname for cname, s, exp in R4_CURVES if o[cname] != exp]
    print(f"{fname}: mismatches={bad}")

print("\n### R5 detail: mismatching scenarios")
for (w, c) in [("W5_onset_split","C1_zero"),("W2_ge7","C1_zero"),("W1_strict8","C2_le1_per_cell"),
               ("W1_strict8","C3_le1_per_leg"),("W4b_pooled63_64","C1_zero"),("W8_xleg_pooled255","C1_zero")]:
    bad = [name for name, normative, _, _ in R5_SCEN if r5_results[(name, w, c)][0] != normative]
    print(f"{w} x {c}: mismatches={bad}")

# equivalence proof artifacts: W1 vs W4a vs W7 identical on every scenario
print("\n### R5 equivalence check W1==W4a==W7 across all scenarios x contested:")
for c in R5_CONT:
    same = all(r5_results[(n,"W1_strict8",c)][0]==r5_results[(n,"W4a_pooled100",c)][0]==r5_results[(n,"W7_xleg_pooled100",c)][0]
               for n,_,_,_ in R5_SCEN)
    print(f"{c}: identical={same}")
