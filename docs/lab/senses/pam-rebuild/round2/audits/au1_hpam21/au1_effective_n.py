#!/usr/bin/env python3
"""AU-1: H-PAM-21 evidence-independence audit of the F5 3-crop quorum.

Reconstructs per-crop reproduction votes for the 300 NEAR percepts of the
frozen F5 full-mechanism battery from the FROZEN, SHA-verified inputs:

  fixtures_ledger.txt  SHA 0c5e2c0db6576bd37ff53513fb1361cdf7936d4826274bdcc9742be2261233a0
  exemplars.tsv        SHA 13f4ca47429bc0bb8788d60406593766e48f6f064cb7538adf28be16a289200e

using the EXACT decision rules of the committed mechanism
(f5_full.zag, SHA c825d65c52da9b406a929bb6a5a4b56a2385f9bdadbea26b03aac3fd4f6e5239):

  predicate  : BLOCKED iff exemplar with same stem, |dconf|<=150, |dmeas|<=2000
  crop votes : v_k = 1 iff exemplar with same stem, |dconf|<=130, |dmeas|<=950
               at crops (conf-10,meas-200), (conf,meas), (conf+10,meas+200)
  quorum     : WITHHOLD iff v1+v2+v3 >= 2, else CONFIRM_INSTALL

VALIDATION GATE: the reconstructed (blocked, quorum-verdict) for every one of
the 300 NEAR percepts is compared against the committed run log run1.out
(SHA d287b4ee67ca546ff4433fe245ad36fbd19f577b432939a15ef0d9ed13b78327).
The audit numbers are only emitted if all 300 match exactly; otherwise the
script exits nonzero with a mismatch report.

STATISTICS (110 blocked NEAR percepts, the quorum's decision set):
  - per-crop marginals, 3-bit vote-pattern distribution
  - vote-conditional agreement: P(vj=1|vi=1), P(vj=0|vi=0) for all 6 pairs
  - mutual information per pair (bits) + normalized MI I/min(Hx,Hy)
  - Pearson correlation per pair, mean rho
  - effective independent sample size: n_eff = 3 / (1 + 2*rho_mean)
    (Kish's ICC form; rho_mean=1 -> 1.0, rho_mean=0 -> 3.0)
  - quorum-vs-single-crop agreement fractions

Deterministic: no RNG, fixed order, fixed float formatting. Byte-identical
reruns: run twice, diff the output files.

Usage: au1_effective_n.py <fixtures_ledger.txt> <exemplars.tsv> <run1.out> <out_report.txt> <out_votes.tsv>
"""
import sys, math

TC, TM = 130, 950          # confirmation core window (frozen prereg §4)
PB_C, PB_M = 150, 2000     # block predicate window (frozen, unchanged)

def stem_of(s):
    if s.startswith("rt4_"):
        s = s[4:]
    cut = s.find("-")
    return s if cut < 0 else s[:cut]

def block_ok(stem, conf, meas, ex):
    for es, ec, em in ex:
        if es == stem and abs(conf - ec) <= PB_C and abs(meas - em) <= PB_M:
            return True
    return False

def core_hit(stem, conf, meas, ex):
    for es, ec, em in ex:
        if es == stem and abs(conf - ec) <= TC and abs(meas - em) <= TM:
            return True
    return False

def mi_bits(xs, ys):
    # mutual information in bits of two binary sequences
    n = len(xs)
    p00 = p01 = p10 = p11 = 0
    for x, y in zip(xs, ys):
        if x == 0 and y == 0: p00 += 1
        elif x == 0 and y == 1: p01 += 1
        elif x == 1 and y == 0: p10 += 1
        else: p11 += 1
    def H(ps):
        h = 0.0
        for p in ps:
            if p > 0: h -= p * math.log(p, 2)
        return h
    px0, px1 = (p00 + p01) / n, (p10 + p11) / n
    py0, py1 = (p00 + p10) / n, (p01 + p11) / n
    i = H([px0, px1]) + H([py0, py1]) - H([q / n for q in (p00, p01, p10, p11)])
    return i, min(H([px0, px1]), H([py0, py1]))

def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    vx = sum((x - mx) ** 2 for x in xs) / n
    vy = sum((y - my) ** 2 for y in ys) / n
    if vx == 0 or vy == 0:
        return float("nan")
    return cov / math.sqrt(vx * vy)

def main():
    led_path, ex_path, run_path, rep_path, votes_path = sys.argv[1:6]

    # ---- exemplars (skip header) ----
    ex = []
    with open(ex_path) as f:
        lines = f.read().splitlines()
    for ln in lines[1:]:
        if not ln.strip():
            continue
        f0, f1, f2, f3 = ln.split("\t")[:4]
        ex.append((stem_of(f1), int(f2), int(f3)))

    # ---- NEAR percepts from the frozen ledger ----
    percepts = []  # (name, conf, meas)
    with open(led_path) as f:
        for ln in f:
            flds = ln.rstrip("\n").split("|")
            if len(flds) == 18 and flds[17] == "SET=NEAR":
                percepts.append((flds[4], int(flds[8]), int(flds[10])))
    assert len(percepts) == 300, f"expected 300 NEAR, got {len(percepts)}"

    # ---- reconstruct votes ----
    rec = []  # (name, blocked, v1, v2, v3, verdict)
    for name, conf, meas in percepts:
        stem = stem_of(name)
        b = block_ok(stem, conf, meas, ex)
        v1 = core_hit(stem, conf - 10, meas - 200, ex)
        v2 = core_hit(stem, conf, meas, ex)
        v3 = core_hit(stem, conf + 10, meas + 200, ex)
        if b:
            verdict = "WITHHOLD" if (v1 + v2 + v3) >= 2 else "CONFIRM_INSTALL"
        else:
            verdict = "-"
        rec.append((name, b, v1, v2, v3, verdict))

    # ---- validation gate against the committed run log ----
    with open(run_path) as f:
        run_lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    near_lines = [ln for ln in run_lines
                if len(ln.split("\t")) >= 3 and ln.split("\t")[2] == "NEAR"]
    assert len(near_lines) == 300, f"expected 300 NEAR log lines, got {len(near_lines)}"
    mism = []
    for (name, b, v1, v2, v3, verdict), ln in zip(rec, near_lines):
        t = ln.split("\t")
        lg_name, lg_blk, lg_ver = t[1], t[3], t[5]
        ok = (lg_name == name and
              (lg_blk == "BLOCKED") == b and
              lg_ver == verdict)
        if not ok:
            mism.append((name, b, verdict, lg_blk, lg_ver))
    if mism:
        sys.stderr.write(f"VALIDATION FAILED: {len(mism)} mismatches vs run log\n")
        for m in mism[:10]:
            sys.stderr.write(f"  {m}\n")
        sys.exit(11)

    # ---- audit panel: the 110 blocked NEAR percepts ----
    panel = [r for r in rec if r[1]]
    assert len(panel) == 110, f"expected 110 blocked, got {len(panel)}"
    vs = [(int(r[2]), int(r[3]), int(r[4])) for r in panel]
    c1 = [v[0] for v in vs]; c2 = [v[1] for v in vs]; c3 = [v[2] for v in vs]
    cols = [c1, c2, c3]

    def p_agree(a, b):
        # P(b=1|a=1), P(b=0|a=0)
        n11 = sum(1 for x, y in zip(a, b) if x == 1 and y == 1)
        n1 = sum(a)
        n00 = sum(1 for x, y in zip(a, b) if x == 0 and y == 0)
        n0 = len(a) - n1
        return (n11 / n1 if n1 else float("nan"),
                n00 / n0 if n0 else float("nan"))

    pats = {}
    for v in vs:
        pats[v] = pats.get(v, 0) + 1

    rhos = []
    mis = []
    agrees = []
    for i in range(3):
        for j in range(i + 1, 3):
            rhos.append(pearson(cols[i], cols[j]))
            i_xy, hmin = mi_bits(cols[i], cols[j])
            mis.append((i_xy, i_xy / hmin if hmin > 0 else float("nan")))
            a1, a0 = p_agree(cols[i], cols[j])
            b1, b0 = p_agree(cols[j], cols[i])
            agrees.append(((i + 1, j + 1, a1, a0), (j + 1, i + 1, b1, b0)))

    rho_mean = sum(rhos) / len(rhos)
    n_eff = 3.0 / (1.0 + 2.0 * rho_mean)

    # quorum vs single crops
    q = [1 if sum(v) >= 2 else 0 for v in vs]
    qv1 = sum(1 for v, qq in zip(vs, q) if (v[0]) == qq)
    qv2 = sum(1 for v, qq in zip(vs, q) if (v[1]) == qq)
    qv3 = sum(1 for v, qq in zip(vs, q) if (v[2]) == qq)
    unan = sum(1 for v in vs if v[0] == v[1] == v[2])
    split = 110 - unan

    def f(x):
        if isinstance(x, float) and math.isnan(x):
            return "n/a"
        return f"{x:.6f}"

    L = []
    L.append("AU-1 H-PAM-21 EVIDENCE-INDEPENDENCE AUDIT")
    L.append("frozen inputs: fixtures_ledger.txt (300 NEAR), exemplars.tsv (6 rows)")
    L.append("frozen log: run1.out (SHA d287b4ee67ca546ff4433fe245ad36fbd19f577b432939a15ef0d9ed13b78327)")
    L.append(f"validation: reconstructed (blocked,quorum) matches run log on 300/300 NEAR percepts: PASS")
    L.append(f"panel: {len(panel)} blocked NEAR percepts (quorum engaged)")
    L.append("")
    L.append("marginals P(vote=1): crop1=%s crop2=%s crop3=%s" %
             (f(sum(c1)/110), f(sum(c2)/110), f(sum(c3)/110)))
    L.append("vote-pattern distribution (v1v2v3):")
    for k in sorted(pats):
        L.append(f"  {k[0]}{k[1]}{k[2]}: {pats[k]}")
    L.append(f"unanimous triples: {unan}/110  split triples: {split}/110")
    L.append("")
    L.append("vote-conditional agreement P(col=1|row=1) / P(col=0|row=0):")
    for (a, b, a1, a0), (c, d, b1, b0) in agrees:
        L.append(f"  P(c{b}=1|c{a}=1)={f(a1)}  P(c{b}=0|c{a}=0)={f(a0)}")
        L.append(f"  P(c{d}=1|c{c}=1)={f(b1)}  P(c{d}=0|c{c}=0)={f(b0)}")
    L.append("")
    L.append("mutual information (bits) and normalized I/min(Hx,Hy):")
    pairs = [(1, 2), (1, 3), (2, 3)]
    for (i, j), (ival, nval) in zip(pairs, mis):
        L.append(f"  crops {i}-{j}: I={f(ival)} bits  I/min(H)={f(nval)}")
    L.append("")
    L.append("Pearson correlation per crop pair:")
    for (i, j), r in zip(pairs, rhos):
        L.append(f"  crops {i}-{j}: rho={f(r)}")
    L.append(f"mean pairwise rho = {f(rho_mean)}")
    L.append(f"EFFECTIVE INDEPENDENT SAMPLE SIZE n_eff = 3/(1+2*rho) = {f(n_eff)}")
    L.append("")
    L.append("quorum-vs-single-crop agreement (of 110):")
    L.append(f"  quorum == crop1 alone: {qv1}/110")
    L.append(f"  quorum == crop2 (center) alone: {qv2}/110")
    L.append(f"  quorum == crop3 alone: {qv3}/110")
    L.append("")
    with open(rep_path, "w") as f:
        f.write("\n".join(L) + "\n")
    with open(votes_path, "w") as f:
        f.write("trial\tname\tblocked\tv1\tv2\tv3\tquorum_verdict\n")
        for k, (name, b, v1, v2, v3, verdict) in enumerate(rec, 1):
            f.write(f"{k}\t{name}\t{1 if b else 0}\t{int(v1)}\t{int(v2)}\t{int(v3)}\t{verdict}\n")
    print(f"validation PASS: 300/300 NEAR match run log")
    print(f"n_eff = {n_eff:.6f} (mean rho = {rho_mean:.6f})")
    print(f"unanimous {unan}/110, split {split}/110")

if __name__ == "__main__":
    main()
