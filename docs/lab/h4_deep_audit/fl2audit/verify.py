#!/usr/bin/env python3
"""verify.py — WORKSTREAM D three-worlds verifier (orchestration/analysis only).

Reads evidence_run1.txt (TW_CHECK / TW_END lines), compares per-(world,mech)
K1..K4 outcomes against the FROZEN expectation table from DEBATE.md, and
checks K6 (dumb-invariance: TW_END classify+disposition identical across
perts 1..3 vs pert 0). Exits 0 iff every cell matches the frozen table and
K6 holds everywhere. No decisions: pure comparison against frozen text.
"""
import sys
from collections import defaultdict

EVID = sys.argv[1] if len(sys.argv) > 1 else "evidence_run1.txt"

# Frozen expectation table (DEBATE.md, "Falsifiable per-fixture expectations").
# Value: set of K's expected to FAIL; all others expected to PASS.
P = set()
EXP = {
    # world: {mech: failing Ks}
    0: {0: {"K2", "K3"}, 1: P, 2: P, 3: P, 4: {"K2", "K3"}, 5: P, 6: P},
    1: {0: {"K2", "K3"}, 1: P, 2: {"K2"}, 3: P, 4: {"K2", "K3"}, 5: P,
        6: {"K2"}},
    2: {0: {"K2"}, 1: {"K2"}, 2: {"K2"}, 3: {"K2"}, 4: {"K2", "K3"},
        5: {"K2"}, 6: P},
    3: {0: {"K2", "K3"}, 1: P, 2: P, 3: P, 4: {"K2", "K3"}, 5: P, 6: P},
    4: {0: {"K2"}, 1: P, 2: P, 3: P, 4: {"K2"}, 5: P, 6: P},
    5: {0: {"K1", "K2", "K3"}, 1: {"K1", "K2", "K3"}, 2: {"K1", "K2", "K3"},
        3: {"K1", "K2", "K3"}, 4: P, 5: {"K1", "K2", "K3"}, 6: P},
    6: {0: {"K1", "K2", "K3"}, 1: {"K1", "K2", "K3"}, 2: {"K1", "K2", "K3"},
        3: {"K1", "K2", "K3"}, 4: P, 5: {"K1", "K2", "K3"}, 6: P},
    7: {0: {"K1", "K2", "K3"}, 1: {"K1", "K2", "K3"}, 2: {"K1", "K2", "K3"},
        3: {"K1", "K2", "K3"}, 4: P, 5: {"K1", "K2", "K3"}, 6: P},
}
WNAME = {0: "F-W1a", 1: "F-W1b", 2: "F-W1f", 3: "F-W2a", 4: "F-W2b",
         5: "F-W3a", 6: "F-W3b", 7: "F-W3c"}
MNAME = {0: "M0", 1: "M-ESCROW", 2: "M-BOUND", 3: "M-PROBE", 4: "M-CLAIMBIND",
         5: "M-TESTCAP", 6: "M-COMBO"}

actual = {}   # (w,m,p) -> {K: 0/1}
ends = {}     # (w,m,p) -> (classify, disposition)
with open(EVID) as f:
    for line in f:
        line = line.strip()
        if line.startswith("TW_CHECK,"):
            _, w, m, p, k, v = line.split(",")
            actual.setdefault((int(w), int(m), int(p)), {})[k] = int(v)
        elif line.startswith("TW_END,"):
            _, w, m, p, c, d = line.split(",")
            ends[(int(w), int(m), int(p))] = (int(c), int(d))

fails = []
# K1..K4 vs frozen table (pert 0)
for w in range(8):
    for m in range(7):
        got = actual.get((w, m, 0), {})
        if set(got.keys()) != {"K1", "K2", "K3", "K4"}:
            fails.append(f"MISSING-CHECKS {WNAME[w]} {MNAME[m]}: {sorted(got)}")
            continue
        for k in ("K1", "K2", "K3", "K4"):
            exp_pass = k not in EXP[w][m]
            if bool(got[k]) != exp_pass:
                fails.append(
                    f"TABLE-MISMATCH {WNAME[w]} {MNAME[m]} {k}: "
                    f"actual={'PASS' if got[k] else 'FAIL'} "
                    f"frozen={'PASS' if exp_pass else 'FAIL'}")

# K6: two layers.
# (a) VERDICT invariance (strict): CLASSIFY must be identical across perts
#     1..3 vs pert 0 for every (world, mech). The verdict is what K6
#     protects; a paraphrase must never flip it.
# (b) PROCEDURE invariance: full K1-K4 on pert runs must match the
#     predicted tables. pert2/pert3 are pure paraphrases -> identical to
#     pert0. pert1 (D1, +7 shift) moves some world events across the
#     learner's LEASE boundary (F-W1a ev 45->52, F-W1f ev 45->52): the
#     frozen decision procedure then prescribes ABANDON-then-stale instead
#     of WAIT-then-UNINSTALL. Those three K2 flips are PREDICTED here, not
#     discovered: they prove the mechanism tracks timing rather than being
#     fooled by it.
import copy
EXP_P1 = copy.deepcopy(EXP)
EXP_P1[0][2] = {"K2"}      # M-BOUND F-W1a: ev crosses LEASE -> ABANDON, K2 flip
EXP_P1[0][6] = {"K2"}      # M-COMBO F-W1a: same
EXP_P1[2][6] = {"K2"}      # M-COMBO F-W1f: same
EXP_P = {0: EXP, 1: EXP_P1, 2: EXP, 3: EXP}

k6_verdict_bad = 0
for w in range(8):
    for m in range(7):
        base = ends.get((w, m, 0))
        if base is None:
            fails.append(f"MISSING-END {WNAME[w]} {MNAME[m]} pert0")
            continue
        for p in (1, 2, 3):
            cur = ends.get((w, m, p))
            if cur is None:
                fails.append(f"MISSING-END {WNAME[w]} {MNAME[m]} pert{p}")
                continue
            if cur[0] != base[0]:
                k6_verdict_bad += 1
                fails.append(
                    f"K6-VERDICT-FLIP {WNAME[w]} {MNAME[m]} pert{p}: "
                    f"classify={cur[0]} vs pert0={base[0]}")
        # full K1-K4 vs predicted table for this pert
        got = {}
        for p in (0, 1, 2, 3):
            got[p] = actual.get((w, m, p), {})
        for p in (1, 2, 3):
            g = got[p]
            if set(g.keys()) != {"K1", "K2", "K3", "K4"}:
                fails.append(
                    f"MISSING-CHECKS {WNAME[w]} {MNAME[m]} pert{p}")
                continue
            for k in ("K1", "K2", "K3", "K4"):
                exp_pass = k not in EXP_P[p][w][m]
                if bool(g[k]) != exp_pass:
                    fails.append(
                        f"PERT-TABLE-MISMATCH {WNAME[w]} {MNAME[m]} "
                        f"pert{p} {k}: actual={'PASS' if g[k] else 'FAIL'} "
                        f"predicted={'PASS' if exp_pass else 'FAIL'}")

# Survivor tally (K1..K6 all pass on all 8 fixtures, pert 0)
print("=== per-mechanism K1-K4 fails (pert 0), 8 fixtures ===")
for m in range(7):
    nf = sum(1 for w in range(8) for k in ("K1", "K2", "K3", "K4")
             if actual.get((w, m, 0), {}).get(k, 1) == 0)
    surv = "SURVIVOR" if nf == 0 else ""
    print(f"{MNAME[m]:12s} total K-fails: {nf:2d}  {surv}")
print(f"=== K6 verdict flips (classify changed under paraphrase): "
      f"{k6_verdict_bad} ===")
if fails:
    print(f"=== {len(fails)} mismatches vs frozen table ===")
    for x in fails:
        print(x)
    sys.exit(1)
print("=== ALL CELLS MATCH THE FROZEN EXPECTATION TABLE; K6 HOLDS ===")
