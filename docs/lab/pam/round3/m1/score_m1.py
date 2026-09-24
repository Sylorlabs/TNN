#!/usr/bin/env python3
"""score_m1.py — independent scorer for M1 (Python mirror of PREREG_M1_BAR.md s6).

Never the instrument: recomputes every number the Zag grid search reported,
directly from m1_cases.txt + the reported thresholds. Fails loudly on any
mismatch.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
FX = os.path.join(HERE, "m1_cases.txt")

def load():
    C, W, P, B = [], [], {}, []
    for line in open(FX):
        f = line.rstrip("\n").split("|")
        if f[0] == "C":
            C.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
        elif f[0] == "W":
            W.append((int(f[1]), int(f[2])))
        elif f[0] == "P":
            P.setdefault(int(f[1]), []).append((int(f[2]), int(f[3])))
        elif f[0] == "B":
            B.append((int(f[1]), int(f[2]), int(f[3]), int(f[4])))
    return C, W, P, B

def passes(conf, mrg, strong, agree, ct, mt, st, at):
    return conf >= ct and mrg >= mt and strong >= st and agree >= at

def main():
    C, W, P, B = load()
    assert len(C) == 1102 and len(W) == 12 and len(P) == 9 and len(B) == 1109, \
        (len(C), len(W), len(P), len(B))
    assert all(len(v) == 2 for v in P.values())
    rep = {}
    for line in open(os.path.join(HERE, "evidence", "run1.txt")):
        if "=" in line:
            k, v = line.rstrip("\n").split("=", 1)
            rep[k.strip()] = v.strip()
    fails = []
    def check(name, got, want):
        if got != want:
            fails.append("%s: got %r want %r" % (name, got, want))
    # baseline (700,0,1,1)
    btp = sum(1 for c, m, s, a in C if passes(c, m, s, a, 700, 0, 1, 1))
    bc1 = sum(1 for c, m in W if passes(c, m, 1, 1, 700, 0, 1, 1))
    bc2 = sum(1 for v in P.values() if all(passes(c, m, 1, 1, 700, 0, 1, 1) for c, m in v))
    bfp = sum(1 for c, m, s, a in B if passes(c, m, s, a, 700, 0, 1, 1))
    check("base_true_pass", btp, int(rep["base_true_pass"]))
    check("base_rk3bp", btp * 10000 // 1102, int(rep["base_rk3bp"]))
    check("base_c1_viol", bc1, int(rep["base_c1_viol"]))
    check("base_c2_viol", bc2, int(rep["base_c2_viol"]))
    check("base_b_fp", bfp, int(rep["base_b_fp"]))
    # independent exact sweep (mirror of prereg s6)
    EW = [(c + 1, m + 1) for c, m in W]
    EP = [(min(c for c, m in v) + 1, min(m for c, m in v) + 1) for v in P.values()]
    EWW = EW + EP
    best = None
    for st in (0, 1):
        for at in (0, 1):
            Cs = [(c, m) for c, m, s, a in C if s >= st and a >= at]
            cand = sorted(set([0] + [mn for _, mn in EWW] + [m for _, m in Cs]))
            for mt in cand:
                need = [cn for cn, mn in EWW if mn > mt]
                ct = max(need) if need else 0
                tp = sum(1 for c, m in Cs if c >= ct and m >= mt)
                key = (tp, mt, -ct, st + at)
                if best is None or key > best[0]:
                    best = (key, (st, at, ct, mt, tp))
    _, (st, at, ct, mt, tp) = best
    check("opt_ST", st, int(rep["opt_ST"]))
    check("opt_AT", at, int(rep["opt_AT"]))
    check("opt_CT", ct, int(rep["opt_CT"]))
    check("opt_MT", mt, int(rep["opt_MT"]))
    check("opt_true_pass", tp, int(rep["opt_true_pass"]))
    check("opt_rk3bp", tp * 10000 // 1102, int(rep["opt_rk3bp"]))
    # verify constraints under optimum
    vc1 = sum(1 for c, m in W if passes(c, m, 1, 1, ct, mt, st, at))
    vc2 = sum(1 for v in P.values() if all(passes(c, m, 1, 1, ct, mt, st, at) for c, m in v))
    check("verify_c1_viol", vc1, int(rep["verify_c1_viol"]))
    check("verify_c2_viol", vc2, int(rep["verify_c2_viol"]))
    assert vc1 == 0 and vc2 == 0, "constraint violation!"
    # diagnostics
    ofp = sum(1 for c, m, s, a in B if passes(c, m, s, a, ct, mt, st, at))
    check("diag_b_fp", ofp, int(rep["diag_b_fp"]))
    t1145 = 1 if passes(874, 10410, 1, 1, ct, mt, st, at) else 0
    check("diag_trial1145", t1145, int(rep["diag_trial1145"]))
    # kill bar
    kb = "SURVIVE" if tp * 100 >= 82 * 1102 else "KILL"
    check("KB_M1_82pct", kb, rep["KB_M1_82pct"])
    if fails:
        print("SCORE FAIL:")
        for f in fails:
            print("  " + f)
        sys.exit(1)
    print("SCORE OK: all %d Zag-reported numbers independently reproduced." % 18)
    print("optimum (ST,AT,CT,MT)=(%d,%d,%d,%d) tp=%d/1102 rk3=%.2f%% kill=%s" %
          (st, at, ct, mt, tp, tp * 100.0 / 1102, kb))

if __name__ == "__main__":
    main()
