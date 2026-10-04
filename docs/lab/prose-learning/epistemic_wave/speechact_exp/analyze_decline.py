#!/usr/bin/env python3
"""Analyze decline-investigation scored evidence: per-family tables + McNemar."""
import os, math, sys

EV = os.path.expanduser("~/workspace/tnn-lab/prose-learning/epistemic_wave/speechact_exp/scored_evidence")

FAMS = [
    ("absurd",  "W001", "W010"),
    ("sarcasm", "W023", "W032"),
    ("hypoth",  "W045", "W054"),
    ("analogy", "W067", "W076"),
    ("countf",  "W109", "W118"),
    ("poetry",  "W089", "W098"),
    ("implic",  "W131", "W140"),
]

def fam_of(iid):
    for name, lo, hi in FAMS:
        if lo <= iid <= hi:
            return name
    return "other"

def load(name):
    """rep1 verdicts -> {id: verdict}"""
    d = {}
    with open(os.path.join(EV, f"dec_{name}_rep1.txt")) as f:
        for line in f:
            line = line.strip()
            if "|" in line and not line.startswith("SUMMARY"):
                iid, v = line.split("|", 1)
                d[iid] = v
    return d

def fam_scores(name):
    d = load(name)
    s = {n: 0 for n, _, _ in FAMS}
    t = {n: 0 for n, _, _ in FAMS}
    for iid, v in d.items():
        fn = fam_of(iid)
        if fn in s:
            t[fn] += 1
            if v == "WITHHOLD":
                s[fn] += 1
    return s, t

def mcnemar(a_name, b_name):
    """paired test on same items: a->b. returns (gained, lost, p_two_sided)."""
    da, db = load(a_name), load(b_name)
    g = l = 0
    for iid in da:
        if iid in db:
            ca = 1 if da[iid] == "WITHHOLD" else 0
            cb = 1 if db[iid] == "WITHHOLD" else 0
            if cb > ca: g += 1
            elif cb < ca: l += 1
    n = g + l
    if n == 0:
        return g, l, 1.0
    # exact two-sided binomial
    p = 0.0
    from math import comb
    for k in range(n + 1):
        if abs(k - n / 2) >= abs(min(g, l) - n / 2) - 1e-9:
            p += comb(n, k) / 2**n
    return g, l, min(p, 1.0)

def table(prefix, rungs):
    names = [n for n, _, _ in FAMS]
    print(f"--- {prefix} ---")
    print("rung | " + " | ".join(f"{n:>6}" for n in names) + " | total")
    for rg in rungs:
        s, t = fam_scores(f"{prefix}_r{rg}")
        tot = sum(s.values())
        print(f"r{rg:>3} | " + " | ".join(f"{s[n]:>2}/{t[n]:<2}" for n in names) + f" | {tot}/70")

if __name__ == "__main__":
    rungs = [0, 1, 2, 4, 8, 16, 32]
    for p in ["ord_diverse", "ord_redundant", "ord_proto", "ord_outlier"]:
        table(p, rungs)
        print()
    print("McNemar r2->r32 (decline) per ordering:")
    for p in ["ord_diverse", "ord_redundant", "ord_proto", "ord_outlier"]:
        g, l, pv = mcnemar(f"{p}_r2", f"{p}_r32")
        print(f"  {p}: gained={g} lost={l} p={pv:.4g}")
    print("McNemar r1->r2 (rise) per ordering:")
    for p in ["ord_diverse", "ord_redundant", "ord_proto", "ord_outlier"]:
        g, l, pv = mcnemar(f"{p}_r1", f"{p}_r2")
        print(f"  {p}: gained={g} lost={l} p={pv:.4g}")
    print()
    print("=== bar / front-end variants (original order) ===")
    for p in ["bar_cnt", "bar_b2", "bar_b3", "fe_f2", "fe_f3"]:
        table(p, rungs)
        print()
    print("McNemar r2->r32 for variants:")
    for p in ["bar_cnt", "bar_b2", "bar_b3", "fe_f2", "fe_f3"]:
        g, l, pv = mcnemar(f"{p}_r2", f"{p}_r32")
        s2, _ = fam_scores(f"{p}_r2")
        s32, _ = fam_scores(f"{p}_r32")
        print(f"  {p}: {sum(s2.values())}->{sum(s32.values())} gained={g} lost={l} p={pv:.4g} | implic {s2['implic']}->{s32['implic']}")
    print()
    print("Implicature column across rungs:")
    for p in ["bar_cnt", "bar_b2", "bar_b3", "fe_f2", "fe_f3"]:
        row = []
        for rg in rungs:
            s, _ = fam_scores(f"{p}_r{rg}")
            row.append(str(s["implic"]))
        print(f"  {p}: " + "-".join(row))
    print()
    print("=== combined corrected candidate: diverse order + count rule ===")
    table("cntdiv", rungs)
    print("McNemar adjacent rungs (cntdiv monotonicity):")
    prev = None
    for rg in rungs:
        if prev is not None:
            g, l, pv = mcnemar(f"cntdiv_r{prev}", f"cntdiv_r{rg}")
            print(f"  r{prev}->r{rg}: gained={g} lost={l} p={pv:.4g}")
        prev = rg
    print("McNemar adjacent rungs (bar_cnt, check r16 dip):")
    prev = None
    for rg in rungs:
        if prev is not None:
            g, l, pv = mcnemar(f"bar_cnt_r{prev}", f"bar_cnt_r{rg}")
            print(f"  r{prev}->r{rg}: gained={g} lost={l} p={pv:.4g}")
        prev = rg
