#!/usr/bin/env python3
"""score_d1.py — D1 stack battery scorer.

Compares Zag battery output against EXPECT_D1.tsv (frozen, from gen_d1.py's
hand-verified Python mirror) and evaluates the frozen kill bars.

Usage: score_d1.py <run1_prefix> <run2_prefix> <run3_prefix>
  Each prefix is a directory containing <stream>.out files (one per stream).
"""
import os, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))

def load_expect():
    exp = {}
    for line in open(os.path.join(HERE, "EXPECT_D1.tsv")):
        if line.startswith("leg\ttrial_idx"):
            continue
        leg, ti, disp, inst = line.strip().split("\t")
        exp[(leg, int(ti))] = (disp, int(inst))
    return exp

def load_run(prefix):
    out = {}
    for fn in os.listdir(prefix):
        if not fn.endswith(".out"):
            continue
        leg = fn[:-4]
        for line in open(os.path.join(prefix, fn)):
            # stream|trial_idx|seq|disp|install|detail
            f = line.rstrip("\n").split("|")
            out[(f[0], int(f[1]))] = (f[3], int(f[4]), f[5] if len(f) > 5 else "")
    return out

def sha_of_run(prefix):
    h = hashlib.sha256()
    for fn in sorted(os.listdir(prefix)):
        if fn.endswith(".out"):
            h.update(open(os.path.join(prefix, fn), "rb").read())
    return h.hexdigest()

def main():
    p1, p2, p3 = sys.argv[1], sys.argv[2], sys.argv[3]
    exp = load_expect()
    r1, r2, r3 = load_run(p1), load_run(p2), load_run(p3)
    # determinism: byte-identical runs
    s1, s2, s3 = sha_of_run(p1), sha_of_run(p2), sha_of_run(p3)
    print("run sha256:", s1)
    print("run sha256:", s2)
    print("run sha256:", s3)
    det_ok = (s1 == s2 == s3)
    print("byte-identical x3:", "PASS" if det_ok else "FAIL")
    # per-trial match vs EXPECT
    mism = []
    for k, (edisp, einst) in exp.items():
        got = r1.get(k)
        if got is None:
            mism.append((k, "missing", (edisp, einst)))
        elif got[0] != edisp or got[1] != einst:
            mism.append((k, got, (edisp, einst)))
    # also check for extra trials
    for k in r1:
        if k not in exp:
            mism.append((k, r1[k], "unexpected"))
    print("trials expected:", len(exp), "trials in run:", len(r1))
    print("mismatches vs EXPECT:", len(mism))
    for m in mism[:20]:
        print("  ", m)
    # kill bars
    # KB-D1a: any false install. Need truth: from streams via gen_d1.
    import gen_d1 as G
    false_installs = []
    for (leg, ti), (disp, inst, detail) in r1.items():
        if inst:
            t = G.streams[leg][ti]
            if t["judgment"] != t["truth"]:
                false_installs.append((leg, ti, t["seq"], t["judgment"], t["truth"], detail))
    print("KB-D1a false installs:", len(false_installs))
    for fi in false_installs:
        print("  ", fi)
    # KB-D1b: true retention on leg1 (34 true candidates)
    leg1 = G.streams["leg1"]
    n_true = sum(1 for t in leg1 if t["judgment"] == t["truth"])
    n_ret = sum(1 for ti, t in enumerate(leg1)
                if t["judgment"] == t["truth"] and r1[("leg1", ti)][1] == 1)
    print("KB-D1b true retention: %d/%d" % (n_ret, n_true))
    # honest F5-less report: the 8 TMB-5 false accepts
    print("8 TMB-5 false accepts (no F5):")
    for ti, t in enumerate(leg1):
        if t["judgment"] != t["truth"] and "TMB-5" in t["fixture"]:
            d, inst, detail = r1[("leg1", ti)]
            print("  idx %2d seq %3d disp %s install %d %s"
                  % (ti, t["seq"], d, inst, detail))
    # verdict
    kb_a = len(false_installs) == 0
    kb_b = n_ret >= 26
    print("KB-D1a (0 false installs):", "PASS" if kb_a else "FAIL -> KILL")
    print("KB-D1b (>=26/34 retained):", "PASS" if kb_b else "FAIL -> KILL")
    if det_ok and len(mism) == 0 and kb_a and kb_b:
        print("VERDICT: SURVIVE")
    else:
        print("VERDICT: KILL")

if __name__ == "__main__":
    main()
