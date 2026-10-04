#!/usr/bin/env python3
"""PAM round-3 crew 5: score A15/A16/A20 batteries vs both organs.

For each (organ, battery): parse the 3 run outputs, assert SHA-identical,
assert EVERY fixture's decision equals the script-computed organ
expectation (from spec_extract_r3.py's organ functions — re-derived here
from the frozen spec, not copied from the binary), then report kill-bar
numbers. Any mismatch fails loud.
"""
import hashlib
import json
import sys
from collections import Counter

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_r3"

EXC = [(718, 2618), (704, 2642), (713, 2626), (701, 2647), (710, 2632),
       (713, 2627)]
TRUE_BOX = (650, 940, 2200, 6700)
TIGHT = (34, 58)
EPS = 5
MEM = set()
for ln in open(D + "/true_memory.tsv"):
    p = ln.rstrip("\n").split("\t")
    MEM.add((int(p[0]), int(p[1])))


def blocked(c, m):
    return any(abs(c - ec) <= 150 and abs(m - em) <= 2000 for ec, em in EXC)


def trap_tight(c, m):
    return any(abs(c - ec) <= TIGHT[0] and abs(m - em) <= TIGHT[1]
               for ec, em in EXC)


def organ_d(c, m):
    if not blocked(c, m):
        return "ALLOWED"
    if trap_tight(c, m):
        return "WITHHOLD"
    if TRUE_BOX[0] <= c <= TRUE_BOX[1] and TRUE_BOX[2] <= m <= TRUE_BOX[3]:
        return "CONFIRM_INSTALL"
    return "WITHHOLD"


def organ_r(c, m):
    if not blocked(c, m):
        return "ALLOWED"
    for c0 in range(c - EPS, c + EPS + 1):
        for m0 in range(m - EPS, m + EPS + 1):
            if (c0, m0) in MEM:
                return "CONFIRM_INSTALL"
    return "WITHHOLD"


ORGS = {"d": organ_d, "r": organ_r}
BATS = ["a15", "a16", "a20"]

report = {}
for org in ORGS:
    for bat in BATS:
        outs = []
        for i in (1, 2, 3):
            p = "%s/run_%s_%s_%d.out" % (D, org, bat, i)
            outs.append(open(p, "rb").read())
        h = [hashlib.sha256(o).hexdigest() for o in outs]
        assert h[0] == h[1] == h[2], (org, bat, h)
        dec = {}
        rc = None
        for ln in outs[0].decode().split("\n"):
            if not ln or ln.startswith(
                    ("SETSUM", "BACKTEST", "DELAYBAR", "HIST", "SERIAL",
                     "SANITY")):
                continue
            f = ln.split("\t")
            dec[f[1]] = (f[3], f[5])
        # every fixture vs script expectation
        fx_of = {}
        for ln in open("%s/attack/ledger_%s.txt" % (D, bat)):
            f = ln.rstrip("\n").split("|")
            fx_of[f[4]] = (int(f[8]), int(f[10]), f[7] != f[12])
        assert set(dec) == set(fx_of), (org, bat, "fixture mismatch")
        bad = []
        for fx, (c, m, isfalse) in fx_of.items():
            exp = ORGS[org](c, m)
            got = dec[fx][1] if dec[fx][0] == "BLOCKED" else "ALLOWED"
            if dec[fx][0] == "BLOCKED":
                got = dec[fx][1]
            else:
                got = "ALLOWED"
            if got != exp:
                bad.append((fx, c, m, exp, got))
        assert not bad, (org, bat, bad[:5])
        # kill-bar numbers
        falses = [(fx, dec[fx]) for fx, (c, m, isf) in fx_of.items() if isf]
        trues = [(fx, dec[fx]) for fx, (c, m, isf) in fx_of.items()
                 if not isf]
        fi = sum(1 for _, (b, d) in falses if d == "CONFIRM_INSTALL")
        tw = sum(1 for _, (b, d) in trues if d == "WITHHOLD")
        report[(org, bat)] = {
            "sha": h[0][:16],
            "n_false": len(falses),
            "false_install": fi,
            "n_true": len(trues),
            "true_withhold": tw,
        }

print("== RT-1 battery results (3x byte-identical, all fixtures match script expectations) ==")
for org in ORGS:
    for bat in BATS:
        r = report[(org, bat)]
        print("organ %s battery %s: falses %d/%d installed | trues %d/%d withheld | sha %s"
              % (org.upper(), bat, r["false_install"], r["n_false"],
                 r["true_withhold"], r["n_true"], r["sha"]))

print("== kill bars ==")
# H-15: >=15/30 per sub-battery kills
d15a = report[("d", "a15")]
# split a15 into A15A/A15B by fixture infix
for org in ORGS:
    for sub, tag in [("A15A", "A15A"), ("A15B", "A15B")]:
        outs = open("%s/run_%s_a15_1.out" % (D, org)).read()
        n = fi = 0
        for ln in outs.split("\n"):
            if "_%s_" % tag in ln and not ln.startswith(
                    ("SETSUM", "BACKTEST", "DELAYBAR", "HIST", "SERIAL",
                     "SANITY")) and ln:
                f = ln.split("\t")
                n += 1
                if f[5] == "CONFIRM_INSTALL":
                    fi += 1
        verdict = "KILL" if fi >= 15 else "survive"
        print("H-15 organ %s %s: %d/%d installed -> %s (bar >=15/30)"
              % (org.upper(), sub, fi, n, verdict))
# H-16: >=24/60 falses kills
for org in ORGS:
    r = report[(org, "a16")]
    verdict = "KILL" if r["false_install"] >= 24 else "survive"
    print("H-16 organ %s falses: %d/%d installed -> %s (bar >=24/60)"
          % (org.upper(), r["false_install"], r["n_false"], verdict))
# H-20: falsified unless false-install <50% AND true-withhold <50%
for org in ORGS:
    r = report[(org, "a20")]
    ffrac = r["false_install"] / r["n_false"]
    tfrac = r["true_withhold"] / r["n_true"] if r["n_true"] else 0
    verdict = "survive" if (ffrac < 0.5 and tfrac < 0.5) else "FALSIFIED"
    print("H-20 organ %s: false-install %d/%d=%.1f%% true-withhold %d/%d=%.1f%% -> %s"
          % (org.upper(), r["false_install"], r["n_false"], 100 * ffrac,
             r["true_withhold"], r["n_true"], 100 * tfrac, verdict))

json.dump({k[0] + "/" + k[1]: v for k, v in report.items()},
          open(D + "/score_rt1.json", "w"), indent=1, sort_keys=True)
print("score written to score_rt1.json")
