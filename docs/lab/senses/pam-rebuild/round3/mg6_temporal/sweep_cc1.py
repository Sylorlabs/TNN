#!/usr/bin/env python3
"""sweep_cc1.py — simulate candidate guards on the frozen CC1 battery.

Battery: 22 cells (frozen gen_guard.py CELLS), G1 gate (ported from frozen
guard_main.zag g1_step), guard consulted ONLY at the corroborated-revision
point (faithful to the CC1 battery). Candidates replace MG6's temporal arm.

Kill bars: 0/9 false installs on CC1_FAMILY, 5/5 installs on THROUGHPUT_CELLS.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/pam_round3/mg6_temporal")
import frozen_gen_guard as G

D_PERM, D_PROV, D_CORR, D_CONF, D_CHAL, D_REV, D_ACC, D_WITH = 0, 1, 2, 3, 4, 5, 6, 7

def tol_of(tc):
    return {0: 8, 1: 40, 2: 60, 3: 4000, 4: 120}.get(tc, 0)

# trial tuple: (tcode,prog,jcode,conf,pred,meas,mrgF,truth,jG,confG,seq,sa,sb)
def g1_cell(trials, pre, no_hist, guard_fn):
    # state: dict
    st = {"prov_on": 0, "prov_j": 0, "prov_m": 0,
          "perm_on": 0, "perm_j": 0, "perm_m": 0, "perm_conf": 0, "perm_seq": -1,
          "perm_mrg": 0,
          "chal_on": 0, "chal_j": 0, "chal_m": 0, "chal_mrg": 0,
          "chal_seq": 0, "chal_sa": 0, "chal_sb": 0}
    if pre is not None:
        st["perm_on"] = 1
        st["perm_j"], st["perm_m"], st["perm_conf"], st["perm_seq"] = pre
    # history of (seq, span_a) per (tcode,jcode) for set statistics
    hist = []
    out = []
    for ti, row in enumerate(trials):
        (tcode, prog, jc, cf, pred, meas, mrg, truth,
         jG, confG, seq, sa, sb) = row
        if prog != 0 or pred != 1:
            out.append((ti, D_WITH, None))
            hist.append((tcode, jc, seq, sa))
            continue
        tol = tol_of(tcode)
        disp, prop = None, None
        if st["perm_on"] and jc == st["perm_j"] and abs(meas - st["perm_m"]) <= tol:
            disp = D_CORR
        elif st["prov_on"] and not st["perm_on"] and jc == st["prov_j"] \
                and abs(meas - st["prov_m"]) <= tol:
            if cf >= 700:
                st.update(perm_on=1, perm_j=jc, perm_m=meas, perm_conf=cf,
                          perm_seq=ti, perm_mrg=mrg, prov_on=0)
                disp = D_PERM
            else:
                disp = D_PROV
        elif st["perm_on"] or st["prov_on"]:
            ij = st["perm_j"] if st["perm_on"] else st["prov_j"]
            if jc != ij:
                if cf >= 700 and no_hist == 0:
                    if st["chal_on"] and st["chal_j"] == jc \
                            and abs(meas - st["chal_m"]) <= tol:
                        # REVISION POINT: consult guard
                        Cseqs = sorted(set(
                            [h[2] for h in hist
                             if h[0] == tcode and h[1] == jc]
                            + [st["chal_seq"], seq]))
                        pair = {"m1": st["chal_mrg"], "m2": mrg,
                                "sa1": st["chal_sa"], "sb1": st["chal_sb"],
                                "sa2": sa, "sb2": sb,
                                "q1": st["chal_seq"], "q2": seq}
                        arms = guard_fn(pair, Cseqs)
                        prop = (pair, Cseqs, arms)
                        if arms:
                            disp = D_CHAL
                        else:
                            st.update(perm_on=1, perm_j=jc, perm_m=meas,
                                      perm_conf=cf, perm_seq=ti, perm_mrg=mrg,
                                      chal_on=0)
                            disp = D_REV
                    else:
                        st.update(chal_on=1, chal_j=jc, chal_m=meas,
                                  chal_mrg=mrg, chal_seq=seq, chal_sa=sa,
                                  chal_sb=sb)
                        disp = D_CHAL
                else:
                    disp = D_CONF
            else:
                st.update(prov_on=1, prov_j=jc, prov_m=meas)
                disp = D_PROV
        else:
            st.update(prov_on=1, prov_j=jc, prov_m=meas)
            disp = D_PROV
        out.append((ti, disp, prop))
        hist.append((tcode, jc, seq, sa))
    # final perm jcode
    pj = st["perm_j"] if st["perm_on"] else -1
    return out, pj

def mg_margin_span(pair):
    arms = []
    if min(pair["m1"], pair["m2"]) < 400:
        arms.append("margin")
    if pair["sa1"] < pair["sb2"] and pair["sa2"] < pair["sb1"]:
        arms.append("span")
    return arms

def mk_guard(name):
    def g(pair, Cseqs):
        arms = mg_margin_span(pair)
        dseq = abs(pair["q1"] - pair["q2"])
        if name == "T0":
            if dseq < 20:
                arms.append("temporal")
        elif name == "T1":
            pass
        elif name == "T2lo":
            if dseq < 2:
                arms.append("temporal")
        elif name == "T2hi":
            if dseq < 6:
                arms.append("temporal")
        elif name == "T3":
            if max(Cseqs) - min(Cseqs) < 20:
                arms.append("temporal")
        elif name == "T4":
            if len(Cseqs) < 3:
                arms.append("temporal")
        return arms
    return g

CANDS = ["T0", "T1", "T2lo", "T2hi", "T3", "T4"]

print("cand | CC1-family false installs | throughput installs | proposal arms")
for c in CANDS:
    gf = mk_guard(c)
    false_cells = []
    thr_installs = []
    prop_arms = {}
    for (name, trials, cfj, pre, no_hist, scored) in G.CELLS:
        out, pj = g1_cell(trials, pre, no_hist, gf)
        # false install: a REV/PERM install whose jcode != truth of installing trial
        for (ti, disp, prop) in out:
            if disp in (D_PERM, D_REV):
                tj = trials[ti][2]
                ttruth = trials[ti][7]
                if tj != ttruth and name in G.CC1_FAMILY:
                    false_cells.append((name, ti))
        if name in G.THROUGHPUT_CELLS:
            # throughput: the correct revision must install (disp REV at last trial)
            rev_ok = any(d == D_REV for (ti, d, p) in out)
            thr_installs.append((name, rev_ok))
        for (ti, disp, prop) in out:
            if prop is not None:
                pair, Cseqs, arms = prop
                prop_arms[name] = (ti, "+".join(arms) or "ALLOW",
                                   pair["q1"], pair["q2"], Cseqs)
    n_false = len(false_cells)
    n_thr = sum(1 for _, ok in thr_installs if ok)
    print("%-4s | false=%d %s | throughput %d/5 %s" % (
        c, n_false, false_cells, n_thr,
        [n for n, ok in thr_installs if not ok]))
    if c == "T0":
        for name in sorted(prop_arms):
            ti, arms, q1, q2, Cseqs = prop_arms[name]
            print("      %-8s trial %d arms=%-16s dseq=%d Cseqs=%s" % (
                name, ti, arms, abs(q1 - q2), Cseqs))
