#!/usr/bin/env python3
"""score_m1_govlh.py — independent Python mirror of PREREG_M1_GOVLH.md sections 3-5.

Recomputes every number the Zag instrument reports, from the fixture +
frozen bars + frozen jitter. Never the instrument. Usage:
  score_m1_govlh.py <m1_govlh_cases.txt> <run1.txt>
Asserts the S=1 anchors (Round-3 reproduction), the section-3 partition
equality, and byte-equality of every reported key.
"""
import math
import sys

OPT = (0, 0, 705, 3588)
SAFE = (1, 1, 705, 3588)
BASE = (1, 1, 700, 0)
SCALES = (1, 10, 100)


def passes(conf, mrg, s, a, bar):
    st, at, ct, mt = bar
    return conf >= ct and mrg >= mt and s >= st and a >= at


def jit_c(r, k):
    return 0 if k == 0 else ((k * 2654435761 + r * 40503) % 7) - 3


def jit_m(r, k):
    return 0 if k == 0 else ((k * 40503 + r * 2654435761) % 7) - 3


def main():
    fx, run = sys.argv[1], sys.argv[2]
    rows = []  # (kind, fam, pid, conf, mrg, s, a, src)
    for ln in open(fx):
        f = ln.rstrip("\n").split("|")
        k = f[0]
        if k in ("C", "W", "B"):
            rows.append((k, 0, -1, int(f[1]), int(f[2]), int(f[3]), int(f[4]), 0))
        elif k == "P":
            rows.append((k, 0, int(f[1]), int(f[2]), int(f[3]), 1, 1, 0))
        elif k == "N":
            rows.append((k, int(f[1]), -1, int(f[2]), int(f[3]), int(f[4]),
                         int(f[5]), int(f[6])))
        elif k == "Q":
            rows.append((k, 4, int(f[1]), int(f[2]), int(f[3]), 1, 1, 1))
        else:
            raise AssertionError(k)
    R = {}
    R["rows_total"] = len(rows)
    for kk in ("C", "W", "P", "B", "N", "Q"):
        R["rows_" + kk] = sum(1 for r in rows if r[0] == kk)
    for fam in (1, 2, 3, 5):
        R["fam_N%d" % fam] = sum(1 for r in rows if r[0] == "N" and r[1] == fam)
    R["fam_N5real"] = sum(1 for r in rows
                          if r[0] == "N" and r[1] == 5 and r[7] == 0)
    R["npairs_P"] = len({r[2] for r in rows if r[0] == "P"})
    R["npairs_Q"] = len({r[2] for r in rows if r[0] == "Q"})
    assert (R["rows_C"], R["rows_W"], R["rows_P"], R["rows_B"]) == (1102, 12, 18, 1109)
    assert (R["fam_N1"], R["fam_N2"], R["fam_N3"], R["fam_N5"]) == (1, 311, 144, 404)
    assert R["fam_N5real"] == 400
    assert (R["npairs_P"], R["npairs_Q"]) == (9, 12)

    ex_o = [passes(c, m, s, a, OPT) for (_, _, _, c, m, s, a, _) in rows]

    for si, S in enumerate(SCALES):
        pre = "S%d_" % S if S < 100 else "S100_"
        tp_o = tp_s = 0
        w_o = w_s = 0
        b_o = b_s = b_b = 0
        n1_o = n1_s = n2_o = n2_s = n3_o = n3_s = n5_o = n5_s = 0
        hj_c = hj_w = 0
        pc_op = {}
        pc_sp = {}
        pc_oq = {}
        pc_sq = {}
        pi_o = pi_s = q_o = q_s = 0
        for k in range(S):
            for ri, (kind, fam, pid, c0, m0, s, a, src) in enumerate(rows):
                c = c0 + jit_c(ri, k)
                m = m0 + jit_m(ri, k)
                po = passes(c, m, s, a, OPT)
                ps = passes(c, m, s, a, SAFE)
                if kind == "C":
                    tp_o += po
                    tp_s += ps
                    if k > 0 and ex_o[ri] and not po:
                        hj_c += 1
                elif kind == "W":
                    w_o += po
                    w_s += ps
                elif kind == "P":
                    pc_op[pid] = pc_op.get(pid, 0) + po
                    pc_sp[pid] = pc_sp.get(pid, 0) + ps
                elif kind == "B":
                    b_o += po
                    b_s += ps
                    b_b += passes(c, m, s, a, BASE)
                elif kind == "N":
                    if fam == 1:
                        n1_o += po
                        n1_s += ps
                    elif fam == 2:
                        n2_o += po
                        n2_s += ps
                    elif fam == 3:
                        n3_o += po
                        n3_s += ps
                    elif fam == 5:
                        n5_o += po
                        n5_s += ps
                    if k > 0 and not ex_o[ri] and po:
                        hj_w += 1
                elif kind == "Q":
                    pc_oq[pid] = pc_oq.get(pid, 0) + po
                    pc_sq[pid] = pc_sq.get(pid, 0) + ps
            for pid, v in pc_op.items():
                if v == 2:
                    pi_o += 1
            for pid, v in pc_sp.items():
                if v == 2:
                    pi_s += 1
            for pid, v in pc_oq.items():
                if v == 2:
                    q_o += 1
            for pid, v in pc_sq.items():
                if v == 2:
                    q_s += 1
            pc_op.clear()
            pc_sp.clear()
            pc_oq.clear()
            pc_sq.clear()
        R[pre + "tp_opt"] = tp_o
        R[pre + "tp_safe"] = tp_s
        R[pre + "H_trial"] = tp_o - math.ceil(82 * 1102 * S / 100)
        R[pre + "W_fp_opt"] = w_o
        R[pre + "W_fp_safe"] = w_s
        R[pre + "P_inst_opt"] = pi_o
        R[pre + "P_inst_safe"] = pi_s
        R[pre + "B_fp_opt"] = b_o
        R[pre + "B_fp_safe"] = b_s
        R[pre + "B_fp_base"] = b_b
        R[pre + "N1_fp_opt"] = n1_o
        R[pre + "N1_fp_safe"] = n1_s
        R[pre + "N2_fp_opt"] = n2_o
        R[pre + "N2_fp_safe"] = n2_s
        R[pre + "N3_fp_opt"] = n3_o
        R[pre + "N3_fp_safe"] = n3_s
        R[pre + "N4_inst_opt"] = q_o
        R[pre + "N4_inst_safe"] = q_s
        R[pre + "N5_fp_opt"] = n5_o
        R[pre + "N5_fp_safe"] = n5_s
        if S >= 10:
            R[pre + "Hj_C_fragile"] = hj_c
            R[pre + "Hj_W_flip"] = hj_w

    # anchors: Round-3 reproduction at S=1
    assert R["S1_tp_opt"] == 910, R["S1_tp_opt"]
    assert R["S1_tp_safe"] == 671, R["S1_tp_safe"]
    assert R["S1_W_fp_opt"] == 0
    assert R["S1_P_inst_opt"] == 0
    assert R["S1_B_fp_opt"] == 712
    assert R["S1_B_fp_base"] == 7
    # partition (prereg section 3)
    assert R["fam_N1"] + R["fam_N2"] + R["fam_N5real"] == R["S1_B_fp_opt"]
    R["partition_ok"] = 1

    habs = 0
    while R["S1_tp_opt"] * 100 >= 82 * (1102 + habs + 1):
        habs += 1
    R["H_absorb"] = habs
    R["H_knife_conf705"] = sum(1 for ri, (kind, _, _, c, _, _, _, _) in enumerate(rows)
                               if kind == "C" and ex_o[ri] and c == 705)
    R["H_knife_mrg3588"] = sum(1 for ri, (kind, _, _, _, m, _, _, _) in enumerate(rows)
                               if kind == "C" and ex_o[ri] and m == 3588)

    # compare against the instrument output
    inst = {}
    for ln in open(run):
        ln = ln.rstrip("\n")
        if "=" in ln and not ln.startswith("M1_GOVLH"):
            kk, vv = ln.split("=", 1)
            inst[kk] = int(vv)
    missing = [kk for kk in R if kk not in inst]
    extra = [kk for kk in inst if kk not in R]
    mism = [(kk, R[kk], inst[kk]) for kk in R if kk in inst and R[kk] != inst[kk]]
    print("keys: mirror=%d instrument=%d" % (len(R), len(inst)))
    if missing:
        print("MISSING from instrument:", missing)
    if extra:
        print("EXTRA in instrument:", extra)
    if mism:
        for kk, a, b in mism:
            print("MISMATCH %s mirror=%s instrument=%s" % (kk, a, b))
    ok = not (missing or extra or mism)
    print("anchors OK; partition OK" if ok else "FAILED")
    # decision-grade summary
    print("--- summary ---")
    for S in SCALES:
        pre = "S%d_" % S if S < 100 else "S100_"
        print("%s tp_opt=%d H_trial=%d B_fp_opt=%d B_fp_safe=%d N1=%d/%d N2=%d/%d N3=%d/%d N5=%d/%d N4inst=%d/%d W=%d P_inst=%d" % (
            pre.rstrip("_"), R[pre + "tp_opt"], R[pre + "H_trial"],
            R[pre + "B_fp_opt"], R[pre + "B_fp_safe"],
            R[pre + "N1_fp_opt"], R[pre + "N1_fp_safe"],
            R[pre + "N2_fp_opt"], R[pre + "N2_fp_safe"],
            R[pre + "N3_fp_opt"], R[pre + "N3_fp_safe"],
            R[pre + "N5_fp_opt"], R[pre + "N5_fp_safe"],
            R[pre + "N4_inst_opt"], R[pre + "N4_inst_safe"],
            R[pre + "W_fp_opt"], R[pre + "P_inst_opt"]))
    print("H_absorb=%d H_knife_conf705=%d H_knife_mrg3588=%d" %
          (R["H_absorb"], R["H_knife_conf705"], R["H_knife_mrg3588"]))
    if S >= 10 or True:
        pass
    print("S10 Hj_C_fragile=%d Hj_W_flip=%d | S100 Hj_C_fragile=%d Hj_W_flip=%d" % (
        R["S10_Hj_C_fragile"], R["S10_Hj_W_flip"],
        R["S100_Hj_C_fragile"], R["S100_Hj_W_flip"]))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
