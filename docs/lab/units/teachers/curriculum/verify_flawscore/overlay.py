#!/usr/bin/env python3
# overlay.py — C5 manifest-rule scoring overlay.
# Reads flawscore_run's W7_FLAW lines (verdict ints) and applies the SEALED
# MANIFEST's near-miss rule (T-5 confirmed per W-05), which the frozen battery
# does NOT implement (battery: same-verdict/different-reason only):
#   wrong-span (k=0..3):    expected REVISE/SPAN_SHIFT; near = REJECT/R1
#   false-confidence (k=4..7): expected REJECT/R1;       near = REVISE/*
#   missing-grounding (k=8,9): expected REJECT/R1;       near = DEFER
#   plausible-false (k=10,11): expected REJECT/R1;       near = REVISE/SPAN_SHIFT
# Verdicts: 1=ADOPT 2=REVISE 3=REJECT 4=DEFER; reasons: 1=R1 11=SPAN_SHIFT.
# Also counts strict task-bar hits (>=10/12 hits) and prints both rules' lines.
import sys, glob, os

def near_credit(k, v, r):
    if k <= 3:
        return 0.5 if (v == 3 and r == 1) else 0.0
    if k <= 7:
        return 0.5 if v == 2 else 0.0
    if k <= 9:
        return 0.5 if v == 4 else 0.0
    return 0.5 if (v == 2 and r == 11) else 0.0

def expected(k):
    if k <= 3: return (2, 11)
    return (3, 1)

print("slice,hits,nears_battery,score_battery_x10,pass_battery,hits_manifest,nears_manifest,score_manifest_x10,strict_bar_10of12")
for path in sorted(glob.glob(os.path.join(sys.argv[1], 'verdict_S*.txt'))):
    sidx = os.path.basename(path).split('_S')[1].split('.')[0]
    flaws = {}
    for line in open(path):
        line = line.strip()
        if not line.startswith('W7_FLAW'): continue
        f = dict(p.split('=', 1) for p in line.split(',')[1:])
        k = int(f['flaw']); v, r = int(f['got'].split('/')[0]), int(f['got'].split('/')[1])
        flaws[k] = (v, r)
    hits = nears_b = nears_m = 0
    score_b = score_m = 0.0
    for k in range(12):
        v, r = flaws[k]
        ev, er = expected(k)
        if v == ev and r == er:
            hits += 1; score_b += 1.0; score_m += 1.0
        else:
            if v == ev: nears_b += 1; score_b += 0.5
            nc = near_credit(k, v, r)
            if v == ev and r != er:
                nears_m += 1; score_m += 0.5
            elif nc > 0:
                nears_m += 1; score_m += 0.5
    stat = [l for l in open(path) if l.startswith('W7_STAT')][0].strip()
    f2 = dict(p.split('=', 1) for p in stat.split(',')[1:])
    strict = 'PASS' if hits >= 10 else 'FAIL'
    print(f"{sidx},{hits},{nears_b},{int(round(score_b*10))},{f2['pass']},{hits},{nears_m},{int(round(score_m*10))},{strict}")
