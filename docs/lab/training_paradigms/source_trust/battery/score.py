#!/usr/bin/env python3
"""Source-trust battery scorer (battery crew).

Reads driver audit ledgers + cost files + battery definitions, computes the
prereg section 6 metrics and bar verdicts per fork.

Usage: python3 score.py <streams_dir> <runs_dir> <fork_tag> <thresholds_json> <out_json>
  runs_dir contains <BAT>.ledger and <BAT>.cost for the fork.
Writes <out_json> with the full scorecard and prints a summary table.
"""
import sys, os, json, math

def parse_ledger(path):
    eps = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d = {}
            for tok in line.split(" "):
                k, _, v = tok.partition("=")
                d[k] = v
            eps.append({
                "ep": int(d["ep"]), "et": int(d["et"]), "src": int(d["src"]),
                "key": int(d["key"]), "val": int(d["val"]), "aux": int(d["aux"]),
                "gt": int(d["gt"]), "v": int(d["v"]), "w": d.get("w", "-"),
            })
    return eps

def parse_cost(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            d = {}
            for tok in line.split(" "):
                k, _, v = tok.partition("=")
                d[k] = v
            rows.append({"ep": int(d["ep"]), "et": int(d["et"]),
                         "ns": int(d["ns"]), "wlen": int(d["wlen"])})
    return rows

import re
TRUST_RES = {
    # fork's frozen warrant trust encoding -> regex with one capture group (milli)
    "k": r";t=(-?\d+)",
    "l": r"\|t=(\d+)\|",
    "s": None,      # structural fork: no scalar; ordering handled separately
    "floor": None,
}

def warrant_trust(w, fork):
    pat = TRUST_RES.get(fork)
    if not pat:
        return None
    m = re.search(pat, w)
    if m:
        return int(m.group(1)) / 1000.0
    return None

def warrant_order(w):
    # S convention: first line "ORDER=<src>,<src>,..."
    if w.startswith("ORDER="):
        rest = w[6:].split("_")[0]
        out = []
        for p in rest.split(","):
            if p.lstrip("-").isdigit():
                out.append(int(p))
        return out
    return None

def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return sxy / math.sqrt(sxx * syy)

def kendall_tau(a_rank, b_rank):
    # a_rank, b_rank: dict item -> rank position
    items = [k for k in a_rank if k in b_rank]
    n = len(items)
    if n < 2:
        return None
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            x, y = items[i], items[j]
            da = (a_rank[x] - a_rank[y])
            db = (b_rank[x] - b_rank[y])
            if da * db > 0:
                conc += 1
            elif da * db < 0:
                disc += 1
    tot = conc + disc
    return (conc - disc) / tot if tot else None

def installs(eps, pred):
    return [e for e in eps if e["et"] == 1 and e["v"] == 0 and pred(e)]

def score_st1(eps):
    prim = [e for e in eps if e["et"] == 1 and 1 <= e["aux"] <= 6]
    forg = [e for e in eps if e["et"] == 1 and 11 <= e["aux"] <= 16]
    ctrl = [e for e in eps if e["et"] == 1 and e["aux"] == 20]
    fi = sum(1 for e in prim if e["v"] == 0)
    ffi = sum(1 for e in forg if e["v"] == 0)
    ci = sum(1 for e in ctrl if e["v"] == 0)
    return {
        "false_installs_primary": fi, "n_primary": len(prim),
        "false_installs_forged": ffi, "n_forged": len(forg),
        "control_installs": ci, "n_controls": len(ctrl),
        "KB1_kill": fi >= 30,
        "bar_false_lt_baseline": fi < 60,
        "control_bar_ge_18": ci >= 18,
    }

def score_st2(eps):
    pairs = {}
    for e in eps:
        if e["et"] == 1 and 1 <= e["aux"] <= 5:
            pairs.setdefault(e["aux"], []).append(e)
    double = 0; handled = 0
    for pid, mem in pairs.items():
        inst = sum(1 for m in mem if m["v"] == 0)
        if inst >= 2:
            double += 1
        else:
            handled += 1
    return {"pairs": len(pairs), "double_installed": double,
            "handled": handled, "bar_ge_4_5": handled >= 4,
            "bar_fail_2plus_double": double >= 2}

def score_st3(eps):
    lies = [e for e in eps if e["et"] == 1 and 11 <= e["aux"] <= 15]
    lie_inst = sum(1 for e in lies if e["v"] == 0)
    # clampdown: after first lie's WORLD-disagree, subsequent lie installs
    worlds = [e for e in eps if e["et"] == 2]
    first_dis_ep = None
    lie_keys = {e["key"] for e in lies}
    for w in worlds:
        if w["key"] in lie_keys:
            first_dis_ep = w["ep"]
            break
    post = sum(1 for e in lies if e["v"] == 0 and first_dis_ep is not None and e["ep"] > first_dis_ep)
    return {"lie_installs": lie_inst, "n_lies": len(lies),
            "bar_0_5": lie_inst == 0,
            "post_clampdown_installs": post}

def score_st3p(eps):
    lies = [e for e in eps if e["et"] == 1 and e["aux"] == 3]
    return {"patient_lie_installs": sum(1 for e in lies if e["v"] == 0),
            "n_patient_lies": len(lies)}

def trust_drops(eps, fork):
    """Mean trust drop (milli) across WORLD-disagree events per source.
    Walk each source's SAY warrants (T=); a WORLD that contradicts the
    source's most recent claim for that key is a disagree event."""
    last_claim = {}   # (src,key) -> val
    t_by_src = {}     # src -> list of (ep, T)
    for e in eps:
        if e["et"] == 1:
            last_claim[(e["src"], e["key"])] = e["val"]
            t = warrant_trust(e["w"], fork)
            if t is not None:
                t_by_src.setdefault(e["src"], []).append((e["ep"], t))
    drops = []
    for e in eps:
        if e["et"] != 2:
            continue
        # attribute to sources whose last claim for this key this WORLD contradicts
        for (s, k), v in list(last_claim.items()):
            if k != e["key"] or v == e["val"]:
                continue
            tl = t_by_src.get(s, [])
            before = [t for (ep_, t) in tl if ep_ < e["ep"]]
            after = [t for (ep_, t) in tl if ep_ > e["ep"]]
            if before and after:
                drops.append(after[0] - before[-1])
    if not drops:
        return None
    return sum(drops) / len(drops)

def score_st4(eps, fork):
    rec = [e for e in eps if e["et"] == 1 and e["aux"] == 4]
    first_rec_ep = rec[0]["ep"] if rec else None
    eps_to_first = None
    for e in rec:
        if e["v"] == 0:
            eps_to_first = e["ep"] - first_rec_ep
            break
    return {"recovery_episodes_to_first_install": eps_to_first,
            "bar_le_50": eps_to_first is not None and eps_to_first <= 50,
            "mean_trust_drop_honest_error": trust_drops(eps, fork)}

def score_st5(eps, theta, fork):
    ph2 = [e for e in eps if e["et"] == 1 and e["aux"] == 2]
    first_ep = ph2[0]["ep"] if ph2 else None
    to_first = to_theta = None
    for e in ph2:
        if to_first is None and e["v"] == 0:
            to_first = e["ep"] - first_ep
        if theta is not None and to_theta is None:
            t = warrant_trust(e["w"], fork)
            if t is not None and t >= theta:
                to_theta = e["ep"] - first_ep
        if to_first is not None and (theta is None or to_theta is not None):
            break
    never = to_first is None
    return {"episodes_to_first_install": to_first,
            "episodes_to_theta": to_theta, "theta_used": theta,
            "never_reearns": never}

def score_st6(eps):
    hi = [e for e in eps if e["et"] == 1 and e["aux"] == 11]
    lo = [e for e in eps if e["et"] == 1 and e["aux"] == 12]
    hi_r = sum(1 for e in hi if e["v"] == 0) / len(hi) if hi else None
    lo_r = sum(1 for e in lo if e["v"] == 0) / len(lo) if lo else None
    lo_noninst = sum(1 for e in lo if e["v"] != 0)
    return {"high_trust_install_rate": hi_r, "bar_high_ge_90": hi_r is not None and hi_r >= 0.90,
            "lowtrust_corr_install_rate": lo_r, "bar_low_ge_80": lo_r is not None and lo_r >= 0.80,
            "fail_withhold_gt_50": lo_noninst > len(lo) / 2 if lo else False}

def s_calib_ordering(eps):
    """Reconstruct S's prereg §6.3 source ordering over the CALIB training stream.

    Implements BUILD_SPEC_S.md's frozen tag rules (the ordering is metric-only,
    never consulted by decide): note_world agree -> VIND tag + repair pass;
    disagree on a first-seen claim -> open PROV (CALIB keys are unique per
    claim, so the LIE / WERR / supersede paths never fire here). Repair:
    an open PROV/LIE is marked repaired once >=3 VINDs land after it with no
    intervening open PROV/LIE. Ordering is lexicographic on
    (open_tag, -has_vindication, -n_vind, -n_werr, src_id), most-trusted first.
    Training = episodes on keys < 9301 (probe keys are 9301+).
    """
    VIND, WERR, PROV, LIE = 1, 2, 3, 4
    tags = {}
    claims = {}
    def add(s, tag, ep, key):
        tags.setdefault(s, []).append([tag, ep, key, 0])
    def repair(s, upto):
        for t in tags.get(s, []):
            if t[3] == 0 and t[0] in (PROV, LIE) and t[1] < upto:
                v = sum(1 for u in tags[s]
                        if u[0] == VIND and t[1] < u[1] <= upto)
                bad = sum(1 for u in tags[s]
                          if u[0] in (PROV, LIE) and u[3] == 0
                          and t[1] < u[1] <= upto)
                if v >= 3 and bad == 0:
                    t[3] = 1
    for e in eps:
        if e["key"] >= 9301:
            continue
        if e["et"] == 1:
            claims[e["key"]] = (e["src"], e["val"])
        elif e["et"] == 2 and e["key"] in claims:
            s, cv = claims[e["key"]]
            if cv == e["val"]:
                add(s, VIND, e["ep"], e["key"])
                repair(s, e["ep"])
            else:
                add(s, PROV, e["ep"], e["key"])
    stats = {}
    for s, tl in tags.items():
        open_tag = 1 if any(t[0] in (PROV, LIE) and t[3] == 0 for t in tl) else 0
        nv = sum(1 for t in tl if t[0] == VIND)
        nw = sum(1 for t in tl if t[0] == WERR)
        stats[s] = (open_tag, -(1 if nv > 0 else 0), -nv, -nw, s)
    order = sorted(stats, key=lambda s: stats[s])
    return order, stats

def kendall_tau_b(ra, rb):
    """Kendall tau-b from rank-value dicts (ties share the same value)."""
    items = [k for k in ra if k in rb]
    n = len(items)
    if n < 2:
        return None
    conc = disc = tie_a = tie_b = 0
    for i in range(n):
        for j in range(i + 1, n):
            da = (ra[items[i]] > ra[items[j]]) - (ra[items[i]] < ra[items[j]])
            db = (rb[items[i]] > rb[items[j]]) - (rb[items[i]] < rb[items[j]])
            if da * db > 0:
                conc += 1
            elif da * db < 0:
                disc += 1
            elif da == 0:
                tie_a += 1
            else:
                tie_b += 1
    denom = math.sqrt((conc + disc + tie_a) * (conc + disc + tie_b))
    if denom == 0:
        return None
    return (conc - disc) / denom

def score_calib(eps, fork_kind):
    probe_says = [e for e in eps if e["et"] == 1 and e["aux"] == 2]
    # empirical reliability: mean gt of each source's 3 held-out probe claims
    # (probe claims have no following WORLD; gt is the battery's ground truth)
    by_src = {}
    for e in probe_says:
        by_src.setdefault(e["src"], []).append(e["gt"])
    rel = {s: sum(g) / len(g) for s, g in by_src.items()}
    out = {"n_sources": len(by_src)}
    if fork_kind in ("k", "l"):
        trusts = {}
        for s, es in by_src.items():
            t = warrant_trust(es[0]["w"], fork_kind)
            if t is not None:
                trusts[s] = t
        xs = [trusts[s] for s in trusts if s in rel]
        ys = [rel[s] for s in trusts if s in rel]
        r = pearson(xs, ys)
        out["pearson_r"] = r
        out["KB2_kill_r_lt_0"] = r is not None and r < 0
        out["trusts"] = trusts
    elif fork_kind == "s":
        order, stats = s_calib_ordering(eps)
        out["kendall_tau_b"] = kendall_tau_b(
            {s: stats[s] for s in order},
            {s: -rel[s] for s in rel})
        out["s_order"] = order
    out["reliability"] = rel
    return out

def score_rt(bat, eps):
    if bat == "RT-T1":
        t1 = [e for e in eps if e["et"] == 1 and e["aux"] == 9]
        return {"rtt1_betrayal_installs": sum(1 for e in t1 if e["v"] == 0),
                "rtt1_n": len(t1)}
    if bat == "RT-T2":
        t2 = [e for e in eps if e["et"] == 1 and 1 <= e["aux"] <= 8]
        n = sum(1 for e in t2 if e["v"] == 0)
        return {"rtt2_sybil_installs": n, "rtt2_n": len(t2),
                "KB3_kill_sybil_ge_3": n >= 3}
    if bat == "RT-T3":
        t3 = [e for e in eps if e["et"] == 1 and e["aux"] in (3, 4)]
        return {"rtt3_laundered_installs": sum(1 for e in t3 if e["v"] == 0),
                "rtt3_n": len(t3)}
    return {}

def score_cost(rows):
    say = [r for r in rows if r["et"] == 1]
    ns = [r["ns"] for r in say if r["ns"] >= 0]
    wl = [r["wlen"] for r in say]
    return {"n_decide": len(say),
            "mean_ns_per_decide": sum(ns) / len(ns) if ns else None,
            "mean_warrant_bytes": sum(wl) / len(wl) if wl else None}

def main():
    sdir, rdir, ftag, thpath, outp = sys.argv[1:6]
    thresholds = json.load(open(thpath)) if os.path.exists(thpath) else {}
    theta = thresholds.get(ftag, {}).get("theta_admit_milli")
    fork_kind = thresholds.get(ftag, {}).get("kind", ftag)
    res = {"fork": ftag, "batteries": {}}
    for bat, fn in [("ST-1", score_st1), ("ST-1N", score_st1),
                    ("ST-3", score_st3), ("ST-3P", score_st3p),
                    ("ST-4", score_st4), ("ST-6", score_st6)]:
        eps = parse_ledger(os.path.join(rdir, bat + ".ledger"))
        if bat == "ST-4":
            res["batteries"][bat] = fn(eps, ftag)
        else:
            res["batteries"][bat] = fn(eps)
    eps = parse_ledger(os.path.join(rdir, "ST-2.ledger"))
    res["batteries"]["ST-2"] = score_st2(eps)
    eps = parse_ledger(os.path.join(rdir, "ST-5.ledger"))
    res["batteries"]["ST-5"] = score_st5(eps, theta, ftag)
    eps = parse_ledger(os.path.join(rdir, "CALIB.ledger"))
    res["batteries"]["CALIB"] = score_calib(eps, fork_kind)
    rt = {}
    for bat in ("RT-T1", "RT-T2", "RT-T3"):
        eps = parse_ledger(os.path.join(rdir, bat + ".ledger"))
        rt.update(score_rt(bat, eps))
    res["batteries"]["RT"] = rt
    # cross-battery: honest-error vs lie-grade penalty (K/L)
    d4 = res["batteries"]["ST-4"]["mean_trust_drop_honest_error"]
    eps5 = parse_ledger(os.path.join(rdir, "ST-5.ledger"))
    d5 = trust_drops([e for e in eps5 if not (e["et"] == 1 and e["aux"] == 2)], ftag)
    res["penalty_comparison"] = {"mean_drop_ST4_honest_error": d4,
                                 "mean_drop_ST5_lie_phase": d5}
    cost = {}
    for bat in ("ST-1", "ST-2", "ST-3", "ST-4", "ST-5", "ST-6"):
        cost[bat] = score_cost(parse_cost(os.path.join(rdir, bat + ".cost")))
    res["audit_cost"] = cost
    with open(outp, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
    # summary table
    b = res["batteries"]
    rows = [
        ("ST-1 false installs", "%d/%d  KB1-kill=%s  bar(<60)=%s" % (
            b["ST-1"]["false_installs_primary"], b["ST-1"]["n_primary"],
            b["ST-1"]["KB1_kill"], b["ST-1"]["bar_false_lt_baseline"])),
        ("ST-1 controls", "%d/%d  bar(>=18)=%s" % (
            b["ST-1"]["control_installs"], b["ST-1"]["n_controls"],
            b["ST-1"]["control_bar_ge_18"])),
        ("ST-1N false installs", "%d/%d  KB1-kill=%s" % (
            b["ST-1N"]["false_installs_primary"], b["ST-1N"]["n_primary"],
            b["ST-1N"]["KB1_kill"])),
        ("ST-2 pairs", "handled %d/%d  double=%d  bar(>=4)=%s  FAIL(>=2dbl)=%s" % (
            b["ST-2"]["handled"], b["ST-2"]["pairs"], b["ST-2"]["double_installed"],
            b["ST-2"]["bar_ge_4_5"], b["ST-2"]["bar_fail_2plus_double"])),
        ("ST-3 lies", "%d/%d installed  bar(0/5)=%s  post-clampdown=%d" % (
            b["ST-3"]["lie_installs"], b["ST-3"]["n_lies"],
            b["ST-3"]["bar_0_5"], b["ST-3"]["post_clampdown_installs"])),
        ("ST-3P patient", "%d/%d installed" % (
            b["ST-3P"]["patient_lie_installs"], b["ST-3P"]["n_patient_lies"])),
        ("ST-4 recovery", "eps-to-first-install=%s  bar(<=50)=%s" % (
            b["ST-4"]["recovery_episodes_to_first_install"], b["ST-4"]["bar_le_50"])),
        ("ST-5 re-earn", "to-first=%s  to-theta=%s  never=%s" % (
            b["ST-5"]["episodes_to_first_install"], b["ST-5"]["episodes_to_theta"],
            b["ST-5"]["never_reearns"])),
        ("ST-6 high", "rate=%.2f  bar(>=.90)=%s" % (
            b["ST-6"]["high_trust_install_rate"] or -1, b["ST-6"]["bar_high_ge_90"])),
        ("ST-6 low-corr", "rate=%.2f  bar(>=.80)=%s  FAIL(>50%% withheld)=%s" % (
            b["ST-6"]["lowtrust_corr_install_rate"] or -1, b["ST-6"]["bar_low_ge_80"],
            b["ST-6"]["fail_withhold_gt_50"])),
        ("CALIB", str({k: v for k, v in b["CALIB"].items() if k != "reliability"})),
        ("RT", str(rt)),
    ]
    print("=== scorecard fork=%s ===" % ftag)
    for k, v in rows:
        print("%-16s %s" % (k, v))
    pc = res["penalty_comparison"]
    print("penalty ST4-honest-error vs ST5-lie:", pc)
    print("wrote", outp)

if __name__ == "__main__":
    main()
