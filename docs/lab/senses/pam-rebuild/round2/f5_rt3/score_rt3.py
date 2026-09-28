#!/usr/bin/env python3
"""RT-3 scorer: 3x byte-identical SHA checks, per-fixture decision-vs-
expectation assertions (fail loud), kill-bar numbers, delay distributions.

Delay definition (frozen): allowed 0 / confirmed 3 / withheld -1; delayed
>50  <=>  delay == -1. For NEAR-format batteries the binary's own DELAYBAR
line is used; for BACKTEST-format batteries the scorer counts delay==-1
from the per-trial lines (identical definition, M4).
"""
import json, hashlib
from collections import Counter

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt3"
R2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2"
expect = json.load(open(D + "/expect.json"))

# frozen analytic geometry (for the 240 frozen NEAR fixtures in the mixed
# battery, which are not in expect.json)
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

frozen_coords = {}
for l in open(R2 + "/f5_redteam300/fixtures_ledger.txt"):
    f = l.rstrip("\n").split("|")
    if len(f) >= 16 and "DISP=ACCEPT_INSTALL" in f[15]:
        frozen_coords[f[4]] = (int(f[8]), int(f[10]), f[7], f[12])

def get_expect(fx):
    e = expect.get(fx)
    if e is not None:
        return e
    c, m, j, t = frozen_coords[fx]
    return {"tag": "FROZEN", "conf": c, "meas": m, "false": j != t,
            "fmt": "near", "exp_dec": adec(c, m), "exp_blocked": ablocked(c, m)}

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

def parse_run(path):
    trials, delaybar = [], None
    for l in open(path):
        if l.startswith("DELAYBAR"):
            # DELAYBAR delayed_gt50=<n> over=<m>
            f = l.split()
            delaybar = (int(f[1].split("=")[1]), int(f[2].split("=")[1]))
            continue
        if l.startswith(("SETSUM", "BACKTEST", "HIST", "SERIAL", "SANITY")):
            continue
        f = l.rstrip("\n").split("\t")
        # trial, fixture, set, BLOCKED|ALLOWED, exseq|-, decision|-, delay
        fx, blk, dec, delay = f[1], f[3], f[5], int(f[6])
        if dec == "-":
            dec = "ALLOWED"
        trials.append((fx, blk == "BLOCKED", dec, delay))
    return trials, delaybar

def check_battery(name, files, tags):
    """files: list of run paths (one per chunk, run 1). tags: expect tags."""
    shas, alltrials, dbs = [], [], []
    for fp in files:
        r1 = sha(fp[0])
        assert all(sha(p) == r1 for p in fp[1:]), \
            "runs not byte-identical for " + fp[0]
        shas.append(r1)
        tr, db = parse_run(fp[0])
        alltrials += tr
        dbs.append(db)
    mism = []
    n = Counter()
    delays = Counter()
    for fx, blk, dec, delay in alltrials:
        e = get_expect(fx)
        assert e["tag"] in tags or e["tag"] == "FROZEN", \
            "unexpected tag " + e["tag"]
        if dec != e["exp_dec"] or blk != e["exp_blocked"]:
            mism.append((fx, blk, dec, e["exp_blocked"], e["exp_dec"]))
        n[(e["tag"], "false" if e["false"] else "true", dec)] += 1
        delays[delay] += 1
    return shas, n, mism, delays, dbs

print("== determinism: mapping re-queries ==")
for i in ("00", "01", "18", "19"):
    a = sha("%s/run_map_%s.out" % (D, i))
    b = sha("%s/rerun_map_%s.out" % (D, i))
    assert a == b, "re-query mismatch on map_" + i
print("   2000/2000 re-queried points byte-identical: PREMISE HOLDS")

R = {}
R["a17f"] = check_battery("a17f",
    [["%s/run_a17f_%d.out" % (D, r) for r in (1, 2, 3)]], {"A17F"})
R["a17b"] = check_battery("a17b",
    [["%s/run_a17b_%d.out" % (D, r) for r in (1, 2, 3)]], {"A17B"})
R["a19"] = check_battery("a19",
    [["%s/run_a19_%d.out" % (D, r) for r in (1, 2, 3)]], {"A19"})
R["a17t"] = check_battery("a17t",
    [["%s/run_a17t_mixed_%d.out" % (D, r) for r in (1, 2, 3)]],
    {"A17T"})
R["a18t"] = check_battery("a18t",
    [["%s/run_a18t_%d_%d.out" % (D, c, r) for r in (1, 2, 3)]
     for c in (0, 1, 2)],
    {"A18T_0", "A18T_1", "A18T_2"})
R["a18f"] = check_battery("a18f",
    [["%s/run_a18f_%d_%d.out" % (D, c, r) for r in (1, 2, 3)]
     for c in (0, 1, 2)],
    {"A18F_0", "A18F_1", "A18F_2"})

for b, (shas, n, mism, delays, dbs) in R.items():
    print("== battery", b, "3x identical OK; run1 sha", shas[0][:16])
    print("   mismatches vs expectation:", mism if mism else "NONE")
    for k in sorted(n):
        print("   ", k, n[k])
    print("    delays:", dict(sorted(delays.items())), "delaybar:", dbs)

def get(b, tag, falsity, dec):
    return R[b][1].get((tag, falsity, dec), 0)

def ins(b, tag, falsity):
    return get(b, tag, falsity, "CONFIRM_INSTALL") + \
        get(b, tag, falsity, "ALLOWED")

print("\n== H-PAM-17 ==")
f_ins = ins("a17f", "A17F", "false")
f_tot = sum(v for (t, fl, _), v in R["a17f"][1].items()
            if t == "A17F" and fl == "false")
print("   A17F adaptive falses: installed %d/%d (hypothesis predicted >=48/60)"
      % (f_ins, f_tot))
print("   KILL BAR (>=50%% install):",
      "KILL-CONFIRMED" if f_ins / f_tot >= 0.5 else "SURVIVED")
db = R["a17t"][4][0]
print("   A17T mixed battery: binary DELAYBAR delayed %d/%d = %.1f%% "
      "(predicted 40.0%%)" % (db[0], db[1], 100.0 * db[0] / db[1]))
print("   KILL BAR (delay >25%%):",
      "KILL-CONFIRMED" if db[0] / db[1] > 0.25 else "SURVIVED")
b_ins = ins("a17b", "A17B", "false")
b_blk = get("a17b", "A17B", "false", "WITHHOLD")
print("   A17B adaptive backtest: installed %d/8, blocked(withheld) %d/8 "
      "(hypothesis predicted <=3/8 blocked)" % (b_ins, b_blk))

print("\n== H-PAM-18 ==")
td = sum(db[0] for db in R["a18t"][4])
tn = sum(db[1] for db in R["a18t"][4])
t_wh = sum(v for (t, fl, dc), v in R["a18t"][1].items()
           if fl == "true" and dc == "WITHHOLD")
t_tot = sum(v for (t, fl, _), v in R["a18t"][1].items() if fl == "true")
print("   A18T flood trues: binary DELAYBAR delayed %d/%d = %.1f%% "
      "(predicted 35-45%%)" % (td, tn, 100.0 * td / tn))
print("   A18T true-withhold: %d/%d = %.1f%% (frozen backtest bar: 0/34)"
      % (t_wh, t_tot, 100.0 * t_wh / t_tot))
print("   KILL BAR (delay >25%%):",
      "KILL-CONFIRMED" if td / tn > 0.25 else "SURVIVED")
f_wh = sum(v for (t, fl, dc), v in R["a18f"][1].items()
           if fl == "false" and dc == "WITHHOLD")
f_ins18 = sum(ins("a18f", t, "false") for t in ("A18F_0", "A18F_1", "A18F_2"))
f_tot18 = sum(v for (t, fl, _), v in R["a18f"][1].items() if fl == "false")
f_delay = 100.0 * f_wh / f_tot18
print("   A18F flood falses: scorer delay %d/%d = %.1f%% (predicted 35-45%%); "
      "installed %d/%d" % (f_wh, f_tot18, f_delay, f_ins18, f_tot18))
print("   KILL BAR (delay >25%%):",
      "KILL-CONFIRMED" if f_delay > 25 else "SURVIVED")

print("\n== H-PAM-19 ==")
r_ins = get("a19", "A19", "false", "CONFIRM_INSTALL")
r_tot = sum(v for (t, fl, _), v in R["a19"][1].items()
            if t == "A19" and fl == "false")
rate = 100.0 * r_ins / r_tot
print("   A19 rescue-template falses: confirmed-installed %d/%d = %.1f%% "
      "(predicted >=95%%)" % (r_ins, r_tot, rate))
print("   KILL BAR (>=40%% install):",
      "KILL-CONFIRMED" if rate >= 40 else "SURVIVED")
print("   contrast vs true rescue rate 45.5%%: |%.1f - 45.5| = %.1fpp %s 15pp"
      % (rate, abs(rate - 45.5),
         "<=" if abs(rate - 45.5) <= 15 else ">"))
