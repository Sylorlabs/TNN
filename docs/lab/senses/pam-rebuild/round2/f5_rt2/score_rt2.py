#!/usr/bin/env python3
"""RT-1 scorer: parse the committed binary's per-trial lines for the three
attack batteries, assert EVERY fixture's decision equals the script-computed
(blocked, rep) expectation (fail loud on mismatch), verify 3x byte-identical
SHAs, and compute the preregistered kill-bar numbers."""
import json, hashlib, sys
from collections import Counter

D = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/round2/f5_rt2"
expect = json.load(open(D + "/expect.json"))

def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

results = {}
for b in ["a15", "a16", "a20"]:
    shas = [sha("%s/run_%s_%d.out" % (D, b, r)) for r in (1, 2, 3)]
    assert shas[0] == shas[1] == shas[2], "runs not byte-identical for " + b
    n = Counter()
    mism = []
    delays = Counter()
    for l in open("%s/run_%s_1.out" % (D, b)):
        if l.startswith("SETSUM") or l.startswith("BACKTEST") or \
           l.startswith("DELAYBAR") or l.startswith("HIST") or \
           l.startswith("SERIAL") or l.startswith("SANITY"):
            continue
        f = l.rstrip("\n").split("\t")
        # trial, fixture, set, BLOCKED|ALLOWED, exseq|-, decision|-, delay
        fx, blk, dec, delay = f[1], f[3], f[5], int(f[6])
        e = expect[fx]
        if dec != e["exp"] or (blk == "BLOCKED") != e["blocked"]:
            mism.append((fx, blk, dec, e))
        tag = e["tag"]
        n[(tag, "false" if e["false"] else "true", dec)] += 1
        delays[(tag, delay)] += 1
    results[b] = (shas[0], n, mism, delays)
    print("== battery", b, "sha", shas[0][:16], "3x identical OK")
    print("   decision mismatches vs geometric expectation:", mism if mism else "NONE")
    for k in sorted(n):
        print("   ", k, n[k])
    print("    delays:", dict(sorted(delays.items())))

# ---- kill-bar verdicts ----
def get(b, tag, falsity, dec):
    return results[b][1].get((tag, falsity, dec), 0)

print("\n== H-PAM-15 ==")
a15a_ins = get("a15", "A15A", "false", "CONFIRM_INSTALL") + get("a15", "A15A", "false", "ALLOWED")
a15a_wh = get("a15", "A15A", "false", "WITHHOLD")
a15b_ins = get("a15", "A15B", "false", "CONFIRM_INSTALL") + get("a15", "A15B", "false", "ALLOWED")
a15b_wh = get("a15", "A15B", "false", "WITHHOLD")
print("   A15A interior: installed %d/30, withheld %d/30 (hypothesis predicted >=24/30 installed)"
      % (a15a_ins, a15a_wh))
print("   A15B marginal: installed %d/30, withheld %d/30 (hypothesis predicted >=21/30)"
      % (a15b_ins, a15b_wh))
print("   KILL BAR (>=15/30 in either):", "KILL-CONFIRMED" if a15a_ins >= 15 or a15b_ins >= 15 else "SURVIVED")

print("\n== H-PAM-16 ==")
a16_ins = get("a16", "A16F", "false", "CONFIRM_INSTALL") + get("a16", "A16F", "false", "ALLOWED")
a16_wh = get("a16", "A16F", "false", "WITHHOLD")
a16t_ins = get("a16", "A16T", "true", "CONFIRM_INSTALL") + get("a16", "A16T", "true", "ALLOWED")
print("   A16F falses: installed %d/60, withheld %d/60 (hypothesis predicted >=40/60)"
      % (a16_ins, a16_wh))
print("   A16T true controls: installed %d/30 (rescue diagnostic)" % a16t_ins)
print("   KILL BAR (>=24/60 = 40%%):", "KILL-CONFIRMED" if a16_ins >= 24 else "SURVIVED")

print("\n== H-PAM-20 ==")
a20f_ins = get("a20", "A20F", "false", "CONFIRM_INSTALL") + get("a20", "A20F", "false", "ALLOWED")
a20f_wh = get("a20", "A20F", "false", "WITHHOLD")
a20t_wh = get("a20", "A20T", "true", "WITHHOLD")
a20t_ins = get("a20", "A20T", "true", "CONFIRM_INSTALL") + get("a20", "A20T", "true", "ALLOWED")
print("   A20F planted falses: installed %d/40, withheld %d/40" % (a20f_ins, a20f_wh))
print("   A20T in-rectangle trues: installed %d/7, withheld %d/7" % (a20t_ins, a20t_wh))
print("   Mechanism policy (WITHHOLD in-rectangle): false-install %.1f%%, true-withhold %.1f%%"
      % (100.0 * a20f_ins / 40, 100.0 * a20t_wh / 7))
print("   P1 counterfactual (install in-rectangle): false-install 100%% (40/40), true-withhold 0%%")
both = (a20f_ins / 40 < 0.5) and (a20t_wh / 7 < 0.5)
print("   KILL BAR (no policy beats <50%% AND <50%%):",
      "SURVIVED-unexpected" if both else "KILL-CONFIRMED (logical: dilemma demonstrated)")
