#!/usr/bin/env python3
"""score_guard.py — scorer for the CC1 margin-guard battery (glue only).

Reads a guard_bin stdout file and:
  1. Fidelity check: per-trial dispositions vs EXPECT_GUARD.tsv, per-cell
     final state vs EXPECT_GUARD_CELL.tsv (both generated from the frozen
     prereg). Exit 0 iff every (cell, config) matches.
  2. Kill-bar evaluation (computed INDEPENDENTLY from run output +
     gen_guard.py cell metadata, not from EXPECT): K1..K4 per candidate.
     K5 (byte-identity) is checked externally via sha256 of the run files.

Usage: python3 score_guard.py evidence/run1.txt .
"""
import sys
sys.path.insert(0, ".")
from gen_guard import (CELLS, CONFIGS, CC1_FAMILY, THROUGHPUT_CELLS,
                       REGRESSION_CELLS, GUARD_CONFIGS)

DISP = {0:"PERM",1:"PROV",2:"CORR",3:"CONF",4:"CHAL",5:"REV",6:"ACC",7:"WITH"}
INSTALLS = {0,1,2,4,5,6}
META = {c[0]: c for c in CELLS}  # name -> (name, trials, cfj, pre, no_hist, scored)

def correct_j(name, cfg):
    cfj = META[name][2]
    if cfj == "G1N_G2Z":
        return None if cfg != "G2" else 0
    return cfj

def load_exp(path):
    exp = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("cell"):
            continue
        c, g, t, d = line.split("\t")
        exp.setdefault((c, g), {})[int(t)] = int(d)
    return exp

def load_exp_cell(path):
    exp = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("cell"):
            continue
        c, g, fj, fi, ni = line.split("\t")
        exp[(c, g)] = (int(fj), int(fi), int(ni))
    return exp

def load_run(path):
    got = {}
    for line in open(path):
        line = line.strip()
        if not line.startswith("GUARD|"):
            continue
        _, c, g, t, d, pj, ps = line.split("|")
        got.setdefault((c, g), {})[int(t)] = (int(d), int(pj), int(ps))
    return got

def false_install(cell, cfg, trials):
    # REV/ACC occurred AND final permanent jcode != correct final jcode
    cj = correct_j(cell, cfg)
    seq = [trials[t][0] for t in sorted(trials)]
    last = max(trials)
    afj = trials[last][1]
    rev_or_acc = any(d in (5, 6) for d in seq)
    if cj is None:
        return 0
    return 1 if (rev_or_acc and afj != cj) else 0

def main():
    run = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else "."
    exp = load_exp(base + "/EXPECT_GUARD.tsv")
    expc = load_exp_cell(base + "/EXPECT_GUARD_CELL.tsv")
    got = load_run(run)

    # ---- 1. fidelity check ----
    fails = 0
    total = 0
    print("=== fidelity: expected vs actual per (cell, config) ===")
    print("cell     cfg  | expected seq        | actual seq          | final exp/act | fi exp/act | installs | verdict")
    for (c, g) in sorted(got):
        total += 1
        eseq = [exp[(c, g)][t] for t in sorted(exp[(c, g)])]
        aseq = [got[(c, g)][t][0] for t in sorted(got[(c, g)])]
        efj, efi, eni = expc[(c, g)]
        last = max(got[(c, g)])
        afj = got[(c, g)][last][1]
        afi = false_install(c, g, got[(c, g)])
        ains = sum(1 for t in got[(c, g)] if got[(c, g)][t][0] in INSTALLS)
        ok = (eseq == aseq) and (afi == efi) and (afj == efj) and (ains == eni)
        if c == "W1":
            ok = ok and (ains == 0)
        if not ok:
            fails += 1
        es = ",".join(DISP[d] for d in eseq)
        as_ = ",".join(DISP[d] for d in aseq)
        print("%-8s %-4s | %-20s | %-20s | %3d / %-3d      | %d / %d     | %-8d | %s" % (
            c, g, es, as_, efj, afj, efi, afi, ains, "PASS" if ok else "FAIL"))
    print("fidelity: %d/%d (cell, config) PASS" % (total - fails, total))

    # ---- 2. kill bars (independent of EXPECT) ----
    print()
    print("=== kill bars per candidate (K1..K4; K5 checked externally) ===")
    results = {}
    for g in GUARD_CONFIGS:
        # K1: zero false installs across the scored CC1 family
        k1_bad = [c for c in CC1_FAMILY if false_install(c, g, got[(c, g)]) != 0]
        # K2: correct REVISED_INSTALL in 5/5 throughput cells
        k2_bad = []
        for c in THROUGHPUT_CELLS:
            trials = got[(c, g)]
            seq = [trials[t][0] for t in sorted(trials)]
            last = max(trials)
            afj = trials[last][1]
            if not (5 in seq and afj == correct_j(c, g)):
                k2_bad.append(c)
        # K3: C3 no REV/ACC, sequence PROV,PERM,CHAL
        c3seq = [got[("C3", g)][t][0] for t in sorted(got[("C3", g)])]
        k3_ok = (5 not in c3seq and 6 not in c3seq and c3seq == [1, 0, 4])
        # K4: regression cells identical to unguarded G1
        k4_bad = [c for c in REGRESSION_CELLS
                  if [got[(c, g)][t][0] for t in sorted(got[(c, g)])] !=
                     [got[(c, "G1")][t][0] for t in sorted(got[(c, "G1")])]]
        k1_ok = (len(k1_bad) == 0)
        k2_ok = (len(k2_bad) == 0)
        k4_ok = (len(k4_bad) == 0)
        verdict = "SURVIVE" if (k1_ok and k2_ok and k3_ok and k4_ok) else "KILL"
        results[g] = verdict
        print("%s: K1 %s%s | K2 %s%s | K3 %s | K4 %s%s => %s" % (
            g,
            "PASS" if k1_ok else "FAIL", "" if k1_ok else str(k1_bad),
            "PASS" if k2_ok else "FAIL", "" if k2_ok else str(k2_bad),
            "PASS" if k3_ok else "FAIL",
            "PASS" if k4_ok else "FAIL", "" if k4_ok else str(k4_bad),
            verdict))
    # V9 ceiling probe (reported, unscored)
    print()
    print("=== V9 ceiling probe (unscored; reported only) ===")
    for g in ["G1", "G2"] + GUARD_CONFIGS:
        fi = false_install("CC1-V9", g, got[("CC1-V9", g)])
        print("CC1-V9 %-4s false_install=%d" % (g, fi))
    print()
    print("summary: fidelity %d/%d; kill bars: %s" % (
        total - fails, total,
        ", ".join("%s=%s" % (g, v) for g, v in results.items())))
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
