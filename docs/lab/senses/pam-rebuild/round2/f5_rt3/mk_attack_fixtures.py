#!/usr/bin/env python3
"""RT-3 attack fixture generator (H-PAM-17/18/19 vs the F5 full mechanism).

Deterministic, zero RNG. All map-derived selections come from the OBSERVED
map (map.json) — no source constants. A19's near-copy verification uses the
frozen analytic constants (the same frozen geometry RT-1 used).

Batteries:
  A17F  falses, BACKTEST format,  map install-side d<=25, thin to 60
  A17Tm mixed: 240 frozen NEAR + 60 adaptive trues (NEAR format)
  A17B  falses, BACKTEST format,  nearest install-side map pt per backtest false (8)
  A18T  1500 trues, NEAR format, 3x500 chunks, [C,C,C,W,W] interleave
  A18F  1500 falses, BACKTEST format, 3x500 chunks, same geometry
  A19   60 falses, BACKTEST format, 50 rescued coords + 10 verified near-copies
"""
import json, math

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt3"
R2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2"

mp = json.load(open(D + "/map.json"))

def norm_dec(v):
    return "ALLOWED" if v["decision"] == "-" else v["decision"]

install_pts, withhold_pts = [], []
for k, v in mp.items():
    c, m = (int(x) for x in k.split(","))
    d = norm_dec(v)
    if d in ("ALLOWED", "CONFIRM_INSTALL"):
        install_pts.append((c, m, v["blocked"], d))
    elif d == "WITHHOLD":
        withhold_pts.append((c, m))

print("install-side map pts:", len(install_pts),
      "withhold-side:", len(withhold_pts))

def min_dist(p, qs):
    c, m = p[0], p[1]
    best = None
    for qc, qm in qs:
        dd = math.hypot(c - qc, m - qm)
        if best is None or dd < best:
            best = dd
    return best

wset = [(c, m) for c, m in withhold_pts]
iset = [(c, m) for c, m, _, _ in install_pts]

cand_install = [(c, m, b, d) for c, m, b, d in install_pts
                if min_dist((c, m), wset) <= 25]
cand_withhold = [(c, m) for c, m in withhold_pts
                 if min_dist((c, m), iset) <= 25]
print("boundary-adjacent install candidates:", len(cand_install))
print("boundary-adjacent withhold candidates:", len(cand_withhold))

def thin(cands, n):
    cands = sorted(cands, key=lambda p: (p[1], p[0]))
    if len(cands) <= n:
        return cands
    k = len(cands) // n
    return cands[::k][:n]

def bt_line(tag, seq, c, m, false):
    j = "RICH"
    t = "DARK" if false else "RICH"
    fx = "rt4_TMB-5_%s_%04d.r24" % (tag, seq)
    f = ["0" * 64, "0" * 64, "0", "3", fx, "2", "1", j, str(c), "0", str(m),
         "0" * 64, t, "1", str(c), "DISP=ACCEPT_INSTALL", "DETAIL=rt3_" + tag]
    return "|".join(f), fx

def near_line(tag, seq, c, m):
    fx = "rt4_TMB-5_%s_%04d.r24" % (tag, seq)
    f = ["0" * 64, "0" * 64, "0", "3", fx, "2", "1", "RICH", str(c), "0",
         str(m), "0" * 64, "RICH", "1", str(c), "DISP=ACCEPT_INSTALL",
         "DETAIL=rt3_" + tag, "SET=NEAR"]
    return "|".join(f), fx

# ---- analytic geometry (frozen consts; only for A19 verification) ----
EX = [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632),
      (713, 2627)]
def ablocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EX)
def arep(c, m):
    n = 0
    for dc, dm in [(-10, -200), (0, 0), (10, 200)]:
        if any(abs(c + dc - ec) <= 130 and abs(m + dm - em) <= 950
               for ec, em in EX):
            n += 1
    return n
def adec(c, m):
    if not ablocked(c, m):
        return "ALLOWED"
    return "WITHHOLD" if arep(c, m) >= 2 else "CONFIRM_INSTALL"

expect = {}
ledgers = {}

def add_battery(name, fmt, items):
    """items: list of (c, m, false). fmt 'bt' or 'near'."""
    lines = []
    for seq, (c, m, false) in enumerate(items):
        if fmt == "bt":
            l, fx = bt_line(name, seq, c, m, false)
        else:
            assert not false
            l, fx = near_line(name, seq, c, m)
        lines.append(l)
        expect[fx] = {"tag": name, "conf": c, "meas": m, "false": false,
                      "fmt": fmt}
    ledgers[name] = lines
    return lines

def map_expect(name):
    for fx, e in expect.items():
        if e["tag"] == name:
            v = mp["%d,%d" % (e["conf"], e["meas"])]
            e["exp_dec"] = norm_dec(v)
            e["exp_blocked"] = v["blocked"]

# ---- A17F: adaptive falses ----
sel_f = thin(cand_install, 60)
print("A17F n=%d (target 60)" % len(sel_f))
add_battery("A17F", "bt", [(c, m, True) for c, m, _, _ in sel_f])
map_expect("A17F")

# ---- A17T: adaptive trues (for the mixed battery) ----
sel_t = thin(cand_withhold, 60)
print("A17T n=%d (target 60)" % len(sel_t))
add_battery("A17T", "near", [(c, m, False) for c, m in sel_t])
map_expect("A17T")

# ---- A17B: adaptive backtest falses ----
btfalse = [(764, 1888), (774, 1915), (788, 1958), (799, 1997),
           (806, 2024), (806, 2373), (819, 2320), (832, 2255)]
a17b = []
for c, m in btfalse:
    best, bd = None, None
    for qc, qm, _, _ in install_pts:
        dd = math.hypot(c - qc, m - qm)
        if bd is None or dd < bd or (dd == bd and (qm, qc) < (best[1], best[0])):
            bd, best = dd, (qc, qm)
    a17b.append((best[0], best[1], True))
    print("A17B backtest (%d,%d) -> install-side (%d,%d) dist %.1f"
          % (c, m, best[0], best[1], bd))
add_battery("A17B", "bt", a17b)
map_expect("A17B")

# ---- A18 pools ----
pool_w = sorted(cand_withhold, key=lambda p: (p[1], p[0]))   # withhold-marginals
pool_c = sorted([(c, m) for c, m, b, _ in cand_install if b],
                key=lambda p: (p[1], p[0]))                  # confirm-marginals (annulus)
print("A18 pools: withhold-marginal %d, confirm-marginal %d"
      % (len(pool_w), len(pool_c)))
# deterministic interleave [C,C,C,W,W]: cycle each pool independently
geom = []
iw = ic = 0
for i in range(1500):
    if i % 5 < 3:
        geom.append(("C", pool_c[ic % len(pool_c)])); ic += 1
    else:
        geom.append(("W", pool_w[iw % len(pool_w)])); iw += 1
nW = sum(1 for k, _ in geom if k == "W")
print("A18 interleave: %d W (expect 600), %d C (expect 900)" % (nW, 1500 - nW))
assert nW == 600

def write_chunks(name, fmt, false):
    items = [(c, m, false) for _, (c, m) in geom]
    for ch in range(3):
        lines = []
        for seq, (c, m, fl) in enumerate(items[ch * 500:(ch + 1) * 500]):
            if fmt == "bt":
                l, fx = bt_line("%s_%d" % (name, ch), seq, c, m, fl)
            else:
                l, fx = near_line("%s_%d" % (name, ch), seq, c, m)
            lines.append(l)
            expect[fx] = {"tag": "%s_%d" % (name, ch), "conf": c, "meas": m,
                          "false": fl, "fmt": fmt,
                          "exp_dec": norm_dec(mp["%d,%d" % (c, m)]),
                          "exp_blocked": mp["%d,%d" % (c, m)]["blocked"]}
        p = "%s/ledger_%s_%d.txt" % (D, name.lower(), ch)
        open(p, "w").write("\n".join(lines) + "\n")
        print("wrote", p, len(lines))

write_chunks("A18T", "near", False)
write_chunks("A18F", "bt", True)

# ---- A19: rescue-template falses ----
rescued = [(650, 3700), (650, 4200), (660, 3700), (660, 4200), (670, 3700),
           (670, 4200), (680, 3700), (680, 4200), (690, 3700), (690, 4200),
           (700, 3700), (700, 4200), (710, 3700), (710, 4200), (720, 3700),
           (720, 4200), (730, 3700), (730, 4200), (740, 3700), (740, 4200),
           (750, 3700), (750, 4200), (760, 3700), (760, 4200), (770, 3700),
           (770, 4200), (780, 3700), (780, 4200), (790, 3700), (790, 4200),
           (800, 3700), (800, 4200), (810, 3700), (810, 4200), (820, 3700),
           (820, 4200), (830, 3700), (830, 4200), (840, 3700), (840, 4200),
           (850, 2200), (850, 2700), (850, 3200), (850, 3700), (850, 4200),
           (860, 2200), (860, 2700), (860, 3200), (860, 3700), (860, 4200)]
assert all(ablocked(c, m) and arep(c, m) < 2 for c, m in rescued)
a19 = [(c, m, True) for c, m in rescued]
used = set(rescued)
for c, m in sorted(rescued, key=lambda p: (p[1], p[0])):
    if len(a19) >= 60:
        break
    for dc, dm in [(1, 0), (-1, 0), (0, 10), (0, -10)]:
        cc, mm = c + dc, m + dm
        if (cc, mm) in used:
            continue
        if ablocked(cc, mm) and arep(cc, mm) < 2:
            a19.append((cc, mm, True))
            used.add((cc, mm))
            break
    else:
        raise AssertionError("no verifying near-copy for %d,%d" % (c, m))
assert len(a19) == 60, len(a19)
print("A19 n=60 (50 rescued + 10 near-copies)")
lines = add_battery("A19", "bt", a19)
for fx, e in expect.items():
    if e["tag"] == "A19":
        e["exp_dec"] = adec(e["conf"], e["meas"])
        e["exp_blocked"] = ablocked(e["conf"], e["meas"])
open(D + "/ledger_a19.txt", "w").write("\n".join(lines) + "\n")

# ---- write A17F / A17B ledgers ----
open(D + "/ledger_a17f.txt", "w").write("\n".join(ledgers["A17F"]) + "\n")
open(D + "/ledger_a17b.txt", "w").write("\n".join(ledgers["A17B"]) + "\n")

# ---- A17T mixed battery: 240 frozen NEAR + 60 adaptive NEAR ----
frozen_near = [l.rstrip("\n") for l in
               open(R2 + "/f5_redteam300/fixtures_ledger.txt")
               if "SET=NEAR" in l][:240]
assert len(frozen_near) == 240
mixed = frozen_near + ledgers["A17T"]
open(D + "/ledger_a17t_mixed.txt", "w").write("\n".join(mixed) + "\n")
print("A17T mixed: %d frozen NEAR + %d adaptive = %d"
      % (len(frozen_near), len(ledgers["A17T"]), len(mixed)))

json.dump(expect, open(D + "/expect.json", "w"), indent=1, sort_keys=True)
print("expect.json entries:", len(expect))
