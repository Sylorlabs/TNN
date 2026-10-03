#!/usr/bin/env python3
"""set_stats.py — compute candidate set-level statistics for the 7 leg1 proposals.

For each proposal, using only guard-visible info (trial fields + history,
never truth/jG/confG): various statistics a replacement temporal/independence
arm could use. Goal: find ANY statistic separating the 4 true from the 3 false.
"""
import sys
sys.path.insert(0, "/home/hatch/workspace/pam_round3/mg6_temporal")
from analyze_geometry import (streams, gtags, run_stream, guard_arms)

V2 = "/home/hatch/workspace/tnn-lab/senses/pam-rebuild/v2"
rec_info = {}
for line in open(V2 + "/redteam/evidence/rec_withhold.records"):
    f = line.rstrip("\n").split("|")
    rec_info[f[2]] = (f[5], f[10], int(f[6]))

def run_with_history(trials, gtags, guard_fn):
    """Like run_stream but also returns per-trial history snapshot."""
    from analyze_geometry import gate_step, harden, TOLS
    from analyze_geometry import D_CHAL, D_PROV, D_REV, D_PERM, D_WITH
    states = {}
    hist = []  # (tcode, jcode, prog, meas)
    full_hist = []  # trial dicts
    out = []
    for ti, t in enumerate(trials):
        tc = t["tcode"]
        st = states.setdefault(tc, {"prov": None, "perm": None, "chal": None})
        tag = gtags[ti]
        # snapshot history BEFORE this trial
        snap = list(full_hist)
        disp, detail, pair = gate_step(st, t, tag)
        install = 0
        prop_info = None
        if disp in ("PROPOSE_PERM", "PROPOSE_REV"):
            is_rev = (disp == "PROPOSE_REV")
            arms = guard_fn(pair)
            prop_info = (pair, arms, is_rev, snap)
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
        out.append((ti, disp, detail, install, prop_info))
        hist.append((tc, t["jcode"], t["prog"], t["meas"]))
        full_hist.append(t)
    return out

out = run_with_history(streams["leg1"], gtags["leg1"], guard_arms)
print("proposal set-level statistics (guard-visible only):")
print("idx true? kind | |C| C_range | #jcode_last10 | conf_pair | meas_gap_pair")
for (ti, disp, detail, inst, pinfo) in out:
    if pinfo is None:
        continue
    pair, arms, is_rev, snap = pinfo
    s, inc = pair[0]["t"], pair[1]["t"]
    tc, jc = inc["tcode"], inc["jcode"]
    # C = same-(tcode,jcode) trials in history (before incoming) + pair
    C = [h for h in snap if h["tcode"] == tc and h["jcode"] == jc]
    Cseqs = sorted(h["seq"] for h in C) + [s["seq"], inc["seq"]]
    Crange = max(Cseqs) - min(Cseqs)
    # distinct jcodes in last 10 trials of history
    last10 = snap[-10:]
    nj = len(set(h["jcode"] for h in last10))
    # conf of pair
    sj, stru, sconf = rec_info[s["fixture"]]
    ij, itru, iconf = rec_info[inc["fixture"]]
    tru = "T" if itru == ij else "F"
    print("idx %2d %s %-4s | |C|=%2d range=%3d | nj10=%d | conf=(%d,%d) | dmeas=%d" % (
        ti, tru, "REV" if is_rev else "PERM",
        len(Cseqs), Crange, nj, s["conf"], inc["conf"],
        abs(s["meas"] - inc["meas"])))
