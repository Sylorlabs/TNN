#!/usr/bin/env python3
"""sweep_guards.py — simulate candidate guards on the frozen D1 battery.

Candidates (guard = margin ARM(400) AND span-arm AND <temporal replacement>):
  T0: dseq >= 20                       (frozen MG6 control)
  T1: (no temporal arm)                (ceiling probe)
  T2lo: dseq >= 2                      (threshold)
  T2hi: dseq >= 6                      (threshold)
  T3: C_range >= 20                    (set-level statistic; C = same-(tcode,jcode)
                                       history + pair, 20 = frozen MG4 constant)
  T4: |C| >= 3                         (historical-mass arm: >=1 prior trial
                                       outside the pair)

Full stack: frozen gate + candidate guard + frozen H6. Reports per candidate:
false installs (all legs), leg1 true retention. This is the preregistration
simulation; the Zag battery must reproduce it exactly.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/pam_round3/mg6_temporal")
from analyze_geometry import (streams, gtags, run_stream, gate_step, harden,
                              TOLS, D_CHAL, D_PROV, D_REV, D_PERM, D_WITH)

V2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2"
# leg1/leg4_withhold truth: rec_withhold.records ONLY (fixture names collide
# across record files; gen_d1.py sourced leg1 from withhold records).
rec_truth = {}
for line in open(V2 + "/redteam/evidence/rec_withhold.records"):
    f = line.rstrip("\n").split("|")
    rec_truth[f[2]] = (f[5], f[10])  # fixture -> (judgment, truth)
# leg2/leg4_install truth
rec_truth_install = {}
for line in open(V2 + "/redteam/evidence/rec_install.records"):
    f = line.rstrip("\n").split("|")
    rec_truth_install[f[2]] = (f[5], f[10])
# leg4_clean / leg4_decoy truth
rec_truth_clean = {}
for line in open(V2 + "/redteam/evidence/rec_clean.records"):
    f = line.rstrip("\n").split("|")
    rec_truth_clean[f[2]] = (f[5], f[10])
rec_truth_decoy = {}
for line in open(V2 + "/redteam/evidence/rec_decoy.records"):
    f = line.rstrip("\n").split("|")
    rec_truth_decoy[f[2]] = (f[5], f[10])

def truth_for(sname, t):
    if sname in ("leg1", "leg4_withhold"):
        return rec_truth[t["fixture"]]
    if sname in ("leg2", "leg4_install"):
        return rec_truth_install[t["fixture"]]
    if sname == "leg4_clean":
        return rec_truth_clean[t["fixture"]]
    if sname == "leg4_decoy":
        return rec_truth_decoy[t["fixture"]]
    raise KeyError(sname)

def mg6_margin_span(pair):
    s, tt = pair[0]["t"], pair[1]["t"]
    arms = []
    if min(s["mrgF"], tt["mrgF"]) < 400:
        arms.append("margin")
    if s["span_a"] < tt["span_b"] and tt["span_a"] < s["span_b"]:
        arms.append("span")
    return arms

def run_with_hist(trials, gtags, guard_fn):
    """Full stack; guard_fn(pair, Cseqs) -> arms. Cseqs = sorted seqs of
    same-(tcode,jcode) history (before incoming) + pair seqs."""
    states = {}
    hist = []
    full_hist = []
    out = []
    for ti, t in enumerate(trials):
        tc = t["tcode"]
        st = states.setdefault(tc, {"prov": None, "perm": None, "chal": None})
        tag = gtags[ti]
        snap = list(full_hist)
        disp, detail, pair = gate_step(st, t, tag)
        install = 0
        if disp in ("PROPOSE_PERM", "PROPOSE_REV"):
            is_rev = (disp == "PROPOSE_REV")
            s, inc = pair[0]["t"], pair[1]["t"]
            # C = DISTINCT seqs of same-(tcode,jcode) trials in history + pair
            Cseqs = sorted(set([h["seq"] for h in snap
                                if h["tcode"] == tc and h["jcode"] == t["jcode"]]
                               + [s["seq"], inc["seq"]]))
            arms = guard_fn(pair, Cseqs)
            if arms:
                disp = D_CHAL if is_rev else D_PROV
                detail = "guard-veto:" + "+".join(arms)
            else:
                ok, hdetail = harden(pair, is_rev, hist, st["perm"], tc)
                if ok:
                    st["perm"] = {"t": pair[1]["t"], "tag": pair[1]["tag"]}
                    st["prov"] = None
                    st["chal"] = None
                    disp = D_REV if is_rev else D_PERM
                    detail = hdetail
                    install = 1
                else:
                    disp = D_WITH
                    detail = hdetail
        out.append((ti, disp, detail, install))
        hist.append((tc, t["jcode"], t["prog"], t["meas"]))
        full_hist.append(t)
    return out

def mk_guard(name):
    def g(pair, Cseqs):
        arms = mg6_margin_span(pair)
        s, tt = pair[0]["t"], pair[1]["t"]
        dseq = abs(s["seq"] - tt["seq"])
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
    g.__name__ = name
    return g

CANDS = ["T0", "T1", "T2lo", "T2hi", "T3", "T4"]

def truth_of(t):
    # leg3 trials have no fixture in rec_truth; use judgment==truth map from gen_guard
    if t["fixture"] in rec_truth:
        j, tru = rec_truth[t["fixture"]]
        return j, tru
    return None, None

# leg3 truth from frozen gen_guard rows: truth field index 7
import frozen_gen_guard as G
leg3_truth = {}
for (cn, rows, cfj, pre, nh, sc) in G.CELLS:
    if cn.startswith("CC1-V") or cn in ("CC2-W1", "CC2-W2", "C1-W3"):
        continue
    sname = "leg3_" + cn
    for ri, row in enumerate(rows):
        leg3_truth[(sname, ri)] = (str(row[2]), str(row[7]))  # (jcode, truth)

print("cand | false_installs (legs1-4) | leg1 true retention | leg1 installs detail")
for c in CANDS:
    gf = mk_guard(c)
    total_false = 0
    false_list = []
    leg1_ret = leg1_true = 0
    leg1_detail = []
    for sname, trials in streams.items():
        out = run_with_hist(trials, gtags[sname], gf)
        for (ti, disp, detail, inst) in out:
            if not inst:
                continue
            t = trials[ti]
            if sname.startswith("leg3_"):
                jj, tru = leg3_truth[(sname, ti)]
                is_false = (jj != tru)
            else:
                j, tru = truth_for(sname, t)
                is_false = (j != tru)
            if is_false:
                total_false += 1
                false_list.append((sname, ti, t["seq"]))
            if sname == "leg1":
                j, tru = rec_truth[t["fixture"]]
                leg1_detail.append((ti, t["seq"], "FALSE" if j != tru else "true",
                                    disp, detail))
    # retention: true candidates installed
    for ti, t in enumerate(streams["leg1"]):
        j, tru = truth_for("leg1", t)
        if j == tru:
            leg1_true += 1
    out1 = run_with_hist(streams["leg1"], gtags["leg1"], gf)
    for (ti, disp, detail, inst) in out1:
        if inst:
            j, tru = truth_for("leg1", streams["leg1"][ti])
            if j == tru:
                leg1_ret += 1
    print("%-4s | false=%d %s | retention %d/%d | %s" % (
        c, total_false, false_list, leg1_ret, leg1_true, leg1_detail))
